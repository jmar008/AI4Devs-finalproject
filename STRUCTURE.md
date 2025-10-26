# 📁 Estructura del Proyecto DealaAI

## ✅ Archivos Creados para el DevContainer

### 🐳 Configuración de DevContainer

```
.devcontainer/
├── devcontainer.json         ✅ Configuración principal del devcontainer
├── docker-compose.yml        ✅ Servicios para desarrollo
├── Dockerfile                ✅ Imagen personalizada de desarrollo
└── post-create.sh            ✅ Script de inicialización automática
```

**Características del DevContainer:**

- ✅ Python 3.11 + Node.js 18 preinstalados
- ✅ Extensiones de VS Code configuradas automáticamente
- ✅ PostgreSQL con pgvector
- ✅ Redis para cache y Celery
- ✅ Auto-instalación de dependencias
- ✅ Configuración de Git y herramientas

### 🐳 Configuración Docker

```
docker/
├── backend/
│   └── Dockerfile            ✅ Imagen del backend Django
├── frontend/
│   └── Dockerfile            ✅ Imagen del frontend Next.js
└── database/
    └── Dockerfile            ✅ PostgreSQL con pgvector

docker-compose.yml            ✅ Orquestación completa de servicios
```

**Servicios configurados:**

- ✅ Backend (Django + DRF) - Puerto 8000
- ✅ Frontend (Next.js) - Puerto 3000
- ✅ PostgreSQL con pgvector - Puerto 5432
- ✅ Redis - Puerto 6379
- ✅ Celery Worker (tareas asíncronas)
- ✅ Celery Beat (tareas programadas)

### 📊 Base de Datos

```
database/
├── init/
│   └── 01-init.sql           ✅ Script de inicialización
├── migrations/               ✅ Directorio para migraciones
├── fixtures/                 ✅ Datos de ejemplo
└── backups/                  ✅ Directorio para backups
```

### 🔧 Scripts de Automatización

```
scripts/
├── setup.sh                  ✅ Setup inicial del proyecto
└── dev.sh                    ✅ Comandos de desarrollo rápidos
```

**Comandos disponibles:**

- `./scripts/setup.sh` - Setup inicial completo
- `./scripts/dev.sh start` - Iniciar servicios
- `./scripts/dev.sh stop` - Detener servicios
- `./scripts/dev.sh logs` - Ver logs
- `./scripts/dev.sh migrate` - Ejecutar migraciones
- `./scripts/dev.sh shell` - Django shell
- `./scripts/dev.sh test-backend` - Tests backend
- `./scripts/dev.sh test-frontend` - Tests frontend

### ⚙️ Configuración VS Code

```
.vscode/
├── settings.json             ✅ Configuración del workspace
├── tasks.json                ✅ Tareas predefinidas
├── launch.json               ✅ Configuración de debugging
└── extensions.json           ✅ Extensiones recomendadas
```

**Tareas disponibles (F1 → Tasks: Run Task):**

- 🚀 Iniciar Backend (Django)
- ⚛️ Iniciar Frontend (Next.js)
- 🐳 Docker: Iniciar todos los servicios
- 🛑 Docker: Detener servicios
- 📊 Docker: Ver logs
- 🔄 Django: Ejecutar migraciones
- 📝 Django: Crear migraciones
- 👤 Django: Crear superusuario
- 🧪 Backend: Ejecutar tests
- 🧪 Frontend: Ejecutar tests
- 🎨 Formatear código
- 🗄️ PostgreSQL: Conectar
- 🧹 Limpiar contenedores

### 📝 Archivos de Configuración

```
├── .editorconfig             ✅ Configuración del editor
├── .gitignore                ✅ Archivos ignorados por Git
├── Makefile                  ✅ Comandos Make simplificados
├── DEVELOPMENT.md            ✅ Guía de desarrollo completa
└── COMMANDS.md               ✅ Referencia rápida de comandos
```

**Makefile - Comandos disponibles:**

- `make help` - Mostrar ayuda
- `make setup` - Setup inicial
- `make start` - Iniciar servicios
- `make stop` - Detener servicios
- `make logs` - Ver logs
- `make test` - Ejecutar tests
- `make migrate` - Ejecutar migraciones
- `make shell-backend` - Django shell
- `make shell-db` - PostgreSQL shell
- `make clean` - Limpiar todo
- `make rebuild` - Rebuild completo

### 📂 Estructura de Carpetas

```
AI4Devs-finalproject/
├── .devcontainer/            ✅ Configuración DevContainer
├── .vscode/                  ✅ Configuración VS Code
├── backend/                  📦 Django (por crear)
│   ├── apps/
│   ├── core/
│   ├── dealaai/
│   ├── fixtures/
│   └── requirements/
├── frontend/                 📦 Next.js (por crear)
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── hooks/
│   ├── store/
│   └── types/
├── database/                 ✅ Scripts de BD
├── docker/                   ✅ Dockerfiles
├── scripts/                  ✅ Scripts de automatización
├── docs/                     📝 Documentación (por crear)
├── docker-compose.yml        ✅ Orquestación
├── Makefile                  ✅ Comandos Make
├── .editorconfig             ✅ Configuración editor
├── .gitignore                ✅ Git ignore
├── DEVELOPMENT.md            ✅ Guía de desarrollo
├── COMMANDS.md               ✅ Comandos útiles
├── readme.md                 ✅ README principal
├── database_model.md         ✅ Modelo de datos
└── prompts.md                ✅ Prompts utilizados
```

## 🚀 Próximos Pasos

### 1. Iniciar el DevContainer

**Opción A: VS Code DevContainer (Recomendado)**

```bash
# 1. Abrir VS Code
# 2. F1 → "Dev Containers: Reopen in Container"
# 3. Esperar a que se construya e inicialice
# 4. ¡Listo para desarrollar!
```

**Opción B: Docker Compose**

```bash
# 1. Dar permisos a scripts
chmod +x scripts/*.sh

# 2. Ejecutar setup
./scripts/setup.sh

# 3. Iniciar servicios
docker-compose up -d

# 4. Ver logs
docker-compose logs -f
```

### 2. Configurar Variables de Entorno

Edita los archivos `.env`:

**backend/.env**

```env
OPENAI_API_KEY=sk-tu-api-key-aqui
SUPABASE_URL=tu-supabase-url (opcional)
SUPABASE_KEY=tu-supabase-key (opcional)
```

**frontend/.env.local**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Crear Estructura del Backend

```bash
# Dentro del devcontainer o usando docker-compose
cd backend

# Crear proyecto Django
django-admin startproject dealaai .

# Crear apps
python manage.py startapp authentication apps/authentication
python manage.py startapp inventory apps/inventory
python manage.py startapp leads apps/leads
python manage.py startapp sales apps/sales
python manage.py startapp ai_chat apps/ai_chat
python manage.py startapp analytics apps/analytics

# Crear requirements
mkdir -p requirements
touch requirements/base.txt
touch requirements/development.txt
touch requirements/production.txt
```

### 4. Crear Estructura del Frontend

```bash
cd frontend

# Inicializar proyecto Next.js
npx create-next-app@latest . --typescript --tailwind --app --import-alias "@/*"

# Instalar dependencias adicionales
npm install @radix-ui/react-* zustand @tanstack/react-query
npm install -D prettier eslint-config-prettier
```

### 5. Configurar Base de Datos

```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Conectar a PostgreSQL
docker-compose exec db psql -U postgres -d dealaai_dev

# Verificar extensión pgvector
\dx

# Salir
\q

# Ejecutar migraciones (cuando existan)
docker-compose exec backend python manage.py migrate
```

## 📚 Documentación

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Guía completa de desarrollo
- **[COMMANDS.md](COMMANDS.md)** - Referencia rápida de comandos
- **[database_model.md](database_model.md)** - Modelo de datos
- **[prompts.md](prompts.md)** - Prompts utilizados

## ✅ Checklist de Verificación

### Infraestructura

- ✅ DevContainer configurado
- ✅ Docker Compose configurado
- ✅ PostgreSQL con pgvector
- ✅ Redis configurado
- ✅ Scripts de automatización
- ✅ VS Code tasks y debugging

### Siguiente Fase

- ⏳ Crear estructura backend (Django)
- ⏳ Crear estructura frontend (Next.js)
- ⏳ Implementar modelos de datos
- ⏳ Configurar APIs REST
- ⏳ Implementar sistema de IA (RAG)
- ⏳ Tests unitarios e integración
- ⏳ Despliegue en producción

## 🎯 Características del Entorno de Desarrollo

### ✨ DevContainer Features

- ✅ Entorno reproducible y consistente
- ✅ Todas las dependencias preinstaladas
- ✅ Extensiones de VS Code automáticas
- ✅ Git configurado
- ✅ Formateo automático de código
- ✅ Linting configurado
- ✅ Debugging ready

### 🔧 Herramientas Instaladas

- ✅ Python 3.11 + pip
- ✅ Node.js 18 + npm/pnpm/yarn
- ✅ PostgreSQL client
- ✅ Redis CLI
- ✅ Git + GitHub CLI
- ✅ Docker-in-Docker
- ✅ Black, isort, flake8 (Python)
- ✅ ESLint, Prettier (JavaScript/TypeScript)

### 📦 Servicios Disponibles

- ✅ Backend API (Django) - http://localhost:8000
- ✅ Frontend (Next.js) - http://localhost:3000
- ✅ Admin Panel - http://localhost:8000/admin
- ✅ PostgreSQL - localhost:5432
- ✅ Redis - localhost:6379

## 💡 Tips y Mejores Prácticas

### Workflow Recomendado

1. **Abrir en DevContainer**

   - Toda la configuración automática
   - No necesitas instalar nada en tu máquina

2. **Usar Tasks de VS Code**

   - F1 → "Tasks: Run Task"
   - Comandos predefinidos listos para usar

3. **Usar Makefile**

   - `make help` para ver comandos disponibles
   - Simplifica operaciones comunes

4. **Debugging**

   - F5 para iniciar debugging
   - Configuraciones pre-establecidas

5. **Git Workflow**
   - GitLens instalado
   - GitHub PR integration
   - Commits desde VS Code

## 🆘 Troubleshooting

### El devcontainer no inicia

```bash
# Rebuild completo
docker-compose down -v
docker system prune -f
# Reabrir en devcontainer
```

### Puertos ocupados

```bash
# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess
Stop-Process -Id <PID>

# Linux/Mac
lsof -i :3000
kill -9 <PID>
```

### Base de datos no conecta

```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Reiniciar servicio
docker-compose restart db

# Ver logs
docker-compose logs db
```

## 📞 Contacto y Soporte

- **Autor:** Jorge Martín García
- **GitHub:** [jorgemartin](https://github.com/jorgemartin)
- **Email:** jorge@example.com

---

**¡Listo para empezar a desarrollar! 🚀**

Para comenzar, abre el proyecto en VS Code y selecciona "Reopen in Container" cuando se te pregunte.
