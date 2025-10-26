#!/bin/bash

# Script de desarrollo - Shortcuts para comandos comunes
set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[Dev]${NC} $1"; }
info() { echo -e "${BLUE}[Info]${NC} $1"; }

# Función de ayuda
show_help() {
    echo "DealaAI - Scripts de Desarrollo"
    echo ""
    echo "Uso: ./scripts/dev.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  start         - Iniciar todos los servicios"
    echo "  stop          - Detener todos los servicios"
    echo "  restart       - Reiniciar todos los servicios"
    echo "  logs          - Ver logs de todos los servicios"
    echo "  backend       - Logs del backend"
    echo "  frontend      - Logs del frontend"
    echo "  db            - Acceder a PostgreSQL"
    echo "  migrate       - Ejecutar migraciones de Django"
    echo "  makemigrations - Crear nuevas migraciones"
    echo "  shell         - Shell de Django"
    echo "  test-backend  - Ejecutar tests del backend"
    echo "  test-frontend - Ejecutar tests del frontend"
    echo "  lint-backend  - Linting del backend"
    echo "  lint-frontend - Linting del frontend"
    echo "  clean         - Limpiar volúmenes y contenedores"
    echo ""
}

case "$1" in
    start)
        log "Iniciando servicios..."
        docker-compose up -d
        info "✓ Servicios iniciados"
        info "Frontend: http://localhost:3000"
        info "Backend:  http://localhost:8000"
        ;;

    stop)
        log "Deteniendo servicios..."
        docker-compose down
        info "✓ Servicios detenidos"
        ;;

    restart)
        log "Reiniciando servicios..."
        docker-compose restart
        info "✓ Servicios reiniciados"
        ;;

    logs)
        docker-compose logs -f
        ;;

    backend)
        docker-compose logs -f backend
        ;;

    frontend)
        docker-compose logs -f frontend
        ;;

    db)
        docker-compose exec db psql -U postgres -d dealaai_dev
        ;;

    migrate)
        log "Ejecutando migraciones..."
        docker-compose exec backend python manage.py migrate
        info "✓ Migraciones completadas"
        ;;

    makemigrations)
        log "Creando migraciones..."
        docker-compose exec backend python manage.py makemigrations
        info "✓ Migraciones creadas"
        ;;

    shell)
        docker-compose exec backend python manage.py shell
        ;;

    test-backend)
        log "Ejecutando tests del backend..."
        docker-compose exec backend pytest
        ;;

    test-frontend)
        log "Ejecutando tests del frontend..."
        cd frontend && npm test
        ;;

    lint-backend)
        log "Linting del backend..."
        docker-compose exec backend black .
        docker-compose exec backend isort .
        docker-compose exec backend flake8 .
        info "✓ Linting completado"
        ;;

    lint-frontend)
        log "Linting del frontend..."
        cd frontend && npm run lint
        info "✓ Linting completado"
        ;;

    clean)
        log "Limpiando contenedores y volúmenes..."
        docker-compose down -v
        docker system prune -f
        info "✓ Limpieza completada"
        ;;

    *)
        show_help
        ;;
esac
