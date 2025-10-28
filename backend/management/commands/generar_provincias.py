"""
Comando Django para generar datos de provincias españolas
"""
from django.core.management.base import BaseCommand
from apps.stock.models import Stock

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

CONCESIONARIOS_ESPAÑA = [
    # Concesionarios principales por provincia
    {'nombre': 'Concesionario Auto Madrid', 'provincia': 'Madrid', 'id': 'CAM001'},
    {'nombre': 'Concesionario Auto Barcelona', 'provincia': 'Barcelona', 'id': 'CAB001'},
    {'nombre': 'Concesionario Auto Valencia', 'provincia': 'Valencia', 'id': 'CAV001'},
    {'nombre': 'Concesionario Auto Sevilla', 'provincia': 'Sevilla', 'id': 'CAS001'},
    {'nombre': 'Concesionario Auto Bilbao', 'provincia': 'Vizcaya', 'id': 'CABi001'},
    {'nombre': 'Concesionario Auto Málaga', 'provincia': 'Málaga', 'id': 'CAMa001'},
    {'nombre': 'Concesionario Auto Murcia', 'provincia': 'Murcia', 'id': 'CAMu001'},
    {'nombre': 'Concesionario Auto Zaragoza', 'provincia': 'Zaragoza', 'id': 'CAZ001'},
    {'nombre': 'Concesionario Auto Palma', 'provincia': 'Palma de Mallorca', 'id': 'CAP001'},
    {'nombre': 'Concesionario Auto Las Palmas', 'provincia': 'Las Palmas', 'id': 'CALP001'},
    {'nombre': 'Concesionario Auto Alicante', 'provincia': 'Alicante', 'id': 'CAAl001'},
    {'nombre': 'Concesionario Auto Córdoba', 'provincia': 'Córdoba', 'id': 'CACo001'},
    {'nombre': 'Concesionario Auto Valladolid', 'provincia': 'Valladolid', 'id': 'CAVal001'},
    {'nombre': 'Concesionario Auto León', 'provincia': 'León', 'id': 'CAL001'},
    {'nombre': 'Concesionario Auto Salamanca', 'provincia': 'Salamanca', 'id': 'CASal001'},
    {'nombre': 'Concesionario Auto Castellón', 'provincia': 'Castellón', 'id': 'CACas001'},
    {'nombre': 'Concesionario Auto Jaén', 'provincia': 'Jaén', 'id': 'CAJ001'},
    {'nombre': 'Concesionario Auto Toledo', 'provincia': 'Toledo', 'id': 'CAT001'},
    {'nombre': 'Concesionario Auto Cuenca', 'provincia': 'Cuenca', 'id': 'CACu001'},
    {'nombre': 'Concesionario Auto Girona', 'provincia': 'Girona', 'id': 'CAG001'},
]


class Command(BaseCommand):
    help = 'Genera datos de provincias y concesionarios en la tabla de Stock'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Limpia todos los datos antes de generar nuevos'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=' * 70)
        )
        self.stdout.write(
            self.style.SUCCESS('🏘️  GENERANDO DATOS DE PROVINCIAS Y CONCESIONARIOS')
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
        self._generar_provincias()

        # Generar datos de concesionarios
        self._generar_concesionarios()

        self.stdout.write(
            self.style.SUCCESS('\n✅ Generación completada')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 70)
        )

    def _generar_provincias(self):
        """Genera registros de prueba por cada provincia"""
        self.stdout.write(
            self.style.WARNING('\n📍 Generando datos de provincias...')
        )

        from datetime import datetime
        from apps.stock.ai_vehicle_generator import generar_datos_vehiculo_aleatorio

        contador = 0
        for provincia in PROVINCIAS_ESPAÑA:
            try:
                # Generar 1-3 vehículos por provincia
                for _ in range(2):
                    datos_vehiculo = generar_datos_vehiculo_aleatorio()

                    Stock.objects.create(
                        bastidor=f"{provincia.upper()[:3]}-{contador:05d}",
                        marca=datos_vehiculo.get('marca', 'Desconocida'),
                        modelo=datos_vehiculo.get('modelo', 'Desconocido'),
                        provincia=provincia,
                        nom_concesionario=f'Concesionario {provincia}',
                        nom_proveedor=f'Proveedor {provincia}',
                        color=datos_vehiculo.get('color', 'Blanco'),
                        anio_matricula=datos_vehiculo.get('anio', 2020),
                        kilometros=datos_vehiculo.get('kilometros', 50000),
                        precio_venta=datos_vehiculo.get('precio', 15000),
                    )
                    contador += 1

                self.stdout.write(
                    f'✔️  {provincia}: {2} vehículos creados'
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error en {provincia}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'✅ {contador} vehículos generados por provincias')
        )

    def _generar_concesionarios(self):
        """Genera registros de prueba por cada concesionario"""
        self.stdout.write(
            self.style.WARNING('\n🏢 Generando datos de concesionarios...')
        )

        from apps.stock.ai_vehicle_generator import generar_datos_vehiculo_aleatorio

        contador = 0
        for concesionario in CONCESIONARIOS_ESPAÑA:
            try:
                # Generar 3-5 vehículos por concesionario
                for i in range(3):
                    datos_vehiculo = generar_datos_vehiculo_aleatorio()

                    Stock.objects.create(
                        bastidor=f"{concesionario['id']}-{i:05d}",
                        marca=datos_vehiculo.get('marca', 'Desconocida'),
                        modelo=datos_vehiculo.get('modelo', 'Desconocido'),
                        provincia=concesionario['provincia'],
                        nom_concesionario=concesionario['nombre'],
                        id_concesionario=concesionario['id'],
                        nom_proveedor=f"Proveedor {concesionario['nombre']}",
                        color=datos_vehiculo.get('color', 'Blanco'),
                        anio_matricula=datos_vehiculo.get('anio', 2020),
                        kilometros=datos_vehiculo.get('kilometros', 50000),
                        precio_venta=datos_vehiculo.get('precio', 15000),
                    )
                    contador += 1

                self.stdout.write(
                    f'✔️  {concesionario["nombre"]} ({concesionario["provincia"]}): 3 vehículos'
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error en {concesionario["nombre"]}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'✅ {contador} vehículos generados por concesionarios')
        )
