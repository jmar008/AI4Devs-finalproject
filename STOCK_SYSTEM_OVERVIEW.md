# 📊 Stock Scraping System - Documentación Visual

## 🎯 Objetivo General

Crear un sistema automatizado que:

1. **Migra diariamente** (01:00 AM) datos de `Stock` → `StockHistorico`
2. **Limpia** la tabla de `Stock`
3. **Scrapeía** nuevos vehículos de [coches.net](https://www.coches.net/segunda-mano/)
4. **Rellena** la tabla de `Stock` con nuevos datos

---

## 📚 Tablas Creadas

### Tabla `stock` (Actual)

```
┌─────────────────────────────────────┐
│           stock (Actual)            │
├─────────────────────────────────────┤
│ bastidor (PK) [VARCHAR(50)]         │ ← Identificador único
│ marca [VARCHAR(100)]                │ ← Marca del vehículo
│ modelo [VARCHAR(100)]               │ ← Modelo del vehículo
│ matricula [VARCHAR(20)]             │ ← Matrícula de registro
│ precio_venta [NUMERIC(12,2)]        │ ← Precio de venta
│ dias_stock [INTEGER]                │ ← Días en stock
│ ... (130 campos más)                │ ← Otros campos
│ fecha_insert [DATETIME] AUTO        │ ← Cuándo se insertó
└─────────────────────────────────────┘
```

### Tabla `stock_historico` (Histórico)

```
┌─────────────────────────────────────┐
│       stock_historico (Histórico)   │
├─────────────────────────────────────┤
│ id [INTEGER] (PK)                   │ ← ID único del registro histórico
│ bastidor [VARCHAR(50)]              │ ← Referencia al vehículo
│ marca [VARCHAR(100)]                │ ← Marca del vehículo
│ modelo [VARCHAR(100)]               │ ← Modelo del vehículo
│ ... (todos los campos de Stock)     │ ← Todos los datos
│ fecha_snapshot [DATE]               │ ← Fecha del snapshot
│ fecha_insert [DATETIME]             │ ← Cuándo se migró
└─────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos - Línea de Tiempo

### DÍA 1 - 00:59 (Antes de la migración)

```
┌──────────────────┐
│  Stock (Actual)  │
├──────────────────┤
│ Vehicle 1        │
│ Vehicle 2        │
│ ...              │
│ Vehicle 100      │
└──────────────────┘

┌──────────────────────────┐
│ Stock Historico (Vacío)  │
└──────────────────────────┘
```

### DÍA 1 - 01:00 (INICIO MIGRACIÓN)

```
PASO 1: COPIAR Stock → StockHistorico
┌──────────────────┐                 ┌──────────────────────────┐
│  Stock (Actual)  │  ────COPY────→  │ Stock Historico          │
├──────────────────┤                 ├──────────────────────────┤
│ Vehicle 1        │                 │ Vehicle 1                │
│ Vehicle 2        │                 │ Vehicle 2                │
│ ...              │                 │ ...                      │
│ Vehicle 100      │                 │ Vehicle 100 (fecha_insert)
└──────────────────┘                 └──────────────────────────┘
```

### DÍA 1 - 01:05 (LIMPIEZA)

```
PASO 2: LIMPIAR Stock
┌──────────────────┐
│  Stock (Vacío)   │
├──────────────────┤
│      (empty)     │
└──────────────────┘
```

### DÍA 1 - 01:10 (SCRAPING)

```
PASO 3: SCRAPEIAR coches.net
┌─────────────────────┐
│   coches.net        │
│  (Web Portal)       │
├─────────────────────┤
│ [HTML] - Vehículo 1 │
│ [HTML] - Vehículo 2 │
│ [HTML] - Vehículo 3 │
│ ...                 │
└─────────────────────┘
        ↓ PARSE
  [JSON Data]
        ↓ INSERT
```

### DÍA 1 - 01:15 (INSERCIÓN)

```
PASO 4: INSERTAR nuevos datos en Stock
┌──────────────────────────┐
│   Stock (100 nuevos)     │
├──────────────────────────┤
│ Vehículo Scrapeado 1     │
│ Vehículo Scrapeado 2     │
│ Vehículo Generado 1      │ ← Si scraping no tuvo datos
│ ...                      │
│ Vehículo Scrapeado N     │
└──────────────────────────┘

┌──────────────────────────┐
│ Stock Historico (100)    │
├──────────────────────────┤
│ Vehicle 1 (DÍA 1)        │
│ Vehicle 2 (DÍA 1)        │
│ ...                      │
│ Vehicle 100 (DÍA 1)      │
└──────────────────────────┘
```

### DÍA 2 - 01:00 (MIGRACIÓN 2)

```
Repite el proceso...
┌──────────────────────────┐
│ Stock (100 del DÍA 1)    │
└──────────────────────────┘
       ↓ MIGRA
┌──────────────────────────┐
│ Stock Historico (200)    │ ← 100 de DÍA 1 + 100 de DÍA 2
└──────────────────────────┘
```

---

## 📂 Estructura del Código

```
/workspace/backend/
│
├── apps/
│   └── stock/                          🆕 NUEVA APP
│       ├── models.py                   📌 Modelos Stock & StockHistorico
│       ├── admin.py                    📌 Interfaz Admin
│       ├── scrapers.py                 📌 Lógica de scraping
│       ├── scheduler.py                📌 Programación automática
│       ├── management/
│       │   └── commands/
│       │       └── migrate_stock_and_scrape.py  📌 Comando Django
│       ├── migrations/
│       │   └── 0001_initial.py         📌 Migración BD
│       └── README_STOCK.md             📌 Documentación detallada
│
├── dealaai/settings/
│   └── base.py                         ✏️ MODIFICADO
│       └── INSTALLED_APPS += 'apps.stock'
│
├── requirements/
│   └── base.txt                        ✏️ MODIFICADO
│       └── + requests, beautifulsoup4, apscheduler
│
├── run_stock_migration.py              🆕 Script manual
└── .env                                ✏️ MODIFICADO (variables)

/workspace/database/
└── migrations/
    └── stock_queries.sql               🆕 Queries SQL útiles

/workspace/
├── docker-compose.yml                  ✏️ YA TIENE Redis, Celery
├── STOCK_SETUP_SUMMARY.md              🆕 Resumen de lo creado
└── QUICK_START_STOCK.md                🆕 Guía rápida de inicio
```

---

## 🔌 Integración con Existentes

### Docker Compose

```yaml
services:
  backend: # Django - Ejecuta scheduler
  db: # PostgreSQL - Almacena datos
  redis: # Redis - Cache (ya existía)
  celery_worker: # Celery - Tareas async (ya existía)
  celery_beat: # Celery Beat - Tareas programadas
```

### Django Settings

```python
INSTALLED_APPS = [
    # ... apps existentes
    'apps.stock',  # ← NUEVO
]

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
```

---

## 🚀 Flujo de Ejecución

```
1️⃣ INICIO DEL SISTEMA
   ├─ Django arranca
   ├─ APScheduler se inicializa
   └─ ⏰ Espera a las 01:00 AM

2️⃣ A LAS 01:00 AM
   ├─ APScheduler trigger se activa
   ├─ Ejecuta manage.py migrate_stock_and_scrape
   └─ ✅ Proceso comienza

3️⃣ DENTRO DEL COMANDO
   ├─ MIGRAR: SELECT * FROM stock → INSERT INTO stock_historico
   ├─ LIMPIAR: DELETE FROM stock
   ├─ SCRAPEIAR: requests.get(coches.net) → Parse HTML
   ├─ INSERTAR: INSERT INTO stock (nuevos datos)
   └─ ✅ Proceso termina

4️⃣ RESULTADO
   ├─ Stock: Contiene 100 vehículos nuevos
   ├─ StockHistorico: Contiene histórico acumulado
   ├─ Logs: Guardados para auditoría
   └─ 📊 Sistema listo para el día siguiente
```

---

## 💾 Campos Capturados

### De `stock_vo_completo_last_snapshot`

```
140+ campos organizados en categorías:

📋 IDENTIFICADORES (5)
   idv, fecha_informe, bastidor, vehicle_key, vehicle_key2

🏢 CONCESIONARIO (6)
   id_concesionario, nom_concesionario, id_proveedor, nom_proveedor,
   dealer_corto, provincia

🚗 VEHÍCULO (20)
   matricula, fecha_matriculacion, marca, modelo, año, color, km, etc.

💰 FINANCIERO (10)
   importe_compra, importe_costo, precio_venta, stock_benef_estimado, etc.

📱 INTERNET (15)
   publicado, id_internet, link, precio_internet, visitas, leads, etc.

📅 STOCK (10)
   dias_stock, meses_en_stock, reservado, tipo_stock, intervalo_dias, etc.

🎯 Y MÁS...
   estado, tipo_vo, fotos, cambios, predicciones, etc.
```

---

## 🧪 Ejemplos de Consultas

### Ver datos en Stock

```bash
# En terminal
docker-compose exec backend python manage.py shell

# En Python
>>> from apps.stock.models import Stock
>>> stocks = Stock.objects.all()[:5]
>>> for s in stocks:
...     print(f"{s.bastidor} - {s.marca} {s.modelo}")
```

### Ver estadísticas

```sql
-- En PostgreSQL
SELECT marca, COUNT(*) FROM stock GROUP BY marca ORDER BY count DESC;
SELECT AVG(precio_venta) FROM stock;
SELECT COUNT(DISTINCT id_concesionario) FROM stock;
```

### Auditoría histórica

```sql
-- Ver qué vehículos ha habido
SELECT DISTINCT bastidor FROM stock_historico;

-- Ver evolución de precios de un vehículo
SELECT bastidor, precio_venta, fecha_insert FROM stock_historico
WHERE bastidor = 'XXX123XXX'
ORDER BY fecha_insert;
```

---

## ⚙️ Parámetros Configurables

| Parámetro          | Ubicación         | Default | Rango  | Uso                    |
| ------------------ | ----------------- | ------- | ------ | ---------------------- |
| `hour`             | `scheduler.py:24` | `1`     | 0-23   | Hora de ejecución      |
| `minute`           | `scheduler.py:25` | `0`     | 0-59   | Minuto de ejecución    |
| `paginas`          | `scheduler.py:42` | `5`     | 1-∞    | Páginas a scrapeiar    |
| `cantidad`         | `scheduler.py:43` | `50`    | 1-∞    | Vehículos a crear      |
| `retraso_segundos` | `scrapers.py:343` | `2.0`   | 0.5-10 | Retraso entre requests |

---

## 📊 Crecimiento de Datos

```
Suposición: 50 vehículos por día

DÍA  | Stock | Histórico | Total | Tamaño aprox.
-----|-------|-----------|-------|---------------
1    | 50    | 50        | 100   | ~2 MB
7    | 50    | 350       | 400   | ~8 MB
30   | 50    | 1,500     | 1,550 | ~31 MB
365  | 50    | 18,250    | 18,300| ~366 MB
730  | 50    | 36,500    | 36,550| ~731 MB

Nota: Estimado ~20 KB por registro
```

---

## 🎯 Casos de Uso

### 1. Análisis Histórico de Precios

```sql
SELECT bastidor, marca, modelo,
       MAX(precio_venta) as max_precio,
       MIN(precio_venta) as min_precio
FROM stock_historico
WHERE fecha_insert > NOW() - INTERVAL '30 days'
GROUP BY bastidor;
```

### 2. Detección de Cambios

```sql
SELECT NEW.bastidor, NEW.precio_venta as precio_nuevo,
       OLD.precio_venta as precio_anterior
FROM stock_historico NEW
JOIN stock_historico OLD
  ON NEW.bastidor = OLD.bastidor
WHERE NEW.fecha_insert > OLD.fecha_insert
ORDER BY NEW.fecha_insert DESC;
```

### 3. Reportes de Ventas

```sql
SELECT DATE(fecha_insert), COUNT(*) as vendidos
FROM stock_historico
WHERE id_estado = 'VEND'
GROUP BY DATE(fecha_insert);
```

---

## 🔒 Seguridad

- ✅ Transacciones atómicas (todo o nada)
- ✅ Validación de datos
- ✅ Manejo de excepciones
- ✅ Logging detallado
- ✅ User-Agents rotados
- ✅ Retrasos entre requests (anti-ban)
- ✅ Bastidor como PRIMARY KEY (sin duplicados)

---

## 📈 Monitoreo

```bash
# Ver logs en tiempo real
docker-compose logs -f backend

# Filtrar por stock
docker-compose logs backend | grep -i "stock\|migración"

# Ver estado de BD
docker-compose exec db psql -U postgres -d dealaai_dev \
  -c "SELECT COUNT(*) FROM stock; SELECT COUNT(*) FROM stock_historico;"

# Ver histórico reciente
docker-compose exec db psql -U postgres -d dealaai_dev \
  -c "SELECT COUNT(*) FROM stock_historico WHERE fecha_insert > NOW() - INTERVAL '1 day';"
```

---

## ✅ Checklist de Implementación

- ✅ Modelos Django creados
- ✅ Migraciones creadas
- ✅ Admin configurado
- ✅ Scraper implementado
- ✅ Comando Django creado
- ✅ Scheduler configurado
- ✅ Dependencias agregadas
- ✅ Docker Compose actualizado
- ✅ Documentación completa
- ✅ Queries SQL proporcionadas

---

**Sistema listo para producción** 🚀

Creado: 26 de Octubre, 2025  
Versión: 1.0
