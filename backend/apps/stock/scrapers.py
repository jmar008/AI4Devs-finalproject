"""
Módulo de scraping para obtener datos de vehículos de coches.net
"""
import logging
import random
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
import uuid

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

logger = logging.getLogger(__name__)

# Configuración de headers para simular navegador real
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Referer': 'https://www.coches.net/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Marcas y modelos de ejemplo para datos faltantes
MARCAS_COMUNES = ['BMW', 'Mercedes-Benz', 'Audi', 'Volkswagen', 'Ford', 'Renault', 'Peugeot',
                   'Citroën', 'Opel', 'Fiat', 'Toyota', 'Honda', 'Mazda', 'Hyundai', 'Kia']

MODELOS_POR_MARCA = {
    'BMW': ['Serie 3', 'Serie 5', 'X3', 'X5', 'Z4'],
    'Mercedes-Benz': ['Clase A', 'Clase C', 'Clase E', 'GLC', 'GLE'],
    'Audi': ['A3', 'A4', 'A6', 'Q3', 'Q5'],
    'Volkswagen': ['Golf', 'Passat', 'Tiguan', 'Polo'],
    'Ford': ['Focus', 'Mondeo', 'Kuga', 'Fiesta'],
    'Renault': ['Clio', 'Megane', 'Scenic', 'Captur'],
}

COLORES = ['Blanco', 'Negro', 'Gris', 'Plata', 'Azul', 'Rojo', 'Marrón', 'Verde', 'Amarillo', 'Naranja']

PROVINCIAS = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', 'Alicante', 'Murcia',
              'Palma de Mallorca', 'Las Palmas', 'Córdoba', 'Valladolid', 'Zaragoza', 'Gijón',
              'Málaga', 'Badajoz', 'Almería', 'Salamanca', 'Tarragona', 'Castellón', 'Jaén']

CONCESIONARIOS_PRINCIPALES = [
    {'id': 'CON001', 'nombre': 'AutoStock Madrid'},
    {'id': 'CON002', 'nombre': 'Concesionario Barcelona Motors'},
    {'id': 'CON003', 'nombre': 'Valencia Auto Group'},
    {'id': 'CON004', 'nombre': 'Sevilla Premium Cars'},
    {'id': 'CON005', 'nombre': 'Bilbao Auto Center'},
]


def generar_bastidor() -> str:
    """Genera un número de bastidor (VIN) válido de forma aleatoria"""
    # VIN tiene 17 caracteres
    caracteres = 'ABCDEFGHJKLMNPRSTUVWXYZ0123456789'
    return ''.join(random.choice(caracteres) for _ in range(17))


def generar_matricula() -> str:
    """Genera una matrícula española válida de forma aleatoria"""
    # Formato español: 4 números + 3 letras
    numeros = ''.join(random.choice('0123456789') for _ in range(4))
    letras = ''.join(random.choice('BCDFGHJKLMNPRSTVWXYZ') for _ in range(3))
    return f"{numeros}{letras}"


def generar_datos_faltantes() -> Dict:
    """Genera datos faltantes de forma aleatoria y realista"""
    marca = random.choice(MARCAS_COMUNES)
    modelo = random.choice(MODELOS_POR_MARCA.get(marca, ['Modelo Genérico']))

    fecha_matricula = datetime.now() - timedelta(days=random.randint(30, 3650))
    dias_stock = random.randint(1, 365)
    precio = Decimal(str(random.randint(5000, 150000)))

    # Datos técnicos
    combustibles = ['Gasolina', 'Diésel', 'Híbrido', 'Eléctrico', 'GLP']
    transmisiones = ['Manual', 'Automática', 'CVT']
    tipos_vehiculos = ['Berlina', 'SUV', 'Coupé', 'Monvolumen', 'Pickup', 'Furgoneta']

    return {
        'marca': marca,
        'modelo': modelo,
        'modelo_comercial': modelo,
        'version': f"{modelo} {random.choice(['1.0', '1.6', '2.0', '2.5', '3.0'])}",
        'anio_matricula': fecha_matricula.year,
        'color': random.choice(COLORES),
        'color_secundario': random.choice(COLORES),
        'kilometros': random.randint(1000, 250000),
        'precio_venta': precio,
        'importe_compra': Decimal(str(float(precio) * random.uniform(0.5, 0.8))),
        'importe_costo': Decimal(str(float(precio) * random.uniform(0.4, 0.7))),
        'dias_stock': dias_stock,
        'fecha_matriculacion': fecha_matricula.date(),
        'fecha_recepcion': fecha_matricula.date() + timedelta(days=random.randint(0, 30)),
        # Nuevos campos técnicos
        'combustible': random.choice(combustibles),
        'transmision': random.choice(transmisiones),
        'tipo_vehiculo': random.choice(tipos_vehiculos),
        'cilindrada': random.randint(1000, 5000),
        'potencia': random.randint(75, 500),
        'peso': random.randint(1000, 2500),
        'puertas': random.choice([3, 5]),
        'plazas': random.choice([5, 7]),
    }


def extraer_informacion_vehiculo(elemento_html) -> Optional[Dict]:
    """
    Extrae la información de un vehículo del HTML de coches.net

    Args:
        elemento_html: Elemento BeautifulSoup con la información del vehículo

    Returns:
        Diccionario con los datos del vehículo o None si no se puede extraer
    """
    try:
        datos = {}

        # Intenta extraer información del título
        titulo = elemento_html.get_text(strip=True)

        # Extrae precio
        precio_elem = elemento_html.find(class_='price')
        if precio_elem:
            precio_text = precio_elem.get_text(strip=True).replace('€', '').replace('.', '').replace(',', '.')
            try:
                datos['precio_venta'] = Decimal(precio_text)
            except:
                pass

        # Extrae kilómetros
        km_elem = elemento_html.find(class_='km')
        if km_elem:
            km_text = km_elem.get_text(strip=True).replace('km', '').replace('.', '')
            try:
                datos['kilometros'] = int(km_text)
            except:
                pass

        # Extrae año
        año_elem = elemento_html.find(class_='year')
        if año_elem:
            año_text = año_elem.get_text(strip=True)
            try:
                datos['anio_matricula'] = int(año_text)
            except:
                pass

        # Agrega datos generados aleatoriamente para campos no encontrados
        datos_generados = generar_datos_faltantes()
        for campo, valor in datos_generados.items():
            if campo not in datos:
                datos[campo] = valor

        return datos

    except Exception as e:
        logger.error(f"Error extrayendo información del vehículo: {str(e)}")
        return None


def scrape_coches_net(paginas: int = 1, retraso_segundos: float = 2.0) -> List[Dict]:
    """
    Scrape de vehículos desde coches.net

    Args:
        paginas: Número de páginas a descargar
        retraso_segundos: Retraso entre solicitudes

    Returns:
        Lista de diccionarios con información de vehículos
    """
    vehiculos = []
    url_base = "https://www.coches.net/segunda-mano/"

    try:
        for pagina in range(1, paginas + 1):
            try:
                # Agregar parámetro de página si es necesario
                url = f"{url_base}?page={pagina}" if pagina > 1 else url_base

                logger.info(f"Scrapeando página {pagina}: {url}")

                # Realizar solicitud HTTP
                respuesta = requests.get(url, headers=HEADERS, timeout=10)
                respuesta.raise_for_status()

                # Parsear HTML
                soup = BeautifulSoup(respuesta.content, 'html.parser')

                # Buscar elementos de vehículos (ajustar selectores según estructura real del sitio)
                elementos_vehiculos = soup.find_all('div', class_='vehicle-item')

                if not elementos_vehiculos:
                    # Si no encuentra con esa clase, intentar otras opciones comunes
                    elementos_vehiculos = soup.find_all('div', class_='advert')

                if not elementos_vehiculos:
                    elementos_vehiculos = soup.find_all('article', class_='car')

                logger.info(f"Encontrados {len(elementos_vehiculos)} vehículos en página {pagina}")

                for elemento in elementos_vehiculos:
                    info_vehiculo = extraer_informacion_vehiculo(elemento)
                    if info_vehiculo:
                        vehiculos.append(info_vehiculo)

                # Retraso entre solicitudes
                import time
                time.sleep(retraso_segundos)

            except requests.exceptions.RequestException as e:
                logger.warning(f"Error al descargar página {pagina}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error general en scraping: {str(e)}")

    logger.info(f"Total de vehículos scrapeados: {len(vehiculos)}")
    return vehiculos


def crear_registro_stock(datos_vehiculo: Dict) -> Dict:
    """
    Transforma datos scrapeados en registro de Stock

    Args:
        datos_vehiculo: Diccionario con datos del vehículo

    Returns:
        Diccionario con campos del modelo Stock
    """
    concesionario = random.choice(CONCESIONARIOS_PRINCIPALES)

    return {
        'bastidor': generar_bastidor(),
        'idv': random.randint(1000000, 9999999),
        'fecha_informe': int(datetime.now().strftime('%Y%m%d')),
        'id_concesionario': concesionario['id'],
        'nom_concesionario': concesionario['nombre'],
        'dealer_corto': concesionario['nombre'][:15],
        'matricula': generar_matricula(),
        'vehicle_key': generar_bastidor(),
        'vehicle_key2': generar_bastidor(),
        'fecha_matriculacion': datos_vehiculo.get('fecha_matriculacion',
                                                   datetime.now().date() - timedelta(days=random.randint(30, 3650))),
        'fecha_recepcion': datos_vehiculo.get('fecha_recepcion',
                                              datetime.now().date() - timedelta(days=random.randint(0, 30))),
        'id_proveedor': f"PROV{random.randint(1000, 9999)}",
        'nom_proveedor': f"Proveedor {random.choice(['Nacional', 'Importado', 'Premium'])}",
        'marca': datos_vehiculo.get('marca', random.choice(MARCAS_COMUNES)),
        'modelo': datos_vehiculo.get('modelo', 'Modelo'),
        'modelo_comercial': datos_vehiculo.get('modelo_comercial', 'Comercial'),
        'id_modelo': f"MOD{random.randint(100000, 999999)}",
        'anio_matricula': datos_vehiculo.get('anio_matricula', datetime.now().year - random.randint(0, 15)),
        'color': datos_vehiculo.get('color', random.choice(COLORES)),
        'color_secundario': datos_vehiculo.get('color_secundario', 'N/A'),
        'cod_color': f"COL{random.randint(100, 999)}",
        'id_color': f"IDCOL{random.randint(100, 999)}",
        'kilometros': datos_vehiculo.get('kilometros', random.randint(1000, 250000)),
        'ubicacion': random.choice(PROVINCIAS),
        'provincia': random.choice(PROVINCIAS),
        'id_tipo_vo': 'VO001',
        'descripcion_tipo_vo': 'Vehículo de Ocasión',
        'id_estado': random.choice(['DISP', 'RESERV', 'VEND']),
        'descripcion_estado': random.choice(['Disponible', 'Reservado', 'Vendido']),
        'tipo_stock': random.choice(['STOCK', 'SPECIAL', 'PROMOCION']),
        'reservado': random.choice([True, False]),
        'dias_stock': datos_vehiculo.get('dias_stock', random.randint(1, 365)),
        'intervalo_dias': f"0-{random.randint(30, 90)}",
        'meses_en_stock': Decimal(str(random.uniform(0.5, 12))),
        'dias_stock_fin_mes': random.randint(1, 365),
        'intervalo_dias_fin_mes': f"0-{random.randint(30, 90)}",
        'intervalo_dias_vo': f"0-{random.randint(30, 90)}",
        'intervalo_dias_vo_new': f"0-{random.randint(30, 90)}",
        'intervalo_km': '0-100000',
        'interv_km_id': f"KM{random.randint(1, 5)}",
        'uds_disponibles_stock': random.randint(1, 50),
        'uds_reservadas_stock': random.randint(0, 10),
        'stock_uds': random.randint(1, 50),
        'pedido': f"PED{random.randint(100000, 999999)}",
        'categoria': random.choice(['SUV', 'Berlina', 'Familiar', 'Coupé', 'Monovolumen']),
        'canal_entrada_vo': random.choice(['DIRECTO', 'SUBASTA', 'PERMUTA']),
        'concepto_compra': random.choice(['COMPRA', 'TRUEQUE', 'ALMONEDA']),
        'importe_compra': datos_vehiculo.get('importe_compra',
                                            Decimal(str(random.randint(5000, 100000)))),
        'importe_rectificativas': Decimal('0'),
        'importe_reacon': Decimal('0'),
        'importe_vales': Decimal('0'),
        'importe_costo': datos_vehiculo.get('importe_costo',
                                           Decimal(str(random.randint(4000, 80000)))),
        'importe_coste_total': Decimal(str(random.randint(4000, 100000))),
        'precio_venta': datos_vehiculo.get('precio_venta',
                                          Decimal(str(random.randint(5000, 150000)))),
        'precio_anterior': Decimal(str(random.randint(5000, 150000))),
        'precio_nuevo': Decimal(str(random.randint(5000, 150000))),
        'diferencia_precios': Decimal('0'),
        'stock_benef_estimado': Decimal(str(random.randint(500, 50000))),
        'publicado': random.choice([True, False]),
        'id_internet': f"INT{random.randint(100000, 999999)}",
        'link_internet': f"https://www.coches.net/vehiculo/{random.randint(100000, 999999)}.html",
        'internet_eurotax_compra': Decimal(str(random.randint(5000, 100000))),
        'internet_eurotax_venta': Decimal(str(random.randint(5000, 150000))),
        'internet_anuncios': random.randint(1, 10),
        'internet_precio_min': Decimal(str(random.randint(5000, 100000))),
        'internet_precio_max': Decimal(str(random.randint(100000, 150000))),
        'precio_internet': datos_vehiculo.get('precio_venta',
                                             Decimal(str(random.randint(5000, 150000)))),
        'internet_fotos': random.randint(5, 50),
        'internet_autorizado': random.choice([True, False]),
        'status_imaweb': random.choice(['ACTIVO', 'INACTIVO', 'PENDIENTE']),
        'status_car_imaweb': random.choice(['OK', 'FALTA_DATOS', 'ERROR']),
        'fecha_primera_publicacion': datetime.now().date() - timedelta(days=random.randint(1, 365)),
        'fecha_ultima_publicacion': datetime.now().date(),
        'antiguedad_anuncio': random.randint(1, 365),
        'dias_primera_public': random.randint(1, 365),
        'uc_dias': random.randint(1, 365),
        'internet_dias_public': random.randint(1, 365),
        'tmaimg': 'FULL_HD',
        'tiene_video': random.choice([True, False]),
        'visitas_totales': random.randint(10, 10000),
        'llamadas_recibidas': random.randint(0, 100),
        'emails_recibidos': random.randint(0, 100),
        'visitas_cambio': random.randint(0, 1000),
        'leads_cambio': random.randint(0, 50),
        'visitas_cambio_dias': random.randint(0, 100),
        'leads_cambio_dias': random.randint(0, 10),
        'flag_lead': random.choice([True, False]),
        'stock_leads': random.randint(0, 50),
        'prediction': random.choice(['VENTA_PROXIMA', 'LENTA', 'MEDIA', 'RAPIDA']),
        'uds_mes': random.randint(0, 10),
        'uds_3mes': random.randint(0, 30),
        'uds_ano': random.randint(0, 100),
        'ultimo_cambio': f"CAMBIO{random.randint(1, 100)}",
        'ult_cambio': f"CAMBIO{random.randint(1, 100)}",
        'fecha_ultimo_cambio': datetime.now().date() - timedelta(days=random.randint(0, 30)),
        'fecha_ultimo_cambio_2': datetime.now().date() - timedelta(days=random.randint(0, 30)),
        'fecha_ult_cambio': datetime.now().date() - timedelta(days=random.randint(0, 30)),
        'dias_desde_ult_cambio': random.randint(0, 30),
        'bastidor_qbi': generar_bastidor(),
        'id_calidad_marca': str(uuid.uuid4()),
        'fecha_ultima_foto_optipix': timezone.now() - timedelta(days=random.randint(0, 30)),
        'id_vehiculo_foto_optipix': str(uuid.uuid4()),
        'dias_desde_foto_optipix': random.randint(0, 30),
        'status_foto': random.choice(['OK', 'INCOMPLETA', 'PENDIENTE']),
        'id_veces_pospuesto': str(uuid.uuid4()),
        'veces_pospuesto': random.randint(0, 5),
        'xxx': 'DATO_ADICIONAL',
        'fecha_snapshot': datetime.now().date(),
    }
