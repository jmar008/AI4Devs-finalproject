#!/bin/bash

# Script de Validación Pre-Despliegue EasyPanel
# Ejecutar antes de subir a EasyPanel

set -e

COLORS='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${COLORS}============================================${NC}"
echo -e "${COLORS}🔍 Validando Configuración para EasyPanel${NC}"
echo -e "${COLORS}============================================${NC}\n"

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0

# Helper function
check() {
    local name=$1
    local command=$2

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $name"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗${NC} $name"
        ((CHECKS_FAILED++))
    fi
}

# 1. Validar archivos requeridos
echo -e "${YELLOW}📁 Verificando Archivos...${NC}"
check "docker-compose.easypanel.yml existe" "test -f docker-compose.easypanel.yml"
check "docker-compose.yml existe" "test -f docker-compose.yml"
check "backend/Dockerfile existe" "test -f backend/Dockerfile"
check "frontend/Dockerfile existe" "test -f frontend/Dockerfile"
check "docker/nginx/nginx.conf existe" "test -f docker/nginx/nginx.conf"
echo ""

# 2. Validar Dockerfiles
echo -e "${YELLOW}🐳 Validando Dockerfiles...${NC}"
check "backend/Dockerfile es válido" "docker build --dry-run -f backend/Dockerfile ./backend"
check "frontend/Dockerfile es válido" "docker build --dry-run -f frontend/Dockerfile ./frontend"
echo ""

# 3. Validar docker-compose
echo -e "${YELLOW}🔧 Validando docker-compose...${NC}"
check "docker-compose.easypanel.yml es válido" "docker-compose -f docker-compose.easypanel.yml config > /dev/null"
check "docker-compose.yml es válido" "docker-compose -f docker-compose.yml config > /dev/null"
echo ""

# 4. Validar configuración de variables
echo -e "${YELLOW}🔐 Verificando Variables de Entorno...${NC}"
if test -f .env; then
    echo -e "${GREEN}✓${NC} Archivo .env encontrado"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Archivo .env no encontrado (necesario en EasyPanel)"
fi

if test -f .env.easypanel.example; then
    echo -e "${GREEN}✓${NC} .env.easypanel.example encontrado"
    ((CHECKS_PASSED++))
else
    echo -e "${RED}✗${NC} .env.easypanel.example no encontrado"
    ((CHECKS_FAILED++))
fi
echo ""

# 5. Validar directorios requeridos
echo -e "${YELLOW}📂 Verificando Directorios...${NC}"
check "Carpeta backend existe" "test -d backend"
check "Carpeta frontend existe" "test -d frontend"
check "Carpeta docker existe" "test -d docker"
check "Carpeta database existe" "test -d database"
echo ""

# 6. Validar archivos críticos del backend
echo -e "${YELLOW}🐍 Validando Backend (Django)...${NC}"
check "manage.py existe" "test -f backend/manage.py"
check "settings.py existe" "test -f backend/dealaai/settings"
check "requirements.txt existe" "test -f backend/requirements.txt"
check "entrypoint.sh existe" "test -f backend/entrypoint.sh"
echo ""

# 7. Validar archivos críticos del frontend
echo -e "${YELLOW}⚛️  Validando Frontend (Next.js)...${NC}"
check "package.json existe" "test -f frontend/package.json"
check "next.config.js existe" "test -f frontend/next.config.js"
check ".gitignore existe en frontend" "test -f frontend/.gitignore"
echo ""

# 8. Validar que no hay archivos problemáticos
echo -e "${YELLOW}🚫 Verificando Exclusiones...${NC}"
check "No hay node_modules en frontend" "! test -d frontend/node_modules"
check "No hay __pycache__ en backend" "! test -d backend/__pycache__"
check "No hay .env en el repositorio" "! test -f backend/.env"
echo ""

# 9. Validar git (si es repositorio)
echo -e "${YELLOW}📦 Validando Git...${NC}"
if test -d .git; then
    check "Repositorio Git válido" "git status > /dev/null"
    check "Todos los cambios están commiteados" "test -z \"\$(git status --porcelain)\""
else
    echo -e "${YELLOW}⚠${NC} No es un repositorio Git (necesario para EasyPanel)"
fi
echo ""

# 10. Resumen
echo -e "${COLORS}============================================${NC}"
echo -e "${COLORS}📊 RESUMEN${NC}"
echo -e "${COLORS}============================================${NC}"
echo -e "✓ Verificaciones pasadas: ${GREEN}${CHECKS_PASSED}${NC}"
echo -e "✗ Verificaciones fallidas: ${RED}${CHECKS_FAILED}${NC}"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ¡Todo está listo para desplegar en EasyPanel!${NC}"
    echo ""
    echo -e "${YELLOW}Próximos pasos:${NC}"
    echo "1. Asegúrate de tener un repositorio Git actualizado"
    echo "2. Conecta tu repositorio en EasyPanel"
    echo "3. Configura el archivo: docker-compose.easypanel.yml"
    echo "4. Agrega las variables de entorno desde .env.easypanel.example"
    echo "5. Despliega el proyecto"
    exit 0
else
    echo -e "${RED}✗ Hay ${CHECKS_FAILED} problema(s) a resolver antes de desplegar${NC}"
    exit 1
fi
