#!/bin/bash

# 🚀 Script de Despliegue a Producción - DealaAI
# Uso: ./deploy-production.sh

set -e

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Funciones
print_header() {
    echo -e "\n${GREEN}================================${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${GREEN}================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Validaciones iniciales
print_header "VALIDACIONES INICIALES"

# Verificar que estamos en main
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    print_error "Debes estar en la rama 'main' para desplegar"
    echo "Rama actual: $CURRENT_BRANCH"
    exit 1
fi
print_success "Rama correcta: main"

# Verificar que no hay cambios sin commitear
if ! git diff-index --quiet HEAD --; then
    print_error "Hay cambios sin commitear"
    echo "Ejecuta 'git status' para ver los cambios"
    exit 1
fi
print_success "No hay cambios sin commitear"

# Verificar .env.production existe
if [ ! -f ".env.production" ]; then
    print_error ".env.production no existe"
    echo "Crea el archivo .env.production con las variables de entorno"
    exit 1
fi
print_success ".env.production encontrado"

# Obtener versión
print_header "INFORMACIÓN DE VERSIÓN"

VERSION=$(grep "version" package.json | head -1 | awk -F: '{ print $2 }' | sed 's/[",]//g' | tr -d ' ')
print_success "Versión detectada: $VERSION"

COMMIT_HASH=$(git rev-parse --short HEAD)
print_success "Commit: $COMMIT_HASH"

# Construir imágenes
print_header "CONSTRUYENDO IMÁGENES DOCKER"

print_warning "Construyendo imagen del backend..."
docker build -f docker/backend/Dockerfile.prod \
  -t dealaai-backend:$VERSION \
  -t dealaai-backend:latest \
  --build-arg DJANGO_SETTINGS_MODULE=dealaai.settings.production \
  ./backend

print_success "Backend construido: dealaai-backend:$VERSION"

print_warning "Construyendo imagen del frontend..."
docker build -f docker/frontend/Dockerfile.prod \
  -t dealaai-frontend:$VERSION \
  -t dealaai-frontend:latest \
  --build-arg NODE_ENV=production \
  ./frontend

print_success "Frontend construido: dealaai-frontend:$VERSION"

# Validaciones de imagen
print_header "VALIDACIONES DE IMAGEN"

print_warning "Validando backend..."
docker run --rm \
  -e DJANGO_SETTINGS_MODULE=dealaai.settings.production \
  dealaai-backend:$VERSION \
  python manage.py check

print_success "Backend validado ✓"

# Crear tag de versión
print_header "CREANDO TAG DE VERSIÓN"

TAG_NAME="v$VERSION-prod-$(date +%Y%m%d)"

print_warning "Creando tag: $TAG_NAME"
git tag -a $TAG_NAME \
  -m "Production Release - DealaAI $VERSION

Docker Images:
- dealaai-backend:$VERSION
- dealaai-frontend:$VERSION

Commit: $COMMIT_HASH
Date: $(date)
"

git push origin $TAG_NAME
print_success "Tag creado y pusheado: $TAG_NAME"

# Preparar para deploy en servidor remoto
print_header "INSTRUCCIONES PARA DEPLOY EN SERVIDOR REMOTO"

cat << EOF

${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}
${GREEN}║  PRÓXIMOS PASOS EN EL SERVIDOR DE PRODUCCIÓN                  ║${NC}
${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}

1. SSH al servidor:
   ${YELLOW}ssh usuario@mcp.jorgemg.es${NC}

2. Navega al directorio del proyecto:
   ${YELLOW}cd /opt/dealaai/AI4Devs-finalproject${NC}

3. Descarga los cambios:
   ${YELLOW}git fetch origin${NC}
   ${YELLOW}git checkout $TAG_NAME${NC}

4. Actualiza imágenes:
   ${YELLOW}docker pull dealaai-backend:$VERSION${NC}
   ${YELLOW}docker pull dealaai-frontend:$VERSION${NC}

5. Detén servicios actuales:
   ${YELLOW}docker-compose -f docker-compose.production.yml down${NC}

6. Levanta nuevos servicios:
   ${YELLOW}docker-compose -f docker-compose.production.yml up -d${NC}

7. Ejecuta migraciones:
   ${YELLOW}docker-compose -f docker-compose.production.yml exec backend \\${NC}
   ${YELLOW}  python manage.py migrate --noinput${NC}

8. Recolecta static files:
   ${YELLOW}docker-compose -f docker-compose.production.yml exec backend \\${NC}
   ${YELLOW}  python manage.py collectstatic --noinput${NC}

9. Verifica estado:
   ${YELLOW}docker-compose -f docker-compose.production.yml ps${NC}

10. Prueba endpoints:
    ${YELLOW}curl -I https://mcp.jorgemg.es/${NC}
    ${YELLOW}curl -I https://mcp.jorgemg.es/api/health/${NC}

${GREEN}════════════════════════════════════════════════════════════════${NC}

Versión deployada: $VERSION
Tag: $TAG_NAME
Commit: $COMMIT_HASH
Timestamp: $(date)

${GREEN}✅ Imágenes Docker listos para push a producción${NC}

EOF

print_success "Script de deploy completado"

