#!/bin/bash
# Script para configurar variables de entorno en producción
# Ejecutar en el VPS después de subir los archivos

echo "=== Configuración de Variables de Entorno para DealaAI ==="
echo "Este script configura las variables necesarias para producción"
echo ""

# Verificar si estamos en el directorio correcto
if [ ! -f "docker-compose.production.yml" ]; then
    echo "❌ Error: No se encuentra docker-compose.production.yml"
    echo "Asegúrate de estar en el directorio raíz del proyecto"
    exit 1
fi

echo "📝 Configurando variables de entorno..."
echo ""

# Generar SECRET_KEY segura
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
echo "✅ SECRET_KEY generada: $SECRET_KEY"

# Solicitar configuración al usuario
read -p "🔐 Contraseña para PostgreSQL [postgres123]: " DB_PASSWORD
DB_PASSWORD=${DB_PASSWORD:-postgres123}

read -p "🤖 API Key de OpenRouter (DeepSeek) [dejar vacío para usar la existente]: " DEEPSEEK_API_KEY
DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY:-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}

read -p "🔑 Contraseña para pgAdmin [admin123]: " PGADMIN_PASSWORD
PGADMIN_PASSWORD=${PGADMIN_PASSWORD:-admin123}

# Crear archivo .env.production si no existe
if [ ! -f ".env.production" ]; then
    echo "📄 Creando .env.production..."
    cat > .env.production << EOF
# Variables de Entorno para Producción - EasyPanel
# Generado automáticamente por setup-production.sh

# Seguridad - Django
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=mcp.jorgemg.es,backend,nginx,localhost,127.0.0.1

# Base de datos PostgreSQL
DB_PASSWORD=$DB_PASSWORD
DATABASE_URL=postgresql://postgres:\${DB_PASSWORD}@db:5432/dealaai_prod

# Redis
REDIS_URL=redis://redis:6379/0

# OpenAI API
OPENAI_API_KEY=$DEEPSEEK_API_KEY
DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY

# CORS y URLs
CORS_ALLOWED_ORIGINS=https://mcp.jorgemg.es
NEXT_PUBLIC_API_URL=https://mcp.jorgemg.es/api/v1
NEXT_PUBLIC_WS_URL=wss://mcp.jorgemg.es/ws
NEXT_PUBLIC_DOMAIN=mcp.jorgemg.es

# pgAdmin
PGADMIN_PASSWORD=$PGADMIN_PASSWORD

# Configuración SSL/TLS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True

# Logging
LOG_LEVEL=INFO
EOF
    echo "✅ Archivo .env.production creado"
else
    echo "⚠️  Archivo .env.production ya existe. Respaldando..."
    cp .env.production .env.production.backup
    echo "✅ Backup creado: .env.production.backup"
fi

# Actualizar backend/.env.production
echo "📝 Actualizando backend/.env.production..."
cat > backend/.env.production << EOF
# Variables de Entorno para Producción - Backend
# Generado automáticamente por setup-production.sh

# Django Settings
DEBUG=False
SECRET_KEY=$SECRET_KEY
ALLOWED_HOSTS=mcp.jorgemg.es,backend,nginx,localhost,127.0.0.1

# Base de datos PostgreSQL
DB_NAME=dealaai_prod
DB_USER=postgres
DB_PASSWORD=$DB_PASSWORD
DB_HOST=db
DB_PORT=5432
DATABASE_URL=postgresql://postgres:$DB_PASSWORD@db:5432/dealaai_prod

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# DeepSeek AI API
DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY

# CORS
CORS_ALLOWED_ORIGINS=https://mcp.jorgemg.es

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Media y Static
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles

# Logging
LOG_LEVEL=INFO

# Seguridad SSL
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
EOF

echo "✅ Archivo backend/.env.production actualizado"
echo ""
echo "🎉 Configuración completada!"
echo ""
echo "📋 Resumen de configuración:"
echo "   SECRET_KEY: $SECRET_KEY"
echo "   DB_PASSWORD: $DB_PASSWORD"
echo "   DEEPSEEK_API_KEY: ${DEEPSEEK_API_KEY:0:20}..."
echo "   PGADMIN_PASSWORD: $PGADMIN_PASSWORD"
echo ""
echo "🚀 Ahora puedes ejecutar:"
echo "   docker-compose -f docker-compose.production.yml up -d"
echo ""
echo "📊 Para verificar el estado:"
echo "   docker-compose -f docker-compose.production.yml ps"
echo ""
echo "📜 Para ver logs del backend:"
echo "   docker logs dealaai_backend_prod"
