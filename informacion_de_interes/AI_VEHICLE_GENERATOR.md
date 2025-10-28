# 🤖 Generación de Vehículos con IA

## Descripción

Se ha implementado un sistema de generación de datos de vehículos usando **Inteligencia Artificial** que produce datos mucho más realistas y coherentes que el sistema de scraping tradicional.

## ✨ Ventajas sobre el Sistema Tradicional

### Sistema Tradicional (Scraping)

❌ Datos aleatorios sin relación lógica
❌ Precios no coherentes con año/kilometraje
❌ Modelos y versiones inventados
❌ Kilometraje sin relación con la edad del vehículo
❌ Especificaciones técnicas aleatorias

### Sistema con IA

✅ **Coherencia lógica**: Año, kilometraje y precio relacionados
✅ **Modelos reales**: Usa modelos y versiones que existen en el mercado
✅ **Precios realistas**: Según marca, año, kilometraje y condición
✅ **Especificaciones técnicas coherentes**: Potencia y cilindrada apropiadas
✅ **Descripciones útiles**: Información relevante sobre el vehículo

## 🔧 Cómo Funciona

El generador con IA utiliza modelos de lenguaje (LLM) de OpenRouter para crear vehículos con las siguientes características:

1. **Relaciones lógicas entre datos**:

   - Coches antiguos → Más kilometraje
   - Coches recientes → Menos kilometraje
   - Marcas premium → Precios más altos
   - Buen estado → Mayor precio

2. **Fallback automático**: Si la IA falla, revierte al sistema tradicional

3. **Multi-modelo**: Intenta con 5 modelos diferentes si uno falla por rate limiting

## 📝 Uso

### Comando Django

```bash
# Generar 50 vehículos con IA (modo por defecto usa scraping)
docker-compose exec backend python manage.py migrate_stock_and_scrape --usar-ia --cantidad 50

# Generar 100 vehículos con IA
docker-compose exec backend python manage.py migrate_stock_and_scrape --usar-ia --cantidad 100

# Sin IA (modo tradicional)
docker-compose exec backend python manage.py migrate_stock_and_scrape --cantidad 50
```

### Script de Prueba

```bash
# Ejecutar prueba del generador de IA
docker-compose exec backend python test_ai_generator.py
```

Este script genera 3 vehículos de marcas variadas y 2 BMWs de ejemplo.

### Desde Código Python

```python
from apps.stock.ai_vehicle_generator import generar_vehiculos_con_ia

# Generar 10 vehículos de cualquier marca
vehiculos = generar_vehiculos_con_ia(num_vehiculos=10)

# Generar 5 vehículos BMW
vehiculos_bmw = generar_vehiculos_con_ia(num_vehiculos=5, marca="BMW")

# Procesar los vehículos generados
for vehiculo in vehiculos:
    print(f"{vehiculo['marca']} {vehiculo['modelo']} - {vehiculo['precio_venta']}€")
```

## 📊 Ejemplo de Datos Generados

### Con IA (Coherente)

```json
{
  "marca": "BMW",
  "modelo": "Serie 3",
  "version": "320d xDrive",
  "anio_matricula": 2019,
  "kilometros": 85000,
  "precio_venta": 24500,
  "color": "Gris",
  "combustible": "Diésel",
  "transmision": "Automática",
  "potencia": 190,
  "descripcion": "BMW Serie 3 en excelente estado, único propietario, mantenimiento oficial"
}
```

✅ **Coherente**: 2019, 85k km, 24.500€ → Precio realista para BMW diésel con esos km

### Sin IA (Aleatorio)

```json
{
  "marca": "BMW",
  "modelo": "Serie 3",
  "version": "Serie 3 1.6",
  "anio_matricula": 2015,
  "kilometros": 45000,
  "precio_venta": 125000,
  "color": "Amarillo",
  "combustible": "GLP",
  "transmision": "CVT",
  "potencia": 450
}
```

❌ **Incoherente**: 2015, 45k km, 125.000€ → Precio absurdo para esos km, motor 1.6 con 450CV imposible

## 🎯 Casos de Uso

### 1. Desarrollo y Testing

```bash
# Generar datos realistas para desarrollo
docker-compose exec backend python manage.py migrate_stock_and_scrape --usar-ia --cantidad 20
```

### 2. Demostración a Clientes

Los datos generados son tan realistas que se pueden usar para demos sin necesidad de datos reales.

### 3. Análisis de Stock

Como los datos tienen sentido, el chat con IA puede proporcionar análisis más útiles:

- "¿Cuál es el precio promedio de los BMWs de 2019?"
- "Muéstrame vehículos con menos de 50,000 km"
- "¿Qué coches tenemos por menos de 15,000€?"

## ⚙️ Configuración

El generador usa la misma configuración del chat con IA:

```python
# backend/dealaai/settings/base.py
DEEPSEEK_API_KEY = "sk-or-v1-..."  # OpenRouter API key
DEEPSEEK_API_BASE = "https://openrouter.ai/api/v1"
DEEPSEEK_MODEL = "meta-llama/llama-3.2-3b-instruct:free"
DEEPSEEK_FALLBACK_MODELS = [
    "qwen/qwen-2-7b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "google/gemini-2.0-flash-exp:free",
    "nousresearch/hermes-3-llama-3.1-405b:free"
]
```

## 🔄 Flujo de Trabajo

1. **Generación con IA**:

   - Crea prompt estructurado con requisitos de coherencia
   - Envía a modelo LLM de OpenRouter
   - Parsea respuesta JSON con datos del vehículo
   - Completa campos adicionales (bastidor, matrícula, concesionario)

2. **Fallback en caso de error**:

   - Si falla modelo principal → Intenta 4 modelos fallback
   - Si fallan todos → Genera datos aleatorios tradicionales
   - Logs detallados de cada intento

3. **Inserción en BD**:
   - Crea objetos Stock con todos los campos
   - Inserta en lotes de 500 para eficiencia
   - Mantiene compatibilidad total con sistema existente

## 🚀 Ventajas para el Proyecto

1. **Mejor experiencia de usuario**: Datos que tienen sentido
2. **Chat IA más útil**: Puede analizar datos realistas
3. **Demos convincentes**: Sin necesidad de datos reales
4. **Testing efectivo**: Escenarios más cercanos a producción
5. **Escalabilidad**: Genera cualquier cantidad de vehículos coherentes

## 📈 Rendimiento

- **Velocidad**: ~5-10 vehículos por request de IA
- **Lotes**: Genera en grupos de 5 para eficiencia
- **Rate Limiting**: Sistema fallback automático entre modelos
- **Costo**: $0 (usa modelos gratuitos de OpenRouter)

## 🔧 Troubleshooting

### Error: Rate Limit (429)

**Solución**: El sistema automáticamente cambia al siguiente modelo fallback.

### Error: SSL Certificate

**Solución**: El sistema ya incluye `verify=False` para proxies corporativos (Zscaler).

### Error: Invalid JSON

**Solución**: El prompt instruye al modelo a responder solo con JSON válido. Si persiste, revisa logs.

### Generación lenta

**Solución**:

- Reduce `--cantidad` a lotes más pequeños
- Usa modelos más rápidos (ej: qwen en vez de llama)

## 📝 Logs

Los logs incluyen información detallada:

```
INFO: Generando vehículos con modelo: meta-llama/llama-3.2-3b-instruct:free
INFO: ✓ Generados 5 vehículos con meta-llama/llama-3.2-3b-instruct:free
INFO: Generados 5 vehículos con IA (total: 5/50)
WARNING: Error con modelo meta-llama/llama-3.2-3b-instruct:free: Rate limit exceeded
INFO: Generando vehículos con modelo: qwen/qwen-2-7b-instruct:free
```

## 🎓 Próximos Pasos

1. **Mejorar prompts**: Añadir más contexto específico del mercado español
2. **Cache de respuestas**: Evitar regenerar vehículos similares
3. **Personalización**: Permitir especificar rango de precios, años, etc.
4. **Imágenes**: Generar URLs de imágenes realistas con IA
5. **Descripciones enriquecidas**: Textos de venta más elaborados

---

**Creado**: 2024
**Autor**: DealaAI Team
**Versión**: 1.0
