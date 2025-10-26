# 🚀 Despliegue en Easypanel con Heroku Buildpacks

## ✅ Archivos Configurados

He configurado el proyecto para usar **Heroku Buildpacks** en lugar de Docker:

### Archivos Creados:

1. **`Procfile`** - Define los procesos a ejecutar:

   - `web`: Gunicorn para Django (Puerto automático $PORT)
   - `worker`: Celery Worker para tareas asíncronas
   - `beat`: Celery Beat para tareas programadas

2. **`runtime.txt`** - Especifica Python 3.11.9

3. **`.buildpacks`** - Lista de buildpacks a usar:

   - Python (Django backend)
   - Node.js (Next.js frontend)
   - APT (dependencias del sistema)

4. **`Aptfile`** - Paquetes del sistema necesarios:

   - postgresql-client
   - build-essential
   - libpq-dev

5. **`package.json`** (raíz) - Para buildpack de Node.js:

   - Build automático del frontend
   - Workspace configuration

6. **`release.sh`** - Tareas pre-deploy:

   - Migraciones de base de datos
   - Collectstatic

7. **`project.toml`** - Configuración Cloud Native Buildpacks

---

## 📋 Configuración en Easypanel

### 1️⃣ Crear Nueva Aplicación

En Easypanel, crea una nueva app con estas configuraciones:

**Tipo de Deploy:** `Buildpacks` (no Docker)

### 2️⃣ Configurar Repositorio

- **GitHub Repo:** `jmar008/AI4Devs-finalproject`
- **Branch:** `feature/TICK-002-user-auth` (o `main`)
- **Auto Deploy:** Activado

### 3️⃣ Variables de Entorno

Configura estas variables en Easypanel:

```bash
# Django
DJANGO_SECRET_KEY=tu-secret-key-super-segura-de-50-caracteres
DJANGO_SETTINGS_MODULE=dealaai.settings.production
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,*.easypanel.host

# Base de Datos (usa el servicio PostgreSQL de Easypanel)
DATABASE_URL=postgres://usuario:password@host:5432/dealaai_prod

# Redis (usa el servicio Redis de Easypanel)
REDIS_URL=redis://host:6379/0
CELERY_BROKER_URL=redis://host:6379/0
CELERY_RESULT_BACKEND=redis://host:6379/1

# CORS
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://app.tu-dominio.com

# DeepSeek AI (para Chat IA)
DEEPSEEK_API_KEY=sk-tu-api-key-de-deepseek

# Opcional: Sentry para monitoreo
SENTRY_DSN=https://...

# Frontend (Next.js)
NEXT_PUBLIC_API_URL=https://tu-dominio.com/api
NODE_ENV=production
```

### 4️⃣ Servicios Adicionales

Crea estos servicios en Easypanel:

#### PostgreSQL con pgvector:

```yaml
image: ankane/pgvector:latest
environment:
  POSTGRES_DB: dealaai_prod
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: TU_PASSWORD_SEGURA
volumes:
  - postgres_data:/var/lib/postgresql/data
```

#### Redis:

```yaml
image: redis:7-alpine
volumes:
  - redis_data:/data
```

### 5️⃣ Procesos a Activar

En la configuración de tu app, activa estos procesos:

- ✅ **web** - Servidor Django (escalable)
- ✅ **worker** - Celery Worker (1 instancia mínimo)
- ✅ **beat** - Celery Beat (solo 1 instancia)

### 6️⃣ Dominio y Routing

**Dominio Principal:** Apunta al proceso `web`

---

## 🔧 Comandos Útiles

### Ver logs en tiempo real:

```bash
# En Easypanel Console
heroku logs --tail
```

### Ejecutar migraciones manualmente:

```bash
heroku run python backend/manage.py migrate
```

### Crear superusuario:

```bash
heroku run python backend/manage.py createsuperuser
```

### Shell de Django:

```bash
heroku run python backend/manage.py shell
```

---

## ⚡ Ventajas de Buildpacks vs Docker

✅ **Más rápido**: Build incremental, no reconstruye todo  
✅ **Más simple**: No necesitas Dockerfile ni docker-compose  
✅ **Auto-detección**: Detecta Python y Node.js automáticamente  
✅ **Escalable**: Fácil escalar procesos web/worker  
✅ **Estándar**: Compatible con Heroku, Railway, Render, etc

---

## 🎯 Próximos Pasos

1. Haz push de estos cambios:

   ```bash
   git add .
   git commit -m "feat: Add Heroku Buildpacks configuration for production"
   git push origin feature/TICK-002-user-auth
   ```

2. En Easypanel:

   - Crea la app con buildpacks
   - Configura las variables de entorno
   - Crea servicios PostgreSQL y Redis
   - Activa los 3 procesos (web, worker, beat)
   - Deploy!

3. Verifica el deploy:
   - Revisa los logs de build
   - Verifica que las migraciones se ejecutaron
   - Prueba la URL de tu app
   - Verifica el Chat IA

---

## 🐛 Troubleshooting

### Build falla en Python:

- Verifica que `runtime.txt` tenga la versión correcta
- Revisa que `requirements.txt` esté en el path correcto

### Build falla en Node.js:

- Verifica que `package.json` tenga los scripts necesarios
- Revisa los logs del `heroku-postbuild`

### App no inicia:

- Verifica las variables de entorno (DATABASE_URL, etc.)
- Revisa los logs del proceso `web`
- Verifica que el puerto sea `$PORT` (no hardcoded)

### Celery no funciona:

- Verifica que REDIS_URL esté configurado
- Revisa los logs del proceso `worker` y `beat`
- Verifica la conexión a Redis

---

¡Listo para desplegar! 🚀
