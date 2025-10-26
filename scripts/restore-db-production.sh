#!/bin/bash

# ============================================================================
# Script de Restauración para Ejecutar en Servidor de Producción (EasyPanel)
# ============================================================================
#
# Este script se ejecuta EN EL SERVIDOR de producción
# Usa para restaurar un backup descargado/subido manualmente
#
# Uso:
#   chmod +x restore-db-production.sh
#   ./restore-db-production.sh /ruta/al/backup.sql
#
# ============================================================================

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# ============================================================================
# VALIDACIONES
# ============================================================================

print_header "Validaciones"

if [ $# -ne 1 ]; then
    print_error "Uso: $0 /ruta/al/backup.sql"
    echo ""
    echo "Ejemplo:"
    echo "  $0 /opt/easypanel/projects/dealaai/backups/db_development_20251026_120000.sql"
    exit 1
fi

BACKUP_FILE="$1"

# Verificar archivo
if [ ! -f "$BACKUP_FILE" ]; then
    print_error "Archivo no encontrado: $BACKUP_FILE"
    exit 1
fi

print_success "Archivo encontrado"

# Verificar permisos
if [ ! -r "$BACKUP_FILE" ]; then
    print_error "No tienes permisos de lectura en: $BACKUP_FILE"
    exit 1
fi

print_success "Archivo es legible"

# ============================================================================
# INFORMACIÓN DEL BACKUP
# ============================================================================

print_header "Información del Backup"

SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
TABLES=$(grep -c "CREATE TABLE" "$BACKUP_FILE" || echo "0")
LINES=$(wc -l < "$BACKUP_FILE")

echo "Archivo: $BACKUP_FILE"
echo "Tamaño: $SIZE"
echo "Líneas: $LINES"
echo "Tablas (estimado): $TABLES"

# ============================================================================
# CONFIRMACIÓN
# ============================================================================

print_header "⚠️  CONFIRMACIÓN"

cat << EOF
🚨 ATENCIÓN - OPERACIÓN DESTRUCTIVA 🚨

Esta operación va a:
1. ELIMINAR todos los datos de la BD actual (dealaai_prod)
2. RESTAURAR los datos del backup

${RED}No se puede deshacer.${NC}

¿Estás seguro? Escribe 'SI RESTAURAR' para continuar:
EOF

read -p "> " CONFIRM

if [ "$CONFIRM" != "SI RESTAURAR" ]; then
    print_warning "Operación cancelada"
    exit 1
fi

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

PROD_CONTAINER="dealaai_db_prod"
DB_NAME="dealaai_prod"
DB_USER="postgres"

# Intentar obtener password de variables de entorno
if [ -z "$DB_PASSWORD" ]; then
    print_warning "DB_PASSWORD no está definido. Usando contraseña por defecto."
    DB_PASSWORD="postgres"  # Por defecto en desarrollo, cambiar en producción
fi

# ============================================================================
# PASO 1: VERIFICAR CONTENEDOR
# ============================================================================

print_header "Paso 1: Verificar Contenedor"

if ! docker ps | grep -q "$PROD_CONTAINER"; then
    print_error "Contenedor $PROD_CONTAINER no está corriendo"
    echo ""
    echo "Inicia los servicios con:"
    echo "  docker-compose up -d"
    exit 1
fi

print_success "Contenedor está corriendo"

# ============================================================================
# PASO 2: PRUEBA DE CONECTIVIDAD
# ============================================================================

print_header "Paso 2: Prueba de Conectividad"

if ! docker exec "$PROD_CONTAINER" psql -U "$DB_USER" -c "SELECT 1;" > /dev/null 2>&1; then
    print_error "No se puede conectar a PostgreSQL"
    exit 1
fi

print_success "Conexión a PostgreSQL establecida"

# ============================================================================
# PASO 3: CREAR BACKUP PREVIO
# ============================================================================

print_header "Paso 3: Crear Backup de Seguridad de BD Actual"

CURRENT_BACKUP="/opt/easypanel/projects/dealaai/backups/db_production_backup_$(date +%Y%m%d_%H%M%S).sql"
mkdir -p "$(dirname "$CURRENT_BACKUP")" 2>/dev/null || mkdir -p ~/backups
CURRENT_BACKUP="${CURRENT_BACKUP:-~/backups/db_production_backup_$(date +%Y%m%d_%H%M%S).sql}"

docker exec "$PROD_CONTAINER" pg_dump \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    > "$CURRENT_BACKUP" 2>/dev/null || true

if [ -f "$CURRENT_BACKUP" ]; then
    SIZE_BACKUP=$(du -h "$CURRENT_BACKUP" | cut -f1)
    print_success "Backup previo creado: $CURRENT_BACKUP ($SIZE_BACKUP)"
else
    print_warning "No se pudo crear backup previo (BD puede estar vacía)"
fi

# ============================================================================
# PASO 4: LIMPIAR BD
# ============================================================================

print_header "Paso 4: Limpiar Base de Datos"

print_warning "Eliminando BD existente..."
docker exec "$PROD_CONTAINER" psql -U "$DB_USER" -c "DROP DATABASE IF EXISTS \"$DB_NAME\";" || true

print_success "Base de datos eliminada"

# Crear BD nueva
print_warning "Creando BD nueva..."
docker exec "$PROD_CONTAINER" psql -U "$DB_USER" -c "CREATE DATABASE \"$DB_NAME\" OWNER \"$DB_USER\";"

print_success "Base de datos creada"

# ============================================================================
# PASO 5: RESTAURAR BACKUP
# ============================================================================

print_header "Paso 5: Restaurar Datos (esto puede tomar tiempo...)"

if docker exec -i "$PROD_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" < "$BACKUP_FILE"; then
    print_success "Base de datos restaurada correctamente"
else
    print_error "Error al restaurar la base de datos"
    print_error "Intenta restaurar manualmente:"
    echo "  psql -U postgres -d $DB_NAME < $BACKUP_FILE"
    exit 1
fi

# ============================================================================
# PASO 6: VERIFICACIÓN
# ============================================================================

print_header "Paso 6: Verificación"

# Contar tablas
RESTORED_TABLES=$(docker exec "$PROD_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c \
    "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" \
    2>/dev/null | grep -o '[0-9]*' | tail -1)

print_success "Tablas restauradas: $RESTORED_TABLES"

# Contar registros de usuarios (si existen)
USERS=$(docker exec "$PROD_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c \
    "SELECT count(*) FROM auth_user WHERE 1=1;" 2>/dev/null | grep -o '[0-9]*' | tail -1) || USERS="N/A"

echo "Usuarios: $USERS"

# ============================================================================
# PASO 7: EJECUTAR MIGRACIONES
# ============================================================================

print_header "Paso 7: Ejecutar Migraciones de Django"

BACKEND_CONTAINER="dealaai_backend_prod"

if docker ps | grep -q "$BACKEND_CONTAINER"; then
    print_warning "Ejecutando migraciones..."

    if docker exec "$BACKEND_CONTAINER" python manage.py migrate --noinput; then
        print_success "Migraciones ejecutadas correctamente"
    else
        print_warning "Migraciones completadas con advertencias"
    fi
else
    print_warning "Contenedor backend no está corriendo"
    echo "Ejecuta migraciones manualmente:"
    echo "  docker exec $BACKEND_CONTAINER python manage.py migrate --noinput"
fi

# ============================================================================
# PASO 8: REINICIAR SERVICIOS
# ============================================================================

print_header "Paso 8: Reiniciar Servicios"

print_warning "Reiniciando backend..."
docker-compose -f docker-compose.production.yml restart backend 2>/dev/null || \
    docker restart "$BACKEND_CONTAINER" || true

sleep 5

print_success "Servicios reiniciados"

# ============================================================================
# RESUMEN
# ============================================================================

print_header "✅ Restauración Completada"

cat << EOF

📊 Resumen:
  • Base de datos: $DB_NAME
  • Tablas restauradas: $RESTORED_TABLES
  • Usuarios importados: $USERS
  • Backup previo: $(basename "$CURRENT_BACKUP")

🔍 Verificación:

Prueba de conectividad:
  docker exec dealaai_backend_prod python manage.py dbshell

Verificar tablas:
  docker exec dealaai_db_prod psql -U postgres -d $DB_NAME -c "\\dt"

Prueba de API:
  curl https://mcp.jorgemg.es/api/health/

📝 Próximos Pasos:
  1. Verificar que los datos se ven correctamente en API
  2. Probar login con usuarios importados
  3. Revisar logs: docker-compose logs backend
  4. Validar integridad de datos

⚠️  En caso de problemas:
  Restaurar desde backup previo:
  docker exec -i dealaai_db_prod psql -U postgres -d $DB_NAME < "$CURRENT_BACKUP"

EOF

