# 🐛 Debugging Producción - EasyPanel

## 🚨 Si sigue mostrando "Container unhealthy"

### Paso 1: Verificar logs en tiempo real

```bash
# En la terminal de EasyPanel o SSH
docker logs -f dealaai_backend_prod

# O si estás en el devcontainer
cd /workspace
docker-compose -f docker-compose.production.yml logs -f backend
```

**Qué buscar:**

- `✓ Database is ready` - Si no aparece, problema de conexión DB
- `✓ Migrations completed successfully` - Si no aparece, error en migraciones
- `Starting Gunicorn` - Si no aparece, error antes de iniciar servidor
- Cualquier línea que empiece con `✗ Error`

---

### Paso 2: Verificar conectividad a Base de Datos

```bash
# Entrar al contenedor backend
docker-compose exec backend bash

# Probar conexión a BD
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='db',
        database='dealaai_prod',
        user='postgres',
        password='${DB_PASSWORD}'
    )
    print('✓ Connection successful')
    conn.close()
except Exception as e:
    print(f'✗ Connection failed: {e}')
"
```

---

### Paso 3: Verificar que curl está disponible

```bash
docker-compose exec backend curl --version
```

Si da error "command not found":

- Esto es un problema en el Dockerfile
- El contenedor necesita `curl` instalado

**Solución:**
El `Dockerfile.prod` ya lo instala. Si sigue sin funcionar, forzar rebuild:

```bash
docker-compose -f docker-compose.production.yml build --no-cache backend
```

---

### Paso 4: Probar el endpoint de health manualmente

```bash
# Dentro del contenedor backend
curl -v http://127.0.0.1:8000/api/health/

# Respuesta esperada:
# < HTTP/1.1 200 OK
# {
#   "status": "healthy",
#   "database": "healthy",
#   "timestamp": "UTC"
# }
```

---

### Paso 5: Verificar variables de entorno

```bash
# Ver todas las variables en el contenedor
docker-compose exec backend env | grep -E "DB_|DATABASE|SECRET|DEBUG"
```

**Esperado:**

```
DEBUG=False
DATABASE_URL=postgresql://postgres:***@db:5432/dealaai_prod
DJANGO_SETTINGS_MODULE=dealaai.settings.production
```

---

### Paso 6: Ejecutar migraciones manualmente

```bash
docker-compose exec backend python manage.py migrate --verbosity=3
```

Si hay error, ver el mensaje completo.

---

### Paso 7: Verificar que Base de Datos está healthy

```bash
# Desde afuera del contenedor
docker-compose ps

# Buscar línea de 'db' - debe decir "healthy"
# NAME                    STATUS
# dealaai_db_prod         Up X minutes (healthy)  ← Debe ser (healthy)
```

Si muestra `(unhealthy)`:

```bash
docker-compose logs db | tail -20
```

---

## 🔧 Soluciones Comunes

### "database connection refused"

```bash
# Verificar que BD está corriendo
docker-compose ps db

# Si no está corriendo
docker-compose up -d db

# Esperar 10 segundos
sleep 10

# Probar reconexión
docker-compose exec backend python manage.py dbshell
```

### "relation 'auth_user' does not exist"

Significa que las migraciones no se ejecutaron correctamente.

```bash
# Ejecutar todas las migraciones
docker-compose exec backend python manage.py migrate --run-syncdb
```

### "curl: command not found"

El healthcheck falla porque curl no está disponible.

```bash
# Opción 1: Usar wget en lugar de curl en el healthcheck
# docker-compose.production.yml línea del healthcheck:
test: ["CMD", "wget", "--spider", "-q", "http://127.0.0.1:8000/api/health/"]

# Opción 2: Rebuild sin cache
docker-compose -f docker-compose.production.yml build --no-cache backend
docker-compose -f docker-compose.production.yml up -d
```

### "Port 8000 already in use"

```bash
# Ver qué está usando el puerto
lsof -i :8000

# O directamente, matar el proceso viejo
docker-compose down
docker-compose -f docker-compose.production.yml up -d
```

---

## ✅ Validación Final

Cuando funcione, deberías ver:

### 1. En `docker-compose ps`:

```
NAME                    STATUS
dealaai_backend_prod    Up X minutes (healthy) ← ¡IMPORTANTE!
dealaai_db_prod         Up X minutes (healthy)
dealaai_frontend_prod   Up X minutes (healthy)
```

### 2. En logs del backend:

```
=== DealaAI Backend Startup ===
Database configuration:
  Host: db
  Database: dealaai_prod
  User: postgres
✓ Database is ready
✓ Migrations completed successfully
✓ Cache table ready
✓ Static files collected
=== Starting Gunicorn ===
[timestamp] [PID] [INFO] Starting gunicorn 22.0.0
[timestamp] [PID] [INFO] Listening at: http://0.0.0.0:8000 (PID)
```

### 3. Endpoint responde correctamente:

```bash
curl http://mcp.jorgemg.es/api/health/

# Respuesta:
{
  "status": "healthy",
  "database": "healthy",
  "timestamp": "UTC"
}
```

---

## 🚀 Si todo sigue sin funcionar

### Opción 1: Clean rebuild completo

```bash
# ADVERTENCIA: Esto elimina toda la data
docker-compose -f docker-compose.production.yml down -v

# Rebuild completo
docker-compose -f docker-compose.production.yml build --no-cache

# Iniciar nuevamente
docker-compose -f docker-compose.production.yml up -d
```

### Opción 2: Verificar archivo docker-compose.production.yml

Asegurar que tiene estas líneas exactas:

```yaml
backend:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://127.0.0.1:8000/api/health/"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 60s
```

### Opción 3: Verificar Dockerfile.prod

Asegurar que tiene estas líneas:

```dockerfile
# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/api/health/ || exit 1

# Instalar curl en dependencias del sistema
RUN apt-get install -y curl
```

---

## 📞 Soporte

Si ninguna solución funciona, envía estos comandos en una terminal:

```bash
docker-compose -f docker-compose.production.yml logs backend 2>&1 | tail -100
docker-compose ps
docker-compose exec backend env | grep -E "DB|DEBUG|DJANGO"
docker-compose exec backend python -c "import django; print(django.get_version())"
```

Copia el output completo para debugging.
