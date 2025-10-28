# 📋 RESUMEN: Migración BD Desarrollo → Producción

**Preparado:** 26 Oct 2025  
**Estado:** ✅ Completo y listo para usar  
**Documentos:** 4 guías + 3 scripts automáticos

---

## 📚 Documentación Preparada

### 1. 📖 **DATABASE_MIGRATION_GUIDE.md** (Completa)

Guía profesional con:

- Dos opciones de migración (automática y manual)
- Verificación post-migración
- Troubleshooting detallado
- Rollback en caso de problemas
- Comparativa de métodos

### 2. 🚀 **DB_MIGRATION_QUICK_REF.md** (Resumen)

Referencia rápida con:

- Comandos directos
- Checklist
- Problema/solución

### 3. 🐛 **PRODUCTION_FIX_HEALTHCHECK.md** (Bonus)

Documento anterior - soluciones para container unhealthy

### 4. 🔧 **DEBUGGING_PRODUCTION_UNHEALTHY.md** (Bonus)

Debugging paso a paso en caso de problemas

---

## 🛠️ Scripts Automáticos Preparados

### 1. **migrate-db-to-production.sh** ✅ Recomendado

```bash
./scripts/migrate-db-to-production.sh
```

**Qué hace:**

- ✓ Valida Docker y conexión
- ✓ Crea backup de desarrollo comprimido
- ✓ Sube a servidor por SSH
- ✓ Restaura en producción automáticamente
- ✓ Ejecuta migraciones
- ✓ Verifica resultado final

**Requisitos:**

- Docker corriendo
- SSH configurado

**Tiempo:** 5-15 minutos

---

### 2. **export-db-for-migration.sh** 📤 Sin SSH

```bash
./scripts/export-db-for-migration.sh
```

**Qué hace:**

- ✓ Exporta BD de desarrollo
- ✓ Crea versión comprimida
- ✓ Muestra instrucciones paso a paso

**Requisitos:**

- Docker corriendo
- Nada más

**Tiempo:** 1-2 minutos

---

### 3. **restore-db-production.sh** 🔄 Para servidor

Copiar a servidor de producción y ejecutar:

```bash
./restore-db-production.sh /ruta/al/backup.sql
```

**Qué hace:**

- ✓ Valida archivo de backup
- ✓ Crea backup previo de producción
- ✓ Limpia BD actual
- ✓ Restaura nuevos datos
- ✓ Ejecuta migraciones
- ✓ Reinicia servicios
- ✓ Verifica resultado

---

## 🎯 Flujo Recomendado

### Escenario A: Tienes SSH configurado ⚡

```bash
cd /workspace
./scripts/migrate-db-to-production.sh
# ¡Listo! Todo automático
```

### Escenario B: Sin SSH 👤

```bash
# Paso 1: Exportar
./scripts/export-db-for-migration.sh

# Paso 2: Descargar archivo de /workspace/database/backups/

# Paso 3: Subir a servidor (SFTP, SCP, etc.)

# Paso 4: Conectarse a servidor
ssh root@mcp.jorgemg.es

# Paso 5: Ejecutar restauración
./restore-db-production.sh /ruta/al/backup.sql
```

---

## 📊 Qué Incluye el Backup

✅ **Incluido:**

- Todas las tablas de Django
- Todos los datos (usuarios, inventario, etc.)
- Secuencias (auto-increment)
- Índices
- Restricciones

❌ **NO Incluido:**

- Roles de usuario (para evitar conflictos)
- Variables de conexión
- Configuración de servidor

---

## 📁 Archivos Creados

```
/workspace/
├── DATABASE_MIGRATION_GUIDE.md        (Guía completa)
├── DB_MIGRATION_QUICK_REF.md          (Resumen rápido)
├── PRODUCTION_FIX_HEALTHCHECK.md      (Bonus)
├── DEBUGGING_PRODUCTION_UNHEALTHY.md  (Bonus)
└── scripts/
    ├── migrate-db-to-production.sh    (Automático)
    ├── export-db-for-migration.sh     (Sin SSH)
    └── restore-db-production.sh       (Para servidor)
```

---

## ⚙️ Detalles Técnicos

### BD de Desarrollo

```
Contenedor: dealaai_db
Nombre: dealaai_dev
Usuario: postgres
Password: postgres
Host: localhost:5432
```

### BD de Producción (EasyPanel)

```
Contenedor: dealaai_db_prod
Nombre: dealaai_prod
Usuario: postgres
Password: ${DB_PASSWORD}
Host: db:5432
```

### Proceso de Backup

1. `pg_dump` con flags:

   - `--no-privileges` (sin permisos de roles)
   - `--no-owner` (sin información de dueño)
   - `--no-role-properties` (sin propiedades de roles)

2. Compresión gzip (reduce ~70% tamaño)

3. Restauración con `psql` en producción

---

## ✅ Verificación Final

Después de migrar, deberías ver:

```bash
# 1. Contenedores healthy
docker ps
# dealaai_backend_prod    Up ... (healthy)
# dealaai_db_prod         Up ... (healthy)
# dealaai_frontend_prod   Up ... (healthy)

# 2. Tablas restauradas
docker exec dealaai_db_prod psql -U postgres -d dealaai_prod -c "\dt"
# Múltiples tablas de django

# 3. API responde
curl https://mcp.jorgemg.es/api/health/
# {"status": "healthy", "database": "healthy"}

# 4. Login funciona
# Acceder a https://mcp.jorgemg.es/login
# Usar usuario de desarrollo
```

---

## 🚨 Seguridad

⚠️ **Importante:**

- El backup incluye todos los datos (incluyendo contraseñas hasheadas)
- Almacena en lugar seguro
- Usa HTTPS en transferencia
- Los scripts no guardan passwords en logs
- Siempre crea backup previo de producción antes de restaurar

---

## 📞 Soporte

### Si algo sale mal:

**Opción 1: Ver logs detallados**

```bash
docker logs dealaai_backend_prod | tail -50
docker logs dealaai_db_prod | tail -50
```

**Opción 2: Ejecutar script con logging**

```bash
./scripts/export-db-for-migration.sh 2>&1 | tee migration.log
# Envía migration.log para debugging
```

**Opción 3: Rollback**

```bash
# Restaurar desde backup previo creado automáticamente
docker exec -i dealaai_db_prod psql -U postgres -d dealaai_prod < \
  /opt/easypanel/projects/dealaai/backups/db_production_backup_*.sql
```

---

## 🎓 Aprendiste

✅ Cómo exportar base de datos PostgreSQL desde Docker  
✅ Cómo comprimir y transferir backups  
✅ Cómo restaurar datos en producción  
✅ Cómo automatizar migraciones de BD  
✅ Cómo hacer rollback en caso de problemas

---

## 🏁 Próximos Pasos

1. ✅ Leer `DATABASE_MIGRATION_GUIDE.md`
2. ✅ Ejecutar script apropiado (automático o manual)
3. ✅ Verificar con checklist
4. ✅ Probar login con usuarios de desarrollo
5. ✅ Validar datos en API
6. ✅ Documentar cualquier problema encontrado

---

**¿Necesitas algo más?**

- Más detalles: Ver `DATABASE_MIGRATION_GUIDE.md`
- Referencia rápida: Ver `DB_MIGRATION_QUICK_REF.md`
- Problemas con healthcheck: Ver `PRODUCTION_FIX_HEALTHCHECK.md`
- Debugging avanzado: Ver `DEBUGGING_PRODUCTION_UNHEALTHY.md`
