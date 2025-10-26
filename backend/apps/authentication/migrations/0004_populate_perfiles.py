# Generated migration to populate Perfil model from legacy profile codes
from django.db import migrations


def populate_perfiles(apps, schema_editor):
    """Crear perfiles por defecto mapeando desde los códigos antiguos"""
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
        if created:
            print(f"Creado perfil: {perfil_data['nombre']}")

    # Asignar perfil_map a usuarios que lo necesitan
    # (los que tenían profile como CharField antes)
    updated_count = 0
    for user in User.objects.filter(profile__isnull=True):
        # Solo actualizar si el usuario estaba activo (sin fecha_baja)
        # y no tiene perfil ya asignado
        if not user.fecha_baja:
            # Asignar perfil por defecto Agente Comercial si no tiene
            user.profile = perfil_map.get('AC')
            user.save(update_fields=['profile'])
            updated_count += 1


def reverse_populate(apps, schema_editor):
    """Reverso: solo limpiar los perfiles si fuera necesario"""
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0003_perfil_user_fecha_baja_alter_user_profile'),
    ]

    operations = [
        migrations.RunPython(populate_perfiles, reverse_populate),
    ]
