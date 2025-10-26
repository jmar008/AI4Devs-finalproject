import secrets
import string
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.authentication.models import User, Perfil, Concesionario, Provincia


# Nombres y apellidos españoles comunes
NOMBRES = [
    'Juan', 'María', 'José', 'Carmen', 'Francisco', 'Isabel', 'Manuel', 'Rosa',
    'Antonio', 'Pilar', 'Luis', 'Ana', 'Diego', 'Encarnación', 'Carlos', 'Elena',
    'Miguel', 'Dolores', 'Andrés', 'Francisca', 'Rafael', 'Juana', 'Pedro', 'Matilde',
    'Javier', 'Concepción', 'Jorge', 'Josefa', 'Ramón', 'Manuela', 'Rubén', 'Inés',
    'Sergio', 'Francisca', 'Enrique', 'Margarita', 'Alberto', 'Antonia', 'Ángel', 'Virtudes',
    'Roberto', 'Natividad', 'Fernando', 'Amparo', 'Ignacio', 'Ascensión', 'Jesús', 'Libertad',
    'Benito', 'Soledad', 'Guillermo', 'Esperanza'
]

APELLIDOS = [
    'García', 'Rodríguez', 'Martínez', 'Hernández', 'López', 'González', 'Pérez', 'Sánchez',
    'Jiménez', 'Moreno', 'Flores', 'Rivera', 'Torres', 'Campos', 'Domínguez', 'Castro',
    'Vargas', 'Ramos', 'Fernández', 'Gómez', 'Díaz', 'Cruz', 'Álvarez', 'Ortega',
    'Navarro', 'Castillo', 'Medina', 'Herrera', 'Romero', 'Benítez', 'Salazar', 'Vega',
    'Molina', 'Suárez', 'Romeu', 'Iglesias', 'Vicente', 'Pardo', 'Fuentes', 'Sáez',
    'Valero', 'Guillén', 'Bosch', 'Amat', 'Barroso', 'Serrano', 'Blanch', 'Estrada'
]


class Command(BaseCommand):
    help = 'Genera usuarios de prueba enriquecidos con datos personales y exporta un fichero markdown con información completa'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50, help='Número de usuarios a generar')
        parser.add_argument('--concesionario', type=str, default=None, help='Nombre del concesionario (se creará si no existe)')
        parser.add_argument('--output', type=str, default='docs/test_users.md', help='Ruta de salida del fichero .md (relativa a workspace/backend)')

    def _random_password(self, length=12):
        alphabet = string.ascii_letters + string.digits
        # ensure at least one digit and one letter
        while True:
            pwd = ''.join(secrets.choice(alphabet) for _ in range(length))
            if any(c.isdigit() for c in pwd) and any(c.isalpha() for c in pwd):
                return pwd

    def _random_date_of_birth(self):
        """Genera una fecha de nacimiento aleatoria entre 25 y 65 años atrás"""
        today = datetime.now()
        min_age = 25
        max_age = 65
        days_range = (max_age - min_age) * 365
        random_days = secrets.randbelow(days_range)
        birth_date = today - timedelta(days=random_days + min_age * 365)
        return birth_date.date()

    def _random_incorporation_date(self):
        """Genera una fecha de incorporación aleatoria en los últimos 5 años"""
        today = datetime.now()
        days_range = 5 * 365
        random_days = secrets.randbelow(days_range)
        incorporation_date = today - timedelta(days=random_days)
        return incorporation_date.date()

    def handle(self, *args, **options):
        count = options['count']
        concesionario_name = options['concesionario'] or 'Concesionario Prueba'
        output_path = options['output']

        with transaction.atomic():
            concesionario, _ = Concesionario.objects.get_or_create(
                nombre=concesionario_name,
                defaults={'provincia': Provincia.objects.first() or None}
            )

            perfil, _ = Perfil.objects.get_or_create(codigo='AC', defaults={'nombre': 'Agente Comercial'})

            # Crear un usuario jefe (el primero será jefe de los demás)
            jefe_nombre = secrets.choice(NOMBRES)
            jefe_apellido1 = secrets.choice(APELLIDOS)
            jefe_apellido2 = secrets.choice(APELLIDOS)

            jefe_username = 'jefe_principal'
            jefe_email = f'{jefe_username}@{concesionario.nombre.replace(" ","").lower()}.local'
            jefe_password = self._random_password(12)

            perfil_jefe, _ = Perfil.objects.get_or_create(codigo='GC', defaults={'nombre': 'Gerente Comercial'})

            jefe = User.objects.create_user(
                username=jefe_username,
                email=jefe_email,
                password=jefe_password,
                profile=perfil_jefe,
                concesionario=concesionario,
                first_name=jefe_nombre,
                last_name=f'{jefe_apellido1} {jefe_apellido2}',
                movil=f'6{secrets.choice(string.digits)}{secrets.choice(string.digits)}{secrets.choice(string.digits)}{secrets.choice(string.digits)}{secrets.choice(string.digits)}{secrets.choice(string.digits)}{secrets.choice(string.digits)}',
                fecha_nacimiento=self._random_date_of_birth(),
                fecha_incorporacion=self._random_incorporation_date(),
                provincia=concesionario.provincia,
            )

            self.stdout.write(f'✓ Jefe principal creado: {jefe.username}')

            users_info = []
            usuarios = []

            for i in range(1, count + 1):
                username = f'emp{i:03d}'
                email = f'{username}@{concesionario.nombre.replace(" ","").lower()}.local'
                password = self._random_password(12)
                movil = f'6{secrets.choice(string.digits)}{secrets.choice(string.digits)}{secrets.choice(string.digits)}{secrets.choice(string.digits)}{secrets.choice(string.digits)}{secrets.choice(string.digits)}{secrets.choice(string.digits)}'

                # Datos personales aleatorios
                nombre = secrets.choice(NOMBRES)
                apellido1 = secrets.choice(APELLIDOS)
                apellido2 = secrets.choice(APELLIDOS)
                fecha_nacimiento = self._random_date_of_birth()
                fecha_incorporacion = self._random_incorporation_date()

                # Provincias disponibles
                provincia = Provincia.objects.order_by('?').first() or concesionario.provincia

                # Crear usuario
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    profile=perfil,
                    concesionario=concesionario,
                    movil=movil,
                    first_name=nombre,
                    last_name=f'{apellido1} {apellido2}',
                    fecha_nacimiento=fecha_nacimiento,
                    fecha_incorporacion=fecha_incorporacion,
                    jefe=jefe,
                    provincia=provincia,
                )

                usuarios.append(user)
                users_info.append({
                    'username': username,
                    'nombre_completo': user.nombre_completo,
                    'email': email,
                    'password': password,
                    'movil': movil,
                    'fecha_nacimiento': fecha_nacimiento.strftime('%Y-%m-%d'),
                    'fecha_incorporacion': fecha_incorporacion.strftime('%Y-%m-%d'),
                    'jefe': jefe.nombre_completo,
                    'provincia': provincia.nombre if provincia else 'N/A',
                })

        # Escribir fichero markdown
        import os
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
        full_output = os.path.join(base_dir, output_path)
        os.makedirs(os.path.dirname(full_output), exist_ok=True)

        with open(full_output, 'w', encoding='utf-8') as f:
            f.write('# Usuarios de prueba - Empleados del Concesionario\n\n')
            f.write(f'**Concesionario:** {concesionario.nombre}\n')
            f.write(f'**Total usuarios:** {count}\n')
            f.write(f'**Jefe principal:** {jefe.nombre_completo} ({jefe_username})\n\n')

            f.write('## Jefe Principal\n\n')
            f.write('| Campo | Valor |\n')
            f.write('|---|---|\n')
            f.write(f'| Username | {jefe_username} |\n')
            f.write(f'| Contraseña | {jefe_password} |\n')
            f.write(f'| Nombre | {jefe.nombre_completo} |\n')
            f.write(f'| Email | {jefe_email} |\n')
            f.write(f'| Móvil | {jefe.movil} |\n')
            f.write(f'| F. Nacimiento | {jefe.fecha_nacimiento} |\n')
            f.write(f'| F. Incorporación | {jefe.fecha_incorporacion} |\n')
            f.write(f'| Provincia | {jefe.provincia.nombre if jefe.provincia else "N/A"} |\n\n')

            f.write('## Empleados\n\n')
            f.write('| # | Username | Contraseña | Nombre Completo | Email | Móvil | F. Nacimiento | F. Incorporación | Jefe | Provincia |\n')
            f.write('|---|---|---|---|---|---|---|---|---|---|\n')
            for idx, u in enumerate(users_info, 1):
                f.write(f"| {idx} | {u['username']} | {u['password']} | {u['nombre_completo']} | {u['email']} | {u['movil']} | {u['fecha_nacimiento']} | {u['fecha_incorporacion']} | {u['jefe']} | {u['provincia']} |\n")

        self.stdout.write(self.style.SUCCESS(f'✓ Se generaron {count} usuarios + 1 jefe. Fichero: {full_output}'))

