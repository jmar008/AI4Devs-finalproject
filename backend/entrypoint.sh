#!/bin/bash
set -e

echo "=== DealaAI Backend Startup ==="

# Extraer nombre de DB de DATABASE_URL o usar variables individuales
if [ -n "$DATABASE_URL" ]; then
    DB_HOST=$(echo $DATABASE_URL | grep -oP 'host=\K[^&]*' || echo 'db')
    DB_NAME=$(echo $DATABASE_URL | grep -oP 'dbname=\K[^&]*' || echo 'dealaai_prod')
    DB_USER=$(echo $DATABASE_URL | grep -oP 'user=\K[^&]*' || echo 'postgres')
    DB_PASSWORD=$(echo $DATABASE_URL | grep -oP 'password=\K[^@]*' || echo 'postgres')
else
    DB_HOST=${DB_HOST:-db}
    DB_NAME=${DB_NAME:-dealaai_prod}
    DB_USER=${DB_USER:-postgres}
    DB_PASSWORD=${DB_PASSWORD:-postgres}
fi

echo "Database configuration:"
echo "  Host: $DB_HOST"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"

# Esperar a que la BD esté lista (máximo 30 intentos)
echo "Waiting for database to be ready..."
max_attempts=30
attempt=1
until python -c "import psycopg2; psycopg2.connect(host='$DB_HOST', database='$DB_NAME', user='$DB_USER', password='$DB_PASSWORD')" 2>/dev/null; do
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
    echo "✓ Migrations completed successfully"
else
    echo "⚠ Migrations failed or no migrations pending"
fi

# Crear tabla de cache
echo "Creating cache table..."
python manage.py createcachetable 2>/dev/null || echo "⚠ Cache table already exists or couldn't be created"
echo "✓ Cache table ready"

# Recopilar archivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear 2>/dev/null || true
echo "✓ Static files collected"

echo "=== Starting Gunicorn ==="
exec "$@"
