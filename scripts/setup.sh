#!/bin/bash

# Script de setup inicial del proyecto
set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Funciones de log
log() { echo -e "${GREEN}[Setup]${NC} $1"; }
info() { echo -e "${BLUE}[Info]${NC} $1"; }
warning() { echo -e "${YELLOW}[Warning]${NC} $1"; }
error() { echo -e "${RED}[Error]${NC} $1"; }

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║       DealaAI - Setup del Proyecto de Desarrollo        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    error "Este script debe ejecutarse desde la raíz del proyecto"
    exit 1
fi

# 1. Verificar dependencias
log "Verificando dependencias..."

command -v docker >/dev/null 2>&1 || { error "Docker no está instalado"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || command -v docker compose >/dev/null 2>&1 || { error "Docker Compose no está instalado"; exit 1; }

info "✓ Docker instalado: $(docker --version)"
info "✓ Docker Compose instalado"

# 2. Crear archivos .env si no existen
log "Configurando archivos de entorno..."

if [ ! -f "backend/.env" ]; then
    warning "Creando backend/.env desde template..."
    cat > backend/.env << 'EOF'
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-dev-$(openssl rand -hex 32)
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,backend

# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/dealaai_dev

# Redis
REDIS_URL=redis://redis:6379/0

# OpenAI
OPENAI_API_KEY=sk-your-api-key-here

# Supabase (opcional)
SUPABASE_URL=
SUPABASE_KEY=

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EOF
    info "✓ Creado backend/.env"
else
    info "✓ backend/.env ya existe"
fi

if [ ! -f "frontend/.env.local" ]; then
    warning "Creando frontend/.env.local desde template..."
    cat > frontend/.env.local << 'EOF'
# API URLs
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Supabase (opcional)
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=

# Environment
NEXT_PUBLIC_ENV=development
EOF
    info "✓ Creado frontend/.env.local"
else
    info "✓ frontend/.env.local ya existe"
fi

# 3. Construir imágenes Docker
log "Construyendo imágenes Docker..."
docker-compose build --no-cache

# 4. Iniciar servicios
log "Iniciando servicios..."
docker-compose up -d db redis

# Esperar a que la base de datos esté lista
info "Esperando a que PostgreSQL esté listo..."
sleep 5
until docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; do
    info "Esperando a PostgreSQL..."
    sleep 2
done
log "✓ PostgreSQL está listo"

# 5. Ejecutar migraciones (si existen)
if [ -d "backend" ]; then
    log "Ejecutando migraciones de Django..."
    docker-compose run --rm backend python manage.py migrate --noinput || warning "Error en migraciones (puede ser normal si aún no existen)"
fi

# 6. Crear superusuario (opcional)
read -p "¿Deseas crear un superusuario de Django? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    docker-compose run --rm backend python manage.py createsuperuser
fi

# 7. Instalar dependencias del frontend
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    log "Instalando dependencias del frontend..."
    cd frontend
    npm install
    cd ..
fi

# 8. Mostrar información de servicios
log "✅ Setup completado!"
echo ""
info "🚀 Servicios disponibles:"
echo "  - Frontend:     http://localhost:3000"
echo "  - Backend API:  http://localhost:8000"
echo "  - Admin Panel:  http://localhost:8000/admin"
echo "  - PostgreSQL:   localhost:5432"
echo "  - Redis:        localhost:6379"
echo ""
info "📚 Comandos útiles:"
echo "  - Iniciar todos los servicios:   docker-compose up -d"
echo "  - Ver logs:                       docker-compose logs -f"
echo "  - Detener servicios:              docker-compose down"
echo "  - Reiniciar servicios:            docker-compose restart"
echo "  - Ejecutar migraciones:           docker-compose exec backend python manage.py migrate"
echo "  - Crear superusuario:             docker-compose exec backend python manage.py createsuperuser"
echo "  - Shell de Django:                docker-compose exec backend python manage.py shell"
echo "  - Acceder a PostgreSQL:           docker-compose exec db psql -U postgres -d dealaai_dev"
echo ""
warning "⚠️  Recuerda configurar tu OPENAI_API_KEY en backend/.env"
echo ""
