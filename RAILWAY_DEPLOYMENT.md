# 🚀 Despliegue en Railway

Guía completa para desplegar tu proyecto DealaAI en Railway.

## 📋 Requisitos Previos

- Cuenta en [Railway.app](https://railway.app)
- Repositorio en GitHub con tu código
- API Key de OpenRouter (para funcionalidades de chat AI)

## 🛠️ Archivos Necesarios

Asegúrate de tener estos archivos en tu repositorio:

- `docker-compose.railway.yml` ✅ (creado)
- `docker/frontend/Dockerfile.prod` ✅ (ya existe)
- `docker/backend/Dockerfile.prod` ✅ (ya existe)
- `backend/.env.production` ✅ (ya existe)
- `.env.railway.example` ✅ (creado)

## 🚀 Pasos de Despliegue

### 1. Preparar el Código

```bash
# Hacer ejecutable el script de configuración
chmod +x setup-railway.sh

# Ejecutar configuración (genera SECRET_KEY y crea .env.railway)
./setup-railway.sh
```

### 2. Subir Código a GitHub

```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### 3. Crear Proyecto en Railway

1. Ve a [railway.app](https://railway.app) y haz login
2. Haz clic en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Conecta tu cuenta de GitHub y selecciona el repositorio
5. Railway detectará automáticamente `docker-compose.railway.yml`

### 4. Configurar Variables de Entorno

En el dashboard de Railway:

1. Ve a la pestaña **"Variables"**
2. Copia las variables desde el archivo `.env.railway` generado:

```env
# Copia estas variables una por una:
SECRET_KEY=tu-secret-key-generado
ALLOWED_HOSTS=tu-proyecto.up.railway.app,backend,nginx,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://tu-proyecto.up.railway.app
NEXT_PUBLIC_API_URL=https://tu-proyecto.up.railway.app
NEXT_PUBLIC_WS_URL=wss://tu-proyecto.up.railway.app/ws
NEXT_PUBLIC_DOMAIN=tu-proyecto.up.railway.app
DEEPSEEK_API_KEY=sk-or-v1-tu-api-key
DEBUG=False
DJANGO_SETTINGS_MODULE=dealaai.settings.production
```

### 5. Desplegar

1. Haz clic en **"Deploy"**
2. Railway construirá y desplegará todos los servicios
3. Espera 5-10 minutos para el primer despliegue

## 🔍 Verificación del Despliegue

Una vez desplegado, verifica que funcione:

- **Frontend**: `https://tu-proyecto.up.railway.app`
- **Admin Django**: `https://tu-proyecto.up.railway.app/admin/`
- **API Health**: `https://tu-proyecto.up.railway.app/health/`
- **API Docs**: `https://tu-proyecto.up.railway.app/api/docs/`

## 🗄️ Base de Datos y Redis

Railway crea automáticamente:

- **PostgreSQL** con pgvector
- **Redis** para cache

Las URLs se configuran automáticamente en:

- `DATABASE_URL`
- `REDIS_URL`

## 👤 Crear Superusuario Django

```bash
# Conectar al contenedor backend
railway connect

# Crear superusuario
python manage.py createsuperuser
```

## 🔧 Comandos Útiles

### Ver Logs

```bash
railway logs
```

### Conectar a Base de Datos

```bash
railway connect
# Dentro del contenedor puedes usar psql o python manage.py dbshell
```

### Ejecutar Migraciones (si es necesario)

```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
```

## 💰 Costos

- **Starter**: Gratuito (~512MB RAM)
- **Hobby**: $5/mes (1GB RAM, 32GB storage)
- **Pro**: $10/mes (4GB RAM, 128GB storage)

## 🐛 Solución de Problemas

### Error: "Build failed"

- Verifica que todos los Dockerfiles sean correctos
- Revisa que las rutas en `docker-compose.railway.yml` existan

### Error: "Database connection failed"

- Verifica que Railway haya creado la base de datos
- Comprueba las variables `DATABASE_URL` y `REDIS_URL`

### Frontend no carga

- Verifica `NEXT_PUBLIC_API_URL`
- Limpia caché del navegador

### API no responde

- Revisa logs: `railway logs`
- Verifica que el backend esté healthy

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs en Railway dashboard
2. Verifica todas las variables de entorno
3. Asegúrate de que los servicios estén "healthy"

¡Tu aplicación estará funcionando 24/7 con SSL automático y escalado incluido! 🎉
