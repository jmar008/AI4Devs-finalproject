from rest_framework import serializers
from .models import ChatConversation, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer para mensajes de chat
    """
    class Meta:
        model = ChatMessage
        fields = [
            'id',
            'role',
            'content',
            'created_at',
            'tokens_used',
            'model_used',
        ]
        read_only_fields = ['id', 'created_at', 'tokens_used', 'model_used']


class ChatConversationSerializer(serializers.ModelSerializer):
    """
    Serializer para conversaciones de chat
    """
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatConversation
        fields = [
            'id',
            'title',
            'created_at',
            'updated_at',
            'is_active',
            'messages',
            'message_count',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()


class ChatConversationListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar conversaciones
    """
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatConversation
        fields = [
            'id',
            'title',
            'created_at',
            'updated_at',
            'is_active',
            'message_count',
            'last_message',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return {
                'content': last_msg.content[:100],
                'created_at': last_msg.created_at,
                'role': last_msg.role,
            }
        return None


class SendMessageSerializer(serializers.Serializer):
    """
    Serializer para enviar un mensaje al chat
    """
    message = serializers.CharField(
        required=True,
        max_length=2000,
        help_text="Mensaje del usuario"
    )
    conversation_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="ID de la conversación existente (opcional, se crea una nueva si no se proporciona)"
    )


class ChatResponseSerializer(serializers.Serializer):
    """
    Serializer para la respuesta del chat
    """
    conversation_id = serializers.IntegerField()
    user_message = ChatMessageSerializer()
    assistant_message = ChatMessageSerializer()
    tokens_used = serializers.IntegerField()
