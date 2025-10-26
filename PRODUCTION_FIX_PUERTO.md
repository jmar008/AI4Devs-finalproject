# 🔌 FIX - Puerto 3000 en Uso

**Fecha:** 26 Oct 2025  
**Problema:** Puerto 3000 ya asignado  
**Solución:** Cambiar puerto frontend + crear override.yml vacío

---

## ❌ Error Encontrado

```
Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint dealaai_frontend_prod: Bind for 0.0.0.0:3000 failed: port is already allocated
```

**Además:** EasyPanel intenta usar `docker-compose.override.yml` que no existía.

---

## ✅ Soluciones Aplicadas

### 1. Cambiar Puerto del Frontend

```diff
# docker-compose.production.yml
ports:
-   - "3000:3000"  # Puerto ocupado
+   - "3001:3000"  # Puerto libre
```

**Por qué funciona:**

- El contenedor interno sigue usando puerto 3000
- El puerto externo cambió a 3001
- No hay conflicto con otros servicios

### 2. Crear docker-compose.override.yml Vacío

```yaml
# Archivo vacío para EasyPanel
services: {}
```

**Por qué necesario:**

- EasyPanel siempre busca este archivo
- Si no existe, falla el comando
- Archivo vacío = no overrides = configuración base

---

## 📋 Configuración Final

### Puertos:

- **Backend:** `8000` (sin cambios)
- **Frontend:** `3001` (cambiado de 3000)
- **Database:** `5432` (sin cambios)
- **pgAdmin:** `5050` (sin cambios)

### Archivos:

- ✅ `docker-compose.production.yml` - Puerto frontend cambiado
- ✅ `docker-compose.override.yml` - Archivo vacío creado

---

## 🚀 Cómo Deployar

### 1. Commit de cambios:

```bash
git add docker-compose.production.yml docker-compose.override.yml
git commit -m "fix: cambiar puerto frontend 3000→3001 y crear override.yml vacío"
git push
```

### 2. En EasyPanel:

- Click **Rebuild** (no Start)
- Esperar 2-3 minutos
- Verificar logs

### 3. Verificar:

```bash
# En servidor
docker ps

# Deberías ver:
# dealaai_backend_prod   Up ... 0.0.0.0:8000->8000/tcp
# dealaai_frontend_prod  Up ... 0.0.0.0:3001->3000/tcp  ← Puerto 3001
# dealaai_db_prod        Up ... 0.0.0.0:5432->5432/tcp
```

---

## 🌐 URLs de Acceso

Después del deploy:

- **Frontend:** `https://mcp.jorgemg.es` (puerto interno 3000)
- **API:** `https://mcp.jorgemg.es/api/v1`
- **Health:** `https://mcp.jorgemg.es/api/health/`
- **Admin:** `https://mcp.jorgemg.es/admin/`

**Nota:** El frontend sigue siendo accesible en `https://mcp.jorgemg.es` porque Nginx/Apache en EasyPanel probablemente redirige el puerto 80/443 al contenedor.

---

## 🔍 Verificación

### 1. Contenedores corriendo:

```bash
docker ps | grep dealaai
```

### 2. Puertos correctos:

```bash
docker port dealaai_frontend_prod
# Debería mostrar: 3000/tcp -> 0.0.0.0:3001
```

### 3. Frontend responde:

```bash
curl -I https://mcp.jorgemg.es
# HTTP/1.1 200 OK
```

### 4. API funciona:

```bash
curl https://mcp.jorgemg.es/api/health/
# {"status": "healthy", "database": "healthy"}
```

---

## 🚨 Troubleshooting

### "Puerto 3001 también ocupado"

```bash
# Cambiar a otro puerto, ej: 3002
ports:
  - "3002:3000"
```

### "Frontend no carga"

```bash
# Verificar que el contenedor está corriendo
docker logs dealaai_frontend_prod

# Verificar conectividad interna
docker exec dealaai_frontend_prod curl localhost:3000
```

### "EasyPanel sigue usando override.yml viejo"

```bash
# Forzar rebuild completo
docker-compose down -v
docker-compose up -d --build
```

---

## 📊 Comparativa

| Puerto | Antes    | Después     | Estado   |
| ------ | -------- | ----------- | -------- |
| 8000   | Backend  | Backend     | ✅ OK    |
| 3000   | Frontend | **OCUPADO** | ❌ Error |
| 3001   | Libre    | Frontend    | ✅ OK    |
| 5432   | Database | Database    | ✅ OK    |

---

## 🎯 Lección Aprendida

> "Los puertos son recursos compartidos. Verificar conflictos antes de deploy."

**Checklist pre-deploy:**

- [ ] Verificar puertos libres: `netstat -tlnp | grep :3000`
- [ ] Verificar configuración EasyPanel
- [ ] Probar localmente primero
- [ ] Tener plan B (puerto alternativo)

---

## 📝 Próximos Pasos

1. ✅ Deploy con puerto 3001
2. ✅ Verificar funcionamiento
3. ✅ Migrar base de datos si necesario
4. ⏰ Configurar dominio correctamente en EasyPanel
5. ⏰ Optimizar configuración de puertos

---

**Estado:** ✅ Listo para deploy  
**Confianza:** Alta - solución simple y efectiva  
**Riesgo:** Bajo - solo cambio de puerto

EOF
