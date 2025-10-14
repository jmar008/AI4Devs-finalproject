# Makefile para DealaAI - Comandos simplificados

.PHONY: help setup start stop restart logs clean test lint format

# Colores para output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "$(GREEN)DealaAI - Comandos disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

setup: ## Setup inicial del proyecto
	@echo "$(GREEN)Ejecutando setup inicial...$(NC)"
	@chmod +x scripts/setup.sh scripts/dev.sh
	@./scripts/setup.sh

start: ## Iniciar todos los servicios
	@echo "$(GREEN)Iniciando servicios...$(NC)"
	@docker-compose up -d
	@echo "$(GREEN)✓ Servicios iniciados$(NC)"
	@echo "$(BLUE)Frontend: http://localhost:3000$(NC)"
	@echo "$(BLUE)Backend:  http://localhost:8000$(NC)"

stop: ## Detener todos los servicios
	@echo "$(YELLOW)Deteniendo servicios...$(NC)"
	@docker-compose down
	@echo "$(GREEN)✓ Servicios detenidos$(NC)"

restart: ## Reiniciar servicios
	@echo "$(YELLOW)Reiniciando servicios...$(NC)"
	@docker-compose restart
	@echo "$(GREEN)✓ Servicios reiniciados$(NC)"

logs: ## Ver logs de todos los servicios
	@docker-compose logs -f

logs-backend: ## Ver logs del backend
	@docker-compose logs -f backend

logs-frontend: ## Ver logs del frontend
	@docker-compose logs -f frontend

status: ## Estado de los servicios
	@docker-compose ps

shell-backend: ## Shell del backend (Django)
	@docker-compose exec backend python manage.py shell

shell-db: ## Conectar a PostgreSQL
	@docker-compose exec db psql -U postgres -d dealaai_dev

migrate: ## Ejecutar migraciones de Django
	@echo "$(GREEN)Ejecutando migraciones...$(NC)"
	@docker-compose exec backend python manage.py migrate
	@echo "$(GREEN)✓ Migraciones completadas$(NC)"

makemigrations: ## Crear nuevas migraciones
	@echo "$(GREEN)Creando migraciones...$(NC)"
	@docker-compose exec backend python manage.py makemigrations

superuser: ## Crear superusuario de Django
	@docker-compose exec backend python manage.py createsuperuser

test: ## Ejecutar todos los tests
	@echo "$(GREEN)Ejecutando tests del backend...$(NC)"
	@docker-compose exec backend pytest
	@echo "$(GREEN)Ejecutando tests del frontend...$(NC)"
	@cd frontend && npm test

test-backend: ## Tests del backend
	@docker-compose exec backend pytest

test-frontend: ## Tests del frontend
	@cd frontend && npm test

test-coverage: ## Tests con cobertura
	@docker-compose exec backend pytest --cov=apps --cov-report=html
	@cd frontend && npm test -- --coverage

lint: ## Linting de código
	@echo "$(GREEN)Linting backend...$(NC)"
	@docker-compose exec backend flake8 .
	@echo "$(GREEN)Linting frontend...$(NC)"
	@cd frontend && npm run lint

format: ## Formatear código
	@echo "$(GREEN)Formateando backend...$(NC)"
	@docker-compose exec backend black .
	@docker-compose exec backend isort .
	@echo "$(GREEN)Formateando frontend...$(NC)"
	@cd frontend && npm run format

clean: ## Limpiar contenedores y volúmenes
	@echo "$(RED)Limpiando contenedores y volúmenes...$(NC)"
	@docker-compose down -v
	@docker system prune -f
	@echo "$(GREEN)✓ Limpieza completada$(NC)"

rebuild: ## Rebuild completo
	@echo "$(YELLOW)Rebuild completo...$(NC)"
	@docker-compose down -v
	@docker-compose build --no-cache
	@docker-compose up -d
	@echo "$(GREEN)✓ Rebuild completado$(NC)"

backup-db: ## Backup de la base de datos
	@echo "$(GREEN)Creando backup de la base de datos...$(NC)"
	@mkdir -p database/backups
	@docker-compose exec -T db pg_dump -U postgres dealaai_dev > database/backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✓ Backup creado en database/backups/$(NC)"

restore-db: ## Restaurar base de datos (usar: make restore-db FILE=backup.sql)
	@echo "$(YELLOW)Restaurando base de datos desde $(FILE)...$(NC)"
	@docker-compose exec -T db psql -U postgres dealaai_dev < $(FILE)
	@echo "$(GREEN)✓ Base de datos restaurada$(NC)"

install-backend: ## Instalar dependencias del backend
	@echo "$(GREEN)Instalando dependencias del backend...$(NC)"
	@docker-compose exec backend pip install -r requirements/development.txt

install-frontend: ## Instalar dependencias del frontend
	@echo "$(GREEN)Instalando dependencias del frontend...$(NC)"
	@cd frontend && npm install

dev-backend: ## Modo desarrollo backend (con auto-reload)
	@docker-compose exec backend python manage.py runserver 0.0.0.0:8000

dev-frontend: ## Modo desarrollo frontend
	@cd frontend && npm run dev

collectstatic: ## Colectar archivos estáticos
	@docker-compose exec backend python manage.py collectstatic --noinput

loaddata: ## Cargar datos de ejemplo (fixtures)
	@docker-compose exec backend python manage.py loaddata fixtures/sample_data.json

dumpdata: ## Exportar datos actuales
	@docker-compose exec backend python manage.py dumpdata --indent 2 > fixtures/backup_$$(date +%Y%m%d_%H%M%S).json

.DEFAULT_GOAL := help
