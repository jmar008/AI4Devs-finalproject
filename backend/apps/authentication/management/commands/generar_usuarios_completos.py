from django.core.management.base import BaseCommand
from django.db import transaction
from apps.authentication.models import User, Perfil, Concesionario, Provincia
from datetime import datetime, date, timedelta
import random
import string
import secrets

# Nombres y apellidos españoles comunes
NOMBRES_MASCULINOS = [
    'Juan', 'José', 'Francisco', 'Manuel', 'Luis', 'Diego', 'Carlos', 'Miguel',
    'Andrés', 'Rafael', 'Pedro', 'Javier', 'Jorge', 'Ramón', 'Rubén', 'Sergio',
    'Enrique', 'Alberto', 'Ángel', 'Roberto', 'Fernando', 'Ignacio', 'Jesús',
    'Benito', 'Guillermo', 'Antonio', 'Pablo', 'Alejandro', 'Adrián', 'David'
]

NOMBRES_FEMENINOS = [
    'María', 'Carmen', 'Isabel', 'Rosa', 'Ana', 'Elena', 'Dolores', 'Francisca',
    'Juana', 'Matilde', 'Concepción', 'Josefa', 'Manuela', 'Inés', 'Margarita',
    'Antonia', 'Virtudes', 'Natividad', 'Amparo', 'Ascensión', 'Libertad',
    'Soledad', 'Esperanza', 'Pilar', 'Teresa', 'Cristina', 'Mónica', 'Patricia'
]

APELLIDOS = [
    'García', 'Rodríguez', 'Martínez', 'Hernández', 'López', 'González', 'Pérez', 'Sánchez',
    'Jiménez', 'Moreno', 'Flores', 'Rivera', 'Torres', 'Campos', 'Domínguez', 'Castro',
    'Vargas', 'Ramos', 'Fernández', 'Gómez', 'Díaz', 'Cruz', 'Álvarez', 'Ortega',
    'Navarro', 'Castillo', 'Medina', 'Herrera', 'Romero', 'Benítez', 'Salazar', 'Vega',
    'Molina', 'Suárez', 'Romeu', 'Iglesias', 'Vicente', 'Pardo', 'Fuentes', 'Sáez'
]

# Perfiles disponibles con jerarquía
PERFILES_DATA = [
    {'codigo': 'CEO', 'nombre': 'Director Ejecutivo', 'nivel': 1},
    {'codigo': 'COO', 'nombre': 'Director de Operaciones', 'nivel': 2},
    {'codigo': 'CFO', 'nombre': 'Director Financiero', 'nivel': 2},
    {'codigo': 'CTO', 'nombre': 'Director de Tecnología', 'nivel': 2},
    {'codigo': 'CMO', 'nombre': 'Director de Marketing', 'nivel': 2},
    {'codigo': 'GC', 'nombre': 'Gerente Comercial', 'nivel': 3},
    {'codigo': 'GF', 'nombre': 'Gerente Financiero', 'nivel': 3},
    {'codigo': 'GT', 'nombre': 'Gerente de Tecnología', 'nivel': 3},
    {'codigo': 'GM', 'nombre': 'Gerente de Marketing', 'nivel': 3},
    {'codigo': 'AC', 'nombre': 'Agente Comercial', 'nivel': 4},
    {'codigo': 'AF', 'nombre': 'Analista Financiero', 'nivel': 4},
    {'codigo': 'DS', 'nombre': 'Desarrollador Senior', 'nivel': 4},
    {'codigo': 'DJ', 'nombre': 'Desarrollador Junior', 'nivel': 5},
    {'codigo': 'AS', 'nombre': 'Asistente', 'nivel': 5},
]

# Usuarios predefinidos (altos ejecutivos)
USUARIOS_EJECUTIVOS = [
    {
        'username': 'ceo',
        'first_name': 'Carlos',
        'last_name': 'Martínez López',
        'email': 'ceo@empresa.com',
        'perfil_codigo': 'CEO',
        'movil': '+34 600 000 001',
        'fecha_nacimiento': date(1965, 3, 15),
        'fecha_incorporacion': date(1990, 1, 1),
    },
    {
        'username': 'coo',
        'first_name': 'María',
        'last_name': 'García Rodríguez',
        'email': 'coo@empresa.com',
        'perfil_codigo': 'COO',
        'movil': '+34 600 000 002',
        'fecha_nacimiento': date(1970, 7, 22),
        'fecha_incorporacion': date(1995, 3, 1),
    },
    {
        'username': 'cfo',
        'first_name': 'Antonio',
        'last_name': 'Fernández Gómez',
        'email': 'cfo@empresa.com',
        'perfil_codigo': 'CFO',
        'movil': '+34 600 000 003',
        'fecha_nacimiento': date(1972, 11, 8),
        'fecha_incorporacion': date(1998, 6, 15),
    },
    {
        'username': 'cto',
        'first_name': 'David',
        'last_name': 'Sánchez Pérez',
        'email': 'cto@empresa.com',
        'perfil_codigo': 'CTO',
        'movil': '+34 600 000 004',
        'fecha_nacimiento': date(1975, 1, 30),
        'fecha_incorporacion': date(2000, 9, 1),
    },
    {
        'username': 'cmo',
        'first_name': 'Isabel',
        'last_name': 'López Martínez',
        'email': 'cmo@empresa.com',
        'perfil_codigo': 'CMO',
        'movil': '+34 600 000 005',
        'fecha_nacimiento': date(1973, 5, 12),
        'fecha_incorporacion': date(1999, 11, 20),
    },
]


class Command(BaseCommand):
    help = 'Genera una estructura completa de usuarios con jerarquía organizacional'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Limpia todos los usuarios antes de generar nuevos'
        )
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Número total de usuarios a generar (excluyendo ejecutivos)'
        )

    def _generate_password(self, length=12):
        """Genera una contraseña segura"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        while True:
            pwd = ''.join(secrets.choice(alphabet) for _ in range(length))
            if (any(c.islower() for c in pwd) and
                any(c.isupper() for c in pwd) and
                any(c.isdigit() for c in pwd) and
                any(c in "!@#$%^&*" for c in pwd)):
                return pwd

    def _random_date_of_birth(self, perfil_nivel):
        """Genera fecha de nacimiento basada en el nivel del perfil"""
        today = date.today()
        if perfil_nivel == 1:  # CEO
            min_age, max_age = 50, 70
        elif perfil_nivel <= 3:  # Directores/Gerentes
            min_age, max_age = 35, 60
        elif perfil_nivel == 4:  # Seniors
            min_age, max_age = 25, 45
        else:  # Juniors/Asistentes
            min_age, max_age = 20, 35

        days_range = (max_age - min_age) * 365
        random_days = random.randint(0, days_range)
        return today - timedelta(days=random_days + min_age * 365)

    def _random_incorporation_date(self, perfil_nivel):
        """Genera fecha de incorporación basada en el nivel del perfil"""
        today = date.today()
        if perfil_nivel == 1:  # CEO
            min_years = 20
        elif perfil_nivel <= 3:  # Directores/Gerentes
            min_years = 10
        elif perfil_nivel == 4:  # Seniors
            min_years = 3
        else:  # Juniors/Asistentes
            min_years = 0

        max_years = 25
        years_range = max_years - min_years
        random_years = random.randint(0, years_range)
        return today - timedelta(days=(min_years + random_years) * 365)

    def _get_random_name(self, gender=None):
        """Genera un nombre aleatorio"""
        if gender == 'M':
            nombre = random.choice(NOMBRES_MASCULINOS)
        elif gender == 'F':
            nombre = random.choice(NOMBRES_FEMENINOS)
        else:
            nombre = random.choice(NOMBRES_MASCULINOS + NOMBRES_FEMENINOS)
        apellido1 = random.choice(APELLIDOS)
        apellido2 = random.choice(APELLIDOS)
        return nombre, f"{apellido1} {apellido2}"

    def _generate_phone(self):
        """Genera un número de móvil español aleatorio"""
        return f"+34 6{random.randint(10,99)} {random.randint(100,999)} {random.randint(100,999)}"

    def handle(self, *args, **options):
        count = options['count']

        self.stdout.write(
            self.style.SUCCESS('=' * 80)
        )
        self.stdout.write(
            self.style.SUCCESS('👥 GENERANDO ESTRUCTURA COMPLETA DE USUARIOS')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 80)
        )

        # Si --limpiar está activo
        if options.get('limpiar'):
            self.stdout.write(
                self.style.WARNING('\n🗑️  Limpiando usuarios anteriores...')
            )
            # No eliminar superusuarios ni el usuario actual
            User.objects.exclude(is_superuser=True).exclude(username='admin').delete()
            self.stdout.write(
                self.style.SUCCESS('✅ Usuarios limpiados')
            )

        with transaction.atomic():
            # Crear perfiles si no existen
            self._crear_perfiles()

            # Crear usuarios ejecutivos predefinidos
            ejecutivos = self._crear_usuarios_ejecutivos()

            # Crear estructura jerárquica de usuarios
            self._crear_usuarios_jerarquicos(count, ejecutivos)

            # Crear algunos usuarios dados de baja
            self._crear_usuarios_baja()

        self.stdout.write(
            self.style.SUCCESS('\n✅ Generación de usuarios completada')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 80)
        )

    def _crear_perfiles(self):
        """Crea los perfiles organizacionales"""
        self.stdout.write(
            self.style.WARNING('\n📋 Creando perfiles organizacionales...')
        )

        perfiles_creados = 0
        for perfil_data in PERFILES_DATA:
            perfil, created = Perfil.objects.get_or_create(
                codigo=perfil_data['codigo'],
                defaults={
                    'nombre': perfil_data['nombre'],
                    'activo': True
                }
            )
            if created:
                perfiles_creados += 1

        self.stdout.write(
            self.style.SUCCESS(f'✅ {perfiles_creados} perfiles creados')
        )

    def _crear_usuarios_ejecutivos(self):
        """Crea los usuarios ejecutivos predefinidos"""
        self.stdout.write(
            self.style.WARNING('\n👔 Creando usuarios ejecutivos...')
        )

        ejecutivos = []
        for ejecutivo_data in USUARIOS_EJECUTIVOS:
            perfil = Perfil.objects.get(codigo=ejecutivo_data['perfil_codigo'])

            # Asignar concesionario y provincia (Madrid por defecto para ejecutivos)
            try:
                concesionario = Concesionario.objects.filter(provincia__nombre='Madrid').first()
                provincia = Provincia.objects.get(nombre='Madrid')
            except:
                concesionario = Concesionario.objects.first()
                provincia = Provincia.objects.first()

            user = User.objects.create_user(
                username=ejecutivo_data['username'],
                email=ejecutivo_data['email'],
                password=self._generate_password(),
                first_name=ejecutivo_data['first_name'],
                last_name=ejecutivo_data['last_name'],
                profile=perfil,
                concesionario=concesionario,
                provincia=provincia,
                movil=ejecutivo_data['movil'],
                fecha_nacimiento=ejecutivo_data['fecha_nacimiento'],
                fecha_incorporacion=ejecutivo_data['fecha_incorporacion'],
                activo=True,
                chat_ai_activo=True,
            )

            ejecutivos.append(user)
            self.stdout.write(
                f'✓ {user.username}: {user.nombre_completo} ({perfil.nombre})'
            )

        return ejecutivos

    def _crear_usuarios_jerarquicos(self, count, ejecutivos):
        """Crea usuarios con estructura jerárquica"""
        self.stdout.write(
            self.style.WARNING(f'\n👥 Creando {count} usuarios jerárquicos...')
        )

        # Obtener CEOs para jerarquía
        ceo = next((e for e in ejecutivos if e.profile.codigo == 'CEO'), None)

        usuarios_creados = 0
        perfiles_por_nivel = {
            3: ['GC', 'GF', 'GT', 'GM'],  # Gerentes
            4: ['AC', 'AF', 'DS'],        # Seniors
            5: ['DJ', 'AS'],              # Juniors/Asistentes
        }

        # Crear gerentes (nivel 3) - reportan al CEO
        gerentes = []
        for perfil_codigo in perfiles_por_nivel[3]:
            perfil = Perfil.objects.get(codigo=perfil_codigo)
            nombre, apellidos = self._get_random_name()

            user = User.objects.create_user(
                username=f"{perfil_codigo.lower()}_{usuarios_creados:03d}",
                email=f"{perfil_codigo.lower()}_{usuarios_creados:03d}@empresa.com",
                password=self._generate_password(),
                first_name=nombre,
                last_name=apellidos,
                profile=perfil,
                jefe=ceo,
                concesionario=random.choice(Concesionario.objects.all()) if Concesionario.objects.exists() else None,
                provincia=random.choice(Provincia.objects.all()) if Provincia.objects.exists() else None,
                movil=self._generate_phone(),
                fecha_nacimiento=self._random_date_of_birth(3),
                fecha_incorporacion=self._random_incorporation_date(3),
                activo=True,
                chat_ai_activo=random.choice([True, True, False]),  # 66% activo
            )
            gerentes.append(user)
            usuarios_creados += 1

        # Crear usuarios de nivel 4 (Seniors) - reportan a gerentes
        seniors = []
        for perfil_codigo in perfiles_por_nivel[4]:
            perfil = Perfil.objects.get(codigo=perfil_codigo)
            for _ in range(max(1, count // 20)):  # Distribuir seniors
                nombre, apellidos = self._get_random_name()
                jefe = random.choice(gerentes) if gerentes else ceo

                user = User.objects.create_user(
                    username=f"{perfil_codigo.lower()}_{usuarios_creados:03d}",
                    email=f"{perfil_codigo.lower()}_{usuarios_creados:03d}@empresa.com",
                    password=self._generate_password(),
                    first_name=nombre,
                    last_name=apellidos,
                    profile=perfil,
                    jefe=jefe,
                    concesionario=jefe.concesionario if jefe and jefe.concesionario else None,
                    provincia=jefe.provincia if jefe and jefe.provincia else None,
                    movil=self._generate_phone(),
                    fecha_nacimiento=self._random_date_of_birth(4),
                    fecha_incorporacion=self._random_incorporation_date(4),
                    activo=True,
                    chat_ai_activo=random.choice([True, True, False]),
                )
                seniors.append(user)
                usuarios_creados += 1

        # Crear usuarios de nivel 5 (Juniors/Asistentes) - reportan a seniors
        for perfil_codigo in perfiles_por_nivel[5]:
            perfil = Perfil.objects.get(codigo=perfil_codigo)
            usuarios_restantes = count - usuarios_creados

            for i in range(max(1, usuarios_restantes // len(perfiles_por_nivel[5]))):
                nombre, apellidos = self._get_random_name()
                jefe = random.choice(seniors) if seniors else random.choice(gerentes) if gerentes else ceo

                user = User.objects.create_user(
                    username=f"{perfil_codigo.lower()}_{usuarios_creados:03d}",
                    email=f"{perfil_codigo.lower()}_{usuarios_creados:03d}@empresa.com",
                    password=self._generate_password(),
                    first_name=nombre,
                    last_name=apellidos,
                    profile=perfil,
                    jefe=jefe,
                    concesionario=jefe.concesionario if jefe and jefe.concesionario else None,
                    provincia=jefe.provincia if jefe and jefe.provincia else None,
                    movil=self._generate_phone(),
                    fecha_nacimiento=self._random_date_of_birth(5),
                    fecha_incorporacion=self._random_incorporation_date(5),
                    activo=True,
                    chat_ai_activo=random.choice([True, False, False]),  # 33% activo
                )
                usuarios_creados += 1

        self.stdout.write(
            self.style.SUCCESS(f'✅ {usuarios_creados} usuarios jerárquicos creados')
        )

    def _crear_usuarios_baja(self):
        """Crea algunos usuarios dados de baja"""
        self.stdout.write(
            self.style.WARNING('\n📉 Creando usuarios dados de baja...')
        )

        # Obtener algunos usuarios existentes para darlos de baja
        usuarios_activos = User.objects.filter(activo=True, is_superuser=False).exclude(username='admin')[:5]

        usuarios_baja = 0
        for user in usuarios_activos:
            # Fecha de baja aleatoria en los últimos 2 años
            dias_atras = random.randint(30, 730)
            fecha_baja = date.today() - timedelta(days=dias_atras)

            user.fecha_baja = fecha_baja
            user.activo = False
            user.is_active = False
            user.save()

            usuarios_baja += 1

        self.stdout.write(
            self.style.SUCCESS(f'✅ {usuarios_baja} usuarios marcados como dados de baja')
        )
