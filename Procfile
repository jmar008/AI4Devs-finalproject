# Procfile para Easypanel con Heroku Buildpacks

# Define los procesos que se ejecutarán en producción

# Servidor web Django con Gunicorn

# $PORT es proporcionado automáticamente por Easypanel

web: cd backend && gunicorn dealaai.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4 --threads 2 --timeout 120 --access-logfile - --error-logfile -

# Celery Worker para tareas asíncronas

worker: cd backend && celery -A dealaai worker --loglevel=info --concurrency=2

# Celery Beat para tareas programadas (migración de stock a la 1 AM)

# IMPORTANTE: Solo ejecutar 1 instancia de beat

beat: cd backend && celery -A dealaai beat --loglevel=info
