# 🗄️ MIGRACIÓN BD: GUÍA RÁPIDA

## 🚀 Opción 1: Automática (Recomendada)

```bash
cd /workspace
./scripts/migrate-db-to-production.sh
```

✅ Requisitos:

- Docker corriendo
- SSH configurado a `mcp.jorgemg.es`

⏱️ Tiempo: 5-15 minutos

---

## 📤 Opción 2: Manual (Sin SSH)

### Paso 1: Exportar datos

```bash
cd /workspace
./scripts/export-db-for-migration.sh
```

📍 Archivo creado: `/workspace/database/backups/db_development_*.sql`

### Paso 2: Descargar archivo

```bash
# En VS Code: Click derecho → Download
# O por SCP:
scp -r user@servidor:/workspace/database/backups/db_development_*.sql ~/Downloads/
```

### Paso 3: Subir a EasyPanel

```bash
scp ~/Downloads/db_development_*.sql root@mcp.jorgemg.es:/opt/easypanel/projects/dealaai/backups/
```

### Paso 4: Conectarse al servidor

```bash
ssh root@mcp.jorgemg.es
```

### Paso 5: Restaurar (opción A - con script)

```bash
cd ~
chmod +x restore-db-production.sh
./restore-db-production.sh /opt/easypanel/projects/dealaai/backups/db_development_*.sql
```

### Paso 5: Restaurar (opción B - manual)

```bash
# Variables
BACKUP="/opt/easypanel/projects/dealaai/backups/db_development_*.sql"
CONTAINER="dealaai_db_prod"

# Limpiar BD
docker exec $CONTAINER psql -U postgres -c "DROP DATABASE IF EXISTS dealaai_prod;"
docker exec $CONTAINER psql -U postgres -c "CREATE DATABASE dealaai_prod OWNER postgres;"

# Restaurar
docker exec -i $CONTAINER psql -U postgres -d dealaai_prod < $BACKUP

# Ejecutar migraciones
docker exec dealaai_backend_prod python manage.py migrate --noinput

# Reiniciar
docker-compose -f docker-compose.production.yml restart backend
```

---

## ✅ Verificar Después

```bash
# 1. Ver estado de contenedores
docker ps

# 2. Ver tablas restauradas
docker exec dealaai_db_prod psql -U postgres -d dealaai_prod -c "\dt"

# 3. Contar usuarios
docker exec dealaai_db_prod psql -U postgres -d dealaai_prod \
  -c "SELECT COUNT(*) FROM auth_user;"

# 4. Probar API
curl https://mcp.jorgemg.es/api/health/

# 5. Ver logs
docker-compose logs backend | tail -20
```

---

## 🎯 Checklist

- [ ] Backup exportado
- [ ] Archivo subido a servidor
- [ ] Restauración completada
- [ ] Migraciones ejecutadas
- [ ] Contenedores healthy
- [ ] API responde
- [ ] Login funciona

---

## 📊 Info Técnica

| Campo          | Desarrollo    | Producción        |
| -------------- | ------------- | ----------------- |
| **BD**         | `dealaai_dev` | `dealaai_prod`    |
| **Usuario**    | `postgres`    | `postgres`        |
| **Host**       | `localhost`   | `db`              |
| **Puerto**     | `5432`        | `5432`            |
| **Contenedor** | `dealaai_db`  | `dealaai_db_prod` |

---

## 🆘 Problemas

**"Connection refused"**
→ `docker-compose up -d db`

**"Database already exists"**
→ `DROP DATABASE dealaai_prod WITH (FORCE);`

**"Backend no conecta después"**
→ `docker exec dealaai_backend_prod python manage.py migrate --noinput`

---

👉 Ver `/workspace/DATABASE_MIGRATION_GUIDE.md` para documentación completa
