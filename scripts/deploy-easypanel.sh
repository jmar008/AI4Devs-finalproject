#!/bin/bash

# Script de Deployment para EasyPanel - DealaAI
# Ejecuta las tareas necesarias para desplegar en producción

set -e  # Salir si cualquier comando falla

echo "🚀 Iniciando deployment de DealaAI en EasyPanel..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.production.yml" ]; then
    print_error "No se encontró docker-compose.production.yml. Ejecuta desde el directorio raíz del proyecto."
    exit 1
fi

# Verificar que las variables de entorno están configuradas
print_status "Verificando variables de entorno..."
if [ -z "$SECRET_KEY" ] || [ -z "$DB_PASSWORD" ] || [ -z "$OPENAI_API_KEY" ]; then
    print_error "Variables de entorno críticas no configuradas. Verifica:"
    echo "  - SECRET_KEY"
    echo "  - DB_PASSWORD"
    echo "  - OPENAI_API_KEY"
    print_warning "Configura estas variables en EasyPanel antes de continuar."
    exit 1
fi

print_success "Variables de entorno verificadas"

# Crear red si no existe
print_status "Configurando red Docker..."
docker network create dealaai_network 2>/dev/null || print_warning "Red dealaai_network ya existe"

# Detener servicios existentes si están corriendo
print_status "Deteniendo servicios existentes..."
docker-compose -f docker-compose.production.yml down --remove-orphans

# Limpiar imágenes antiguas (opcional)
read -p "¿Quieres limpiar imágenes Docker antiguas? [y/N]: " cleanup
if [[ $cleanup =~ ^[Yy]$ ]]; then
    print_status "Limpiando imágenes Docker antiguas..."
    docker system prune -f
    docker image prune -f
fi

# Build de imágenes
print_status "Construyendo imágenes Docker..."
docker-compose -f docker-compose.production.yml build --no-cache

# Iniciar base de datos primero
print_status "Iniciando base de datos..."
docker-compose -f docker-compose.production.yml up -d db redis

# Esperar a que la base de datos esté lista
print_status "Esperando a que la base de datos esté lista..."
while ! docker-compose -f docker-compose.production.yml exec -T db pg_isready -U postgres -d dealaai_prod; do
    print_status "Esperando PostgreSQL..."
    sleep 5
done

print_success "Base de datos lista"

# Ejecutar migraciones
print_status "Ejecutando migraciones de Django..."
docker-compose -f docker-compose.production.yml run --rm backend python manage.py migrate

# Recopilar archivos estáticos
print_status "Recopilando archivos estáticos..."
docker-compose -f docker-compose.production.yml run --rm backend python manage.py collectstatic --noinput

# Crear superusuario si no existe
print_status "Configurando superusuario..."
docker-compose -f docker-compose.production.yml run --rm backend python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@mcp.jorgemg.es').exists():
    User.objects.create_superuser('admin@mcp.jorgemg.es', 'admin123')
    print('Superusuario creado: admin@mcp.jorgemg.es / admin123')
else:
    print('Superusuario ya existe')
"

# Cargar datos de ejemplo (opcional)
read -p "¿Quieres cargar datos de ejemplo? [y/N]: " load_fixtures
if [[ $load_fixtures =~ ^[Yy]$ ]]; then
    print_status "Cargando datos de ejemplo..."
    docker-compose -f docker-compose.production.yml run --rm backend python manage.py loaddata fixtures/sample_data.json
fi

# Iniciar todos los servicios
print_status "Iniciando todos los servicios..."
docker-compose -f docker-compose.production.yml up -d

# Verificar que los servicios están corriendo
print_status "Verificando estado de los servicios..."
sleep 30

services=("nginx" "frontend" "backend" "db" "redis" "celery_worker" "celery_beat")
for service in "${services[@]}"; do
    if docker-compose -f docker-compose.production.yml ps | grep -q "${service}.*Up"; then
        print_success "✓ $service está corriendo"
    else
        print_error "✗ $service no está corriendo"
        docker-compose -f docker-compose.production.yml logs $service
    fi
done

# Health checks
print_status "Ejecutando health checks..."

# Check frontend
if curl -f -s http://localhost:3000/health > /dev/null; then
    print_success "✓ Frontend respondiendo"
else
    print_warning "⚠ Frontend no responde en puerto 3000"
fi

# Check backend
if curl -f -s http://localhost:8000/api/health/ > /dev/null; then
    print_success "✓ Backend API respondiendo"
else
    print_warning "⚠ Backend API no responde en puerto 8000"
fi

# Check nginx
if curl -f -s http://localhost/health > /dev/null; then
    print_success "✓ Nginx proxy respondiendo"
else
    print_warning "⚠ Nginx proxy no responde"
fi

# Mostrar información de deployment
print_success "🎉 Deployment completado!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 INFORMACIÓN DEL DEPLOYMENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Aplicación principal: https://mcp.jorgemg.es"
echo "🔧 Django Admin: https://mcp.jorgemg.es/admin"
echo "📡 API: https://mcp.jorgemg.es/api/v1"
echo "🗄️ pgAdmin: https://mcp.jorgemg.es/pgadmin"
echo "🏗️ Supabase Studio: https://mcp.jorgemg.es/studio"
echo ""
echo "👤 Credenciales por defecto:"
echo "   Admin: admin@mcp.jorgemg.es / admin123"
echo "   pgAdmin: admin@mcp.jorgemg.es / (configurado en variables)"
echo ""
echo "📋 Comandos útiles:"
echo "   Ver logs: docker-compose -f docker-compose.production.yml logs -f"
echo "   Reiniciar: docker-compose -f docker-compose.production.yml restart"
echo "   Detener: docker-compose -f docker-compose.production.yml down"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Mostrar logs en tiempo real (opcional)
read -p "¿Quieres ver los logs en tiempo real? [y/N]: " show_logs
if [[ $show_logs =~ ^[Yy]$ ]]; then
    print_status "Mostrando logs en tiempo real... (Ctrl+C para salir)"
    docker-compose -f docker-compose.production.yml logs -f
fi
