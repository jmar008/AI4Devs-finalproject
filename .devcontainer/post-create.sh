#!/bin/bash

# Script de inicialización después de crear el devcontainer
set -e

echo "🚀 Iniciando configuración del entorno de desarrollo DealaAI..."

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función de log
log() {
    echo -e "${GREEN}[DealaAI Setup]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[Warning]${NC} $1"
}

info() {
    echo -e "${BLUE}[Info]${NC} $1"
}

# 1. Configurar Git
log "Configurando Git..."
git config --global core.autocrlf input
git config --global pull.rebase false

# 2. Crear archivos .env si no existen
log "Creando archivos de configuración..."

if [ ! -f "backend/.env" ]; then
    cat > backend/.env << 'EOF'
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dealaai_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# OpenAI
OPENAI_API_KEY=your-openai-api-key-here

# Supabase (opcional para desarrollo)
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF
    info "Creado backend/.env (recuerda configurar tus API keys)"
fi

if [ ! -f "frontend/.env.local" ]; then
    cat > frontend/.env.local << 'EOF'
# API URLs
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Supabase (opcional)
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key

# Environment
NEXT_PUBLIC_ENV=development
EOF
    info "Creado frontend/.env.local"
fi

# 3. Instalar dependencias del backend (Python)
if [ -d "backend" ]; then
    log "Instalando dependencias de Python..."
    cd backend

    # Crear entorno virtual si no existe
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi

    # Activar entorno virtual e instalar dependencias
    source venv/bin/activate

    if [ -f "requirements/development.txt" ]; then
        pip install -r requirements/development.txt
    elif [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        warning "No se encontró requirements.txt en backend/"
    fi

    deactivate
    cd ..
fi

# 4. Instalar dependencias del frontend (Node.js)
if [ -d "frontend" ]; then
    log "Instalando dependencias de Node.js..."
    cd frontend

    if [ -f "package.json" ]; then
        npm install
    else
        warning "No se encontró package.json en frontend/"
    fi

    cd ..
fi

# 5. Esperar a que la base de datos esté lista
log "Esperando a que PostgreSQL esté listo..."
until pg_isready -h localhost -p 5432 -U postgres; do
    info "Esperando a PostgreSQL..."
    sleep 2
done

# 6. Configurar la base de datos
if [ -d "backend" ]; then
    log "Configurando base de datos..."
    cd backend
    source venv/bin/activate

    # Habilitar extensión pgvector
    PGPASSWORD=postgres psql -h localhost -U postgres -d dealaai_dev -c "CREATE EXTENSION IF NOT EXISTS vector;" || true

    # Ejecutar migraciones si existen
    if [ -f "manage.py" ]; then
        python manage.py migrate --noinput || warning "Error en migraciones"
    fi

    deactivate
    cd ..
fi

# 7. Crear directorios necesarios
log "Creando estructura de directorios..."
mkdir -p backend/{apps,core,fixtures,media,static,logs}
mkdir -p frontend/{app,components,lib,hooks,store,types,public}
mkdir -p database/{migrations,fixtures,backups}
mkdir -p docker/{frontend,backend,nginx}
mkdir -p docs/{api,architecture,deployment}

# 8. Crear archivos de configuración adicionales
log "Creando archivos de configuración..."

# .editorconfig
cat > .editorconfig << 'EOF'
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
EOF

# .gitignore
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/
*.egg-info/
dist/
build/

# Django
*.log
db.sqlite3
media/
staticfiles/
.env

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Next.js
.next/
out/
.vercel
*.tsbuildinfo

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
.coverage
htmlcov/
.pytest_cache/

# Docker
*.log
EOF
fi

# 9. Mostrar información útil
echo ""
log "✅ Configuración completada!"
echo ""
info "📚 Comandos útiles:"
echo ""
echo "  Backend (Django):"
echo "    cd backend && source venv/bin/activate"
echo "    python manage.py runserver 0.0.0.0:8000"
echo "    python manage.py makemigrations"
echo "    python manage.py migrate"
echo "    python manage.py createsuperuser"
echo ""
echo "  Frontend (Next.js):"
echo "    cd frontend"
echo "    npm run dev"
echo "    npm run build"
echo "    npm run lint"
echo ""
echo "  Base de datos:"
echo "    psql -h localhost -U postgres -d dealaai_dev"
echo ""
echo "  Docker:"
echo "    docker-compose up -d"
echo "    docker-compose logs -f"
echo "    docker-compose down"
echo ""
info "🔧 Recuerda configurar tus API keys en los archivos .env"
info "📖 Consulta el README.md para más información"
echo ""
