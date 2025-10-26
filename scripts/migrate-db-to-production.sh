#!/bin/bash

# ============================================================================
# Script de Migración de Base de Datos de Desarrollo a Producción
# ============================================================================
#
# Este script realiza un backup de la base de datos de DESARROLLO
# y la restaura en PRODUCCIÓN (EasyPanel)
#
# IMPORTANTE: Este script asume que:
# 1. Docker está corriendo localmente
# 2. Tienes acceso SSH a tu servidor de producción (EasyPanel)
# 3. Las variables de entorno están configuradas
#
# ============================================================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones auxiliares
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Variables de desarrollo (local)
DEV_DB_NAME="dealaai_dev"
DEV_DB_USER="postgres"
DEV_DB_PASSWORD="postgres"
DEV_DB_HOST="localhost"
DEV_DB_PORT="5432"
DEV_CONTAINER="dealaai_db"

# Variables de producción (EasyPanel)
PROD_SERVER="mcp.jorgemg.es"
PROD_SSH_USER="root"  # O el usuario que uses
PROD_DB_NAME="dealaai_prod"
PROD_DB_USER="postgres"
PROD_DB_PASSWORD="${DB_PASSWORD}"  # Debe estar en variables de entorno
PROD_DB_HOST="db"  # Nombre del contenedor en docker-compose
PROD_CONTAINER="dealaai_db_prod"

# Rutas
BACKUP_DIR="/workspace/database/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/backup_dev_${TIMESTAMP}.sql"
BACKUP_FILE_COMPRESSED="${BACKUP_DIR}/backup_dev_${TIMESTAMP}.sql.gz"

# ============================================================================
# VALIDACIONES INICIALES
# ============================================================================

print_header "Validaciones Iniciales"

# Verificar que docker está corriendo
if ! docker ps > /dev/null 2>&1; then
    print_error "Docker no está corriendo o no tienes permisos"
    exit 1
fi
print_success "Docker está corriendo"

# Verificar que el contenedor de BD de desarrollo existe
if ! docker ps -a | grep -q "$DEV_CONTAINER"; then
    print_error "Contenedor $DEV_CONTAINER no encontrado"
    print_warning "Ejecuta primero: docker-compose up -d db"
    exit 1
fi
print_success "Contenedor de desarrollo encontrado"

# Verificar que el contenedor de BD está corriendo
if ! docker ps | grep -q "$DEV_CONTAINER"; then
    print_warning "Contenedor $DEV_CONTAINER no está corriendo. Iniciando..."
    docker-compose up -d db
    sleep 5
fi
print_success "Contenedor de desarrollo está corriendo"

# Crear directorio de backups si no existe
mkdir -p "$BACKUP_DIR"
print_success "Directorio de backups: $BACKUP_DIR"

# ============================================================================
# PASO 1: CREAR BACKUP DE BASE DE DATOS DE DESARROLLO
# ============================================================================

print_header "Paso 1: Crear Backup de Base de Datos de Desarrollo"

echo "Backup from: $DEV_DB_NAME@$DEV_DB_HOST:$DEV_DB_PORT"
echo "Backup file: $BACKUP_FILE"

# Exportar la base de datos completa (sin roles, solo datos y esquema)
docker exec $DEV_CONTAINER pg_dump \
    -U $DEV_DB_USER \
    -h $DEV_DB_HOST \
    -p $DEV_DB_PORT \
    -d $DEV_DB_NAME \
    --no-privileges \
    --no-owner \
    --no-role-properties \
    --format=plain \
    > "$BACKUP_FILE"

if [ -f "$BACKUP_FILE" ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    print_success "Backup creado correctamente ($SIZE)"

    # Comprimir el backup
    gzip -f "$BACKUP_FILE"
    SIZE_COMPRESSED=$(du -h "$BACKUP_FILE_COMPRESSED" | cut -f1)
    print_success "Backup comprimido ($SIZE_COMPRESSED)"
else
    print_error "Error al crear el backup"
    exit 1
fi

# ============================================================================
# PASO 2: VALIDAR BACKUP
# ============================================================================

print_header "Paso 2: Validar Backup"

# Contar tablas en el backup
TABLE_COUNT=$(zcat "$BACKUP_FILE_COMPRESSED" | grep "CREATE TABLE" | wc -l)
print_success "Tablas encontradas en backup: $TABLE_COUNT"

if [ $TABLE_COUNT -eq 0 ]; then
    print_warning "No se encontraron tablas en el backup. ¿La BD está vacía?"
fi

# ============================================================================
# PASO 3: PREPARAR ARCHIVO PARA PRODUCCIÓN
# ============================================================================

print_header "Paso 3: Preparar Archivo para Producción"

# Descomprimir para procesar
BACKUP_FILE_UNCOMPRESSED="${BACKUP_DIR}/backup_dev_${TIMESTAMP}_uncompressed.sql"
gunzip -c "$BACKUP_FILE_COMPRESSED" > "$BACKUP_FILE_UNCOMPRESSED"

print_success "Backup descomprimido para procesamiento"

# ============================================================================
# PASO 4: SUBIR A PRODUCCIÓN
# ============================================================================

print_header "Paso 4: Subir Backup a Producción"

# Verificar conectividad SSH
if ! ssh -o ConnectTimeout=5 "${PROD_SSH_USER}@${PROD_SERVER}" "echo 'SSH OK'" > /dev/null 2>&1; then
    print_error "No se puede conectar a ${PROD_SSH_USER}@${PROD_SERVER} por SSH"
    print_warning "Verifica que:"
    print_warning "  1. Tu clave SSH está configurada"
    print_warning "  2. El servidor es accesible desde tu red"
    print_warning "  3. El usuario es correcto"
    echo ""
    echo "Alternativa: Sube el archivo manualmente a producción"
    echo "Archivo local: $BACKUP_FILE_UNCOMPRESSED"
    echo ""
    exit 1
fi

print_success "Conexión SSH verificada"

# Crear directorio en servidor remoto
ssh "${PROD_SSH_USER}@${PROD_SERVER}" "mkdir -p /opt/easypanel/projects/dealaai/backups || mkdir -p ~/backups"

# Copiar archivo
print_warning "Subiendo archivo (~${SIZE})... esto puede tomar un tiempo"
scp -C "$BACKUP_FILE_UNCOMPRESSED" "${PROD_SSH_USER}@${PROD_SERVER}:/opt/easypanel/projects/dealaai/backups/" || \
    scp -C "$BACKUP_FILE_UNCOMPRESSED" "${PROD_SSH_USER}@${PROD_SERVER}:~/backups/"

print_success "Archivo subido a producción"

# ============================================================================
# PASO 5: RESTAURAR EN PRODUCCIÓN
# ============================================================================

print_header "Paso 5: Restaurar en Producción"

# Crear script de restauración para ejecutar en servidor
RESTORE_SCRIPT="/tmp/restore_${TIMESTAMP}.sh"

cat > "$RESTORE_SCRIPT" << 'EOF'
#!/bin/bash
set -e

PROD_CONTAINER="dealaai_db_prod"
BACKUP_FILE="$1"
DB_PASSWORD="$2"
DB_NAME="$3"
DB_USER="$4"

echo "Restaurando base de datos en producción..."

# Asegurar que el archivo existe
if [ ! -f "$BACKUP_FILE" ]; then
    echo "✗ Archivo de backup no encontrado: $BACKUP_FILE"
    exit 1
fi

echo "Archivo encontrado: $BACKUP_FILE"

# Limpiar base de datos existente (CUIDADO: Esto elimina todos los datos)
echo "Limpiando base de datos existente..."
docker exec "$PROD_CONTAINER" psql -U "$DB_USER" -d postgres << SQL
DROP DATABASE IF EXISTS "$DB_NAME";
CREATE DATABASE "$DB_NAME" OWNER "$DB_USER";
EOF

echo "✓ Base de datos limpiada"

# Restaurar desde backup
echo "Restaurando datos..."
docker exec -i "$PROD_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" < "$BACKUP_FILE"

echo "✓ Base de datos restaurada correctamente"

# Verificar
TABLES=$(docker exec "$PROD_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" | tail -1)
echo "✓ Tablas en BD: $TABLES"

EOF

chmod +x "$RESTORE_SCRIPT"

# Ejecutar script de restauración en servidor remoto
print_warning "Ejecutando restauración en producción (esto puede tomar varios minutos)..."

REMOTE_BACKUP="/opt/easypanel/projects/dealaai/backups/backup_dev_${TIMESTAMP}_uncompressed.sql"
[ ! -f "/opt/easypanel/projects/dealaai/backups/backup_dev_${TIMESTAMP}_uncompressed.sql" ] && \
    REMOTE_BACKUP="${PROD_SSH_USER}@${PROD_SERVER}:~/backups/backup_dev_${TIMESTAMP}_uncompressed.sql"

ssh "${PROD_SSH_USER}@${PROD_SERVER}" << "EOF"
#!/bin/bash
set -e

PROD_CONTAINER="dealaai_db_prod"
BACKUP_FILE="$(find /opt/easypanel/projects/dealaai/backups -name 'backup_dev_*_uncompressed.sql' -type f | sort -r | head -1)" || \
BACKUP_FILE="$(find ~ -name 'backup_dev_*_uncompressed.sql' -type f | sort -r | head -1)"
DB_PASSWORD="${DB_PASSWORD}"
DB_NAME="dealaai_prod"
DB_USER="postgres"

if [ -z "$BACKUP_FILE" ]; then
    echo "✗ No se encontró archivo de backup"
    exit 1
fi

echo "Limpiando base de datos existente..."
docker exec "$PROD_CONTAINER" psql -U "$DB_USER" -c "DROP DATABASE IF EXISTS \"$DB_NAME\";" || true
docker exec "$PROD_CONTAINER" psql -U "$DB_USER" -c "CREATE DATABASE \"$DB_NAME\" OWNER \"$DB_USER\";"

echo "Restaurando desde: $BACKUP_FILE"
docker exec -i "$PROD_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" < "$BACKUP_FILE"

echo "✓ Base de datos restaurada correctamente"

TABLES=$(docker exec "$PROD_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" | tail -1)
echo "✓ Tablas en BD: $TABLES"

EOF

print_success "Restauración completada"

# ============================================================================
# PASO 6: VERIFICACIÓN FINAL
# ============================================================================

print_header "Paso 6: Verificación Final"

print_warning "Verificando en producción..."
ssh "${PROD_SSH_USER}@${PROD_SERVER}" << "EOF"
echo "Verificando contenedores..."
docker ps | grep -E "db|backend|frontend"

echo ""
echo "Verificando tablas de BD..."
docker exec dealaai_db_prod psql -U postgres -d dealaai_prod -c "\dt public.*" | head -20

EOF

print_success "Verificación completada"

# ============================================================================
# RESUMEN
# ============================================================================

print_header "Resumen"

echo "Base de datos exportada: $BACKUP_FILE_COMPRESSED"
echo "Base de datos sin comprimir: $BACKUP_FILE_UNCOMPRESSED"
echo ""
echo "Próximos pasos:"
echo "  1. Verificar que todos los datos están correctos en producción"
echo "  2. Hacer pruebas en los endpoints de API"
echo "  3. Limpiar archivos de backup antiguos: rm $BACKUP_DIR/backup_dev_*"
echo ""

print_success "¡Migración completada exitosamente!"

# Limpiar
rm "$RESTORE_SCRIPT"

