"""
Script manual para ejecutar la migración de Stock a Histórico y scraping de coches.net
Puede ejecutarse manualmente o mediante el scheduler automático
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealaai.settings.development')
django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Migra Stock a Histórico y scrapeía nuevos vehículos de coches.net'
    )
    parser.add_argument(
        '--paginas',
        type=int,
        default=5,
        help='Número de páginas a scrapeiar (default: 5)'
    )
    parser.add_argument(
        '--cantidad',
        type=int,
        default=50,
        help='Número de vehículos a crear (default: 50)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Modo debug'
    )

    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("🚀 MIGRACIÓN DE STOCK Y SCRAPING DE COCHES.NET")
    print("=" * 70 + "\n")

    try:
        call_command(
            'migrate_stock_and_scrape',
            paginas=args.paginas,
            cantidad=args.cantidad,
            debug=args.debug,
            verbosity=2
        )
        print("\n" + "=" * 70)
        print("✅ Proceso completado exitosamente")
        print("=" * 70 + "\n")
        sys.exit(0)

    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ Error: {str(e)}")
        print("=" * 70 + "\n")
        sys.exit(1)
