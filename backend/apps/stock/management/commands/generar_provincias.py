"""
Comando Django para generar datos de provincias españolas sin IA
"""
from django.core.management.base import BaseCommand
from apps.stock.models import Stock
from apps.stock.scrapers import generar_datos_faltantes

PROVINCIAS_ESPAÑA = [
    'Álava',
    'Albacete',
    'Alicante',
    'Almería',
    'Asturias',
    'Ávila',
    'Badajoz',
    'Barcelona',
    'Burgos',
    'Cáceres',
    'Cádiz',
    'Cantabria',
    'Castellón',
    'Ciudad Real',
    'Córdoba',
    'Cuenca',
    'Girona',
    'Granada',
    'Guadalajara',
    'Guipúzcoa',
    'Huesca',
    'Jaén',
    'La Coruña',
    'La Rioja',
    'Las Palmas',
    'León',
    'Lleida',
    'Lugo',
    'Madrid',
    'Málaga',
    'Murcia',
    'Navarra',
    'Ourense',
    'Palencia',
    'Palma de Mallorca',
    'Pamplona',
    'Pontevedra',
    'Salamanca',
    'Segovia',
    'Sevilla',
    'Soria',
    'Tarragona',
    'Teruel',
    'Toledo',
    'Valencia',
    'Valladolid',
    'Vizcaya',
    'Zamora',
    'Zaragoza',
]


class Command(BaseCommand):
    help = 'Genera datos de provincias españolas en la tabla de Stock'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Limpia todos los datos antes de generar nuevos'
        )
        parser.add_argument(
            '--vehiculos-por-provincia',
            type=int,
            default=2,
            help='Número de vehículos por provincia (default: 2)'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=' * 70)
        )
        self.stdout.write(
            self.style.SUCCESS('🏘️  GENERANDO DATOS DE PROVINCIAS ESPAÑOLAS')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 70)
        )

        # Si --limpiar está activo
        if options.get('limpiar'):
            self.stdout.write(
                self.style.WARNING('\n🗑️  Limpiando datos anteriores...')
            )
            Stock.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS('✅ Datos limpiados')
            )

        # Generar datos de provincias
        vehiculos_por_provincia = options.get('vehiculos_por_provincia', 2)
        self._generar_provincias(vehiculos_por_provincia)

        self.stdout.write(
            self.style.SUCCESS('\n✅ Generación completada')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 70)
        )

    def _generar_provincias(self, vehiculos_por_provincia=2):
        """Genera registros de prueba por cada provincia"""
        self.stdout.write(
            self.style.WARNING('\n📍 Generando datos de provincias...')
        )

        contador = 0
        for provincia in PROVINCIAS_ESPAÑA:
            try:
                # Generar N vehículos por provincia usando datos aleatorios
                for i in range(vehiculos_por_provincia):
                    datos_vehiculo = generar_datos_faltantes()

                    Stock.objects.create(
                        bastidor=datos_vehiculo.get('bastidor', f"{provincia.upper()[:3]}-{contador:05d}"),
                        marca=datos_vehiculo.get('marca', 'Desconocida'),
                        modelo=datos_vehiculo.get('modelo', 'Desconocido'),
                        provincia=provincia,
                        nom_concesionario=f'Concesionario {provincia}',
                        nom_proveedor=datos_vehiculo.get('nom_proveedor', f'Proveedor {provincia}'),
                        color=datos_vehiculo.get('color', 'Blanco'),
                        anio_matricula=datos_vehiculo.get('anio_matricula', 2020),
                        kilometros=datos_vehiculo.get('kilometros', 50000),
                        precio_venta=datos_vehiculo.get('precio_venta', 15000),
                        matricula=datos_vehiculo.get('matricula', ''),
                    )
                    contador += 1

                self.stdout.write(
                    f'✔️  {provincia}: {vehiculos_por_provincia} vehículos creados'
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error en {provincia}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ {contador} vehículos generados en total')
        )
