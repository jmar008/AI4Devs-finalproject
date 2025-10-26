from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class StockConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.stock"
    verbose_name = "Gestión de Stock"

    def ready(self):
        """Inicializa el scheduler cuando la aplicación está lista"""
        try:
            from apps.stock.scheduler import schedule_stock_migration
            schedule_stock_migration()
        except Exception as e:
            logger.warning(f"No se pudo inicializar el scheduler: {str(e)}")

