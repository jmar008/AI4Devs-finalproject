# 🔧 EasyPanel - Fix Docker Build

**Fecha:** 26 de Octubre, 2025  
**Status:** ✅ CORREGIDO

---

## 📋 Problemas Solucionados

### 1. ❌ Error: `requirements file not found: base.txt`

**Problema:**

```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'base.txt'
```

**Causa:**

- El `requirements/production.txt` contenía `-r base.txt` (import relativo)
- El Dockerfile copiaba `requirements/production.txt` pero no `requirements/base.txt`
- En Docker, la ruta relativa no funcionaba

**Solución:**
✅ Creado `/workspace/backend/requirements.txt` consolidado

- Contiene TODAS las dependencias de `base.txt` + `production.txt`
- Actualizado `Dockerfile.prod` para usar `requirements.txt` directamente

---

### 2. ❌ Warning: `version attribute is obsolete`

**Problema:**

```
the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
```

**Causa:**

- El archivo `docker-compose.production.yml` tenía `version: "3.8"` en el inicio
- EasyPanel deprecó esta versión (Docker Compose 2.0+)

**Solución:**
✅ Eliminada la línea `version: "3.8"`

- El archivo ahora empieza directamente con `services:`

---

### 3. ❌ Warning: Variables de entorno vacías

**Problema:**

```
The "DB_PASSWORD" variable is not set. Defaulting to a blank string.
The "SECRET_KEY" variable is not set. Defaulting to a blank string.
```

**Causa:**

- EasyPanel no tenía las variables de entorno configuradas
- El `docker-compose.yml` referencia variables con `${VARIABLE_NAME}`

**Solución:**
✅ Configurar variables en EasyPanel (ver sección **Configuración en EasyPanel**)

---

## 📦 Cambios Realizados

### Nuevo archivo: `/workspace/backend/requirements.txt`

Consolidación de todas las dependencias Python:

```
# Core Django
Django==4.2.7
djangorestframework==3.14.0
django-filter==23.3
django-cors-headers==4.3.0

# Database
psycopg2-binary==2.9.9
pgvector==0.2.3

# Authentication
djangorestframework-simplejwt==5.3.0

# API Documentation
drf-spectacular==0.26.5

# Environment
python-decouple==3.8

# Utilities
python-slugify==8.0.1
Pillow==10.1.0

# Date/Time
pytz==2023.3

# Web Scraping
requests==2.31.0
beautifulsoup4==4.12.2

# Scheduled Tasks
celery==5.3.4
redis==5.0.1

# APScheduler for background tasks
apscheduler==3.10.4

# Production Server
gunicorn==21.2.0

# Monitoring
sentry-sdk==1.38.0

# Performance
django-redis==5.4.0
```

### Modificado: `/workspace/docker/backend/Dockerfile.prod`

**Cambio:**

```dockerfile
# Antes:
COPY requirements/production.txt requirements.txt

# Ahora:
COPY requirements.txt requirements.txt
```

### Modificado: `/workspace/docker-compose.production.yml`

**Cambio:**

```yaml
# Antes:
version: "3.8"
services:

# Ahora:
services:
```

---

## 🔐 Configuración en EasyPanel

### Paso 1: Accede a EasyPanel

1. Ve a tu panel: `https://easypanel.io`
2. Selecciona el proyecto **dealaai**
3. Ve a **"Settings"** o **"Environment"**

### Paso 2: Agrega estas variables

Copia y pega en EasyPanel:

```
# Base de Datos
DB_PASSWORD=contraseña_muy_segura_aqui_123456

# Seguridad Django
SECRET_KEY=django-insecure-asdfjkl;asdfjkl;asdfjkl;asdfjkl;asdfjkl;

# OpenAI (si usas IA)
OPENAI_API_KEY=sk-proj-tu-api-key-aqui

# JWT
JWT_SECRET=tu-jwt-secret-muy-largo-aqui

# PgAdmin
PGADMIN_PASSWORD=contraseña_pgadmin_123

# Google OAuth (opcional)
GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-google-client-secret

# Supabase (opcional)
SUPABASE_ANON_KEY=tu-supabase-anon-key
SUPABASE_SERVICE_KEY=tu-supabase-service-key
```

### Paso 3: Genera valores seguros

Para `SECRET_KEY` y `JWT_SECRET`, ejecuta en terminal:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

Repite 2 veces para tener 2 valores diferentes.

### Paso 4: Redeploy

1. En EasyPanel, click **"Redeploy"** o **"Deploy"**
2. Espera a que compile (3-5 minutos)
3. Los errores deberían desaparecer ✅

---

## ✅ Verificación

Después del redeploy:

```bash
# 1. Verifica que no hay warnings
# (Los logs deberían estar limpios sin "The X variable is not set")

# 2. Prueba la app
curl -I https://mcp.jorgemg.es/
# Debería responder con 200 o 302 (redirect a login)

# 3. Prueba el login
# https://mcp.jorgemg.es/login

# 4. Verifica logs
docker-compose -f docker-compose.production.yml logs backend | tail -50
```

---

## 📊 Cambios en Git

```bash
commit 4c010cd
Author: Tu Nombre
Date:   Oct 26, 2025

    fix: consolidate requirements.txt for Docker production build

    - Created /workspace/backend/requirements.txt with all dependencies
    - Updated Dockerfile.prod to use consolidated requirements.txt
    - Removed version attribute from docker-compose.production.yml

 DOCKERFILES_PRODUCTION_EASYPANEL.md |  21 +++++
 docker/backend/Dockerfile.prod       |   2 +-
 backend/requirements.txt             | 94 ++++++++++++++++++++++++
```

---

## 🚀 Próximos Pasos

1. ✅ Verifica que no hay warnings en EasyPanel
2. ✅ Prueba login/logout
3. ✅ Verifica que sesión persiste (F5)
4. ✅ Verifica que stock table carga datos
5. ✅ Configura backups y healthchecks
6. ✅ Monitorea logs las primeras 24 horas

---

## 🆘 Troubleshooting

### Sigue habiendo errores de `requirements`?

1. Limpia caché de Docker:

   ```bash
   docker system prune -a
   ```

2. Redeploy en EasyPanel con **"Force Rebuild"**

### Variables siguen vacías?

1. Verifica que están guardadas en EasyPanel
2. Recarga la página (Ctrl+Shift+R)
3. Redeploy nuevamente

### 502 Bad Gateway?

1. Espera 30 segundos (el contenedor está iniciando)
2. Verifica logs: `docker-compose logs backend | tail -100`
3. Comprueba que la BD está UP: `docker-compose logs db | tail -20`

---

## 📞 Soporte

Si tienes dudas:

1. Revisa `/workspace/DEPLOYMENT_GUIDE_PRODUCTION.md` (sección Troubleshooting)
2. Verifica logs en EasyPanel: **"Logs"** tab
3. Ejecuta healthcheck: `/api/health/`

---

**¡Listo para producción! 🚀**
