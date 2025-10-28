"""
Comando Django para generar solo las 49 provincias de España
"""
from django.core.management.base import BaseCommand
from apps.authentication.models import Provincia

class Command(BaseCommand):
    help = 'Genera las 49 provincias de España en la base de datos'

    PROVINCIAS_ESPAÑA = [
        ("01", "Álava"), ("02", "Albacete"), ("03", "Alicante"),
        ("04", "Almería"), ("33", "Asturias"), ("05", "Ávila"),
        ("06", "Badajoz"), ("07", "Palma de Mallorca"), ("08", "Barcelona"),
        ("09", "Burgos"), ("10", "Cáceres"), ("11", "Cádiz"),
        ("39", "Cantabria"), ("12", "Castellón"), ("13", "Ciudad Real"),
        ("14", "Córdoba"), ("15", "La Coruña"), ("16", "Cuenca"),
        ("17", "Girona"), ("18", "Granada"), ("19", "Guadalajara"),
        ("20", "Guipúzcoa"), ("21", "Huelva"), ("22", "Huesca"),
        ("23", "Jaén"), ("26", "La Rioja"), ("24", "León"),
        ("25", "Lleida"), ("27", "Lugo"), ("28", "Madrid"),
        ("29", "Málaga"), ("30", "Murcia"), ("31", "Navarra"),
        ("32", "Ourense"), ("34", "Palencia"), ("35", "Las Palmas"),
        ("36", "Pontevedra"), ("37", "Salamanca"), ("38", "Santa Cruz de Tenerife"),
        ("40", "Segovia"), ("41", "Sevilla"), ("42", "Soria"),
        ("43", "Tarragona"), ("44", "Teruel"), ("45", "Toledo"),
        ("46", "Valencia"), ("47", "Valladolid"), ("48", "Vizcaya"),
        ("49", "Zamora"), ("50", "Zaragoza")
    ]

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS("📍 GENERANDO PROVINCIAS DE ESPAÑA"))
        self.stdout.write("="*60 + "\n")

        created_count = 0
        updated_count = 0

        for codigo, nombre in self.PROVINCIAS_ESPAÑA:
            provincia, created = Provincia.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre}
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"  ✅ Creada: {codigo} - {nombre}")
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"  ℹ️  Ya existe: {codigo} - {nombre}")
                )

        self.stdout.write("\n" + "="*60)
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Proceso completado: {created_count} creadas, {updated_count} ya existían"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f"📊 Total provincias en BD: {Provincia.objects.count()}")
        )
        self.stdout.write("="*60 + "\n")
