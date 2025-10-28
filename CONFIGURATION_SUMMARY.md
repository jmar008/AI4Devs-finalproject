# 📋 Configuración Actual - Resumen

## ✅ Archivos de Configuración Completados

### 1. **`.env`** (Raíz del Proyecto)

Ubicación: `c:\___apps___\all4devs\AI4Devs-finalproject\.env`

**Propósito**: Variables globales para docker-compose

**Variables Configuradas**:

```env
# Docker
COMPOSE_PROJECT_NAME=dealaai

# Backend
DJANGO_SETTINGS_MODULE=dealaai.settings.development
DEBUG=True
DB_NAME=dealaai_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
REDIS_URL=redis://redis:6379/0

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8080
NODE_ENV=development

# Database
POSTGRES_DB=dealaai_dev

# PgAdmin
PGADMIN_DEFAULT_EMAIL=admin@dealaai.com
PGADMIN_DEFAULT_PASSWORD=admin123
```

### 2. **`backend/.env`** (Backend Django)

Ubicación: `c:\___apps___\all4devs\AI4Devs-finalproject\backend\.env`

**Propósito**: Configuración específica de Django

**Variables Configuradas**:

```env
# Django
DEBUG=True
SECRET_KEY=django-insecure-dev-key-...
ALLOWED_HOSTS=localhost,127.0.0.1,backend,nginx

# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/dealaai_dev

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://localhost:3000,http://localhost:3001

# Media/Static
MEDIA_ROOT=/app/media
STATIC_ROOT=/app/staticfiles

# Logging
LOG_LEVEL=DEBUG

# Seguridad (Desarrollo - Deshabilitado)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
```

---

## 🔑 Credenciales de Desarrollo

### Acceso a Servicios

| Servicio          | URL                          | Usuario             | Contraseña |
| ----------------- | ---------------------------- | ------------------- | ---------- |
| **Frontend**      | http://localhost:8080        | -                   | -          |
| **Backend Admin** | http://localhost:8080/admin/ | `admin`             | `admin123` |
| **PgAdmin**       | http://localhost:5050        | `admin@dealaai.com` | `admin123` |
| **PostgreSQL**    | localhost:5433               | `postgres`          | `postgres` |
| **Redis**         | localhost:6380               | -                   | -          |

### Base de Datos

```
Host: db (docker) o localhost:5433 (host)
Puerto: 5432 (docker) o 5433 (host)
Database: dealaai_dev
Usuario: postgres
Contraseña: postgres
```

---

## 🐳 Docker Compose

### Servicios Disponibles

```yaml
Servicios en docker-compose.yml:
├── db (PostgreSQL + pgvector)
├── redis (Cache)
├── backend (Django - puerto 8000)
├── frontend (Next.js - puerto 3001)
├── nginx (Reverse Proxy - puerto 8080)
└── pgadmin (Administración BD - puerto 5050)
```

### Comandos Útiles

```powershell
# Iniciar todo
docker-compose up -d

# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f

# Parar todo
docker-compose down

# Limpiar volúmenes (⚠️ borra datos)
docker-compose down -v
```

---

## 🔄 Punto de Entrada

### Acceder a la Aplicación

1. **Frontend (Principal)**

   ```
   http://localhost:8080
   ```

2. **Django Admin**

   ```
   http://localhost:8080/admin/
   Credenciales: admin / admin123
   ```

3. **PgAdmin (Gestión BD)**
   ```
   http://localhost:5050
   Credenciales: admin@dealaai.com / admin123
   ```

---

## ⚙️ Configuración por Entorno

### Desarrollo (Actual)

- ✅ `DEBUG=True` (muestra errores detallados)
- ✅ `ALLOWED_HOSTS=localhost,127.0.0.1,backend,nginx`
- ✅ `SECURE_SSL_REDIRECT=False`
- ✅ `EMAIL_BACKEND=console` (muestra emails en logs)
- ✅ Logs detallados (`LOG_LEVEL=DEBUG`)

### Producción (EasyPanel)

- ✅ `DEBUG=False` (oculta errores internos)
- ✅ `ALLOWED_HOSTS=tu-dominio.com` (configurable)
- ✅ `SECURE_SSL_REDIRECT=True` (fuerza HTTPS)
- ✅ `SESSION_COOKIE_SECURE=True`
- ✅ Logs limitados

---

## 🤖 API Key de OpenRouter (Chat AI)

### Estado Actual

- ⚠️ La API key incluida está **expirada**
- ❌ Error 401 - User not found
- 🔧 El chat AI no funciona hasta renovar la key

### Cómo Renovar

1. **Ir a**: https://openrouter.ai/
2. **Crear cuenta** o iniciar sesión
3. **Settings** → **Keys** → **New Key**
4. **Copiar** la nueva key
5. **Actualizar** en `backend/.env`:
   ```env
   DEEPSEEK_API_KEY=sk-or-v1-NUEVA-KEY-AQUI
   ```
6. **Reiniciar** backend:
   ```powershell
   docker-compose restart backend
   ```

---

## 📊 Estructura de Archivos `.env`

```
AI4Devs-finalproject/
├── .env                              ← Variables globales (docker-compose)
│
├── backend/
│   └── .env                          ← Variables Django específicas
│
├── frontend/
│   └── .env.local                    ← Variables Next.js (si existe)
│
├── .env.easypanel.example            ← Plantilla para producción
└── .env.example                      ← Plantilla para desarrollo
```

---

## ✅ Verificación Rápida

### Validar Configuración

```powershell
# 1. Ver que se cargaron las variables
docker-compose config | grep -E "DEBUG|DB_NAME|POSTGRES_PASSWORD"

# 2. Verificar que los contenedores ven las variables
docker-compose exec backend printenv | grep DEBUG
docker-compose exec backend printenv | grep DB_NAME

# 3. Verificar conexión a BD
docker-compose exec backend python manage.py dbshell

# 4. Verificar Redis
docker-compose exec redis redis-cli ping
```

### Esperado

```
✅ DEBUG=True
✅ DB_NAME=dealaai_dev
✅ POSTGRES_PASSWORD=postgres
✅ NEXT_PUBLIC_API_URL=http://localhost:8080
✅ Todos los servicios "healthy"
```

---

## 🚀 Próximos Pasos

1. ✅ **Configuración lista** - `.env` completado
2. ⏭️ **Iniciar servicios**:
   ```powershell
   docker-compose down -v  # Limpiar
   docker-compose up -d --build  # Iniciar
   ```
3. ⏭️ **Esperar** a que todos los servicios estén healthy
4. ⏭️ **Verificar** acceso a http://localhost:8080
5. ⏭️ **Crear superusuario** si es necesario:
   ```powershell
   docker-compose exec backend python manage.py createsuperuser
   ```

---

## 📞 Troubleshooting Rápido

### ❌ "Connection refused" en Backend

```powershell
# Esperar a que DB inicie
docker-compose logs db
docker-compose restart backend
```

### ❌ "Frontend no carga"

```powershell
# Reconstruir frontend
docker-compose up -d --build frontend
docker-compose logs frontend  # Ver si hay errores
```

### ❌ "Variables de entorno no se cargan"

```powershell
# Docker-compose no lee .env automáticamente después de cambios
# Solución:
docker-compose down
docker-compose up -d  # Vuelve a leer .env
```

### ❌ "Puertos ya en uso"

```powershell
# Ver qué ocupan los puertos
netstat -ano | findstr :8080
netstat -ano | findstr :5433

# O cambiar puertos en docker-compose.yml
```

---

## 📚 Documentación Relacionada

- `DEVELOPMENT_ENVIRONMENT_READY.md` - Estado general del entorno
- `EASYPANEL_DEPLOYMENT_READY.md` - Para despliegue en producción
- `.env.easypanel.example` - Variables para producción
- `EASYPANEL_TROUBLESHOOTING.md` - Solucionar problemas en EasyPanel

---

**¡Configuración de desarrollo completada! 🎉**

Para empezar a trabajar:

```powershell
cd c:\___apps___\all4devs\AI4Devs-finalproject
docker-compose up -d
```

Luego accede a: **http://localhost:8080**
