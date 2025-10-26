# Release Tasks - Se ejecutan automáticamente en cada deploy
# Estas tareas se ejecutan ANTES de iniciar los procesos del Procfile

# Ejecutar migraciones de base de datos
release: cd backend && python manage.py migrate --noinput

# Recopilar archivos estáticos
release: cd backend && python manage.py collectstatic --noinput
