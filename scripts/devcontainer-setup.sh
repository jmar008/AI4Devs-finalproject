#!/bin/bash

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 Configurando entorno de desarrollo en DevContainer...${NC}"

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para mostrar progreso
show_progress() {
    echo -e "${GREEN}✅ $1${NC}"
}

show_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

show_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar que estamos en DevContainer
if [ ! -f /.dockerenv ]; then
    show_warning "No parece que estés ejecutando esto dentro de un DevContainer"
    echo "Para obtener la mejor experiencia, abre este proyecto en VS Code con DevContainer"
fi

# Instalar dependencias del backend
echo -e "${BLUE}📦 Instalando dependencias del backend...${NC}"
cd /workspaces/AI4Devs-finalproject/backend
if [ -f "requirements/development.txt" ]; then
    python -m pip install --upgrade pip
    pip install -r requirements/development.txt
    show_progress "Dependencias del backend instaladas"
else
    show_error "No se encontró requirements/development.txt"
fi

# Instalar dependencias del frontend
echo -e "${BLUE}📦 Instalando dependencias del frontend...${NC}"
cd /workspaces/AI4Devs-finalproject/frontend
if [ -f "package.json" ]; then
    npm install
    show_progress "Dependencias del frontend instaladas"
else
    show_error "No se encontró package.json en frontend"
fi

# Volver al directorio raíz
cd /workspaces/AI4Devs-finalproject

# Iniciar servicios de base de datos
echo -e "${BLUE}🗄️ Iniciando servicios de base de datos...${NC}"
docker-compose up -d db redis
sleep 5
show_progress "Servicios de base de datos iniciados"

# Ejecutar migraciones
echo -e "${BLUE}🔄 Ejecutando migraciones...${NC}"
cd backend
python manage.py migrate
show_progress "Migraciones ejecutadas"

# Crear superusuario si no existe
echo -e "${BLUE}👤 Verificando superusuario...${NC}"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('No existe superusuario. Crear uno con: python manage.py createsuperuser')
else:
    print('✅ Superusuario ya existe')
"

cd /workspaces/AI4Devs-finalproject

echo ""
echo -e "${GREEN}🎉 ¡Configuración completada!${NC}"
echo ""
echo -e "${BLUE}📋 Comandos útiles:${NC}"
echo -e "  ${YELLOW}Frontend:${NC}"
echo -e "    cd frontend && npm run dev    # Iniciar desarrollo"
echo -e "    npm test                      # Ejecutar tests"
echo -e "    npm run format                # Formatear código"
echo ""
echo -e "  ${YELLOW}Backend:${NC}"
echo -e "    cd backend && python manage.py runserver 0.0.0.0:8000"
echo -e "    python manage.py test         # Ejecutar tests"
echo -e "    python manage.py shell        # Django shell"
echo ""
echo -e "  ${YELLOW}Docker:${NC}"
echo -e "    docker-compose up -d          # Iniciar todos los servicios"
echo -e "    docker-compose logs -f        # Ver logs"
echo ""
echo -e "${BLUE}🌐 URLs importantes:${NC}"
echo -e "  Frontend:    http://localhost:3000"
echo -e "  Backend:     http://localhost:8000"
echo -e "  Admin:       http://localhost:8000/admin"
echo -e "  PgAdmin:     http://localhost:5050"
echo ""
echo -e "${GREEN}¡Listo para desarrollar! 🚀${NC}"