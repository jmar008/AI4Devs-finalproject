"""
Configuración de tareas programadas para ejecutarse a las 1:00 AM diariamente
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

logger = logging.getLogger(__name__)


def schedule_stock_migration():
    """Configura la migración automática de stock para las 1:00 AM"""
    scheduler = BackgroundScheduler()

    # Agregar trabajo: ejecutar migrate_stock_and_scrape a las 1:00 AM todos los días
    scheduler.add_job(
        func=_run_stock_migration,
        trigger="cron",
        hour=1,
        minute=0,
        id='migrate_stock_daily',
        name='Migración diaria de Stock',
        replace_existing=True,
        max_instances=1,
    )

    # Iniciar el scheduler si no está ya en ejecución
    if not scheduler.running:
        scheduler.start()
        logger.info("✅ APScheduler iniciado - Migración de Stock programada para 01:00 AM")


def _run_stock_migration():
    """Ejecuta el comando de migración de stock"""
    try:
        logger.info("🚀 Iniciando migración programada de Stock...")
        call_command(
            'migrate_stock_and_scrape',
            paginas=5,
            cantidad=50,
            verbosity=2
        )
        logger.info("✅ Migración de Stock completada exitosamente")
    except Exception as e:
        logger.error(f"❌ Error en migración programada: {str(e)}", exc_info=True)
