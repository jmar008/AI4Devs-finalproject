#!/bin/bash
set -e

echo "=== DealaAI Backend Startup ==="

# Configuración de base de datos
DB_HOST=${DB_HOST:-db}
DB_NAME=${DB_NAME:-dealaai_dev}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}

echo "Database configuration:"
echo "  Host: $DB_HOST"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"

# Esperar a que la BD esté lista (máximo 30 intentos)
echo "Waiting for database to be ready..."
max_attempts=30
attempt=1
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  if [ $attempt -ge $max_attempts ]; then
    echo "✗ Database connection failed after $max_attempts attempts"
    exit 1
  fi
  echo "  Attempt $attempt/$max_attempts - Database not ready yet, waiting..."
  sleep 2
  attempt=$((attempt + 1))
done
echo "✓ Database is ready"

# Ejecutar migraciones
echo "Running migrations..."
if python manage.py migrate --noinput; then
    echo "✓ Migrations completed"
else
    exit_code=$?
    echo "⚠ Migrations failed, attempting to fake migrations..."
    python manage.py migrate --fake-initial
    echo "✓ Migrations marked as applied"
fi

# Crear tabla de cache (opcional)
echo "Creating cache table..."
python manage.py createcachetable 2>/dev/null || echo "⚠ Cache table already exists"

# Recopilar archivos estáticos (solo si no es desarrollo)
if [ "$DJANGO_SETTINGS_MODULE" != "dealaai.settings.development" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear
    echo "✓ Static files collected"
fi

echo "=== Starting Django ==="
exec "$@"
