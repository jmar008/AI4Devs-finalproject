from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
import logging

from .models import ChatConversation, ChatMessage
from .serializers import (
    ChatConversationSerializer,
    ChatConversationListSerializer,
    SendMessageSerializer,
    ChatResponseSerializer,
    ChatMessageSerializer,
)
from .services import StockQueryService
from .deepseek_service import DeepSeekService

logger = logging.getLogger(__name__)


class ChatViewSet(viewsets.ViewSet):
    """
    ViewSet para manejar operaciones del chat con IA
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='send')
    def send_message(self, request):
        """
        Envía un mensaje al chat y obtiene respuesta de la IA

        POST /api/chat/send/
        Body: {
            "message": "¿Cuántos coches tenemos?",
            "conversation_id": 1  // Opcional
        }
        """
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_message_text = serializer.validated_data['message']
        conversation_id = serializer.validated_data.get('conversation_id')

        try:
            with transaction.atomic():
                # 1. Obtener o crear conversación
                if conversation_id:
                    try:
                        conversation = ChatConversation.objects.get(
                            id=conversation_id,
                            user=request.user,
                            is_active=True
                        )
                    except ChatConversation.DoesNotExist:
                        return Response(
                            {'error': 'Conversación no encontrada'},
                            status=status.HTTP_404_NOT_FOUND
                        )
                else:
                    # Crear nueva conversación
                    conversation = ChatConversation.objects.create(
                        user=request.user,
                        title=user_message_text[:50] + ('...' if len(user_message_text) > 50 else '')
                    )

                # 2. Guardar mensaje del usuario
                user_message = ChatMessage.objects.create(
                    conversation=conversation,
                    role='user',
                    content=user_message_text
                )

                # 3. Obtener historial de la conversación
                previous_messages = ChatMessage.objects.filter(
                    conversation=conversation
                ).exclude(
                    id=user_message.id
                ).order_by('created_at')

                conversation_history = [
                    {
                        'role': msg.role,
                        'content': msg.content
                    }
                    for msg in previous_messages
                ]

                # 4. Obtener contexto del stock
                stock_context = StockQueryService.get_context_for_ai()

                # 5. Llamar a DeepSeek
                deepseek = DeepSeekService()
                messages = deepseek.prepare_messages(
                    user_message=user_message_text,
                    conversation_history=conversation_history,
                    context=stock_context
                )

                ai_response = deepseek.chat(messages=messages)

                # 6. Guardar respuesta de la IA
                assistant_message = ChatMessage.objects.create(
                    conversation=conversation,
                    role='assistant',
                    content=ai_response['content'],
                    tokens_used=ai_response['usage']['total_tokens'],
                    model_used=ai_response['model']
                )

                # 7. Preparar respuesta
                response_data = {
                    'conversation_id': conversation.id,
                    'user_message': ChatMessageSerializer(user_message).data,
                    'assistant_message': ChatMessageSerializer(assistant_message).data,
                    'tokens_used': ai_response['usage']['total_tokens'],
                }

                return Response(
                    response_data,
                    status=status.HTTP_200_OK
                )

        except ValueError as e:
            logger.error(f"Configuration error: {str(e)}")
            return Response(
                {'error': 'El servicio de IA no está configurado correctamente. Contacta al administrador.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            error_str = str(e)
            logger.error(f"Error in chat: {error_str}", exc_info=True)

            # Mensaje más específico para errores de autenticación
            if '401' in error_str or 'User not found' in error_str:
                error_message = 'La API key de OpenRouter es inválida o ha expirado. Contacta al administrador para obtener una nueva key en https://openrouter.ai/'
            elif '404' in error_str:
                error_message = 'El modelo de IA no está disponible. Intenta de nuevo en unos minutos.'
            else:
                error_message = 'Error al procesar el mensaje. Intenta de nuevo.'

            return Response(
                {'error': error_message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='conversations')
    def list_conversations(self, request):
        """
        Lista todas las conversaciones del usuario

        GET /api/chat/conversations/
        """
        conversations = ChatConversation.objects.filter(
            user=request.user,
            is_active=True
        ).order_by('-updated_at')

        serializer = ChatConversationListSerializer(conversations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='conversation/(?P<conversation_id>[^/.]+)')
    def get_conversation(self, request, conversation_id=None):
        """
        Obtiene una conversación específica con todos sus mensajes

        GET /api/chat/conversation/{id}/
        """
        try:
            conversation = ChatConversation.objects.get(
                id=conversation_id,
                user=request.user,
                is_active=True
            )
        except ChatConversation.DoesNotExist:
            return Response(
                {'error': 'Conversación no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChatConversationSerializer(conversation)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='conversation/(?P<conversation_id>[^/.]+)/delete')
    def delete_conversation(self, request, conversation_id=None):
        """
        Elimina (desactiva) una conversación

        DELETE /api/chat/conversation/{id}/delete/
        """
        try:
            conversation = ChatConversation.objects.get(
                id=conversation_id,
                user=request.user,
                is_active=True
            )
            conversation.is_active = False
            conversation.save()
            return Response(
                {'message': 'Conversación eliminada'},
                status=status.HTTP_200_OK
            )
        except ChatConversation.DoesNotExist:
            return Response(
                {'error': 'Conversación no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], url_path='clear')
    def clear_all(self, request):
        """
        Desactiva todas las conversaciones del usuario

        POST /api/chat/clear/
        """
        ChatConversation.objects.filter(
            user=request.user,
            is_active=True
        ).update(is_active=False)

        return Response(
            {'message': 'Todas las conversaciones han sido limpiadas'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='stock-summary')
    def stock_summary(self, request):
        """
        Obtiene un resumen del stock (para debugging o info directa)

        GET /api/chat/stock-summary/
        """
        summary = StockQueryService.get_stock_summary()
        brands = StockQueryService.get_brands_summary()

        return Response({
            'summary': summary,
            'top_brands': brands,
        })
