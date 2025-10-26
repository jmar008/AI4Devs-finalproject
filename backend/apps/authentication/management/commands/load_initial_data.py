from django.core.management.base import BaseCommand
from django.db import transaction
from apps.authentication.models import Provincia, Concesionario, Perfil


class Command(BaseCommand):
    help = 'Carga datos iniciales de provincias, concesionarios y perfiles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Fuerza la recarga de datos incluso si ya existen',
        )

    def handle(self, *args, **options):
        force = options['force']

        # Datos de provincias españolas
        provincias_data = [
            {'nombre': 'Álava', 'codigo': '01'},
            {'nombre': 'Albacete', 'codigo': '02'},
            {'nombre': 'Alicante', 'codigo': '03'},
            {'nombre': 'Almería', 'codigo': '04'},
            {'nombre': 'Ávila', 'codigo': '05'},
            {'nombre': 'Badajoz', 'codigo': '06'},
            {'nombre': 'Baleares', 'codigo': '07'},
            {'nombre': 'Barcelona', 'codigo': '08'},
            {'nombre': 'Burgos', 'codigo': '09'},
            {'nombre': 'Cáceres', 'codigo': '10'},
            {'nombre': 'Cádiz', 'codigo': '11'},
            {'nombre': 'Castellón', 'codigo': '12'},
            {'nombre': 'Ciudad Real', 'codigo': '13'},
            {'nombre': 'Córdoba', 'codigo': '14'},
            {'nombre': 'Coruña, A', 'codigo': '15'},
            {'nombre': 'Cuenca', 'codigo': '16'},
            {'nombre': 'Girona', 'codigo': '17'},
            {'nombre': 'Granada', 'codigo': '18'},
            {'nombre': 'Guadalajara', 'codigo': '19'},
            {'nombre': 'Gipuzkoa', 'codigo': '20'},
            {'nombre': 'Huelva', 'codigo': '21'},
            {'nombre': 'Huesca', 'codigo': '22'},
            {'nombre': 'Jaén', 'codigo': '23'},
            {'nombre': 'León', 'codigo': '24'},
            {'nombre': 'Lleida', 'codigo': '25'},
            {'nombre': 'Rioja, La', 'codigo': '26'},
            {'nombre': 'Lugo', 'codigo': '27'},
            {'nombre': 'Madrid', 'codigo': '28'},
            {'nombre': 'Málaga', 'codigo': '29'},
            {'nombre': 'Murcia', 'codigo': '30'},
            {'nombre': 'Navarra', 'codigo': '31'},
            {'nombre': 'Ourense', 'codigo': '32'},
            {'nombre': 'Asturias', 'codigo': '33'},
            {'nombre': 'Palencia', 'codigo': '34'},
            {'nombre': 'Palmas, Las', 'codigo': '35'},
            {'nombre': 'Pontevedra', 'codigo': '36'},
            {'nombre': 'Salamanca', 'codigo': '37'},
            {'nombre': 'Santa Cruz de Tenerife', 'codigo': '38'},
            {'nombre': 'Cantabria', 'codigo': '39'},
            {'nombre': 'Segovia', 'codigo': '40'},
            {'nombre': 'Sevilla', 'codigo': '41'},
            {'nombre': 'Soria', 'codigo': '42'},
            {'nombre': 'Tarragona', 'codigo': '43'},
            {'nombre': 'Teruel', 'codigo': '44'},
            {'nombre': 'Toledo', 'codigo': '45'},
            {'nombre': 'Valencia', 'codigo': '46'},
            {'nombre': 'Valladolid', 'codigo': '47'},
            {'nombre': 'Bizkaia', 'codigo': '48'},
            {'nombre': 'Zamora', 'codigo': '49'},
            {'nombre': 'Zaragoza', 'codigo': '50'},
            {'nombre': 'Ceuta', 'codigo': '51'},
            {'nombre': 'Melilla', 'codigo': '52'},
        ]

        with transaction.atomic():
            # Cargar perfiles
            if force or not Perfil.objects.exists():
                if force:
                    Perfil.objects.all().delete()
                    self.stdout.write('Eliminando perfiles existentes...')

                self.stdout.write('Cargando perfiles de usuario...')
                perfiles_data = [
                    {'codigo': 'DC', 'nombre': 'Director Comercial'},
                    {'codigo': 'GC', 'nombre': 'Gerente Comercial'},
                    {'codigo': 'AC', 'nombre': 'Agente Comercial'},
                    {'codigo': 'TAS', 'nombre': 'Tasador'},
                ]
                for perfil_data in perfiles_data:
                    perfil, created = Perfil.objects.get_or_create(
                        codigo=perfil_data['codigo'],
                        defaults={'nombre': perfil_data['nombre']}
                    )
                    if created:
                        self.stdout.write(f'✓ Creado perfil: {perfil.nombre}')

                self.stdout.write(
                    self.style.SUCCESS(f'Se cargaron {len(perfiles_data)} perfiles')
                )
            else:
                self.stdout.write('Los perfiles ya existen. Usa --force para recargar.')

            # Cargar provincias
            if force or not Provincia.objects.exists():
                if force:
                    Provincia.objects.all().delete()
                    self.stdout.write('Eliminando provincias existentes...')

                self.stdout.write('Cargando provincias...')
                for provincia_data in provincias_data:
                    provincia, created = Provincia.objects.get_or_create(
                        codigo=provincia_data['codigo'],
                        defaults={'nombre': provincia_data['nombre']}
                    )
                    if created:
                        self.stdout.write(f'✓ Creada provincia: {provincia.nombre}')

                self.stdout.write(
                    self.style.SUCCESS(f'Se cargaron {len(provincias_data)} provincias')
                )
            else:
                self.stdout.write('Las provincias ya existen. Usa --force para recargar.')

            # Crear algunos concesionarios de ejemplo
            concesionarios_ejemplo = [
                {
                    'nombre': 'AutoMadrid Centro',
                    'direccion': 'Calle Gran Vía 123, Madrid',
                    'telefono': '915123456',
                    'email': 'info@automadrid.com',
                    'provincia_codigo': '28'
                },
                {
                    'nombre': 'Barcelona Motor',
                    'direccion': 'Passeig de Gràcia 456, Barcelona',
                    'telefono': '934567890',
                    'email': 'contacto@barcelonamotor.com',
                    'provincia_codigo': '08'
                },
                {
                    'nombre': 'Valencia Automóviles',
                    'direccion': 'Avenida del Puerto 789, Valencia',
                    'telefono': '963789012',
                    'email': 'ventas@valenciauto.com',
                    'provincia_codigo': '46'
                },
                {
                    'nombre': 'Sevilla Cars',
                    'direccion': 'Calle Sierpes 321, Sevilla',
                    'telefono': '954321098',
                    'email': 'info@sevillacars.com',
                    'provincia_codigo': '41'
                },
                {
                    'nombre': 'Bilbao Premium',
                    'direccion': 'Gran Vía 654, Bilbao',
                    'telefono': '944654321',
                    'email': 'premium@bilbaoauto.com',
                    'provincia_codigo': '48'
                }
            ]

            if force or not Concesionario.objects.exists():
                if force:
                    Concesionario.objects.all().delete()
                    self.stdout.write('Eliminando concesionarios existentes...')

                self.stdout.write('Cargando concesionarios de ejemplo...')
                for concesionario_data in concesionarios_ejemplo:
                    try:
                        provincia = Provincia.objects.get(codigo=concesionario_data['provincia_codigo'])
                        concesionario, created = Concesionario.objects.get_or_create(
                            nombre=concesionario_data['nombre'],
                            defaults={
                                'direccion': concesionario_data['direccion'],
                                'telefono': concesionario_data['telefono'],
                                'email': concesionario_data['email'],
                                'provincia': provincia
                            }
                        )
                        if created:
                            self.stdout.write(f'✓ Creado concesionario: {concesionario.nombre}')
                    except Provincia.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f'Error: Provincia con código {concesionario_data["provincia_codigo"]} no encontrada'
                            )
                        )

                self.stdout.write(
                    self.style.SUCCESS(f'Se cargaron {len(concesionarios_ejemplo)} concesionarios de ejemplo')
                )
            else:
                self.stdout.write('Los concesionarios ya existen. Usa --force para recargar.')

        self.stdout.write(
            self.style.SUCCESS('¡Datos iniciales cargados exitosamente!')
        )
