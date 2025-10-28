# 🚀 Guía Rápida de Inicio - Stock & Scraping

## Paso 1: Instalar Dependencias

```bash
# Entrar al backend
cd /workspace/backend

# Instalar dependencias (ya incluye requests, beautifulsoup4, apscheduler, etc.)
pip install -r requirements/base.txt
```

## Paso 2: Crear las Tablas en BD

```bash
cd /workspace/backend

# Crear migraciones de la app stock
python manage.py makemigrations stock

# Aplicar migraciones (crear tablas)
python manage.py migrate stock

# Verificar en la BD
python manage.py shell
>>> from apps.stock.models import Stock, StockHistorico
>>> Stock.objects.count()  # Debe devolver 0
>>> StockHistorico.objects.count()  # Debe devolver 0
```

## Paso 3: Probar Manualmente (Opcional)

```bash
cd /workspace/backend

# Ejecutar una migración de prueba
python manage.py migrate_stock_and_scrape --paginas 2 --cantidad 20 --debug

# Verificar que se crearon los datos
python manage.py shell
>>> from apps.stock.models import Stock
>>> Stock.objects.count()  # Debe devolver 20
>>> stock = Stock.objects.first()
>>> print(f"{stock.bastidor} - {stock.marca} {stock.modelo}")
```

## Paso 4: Iniciar en Docker (Producción)

```bash
# Iniciar todos los servicios
docker-compose up -d

# Aplicar migraciones en Docker
docker-compose exec backend python manage.py migrate stock

# Verificar que funciona
docker-compose logs backend | grep "Starting development server"

# Ver que el scheduler está activo
docker-compose logs backend | grep "APScheduler iniciado"
```

## Paso 5: Verificar Funcionamiento

### Opción A: Desde Django Admin

```
1. Acceder a: http://localhost:8000/admin/
2. Usuario: admin
3. Contraseña: [tu contraseña]
4. Ir a: Stock > Stock
5. Deberías ver vehículos
```

### Opción B: Desde BD

```bash
docker-compose exec db psql -U postgres -d dealaai_dev

# Ver cantidad de registros
SELECT COUNT(*) FROM stock;
SELECT COUNT(*) FROM stock_historico;

# Ver últimos registros
SELECT bastidor, marca, modelo, precio_venta FROM stock LIMIT 5;
```

### Opción C: Desde Django Shell

```bash
cd /workspace/backend
python manage.py shell

>>> from apps.stock.models import Stock
>>> print(Stock.objects.count())
>>> for stock in Stock.objects.all()[:3]:
...     print(f"{stock.bastidor} - {stock.marca} {stock.modelo}")
```

## Paso 6: Automatización

El scheduler se ejecutará automáticamente a las **01:00 AM** todos los días.

Para cambiar la hora:

```bash
# Editar apps/stock/scheduler.py
nano /workspace/backend/apps/stock/scheduler.py

# Línea ~24:
scheduler.add_job(
    func=_run_stock_migration,
    trigger="cron",
    hour=1,      # ← Cambiar aquí (0-23)
    minute=0,    # ← Cambiar aquí
```

## Paso 7: Monitoreo Diario

```bash
# Ver logs en tiempo real
docker-compose logs -f backend

# Filtrar por stock
docker-compose logs backend | grep -i stock

# Ver si el scheduler está ejecutándose
docker-compose logs backend | grep -i "scheduler\|migración"

# Ver estadísticas
docker-compose exec db psql -U postgres -d dealaai_dev <<EOF
SELECT COUNT(*) FROM stock;
SELECT COUNT(*) FROM stock_historico;
EOF
```

## Paso 8: Ejecutar Manualmente (Si es Necesario)

```bash
# Opción 1: Comando Django
docker-compose exec backend python manage.py migrate_stock_and_scrape

# Opción 2: Script Python
docker-compose exec backend python run_stock_migration.py

# Opción 3: Con opciones personalizadas
docker-compose exec backend python manage.py migrate_stock_and_scrape --paginas 10 --cantidad 100

# Opción 4: Desde shell local (sin Docker)
cd /workspace/backend
python manage.py migrate_stock_and_scrape
```

## 🎯 Checklist de Verificación

- [ ] Dependencias instaladas (`requirements/base.txt`)
- [ ] Tablas creadas (`python manage.py migrate stock`)
- [ ] Al menos una ejecución manual exitosa
- [ ] Datos visibles en Admin o BD
- [ ] Docker running y scheduler activo
- [ ] Logs sin errores
- [ ] Histórico comenzó a acumular datos

## 🐛 Troubleshooting Rápido

### Error: "No module named 'requests'"

```bash
pip install -r requirements/base.txt
```

### Error: "table stock does not exist"

```bash
python manage.py migrate stock
```

### Error: "Scaper no encuentra vehículos"

- Normal si coches.net cambió su estructura HTML
- Se generarán datos aleatorios en su lugar
- Ver logs para más detalles

### El scheduler no ejecuta a las 01:00

- Verificar que Django está en primer plano (no daemon)
- Ver logs: `docker-compose logs backend | grep -i scheduler`
- Probar ejecución manual: `python manage.py migrate_stock_and_scrape`

### Datos duplicados en BD

- Verificar bastidores únicos: `SELECT DISTINCT bastidor FROM stock`
- El modelo usa `bastidor` como PRIMARY KEY
- No debería haber duplicados

## 📊 Ejemplos de Consultas Útiles

```bash
# Entrar a PostgreSQL
docker-compose exec db psql -U postgres -d dealaai_dev

# Ver cantidad de registros
SELECT COUNT(*) as total FROM stock;

# Ver distribución por marca
SELECT marca, COUNT(*) FROM stock GROUP BY marca ORDER BY count DESC;

# Ver vehículos más antiguos en stock
SELECT bastidor, marca, modelo, dias_stock FROM stock ORDER BY dias_stock DESC LIMIT 5;

# Ver histórico del último día
SELECT COUNT(*) FROM stock_historico WHERE fecha_insert > NOW() - INTERVAL '1 day';

# Salir
\q
```

## 🎓 Estructura de Archivos Relevantes

```
/workspace/backend/
├── apps/stock/
│   ├── models.py                    # Modelos Stock y StockHistorico
│   ├── admin.py                     # Interfaz Admin
│   ├── scrapers.py                  # Lógica de scraping
│   ├── scheduler.py                 # Programación automática
│   ├── management/commands/
│   │   └── migrate_stock_and_scrape.py  # Comando Django
│   └── README_STOCK.md              # Documentación completa
├── run_stock_migration.py           # Script manual
├── requirements/
│   └── base.txt                     # Dependencias
└── manage.py

/workspace/database/
└── migrations/
    └── stock_queries.sql            # Queries SQL útiles

/workspace/
├── docker-compose.yml               # Servicios (ya tiene Redis, Celery, etc.)
└── STOCK_SETUP_SUMMARY.md           # Resumen de lo creado
```

## 📞 Contacto y Soporte

Para problemas o mejoras, consultar con el equipo de desarrollo.

---

**Última actualización**: 26 de Octubre, 2025  
**Versión**: 1.0 - Producción  
**Status**: ✅ Listo para usar
