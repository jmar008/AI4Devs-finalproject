#!/bin/bash
# Script de configuración para Railway
# Ejecutar después de crear el proyecto en Railway

echo "=== 🚀 Configuración para Railway ==="
echo "Este script te ayuda a configurar las variables de entorno para Railway"
echo ""

# Verificar si estamos en el directorio correcto
if [ ! -f "docker-compose.railway.yml" ]; then
    echo "❌ Error: No se encuentra docker-compose.railway.yml"
    echo "Asegúrate de estar en el directorio raíz del proyecto"
    exit 1
fi

echo "📝 Configurando variables de entorno para Railway..."
echo ""

# Generar SECRET_KEY segura
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))" 2>/dev/null || openssl rand -hex 32)
echo "✅ SECRET_KEY generada: $SECRET_KEY"

# Solicitar información del proyecto Railway
read -p "🔗 URL de tu proyecto Railway (ej: https://tu-proyecto.up.railway.app): " RAILWAY_URL
RAILWAY_URL=${RAILWAY_URL:-https://tu-proyecto.up.railway.app}

# Extraer dominio de la URL
DOMAIN=$(echo $RAILWAY_URL | sed 's|https://||' | sed 's|http://||')
echo "✅ Dominio detectado: $DOMAIN"

# Solicitar API keys
read -p "🤖 API Key de OpenRouter (DeepSeek) [dejar vacío para usar existente]: " DEEPSEEK_API_KEY
DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY:-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}

# Crear archivo .env.railway
cat > .env.railway << EOF
# Variables de Entorno para Railway - Generado automáticamente
# Sube este archivo a Railway como variables de entorno

# Seguridad - Django
SECRET_KEY=$SECRET_KEY

# Hosts y CORS
ALLOWED_HOSTS=$DOMAIN,backend,nginx,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=$RAILWAY_URL

# Frontend - Next.js
NEXT_PUBLIC_API_URL=$RAILWAY_URL
NEXT_PUBLIC_WS_URL=wss://$DOMAIN/ws
NEXT_PUBLIC_DOMAIN=$DOMAIN

# AI APIs
DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY

# Configuración de producción
DEBUG=False
DJANGO_SETTINGS_MODULE=dealaai.settings.production
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Media y Static
MEDIA_URL=/media/
STATIC_URL=/static/

# Logging
LOG_LEVEL=INFO
EOF

echo "✅ Archivo .env.railway creado"
echo ""
echo "🎯 Variables que necesitas configurar en Railway:"
echo ""
echo "Ve a https://railway.app/dashboard y selecciona tu proyecto"
echo "Ve a Variables y copia estas variables desde .env.railway:"
echo ""
echo "- SECRET_KEY"
echo "- ALLOWED_HOSTS"
echo "- CORS_ALLOWED_ORIGINS"
echo "- NEXT_PUBLIC_API_URL"
echo "- NEXT_PUBLIC_WS_URL"
echo "- NEXT_PUBLIC_DOMAIN"
echo "- DEEPSEEK_API_KEY"
echo "- DEBUG"
echo "- DJANGO_SETTINGS_MODULE"
echo ""
echo "Railway configura automáticamente:"
echo "- DATABASE_URL (PostgreSQL)"
echo "- REDIS_URL (Redis)"
echo ""
echo "📋 Próximos pasos:"
echo "1. Copia las variables de .env.railway al dashboard de Railway"
echo "2. Railway detectará automáticamente docker-compose.railway.yml"
echo "3. Haz clic en 'Deploy'"
echo "4. ¡Tu aplicación estará lista en $RAILWAY_URL!"
echo ""
echo "🔍 Para verificar:"
echo "- Frontend: $RAILWAY_URL"
echo "- Admin Django: $RAILWAY_URL/admin/"
echo "- API Health: $RAILWAY_URL/health/"
echo ""
echo "📞 Si hay problemas, revisa los logs en Railway dashboard"
