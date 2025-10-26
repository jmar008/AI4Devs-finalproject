"""
Servicio para interactuar con la API de DeepSeek
"""
from openai import OpenAI
from django.conf import settings
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DeepSeekService:
    """
    Servicio que maneja la comunicación con DeepSeek AI
    """

    def __init__(self):
        """
        Inicializa el cliente de OpenAI configurado para DeepSeek
        """
        if not settings.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY no está configurada en settings")

        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_API_BASE
        )
        self.model = settings.DEEPSEEK_MODEL

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> Dict[str, Any]:
        """
        Envía mensajes a DeepSeek y obtiene la respuesta

        Args:
            messages: Lista de mensajes en formato [{"role": "user", "content": "..."}]
            temperature: Creatividad de la respuesta (0-2)
            max_tokens: Máximo número de tokens en la respuesta

        Returns:
            Dict con la respuesta y metadatos
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )

            # Extraer la respuesta
            assistant_message = response.choices[0].message.content

            # Metadatos
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }

            logger.info(f"DeepSeek API call successful. Tokens used: {usage['total_tokens']}")

            return {
                'content': assistant_message,
                'usage': usage,
                'model': response.model,
                'finish_reason': response.choices[0].finish_reason,
            }

        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {str(e)}")
            raise

    def create_system_message(self, context: str) -> Dict[str, str]:
        """
        Crea el mensaje de sistema con el contexto del stock
        """
        system_prompt = f"""Eres un asistente inteligente para un sistema de gestión de concesionarios de vehículos llamado DealaAI.

Tu función es ayudar a los usuarios a consultar información sobre el stock de vehículos disponibles.

REGLAS:
1. Responde siempre en español de forma clara y profesional
2. Utiliza los datos proporcionados para dar respuestas precisas
3. Si no tienes información suficiente, pregunta al usuario por más detalles
4. Formatea números de precio con el símbolo € (ejemplo: 25.000 €)
5. Sé conciso pero informativo
6. Cuando sugieras vehículos, menciona marca, modelo, precio y características clave

{context}

Recuerda: Solo tienes información sobre el stock actual. No puedes realizar compras, reservas o modificaciones, solo consultas e información.
"""
        return {"role": "system", "content": system_prompt}

    def prepare_messages(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        context: str
    ) -> List[Dict[str, str]]:
        """
        Prepara todos los mensajes para enviar a DeepSeek

        Args:
            user_message: El mensaje actual del usuario
            conversation_history: Historial de la conversación
            context: Contexto del stock generado por StockQueryService

        Returns:
            Lista de mensajes formateada para la API
        """
        messages = []

        # 1. Mensaje de sistema con contexto
        messages.append(self.create_system_message(context))

        # 2. Historial de conversación (últimos 10 mensajes para no exceder límites)
        recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        messages.extend(recent_history)

        # 3. Mensaje actual del usuario
        messages.append({"role": "user", "content": user_message})

        return messages
