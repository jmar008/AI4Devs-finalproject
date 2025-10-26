#!/bin/bash
set -e

echo "=== DealaAI Backend Startup ==="

# Esperar a que la BD esté lista
echo "Waiting for database..."
while ! python -c "import psycopg2; psycopg2.connect('dbname=dealaai_prod user=postgres host=db password=${DB_PASSWORD}')" 2>/dev/null; do
  echo "Database not ready, waiting..."
  sleep 1
done
echo "✓ Database is ready"

# Ejecutar migraciones
echo "Running migrations..."
python manage.py migrate --noinput
echo "✓ Migrations completed"

# Crear tabla de cache
echo "Creating cache table..."
python manage.py createcachetable || true
echo "✓ Cache table created"

# Recopilar archivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || true
echo "✓ Static files collected"

echo "=== Starting Gunicorn ==="
exec "$@"
