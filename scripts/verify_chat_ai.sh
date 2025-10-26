#!/bin/bash

# Script de verificación del Chat AI
# Ejecutar desde la raíz del proyecto

echo "🔍 Verificando implementación del Chat AI..."
echo ""

# Verificar archivos backend
echo "📁 Backend Files:"
files=(
    "backend/apps/ai_chat/__init__.py"
    "backend/apps/ai_chat/models.py"
    "backend/apps/ai_chat/views.py"
    "backend/apps/ai_chat/serializers.py"
    "backend/apps/ai_chat/services.py"
    "backend/apps/ai_chat/deepseek_service.py"
    "backend/apps/ai_chat/urls.py"
    "backend/apps/ai_chat/admin.py"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING"
    fi
done

echo ""
echo "📁 Frontend Files:"
frontend_files=(
    "frontend/store/chatStore.ts"
    "frontend/lib/chatAPI.ts"
    "frontend/components/ChatWidget.tsx"
)

for file in "${frontend_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING"
    fi
done

echo ""
echo "🔧 Configuración:"

# Verificar dependencia en requirements.txt
if grep -q "openai" backend/requirements.txt; then
    echo "  ✅ openai en requirements.txt"
else
    echo "  ❌ openai NO está en requirements.txt"
fi

# Verificar app en INSTALLED_APPS
if grep -q "apps.ai_chat" backend/dealaai/settings/base.py; then
    echo "  ✅ ai_chat en INSTALLED_APPS"
else
    echo "  ❌ ai_chat NO está en INSTALLED_APPS"
fi

# Verificar URLs
if grep -q "ai_chat.urls" backend/dealaai/urls.py; then
    echo "  ✅ URLs del chat configuradas"
else
    echo "  ❌ URLs del chat NO configuradas"
fi

echo ""
echo "🔑 Variables de Entorno:"

if [ -f "backend/.env" ]; then
    if grep -q "DEEPSEEK_API_KEY" backend/.env; then
        echo "  ✅ DEEPSEEK_API_KEY encontrada en .env"
        # Verificar si tiene valor
        if grep "DEEPSEEK_API_KEY=sk-" backend/.env > /dev/null; then
            echo "  ✅ DEEPSEEK_API_KEY parece válida"
        else
            echo "  ⚠️  DEEPSEEK_API_KEY necesita configurarse"
        fi
    else
        echo "  ❌ DEEPSEEK_API_KEY NO está en .env"
    fi
else
    echo "  ⚠️  Archivo .env no encontrado"
fi

echo ""
echo "📊 Próximos pasos:"
echo "  1. Configura DEEPSEEK_API_KEY en backend/.env"
echo "  2. Instala dependencias: cd backend && pip install -r requirements.txt"
echo "  3. Ejecuta migraciones: python manage.py makemigrations ai_chat"
echo "  4. Aplica migraciones: python manage.py migrate"
echo "  5. Inicia el servidor: python manage.py runserver"
echo "  6. Inicia el frontend: cd frontend && npm run dev"
echo ""
echo "✨ ¡Todo listo para usar el Chat AI!"
