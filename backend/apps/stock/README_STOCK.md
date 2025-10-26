# 📊 Módulo de Stock - Scraping y Migración

## 📋 Descripción General

Este módulo gestiona:

- **Tabla `Stock`**: Datos actuales de vehículos (se vacía diariamente)
- **Tabla `StockHistorico`**: Histórico de datos de stock (se rellena diariamente a las 01:00)
- **Scraping automático**: Obtiene datos de coches.net y rellena la tabla de stock

### Flujo Diario (01:00 AM)

```
┌─────────────────────────────────┐
│  MIGRACIÓN DIARIA (01:00 AM)    │
└─────────────────────────────────┘
           ↓
┌─────────────────────────────────┐
│ 1. Migrar Stock → StockHistorico │
│    (Copia todos los registros)  │
└─────────────────────────────────┘
           ↓
┌─────────────────────────────────┐
│ 2. Limpiar tabla Stock          │
│    (Vaciar para nuevos datos)   │
└─────────────────────────────────┘
           ↓
┌─────────────────────────────────┐
│ 3. Scrapeiar coches.net         │
│    (Obtener nuevos vehículos)   │
└─────────────────────────────────┘
           ↓
┌─────────────────────────────────┐
│ 4. Insertar en Stock            │
│    (Llenar con nuevos datos)    │
└─────────────────────────────────┘
```

## 🚀 Instalación

### 1. Instalar dependencias

```bash
# Las dependencias ya están en requirements/base.txt:
# - requests==2.31.0
# - beautifulsoup4==4.12.2
# - apscheduler==3.10.4
# - redis==5.0.1
# - celery==5.3.4

pip install -r backend/requirements/base.txt
```

### 2. Crear las tablas

```bash
cd /workspace/backend
python manage.py migrate stock
```

## 📝 Estructura de Archivos

```
apps/stock/
├── models.py                           # Modelos Stock y StockHistorico
├── admin.py                            # Interfaz admin
├── scrapers.py                         # Módulo de scraping
├── scheduler.py                        # Programación de tareas
├── management/
│   └── commands/
│       └── migrate_stock_and_scrape.py # Comando Django
└── migrations/
    └── 0001_initial.py                 # Migración inicial
```

## 🎯 Uso

### Ejecución Automática (Recomendado)

El scheduler se inicializa automáticamente cuando Django arranca:

```bash
python manage.py runserver
# El scheduler ejecutará la migración a las 01:00 AM automáticamente
```

### Ejecución Manual

#### Opción 1: Usando el comando Django

```bash
# Básico (5 páginas, 50 vehículos)
python manage.py migrate_stock_and_scrape

# Personalizado
python manage.py migrate_stock_and_scrape --paginas 10 --cantidad 100 --debug
```

#### Opción 2: Usando el script de Python

```bash
# Desde /workspace/backend
python run_stock_migration.py

# Con opciones
python run_stock_migration.py --paginas 10 --cantidad 100 --debug
```

#### Opción 3: Desde Docker

```bash
# Ejecutar comando dentro del contenedor
docker-compose exec backend python manage.py migrate_stock_and_scrape

# O ejecutar el script
docker-compose exec backend python run_stock_migration.py
```

## 📊 Campos de la Tabla Stock/StockHistorico

### Identificadores

- `bastidor` (PK): Número de bastidor VIN
- `idv`: Identificador interno
- `vehicle_key`: Clave del vehículo
- `id_concesionario`: ID del concesionario

### Datos del Vehículo

- `marca`: Marca del vehículo
- `modelo`: Modelo del vehículo
- `matricula`: Matrícula de registro
- `anio_matricula`: Año de matriculación
- `color`: Color principal
- `kilometros`: Kilómetros recorridos

### Estado del Stock

- `dias_stock`: Días en stock
- `meses_en_stock`: Meses en stock
- `reservado`: ¿Está reservado?
- `tipo_stock`: Tipo (STOCK, SPECIAL, PROMOCION)

### Datos Financieros

- `importe_compra`: Precio de compra
- `importe_costo`: Costo del vehículo
- `precio_venta`: Precio de venta
- `stock_benef_estimado`: Beneficio estimado

### Internet

- `publicado`: ¿Publicado online?
- `id_internet`: ID en portal
- `link_internet`: URL del anuncio
- `precio_internet`: Precio online
- `visitas_totales`: Visitas totales

### Metadatos

- `fecha_snapshot`: Fecha del snapshot
- `fecha_insert`: Fecha de inserción (auto)
- `fecha_actualizacion`: Fecha de actualización

## ⚙️ Configuración

### Cambiar hora de ejecución

Editar `apps/stock/scheduler.py`:

```python
scheduler.add_job(
    func=_run_stock_migration,
    trigger="cron",
    hour=1,      # ← Cambiar aquí (0-23)
    minute=0,    # ← Cambiar aquí (0-59)
    ...
)
```

### Cambiar cantidad de vehículos por defecto

Editar `apps/stock/scheduler.py`:

```python
call_command(
    'migrate_stock_and_scrape',
    paginas=5,      # ← Cambiar aquí
    cantidad=50,    # ← Cambiar aquí
    verbosity=2
)
```

## 🔧 Manejo de Errores

### Scraping falla

Si coches.net no responde o cambia su estructura:

1. Se captura la excepción
2. Se generan datos aleatorios realistas
3. Se continúa sin interrumpir el flujo
4. Se registra en logs

### Duplicados

El comando usa `bulk_create` con `ignore_conflicts=True` para evitar duplicados de bastidor.

### Integridad de datos

- Transacción atómica: Si algo falla, se revierte todo
- Validación de campos: Todos los campos tienen `null=True, blank=True`
- Índices en campos críticos para búsquedas rápidas

## 📈 Monitoreo

### Ver logs de migración

```bash
# Logs generales
docker-compose logs backend

# Filtrar por stock
docker-compose logs backend | grep -i stock

# Seguimiento en tiempo real
docker-compose logs -f backend
```

### Verificar datos en BD

```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U postgres -d dealaai_dev

# Consultas útiles
SELECT COUNT(*) FROM stock;
SELECT COUNT(*) FROM stock_historico;
SELECT * FROM stock LIMIT 5;
SELECT * FROM stock_historico WHERE fecha_insert > NOW() - INTERVAL '1 day';
```

### Verificar en Django Admin

```
http://localhost:8000/admin/stock/stock/
http://localhost:8000/admin/stock/stockhistorico/
```

## 🐛 Troubleshooting

### Error: "No module named 'requests'"

```bash
pip install -r requirements/base.txt
```

### Error: "APScheduler iniciado pero no ejecuta"

Verificar que Django esté corriendo en modo no-daemon y que el scheduler no esté ya ejecutándose.

### Scraping muy lento

Ajustar el retraso entre solicitudes en `scrapers.py`:

```python
def scrape_coches_net(paginas: int = 1, retraso_segundos: float = 2.0):
    # ← Cambiar este valor (en segundos)
```

### Muchos datos duplicados

Verificar que los VINs/bastidores sean únicos. El modelo usa bastidor como PRIMARY KEY, así que no debería haber duplicados.

## 📝 Ejemplo de Uso Completo

```bash
# 1. Acceder al contenedor
docker-compose exec backend bash

# 2. Ejecutar migración manual
python manage.py migrate_stock_and_scrape --paginas 5 --cantidad 100

# 3. Verificar en BD
python manage.py shell
>>> from apps.stock.models import Stock
>>> Stock.objects.count()
100
>>> Stock.objects.first()
<Stock: BASTIDOR123456 - BMW X3>

# 4. Ver en admin
# Acceder a http://localhost:8000/admin/stock/stock/
```

## 🔄 Actualización de Scrapers

Para actualizar la lógica de scraping:

1. Editar `apps/stock/scrapers.py`
2. Modificar la función `extraer_informacion_vehiculo()` con nuevos selectores CSS
3. Ejecutar manualmente para probar: `python manage.py migrate_stock_and_scrape --debug`
4. Si funciona, dejará ejecutarse automáticamente

## 📞 Soporte

Para problemas o mejoras, consultar con el equipo de desarrollo.

---

**Última actualización**: 26 de Octubre, 2025  
**Versión**: 1.0  
**Estado**: Producción
