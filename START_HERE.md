# 🚀 COMIENZA AQUÍ - Producción (26 Oct 2025)

## ¿Cuál es tu situación?

### Situación 1: Container Backend "Unhealthy" ❌
```bash
# Ver: PRODUCTION_FIX_HEALTHCHECK.md

# Ya está solucionado en repo
git pull
# En EasyPanel: Click Rebuild
```

### Situación 2: Necesito Migrar BD a Producción 📊
```bash
# Opción A: Con SSH (automático)
cd /workspace
./scripts/migrate-db-to-production.sh

# Opción B: Sin SSH (manual)
cd /workspace
./scripts/export-db-for-migration.sh
# Luego sube archivo a servidor manualmente
```

### Situación 3: Ambas cosas (empezar desde cero) 🎯
```bash
# 1. Arreglar healthcheck
git pull
# En EasyPanel: Rebuild

# 2. Esperar a que esté healthy
docker ps | grep backend

# 3. Migrar BD
./scripts/migrate-db-to-production.sh

# 4. Verificar
curl https://mcp.jorgemg.es/api/health/
```

---

## 📚 Documentación Disponible

### 🎯 RÁPIDA (5 min)
- **DB_MIGRATION_QUICK_REF.md** - Comandos directos

### 📖 COMPLETA (30 min)
- **DATABASE_MIGRATION_GUIDE.md** - Guía profesional
- **PRODUCTION_COMPLETE_GUIDE.md** - Overview integrado

### 🔧 TROUBLESHOOTING
- **DEBUGGING_PRODUCTION_UNHEALTHY.md** - Si healthcheck falla

---

## 🛠️ Scripts Disponibles

```bash
# Migración automática (requiere SSH)
./scripts/migrate-db-to-production.sh

# Exportar BD (sin SSH)
./scripts/export-db-for-migration.sh

# Restaurar en servidor
./scripts/restore-db-production.sh
```

---

## ✅ Checklist Rápido

- [ ] Healthcheck en container: `docker ps`
- [ ] API responde: `curl https://mcp.jorgemg.es/api/health/`
- [ ] BD migrada: `docker exec db psql -U postgres -d dealaai_prod -c "\dt"`
- [ ] Login funciona: https://mcp.jorgemg.es/login
- [ ] Datos en API: Verifica endpoints

---

## 🚨 Problemas Rápidos

| Problema | Solución |
|----------|----------|
| Container unhealthy | Ver: DEBUGGING_PRODUCTION_UNHEALTHY.md |
| BD no se migra | Ver: DATABASE_MIGRATION_GUIDE.md |
| Login no funciona | `docker logs backend \| tail -50` |
| Datos no visibles | Ejecutar migraciones: `docker exec backend python manage.py migrate` |

---

## 📖 Próxima Lectura

1. **Si tienes urgencia:** DB_MIGRATION_QUICK_REF.md
2. **Para entender todo:** PRODUCTION_COMPLETE_GUIDE.md
3. **Referencia completa:** DATABASE_MIGRATION_GUIDE.md

---

**¿Listo?** Elige tu camino arriba ☝️
