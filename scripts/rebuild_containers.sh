#!/bin/bash

# Script para reconstruir y reiniciar los contenedores con las nuevas dependencias
# Ejecutar después de cambiar requirements.txt

echo "🔨 Reconstruyendo contenedores Docker..."
echo ""

# Detener contenedores
echo "1️⃣ Deteniendo contenedores..."
docker-compose down

# Reconstruir backend (donde está openai)
echo ""
echo "2️⃣ Reconstruyendo backend con nuevas dependencias..."
docker-compose build --no-cache backend

# Reconstruir workers de Celery (usan el mismo requirements.txt)
echo ""
echo "3️⃣ Reconstruyendo workers..."
docker-compose build --no-cache celery_worker celery_beat

# Iniciar todos los servicios
echo ""
echo "4️⃣ Iniciando todos los servicios..."
docker-compose up -d

# Mostrar logs del backend
echo ""
echo "5️⃣ Logs del backend:"
docker-compose logs -f backend

echo ""
echo "✅ ¡Contenedores reconstruidos y en ejecución!"
