#!/bin/bash

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           🔧 VERIFICACIÓN DE FRONTEND - DealaAI               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "/workspace/frontend/package.json" ]; then
  echo -e "${RED}❌ Error: package.json no encontrado${NC}"
  exit 1
fi

cd /workspace/frontend

echo -e "${YELLOW}📋 VERIFICACIÓN 1: Componentes UI${NC}"
echo "────────────────────────────────────────────────────────────────"

COMPONENTS=(
  "components/ui/button.tsx"
  "components/ui/input.tsx"
  "components/ui/label.tsx"
  "components/ui/table.tsx"
  "components/ui/dropdown-menu.tsx"
  "components/ui/avatar.tsx"
  "components/ui/index.ts"
)

for component in "${COMPONENTS[@]}"; do
  if [ -f "$component" ]; then
    echo -e "${GREEN}✅${NC} $component"
  else
    echo -e "${RED}❌${NC} $component (NO ENCONTRADO)"
  fi
done

echo ""
echo -e "${YELLOW}📋 VERIFICACIÓN 2: Archivos Modificados${NC}"
echo "────────────────────────────────────────────────────────────────"

FILES_TO_CHECK=(
  "app/login/page.tsx"
  "app/dashboard/layout.tsx"
  "app/dashboard/page.tsx"
  "app/dashboard/stock/page.tsx"
  "components/Sidebar.tsx"
  "components/Topbar.tsx"
  "store/authStore.ts"
  "lib/api.ts"
  "middleware.ts"
)

for file in "${FILES_TO_CHECK[@]}"; do
  if [ -f "$file" ]; then
    echo -e "${GREEN}✅${NC} $file"
  else
    echo -e "${RED}❌${NC} $file (NO ENCONTRADO)"
  fi
done

echo ""
echo -e "${YELLOW}📋 VERIFICACIÓN 3: Importaciones Críticas${NC}"
echo "────────────────────────────────────────────────────────────────"

# Verificar que React está importado en button.tsx
if grep -q "import \* as React from 'react'" "components/ui/button.tsx"; then
  echo -e "${GREEN}✅${NC} React importado en button.tsx"
else
  echo -e "${RED}❌${NC} React NO importado en button.tsx"
fi

# Verificar que useAuthStore se exporta correctamente
if grep -q "export const useAuthStore = create" "store/authStore.ts"; then
  echo -e "${GREEN}✅${NC} useAuthStore exportado correctamente"
else
  echo -e "${RED}❌${NC} useAuthStore NO exportado correctamente"
fi

# Verificar que globals.css no importa Google Fonts
if grep -q "^/\* Google Fonts" "app/globals.css"; then
  echo -e "${GREEN}✅${NC} Google Fonts comentadas en globals.css"
else
  echo -e "${RED}❌${NC} Google Fonts aún importadas (puede fallar)"
fi

echo ""
echo -e "${YELLOW}📋 VERIFICACIÓN 4: Dependencias Instaladas${NC}"
echo "────────────────────────────────────────────────────────────────"

DEPS=(
  "react"
  "next"
  "typescript"
  "zustand"
  "react-hook-form"
  "@radix-ui/react-avatar"
  "@radix-ui/react-dropdown-menu"
  "tailwindcss"
  "class-variance-authority"
  "clsx"
  "tailwind-merge"
)

for dep in "${DEPS[@]}"; do
  if npm list "$dep" >/dev/null 2>&1; then
    VERSION=$(npm list "$dep" 2>/dev/null | grep -oP "(?<=$dep@)\d+\.\d+\.\d+" | head -1)
    echo -e "${GREEN}✅${NC} $dep@$VERSION"
  else
    echo -e "${RED}❌${NC} $dep (NO INSTALADA)"
  fi
done

echo ""
echo -e "${YELLOW}📋 VERIFICACIÓN 5: Configuración${NC}"
echo "────────────────────────────────────────────────────────────────"

# Verificar next.config.js
if grep -q 'experimental.*appDir' "next.config.js"; then
  echo -e "${RED}❌${NC} next.config.js aún tiene appDir (deprecated)"
else
  echo -e "${GREEN}✅${NC} next.config.js sin appDir deprecated"
fi

# Verificar tsconfig.json
if [ -f "tsconfig.json" ]; then
  echo -e "${GREEN}✅${NC} tsconfig.json existe"
else
  echo -e "${RED}❌${NC} tsconfig.json NO encontrado"
fi

echo ""
echo -e "${YELLOW}📋 VERIFICACIÓN 6: Build${NC}"
echo "────────────────────────────────────────────────────────────────"

echo "🔨 Compilando frontend (esto toma ~30-60 segundos)..."
if npm run build 2>&1 | tee /tmp/build.log | tail -5 | grep -q "compiled successfully\|Build complete"; then
  echo -e "${GREEN}✅${NC} Frontend compilado exitosamente"
else
  ERRORS=$(grep -c "error" /tmp/build.log)
  if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}❌${NC} Frontend tiene $ERRORS errores de compilación"
    echo ""
    echo -e "${RED}ERRORES ENCONTRADOS:${NC}"
    grep "error" /tmp/build.log | head -10
  else
    echo -e "${YELLOW}⚠️${NC} No se pudo determinar el estado de compilación"
  fi
fi

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                  ✅ VERIFICACIÓN COMPLETADA                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"

echo ""
echo -e "${GREEN}Próximos Pasos:${NC}"
echo "1. Inicia el servidor: npm run dev"
echo "2. Abre http://localhost:3000/login en tu navegador"
echo "3. Login con admin/admin123"
echo "4. Navega por el dashboard"
echo ""
