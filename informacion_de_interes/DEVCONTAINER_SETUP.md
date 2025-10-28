# 🐳 Configuración del DevContainer

## Estado Actual

✅ **DevContainer Completamente Funcional**

Se han corregido todos los problemas y el devcontainer está funcionando perfectamente:

- ✅ Entorno virtual de Python 3.12 con herramientas de desarrollo
- ✅ Node.js 18 LTS con herramientas globales
- ✅ PostgreSQL 15 con pgvector (puerto 5432 expuesto)
- ✅ Redis 7 para cache y Celery (puerto 6379 expuesto)
- ✅ Archivos del proyecto correctamente mapeados en `/workspace`
- ✅ Todas las extensiones de VS Code configuradas

## Problemas Corregidos

### 1. Configuración de VS Code

- ✅ Eliminadas configuraciones obsoletas de Python (`python.linting.*`, `python.formatting.provider`)
- ✅ Actualizadas a las nuevas APIs de extensiones
- ✅ Corregidos valores booleanos en `codeActionsOnSave` (ahora usan `"explicit"`)
- ✅ Eliminada sección duplicada `[python]`

### 2. Docker Compose

- ✅ Eliminado `version: "3.8"` (obsoleto en Docker Compose v2)
- ✅ Simplificada configuración de red con `network_mode: service:db`
- ✅ Variables de entorno configuradas en `devcontainer.json`

### 3. Archivos de Entorno

- ✅ Creados `backend/.env` y `frontend/.env.local`
- ✅ Creados archivos `.env.example` para referencia
- ✅ Configuradas todas las variables necesarias para desarrollo

### 5. Mapeo de Volúmenes Corregido

- ✅ **Volumen corregido**: `..:/workspace:cached` (antes era `../..:/workspace:cached`)
- ✅ **Archivos del proyecto visibles** en `/workspace`
- ✅ **Workspace folder** configurado correctamente en `devcontainer.json`

## 🚀 Cómo Usar el DevContainer

### Opción 1: Desde VS Code (Recomendado)

1. **Abrir el proyecto en VS Code**

   ```bash
   code c:\___apps___\all4devs\AI4Devs-finalproject
   ```

2. **Abrir en DevContainer**
   - Presiona `F1` o `Ctrl+Shift+P`
   - Busca: `Dev Containers: Reopen in Container`
   - Selecciona la opción
3. **Esperar la Construcción**
   - Primera vez: 5-10 minutos (descarga imágenes e instala dependencias)
   - Siguientes veces: 1-2 minutos

### Opción 2: Desde la Línea de Comandos

```powershell
# Navegar al directorio del devcontainer
cd c:\___apps___\all4devs\AI4Devs-finalproject\.devcontainer

# Construir y levantar los contenedores
docker compose -f docker-compose.yml up -d --build

# Verificar que estén corriendo
docker compose -f docker-compose.yml ps
```

## 📦 Servicios Incluidos

El devcontainer incluye 3 servicios:

### 1. **app** (Contenedor Principal)

- Python 3.12 + Node.js 18
- Herramientas de desarrollo (black, isort, flake8, pytest)
- Cliente PostgreSQL
- Git, GitHub CLI
- Docker-in-Docker

### 2. **db** (PostgreSQL 15 + pgvector)

- Base de datos principal
- Extensión pgvector para embeddings
- Puerto: 5432 (accesible desde localhost)

### 3. **redis** (Redis 7 Alpine)

- Cache y broker para Celery
- Puerto: 6379 (accesible desde localhost)

## 🔧 Configuración Post-Inicialización

Una vez dentro del devcontainer:

### 1. Crear el proyecto Django

```bash
cd /workspace/backend
django-admin startproject dealaai .
```

### 2. Crear el proyecto Next.js

```bash
cd /workspace/frontend
npx create-next-app@latest . --typescript --tailwind --app --src-dir
```

### 3. Configurar la base de datos

```bash
cd /workspace/backend
python manage.py migrate
python manage.py createsuperuser
```

## 🌐 Acceso desde Fuera del DevContainer

Todos los servicios están configurados para ser accesibles desde tu máquina local:

### Base de Datos PostgreSQL

```bash
# Conectar desde tu máquina local
psql postgresql://postgres:postgres@localhost:5432/dealaai_dev

# O usando herramientas GUI como DBeaver, pgAdmin, etc.
Host: localhost
Port: 5432
Database: dealaai_dev
Username: postgres
Password: postgres
```

### Redis Cache

```bash
# Conectar desde tu máquina local
redis-cli -h localhost -p 6379

# Verificar conexión
redis-cli -h localhost -p 6379 ping
```

### API Backend (Django)

```bash
# Una vez que el backend esté corriendo
curl http://localhost:8000/api/health/
# O abrir en navegador: http://localhost:8000
```

### Frontend (Next.js)

```bash
# Una vez que el frontend esté corriendo
# Abrir en navegador: http://localhost:3000
```

## 🚀 Inicialización de Proyectos

Para inicializar automáticamente los proyectos Django y Next.js con configuración completa:

```bash
# Desde dentro del devcontainer
./scripts/init-projects.sh
```

Este script:

- ✅ Crea proyecto Django en `backend/`
- ✅ Crea proyecto Next.js en `frontend/`
- ✅ Actualiza `docker-compose.yml` con servicios expuestos
- ✅ Reinicia todos los servicios con puertos accesibles

## 📝 Variables de Entorno

### Backend (`backend/.env`)

```bash
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-this-in-production
DATABASE_URL=postgresql://postgres:postgres@db:5432/dealaai_dev
REDIS_URL=redis://redis:6379/0
OPENAI_API_KEY=your-openai-api-key-here
```

### Frontend (`frontend/.env.local`)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NODE_ENV=development
```

## 🐛 Solución de Problemas

### El contenedor no se construye

1. Verificar que Docker Desktop esté corriendo
2. Limpiar contenedores previos:
   ```powershell
   docker compose -f .devcontainer\docker-compose.yml down -v
   docker system prune -a
   ```
3. Reconstruir desde cero:
   ```powershell
   docker compose -f .devcontainer\docker-compose.yml up -d --build --force-recreate
   ```

### No puedo conectarme a la base de datos

1. Verificar que el servicio `db` esté corriendo:

   ```bash
   docker compose -f .devcontainer/docker-compose.yml ps
   ```

2. Probar conexión manual:
   ```bash
   psql postgresql://postgres:postgres@localhost:5432/dealaai_dev
   ```

### Las extensiones de VS Code no funcionan

1. Recargar la ventana: `F1` → `Developer: Reload Window`
2. Reinstalar extensiones: Eliminar `.vscode/extensions` y reabrir

### Python no encuentra los módulos

1. Verificar que PYTHONPATH esté configurado:

   ```bash
   echo $PYTHONPATH  # Debe ser /workspace/backend
   ```

2. Reinstalar dependencias:
   ```bash
   cd /workspace/backend
   pip install -r requirements.txt
   ```

## � Próximos Pasos

1. ✅ DevContainer configurado y funcionando
2. ✅ Servicios accesibles desde fuera del contenedor
3. ⏳ **Inicializar proyectos**: Ejecutar `./scripts/init-projects.sh`
4. ⏳ Configurar la base de datos: `python manage.py migrate`
5. ⏳ Crear superusuario: `python manage.py createsuperuser`
6. ⏳ Configurar variables de entorno (OPENAI_API_KEY, etc.)
7. ⏳ Implementar modelos de base de datos
8. ⏳ Implementar APIs REST
9. ⏳ Implementar sistema RAG con pgvector
10. ⏳ Crear interfaz de usuario

## 🆘 Soporte

Si encuentras problemas:

1. Verifica el log del devcontainer: `F1` → `Dev Containers: Show Container Log`
2. Revisa los logs de Docker: `docker compose -f .devcontainer/docker-compose.yml logs`
3. Consulta la documentación: `DEVELOPMENT.md`, `COMMANDS.md`, `QUICKSTART.md`

---

**Última actualización**: 14 de octubre de 2025
