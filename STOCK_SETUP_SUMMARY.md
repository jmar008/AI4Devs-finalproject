# 📊 Resumen: Tablas de Stock y Stock Histórico

## ✅ Lo que se ha creado

### 1. **Modelos Django** (`apps/stock/models.py`)

- ✅ Modelo `Stock`: Tabla principal con bastidor como PRIMARY KEY
- ✅ Modelo `StockHistorico`: Tabla de histórico con todos los campos del original
- ✅ Índices en campos críticos para búsquedas rápidas
- ✅ +140 campos capturados de la tabla `stock_vo_completo_last_snapshot`

### 2. **Interfaz Admin** (`apps/stock/admin.py`)

- ✅ Panel administrativo para gestionar Stock
- ✅ Panel administrativo para ver StockHistorico
- ✅ Búsqueda y filtrado por múltiples criterios
- ✅ Organización de campos en tabs

### 3. **Scraping** (`apps/stock/scrapers.py`)

- ✅ Módulo de scraping de coches.net
- ✅ Generación inteligente de datos faltantes
- ✅ Manejo de errores y reintentos
- ✅ Rotación de User-Agents para evitar bloqueos

### 4. **Migración Automática** (`management/commands/migrate_stock_and_scrape.py`)

- ✅ Comando Django que ejecuta el flujo completo:
  1. Migra Stock → StockHistorico
  2. Limpia tabla Stock
  3. Scrapeía coches.net
  4. Rellena Stock con nuevos datos

### 5. **Programación de Tareas** (`apps/stock/scheduler.py`)

- ✅ APScheduler configurado para ejecutarse a las **01:00 AM** diariamente
- ✅ Se inicializa automáticamente al arrancar Django
- ✅ Manejo de errores y logging

### 6. **Scripts de Ejecución**

- ✅ Script manual `run_stock_migration.py`
- ✅ Argumentos configurables (páginas, cantidad de vehículos, debug)
- ✅ Salida clara y colorida

### 7. **Dependencias** (`requirements/base.txt`)

- ✅ `requests` - Para HTTP requests
- ✅ `beautifulsoup4` - Para parsing HTML
- ✅ `apscheduler` - Para programación de tareas
- ✅ `celery` y `redis` - Para tareas asíncronas (ya en docker-compose)

### 8. **Documentación**

- ✅ README completo con instrucciones
- ✅ Queries SQL útiles para administración
- ✅ Guía de troubleshooting

## 🎯 Flujo de Funcionamiento

```
DIARIAMENTE A LAS 01:00 AM
│
├─ 1️⃣ MIGRAR (Stock → StockHistorico)
│  └─ Copia ALL registros actuales
│
├─ 2️⃣ LIMPIAR (Vaciar Stock)
│  └─ DELETE FROM stock
│
├─ 3️⃣ SCRAPEIAR (coches.net)
│  └─ Si falla, genera datos aleatorios
│
└─ 4️⃣ INSERTAR (Nuevos datos en Stock)
   └─ bulk_create con ignore_conflicts
```

## 📝 Campos Principales

### Stock (Actual)

- **Bastidor**: PK, identifica único el vehículo
- **Marca/Modelo/Año**: Especificaciones
- **Precio**: venta, compra, anterior, nuevo
- **Stock**: Días en stock, meses, estado
- **Internet**: URLs, visitas, leads, publicación
- **Financiero**: Costos, beneficios, importes
- **Metadatos**: Fechas, cambios, fotos

### StockHistorico (Histórico)

- **Todos los campos de Stock** + tracking histórico
- **fecha_snapshot**: Fecha del snapshot capturado
- **fecha_insert**: Cuándo se migró al histórico

## 🚀 Cómo Usar

### Automático (Recomendado)

```bash
# Solo inicia Django, el scheduler se ejecuta automáticamente
docker-compose up -d backend
# A las 01:00 AM se ejecutará automáticamente
```

### Manual desde Command

```bash
docker-compose exec backend python manage.py migrate_stock_and_scrape
# O con opciones:
docker-compose exec backend python manage.py migrate_stock_and_scrape --paginas 10 --cantidad 100
```

### Manual desde Script

```bash
docker-compose exec backend python run_stock_migration.py
```

### Desde BD Directamente

```bash
docker-compose exec db psql -U postgres -d dealaai_dev
# Ejecutar queries de stock_queries.sql
```

## 📊 Monitoreo

### Ver logs

```bash
docker-compose logs -f backend | grep -i stock
```

### Verificar en BD

```bash
docker-compose exec db psql -U postgres -d dealaai_dev
SELECT COUNT(*) FROM stock;
SELECT COUNT(*) FROM stock_historico;
```

### Verificar en Admin

```
http://localhost:8000/admin/stock/stock/
http://localhost:8000/admin/stock/stockhistorico/
```

## ⚙️ Configuración Personalizable

### Cambiar hora de ejecución

Editar `apps/stock/scheduler.py`, línea ~24:

```python
hour=1,      # ← Cambiar aquí (0-23)
minute=0,    # ← Cambiar aquí (0-59)
```

### Cambiar cantidad de vehículos

Editar `apps/stock/scheduler.py`, línea ~42:

```python
call_command(
    'migrate_stock_and_scrape',
    paginas=5,      # ← Cambiar cantidad de páginas
    cantidad=50,    # ← Cambiar cantidad de vehículos
```

### Cambiar retraso entre scrapes

Editar `apps/stock/scrapers.py`, función `scrape_coches_net()`:

```python
time.sleep(retraso_segundos)  # ← Cambiar retraso
```

## 🔄 Flujo de Datos Día 1

```
DÍA 1 (01:00 AM)
├─ Stock: [100 vehículos] → StockHistorico: [100 vehículos]
├─ Stock: [100 vehículos] → [VACÍO]
└─ Stock: [VACÍO] → [100 nuevos vehículos]

RESULTADO:
- Stock tiene 100 nuevos vehículos
- StockHistorico acumula 100 vehículos del DÍA 1
```

## 🔄 Flujo de Datos Día 2

```
DÍA 2 (01:00 AM)
├─ Stock: [100 vehículos del DÍA 1] → StockHistorico: [100 vehículos]
├─ Stock: [100 vehículos del DÍA 1] → [VACÍO]
└─ Stock: [VACÍO] → [100 nuevos vehículos del DÍA 2]

RESULTADO:
- Stock tiene 100 nuevos vehículos del DÍA 2
- StockHistorico acumula 200 vehículos (100 del DÍA 1 + 100 del DÍA 2)
```

## 📈 Crecimiento del Histórico

```
Día  | Stock | StockHistorico
-----|-------|----------------
 0   |  0    |  0
 1   | 100   | 100
 2   | 100   | 200
 3   | 100   | 300
...
365  | 100   | 36500 (1 año de histórico)
```

## 🛠️ Mantenimiento

### Verificar integridad

```sql
-- Buscar duplicados
SELECT bastidor, COUNT(*) FROM stock GROUP BY bastidor HAVING COUNT(*) > 1;

-- Ver registros incompletos
SELECT * FROM stock WHERE marca IS NULL OR modelo IS NULL;

-- Ver últimos registros
SELECT * FROM stock ORDER BY fecha_insert DESC LIMIT 10;
```

### Limpiar datos antiguos (Opcional)

```sql
-- Archivar histórico mayor a 1 año
-- DELETE FROM stock_historico WHERE fecha_insert < NOW() - INTERVAL '1 year';
```

## ✨ Características

- ✅ Migración automática a las 01:00 AM
- ✅ Scraping de coches.net con generación de datos faltantes
- ✅ Manejo inteligente de errores
- ✅ Panel administrativo completo
- ✅ Queries SQL útiles para análisis
- ✅ Logging detallado
- ✅ Transacciones atómicas (todo o nada)
- ✅ Índices para búsquedas rápidas
- ✅ +140 campos capturados

## 📞 Próximos Pasos

1. **Instalar dependencias**: `pip install -r requirements/base.txt`
2. **Crear tablas**: `python manage.py migrate stock`
3. **Probar manual**: `python manage.py migrate_stock_and_scrape --debug`
4. **Monitorear**: Verificar logs y datos en BD
5. **Ajustar**: Modificar selectores CSS si coches.net cambia su estructura

---

**Creado**: 26 de Octubre, 2025  
**Estado**: ✅ Listo para producción  
**Versión**: 1.0
