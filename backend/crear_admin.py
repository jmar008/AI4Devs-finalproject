
#!/usr/bin/env python
"""
Script para crear o actualizar el usuario admin con contraseña admin123
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealaai.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear o actualizar usuario admin
user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@dealaai.com',
        'is_staff': True,
        'is_superuser': True,
        'first_name': 'Admin',
        'last_name': 'DealaAI'
    }
)

# Configurar contraseña y permisos
user.set_password('admin123')
user.is_staff = True
user.is_superuser = True
user.email = 'admin@dealaai.com'
user.save()

if created:
    print('✅ Usuario admin CREADO correctamente')
else:
    print('✅ Usuario admin ACTUALIZADO correctamente')

print(f'\n📋 Credenciales:')
print(f'   Username: admin')
print(f'   Password: admin123')
print(f'   Email: admin@dealaai.com')
print(f'\n🌐 Acceso: http://mcp.jorgemg.es/admin/')
