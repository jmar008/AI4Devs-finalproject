# 🚀 PRODUCCIÓN: Guía Completa de Setup & Migración

**Estado Actual:** 26 Oct 2025  
**Problemas Resueltos:** ✅ Healthcheck + ✅ Migración BD

---

## 🎯 Resumen de lo que hicimos

### Problema 1: Container Backend "Unhealthy" ✅ RESUELTO

**Causa:** Healthcheck usando `localhost` en Docker  
**Solución:**

- ✅ Cambiar a `127.0.0.1` en docker-compose.production.yml
- ✅ Aumentar start_period a 60s
- ✅ Mejorar entrypoint.sh con mejor manejo de BD
- ✅ Crear docker-compose.override.yml

**Archivos modificados:**

- `docker-compose.production.yml`
- `backend/entrypoint.sh`
- `docker-compose.override.yml` (nuevo)

**Documentación:**

- `PRODUCTION_FIX_HEALTHCHECK.md` (paso a paso)
- `DEBUGGING_PRODUCTION_UNHEALTHY.md` (troubleshooting)

---

### Problema 2: Migrar BD Desarrollo → Producción ✅ LISTO

**Solución:** Scripts automáticos + documentación

**Scripts creados:**

- `scripts/migrate-db-to-production.sh` (automático con SSH)
- `scripts/export-db-for-migration.sh` (exportar backup)
- `scripts/restore-db-production.sh` (restaurar en servidor)

**Documentación:**

- `DATABASE_MIGRATION_GUIDE.md` (guía completa)
- `DB_MIGRATION_QUICK_REF.md` (referencia rápida)
- `MIGRATION_SUMMARY.md` (resumen)

---

## 🔧 Paso 1: Arreglar Healthcheck (Ya Hecho)

### ¿Necesito hacer algo?

Depende de si ya desplegaste en EasyPanel:

**Si aún NO has desplegado:**

```bash
# Haz commit de los cambios
git add docker-compose.production.yml backend/entrypoint.sh docker-compose.override.yml
git commit -m "fix: healthcheck backend en producción"
git push

# Luego deploy normal en EasyPanel
```

**Si YA lo desplegaste con error:**

```bash
# 1. Hacer los cambios locales (ya están hechos)
git add docker-compose.production.yml backend/entrypoint.sh docker-compose.override.yml
git commit -m "fix: healthcheck backend en producción"
git push

# 2. En EasyPanel: Hacer rebuild
# Dashboard → DealaAI → Rebuild (no Start)

# 3. Ver logs
docker-compose logs backend | head -50
```

---

## 📤 Paso 2: Migrar Base de Datos

Tienes dos opciones dependiendo de tu configuración:

### Opción A: SSH Configurado (Automático) ⚡

```bash
cd /workspace
./scripts/migrate-db-to-production.sh
```

**Qué hace:**

1. Valida Docker y SSH
2. Exporta BD de desarrollo
3. Sube a servidor de producción
4. Restaura datos
5. Ejecuta migraciones
6. Verifica resultado

**Tiempo:** 5-15 minutos

---

### Opción B: Sin SSH (Manual) 👤

#### Paso 1: Exportar en desarrollo

```bash
cd /workspace
./scripts/export-db-for-migration.sh
```

Archivo creado: `/workspace/database/backups/db_development_YYYYMMDD_HHMMSS.sql`

#### Paso 2: Descargar

- En VS Code: Click derecho en archivo → Download
- O por SCP: `scp user@devcontainer:/workspace/database/backups/db_*.sql ~/Downloads/`

#### Paso 3: Subir a EasyPanel

```bash
# Via SCP
scp ~/Downloads/db_development_*.sql root@mcp.jorgemg.es:/opt/easypanel/projects/dealaai/backups/

# O via SFTP (Filezilla, WinSCP)
# Server: mcp.jorgemg.es
# Upload: /opt/easypanel/projects/dealaai/backups/
```

#### Paso 4: Conectar a servidor

```bash
ssh root@mcp.jorgemg.es
```

#### Paso 5: Restaurar

```bash
# Descargar script de restauración
wget https://raw.githubusercontent.com/tu-repo/main/scripts/restore-db-production.sh
chmod +x restore-db-production.sh

# Ejecutar
./restore-db-production.sh /opt/easypanel/projects/dealaai/backups/db_development_*.sql

# O hacerlo manualmente (sin script):
BACKUP="/opt/easypanel/projects/dealaai/backups/db_development_*.sql"
CONTAINER="dealaai_db_prod"

docker exec $CONTAINER psql -U postgres -c "DROP DATABASE dealaai_prod WITH (FORCE);"
docker exec $CONTAINER psql -U postgres -c "CREATE DATABASE dealaai_prod OWNER postgres;"
docker exec -i $CONTAINER psql -U postgres -d dealaai_prod < "$BACKUP"
docker exec dealaai_backend_prod python manage.py migrate --noinput
docker-compose -f docker-compose.production.yml restart backend
```

---

## ✅ Verificación Post-Migración

### 1. Healthcheck

```bash
docker ps
# Deberías ver (healthy) para todos
```

### 2. Base de Datos

```bash
# Ver tablas
docker exec dealaai_db_prod psql -U postgres -d dealaai_prod -c "\dt"

# Contar usuarios
docker exec dealaai_db_prod psql -U postgres -d dealaai_prod \
  -c "SELECT COUNT(*) FROM auth_user;"
```

### 3. API

```bash
# Health endpoint
curl https://mcp.jorgemg.es/api/health/

# Debe responder:
# {"status": "healthy", "database": "healthy", "timestamp": "UTC"}
```

### 4. Frontend

- Accede a https://mcp.jorgemg.es
- Deberías ver la app cargando

### 5. Login

- Ve a https://mcp.jorgemg.es/login
- Usa usuario de desarrollo
- Deberías poder entrar

### 6. Logs

```bash
docker logs dealaai_backend_prod | tail -30
# No deberían haber errores de BD
```

---

## 📊 Comparativa: Antes vs Después

### ANTES ❌

```
Container: dealaai_backend_prod
Status: Unhealthy
Error: Health check failed
Reason: Cannot connect to http://localhost:8000/api/health/
```

### DESPUÉS ✅

```
Container: dealaai_backend_prod
Status: Healthy
Response: HTTP 200 OK
Database: Disponible con datos de desarrollo
```

---

## 🎯 Checklist Final

### Pre-Deployment

- [ ] Cambios locales committeados
- [ ] Docker compose files revisados
- [ ] Entrypoint.sh mejorado

### Deployment en EasyPanel

- [ ] Push de cambios a main/tu-rama
- [ ] Pull en EasyPanel (o redeploy)
- [ ] Rebuild completado sin errores
- [ ] Backend mostrando healthy

### Post-Migración BD

- [ ] Backup de desarrollo exportado
- [ ] Datos transferidos a producción
- [ ] Migraciones ejecutadas
- [ ] Tablas restauradas correctamente

### Validación Final

- [ ] Healthcheck responde
- [ ] API endpoints funcionan
- [ ] Login funciona
- [ ] Datos visibles en app
- [ ] Logs sin errores

---

## 🚨 Si algo falla

### Container aún unhealthy

```bash
# Ver logs
docker logs dealaai_backend_prod | tail -100

# Troubleshooting: Ver DEBUGGING_PRODUCTION_UNHEALTHY.md
```

### BD no se migró

```bash
# Verificar archivo de backup
ls -la /opt/easypanel/projects/dealaai/backups/

# Ver tabla de usuarios
docker exec dealaai_db_prod psql -U postgres -d dealaai_prod -c "SELECT COUNT(*) FROM auth_user;"

# Troubleshooting: Ver DATABASE_MIGRATION_GUIDE.md
```

### Login no funciona

```bash
# Verificar que migraciones se ejecutaron
docker exec dealaai_backend_prod python manage.py migrate --verbosity=3

# Ver logs
docker logs dealaai_backend_prod | grep -i auth
```

---

## 📁 Documentación Disponible

### Para Healthcheck

- `PRODUCTION_FIX_HEALTHCHECK.md` - Solución y explicación
- `DEBUGGING_PRODUCTION_UNHEALTHY.md` - Troubleshooting detallado

### Para Migración BD

- `DATABASE_MIGRATION_GUIDE.md` - Guía profesional completa
- `DB_MIGRATION_QUICK_REF.md` - Referencia rápida
- `MIGRATION_SUMMARY.md` - Resumen de lo que se preparó

### Documentación Anterior (Bonus)

- `EASYPANEL_SETUP.md`
- `DEPLOYMENT_GUIDE_PRODUCTION.md`

---

## 🎓 Lo que puedes hacer ahora

### Opción 1: Migración Completa (Recomendada)

```bash
# 1. Arreglar healthcheck (cambios ya en repo)
git commit && git push

# 2. Deploy en EasyPanel
# Click rebuild en dashboard

# 3. Migrar BD
./scripts/migrate-db-to-production.sh

# 4. Verificar todo funciona
curl https://mcp.jorgemg.es/api/health/
```

### Opción 2: Paso a Paso

```bash
# 1. Primero arreglar healthcheck
# 2. Esperar a que esté healthy
# 3. Luego migrar BD
# 4. Verificar cada paso
```

### Opción 3: Ya en Producción

```bash
# Si ya tienes BD en producción y solo necesitas healthcheck:
# 1. Push cambios
# 2. Rebuild en EasyPanel
# No migrar BD
```

---

## 📞 Resumen de URLs

```
API Base:         https://mcp.jorgemg.es/api/v1
Health Check:     https://mcp.jorgemg.es/api/health/
Admin:            https://mcp.jorgemg.es/admin/
API Docs:         https://mcp.jorgemg.es/api/docs/
Frontend:         https://mcp.jorgemg.es/
Login:            https://mcp.jorgemg.es/login
```

---

## ✨ Resultado Final

```
✅ Backend corriendo y healthy
✅ Frontend accesible
✅ Base de datos migrada con datos de desarrollo
✅ Login funcionando
✅ API respondiendo correctamente
✅ Migraciones de Django ejecutadas
✅ Static files servidos correctamente
✅ Todo en producción via EasyPanel
```

---

## 🏁 Próximos Pasos

1. **Hoy:** Ejecutar migración BD si no la hiciste
2. **Mañana:** Validar que todo funciona en producción
3. **Siguiente:** Hacer cambios de desarrollo → testing en producción
4. **Eventualmente:** Configurar CI/CD automático

---

## 💡 Tips

- Los scripts son idempotentes (puedes ejecutarlos varias veces)
- Los backups se guardan en `/workspace/database/backups/`
- Siempre mantén copias de backups importantes
- Lee los logs - contienen mucha información útil
- Los errores de BD suelen ser por variables de entorno faltantes

---

**¿Listo para producción?** 🚀

Ver: `DATABASE_MIGRATION_GUIDE.md` o `DB_MIGRATION_QUICK_REF.md`
