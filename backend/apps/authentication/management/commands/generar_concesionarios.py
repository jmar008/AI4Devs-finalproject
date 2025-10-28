from django.core.management.base import BaseCommand
from apps.authentication.models import Concesionario, Provincia
import random

# Datos de concesionarios por provincia
CONCESIONARIOS_DATA = [
    # Madrid
    {
        'provincia': 'Madrid',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Madrid Centro',
                'direccion': 'Calle Gran Vía, 45, Madrid',
                'telefono': '+34 911 123 456',
                'email': 'info@automadrid.es'
            },
            {
                'nombre': 'Concesionario Auto Madrid Norte',
                'direccion': 'Avenida de Burgos, 123, Madrid',
                'telefono': '+34 911 234 567',
                'email': 'norte@automadrid.es'
            },
            {
                'nombre': 'Concesionario Auto Madrid Sur',
                'direccion': 'Calle Toledo, 78, Madrid',
                'telefono': '+34 911 345 678',
                'email': 'sur@automadrid.es'
            }
        ]
    },
    # Barcelona
    {
        'provincia': 'Barcelona',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Barcelona',
                'direccion': 'Paseo de Gracia, 89, Barcelona',
                'telefono': '+34 932 123 456',
                'email': 'info@autobarcelona.es'
            },
            {
                'nombre': 'Concesionario Auto Barcelona Norte',
                'direccion': 'Carrer de Provença, 234, Barcelona',
                'telefono': '+34 932 234 567',
                'email': 'norte@autobarcelona.es'
            }
        ]
    },
    # Valencia
    {
        'provincia': 'Valencia',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Valencia',
                'direccion': 'Calle de la Paz, 12, Valencia',
                'telefono': '+34 963 123 456',
                'email': 'info@autovalencia.es'
            }
        ]
    },
    # Sevilla
    {
        'provincia': 'Sevilla',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Sevilla',
                'direccion': 'Avenida de la Constitución, 56, Sevilla',
                'telefono': '+34 954 123 456',
                'email': 'info@autosevilla.es'
            }
        ]
    },
    # Vizcaya (Bilbao)
    {
        'provincia': 'Vizcaya',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Bilbao',
                'direccion': 'Gran Vía, 78, Bilbao',
                'telefono': '+34 944 123 456',
                'email': 'info@autobilbao.es'
            }
        ]
    },
    # Málaga
    {
        'provincia': 'Málaga',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Málaga',
                'direccion': 'Paseo del Parque, 34, Málaga',
                'telefono': '+34 952 123 456',
                'email': 'info@automálaga.es'
            }
        ]
    },
    # Murcia
    {
        'provincia': 'Murcia',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Murcia',
                'direccion': 'Gran Vía del Escultor, 12, Murcia',
                'telefono': '+34 968 123 456',
                'email': 'info@automurcia.es'
            }
        ]
    },
    # Zaragoza
    {
        'provincia': 'Zaragoza',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Zaragoza',
                'direccion': 'Paseo de la Independencia, 23, Zaragoza',
                'telefono': '+34 976 123 456',
                'email': 'info@autozaragoza.es'
            }
        ]
    },
    # Palma de Mallorca
    {
        'provincia': 'Palma de Mallorca',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Palma',
                'direccion': 'Avinguda Jaume III, 15, Palma',
                'telefono': '+34 971 123 456',
                'email': 'info@autopalma.es'
            }
        ]
    },
    # Las Palmas
    {
        'provincia': 'Las Palmas',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Las Palmas',
                'direccion': 'Calle León y Castillo, 345, Las Palmas',
                'telefono': '+34 928 123 456',
                'email': 'info@autolaspalmas.es'
            }
        ]
    },
    # Alicante
    {
        'provincia': 'Alicante',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Alicante',
                'direccion': 'Rambla Méndez Núñez, 67, Alicante',
                'telefono': '+34 965 123 456',
                'email': 'info@autoalicante.es'
            }
        ]
    },
    # Córdoba
    {
        'provincia': 'Córdoba',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Córdoba',
                'direccion': 'Avenida del Gran Capitán, 8, Córdoba',
                'telefono': '+34 957 123 456',
                'email': 'info@autocordoba.es'
            }
        ]
    },
    # Valladolid
    {
        'provincia': 'Valladolid',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Valladolid',
                'direccion': 'Calle Santiago, 12, Valladolid',
                'telefono': '+34 983 123 456',
                'email': 'info@autovalladolid.es'
            }
        ]
    },
    # León
    {
        'provincia': 'León',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto León',
                'direccion': 'Calle Ancha, 45, León',
                'telefono': '+34 987 123 456',
                'email': 'info@autoleon.es'
            }
        ]
    },
    # Salamanca
    {
        'provincia': 'Salamanca',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Salamanca',
                'direccion': 'Plaza Mayor, 23, Salamanca',
                'telefono': '+34 923 123 456',
                'email': 'info@autosalamanca.es'
            }
        ]
    },
    # Castellón
    {
        'provincia': 'Castellón',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Castellón',
                'direccion': 'Avenida del Mar, 78, Castellón',
                'telefono': '+34 964 123 456',
                'email': 'info@autocastellon.es'
            }
        ]
    },
    # Jaén
    {
        'provincia': 'Jaén',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Jaén',
                'direccion': 'Calle Maestra, 34, Jaén',
                'telefono': '+34 953 123 456',
                'email': 'info@autojaen.es'
            }
        ]
    },
    # Toledo
    {
        'provincia': 'Toledo',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Toledo',
                'direccion': 'Calle Comercio, 56, Toledo',
                'telefono': '+34 925 123 456',
                'email': 'info@autotoledo.es'
            }
        ]
    },
    # Cuenca
    {
        'provincia': 'Cuenca',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Cuenca',
                'direccion': 'Calle Carretería, 12, Cuenca',
                'telefono': '+34 969 123 456',
                'email': 'info@autocuenca.es'
            }
        ]
    },
    # Girona
    {
        'provincia': 'Girona',
        'concesionarios': [
            {
                'nombre': 'Concesionario Auto Girona',
                'direccion': 'Rambla de la Llibertat, 45, Girona',
                'telefono': '+34 972 123 456',
                'email': 'info@autogirona.es'
            }
        ]
    }
]


class Command(BaseCommand):
    help = 'Genera datos de concesionarios para las provincias existentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Limpia todos los concesionarios antes de generar nuevos'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=' * 70)
        )
        self.stdout.write(
            self.style.SUCCESS('🏢 GENERANDO DATOS DE CONCESIONARIOS')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 70)
        )

        # Si --limpiar está activo
        if options.get('limpiar'):
            self.stdout.write(
                self.style.WARNING('\n🗑️  Limpiando concesionarios anteriores...')
            )
            Concesionario.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS('✅ Concesionarios limpiados')
            )

        # Generar datos de concesionarios
        self._generar_concesionarios()

        self.stdout.write(
            self.style.SUCCESS('\n✅ Generación de concesionarios completada')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 70)
        )

    def _generar_concesionarios(self):
        """Genera registros de concesionarios por provincia"""
        self.stdout.write(
            self.style.WARNING('\n🏢 Generando datos de concesionarios...')
        )

        contador = 0
        for provincia_data in CONCESIONARIOS_DATA:
            try:
                # Obtener la provincia
                provincia = Provincia.objects.get(nombre=provincia_data['provincia'])

                # Crear concesionarios para esta provincia
                for concesionario_data in provincia_data['concesionarios']:
                    Concesionario.objects.create(
                        nombre=concesionario_data['nombre'],
                        direccion=concesionario_data['direccion'],
                        telefono=concesionario_data['telefono'],
                        email=concesionario_data['email'],
                        provincia=provincia,
                        activo=True
                    )
                    contador += 1

                self.stdout.write(
                    f'✔️  {provincia.nombre}: {len(provincia_data["concesionarios"])} concesionarios creados'
                )

            except Provincia.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Provincia {provincia_data["provincia"]} no encontrada')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error en {provincia_data["provincia"]}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'✅ {contador} concesionarios generados en total')
        )
