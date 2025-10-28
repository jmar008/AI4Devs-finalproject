# Dockerfile para el backend Django
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requirements
COPY requirements/ ./requirements/
COPY requirements.txt .

# Instalar dependencias de Python (desarrollo)
RUN pip install --no-cache-dir -r requirements/development.txt

# Copiar código de la aplicación
COPY . .

# Copiar y dar permisos al entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Crear directorio para archivos estáticos y media
RUN mkdir -p /app/static /app/media /app/logs

# Exponer puerto
EXPOSE 8000

# Usar entrypoint para ejecutar migraciones antes de arrancar
ENTRYPOINT ["/entrypoint.sh"]

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
