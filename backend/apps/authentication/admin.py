from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Provincia, Concesionario, Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo", "activo")
    search_fields = ("nombre", "codigo")
    list_filter = ("activo",)

@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo")
    search_fields = ("nombre", "codigo")
    ordering = ("nombre",)

@admin.register(Concesionario)
class ConcesionarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "provincia", "telefono", "email", "activo", "fecha_creacion")
    list_filter = ("provincia", "activo", "fecha_creacion")
    search_fields = ("nombre", "telefono", "email")
    readonly_fields = ("fecha_creacion", "fecha_actualizacion")
    ordering = ("nombre",)

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # Use Django's built-in UserAdmin to get proper password handling (change form)
    list_display = (
        "username",
        "nombre_completo",
        "email",
        "profile",
        "concesionario",
        "provincia",
        "jefe",
        "chat_ai_activo",
        "fecha_baja",
        "is_active",
    )
    list_filter = (
        "profile",
        "concesionario",
        "provincia",
        "chat_ai_activo",
        "is_active",
        "is_staff",
        "fecha_incorporacion",
        "fecha_baja",
    )
    search_fields = ("username", "email", "first_name", "last_name", "movil")
    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "movil", "fecha_nacimiento")}),
        (_("Professional info"), {"fields": ("profile", "jefe", "concesionario", "provincia", "fecha_incorporacion", "fecha_baja", "chat_ai_activo")} ),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")} ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")} ),
    )

    def nombre_completo(self, obj):
        return obj.nombre_completo
    nombre_completo.short_description = "Nombre completo"
