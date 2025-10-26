from django.db import models
from apps.authentication.models import User


class ChatConversation(models.Model):
    """
    Representa una conversación de chat con la IA.
    Cada usuario puede tener múltiples conversaciones.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_conversations',
        verbose_name='Usuario'
    )
    title = models.CharField(
        max_length=255,
        default='Nueva conversación',
        verbose_name='Título'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activa'
    )

    class Meta:
        db_table = 'ai_chat_conversations'
        verbose_name = 'Conversación'
        verbose_name_plural = 'Conversaciones'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['is_active', '-updated_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.title}"


class ChatMessage(models.Model):
    """
    Representa un mensaje individual dentro de una conversación.
    Puede ser del usuario o de la IA.
    """
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('assistant', 'Asistente'),
        ('system', 'Sistema'),
    ]

    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Conversación'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name='Rol'
    )
    content = models.TextField(
        verbose_name='Contenido'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
        db_index=True
    )

    # Metadata opcional para tracking
    tokens_used = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Tokens utilizados'
    )
    model_used = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Modelo utilizado'
    )

    class Meta:
        db_table = 'ai_chat_messages'
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['role', 'created_at']),
        ]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
