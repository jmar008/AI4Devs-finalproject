from django.db import models
from django.contrib.auth.models import AbstractUser

class Provincia(models.Model):
    """Modelo para las provincias españolas"""
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la provincia")
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código de la provincia")

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Concesionario(models.Model):
    """Modelo para los concesionarios"""
    nombre = models.CharField(max_length=200, verbose_name="Nombre del concesionario")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        verbose_name="Provincia"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Concesionario"
        verbose_name_plural = "Concesionarios"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.provincia.nombre}"

class Perfil(models.Model):
    """Modelo de perfiles de usuario editable (similar a los grupos)."""
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class User(AbstractUser):
    profile = models.ForeignKey(
        Perfil,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Perfil del usuario",
        related_name='users'
    )

    # Nuevos campos solicitados
    jefe = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinados',
        verbose_name="Jefe directo"
    )

    concesionario = models.ForeignKey(
        Concesionario,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Concesionario"
    )

    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Provincia"
    )

    chat_ai_activo = models.BooleanField(
        default=True,
        verbose_name="Chat con AI activo"
    )

    movil = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono móvil"
    )

    # Fecha de baja: si existe, el usuario debe considerarse dado de baja
    fecha_baja = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de baja"
    )

    # Campos adicionales de información personal
    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de nacimiento"
    )

    fecha_incorporacion = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de incorporación"
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Usuario activo"
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

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['username']

    def __str__(self):
        profile_label = self.profile.nombre if self.profile else 'sin perfil'
        return f"{self.username} ({profile_label})"

    @property
    def nombre_completo(self) -> str:
        """Devuelve el nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def tiene_subordinados(self):
        """Verifica si el usuario tiene subordinados"""
        return self.subordinados.exists()

    def get_jerarquia(self):
        """Devuelve la jerarquía del usuario hacia arriba"""
        jerarquia = []
        usuario_actual = self

        while usuario_actual.jefe:
            jerarquia.append(usuario_actual.jefe)
            usuario_actual = usuario_actual.jefe

        return jerarquia

    def save(self, *args, **kwargs):
        """Sincroniza el estado activo con la fecha de baja.

        Si `fecha_baja` está definida, el usuario se marca como inactivo.
        Si se limpia `fecha_baja`, se vuelve a activar el usuario (is_active=True).
        También sincroniza el campo `activo` auxiliar.
        """
        if self.fecha_baja:
            # Si hay fecha de baja, asegurarnos de que el usuario esté inactivo
            self.is_active = False
            self.activo = False
        else:
            # Si no hay fecha de baja, mantendremos is_active según el campo activo
            # (no forzamos True aquí si admin lo ha desactivado explícitamente)
            self.is_active = bool(self.activo)

        super().save(*args, **kwargs)
