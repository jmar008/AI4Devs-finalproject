#!/bin/bash

# Script para inicializar proyectos y configurar servicios
set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Funciones de log
log() { echo -e "${GREEN}[Init]${NC} $1"; }
info() { echo -e "${BLUE}[Info]${NC} $1"; }
warning() { echo -e "${YELLOW}[Warning]${NC} $1"; }
error() { echo -e "${RED}[Error]${NC} $1"; }

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║       Inicialización de Proyectos - DealaAI            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f ".devcontainer/devcontainer.json" ]; then
    error "Este script debe ejecutarse desde la raíz del proyecto"
    exit 1
fi

# 1. Inicializar proyecto Django si no existe
if [ ! -d "backend" ]; then
    log "Creando directorio backend..."
    mkdir -p backend
fi

if [ ! -f "backend/manage.py" ]; then
    log "Inicializando proyecto Django..."
    cd backend
    django-admin startproject dealaai .
    cd ..
    info "✓ Proyecto Django creado en backend/"
else
    info "✓ Proyecto Django ya existe"
fi

# 2. Inicializar proyecto Next.js si no existe
if [ ! -d "frontend" ]; then
    log "Creando directorio frontend..."
    mkdir -p frontend
fi

if [ ! -f "frontend/package.json" ]; then
    log "Inicializando proyecto Next.js..."
    cd frontend
    npx create-next-app@latest . --typescript --tailwind --app --src-dir --eslint --import-alias "@/*" --yes
    cd ..
    info "✓ Proyecto Next.js creado en frontend/"
else
    info "✓ Proyecto Next.js ya existe"
fi

# 3. Actualizar docker-compose.yml para incluir servicios con puertos expuestos
log "Actualizando configuración de servicios..."

DOCKER_COMPOSE_FILE=".devcontainer/docker-compose.yml"

# Backup del archivo original
cp "$DOCKER_COMPOSE_FILE" "${DOCKER_COMPOSE_FILE}.backup"

# Crear nuevo docker-compose.yml con servicios expuestos
cat > "$DOCKER_COMPOSE_FILE" << 'EOF'
services:
  # Contenedor principal de desarrollo
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ../..:/workspaces:cached
    command: sleep infinity
    network_mode: service:db
    depends_on:
      - db
      - redis

  # Base de datos PostgreSQL con pgvector
  db:
    image: ankane/pgvector:latest
    restart: unless-stopped
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: dealaai_dev
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis para cache y Celery
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend Django (cuando esté listo)
  backend:
    build:
      context: ../backend
      dockerfile: ../docker/backend/Dockerfile
    restart: unless-stopped
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ../backend:/app
    ports:
      - "8000:8000"
    env_file:
      - ../backend/.env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - default
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Frontend Next.js (cuando esté listo)
  frontend:
    build:
      context: ../frontend
      dockerfile: ../docker/frontend/Dockerfile
    restart: unless-stopped
    command: npm run dev
    volumes:
      - ../frontend:/app
      - /app/node_modules
      - /app/.next
    ports:
      - "3000:3000"
    env_file:
      - ../frontend/.env.local
    depends_on:
      - backend
    networks:
      - default
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  postgres-data:
  redis-data:

EOF

info "✓ Docker Compose actualizado con servicios expuestos"

# 4. Verificar configuración
log "Verificando configuración..."

if docker compose -f "$DOCKER_COMPOSE_FILE" config > /dev/null 2>&1; then
    info "✓ Configuración de Docker Compose válida"
else
    error "❌ Error en configuración de Docker Compose"
    # Restaurar backup
    mv "${DOCKER_COMPOSE_FILE}.backup" "$DOCKER_COMPOSE_FILE"
    exit 1
fi

# 5. Reiniciar servicios
log "Reiniciando servicios..."

docker compose -f "$DOCKER_COMPOSE_FILE" down
docker compose -f "$DOCKER_COMPOSE_FILE" up -d --build

# Limpiar backup
rm -f "${DOCKER_COMPOSE_FILE}.backup"

echo ""
log "🎉 Inicialización completada!"
echo ""
info "Servicios disponibles:"
info "  📊 PostgreSQL: localhost:5432"
info "  🔄 Redis: localhost:6379"
info "  🚀 Backend API: localhost:8000 (cuando esté listo)"
info "  🌐 Frontend: localhost:3000 (cuando esté listo)"
echo ""
info "Para acceder desde fuera del devcontainer:"
info "  - PostgreSQL: psql postgresql://postgres:postgres@localhost:5432/dealaai_dev"
info "  - Redis: redis-cli -h localhost -p 6379"
info "  - API: http://localhost:8000"
info "  - Frontend: http://localhost:3000"
echo ""

# 6. Próximos pasos
echo "📋 Próximos pasos:"
echo "  1. Configurar la base de datos: python manage.py migrate"
echo "  2. Crear superusuario: python manage.py createsuperuser"
echo "  3. Instalar dependencias del frontend: npm install"
echo "  4. Configurar variables de entorno (OPENAI_API_KEY, etc.)"
echo ""
