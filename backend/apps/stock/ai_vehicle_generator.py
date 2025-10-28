"""
Generador de datos de vehículos usando IA para mayor realismo y coherencia
"""
import logging
import random
import json
import time
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional
import uuid

from django.conf import settings
from openai import OpenAI
import httpx

from apps.stock.scrapers import (
    generar_bastidor, generar_matricula, COLORES, PROVINCIAS,
    CONCESIONARIOS_PRINCIPALES
)

logger = logging.getLogger(__name__)


class AIVehicleGenerator:
    """Generador de datos de vehículos usando IA"""

    def __init__(self):
        """Inicializa el cliente de OpenAI con configuración para Zscaler"""
        # Cliente httpx con SSL deshabilitado para Zscaler
        http_client = httpx.Client(verify=False)

        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_API_BASE,
            http_client=http_client,
        )
        self.model = settings.DEEPSEEK_MODEL
        # Solo usar el modelo principal, sin fallbacks para asegurar consistencia
        self.fallback_models = []

    def generate_vehicles(self, count: int = 10, brand: Optional[str] = None) -> List[Dict]:
        """
        Genera vehículos usando IA

        Args:
            count: Número de vehículos a generar
            brand: Marca específica (opcional)

        Returns:
            Lista de diccionarios con datos de vehículos generados por IA
        """
        vehicles = []

        # Optimización para generar 1000 coches eficientemente
        # Usar lotes más grandes pero manejables para openai/gpt-oss-20b
        if count >= 1000:
            batch_size = 30  # Lotes de 15 para generación masiva eficiente
        elif count > 100:
            batch_size = 20
        elif count > 50:
            batch_size = 10
        else:
            batch_size = 5  # Lotes pequeños para cantidades menores

        logger.info(f"Generando {count} vehículos con IA en lotes de {batch_size}")

        for i in range(0, count, batch_size):
            batch_count = min(batch_size, count - i)
            try:
                batch = self._generate_batch(batch_count, brand)
                vehicles.extend(batch)
                logger.info(f"✓ Lote completado: {len(batch)} vehículos (total: {len(vehicles)}/{count})")

                # Delay optimizado entre lotes para eficiencia con lotes más grandes
                if i + batch_size < count:
                    time.sleep(1.0)  # 1 segundo entre lotes para buen balance entre velocidad y estabilidad

            except Exception as e:
                logger.error(f"❌ Error generando lote de vehículos: {str(e)}")
                # Si falla la IA, generar datos básicos para no bloquear
                logger.warning(f"⚠️  Usando generación fallback para {batch_count} vehículos")
                for _ in range(batch_count):
                    vehicles.append(self._generate_fallback_vehicle(brand))

        return vehicles

    def _generate_batch(self, count: int, brand: Optional[str] = None) -> List[Dict]:
        """Genera un lote de vehículos usando IA"""

        prompt = self._create_prompt(count, brand)

        # Solo usar el modelo principal openai/gpt-oss-20b
        models_to_try = [self.model]
        last_error = None

        for model in models_to_try:
            try:
                logger.info(f"Generando vehículos con modelo: {model}")

                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Eres un experto en el mercado de vehículos de ocasión en España. "
                                     "Generas datos realistas y coherentes de vehículos usados con relaciones "
                                     "lógicas entre año, kilometraje, precio y condición. "
                                     "Siempre respondes ÚNICAMENTE con JSON válido, sin texto adicional."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,  # Temperatura moderada para consistencia
                    max_tokens=4000,  # Aumentado proporcionalmente al batch_size para lotes más grandes
                    extra_body={
                        "data_collection": "allow"
                    }
                )

                # Parsear respuesta JSON con mejor manejo de errores
                content = response.choices[0].message.content
                logger.debug(f"Respuesta cruda del modelo {model}: {content[:500]}...")

                try:
                    vehicles_data = json.loads(content)
                except json.JSONDecodeError as e:
                    logger.error(f"❌ Error parseando JSON de {model}: {str(e)}")
                    logger.error(f"Contenido recibido: {content}")

                    # Intentar limpiar el JSON si tiene problemas comunes
                    try:
                        cleaned_content = self._clean_json_response(content)
                        vehicles_data = json.loads(cleaned_content)
                        logger.info(f"✓ JSON limpiado exitosamente para {model}")
                    except json.JSONDecodeError:
                        logger.error(f"❌ No se pudo limpiar el JSON de {model}")
                        # Usar fallback en lugar de fallar
                        logger.warning(f"⚠️  Usando generación fallback para {count} vehículos")
                        return [self._generate_fallback_vehicle(brand) for _ in range(count)]

                # Validar y completar datos
                vehicles = []
                for vehicle_data in vehicles_data.get('vehicles', []):
                    vehicle = self._complete_vehicle_data(vehicle_data)
                    vehicles.append(vehicle)

                logger.info(f"✓ Generados {len(vehicles)} vehículos con {model}")
                return vehicles

            except Exception as e:
                error_str = str(e)
                logger.error(f"❌ Error con modelo {model}: {error_str}")
                last_error = e
                # Si hay error, usar fallback inmediatamente
                logger.warning(f"⚠️  Error con {model}, usando generación fallback para {count} vehículos")
                return [self._generate_fallback_vehicle(brand) for _ in range(count)]

    def _create_prompt(self, count: int, brand: Optional[str] = None) -> str:
        """Crea el prompt para generar vehículos"""

        brand_constraint = f"de la marca {brand}" if brand else "de marcas populares en España (BMW, Mercedes, Audi, VW, Ford, Renault, Peugeot, etc.)"

        return f"""Genera {count} vehículos de ocasión realistas {brand_constraint} para un concesionario en España.

INSTRUCCIONES CRÍTICAS PARA JSON VÁLIDO:
- Responde ÚNICAMENTE con JSON válido - nada más, ningún texto adicional
- NO incluyas explicaciones, comentarios o formato markdown
- El JSON debe empezar con {{ y terminar con }} exactamente
- Todas las claves deben estar entre comillas dobles
- Todas las cadenas de texto deben estar entre comillas dobles
- NO uses comillas simples para strings
- Los números no van entre comillas
- El array "vehicles" debe contener exactamente {count} objetos

Para cada vehículo, considera relaciones lógicas:
- Coches más antiguos tienen más kilómetros (ej: 2015 → 80,000-150,000 km)
- Coches recientes tienen menos kilómetros (ej: 2022 → 10,000-50,000 km)
- Precio coherente con año, km y marca (ej: BMW 2020 con 30,000km → 25,000-35,000€)
- Modelos y versiones reales de cada marca
- Potencia y cilindrada coherentes con el modelo

Formato JSON exacto requerido (ejemplo con 2 vehículos):
{{
  "vehicles": [
    {{
      "marca": "BMW",
      "modelo": "Serie 3",
      "version": "320d xDrive",
      "anio_matricula": 2019,
      "kilometros": 85000,
      "precio_venta": 24500,
      "color": "Gris",
      "combustible": "Diésel",
      "transmision": "Automática",
      "tipo_vehiculo": "Berlina",
      "cilindrada": 1995,
      "potencia": 190,
      "puertas": 5,
      "plazas": 5,
      "descripcion": "BMW Serie 3 en excelente estado, único propietario, mantenimiento oficial"
    }},
    {{
      "marca": "Mercedes",
      "modelo": "Clase C",
      "version": "C200",
      "anio_matricula": 2018,
      "kilometros": 95000,
      "precio_venta": 23000,
      "color": "Blanco",
      "combustible": "Gasolina",
      "transmision": "Automática",
      "tipo_vehiculo": "Berlina",
      "cilindrada": 1998,
      "potencia": 184,
      "puertas": 5,
      "plazas": 5,
      "descripcion": "Mercedes Clase C bien conservado, 1 propietario, revisiones al día"
    }}
  ]
}}

IMPORTANTE:
1. El JSON debe ser válido y parseable
2. Los precios deben ser coherentes (vehículos premium más caros)
3. El kilometraje debe ser realista según el año
4. Los modelos y versiones deben existir realmente
5. Cada descripción debe mencionar características relevantes del vehículo
6. NO agregar texto fuera del JSON"""

    def _complete_vehicle_data(self, ai_data: Dict) -> Dict:
        """Completa los datos del vehículo con campos adicionales"""

        # Extraer datos de IA
        marca = ai_data.get('marca', 'Volkswagen')
        modelo = ai_data.get('modelo', 'Golf')
        version = ai_data.get('version', '1.6 TDI')
        anio = ai_data.get('anio_matricula', datetime.now().year - random.randint(3, 10))
        km = ai_data.get('kilometros', random.randint(20000, 150000))
        precio = Decimal(str(ai_data.get('precio_venta', random.randint(10000, 30000))))

        # Calcular fechas coherentes
        fecha_matricula = datetime.now() - timedelta(days=(datetime.now().year - anio) * 365 + random.randint(0, 364))
        dias_stock = random.randint(1, 180)  # Máximo 6 meses en stock
        fecha_recepcion = datetime.now() - timedelta(days=dias_stock)

        # Calcular costos coherentes con máximo 10% de diferencia
        # El precio de compra está entre 90% y 100% del precio de venta
        margen = random.uniform(0.90, 1.00)
        importe_compra = Decimal(str(float(precio) * margen))
        # El costo está muy cerca del precio de compra (±2%)
        importe_costo = Decimal(str(float(importe_compra) * random.uniform(0.98, 1.02)))

        concesionario = random.choice(CONCESIONARIOS_PRINCIPALES)

        return {
            # Datos de IA
            'marca': marca,
            'modelo': modelo,
            'version': version,
            'modelo_comercial': modelo,
            'anio_matricula': anio,
            'kilometros': km,
            'precio_venta': precio,
            'color': ai_data.get('color', random.choice(COLORES)),
            'combustible': ai_data.get('combustible', 'Diésel'),
            'transmision': ai_data.get('transmision', 'Manual'),
            'tipo_vehiculo': ai_data.get('tipo_vehiculo', 'Berlina'),
            'cilindrada': ai_data.get('cilindrada', 1600),
            'potencia': ai_data.get('potencia', 110),
            'puertas': ai_data.get('puertas', 5),
            'plazas': ai_data.get('plazas', 5),

            # Datos calculados
            'fecha_matriculacion': fecha_matricula.date(),
            'fecha_recepcion': fecha_recepcion.date(),
            'dias_stock': dias_stock,
            'importe_compra': importe_compra,
            'importe_costo': importe_costo,

            # Datos generados
            'color_secundario': ai_data.get('color', random.choice(COLORES)),
            'peso': random.randint(1200, 2000),
            'bastidor': generar_bastidor(),
            'matricula': generar_matricula(),
            'ubicacion': random.choice(PROVINCIAS),
            'provincia': random.choice(PROVINCIAS),

            # Datos del concesionario
            'id_concesionario': concesionario['id'],
            'nom_concesionario': concesionario['nombre'],
            'dealer_corto': concesionario['nombre'][:15],
        }

    def _generate_fallback_vehicle(self, brand: Optional[str] = None) -> Dict:
        """Genera un vehículo con datos básicos si falla la IA"""

        from apps.stock.scrapers import generar_datos_faltantes

        datos = generar_datos_faltantes()

        if brand:
            datos['marca'] = brand

        logger.warning("Usando generación fallback (sin IA) para vehículo")
        return datos

    def _clean_json_response(self, content: str) -> str:
        """Limpia la respuesta JSON para manejar errores comunes de los modelos de IA"""

        import re

        # Remover posibles textos introductorios o explicativos
        start_idx = content.find('{')
        if start_idx > 0:
            content = content[start_idx:]

        # Intentar encontrar el final del JSON válido
        # Buscar el último '}' que tenga un matching '{'
        brace_count = 0
        last_valid_end = -1

        for i, char in enumerate(content):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    last_valid_end = i

        # Si encontramos un final válido, usar solo esa parte
        if last_valid_end >= 0:
            content = content[:last_valid_end + 1]

        # Limpiar caracteres de escape problemáticos
        content = re.sub(r"'([^']*)'", r'"\1"', content)  # Comillas simples a dobles
        content = content.replace('\\"', '"')  # Corregir escapes incorrectos

        # Asegurar que las claves estén entre comillas dobles
        # Patrón más específico para evitar romper JSON ya válido
        content = re.sub(r'(?<![\"\'])(\w+)(?=\s*:)', r'"\1"', content)

        # Corregir strings truncadas al final
        # Si el contenido termina con una cadena incompleta, intentar cerrarla
        if content.count('"') % 2 == 1:  # Número impar de comillas
            # Buscar la última comilla y agregar cierre si es necesario
            last_quote_idx = content.rfind('"')
            if last_quote_idx >= 0:
                # Verificar si después de la última comilla hay contenido sin cerrar
                after_quote = content[last_quote_idx + 1:]
                if after_quote and not after_quote[-1] in [',', '}', ']', ' ']:
                    # Agregar comilla de cierre antes del último carácter válido
                    content = content.rstrip()
                    if content.endswith(','):
                        content = content[:-1] + '",'
                    elif content.endswith('}'):
                        content = content[:-1] + '"}'
                    elif content.endswith(']'):
                        content = content[:-1] + '"]'
                    else:
                        content += '"'

        # Limpiar espacios en blanco extra
        content = content.strip()

        # Asegurar que termine con }
        if content and not content.endswith('}'):
            content += '}'

        return content


def generar_vehiculos_con_ia(num_vehiculos: int = 10, marca: Optional[str] = None) -> List[Dict]:
    """
    Función de conveniencia para generar vehículos con IA

    Args:
        num_vehiculos: Cantidad de vehículos a generar
        marca: Marca específica (opcional)

    Returns:
        Lista de diccionarios con datos de vehículos
    """
    generator = AIVehicleGenerator()
    return generator.generate_vehicles(count=num_vehiculos, brand=marca)
