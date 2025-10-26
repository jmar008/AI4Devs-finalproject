"""
Comando Django para migrar stock a histórico y actualizar con nuevos datos de coches.net
Ejecuta a las 1:00 AM todos los días
"""
import logging
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.stock.models import Stock, StockHistorico
from apps.stock.scrapers import scrape_coches_net, crear_registro_stock
from apps.stock.ai_vehicle_generator import generar_vehiculos_con_ia

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Migra datos de stock a histórico y actualiza stock con nuevos vehículos de coches.net'

    def add_arguments(self, parser):
        parser.add_argument(
            '--paginas',
            type=int,
            default=5,
            help='Número de páginas a scrapeiar de coches.net (default: 5)'
        )
        parser.add_argument(
            '--cantidad',
            type=int,
            default=50,
            help='Número de vehículos a crear (si scraping falla) (default: 50)'
        )
        parser.add_argument(
            '--usar-ia',
            action='store_true',
            help='Usar IA para generar datos de vehículos más realistas (requiere configuración OpenRouter)'
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Habilita modo debug'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """Ejecuta la migración de stock"""
        debug = options.get('debug', False)
        paginas = options.get('paginas', 5)
        cantidad = options.get('cantidad', 50)
        usar_ia = options.get('usar_ia', False)

        self.stdout.write(
            self.style.SUCCESS('=' * 60)
        )
        self.stdout.write(
            self.style.SUCCESS(f'Iniciando migración de Stock - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        )
        if usar_ia:
            self.stdout.write(
                self.style.SUCCESS('🤖 Modo: Generación con IA (datos realistas)')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('📊 Modo: Scraping tradicional')
            )
        self.stdout.write(
            self.style.SUCCESS('=' * 60)
        )

        try:
            # Paso 1: Migrar datos actuales de Stock a StockHistorico
            self.stdout.write(
                self.style.WARNING('\n📋 PASO 1: Migrando datos de Stock a StockHistorico...')
            )
            self._migrar_stock_a_historico(debug)

            # Paso 2: Limpiar tabla de Stock
            self.stdout.write(
                self.style.WARNING('\n🧹 PASO 2: Limpiando tabla de Stock...')
            )
            self._limpiar_stock(debug)

            # Paso 3: Scrapeiar nuevos datos de coches.net o generar con IA
            if usar_ia:
                self.stdout.write(
                    self.style.WARNING('\n🤖 PASO 3: Generando vehículos con IA...')
                )
                vehiculos_scrapeados = self._generar_vehiculos_ia(cantidad, debug)
            else:
                self.stdout.write(
                    self.style.WARNING('\n🔍 PASO 3: Scrapeando nuevos vehículos de coches.net...')
                )
                vehiculos_scrapeados = self._scrapeiar_vehiculos(paginas, debug)

            # Paso 4: Insertar nuevos datos en Stock
            self.stdout.write(
                self.style.WARNING('\n➕ PASO 4: Insertando nuevos vehículos en Stock...')
            )
            self._insertar_nuevos_vehiculos(vehiculos_scrapeados, cantidad, debug)

            self.stdout.write(
                self.style.SUCCESS('\n✅ Migración completada exitosamente')
            )
            self.stdout.write(
                self.style.SUCCESS('=' * 60)
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error durante la migración: {str(e)}')
            )
            logger.error(f"Error en migración de stock: {str(e)}", exc_info=True)
            raise

    def _migrar_stock_a_historico(self, debug=False):
        """Migra todos los registros de Stock a StockHistorico"""
        try:
            stock_actual = Stock.objects.all()
            cantidad_registros = stock_actual.count()

            if cantidad_registros == 0:
                self.stdout.write(
                    self.style.WARNING('ℹ️  No hay registros en Stock para migrar')
                )
                return

            self.stdout.write(
                f'📊 Encontrados {cantidad_registros} registros en Stock'
            )

            # Crear registros históricos a partir de los actuales
            registros_historicos = []
            for stock in stock_actual:
                historico = StockHistorico(
                    idv=stock.idv,
                    fecha_informe=stock.fecha_informe,
                    bastidor=stock.bastidor,
                    vehicle_key=stock.vehicle_key,
                    vehicle_key2=stock.vehicle_key2,
                    id_concesionario=stock.id_concesionario,
                    nom_concesionario=stock.nom_concesionario,
                    id_proveedor=stock.id_proveedor,
                    nom_proveedor=stock.nom_proveedor,
                    dealer_corto=stock.dealer_corto,
                    provincia=stock.provincia,
                    matricula=stock.matricula,
                    fecha_matriculacion=stock.fecha_matriculacion,
                    fecha_recepcion=stock.fecha_recepcion,
                    marca=stock.marca,
                    modelo=stock.modelo,
                    modelo_comercial=stock.modelo_comercial,
                    id_modelo=stock.id_modelo,
                    modelo_qbi=stock.modelo_qbi,
                    descripcion_modelo_qbi=stock.descripcion_modelo_qbi,
                    modelo_bastidor=stock.modelo_bastidor,
                    anio_matricula=stock.anio_matricula,
                    color=stock.color,
                    color_secundario=stock.color_secundario,
                    cod_color=stock.cod_color,
                    id_color=stock.id_color,
                    kilometros=stock.kilometros,
                    ubicacion=stock.ubicacion,
                    id_tipo_vo=stock.id_tipo_vo,
                    descripcion_tipo_vo=stock.descripcion_tipo_vo,
                    id_estado=stock.id_estado,
                    descripcion_estado=stock.descripcion_estado,
                    tipo_stock=stock.tipo_stock,
                    reservado=stock.reservado,
                    dias_stock=stock.dias_stock,
                    intervalo_dias=stock.intervalo_dias,
                    meses_en_stock=stock.meses_en_stock,
                    dias_stock_fin_mes=stock.dias_stock_fin_mes,
                    intervalo_dias_fin_mes=stock.intervalo_dias_fin_mes,
                    intervalo_dias_vo=stock.intervalo_dias_vo,
                    intervalo_dias_vo_new=stock.intervalo_dias_vo_new,
                    intervalo_km=stock.intervalo_km,
                    interv_km_id=stock.interv_km_id,
                    uds_disponibles_stock=stock.uds_disponibles_stock,
                    uds_reservadas_stock=stock.uds_reservadas_stock,
                    stock_uds=stock.stock_uds,
                    pedido=stock.pedido,
                    categoria=stock.categoria,
                    canal_entrada_vo=stock.canal_entrada_vo,
                    concepto_compra=stock.concepto_compra,
                    importe_compra=stock.importe_compra,
                    importe_rectificativas=stock.importe_rectificativas,
                    importe_reacon=stock.importe_reacon,
                    importe_vales=stock.importe_vales,
                    importe_costo=stock.importe_costo,
                    importe_coste_total=stock.importe_coste_total,
                    precio_venta=stock.precio_venta,
                    precio_anterior=stock.precio_anterior,
                    precio_nuevo=stock.precio_nuevo,
                    diferencia_precios=stock.diferencia_precios,
                    stock_benef_estimado=stock.stock_benef_estimado,
                    publicado=stock.publicado,
                    id_internet=stock.id_internet,
                    link_internet=stock.link_internet,
                    internet_eurotax_compra=stock.internet_eurotax_compra,
                    internet_eurotax_venta=stock.internet_eurotax_venta,
                    internet_anuncios=stock.internet_anuncios,
                    internet_precio_min=stock.internet_precio_min,
                    internet_precio_max=stock.internet_precio_max,
                    precio_internet=stock.precio_internet,
                    internet_fotos=stock.internet_fotos,
                    internet_autorizado=stock.internet_autorizado,
                    status_imaweb=stock.status_imaweb,
                    status_car_imaweb=stock.status_car_imaweb,
                    fecha_primera_publicacion=stock.fecha_primera_publicacion,
                    fecha_ultima_publicacion=stock.fecha_ultima_publicacion,
                    antiguedad_anuncio=stock.antiguedad_anuncio,
                    dias_primera_public=stock.dias_primera_public,
                    uc_dias=stock.uc_dias,
                    internet_dias_public=stock.internet_dias_public,
                    tmaimg=stock.tmaimg,
                    tiene_video=stock.tiene_video,
                    visitas_totales=stock.visitas_totales,
                    llamadas_recibidas=stock.llamadas_recibidas,
                    emails_recibidos=stock.emails_recibidos,
                    visitas_cambio=stock.visitas_cambio,
                    leads_cambio=stock.leads_cambio,
                    visitas_cambio_dias=stock.visitas_cambio_dias,
                    leads_cambio_dias=stock.leads_cambio_dias,
                    flag_lead=stock.flag_lead,
                    stock_leads=stock.stock_leads,
                    prediction=stock.prediction,
                    uds_mes=stock.uds_mes,
                    uds_3mes=stock.uds_3mes,
                    uds_ano=stock.uds_ano,
                    ultimo_cambio=stock.ultimo_cambio,
                    ult_cambio=stock.ult_cambio,
                    fecha_ultimo_cambio=stock.fecha_ultimo_cambio,
                    fecha_ultimo_cambio_2=stock.fecha_ultimo_cambio_2,
                    fecha_ult_cambio=stock.fecha_ult_cambio,
                    dias_desde_ult_cambio=stock.dias_desde_ult_cambio,
                    bastidor_qbi=stock.bastidor_qbi,
                    id_calidad_marca=stock.id_calidad_marca,
                    fecha_ultima_foto_optipix=stock.fecha_ultima_foto_optipix,
                    id_vehiculo_foto_optipix=stock.id_vehiculo_foto_optipix,
                    dias_desde_foto_optipix=stock.dias_desde_foto_optipix,
                    status_foto=stock.status_foto,
                    id_veces_pospuesto=stock.id_veces_pospuesto,
                    veces_pospuesto=stock.veces_pospuesto,
                    xxx=stock.xxx,
                    fecha_snapshot=stock.fecha_snapshot,
                    fecha_insert=timezone.now(),
                )
                registros_historicos.append(historico)

            # Insertar en lotes de 1000
            lote = 1000
            for i in range(0, len(registros_historicos), lote):
                StockHistorico.objects.bulk_create(
                    registros_historicos[i:i + lote],
                    ignore_conflicts=True
                )
                self.stdout.write(
                    f'✔️  Migrados {min(i + lote, len(registros_historicos))}/{len(registros_historicos)} registros'
                )

            self.stdout.write(
                self.style.SUCCESS(f'✅ {cantidad_registros} registros migrados a histórico')
            )

        except Exception as e:
            logger.error(f"Error migrando stock a histórico: {str(e)}", exc_info=True)
            raise

    def _limpiar_stock(self, debug=False):
        """Limpia la tabla de Stock"""
        try:
            cantidad = Stock.objects.all().count()
            Stock.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f'✅ {cantidad} registros eliminados de Stock')
            )
        except Exception as e:
            logger.error(f"Error limpiando stock: {str(e)}", exc_info=True)
            raise

    def _scrapeiar_vehiculos(self, paginas, debug=False):
        """Scrapeía vehículos de coches.net"""
        try:
            self.stdout.write(
                f'🌐 Scrapeando {paginas} páginas de coches.net...'
            )
            vehiculos = scrape_coches_net(paginas=paginas, retraso_segundos=1.5)
            self.stdout.write(
                self.style.SUCCESS(f'✅ {len(vehiculos)} vehículos scrapeados')
            )
            return vehiculos
        except Exception as e:
            logger.warning(f"Error scrapeando coches.net: {str(e)}")
            self.stdout.write(
                self.style.WARNING(f'⚠️  Error en scraping: {str(e)}. Generando datos aleatorios.')
            )
            return []

    def _generar_vehiculos_ia(self, cantidad, debug=False):
        """Genera vehículos usando IA"""
        try:
            self.stdout.write(
                f'🤖 Generando {cantidad} vehículos con IA...'
            )
            vehiculos = generar_vehiculos_con_ia(num_vehiculos=cantidad)
            self.stdout.write(
                self.style.SUCCESS(f'✅ {len(vehiculos)} vehículos generados con IA')
            )
            return vehiculos
        except Exception as e:
            logger.error(f"Error generando vehículos con IA: {str(e)}", exc_info=True)
            self.stdout.write(
                self.style.ERROR(f'❌ Error generando con IA: {str(e)}')
            )
            self.stdout.write(
                self.style.WARNING('⚠️  Revirtiendo a generación aleatoria tradicional...')
            )
            return []

    def _insertar_nuevos_vehiculos(self, vehiculos_scrapeados, cantidad, debug=False):
        """Inserta nuevos vehículos en Stock"""
        try:
            # Si el scraping no obtuvo suficientes resultados, generar datos aleatorios
            if len(vehiculos_scrapeados) < cantidad:
                self.stdout.write(
                    f'⚠️  Scraping obtuvo {len(vehiculos_scrapeados)} vehículos, generando {cantidad - len(vehiculos_scrapeados)} adicionales...'
                )
                diferencia = cantidad - len(vehiculos_scrapeados)
                for _ in range(diferencia):
                    vehiculos_scrapeados.append({})

            # Crear registros de Stock
            nuevos_stock = []
            for i, vehiculo in enumerate(vehiculos_scrapeados[:cantidad]):
                stock = Stock(**crear_registro_stock(vehiculo))
                nuevos_stock.append(stock)

            # Insertar en lotes
            lote = 500
            for i in range(0, len(nuevos_stock), lote):
                Stock.objects.bulk_create(
                    nuevos_stock[i:i + lote],
                    ignore_conflicts=True
                )
                self.stdout.write(
                    f'✔️  Insertados {min(i + lote, len(nuevos_stock))}/{len(nuevos_stock)} vehículos'
                )

            self.stdout.write(
                self.style.SUCCESS(f'✅ {len(nuevos_stock)} nuevos vehículos insertados en Stock')
            )

        except Exception as e:
            logger.error(f"Error insertando vehículos: {str(e)}", exc_info=True)
            raise
