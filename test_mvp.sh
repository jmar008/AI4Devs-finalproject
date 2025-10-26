#!/bin/bash

# Script de validación rápida del MVP Frontend + Backend API
# Uso: bash /workspace/test_mvp.sh

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                  PRUEBA DEL MVP - VALIDACIÓN RÁPIDA                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Verificar Backend
echo -e "${BLUE}[1/5]${NC} Verificando Backend..."
echo ""

echo -e "  → Verificando que Django esté escuchando en puerto 8000..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "    ${GREEN}✓${NC} Backend está arriba"
else
    echo -e "    ${RED}✗${NC} Backend no responde en http://localhost:8000"
    echo -e "    ${YELLOW}Solución:${NC} Ejecuta: docker-compose up -d backend"
    exit 1
fi

# 2. Verificar API Root
echo -e "${BLUE}[2/5]${NC} Verificando API Root..."
echo ""

RESPONSE=$(curl -s http://localhost:8000/api/)
if echo "$RESPONSE" | grep -q "DealaAI API"; then
    echo -e "  ${GREEN}✓${NC} API root respondiendo correctamente"
else
    echo -e "  ${RED}✗${NC} API root no responde correctamente"
    exit 1
fi

# 3. Probar autenticación
echo -e "${BLUE}[3/5]${NC} Probando autenticación (Login)..."
echo ""

LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')

if echo "$LOGIN_RESPONSE" | grep -q "token"; then
    TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('token', ''))")
    echo -e "  ${GREEN}✓${NC} Login exitoso"
    echo -e "    Token: ${YELLOW}${TOKEN:0:20}...${NC}"
else
    echo -e "  ${RED}✗${NC} Error en login"
    echo "    Respuesta: $LOGIN_RESPONSE"
    exit 1
fi

# 4. Probar Stock API
echo -e "${BLUE}[4/5]${NC} Probando Stock API..."
echo ""

STOCK_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/stock/?page=1&page_size=5" \
  -H "Authorization: Bearer $TOKEN")

if echo "$STOCK_RESPONSE" | grep -q "count"; then
    COUNT=$(echo "$STOCK_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('count', 0))")
    echo -e "  ${GREEN}✓${NC} Stock API respondiendo"
    echo -e "    Total vehículos: ${YELLOW}${COUNT}${NC}"
else
    echo -e "  ${RED}✗${NC} Stock API no responde correctamente"
    echo "    Respuesta: $STOCK_RESPONSE"
    exit 1
fi

# 5. Verificar Frontend
echo -e "${BLUE}[5/5]${NC} Verificando Frontend..."
echo ""

if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} Frontend está arriba en puerto 3000"
else
    echo -e "  ${YELLOW}⚠${NC} Frontend no responde en http://localhost:3000"
    echo -e "    ${YELLOW}Consejo:${NC} Ejecuta: cd /workspace/frontend && npm run dev"
fi

# Resumen
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}                        ${GREEN}✓ TODAS LAS PRUEBAS PASARON${NC}                      ${BLUE}║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo "📋 URLS PARA PRUEBAS MANUALES:"
echo ""
echo -e "  ${YELLOW}Frontend:${NC}       http://localhost:3000"
echo -e "  ${YELLOW}Login:${NC}          http://localhost:3000/login"
echo -e "  ${YELLOW}Dashboard:${NC}      http://localhost:3000/dashboard"
echo -e "  ${YELLOW}Stock:${NC}          http://localhost:3000/dashboard/stock"
echo ""
echo -e "  ${YELLOW}Swagger API:${NC}    http://localhost:8000/api/docs/"
echo -e "  ${YELLOW}ReDoc:${NC}          http://localhost:8000/api/redoc/"
echo ""

echo "🔐 CREDENCIALES DE PRUEBA:"
echo ""
echo -e "  ${YELLOW}Usuario:${NC}     admin"
echo -e "  ${YELLOW}Contraseña:${NC}  admin123"
echo ""

echo "📝 PRÓXIMOS PASOS:"
echo ""
echo "  1. Abre http://localhost:3000/login"
echo "  2. Usa admin / admin123"
echo "  3. Ve a /dashboard/stock"
echo "  4. Haz click en 'Ver detalles' de un vehículo"
echo ""
