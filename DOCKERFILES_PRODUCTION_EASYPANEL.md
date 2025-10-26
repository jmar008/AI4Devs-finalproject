# 🐳 Dockerfiles de Producción para EasyPanel

## 📋 Ubicación de todos los Dockerfiles

### Estructura de directorios:

```
/workspace/docker/
├── backend/
│   ├── Dockerfile          (desarrollo)
│   └── Dockerfile.prod     (PRODUCCIÓN) ✅
├── frontend/
│   ├── Dockerfile          (desarrollo)
│   └── Dockerfile.prod     (PRODUCCIÓN) ✅
├── database/
│   └── Dockerfile          (PRODUCCIÓN - pgvector)
├── nginx/
│   ├── nginx.conf          (producción)
│   └── nginx.dev.conf      (desarrollo)
├── pgadmin/
│   └── servers.json        (config)
└── redis/
    └── redis.conf          (config)
```

---

## 🔧 Dockerfiles de PRODUCCIÓN

### 1️⃣ **Backend Django** - `/workspace/docker/backend/Dockerfile.prod`

**Ubicación:** `/workspace/docker/backend/Dockerfile.prod`

**Características principales:**
- ✅ Multi-stage build (menor tamaño de imagen)
- ✅ Python 3.11-slim
- ✅ Usuario no-root (`django`)
- ✅ Gunicorn + gevent (alta concurrencia)
- ✅ Health check incluido
- ✅ Collectstatic automático
- ✅ Logs a stdout/stderr

**Puertos:**
- `8000` - HTTP

**Comando:** 
```bash
gunicorn dealaai.wsgi:application --bind 0.0.0.0:8000 --workers 3 --worker-class gevent
```

**Variables de entorno necesarias:**
```
DJANGO_SETTINGS_MODULE=dealaai.settings.production
ALLOWED_HOSTS=mcp.jorgemg.es
DEBUG=False
SECRET_KEY=<producción-key>
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

**Requisitos:**
- Python 3.11
- PostgreSQL client libraries
- Build tools

---

### 2️⃣ **Frontend Next.js** - `/workspace/docker/frontend/Dockerfile.prod`

**Ubicación:** `/workspace/docker/frontend/Dockerfile.prod`

**Características principales:**
- ✅ Multi-stage build (distroless-like)
- ✅ Node 18-alpine (muy ligero)
- ✅ Build optimization (standalone output)
- ✅ Usuario no-root (`nextjs`)
- ✅ Health check incluido
- ✅ Soporta yarn/npm/pnpm

**Puertos:**
- `3000` - HTTP

**Comando:** 
```bash
node server.js
```

**Variables de entorno en build:**
```
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://mcp.jorgemg.es/api
NEXT_PUBLIC_WS_URL=wss://mcp.jorgemg.es/ws
NEXT_PUBLIC_DOMAIN=mcp.jorgemg.es
NEXT_TELEMETRY_DISABLED=1
```

**Requisitos:**
- Node 18+
- Build tools para libc

---

### 3️⃣ **Database PostgreSQL + pgvector** - `/workspace/docker/database/Dockerfile`

**Ubicación:** `/workspace/docker/database/Dockerfile`

**Características principales:**
- ✅ Base: `ankane/pgvector:latest` (PostgreSQL + extensión pgvector)
- ✅ Soporte para búsquedas vectoriales
- ✅ Scripts de inicialización

**Puertos:**
- `5432` - PostgreSQL

**Variables de entorno:**
```
POSTGRES_DB=dealaai_dev
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<segura>
```

**Scripts de inicialización:**
- Ubicación: `/docker-entrypoint-initdb.d/`
- Se ejecutan automáticamente en primer inicio

---

## 🚀 Cómo usar en EasyPanel

### Paso 1: Copiar Dockerfiles al servidor

```bash
# En el servidor con EasyPanel
mkdir -p /opt/dealaai/docker/{backend,frontend,database,nginx,redis,pgadmin}

# Copiar desde local
scp -r /workspace/docker/* usuario@servidor:/opt/dealaai/docker/
```

### Paso 2: Estructura en EasyPanel

```
/opt/dealaai/
├── docker-compose.production.yml
├── .env.production
└── docker/
    ├── backend/
    │   └── Dockerfile.prod      ← EasyPanel usa esta
    ├── frontend/
    │   └── Dockerfile.prod      ← EasyPanel usa esta
    └── database/
        └── Dockerfile           ← EasyPanel usa esta
```

### Paso 3: Crear servicios en EasyPanel

**Para Backend:**
```yaml
service: backend
dockerfile: ./docker/backend/Dockerfile.prod
build_context: .
ports: ["8000:8000"]
environment:
  - DJANGO_SETTINGS_MODULE=dealaai.settings.production
  - ALLOWED_HOSTS=mcp.jorgemg.es
```

**Para Frontend:**
```yaml
service: frontend
dockerfile: ./docker/frontend/Dockerfile.prod
build_context: .
ports: ["3000:3000"]
build_args:
  - NEXT_PUBLIC_API_URL=https://mcp.jorgemg.es/api
  - NEXT_PUBLIC_DOMAIN=mcp.jorgemg.es
```

**Para Database:**
```yaml
service: db
dockerfile: ./docker/database/Dockerfile
build_context: ./docker/database
ports: ["5432:5432"]
environment:
  - POSTGRES_PASSWORD=<segura>
```

---

## 📊 Comparación: Desarrollo vs Producción

| Característica | Dockerfile | Dockerfile.prod |
|---|---|---|
| **Imagen base** | Full | Slim/Alpine |
| **Tamaño** | ~1-2GB | ~200-500MB |
| **User** | Root | No-root |
| **Gunicorn** | ❌ | ✅ (3 workers) |
| **Health check** | ❌ | ✅ |
| **Multi-stage** | ❌ | ✅ |
| **DEBUG** | True | False |
| **Static files** | Servidos por Django | Pre-recolectados |

---

## 🔐 Seguridad en Dockerfiles

### Backend (Dockerfile.prod):
- ✅ Usuario `django` (no-root)
- ✅ Directorio de trabajo protegido
- ✅ Permisos correctos (`chown`)
- ✅ No ejecuta como root

### Frontend (Dockerfile.prod):
- ✅ Usuario `nextjs` (no-root)
- ✅ GID 1001, UID 1001 fijos
- ✅ Standalone build (sin fuentes)

### Database (Dockerfile):
- ✅ Basado en imagen oficial de pgvector
- ✅ Contraseña en variables de entorno
- ✅ No tiene credenciales hardcodeadas

---

## 🏗️ Proceso de Build en EasyPanel

### Backend:
1. **Base stage**: Python 3.11-slim
2. **Builder stage**: Instala dependencias de `requirements/production.txt`
3. **Production stage**: Copia solo lo necesario
4. **Collectstatic**: Recolecta static files
5. **Cmd**: Inicia gunicorn

**Tiempo**: ~3-5 minutos (primera vez), ~1-2 min (cached)

### Frontend:
1. **Base stage**: Node 18-alpine
2. **Deps stage**: Instala dependencias
3. **Builder stage**: Build de Next.js
4. **Runner stage**: Imagen final optimizada
5. **Cmd**: Inicia servidor Next.js

**Tiempo**: ~4-8 minutos (primera vez), ~2-3 min (cached)

### Database:
1. **Base**: pgvector preinstalado
2. **Init scripts**: Copia scripts
3. **Ready**: Listo para usar

**Tiempo**: ~30-60 segundos

---

## 🔍 Verificación de Dockerfiles

### Validar Dockerfile syntax:
```bash
docker build --dry-run -f /workspace/docker/backend/Dockerfile.prod /workspace
docker build --dry-run -f /workspace/docker/frontend/Dockerfile.prod /workspace/frontend
```

### Build local para testing:
```bash
# Backend
cd /workspace
docker build -f docker/backend/Dockerfile.prod -t dealaai-backend:prod .

# Frontend
cd /workspace/frontend
docker build -f ../docker/frontend/Dockerfile.prod -t dealaai-frontend:prod .

# Database
docker build -f docker/database/Dockerfile -t dealaai-db:prod docker/database
```

### Verificar imagen:
```bash
docker inspect dealaai-backend:prod
docker inspect dealaai-frontend:prod
docker inspect dealaai-db:prod
```

---

## 📝 Variables de Entorno en Dockerfiles

### Backend:
```dockerfile
ARG DJANGO_SETTINGS_MODULE=dealaai.settings.production
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
```

### Frontend:
```dockerfile
ARG NODE_ENV=production
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_WS_URL
ARG NEXT_PUBLIC_DOMAIN

ENV NODE_ENV=${NODE_ENV}
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV NEXT_PUBLIC_WS_URL=${NEXT_PUBLIC_WS_URL}
ENV NEXT_PUBLIC_DOMAIN=${NEXT_PUBLIC_DOMAIN}
ENV NEXT_TELEMETRY_DISABLED=1
```

---

## 🐳 Docker Compose para Producción

**Ubicación:** `/workspace/docker-compose.production.yml`

Usa automáticamente los Dockerfile.prod:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/backend/Dockerfile.prod    # ← Usa .prod
    environment:
      - DJANGO_SETTINGS_MODULE=dealaai.settings.production
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/frontend/Dockerfile.prod  # ← Usa .prod
      args:
        NEXT_PUBLIC_API_URL: https://mcp.jorgemg.es/api
    ports:
      - "3000:3000"

  db:
    build:
      context: docker/database
      dockerfile: Dockerfile
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

---

## 🚀 Comando para Deploy en EasyPanel

```bash
# Clonar repositorio
git clone <repo> /opt/dealaai

# Copiar .env.production
cp .env.production.template .env.production
# Editar con valores reales

# Build y start
docker-compose -f docker-compose.production.yml build
docker-compose -f docker-compose.production.yml up -d

# Verificar
docker-compose -f docker-compose.production.yml ps
docker-compose -f docker-compose.production.yml logs -f
```

---

## 📚 Referencias

| Archivo | Propósito | Ubicación |
|---------|----------|----------|
| **Dockerfile.prod (Backend)** | Build Django producción | `/workspace/docker/backend/Dockerfile.prod` |
| **Dockerfile.prod (Frontend)** | Build Next.js producción | `/workspace/docker/frontend/Dockerfile.prod` |
| **Dockerfile (DB)** | PostgreSQL + pgvector | `/workspace/docker/database/Dockerfile` |
| **nginx.conf** | Config Nginx producción | `/workspace/docker/nginx/nginx.conf` |
| **docker-compose.prod.yml** | Orquestación servicios | `/workspace/docker-compose.production.yml` |

---

## ✅ Checklist: Dockerfiles Listos

- ✅ Backend Dockerfile.prod validado
- ✅ Frontend Dockerfile.prod validado
- ✅ Database Dockerfile validado
- ✅ Multi-stage builds optimizados
- ✅ Health checks incluidos
- ✅ Usuarios no-root configurados
- ✅ Variables de entorno documentadas
- ✅ Docker-compose.production.yml listo
- ✅ Nginx configurado para proxy
- ✅ Listo para EasyPanel

---

## 🔗 Links rápidos

- **Dockerfile Backend**: `/workspace/docker/backend/Dockerfile.prod`
- **Dockerfile Frontend**: `/workspace/docker/frontend/Dockerfile.prod`
- **Dockerfile Database**: `/workspace/docker/database/Dockerfile`
- **Docker Compose**: `/workspace/docker-compose.production.yml`
- **Nginx Config**: `/workspace/docker/nginx/nginx.conf`

---

**Última actualización:** 26 de Octubre, 2025  
**Status:** ✅ DOCKERFILES LISTOS PARA PRODUCCIÓN
