from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(models.TextChoices):
    DIRECTOR_COMERCIAL = "DC", "Director Comercial"
    GERENTE_GERENTE = "GC", "Gerente Gerente"
    AGENTE_COMERCIAL = "AC", "Agente Comercial"
    TASADOR = "TAS", "Tasador"
    # Se pueden añadir más perfiles en el futuro

class User(AbstractUser):
    profile = models.CharField(
        max_length=10,
        choices=UserProfile.choices,
        default=UserProfile.AGENTE_COMERCIAL,
        verbose_name="Perfil del usuario"
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.get_profile_display()})"
