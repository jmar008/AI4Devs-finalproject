#!/bin/bash

# ============================================================================
# Script Simple: Exportar BD de Desarrollo para Migración Manual
# ============================================================================
#
# Si no tienes SSH configurado o prefieres hacerlo manualmente,
# este script crea un backup que puedes subir manualmente a EasyPanel
#
# ============================================================================

set -e

# Colores
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

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

print_header "Exportar Base de Datos de Desarrollo"

DEV_DB_NAME="dealaai_dev"
DEV_DB_USER="postgres"
DEV_DB_PASSWORD="postgres"
DEV_CONTAINER="dealaai_db"

BACKUP_DIR="/workspace/database/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/db_development_${TIMESTAMP}.sql"

# Crear directorio
mkdir -p "$BACKUP_DIR"

# ============================================================================
# PASO 1: VERIFICAR CONTENEDOR
# ============================================================================

print_header "Verificar Contenedor"

if ! docker ps | grep -q "$DEV_CONTAINER"; then
    print_warning "Contenedor no está corriendo, iniciando..."
    docker-compose up -d db
    sleep 5
fi

print_success "Contenedor está corriendo"

# ============================================================================
# PASO 2: CREAR BACKUP
# ============================================================================

print_header "Crear Backup de Desarrollo"

docker exec $DEV_CONTAINER pg_dump \
    -U $DEV_DB_USER \
    -d $DEV_DB_NAME \
    --no-privileges \
    --no-owner \
    > "$BACKUP_FILE"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "✗ Error al crear backup"
    exit 1
fi

SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
print_success "Backup creado: $BACKUP_FILE ($SIZE)"

# ============================================================================
# PASO 3: INFORMACIÓN IMPORTANTE
# ============================================================================

print_header "Próximos Pasos"

cat << EOF

📋 INSTRUCCIONES DE MIGRACIÓN MANUAL A EASYPANEL

1️⃣ DESCARGAR EL BACKUP
   Archivo local: $BACKUP_FILE

   Opciones:
   a) En VS Code: Click derecho en el archivo → "Download"
   b) Por SCP: scp -r /workspace/database/backups user@tu-máquina:/ruta/local
   c) Por terminal:
      cat $BACKUP_FILE | gzip > database_backup.sql.gz

2️⃣ SUBIR A PRODUCCIÓN (EasyPanel)

   Option A: Via SSH
   ───────────────
   scp $BACKUP_FILE root@mcp.jorgemg.es:/opt/easypanel/projects/dealaai/backups/

   Option B: Via SFTP (Filezilla, WinSCP, etc.)
   ─────────────────────────────────────────
   Server: mcp.jorgemg.es
   Port: 22
   User: root
   Upload to: /opt/easypanel/projects/dealaai/backups/

3️⃣ RESTAURAR EN PRODUCCIÓN (En tu servidor)

   Conectarse por SSH:
   ssh root@mcp.jorgemg.es

   Ejecutar estos comandos:
   ────────────────────────
   BACKUP_FILE="/opt/easypanel/projects/dealaai/backups/db_development_${TIMESTAMP}.sql"

   # Limpiar BD existente
   docker exec dealaai_db_prod psql -U postgres -c "DROP DATABASE IF EXISTS dealaai_prod;"
   docker exec dealaai_db_prod psql -U postgres -c "CREATE DATABASE dealaai_prod OWNER postgres;"

   # Restaurar datos
   docker exec -i dealaai_db_prod psql -U postgres -d dealaai_prod < "\$BACKUP_FILE"

   # Verificar
   docker exec dealaai_db_prod psql -U postgres -d dealaai_prod -c "\\dt"

4️⃣ REINICIAR SERVICIOS (En EasyPanel)

   docker-compose -f docker-compose.production.yml restart backend

5️⃣ VERIFICAR

   Endpoint de health:
   curl https://mcp.jorgemg.es/api/health/

   Debe responder: {"status": "healthy", "database": "healthy"}

═══════════════════════════════════════════════════════════════════

📊 INFORMACIÓN DEL BACKUP

Archivo: $BACKUP_FILE
Tamaño: $SIZE
Contenedor: $DEV_CONTAINER
BD: $DEV_DB_NAME
Usuario: $DEV_DB_USER
Timestamp: $TIMESTAMP

═══════════════════════════════════════════════════════════════════

⚠️ IMPORTANTE

• Este backup incluye TODOS los datos de desarrollo
• No incluye roles de usuario (para evitar conflictos)
• Asegúrate de tener espacios en disco en producción
• Haz un backup de la BD de producción ANTES de restaurar
• Después de restaurar, ejecuta migraciones:
  docker-compose exec backend python manage.py migrate

═══════════════════════════════════════════════════════════════════

EOF

# ============================================================================
# PASO 4: CREAR VERSIÓN COMPRIMIDA
# ============================================================================

print_header "Crear Versión Comprimida"

BACKUP_COMPRESSED="${BACKUP_FILE}.gz"
gzip -k "$BACKUP_FILE"  # -k: mantener original
SIZE_COMPRESSED=$(du -h "$BACKUP_COMPRESSED" | cut -f1)

print_success "Backup comprimido: $BACKUP_COMPRESSED ($SIZE_COMPRESSED)"

echo ""
echo "Tienes dos opciones para transferir:"
echo "  1. Sin comprimir (más lento): $(basename "$BACKUP_FILE") ($SIZE)"
echo "  2. Comprimido (recomendado): $(basename "$BACKUP_COMPRESSED") ($SIZE_COMPRESSED)"

