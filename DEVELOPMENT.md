# DealaAI - Guía de Desarrollo con DevContainer

## 🚀 Inicio Rápido

### Opción 1: Usando VS Code DevContainer (Recomendado)

1. **Abrir el proyecto en VS Code**
2. **Instalar la extensión "Dev Containers"** (ms-vscode-remote.remote-containers)
3. Presionar `F1` y seleccionar `Dev Containers: Reopen in Container`
4. Esperar a que el contenedor se construya e inicialice
5. ¡Listo! El entorno está configurado automáticamente

**Servicios disponibles en DevContainer:**

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin: http://localhost:8000/admin
- Nginx (desarrollo): http://localhost
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Opción 2: Usando Docker Compose

```bash
# 1. Clonar el repositorio
git clone https://github.com/jorgemartin/dealaai-concesionario.git
cd dealaai-concesionario

# 2. Ejecutar script de setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Iniciar servicios con Nginx
docker-compose up -d

# 4. Acceder a los servicios
# Nginx (proxy): http://localhost
# Frontend directo: http://localhost:3000
# Backend directo: http://localhost:8000
# Admin: http://localhost/admin
```

### Opción 3: Producción con EasyPanel

```bash
# 1. Configurar variables de entorno en EasyPanel
# Usar como base el archivo .env.production

# 2. Desplegar con docker-compose.production.yml
docker-compose -f docker-compose.production.yml up -d

# 3. Acceder a los servicios en producción
# Aplicación: https://mcp.jorgemg.es
# API: https://mcp.jorgemg.es/api/v1
# Admin: https://mcp.jorgemg.es/admin
# pgAdmin: https://mcp.jorgemg.es/pgadmin
# Supabase Studio: https://mcp.jorgemg.es/studio
```

## 📦 Estructura del Proyecto

```
AI4Devs-finalproject/
├── .devcontainer/              # Configuración de DevContainer
│   ├── devcontainer.json       # Configuración principal
│   ├── docker-compose.yml      # Servicios del devcontainer
│   ├── Dockerfile              # Imagen del contenedor de desarrollo
│   └── post-create.sh          # Script de inicialización
│
├── backend/                    # Aplicación Django
│   ├── apps/                   # Aplicaciones Django por módulo
│   │   ├── authentication/     # Sistema de autenticación
│   │   ├── inventory/          # Gestión de vehículos
│   │   ├── leads/              # CRM de leads
│   │   ├── sales/              # Gestión de ventas
│   │   ├── ai_chat/            # Sistema de chat IA
│   │   └── analytics/          # Reportes y analytics
│   ├── core/                   # Utilidades compartidas
│   ├── dealaai/                # Configuración del proyecto
│   │   └── settings/           # Settings por ambiente
│   ├── fixtures/               # Datos de prueba
│   ├── requirements/           # Dependencias Python
│   │   ├── base.txt
│   │   ├── development.txt
│   │   └── production.txt
│   ├── manage.py
│   └── .env                    # Variables de entorno
│
├── frontend/                   # Aplicación Next.js
│   ├── app/                    # App Router (Next.js 13+)
│   │   ├── (dashboard)/        # Rutas del dashboard
│   │   │   ├── inventory/
│   │   │   ├── leads/
│   │   │   ├── sales/
│   │   │   └── chat/
│   │   └── api/                # API Routes
│   ├── components/             # Componentes React
│   │   ├── ui/                 # Componentes base
│   │   ├── forms/              # Formularios
│   │   ├── charts/             # Gráficos
│   │   └── chat/               # Chat UI
│   ├── lib/                    # Utilidades
│   ├── hooks/                  # Custom hooks
│   ├── store/                  # Estado global (Zustand)
│   ├── types/                  # TypeScript types
│   ├── public/                 # Assets estáticos
│   ├── package.json
│   └── .env.local              # Variables de entorno
│
├── database/                   # Base de datos
│   ├── init/                   # Scripts de inicialización
│   ├── migrations/             # Migraciones SQL
│   ├── fixtures/               # Datos de ejemplo
│   └── backups/                # Backups
│
├── docker/                     # Configuración Docker
│   ├── backend/
│   │   └── Dockerfile
│   ├── frontend/
│   │   └── Dockerfile
│   ├── database/
│   │   └── Dockerfile
│   └── nginx/
│       └── nginx.conf
│
├── scripts/                    # Scripts de automatización
│   ├── setup.sh                # Setup inicial
│   ├── dev.sh                  # Comandos de desarrollo
│   └── backup.sh               # Backup de datos
│
├── docs/                       # Documentación
│   ├── api/                    # Documentación API
│   ├── architecture/           # Diagramas arquitectura
│   └── deployment/             # Guías de despliegue
│
├── docker-compose.yml          # Orquestación de servicios
├── .editorconfig               # Configuración del editor
├── .gitignore                  # Archivos ignorados por Git
└── README.md                   # Este archivo
```

## 🛠️ Tecnologías

### Backend

- **Django 4.2 LTS** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL 15** - Base de datos relacional
- **pgvector** - Extensión para vectores de embeddings
- **Celery** - Tareas asíncronas
- **Redis** - Cache y message broker
- **OpenAI API** - Integración con GPT-4
- **LangChain** - Framework para RAG

### Frontend

- **Next.js 13+** - Framework React con App Router
- **TypeScript** - Tipado estático
- **TailwindCSS** - Framework CSS
- **Radix UI** - Componentes accesibles
- **Zustand** - Gestión de estado
- **React Query** - Data fetching
- **Chart.js** - Visualización de datos

### DevOps y Deployment

- **Docker & Docker Compose** - Containerización
- **VS Code DevContainers** - Entorno de desarrollo
- **GitHub Actions** - CI/CD
- **Nginx** - Reverse proxy y load balancer
- **PostgreSQL + pgvector** - Base de datos con vectores
- **Redis** - Cache y message broker
- **EasyPanel** - Plataforma de deployment
- **Let's Encrypt** - Certificados SSL automáticos

## 💻 Comandos de Desarrollo

### Usando DevContainer

Una vez dentro del devcontainer, puedes usar estos comandos:

```bash
# Backend (Django)
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell

# Frontend (Next.js)
cd frontend
npm run dev
npm run build
npm run lint
npm test

# Base de datos
psql -h localhost -U postgres -d dealaai_dev
```

### Usando Docker Compose

```bash
# Desarrollo con Nginx proxy
docker-compose up -d
# Acceso: http://localhost (nginx) o http://localhost:3000 (directo)

# Producción (EasyPanel)
docker-compose -f docker-compose.production.yml up -d
# Acceso: https://mcp.jorgemg.es

# Ver logs
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx

# Ejecutar comandos en contenedores
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec db psql -U postgres -d dealaai_dev

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache

# Limpiar todo
docker-compose down -v
docker system prune -f
```

### Scripts de ayuda

```bash
# Setup inicial
./scripts/setup.sh

# Comandos de desarrollo
./scripts/dev.sh start          # Iniciar servicios
./scripts/dev.sh stop           # Detener servicios
./scripts/dev.sh logs           # Ver logs
./scripts/dev.sh migrate        # Ejecutar migraciones
./scripts/dev.sh shell          # Django shell
./scripts/dev.sh test-backend   # Tests backend
./scripts/dev.sh test-frontend  # Tests frontend
```

## 🔧 Configuración

### Variables de Entorno

#### Backend (`backend/.env`)

```env
# Django
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/dealaai_dev

# Redis
REDIS_URL=redis://redis:6379/0

# OpenAI
OPENAI_API_KEY=sk-tu-api-key-aqui

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

#### Frontend (`frontend/.env.local`)

```env
# API
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Environment
NEXT_PUBLIC_ENV=development
```

## 🧪 Testing

### Backend (Python/Django)

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=apps --cov-report=html

# Tests específicos
pytest apps/inventory/tests/
pytest -k test_vehicle_creation
```

### Frontend (JavaScript/TypeScript)

```bash
# Ejecutar tests
npm test

# Con cobertura
npm test -- --coverage

# Watch mode
npm test -- --watch

# E2E tests
npm run test:e2e
```

## 📚 Documentación Adicional

- [Arquitectura del Sistema](docs/architecture/README.md)
- [API Documentation](docs/api/README.md)
- [Guía de Despliegue](docs/deployment/README.md)
- [Modelo de Datos](database_model.md)

## 🔐 Seguridad

- Nunca commitear archivos `.env` con credenciales reales
- Usar variables de entorno para secretos
- Mantener dependencias actualizadas
- Seguir las mejores prácticas de Django y Next.js

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto es privado y confidencial.

## 👥 Autores

- **Jorge Martín García** - _Desarrollo inicial_ - [GitHub](https://github.com/jorgemartin)

## 🆘 Soporte

Si tienes problemas:

1. Verifica que Docker esté corriendo
2. Revisa los logs: `docker-compose logs`
3. Limpia y reconstruye: `docker-compose down -v && docker-compose up --build`
4. Consulta la documentación en `docs/`

## 📊 Estado del Proyecto

- ✅ Configuración inicial
- ✅ DevContainer setup
- ⏳ Backend en desarrollo
- ⏳ Frontend en desarrollo
- ⏳ Sistema de IA en desarrollo
- ⏳ Despliegue en producción

---

**Fecha de última actualización:** Octubre 2025
