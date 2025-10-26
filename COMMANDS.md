# Comandos Útiles - DealaAI

## 🚀 Inicio Rápido

```bash
# Opción 1: DevContainer (VS Code)
# 1. Abrir en VS Code
# 2. F1 -> "Dev Containers: Reopen in Container"

# Opción 2: Docker Compose
./scripts/setup.sh
docker-compose up -d
```

## 🐳 Docker Compose

```bash
# Iniciar servicios
docker-compose up -d

# Iniciar servicios con rebuild
docker-compose up -d --build

# Ver logs
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reiniciar un servicio específico
docker-compose restart backend

# Ver estado de servicios
docker-compose ps

# Ejecutar comando en un contenedor
docker-compose exec backend bash
docker-compose exec db psql -U postgres
```

## 🐍 Backend (Django)

```bash
# Entrar al contenedor
docker-compose exec backend bash

# O ejecutar comandos directamente
docker-compose exec backend python manage.py [comando]

# Migraciones
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py showmigrations

# Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Shell de Django
docker-compose exec backend python manage.py shell
docker-compose exec backend python manage.py shell_plus  # Si tienes django-extensions

# Ejecutar tests
docker-compose exec backend pytest
docker-compose exec backend pytest --cov
docker-compose exec backend pytest apps/inventory/tests/

# Crear nueva app
docker-compose exec backend python manage.py startapp nombre_app

# Cargar fixtures
docker-compose exec backend python manage.py loaddata fixtures/sample_data.json

# Crear fixtures
docker-compose exec backend python manage.py dumpdata --indent 2 > fixtures/backup.json

# Linting y formateo
docker-compose exec backend black .
docker-compose exec backend isort .
docker-compose exec backend flake8 .

# Colectar archivos estáticos
docker-compose exec backend python manage.py collectstatic --noinput

# Crear usuario de prueba
docker-compose exec backend python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
```

## ⚛️ Frontend (Next.js)

```bash
# Desarrollo local (fuera de Docker)
cd frontend
npm install
npm run dev
npm run build
npm run start

# Dentro de Docker
docker-compose exec frontend npm run dev
docker-compose exec frontend npm run build

# Linting y formateo
cd frontend
npm run lint
npm run lint:fix
npm run format

# Tests
npm test
npm test -- --coverage
npm run test:watch

# E2E tests
npm run test:e2e
npm run test:e2e:ui

# Análisis de bundle
npm run analyze
```

## 🗄️ Base de Datos (PostgreSQL)

```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U postgres -d dealaai_dev

# Comandos SQL útiles
\l                  # Listar bases de datos
\c dealaai_dev      # Conectar a base de datos
\dt                 # Listar tablas
\d nombre_tabla     # Describir tabla
\du                 # Listar usuarios
\q                  # Salir

# Backup
docker-compose exec db pg_dump -U postgres dealaai_dev > backup.sql

# Restore
docker-compose exec -T db psql -U postgres dealaai_dev < backup.sql

# Ejecutar script SQL
docker-compose exec -T db psql -U postgres dealaai_dev < database/migrations/001_create_tables.sql

# Verificar extensión pgvector
docker-compose exec db psql -U postgres -d dealaai_dev -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

## 🔴 Redis

```bash
# Conectar a Redis
docker-compose exec redis redis-cli

# Comandos Redis útiles
KEYS *              # Ver todas las keys
GET key_name        # Obtener valor
SET key_name value  # Establecer valor
DEL key_name        # Eliminar key
FLUSHALL            # Limpiar todo
INFO                # Información del servidor
MONITOR             # Monitorear comandos en tiempo real
```

## 🔄 Celery

```bash
# Ver workers activos
docker-compose exec celery_worker celery -A dealaai inspect active

# Ver tareas programadas
docker-compose exec celery_beat celery -A dealaai inspect scheduled

# Limpiar cola
docker-compose exec celery_worker celery -A dealaai purge

# Estadísticas
docker-compose exec celery_worker celery -A dealaai inspect stats
```

## 🔍 Debugging

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Ver últimas 100 líneas
docker-compose logs --tail=100 backend

# Inspeccionar contenedor
docker inspect dealaai_backend

# Ver procesos en contenedor
docker-compose exec backend ps aux

# Ver uso de recursos
docker stats

# Entrar en modo debug (detener servicio y correr manualmente)
docker-compose stop backend
docker-compose run --rm --service-ports backend python manage.py runserver 0.0.0.0:8000
```

## 🧹 Limpieza

```bash
# Limpiar contenedores detenidos
docker container prune

# Limpiar imágenes no usadas
docker image prune

# Limpiar volúmenes no usados
docker volume prune

# Limpiar todo
docker system prune -a

# Limpiar específicamente este proyecto
docker-compose down -v
docker volume rm $(docker volume ls -q | grep ai4devs-finalproject)

# Rebuild completo
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 📊 Monitoreo

```bash
# Estado de servicios
docker-compose ps

# Uso de recursos
docker stats

# Logs de errores
docker-compose logs --tail=50 | grep -i error

# Health checks
docker-compose exec backend curl http://localhost:8000/api/health/
docker-compose exec frontend wget --quiet --tries=1 --spider http://localhost:3000

# Ver configuración
docker-compose config
```

## 🔐 Seguridad

```bash
# Actualizar dependencias Python
docker-compose exec backend pip list --outdated
docker-compose exec backend pip install --upgrade -r requirements/development.txt

# Actualizar dependencias Node
cd frontend
npm outdated
npm update

# Escanear vulnerabilidades
docker-compose exec backend safety check
cd frontend && npm audit

# Fix automático
cd frontend && npm audit fix
```

## 📦 Gestión de Dependencias

```bash
# Backend - Agregar nueva dependencia
docker-compose exec backend pip install nombre_paquete
# Luego actualizar requirements.txt
docker-compose exec backend pip freeze > requirements/base.txt

# Frontend - Agregar nueva dependencia
cd frontend
npm install nombre_paquete
npm install -D nombre_paquete  # Dev dependency
```

## 🚀 Despliegue

```bash
# Build para producción
docker-compose -f docker-compose.prod.yml build

# Ejecutar en producción
docker-compose -f docker-compose.prod.yml up -d

# Ver logs de producción
docker-compose -f docker-compose.prod.yml logs -f
```

## 💡 Tips

```bash
# Alias útiles para .bashrc o .zshrc
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'
alias dcl='docker-compose logs -f'
alias dcb='docker-compose exec backend'
alias dcf='docker-compose exec frontend'
alias dce='docker-compose exec'
alias dcps='docker-compose ps'

# Shortcuts de scripts
./scripts/dev.sh start
./scripts/dev.sh stop
./scripts/dev.sh logs
./scripts/dev.sh migrate
./scripts/dev.sh shell
```

## 🆘 Troubleshooting

```bash
# Puerto ocupado
sudo lsof -i :3000  # Ver qué usa el puerto
sudo kill -9 PID    # Matar proceso

# Permisos de Docker
sudo usermod -aG docker $USER
newgrp docker

# Problemas de caché
docker-compose build --no-cache
rm -rf frontend/.next
rm -rf backend/__pycache__

# Resetear base de datos
docker-compose down -v
docker-compose up -d db
# Esperar y ejecutar migraciones
docker-compose exec backend python manage.py migrate

# Ver variables de entorno
docker-compose exec backend env
docker-compose exec frontend env
```
