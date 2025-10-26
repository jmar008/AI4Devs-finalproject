# Migration to populate Perfil model and migrate data from old profile field
from django.db import migrations


def create_default_perfiles(apps, schema_editor):
    """Crear perfiles por defecto y mapear datos existentes"""
    Perfil = apps.get_model('authentication', 'Perfil')
    User = apps.get_model('authentication', 'User')

    # Crear perfiles por defecto
    perfiles_default = [
        {'codigo': 'DC', 'nombre': 'Director Comercial'},
        {'codigo': 'GC', 'nombre': 'Gerente Comercial'},
        {'codigo': 'AC', 'nombre': 'Agente Comercial'},
        {'codigo': 'TAS', 'nombre': 'Tasador'},
    ]

    perfil_map = {}
    for perfil_data in perfiles_default:
        perfil, created = Perfil.objects.get_or_create(
            codigo=perfil_data['codigo'],
            defaults={'nombre': perfil_data['nombre']}
        )
        perfil_map[perfil_data['codigo']] = perfil

    # Migrar datos de usuarios existentes
    for user in User.objects.all():
        if hasattr(user, 'profile') and user.profile:
            # El campo profile todavía es CharField en este punto
            profile_code = user.profile
            if profile_code in perfil_map:
                user.profile_new = perfil_map[profile_code]
                user.save(update_fields=['profile_new'])


def reverse_migration(apps, schema_editor):
    """Reverso: copiar de profile_new de vuelta a profile (si fuera necesario)"""
    User = apps.get_model('authentication', 'User')

    for user in User.objects.all():
        if user.profile_new:
            user.profile = user.profile_new.codigo
            user.save(update_fields=['profile'])


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0002_create_perfil_model'),
    ]

    operations = [
        migrations.RunPython(create_default_perfiles, reverse_migration),
    ]
