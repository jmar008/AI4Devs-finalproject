# 📦 LISTA DE VERIFICACIÓN COMPLETA - DESPLIEGUE A PRODUCCIÓN

## 🎯 Resumen Ejecutivo

**MVP v1.0.0** está listo para desplegar. Tienes **3 documentos principales**:

1. **DEPLOYMENT_SUMMARY.md** ← 📍 EMPIEZA AQUÍ (resumen ejecutivo)
2. **DEPLOYMENT_GUIDE_PRODUCTION.md** ← Guía detallada paso a paso
3. **deploy-production.sh** ← Script automático opcional

---

## 🚀 FLUJO RÁPIDO DE 5 PASOS

```
┌─────────────────────────────────────────────────────┐
│ PASO 1: Git & Versioning (5 min)                    │
│ - Commit cambios en main                            │
│ - Crear tag v1.0.0-mvp                             │
│ - Push a GitHub                                     │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ PASO 2: Preparar Variables de Entorno (10 min)      │
│ - Crear .env.production                            │
│ - Variables de BD, Redis, CORS, SSL                │
│ - NO commitear a Git                               │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ PASO 3: Setup Servidor (45 min)                     │
│ - SSH a servidor remoto                            │
│ - Crear directorios /opt/dealaai/                  │
│ - Clonar repo en servidor                          │
│ - Generar certificados SSL                         │
│ - Copiar .env.production                           │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ PASO 4: Levantar Servicios (10 min)                 │
│ - docker-compose -f docker-compose.production.yml  │
│   up -d                                            │
│ - Esperar 60 segundos (BD se inicia)              │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│ PASO 5: Configurar BD & Verificar (20 min)          │
│ - Ejecutar migraciones                             │
│ - Crear superusuario                               │
│ - Recolectar static files                          │
│ - Verificar en navegador                           │
└─────────────────────────────────────────────────────┘
                         ↓
              ✅ EN PRODUCCIÓN
```

---

## 📋 CHECKLIST DETALLADO

### FASE 1: PREPARACIÓN LOCAL (30 minutos)

```bash
# ✓ Paso 1.1: Actualizar código
├─ git status                           # Verificar sin cambios
├─ git add -A
├─ git commit -m "feat: MVP v1.0.0"
└─ git push origin main

# ✓ Paso 1.2: Crear versión
├─ git tag -a v1.0.0-mvp -m "Release"
└─ git push origin v1.0.0-mvp

# ✓ Paso 1.3: Crear .env.production
├─ cat > .env.production << EOF
├─ DEBUG=False
├─ SECRET_KEY=<GENERAR CON: python3 -c 'import secrets; print(secrets.token_urlsafe(50))'>
├─ DATABASE_URL=postgresql://dealaai_user:PASSWORD@db:5432/dealaai_prod
├─ REDIS_URL=redis://redis:6379/0
├─ SECURE_SSL_REDIRECT=True
├─ SESSION_COOKIE_SECURE=True
├─ CSRF_COOKIE_SECURE=True
├─ CORS_ALLOWED_ORIGINS=https://mcp.jorgemg.es,https://www.mcp.jorgemg.es
├─ NEXT_PUBLIC_API_URL=https://mcp.jorgemg.es/api
└─ EOF

# ✓ Paso 1.4: Validar dockerfiles
├─ cat docker/backend/Dockerfile.prod        # Verificar gunicorn, healthcheck
└─ cat docker/frontend/Dockerfile.prod       # Verificar npm build, healthcheck

# ✓ Paso 1.5: Construir imágenes (OPCIONAL)
├─ docker build -f docker/backend/Dockerfile.prod -t dealaai-backend:1.0.0 ./backend
└─ docker build -f docker/frontend/Dockerfile.prod -t dealaai-frontend:1.0.0 ./frontend
```

---

### FASE 2: PREPARAR SERVIDOR REMOTO (45 minutos)

```bash
# ✓ Paso 2.1: Conectar a servidor
ssh usuario@mcp.jorgemg.es

# ✓ Paso 2.2: Crear estructura de directorios
├─ sudo mkdir -p /opt/dealaai/data/{postgres,redis,media,static,logs,backups}
├─ sudo mkdir -p /opt/dealaai/docker/nginx/ssl
└─ sudo chown -R usuario:usuario /opt/dealaai

# ✓ Paso 2.3: Clonar repositorio
├─ cd /opt/dealaai
├─ git clone https://github.com/jmar008/AI4Devs-finalproject.git
└─ cd AI4Devs-finalproject && git checkout v1.0.0-mvp

# ✓ Paso 2.4: Generar certificados SSL
├─ sudo apt-get update
├─ sudo apt-get install certbot python3-certbot-nginx
├─ sudo certbot certonly --standalone \
│   -d mcp.jorgemg.es -d www.mcp.jorgemg.es \
│   -m admin@mcp.jorgemg.es --non-interactive --agree-tos
└─ sudo cp /etc/letsencrypt/live/mcp.jorgemg.es/*.pem \
    /opt/dealaai/AI4Devs-finalproject/docker/nginx/ssl/

# ✓ Paso 2.5: Copiar archivo .env.production
├─ # ⚠️ CREAR MANUALMENTE EN SERVIDOR (NO clonar de git)
├─ scp .env.production usuario@mcp.jorgemg.es:/opt/dealaai/AI4Devs-finalproject/
└─ chmod 600 .env.production

# ✓ Paso 2.6: Crear volúmenes Docker
├─ docker volume create dealaai_postgres_data
├─ docker volume create dealaai_redis_data
├─ docker volume create dealaai_backend_media
├─ docker volume create dealaai_backend_static
└─ docker volume create dealaai_backend_logs
```

---

### FASE 3: DESPLIEGUE DE SERVICIOS (30 minutos)

```bash
# ✓ Paso 3.1: Levantar servicios con Docker Compose
cd /opt/dealaai/AI4Devs-finalproject
docker-compose -f docker-compose.production.yml up -d

# ✓ Paso 3.2: Verificar servicios (esperar 60 segundos)
└─ docker-compose -f docker-compose.production.yml ps
   Esperado: Todos "Up"

# ✓ Paso 3.3: Ver logs iniciales
├─ docker-compose -f docker-compose.production.yml logs
├─ docker-compose -f docker-compose.production.yml logs backend
└─ docker-compose -f docker-compose.production.yml logs frontend

# ✓ Paso 3.4: Ejecutar migraciones
docker-compose -f docker-compose.production.yml exec backend \
  python manage.py migrate --noinput

# ✓ Paso 3.5: Crear superusuario
docker-compose -f docker-compose.production.yml exec backend \
  python manage.py createsuperuser
  ├─ Username: admin
  ├─ Email: admin@mcp.jorgemg.es
  ├─ Password: [Contraseña fuerte]
  └─ Confirm: [Confirmar]

# ✓ Paso 3.6: Recolectar static files
docker-compose -f docker-compose.production.yml exec backend \
  python manage.py collectstatic --noinput

# ✓ Paso 3.7: Verificar volúmenes
├─ docker volume inspect dealaai_backend_static
├─ docker volume inspect dealaai_backend_media
└─ docker volume inspect dealaai_postgres_data
```

---

### FASE 4: VALIDAR DESPLIEGUE (20 minutos)

```bash
# ✓ Paso 4.1: Pruebas de conectividad HTTP
├─ curl -I https://mcp.jorgemg.es/              # Esperado: 200
├─ curl -I https://mcp.jorgemg.es/api/          # Esperado: 200 o 404 es ok
├─ curl -I https://mcp.jorgemg.es/admin/        # Esperado: 302 (redirect)
└─ curl https://mcp.jorgemg.es/api/health/      # Verificar respuesta

# ✓ Paso 4.2: Verificar logs del sistema
├─ docker-compose -f docker-compose.production.yml logs nginx | tail -20
├─ docker-compose -f docker-compose.production.yml logs backend | tail -20
└─ docker-compose -f docker-compose.production.yml logs frontend | tail -20

# ✓ Paso 4.3: Testing MANUAL en navegador
├─ Abrir: https://mcp.jorgemg.es/
│   └─ ✓ Frontend carga
│   └─ ✓ CSS/JS carga correctamente
│   └─ ✓ Sin errores en consola
│
├─ Ir a: https://mcp.jorgemg.es/login
│   └─ ✓ Página de login visible
│   └─ ✓ Campos de usuario/contraseña
│
├─ Login con superusuario
│   └─ ✓ Redirige a /dashboard
│   └─ ✓ Token en localStorage
│   └─ ✓ Sidebar visible
│
├─ Presionar F5 (recarga)
│   └─ ✓ Sesión se mantiene
│   └─ ✓ NO redirige a login
│
├─ Click en "Stock"
│   └─ ✓ Tabla carga con datos
│   └─ ✓ Leyenda de tipos visible
│   └─ ✓ Paginación funciona
│
├─ Logout
│   └─ ✓ Redirige a /login
│   └─ ✓ localStorage limpio
│
└─ Intentar acceder a /stock sin login
    └─ ✓ Redirige a /login

# ✓ Paso 4.4: Performance básico
├─ time curl https://mcp.jorgemg.es/          # <2s OK
└─ curl -w "Time: %{time_total}s\n" https://mcp.jorgemg.es/api/health/
```

---

### FASE 5: CONFIGURAR MONITOREO & BACKUPS (20 minutos)

```bash
# ✓ Paso 5.1: Crear script de backup
cat > /opt/dealaai/backup.sh << 'EOF'
#!/bin/bash
set -e
BACKUP_DIR="/opt/dealaai/data/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/opt/dealaai/data/logs/backup.log"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Iniciando backup..." >> "$LOG_FILE"

docker-compose -f /opt/dealaai/AI4Devs-finalproject/docker-compose.production.yml \
  exec -T db pg_dump -U postgres dealaai_prod | \
  gzip > "$BACKUP_DIR/db_$TIMESTAMP.sql.gz"

tar -czf "$BACKUP_DIR/media_$TIMESTAMP.tar.gz" \
  -C /opt/dealaai/data media/ 2>/dev/null || true

find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete

echo "[$(date)] Backup completado: $TIMESTAMP" >> "$LOG_FILE"
EOF

chmod +x /opt/dealaai/backup.sh

# ✓ Paso 5.2: Agregar a cron (3 AM diarios)
(crontab -l 2>/dev/null || true; \
  echo "0 3 * * * /opt/dealaai/backup.sh >> /opt/dealaai/data/logs/backup.log 2>&1") | \
  crontab -

# ✓ Paso 5.3: Crear script de healthcheck
cat > /opt/dealaai/healthcheck.sh << 'EOF'
#!/bin/bash
set -e

BACKEND=$(curl -s -o /dev/null -w "%{http_code}" https://mcp.jorgemg.es/api/health/ || echo "000")
FRONTEND=$(curl -s -o /dev/null -w "%{http_code}" https://mcp.jorgemg.es/ || echo "000")

echo "[$(date)] Backend: $BACKEND, Frontend: $FRONTEND" >> /opt/dealaai/data/logs/healthcheck.log

if [ "$BACKEND" != "200" ] || [ "$FRONTEND" != "200" ]; then
    echo "[$(date)] ⚠️ ALERTA: Servicios no responden correctamente" >> /opt/dealaai/data/logs/healthcheck.log

    docker-compose -f /opt/dealaai/AI4Devs-finalproject/docker-compose.production.yml restart

    sleep 30

    BACKEND_RETRY=$(curl -s -o /dev/null -w "%{http_code}" https://mcp.jorgemg.es/api/health/ || echo "000")

    if [ "$BACKEND_RETRY" != "200" ]; then
        echo "DealaAI Backend Down (Status: $BACKEND_RETRY)" | \
        mail -s "🚨 ALERTA PRODUCCIÓN" admin@mcp.jorgemg.es
    fi
fi
EOF

chmod +x /opt/dealaai/healthcheck.sh

# ✓ Paso 5.4: Agregar healthcheck a cron (cada 5 minutos)
(crontab -l 2>/dev/null || true; \
  echo "*/5 * * * * /opt/dealaai/healthcheck.sh 2>&1") | \
  crontab -

# ✓ Paso 5.5: Verificar crontabs
crontab -l
```

---

## ⚠️ PROBLEMAS COMUNES Y SOLUCIONES

### Problema: 502 Bad Gateway

```bash
# Diagnóstico
docker-compose -f docker-compose.production.yml logs backend | grep ERROR

# Solución
docker-compose -f docker-compose.production.yml restart backend
# Esperar 30 segundos
curl https://mcp.jorgemg.es/api/health/
```

### Problema: Frontend no carga CSS/JS

```bash
# Diagnóstico
docker-compose -f docker-compose.production.yml logs frontend

# Solución
docker-compose -f docker-compose.production.yml restart frontend
# o
docker-compose -f docker-compose.production.yml up -d --build frontend
```

### Problema: Base de datos no conecta

```bash
# Diagnóstico
docker-compose -f docker-compose.production.yml exec db pg_isready

# Solución
docker-compose -f docker-compose.production.yml restart db
# Esperar 60 segundos antes de intentar login
```

### Problema: Static files no cargan

```bash
# Solución
docker-compose -f docker-compose.production.yml exec backend \
  python manage.py collectstatic --noinput --clear
```

---

## 📞 SOPORTE POST-DEPLOYMENT

### Ver logs en tiempo real

```bash
# Todos
docker-compose -f docker-compose.production.yml logs -f

# Backend solamente
docker-compose -f docker-compose.production.yml logs -f backend

# Frontend solamente
docker-compose -f docker-compose.production.yml logs -f frontend

# Nginx solamente
docker-compose -f docker-compose.production.yml logs -f nginx
```

### Reiniciar servicios

```bash
# Un servicio
docker-compose -f docker-compose.production.yml restart backend

# Todos
docker-compose -f docker-compose.production.yml restart

# Full reset
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d
```

### Ejecutar comandos Django

```bash
# Shell interactivo
docker-compose -f docker-compose.production.yml exec backend python manage.py shell

# Ver migraciones pendientes
docker-compose -f docker-compose.production.yml exec backend \
  python manage.py migrate --plan

# Crear dump de base de datos
docker-compose -f docker-compose.production.yml exec -T db \
  pg_dump -U postgres dealaai_prod > backup.sql
```

---

## 🎯 URLS Y CREDENCIALES FINALES

```
┌─ PRODUCCIÓN ─────────────────────────────────────────┐
│ Dominio: https://mcp.jorgemg.es                      │
├─ ACCESO PÚBLICO ──────────────────────────────────────┤
│ Frontend: https://mcp.jorgemg.es/                    │
│ Login: https://mcp.jorgemg.es/login                  │
│ Dashboard: https://mcp.jorgemg.es/dashboard          │
│ Stock: https://mcp.jorgemg.es/stock                  │
├─ ACCESO ADMINISTRATIVO ────────────────────────────────┤
│ Admin Panel: https://mcp.jorgemg.es/admin/           │
│ Django User: admin                                    │
│ Django Email: admin@mcp.jorgemg.es                   │
│ Django Pass: [Ver .env.production - creado en paso] │
├─ ACCESO TÉCNICO ──────────────────────────────────────┤
│ SSH: ssh usuario@mcp.jorgemg.es                      │
│ Directorio: /opt/dealaai/AI4Devs-finalproject       │
│ Docker: docker-compose -f docker-compose.production  │
└────────────────────────────────────────────────────────┘
```

---

## 📊 ESTADÍSTICAS DE DEPLOYMENT

| Métrica              | Valor      |
| -------------------- | ---------- |
| Versión MVP          | 1.0.0      |
| Features Completadas | 10         |
| Servicios Docker     | 8          |
| Tiempo de Deploy     | ~2 horas   |
| Tiempo de Validación | 20 minutos |
| SLA Target           | 99% uptime |
| Backup Retention     | 30 días    |
| Healthcheck Interval | 5 minutos  |

---

## ✅ PRÓXIMOS PASOS

1. **Inmediato** (Después de deploy)

   - [ ] Monitorear logs durante 1 hora
   - [ ] Probar login/logout
   - [ ] Verificar stock data

2. **Hoy**

   - [ ] Validar backups funcionan
   - [ ] Probar restore (en ambiente de test)
   - [ ] Documentar acceso en equipo

3. **Esta Semana**

   - [ ] Testing con usuarios reales
   - [ ] Recopilar feedback
   - [ ] Bugfixes si aplican

4. **Próxima Versión (v1.1.0)**
   - [ ] Sistema de leads
   - [ ] Chat con IA
   - [ ] Reportes avanzados

---

**Versión**: 1.0.0-mvp
**Fecha**: 26 de Octubre, 2025
**Dominio**: https://mcp.jorgemg.es
**Status**: ✅ LISTO PARA DESPLEGAR
