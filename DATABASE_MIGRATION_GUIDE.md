# 📊 Migración de Base de Datos - Desarrollo a Producción

**Fecha:** 26 Oct 2025  
**Objetivo:** Migrar BD de desarrollo (dealaai_dev) a producción (dealaai_prod)

---

## 🚀 Inicio Rápido

Si tienes SSH configurado y urgencia:

```bash
cd /workspace
chmod +x scripts/migrate-db-to-production.sh
./scripts/migrate-db-to-production.sh
```

Si prefieres hacerlo manualmente o no tienes SSH:

```bash
cd /workspace
chmod +x scripts/export-db-for-migration.sh
./scripts/export-db-for-migration.sh
```

---

## 📋 Opción 1: Migración Automática (Recomendada)

### Requisitos

- ✅ Docker corriendo localmente
- ✅ SSH configurado a `mcp.jorgemg.es`
- ✅ Variable de entorno `DB_PASSWORD` configurada

### Pasos

#### 1. Verificar Conectividad SSH

```bash
ssh root@mcp.jorgemg.es "echo 'SSH OK'"
```

#### 2. Ejecutar Script de Migración

```bash
cd /workspace
chmod +x scripts/migrate-db-to-production.sh
./scripts/migrate-db-to-production.sh
```

#### 3. Ver Progreso

El script mostrará:

```
=== Validaciones Iniciales ===
✓ Docker está corriendo
✓ Contenedor de desarrollo encontrado
✓ Contenedor de desarrollo está corriendo

=== Paso 1: Crear Backup de Base de Datos de Desarrollo ===
✓ Backup creado correctamente (45MB)
✓ Backup comprimido (12MB)

=== Paso 2: Validar Backup ===
✓ Tablas encontradas en backup: 23

=== Paso 3: Preparar Archivo para Producción ===
✓ Backup descomprimido para procesamiento

=== Paso 4: Subir Backup a Producción ===
Subiendo archivo (~45MB)... esto puede tomar un tiempo
✓ Archivo subido a producción

=== Paso 5: Restaurar en Producción ===
✓ Restauración completada

=== Paso 6: Verificación Final ===
✓ Verificación completada

=== Resumen ===
✓ ¡Migración completada exitosamente!
```

---

## 📋 Opción 2: Migración Manual (Sin SSH)

### Paso 1: Exportar Base de Datos

```bash
cd /workspace
chmod +x scripts/export-db-for-migration.sh
./scripts/export-db-for-migration.sh
```

Esto crea un archivo en:

```
/workspace/database/backups/db_development_YYYYMMDD_HHMMSS.sql
```

### Paso 2: Descargar el Archivo

**Opción A: Desde VS Code**

1. Click derecho en `/workspace/database/backups/`
2. Selecciona "Download"

**Opción B: Desde terminal**

```bash
# Si estás en local
scp -r user@dev-container:/workspace/database/backups/db_development*.sql ~/Downloads/

# O comprimir primero (más rápido)
cd /workspace/database/backups
gzip -k db_development_*.sql
```

### Paso 3: Subir a Producción (EasyPanel)

**Opción A: Via SFTP (Interfaz gráfica)**

- Usar FileZilla, WinSCP o Cyberduck
- Conectar a: `mcp.jorgemg.es`
- Subir a: `/opt/easypanel/projects/dealaai/backups/`

**Opción B: Via SCP**

```bash
scp ~/Downloads/db_development_*.sql root@mcp.jorgemg.es:/opt/easypanel/projects/dealaai/backups/
```

**Opción C: Via SSH + cat**

```bash
ssh root@mcp.jorgemg.es << 'EOF'
cat > /opt/easypanel/projects/dealaai/backups/db_development.sql << 'BACKUP'
# Pegar aquí el contenido del archivo SQL
BACKUP
EOF
```

### Paso 4: Conectarse al Servidor

```bash
ssh root@mcp.jorgemg.es
```

### Paso 5: Restaurar Backup en Producción

Copiar el script de restauración:

```bash
# Desde tu máquina local
scp /workspace/scripts/restore-db-production.sh root@mcp.jorgemg.es:~/

# O desde el servidor, descargar el script:
cd ~
wget https://raw.githubusercontent.com/tu-repo/main/scripts/restore-db-production.sh
```

Ejecutar restauración:

```bash
chmod +x ~/restore-db-production.sh
~/restore-db-production.sh /opt/easypanel/projects/dealaai/backups/db_development_*.sql
```

O hacerlo manualmente (sin script):

```bash
# Variables
BACKUP_FILE="/opt/easypanel/projects/dealaai/backups/db_development_*.sql"
CONTAINER="dealaai_db_prod"
DB_NAME="dealaai_prod"
DB_USER="postgres"

# Eliminar BD existente (CUIDADO!)
docker exec $CONTAINER psql -U $DB_USER -c "DROP DATABASE IF EXISTS \"$DB_NAME\";"

# Crear BD nueva
docker exec $CONTAINER psql -U $DB_USER -c "CREATE DATABASE \"$DB_NAME\" OWNER \"$DB_USER\";"

# Restaurar datos
docker exec -i $CONTAINER psql -U $DB_USER -d $DB_NAME < $BACKUP_FILE

# Verificar
docker exec $CONTAINER psql -U $DB_USER -d $DB_NAME -c "\dt"

# Ejecutar migraciones
docker exec dealaai_backend_prod python manage.py migrate --noinput

# Reiniciar servicios
docker-compose -f docker-compose.production.yml restart backend
```

---

## 🔍 Verificación Post-Migración

### 1. Verificar Contenedores

```bash
# En servidor de producción
docker ps

# Todos deben estar (healthy)
# dealaai_db_prod        healthy
# dealaai_backend_prod   healthy
# dealaai_frontend_prod  healthy
```

### 2. Verificar Tablas Restauradas

```bash
docker exec dealaai_db_prod psql -U postgres -d dealaai_prod -c "\dt"

# Deberías ver tablas como:
# auth_user, stock_product, stock_transaction, etc.
```

### 3. Verificar Datos de Usuarios

```bash
docker exec dealaai_db_prod psql -U postgres -d dealaai_prod -c \
  "SELECT COUNT(*) as total_usuarios FROM auth_user;"
```

### 4. Probar Endpoint de API

```bash
# Health check
curl https://mcp.jorgemg.es/api/health/

# Respuesta esperada:
# {"status": "healthy", "database": "healthy", "timestamp": "UTC"}

# Ver logs
docker-compose logs backend | tail -50
```

### 5. Probar Login

- Accede a https://mcp.jorgemg.es/login
- Usa las credenciales de un usuario que exista en tu BD de desarrollo
- Deberías poder entrar correctamente

---

## 🚨 Problemas Comunes

### Error: "permission denied" en SSH

```bash
# Verificar permisos
ssh root@mcp.jorgemg.es "ls -la /opt/easypanel/projects/dealaai/backups/"

# Crear directorio si no existe
ssh root@mcp.jorgemg.es "mkdir -p /opt/easypanel/projects/dealaai/backups"
```

### Error: "Database already exists"

```bash
# Forzar eliminación
docker exec dealaai_db_prod psql -U postgres -c "DROP DATABASE dealaai_prod WITH (FORCE);"
```

### Error: "psql: error: role 'postgres' does not exist"

```bash
# Verificar usuario en contenedor
docker exec dealaai_db_prod psql -c "\du"

# Usar el usuario correcto (puede ser 'root', 'postgres', etc.)
```

### Error: "FATAL: password authentication failed"

```bash
# Verificar que DB_PASSWORD es correcto
echo $DB_PASSWORD

# O usar -w (no pedir password)
docker exec dealaai_db_prod psql -U postgres -w -d dealaai_prod -c "SELECT 1;"
```

### BD Restaurada pero Backend no conecta

```bash
# Reiniciar backend
docker-compose -f docker-compose.production.yml restart backend

# Ver logs
docker logs dealaai_backend_prod | tail -50

# Si sigue error, ejecutar migraciones
docker exec dealaai_backend_prod python manage.py migrate --noinput
```

### "relation 'auth_user' does not exist" después de restaurar

```bash
# Las migraciones de Django no se han ejecutado
# Ejecutar:
docker exec dealaai_backend_prod python manage.py migrate --noinput

# Si eso no funciona, ejecutar con verbosity
docker exec dealaai_backend_prod python manage.py migrate --verbosity=3
```

---

## 📊 Comparativa de Métodos

| Aspecto           | Automático     | Manual           |
| ----------------- | -------------- | ---------------- |
| **Requisito SSH** | ✅ Necesario   | ❌ No            |
| **Tiempo**        | ⚡ 5-15 min    | 🐢 15-30 min     |
| **Control**       | 🔄 Automático  | 👤 Manual        |
| **Errores**       | 📋 Fácil debug | 🔍 Más complejo  |
| **Recomendado**   | ✅ Sí          | Si no tienes SSH |

---

## ✅ Checklist Pre-Migración

- [ ] Backup de BD de desarrollo creado
- [ ] SSH configurado (si usas opción automática)
- [ ] Espacio disponible en servidor (al menos 2x tamaño del backup)
- [ ] Base de datos de producción vacía o con backup previo
- [ ] Contenedores de producción corriendo
- [ ] Variables de entorno correctas en EasyPanel

---

## ✅ Checklist Post-Migración

- [ ] Contenedores están healthy
- [ ] Tablas restauradas correctamente
- [ ] Número de usuarios correcto
- [ ] Endpoint /api/health/ responde
- [ ] Login funciona con usuarios de desarrollo
- [ ] Datos de inventario correctos (si aplica)
- [ ] Sin errores en logs de backend
- [ ] Frontend conecta sin problemas

---

## 🔄 Rollback (Si algo sale mal)

### Opción 1: Restaurar desde backup anterior

```bash
# En servidor de producción
BACKUP_PREVIO=$(ls -t /opt/easypanel/projects/dealaai/backups/db_production_backup_* | head -1)
docker exec -i dealaai_db_prod psql -U postgres -d dealaai_prod < $BACKUP_PREVIO
```

### Opción 2: Recrear contenedor desde cero

```bash
# Esto elimina TODO
docker-compose -f docker-compose.production.yml down -v
docker-compose -f docker-compose.production.yml up -d
```

---

## 📝 Notas Importantes

1. **Datos Sensibles**: El backup incluye todos los datos, incluyendo contraseñas hasheadas
2. **Migraciones**: Las migraciones de Django se ejecutan automáticamente
3. **Índices**: Se recrean automáticamente después de restaurar
4. **Roles de BD**: No se incluyen roles para evitar conflictos
5. **Extensiones**: pgvector, uuid-ossp, etc. ya están habilitadas en producción

---

## 📞 Soporte

Si necesitas ayuda:

1. Ejecutar script de export en local:

   ```bash
   /workspace/scripts/export-db-for-migration.sh
   ```

2. Capturar todos los errores:

   ```bash
   /workspace/scripts/export-db-for-migration.sh 2>&1 | tee migration.log
   ```

3. Compartir el archivo `migration.log`
