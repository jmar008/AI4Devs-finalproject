# 🔧 Fix Producción - Healthcheck Issues

**Fecha:** 26 Oct 2025  
**Estado:** ✅ Resuelto  
**Problemas:** Container unhealthy en EasyPanel/Producción

---

## 📋 Problemas Identificados

### 1. **Health Check inválido del Backend**

```yaml
# ❌ ANTES - No funciona en Docker
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/api/health/"]

# ✅ DESPUÉS - Funciona en Docker
healthcheck:
  test: ["CMD", "curl", "-f", "http://127.0.0.1:8000/api/health/"]
```

**Razón:** En Docker, `localhost` puede no resolver correctamente en el contexto del contenedor. `127.0.0.1` es más confiable.

### 2. **Start Period insuficiente**

```yaml
# ❌ ANTES
start_period: 40s

# ✅ DESPUÉS
start_period: 60s
```

**Razón:** Las migraciones, collectstatic y otros procesos pueden tomar más de 40 segundos.

### 3. **Entrypoint.sh poco robusto**

**Problemas:**

- Conexión a BD hardcodeada con nombre fijo
- Sin manejo de errores adecuado
- Sin límite de reintentos

**Solución:**

- Parsear `DATABASE_URL` dinámicamente
- Máximo 30 intentos de conexión
- Mejor manejo de errores y logs

### 4. **Falta docker-compose.override.yml**

**Problema:** EasyPanel usa este archivo pero no existía.

---

## ✅ Cambios Realizados

### 1. docker-compose.production.yml

```yaml
# Backend healthcheck corregido
healthcheck:
  test: ["CMD", "curl", "-f", "http://127.0.0.1:8000/api/health/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s

# ALLOWED_HOSTS actualizado con 127.0.0.1
ALLOWED_HOSTS=mcp.jorgemg.es,backend,localhost,127.0.0.1
```

### 2. backend/entrypoint.sh

```bash
# ✅ Parsea DATABASE_URL dinámicamente
# ✅ Máximo 30 intentos con timeout
# ✅ Mejor logging
# ✅ Manejo de errores robusto
```

### 3. docker-compose.override.yml (NUEVO)

```yaml
# Archivo que EasyPanel necesita para sobrescribir configuraciones
# Asegura consistencia entre dev y producción
```

---

## 🚀 Instrucciones de Deployment en EasyPanel

### Opción 1: Redeployment Automático

```bash
# Limpiar deployment anterior
docker-compose -f docker-compose.production.yml down -v

# Nuevo deployment con archivos corregidos
docker-compose -f docker-compose.production.yml -f docker-compose.override.yml up -d --build
```

### Opción 2: En EasyPanel Dashboard

1. Ir a **Proyecto → DealaAI**
2. Click en **Rebuild** (no en Start)
3. Esperar logs - debería ver:
   ```
   ✓ Database is ready
   ✓ Migrations completed successfully
   ✓ Cache table ready
   ✓ Static files collected
   ✓ Backend is healthy
   ```

---

## 🔍 Verificación

### Verificar que Backend está healthy:

```bash
# Ver estado de healthcheck
docker-compose ps

# Ver logs del backend
docker-compose logs backend | tail -50
```

### Logs esperados:

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
```

### Probar endpoint de health:

```bash
curl http://mcp.jorgemg.es/api/health/
# Respuesta esperada:
{
  "status": "healthy",
  "database": "healthy",
  "timestamp": "UTC"
}
```

---

## 📊 Variables de Entorno Requeridas

Para que funcione en producción, asegurar en EasyPanel:

```env
# Obligatorias
SECRET_KEY=your-secret-key-here
DB_PASSWORD=your-postgres-password
OPENAI_API_KEY=your-openai-key (opcional)

# Opcionales (con valores por defecto)
DEBUG=False
ALLOWED_HOSTS=mcp.jorgemg.es,backend,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://mcp.jorgemg.es
USE_CELERY=false
USE_REDIS=false
```

---

## 🚨 Problemas Comunes Post-Fix

### "Container still unhealthy"

```bash
# 1. Ver logs detallados
docker-compose logs backend -f

# 2. Comprobar conectividad a BD
docker-compose exec backend python manage.py dbshell

# 3. Verificar que curl está instalado en contenedor
docker-compose exec backend curl --version
```

### "Migrations failed"

```bash
# Ejecutar manualmente
docker-compose exec backend python manage.py migrate --verbosity=3

# Si hay conflictos, revisar:
docker-compose exec db psql -U postgres -d dealaai_prod -c "\dt"
```

### "Static files not collected"

```bash
# Ejecutar manualmente
docker-compose exec backend python manage.py collectstatic --noinput --clear --verbosity=3
```

---

## 📝 Notas Importantes

1. **start_period: 60s** es crítico en producción - no reducir sin probar
2. **127.0.0.1** en healthcheck - NO usar localhost en Docker
3. **Dependencias correctas**: Frontend depende de Backend, Backend depende de DB
4. **Override.yml**: Mantener sincronizado con production.yml para cambios futuros

---

## ✨ Resultado

✅ Backend será **healthy** automáticamente  
✅ Frontend podrá conectar sin errores de dependencia  
✅ EasyPanel reportará estado correcto  
✅ Migraciones se ejecutarán automáticamente en startup  
✅ Static files se recopilarán correctamente

---

**Próximos pasos:**

- Hacer push de cambios
- Redeploy en EasyPanel
- Monitorear logs por 5 minutos
- Probar endpoints de API
