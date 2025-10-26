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
        self.fallback_models = settings.DEEPSEEK_FALLBACK_MODELS

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

        # Para lotes grandes, aumentar el tamaño del batch
        # Esto reduce el número de llamadas a la API
        if count > 100:
            batch_size = 10  # Lotes de 10 para generación masiva
        elif count > 50:
            batch_size = 8
        else:
            batch_size = 5  # Lotes de 5 para cantidades pequeñas

        logger.info(f"Generando {count} vehículos con IA en lotes de {batch_size}")

        for i in range(0, count, batch_size):
            batch_count = min(batch_size, count - i)
            try:
                batch = self._generate_batch(batch_count, brand)
                vehicles.extend(batch)
                logger.info(f"✓ Lote completado: {len(batch)} vehículos (total: {len(vehicles)}/{count})")

                # Pequeño delay entre lotes para evitar rate limiting
                # Solo si no es el último lote
                if i + batch_size < count:
                    time.sleep(0.5)  # 500ms entre lotes

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

        # Intentar con el modelo principal y fallbacks
        models_to_try = [self.model] + self.fallback_models
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
                                     "lógicas entre año, kilometraje, precio y condición."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.8,  # Mayor creatividad para variedad
                    max_tokens=3500,  # Aumentado para soportar lotes de 10 vehículos
                    extra_body={
                        "data_collection": "allow"  # Para modelos gratuitos de OpenRouter
                    }
                )

                # Parsear respuesta JSON
                content = response.choices[0].message.content
                vehicles_data = json.loads(content)

                # Validar y completar datos
                vehicles = []
                for vehicle_data in vehicles_data.get('vehicles', []):
                    vehicle = self._complete_vehicle_data(vehicle_data)
                    vehicles.append(vehicle)

                logger.info(f"✓ Generados {len(vehicles)} vehículos con {model}")
                return vehicles

            except json.JSONDecodeError as e:
                logger.error(f"❌ Error parseando JSON de {model}: {str(e)}")
                last_error = e
                continue
            except Exception as e:
                error_str = str(e)
                logger.warning(f"⚠️  Error con modelo {model}: {error_str}")
                last_error = e

                # Si es rate limit (429) o modelo no disponible (404), intentar siguiente modelo
                if "429" in error_str or "rate" in error_str.lower():
                    logger.info(f"→ Rate limit detectado, cambiando al siguiente modelo...")
                    continue
                elif "404" in error_str or "not found" in error_str.lower():
                    logger.info(f"→ Modelo no disponible (404), cambiando al siguiente modelo...")
                    continue
                # Otros errores, también intentar siguiente
                continue

        # Si todos los modelos fallan, lanzar error
        if last_error:
            raise last_error
        raise Exception("No se pudo generar vehículos con ningún modelo")

    def _create_prompt(self, count: int, brand: Optional[str] = None) -> str:
        """Crea el prompt para generar vehículos"""

        brand_constraint = f"de la marca {brand}" if brand else "de marcas populares en España (BMW, Mercedes, Audi, VW, Ford, Renault, Peugeot, etc.)"

        return f"""Genera {count} vehículos de ocasión realistas {brand_constraint} para un concesionario en España.

Para cada vehículo, considera relaciones lógicas:
- Coches más antiguos tienen más kilómetros (ej: 2015 → 80,000-150,000 km)
- Coches recientes tienen menos kilómetros (ej: 2022 → 10,000-50,000 km)
- Precio coherente con año, km y marca (ej: BMW 2020 con 30,000km → 25,000-35,000€)
- Modelos y versiones reales de cada marca
- Potencia y cilindrada coherentes con el modelo

Responde ÚNICAMENTE con JSON válido en este formato:
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
    }}
  ]
}}

Asegúrate de que:
1. El JSON sea válido (sin comentarios ni texto extra)
2. Los precios sean coherentes (vehículos premium más caros)
3. El kilometraje sea realista según el año
4. Los modelos y versiones existan realmente
5. La descripción mencione características relevantes del vehículo"""

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
