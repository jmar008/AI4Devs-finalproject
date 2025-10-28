"""
Comando Django para generar todas las provincias españolas en la base de datos
"""
from django.core.management.base import BaseCommand
from apps.authentication.models import Provincia

PROVINCIAS_ESPAÑA = [
    ('01', 'Álava'),
    ('02', 'Albacete'),
    ('03', 'Alicante'),
    ('04', 'Almería'),
    ('05', 'Asturias'),
    ('06', 'Ávila'),
    ('07', 'Badajoz'),
    ('08', 'Barcelona'),
    ('09', 'Burgos'),
    ('10', 'Cáceres'),
    ('11', 'Cádiz'),
    ('12', 'Cantabria'),
    ('13', 'Castellón'),
    ('14', 'Ciudad Real'),
    ('15', 'Córdoba'),
    ('16', 'Cuenca'),
    ('17', 'Girona'),
    ('18', 'Granada'),
    ('19', 'Guadalajara'),
    ('20', 'Guipúzcoa'),
    ('21', 'Huesca'),
    ('22', 'Jaén'),
    ('23', 'La Coruña'),
    ('24', 'La Rioja'),
    ('25', 'Las Palmas'),
    ('26', 'León'),
    ('27', 'Lleida'),
    ('28', 'Lugo'),
    ('29', 'Madrid'),
    ('30', 'Málaga'),
    ('31', 'Murcia'),
    ('32', 'Navarra'),
    ('33', 'Ourense'),
    ('34', 'Palencia'),
    ('35', 'Palma de Mallorca'),
    ('36', 'Pamplona'),
    ('37', 'Pontevedra'),
    ('38', 'Salamanca'),
    ('39', 'Segovia'),
    ('40', 'Sevilla'),
    ('41', 'Soria'),
    ('42', 'Tarragona'),
    ('43', 'Teruel'),
    ('44', 'Toledo'),
    ('45', 'Valencia'),
    ('46', 'Valladolid'),
    ('47', 'Vizcaya'),
    ('48', 'Zamora'),
    ('49', 'Zaragoza'),
]


class Command(BaseCommand):
    help = 'Genera todas las provincias españolas en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Elimina todas las provincias antes de generar nuevas'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=' * 70)
        )
        self.stdout.write(
            self.style.SUCCESS('🗺️  GENERANDO PROVINCIAS ESPAÑOLAS')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 70)
        )

        # Si --limpiar está activo
        if options.get('limpiar'):
            self.stdout.write(
                self.style.WARNING('\n🗑️  Limpiando provincias anteriores...')
            )
            cantidad_eliminada, _ = Provincia.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f'✅ {cantidad_eliminada} provincias eliminadas')
            )

        # Generar provincias
        self._generar_provincias()

        self.stdout.write(
            self.style.SUCCESS('\n✅ Generación completada')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 70)
        )

    def _generar_provincias(self):
        """Genera todas las provincias españolas"""
        self.stdout.write(
            self.style.WARNING('\n📍 Generando provincias de España...')
        )

        contador_creadas = 0
        contador_existentes = 0

        for codigo, nombre in PROVINCIAS_ESPAÑA:
            try:
                provincia, creada = Provincia.objects.get_or_create(
                    codigo=codigo,
                    defaults={'nombre': nombre}
                )

                if creada:
                    self.stdout.write(
                        f'✔️  Creada: {nombre} (código: {codigo})'
                    )
                    contador_creadas += 1
                else:
                    self.stdout.write(
                        f'ℹ️  Existente: {nombre} (código: {codigo})'
                    )
                    contador_existentes += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error con {nombre}: {str(e)}')
                )

        total = contador_creadas + contador_existentes
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Provincias procesadas: {total}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'   • Nuevas: {contador_creadas}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'   • Existentes: {contador_existentes}')
        )
