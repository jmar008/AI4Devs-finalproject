"""
Servicio para interactuar con la API de DeepSeek via OpenRouter
"""
from openai import OpenAI
from django.conf import settings
from typing import List, Dict, Any
import logging
import httpx

logger = logging.getLogger(__name__)


class DeepSeekService:
    """
    Servicio que maneja la comunicación con DeepSeek AI via OpenRouter
    """

    def __init__(self):
        """
        Inicializa el cliente de OpenAI configurado para OpenRouter
        """
        if not settings.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY no está configurada en settings")

        # Headers específicos de OpenRouter
        default_headers = {
            "HTTP-Referer": "https://dealaai.com",  # Tu sitio web
            "X-Title": "DealaAI Chat",  # Nombre de tu app
        }

        # Crear cliente httpx personalizado para manejar Zscaler y proxies corporativos
        http_client = httpx.Client(
            verify=False,  # Desactivar verificación SSL para Zscaler
            timeout=60.0,  # Timeout de 60 segundos
            headers=default_headers,
        )

        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_API_BASE,
            http_client=http_client,  # Usar cliente personalizado
            default_headers=default_headers,  # Headers para OpenRouter
        )
        self.model = settings.DEEPSEEK_MODEL

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> Dict[str, Any]:
        """
        Envía mensajes a OpenRouter y obtiene la respuesta
        Implementa fallback automático si el modelo principal tiene rate limit

        Args:
            messages: Lista de mensajes en formato [{"role": "user", "content": "..."}]
            temperature: Creatividad de la respuesta (0-2)
            max_tokens: Máximo número de tokens en la respuesta

        Returns:
            Dict con la respuesta y metadatos
        """
        # Lista de modelos a probar (principal + fallbacks)
        models_to_try = [self.model]
        if hasattr(settings, 'DEEPSEEK_FALLBACK_MODELS'):
            models_to_try.extend(settings.DEEPSEEK_FALLBACK_MODELS)

        last_error = None

        for model in models_to_try:
            try:
                logger.info(f"Intentando con modelo: {model}")

                # Extra params para OpenRouter - permite usar modelos gratuitos
                extra_body = {
                    "provider": {
                        "allow_fallbacks": True,
                        "data_collection": "allow"  # Permite uso de modelos gratuitos
                    }
                }

                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=False,
                    extra_body=extra_body  # Parámetros adicionales para OpenRouter
                )

                # Extraer la respuesta
                assistant_message = response.choices[0].message.content

                # Metadatos
                usage = {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens,
                }

                logger.info(f"OpenRouter API call successful. Model: {response.model}, Tokens used: {usage['total_tokens']}")

                return {
                    'content': assistant_message,
                    'usage': usage,
                    'model': response.model,
                    'finish_reason': response.choices[0].finish_reason,
                }

            except Exception as e:
                error_str = str(e)
                last_error = e

                # Si es rate limit (429) o modelo no disponible (404), intentar con el siguiente modelo
                if '429' in error_str or 'rate' in error_str.lower():
                    logger.warning(f"⚠️  Rate limit con {model}, probando siguiente modelo...")
                    continue
                elif '404' in error_str or 'not found' in error_str.lower():
                    logger.warning(f"⚠️  Modelo {model} no disponible (404), probando siguiente modelo...")
                    continue
                else:
                    # Si es otro tipo de error, lanzar inmediatamente
                    logger.error(f"❌ Error calling OpenRouter API with {model}: {error_str}")
                    raise

        # Si llegamos aquí, todos los modelos fallaron
        logger.error(f"❌ Todos los modelos fallaron. Último error: {str(last_error)}")
        raise last_error

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

EJEMPLOS DE PREGUNTAS QUE PUEDES RESPONDER:
- "¿Cuántos coches hay en total en el stock?"
- "¿Cuántos Mercedes tenemos?"
- "¿Cuántos BMW hay disponibles?"
- "¿Qué coches tenemos de Toyota?"
- "Búscame coches de menos de 15.000€"
- "¿Cuál es el precio medio de los Audi?"
- "¿Qué vehículos disponibles (no reservados) hay?"
- "Muéstrame coches con menos de 50.000 km"
- "¿Qué marcas tenemos en stock?"
- "¿Cuántos días llevan los coches en stock de media?"
- "¿Qué coches tenemos publicados en internet?"
- "Recomiéndame un coche familiar económico"

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
