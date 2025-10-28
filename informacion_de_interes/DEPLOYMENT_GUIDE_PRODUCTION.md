# 🚀 GUÍA COMPLETA DE DESPLIEGUE A PRODUCCIÓN - DealaAI

## 📋 Estado Actual del Proyecto

**Versión**: 1.0.0 MVP
**Estado**: ✅ Listo para producción (mvp)

### ✅ Funcionalidades Completadas

- ✅ Autenticación de usuarios (Django + JWT Tokens)
- ✅ Login/Logout con persistencia de sesión
- ✅ Layout protegido con Sidebar y Topbar
- ✅ Ruta de Stock con tabla completa
- ✅ Vista detalle de vehículos
- ✅ Perfil de usuario
- ✅ Páginas placeholder (Leads, Chat, Settings)
- ✅ Dashboard con estadísticas
- ✅ Leyenda de tipos de stock
- ✅ Persistencia de sesión en recarga

---

## 🎯 PASOS PARA DESPLEGAR A PRODUCCIÓN

### PASO 1: Preparar el Código (30 minutos)

#### 1.1 - Hacer Commit de Cambios

```bash
cd /workspace
git status
git add -A
git commit -m "feat: MVP completado - autenticación, rutas protegidas y tabla stock"
git push origin feature/TICK-002-user-auth
```

#### 1.2 - Mergear a Main

```bash
git checkout main
git pull origin main
git merge feature/TICK-002-user-auth
git push origin main
```

#### 1.3 - Crear Tag de Versión

```bash
git tag -a v1.0.0-mvp -m "MVP Release - Autenticación y Stock System"
git push origin v1.0.0-mvp
```

---

### PASO 2: Preparar Variables de Entorno (15 minutos)

#### 2.1 - Crear archivo `.env.production` en raíz del proyecto

```bash
# DJANGO SETTINGS
DEBUG=False
DJANGO_SETTINGS_MODULE=dealaai.settings.production
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')

# ALLOWED HOSTS (actualizar con tu dominio)
ALLOWED_HOSTS=mcp.jorgemg.es,www.mcp.jorgemg.es,localhost,127.0.0.1

# DATABASE
DB_ENGINE=django.db.backends.postgresql
DB_NAME=dealaai_prod
DB_USER=dealaai_user
DB_PASSWORD=GenerarContraseniaFuerte123!
DB_HOST=db
DB_PORT=5432
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# CACHE & BROKER
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0

# SECURITY
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# CORS
CORS_ALLOWED_ORIGINS=https://mcp.jorgemg.es,https://www.mcp.jorgemg.es

# FRONTEND
NEXT_PUBLIC_API_URL=https://mcp.jorgemg.es/api
NEXT_PUBLIC_APP_NAME=DealaAI
NEXT_PUBLIC_APP_VERSION=1.0.0
NODE_ENV=production

# EMAIL (Opcional - para notificaciones)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@dealaai.com
EMAIL_HOST_PASSWORD=app_password_from_gmail

# OPENAI (Para futuras features de IA)
OPENAI_API_KEY=sk-tu-api-key-aqui

# PGADMIN
PGADMIN_DEFAULT_EMAIL=admin@mcp.jorgemg.es
PGADMIN_PASSWORD=PgAdminContraseniaFuerte123!
```

**⚠️ IMPORTANTE**:

- NO pushear este archivo a Git
- Guardar en servidor de producción de forma segura
- Usar variables de entorno del hosting en lugar de archivo

---

### PASO 3: Validar Configuración Backend (20 minutos)

#### 3.1 - Revisar Dockerfile.prod para Backend

```bash
cat docker/backend/Dockerfile.prod
```

Debe incluir:

- ✅ Etapa de compilación (builder)
- ✅ Etapa final con imagen ligera
- ✅ Colectar static files
- ✅ Usar gunicorn para servidor
- ✅ Healthcheck configurado

#### 3.2 - Revisar Dockerfile.prod para Frontend

```bash
cat docker/frontend/Dockerfile.prod
```

Debe incluir:

- ✅ Build de Next.js
- ✅ Etapa de production
- ✅ Variables NEXT*PUBLIC* configuradas
- ✅ Healthcheck configurado

#### 3.3 - Verificar settings/production.py

```bash
cat backend/dealaai/settings/production.py
```

Checklist:

- ✅ DEBUG = False
- ✅ ALLOWED_HOSTS desde variable
- ✅ SECURE_SSL_REDIRECT = True
- ✅ Conexión a PostgreSQL
- ✅ Redis configurado
- ✅ Static files en STATIC_ROOT
- ✅ Media files en MEDIA_ROOT

---

### PASO 4: Construir y Probar Imágenes Docker (30 minutos)

#### 4.1 - Construir imágenes localmente

```bash
cd /workspace

# Backend
docker build -f docker/backend/Dockerfile.prod \
  -t dealaai-backend:1.0.0-mvp \
  --build-arg DJANGO_SETTINGS_MODULE=dealaai.settings.production \
  ./backend

# Frontend
docker build -f docker/frontend/Dockerfile.prod \
  -t dealaai-frontend:1.0.0-mvp \
  --build-arg NODE_ENV=production \
  --build-arg NEXT_PUBLIC_API_URL=https://mcp.jorgemg.es/api \
  ./frontend
```

#### 4.2 - Verificar imágenes

```bash
docker images | grep dealaai
docker history dealaai-backend:1.0.0-mvp
docker history dealaai-frontend:1.0.0-mvp
```

#### 4.3 - Test de imagen (opcional)

```bash
# Test Backend
docker run --rm -it \
  -e DJANGO_SETTINGS_MODULE=dealaai.settings.production \
  dealaai-backend:1.0.0-mvp \
  python manage.py check

# Test Frontend
docker run --rm -it dealaai-frontend:1.0.0-mvp \
  npm run build --production
```

---

### PASO 5: Preparar Servidor de Producción (1 hora)

#### 5.1 - En el servidor remoto, crear directorio

```bash
ssh usuario@mcp.jorgemg.es

# Crear estructura
sudo mkdir -p /opt/dealaai
sudo mkdir -p /opt/dealaai/data/{postgres,redis,media,static,logs,backups}
sudo chown -R usuario:usuario /opt/dealaai
cd /opt/dealaai
```

#### 5.2 - Clonar repositorio en producción

```bash
git clone https://github.com/jmar008/AI4Devs-finalproject.git
cd AI4Devs-finalproject
git checkout v1.0.0-mvp
```

#### 5.3 - Copiar archivo .env.production

```bash
# Crear en servidor (NO en git)
cat > .env.production << 'EOF'
# Pegar contenido del archivo .env.production del PASO 2
EOF

chmod 600 .env.production
```

#### 5.4 - Crear volúmenes de Docker

```bash
docker volume create dealaai_postgres_data
docker volume create dealaai_redis_data
docker volume create dealaai_backend_media
docker volume create dealaai_backend_static
docker volume create dealaai_backend_logs
```

---

### PASO 6: Configurar Nginx y SSL (30 minutos)

#### 6.1 - Crear certificados SSL con Let's Encrypt

```bash
# En servidor de producción
sudo apt-get install certbot python3-certbot-nginx

# Generar certificado
sudo certbot certonly --standalone \
  -d mcp.jorgemg.es \
  -d www.mcp.jorgemg.es \
  --non-interactive \
  --agree-tos \
  -m admin@mcp.jorgemg.es
```

Certificados estarán en:

- `/etc/letsencrypt/live/mcp.jorgemg.es/fullchain.pem`
- `/etc/letsencrypt/live/mcp.jorgemg.es/privkey.pem`

#### 6.2 - Copiar certificados a directorio Docker

```bash
sudo cp /etc/letsencrypt/live/mcp.jorgemg.es/fullchain.pem \
  /opt/dealaai/docker/nginx/ssl/
sudo cp /etc/letsencrypt/live/mcp.jorgemg.es/privkey.pem \
  /opt/dealaai/docker/nginx/ssl/
sudo chmod 644 /opt/dealaai/docker/nginx/ssl/*
```

#### 6.3 - Verificar Nginx config

```bash
cat docker/nginx/nginx.conf
# Debe tener:
# - upstream backend (puerto 8000)
# - upstream frontend (puerto 3000)
# - redirección de HTTP a HTTPS
# - headers de seguridad
# - gzip compression
```

---

### PASO 7: Levantarlos Servicios (20 minutos)

#### 7.1 - Levantar con docker-compose en producción

```bash
cd /opt/dealaai/AI4Devs-finalproject

# Actualizar archivo con rutas correctas
export APP_ENV=production

# Levantar servicios
docker-compose -f docker-compose.production.yml up -d

# Verificar estatus
docker-compose -f docker-compose.production.yml ps
```

**Esperado:**

```
NAME                        STATUS
dealaai_nginx_prod          Up
dealaai_frontend_prod       Up
dealaai_backend_prod        Up
dealaai_db_prod             Up
dealaai_redis_prod          Up
dealaai_celery_worker_prod  Up
dealaai_celery_beat_prod    Up
```

#### 7.2 - Verificar logs

```bash
docker-compose -f docker-compose.production.yml logs -f
```

---

### PASO 8: Ejecutar Migraciones de Base de Datos (10 minutos)

#### 8.1 - Conectarse a backend

```bash
docker-compose -f docker-compose.production.yml exec backend bash
```

#### 8.2 - Ejecutar migraciones

```bash
python manage.py migrate --noinput
```

Esperado:

```
Running migrations:
  Applying authentication.0001_initial... OK
  Applying stock.0001_initial... OK
  ...
```

#### 8.3 - Crear superusuario

```bash
python manage.py createsuperuser

# Ingresar:
# Username: admin
# Email: admin@mcp.jorgemg.es
# Password: [Contraseña fuerte]
```

#### 8.4 - Recolectar static files

```bash
python manage.py collectstatic --noinput --clear
```

---

### PASO 9: Validar Despliegue (30 minutos)

#### 9.1 - Pruebas de Conectividad

```bash
# Frontend
curl -I https://mcp.jorgemg.es/

# API
curl -I https://mcp.jorgemg.es/api/

# Admin
curl -I https://mcp.jorgemg.es/admin/

# Health checks
curl https://mcp.jorgemg.es/api/health/
```

Esperado: Todos deben responder con 200

#### 9.2 - Verificar Servicios Backend

```bash
# Logs del backend
docker-compose -f docker-compose.production.yml logs backend | tail -50

# Verificar conexión a DB
docker-compose -f docker-compose.production.yml exec db \
  psql -U postgres -d dealaai_prod -c "SELECT 1"
```

#### 9.3 - Pruebas del Sistema

Abrir navegador y verificar:

1. **Login**: https://mcp.jorgemg.es/login

   - ✅ Página carga
   - ✅ Formulario de login visible
   - ✅ Sin errores en consola

2. **Autenticación**:

   - Ingresar credenciales de superusuario
   - ✅ Redirige a /dashboard
   - ✅ Token guardado en localStorage

3. **Sesión Persistente**:

   - F5 para recargar
   - ✅ Sesión se mantiene
   - ✅ No redirige a login

4. **Dashboard**:

   - ✅ Sidebar visible con menú
   - ✅ Topbar con usuario
   - ✅ Estadísticas cargadas

5. **Stock**:

   - Click en "Stock" en sidebar
   - ✅ Tabla carga con datos
   - ✅ Leyenda de tipos visible
   - ✅ Paginación funciona

6. **Rutas Protegidas**:
   - Ir a https://mcp.jorgemg.es/stock
   - ✅ Carga correctamente
   - Layout se mantiene al navegar
   - ✅ Logout funciona

#### 9.4 - Verificar Performance

```bash
# Medir tiempo de respuesta
time curl https://mcp.jorgemg.es/api/

# Ver tamaño de respuesta
curl -i https://mcp.jorgemg.es/ | head -20
```

---

### PASO 10: Configurar Backups y Monitoreo (20 minutos)

#### 10.1 - Script de Backup Diario

```bash
cat > /opt/dealaai/backup.sh << 'EOF'
#!/bin/bash
set -e

BACKUP_DIR="/opt/dealaai/data/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DAYS_KEEP=30

# Crear backup de DB
docker-compose -f docker-compose.production.yml exec -T db \
  pg_dump -U postgres dealaai_prod | gzip > \
  "$BACKUP_DIR/db_$TIMESTAMP.sql.gz"

# Backup de media files
tar -czf "$BACKUP_DIR/media_$TIMESTAMP.tar.gz" \
  -C /opt/dealaai/data media/

# Limpiar backups antiguos
find "$BACKUP_DIR" -name "*.gz" -mtime +$DAYS_KEEP -delete

echo "[$(date)] Backup completado: $TIMESTAMP"
EOF

chmod +x /opt/dealaai/backup.sh
```

#### 10.2 - Agregar a CronTab

```bash
crontab -e

# Agregar línea:
0 3 * * * /opt/dealaai/backup.sh >> /opt/dealaai/data/logs/backup.log 2>&1
```

#### 10.3 - Script de Healthcheck

```bash
cat > /opt/dealaai/healthcheck.sh << 'EOF'
#!/bin/bash

BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://mcp.jorgemg.es/api/health/ || echo "000")
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://mcp.jorgemg.es/ || echo "000")

if [ "$BACKEND_STATUS" != "200" ] || [ "$FRONTEND_STATUS" != "200" ]; then
    echo "⚠️ ALERTA: Backend=$BACKEND_STATUS Frontend=$FRONTEND_STATUS"

    # Intentar reiniciar
    docker-compose -f docker-compose.production.yml restart

    sleep 30

    # Verificar nuevamente
    BACKEND_RETRY=$(curl -s -o /dev/null -w "%{http_code}" https://mcp.jorgemg.es/api/health/ || echo "000")

    if [ "$BACKEND_RETRY" != "200" ]; then
        # Enviar alerta por email (requiere mailutils instalado)
        echo "DealaAI servicios DOWN - Backend: $BACKEND_RETRY" | \
        mail -s "🚨 ALERTA PRODUCCIÓN" admin@mcp.jorgemg.es
    fi
fi

echo "[$(date)] Healthcheck: Backend=$BACKEND_STATUS Frontend=$FRONTEND_STATUS"
EOF

chmod +x /opt/dealaai/healthcheck.sh
```

#### 10.4 - Agregar Healthcheck a CronTab

```bash
# Ejecutar cada 5 minutos
*/5 * * * * /opt/dealaai/healthcheck.sh >> /opt/dealaai/data/logs/healthcheck.log 2>&1
```

---

### PASO 11: Documentar Acceso a Producción (10 minutos)

#### 11.1 - Crear archivo de acceso

````bash
cat > /opt/dealaai/PRODUCTION_ACCESS.md << 'EOF'
# 🚀 Acceso a Producción - DealaAI v1.0.0-mvp

## URLs Públicas

- **Frontend**: https://mcp.jorgemg.es/
- **Login**: https://mcp.jorgemg.es/login
- **Dashboard**: https://mcp.jorgemg.es/dashboard
- **API Docs**: https://mcp.jorgemg.es/api/docs/
- **Admin Panel**: https://mcp.jorgemg.es/admin/

## Credenciales

### Superusuario Django
- Email: admin@mcp.jorgemg.es
- Usuario: admin
- Password: [Ver .env.production]

### pgAdmin
- Email: admin@mcp.jorgemg.es
- Password: [Ver .env.production - PGADMIN_PASSWORD]

## SSH Access

```bash
ssh usuario@mcp.jorgemg.es
cd /opt/dealaai/AI4Devs-finalproject
````

## Docker Compose Commands

```bash
# Ver estado
docker-compose -f docker-compose.production.yml ps

# Logs
docker-compose -f docker-compose.production.yml logs -f

# Reiniciar
docker-compose -f docker-compose.production.yml restart

# Stop/Start
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d
```

## Versión Deployada

- Version: v1.0.0-mvp
- Commit: [Ver git log]
- Deploy Date: 2025-10-26
- Status: ✅ PRODUCCIÓN

## Features

✅ Autenticación con JWT Tokens
✅ Rutas protegidas
✅ Tabla de Stock
✅ Dashboard
✅ Perfil de usuario
✅ Persistencia de sesión
✅ Reverse proxy Nginx
✅ SSL/HTTPS

## Monitoring

- Health checks: Cada 5 minutos
- Backups: Diarios a las 3 AM
- Logs: Docker Compose
- Status: https://mcp.jorgemg.es/api/health/

EOF

cat /opt/dealaai/PRODUCTION_ACCESS.md

```

---

## ✅ CHECKLIST FINAL PRE-PRODUCCIÓN

```

CÓDIGO Y VERSIONES
☐ Código commiteado en main
☐ Tag v1.0.0-mvp creado
☐ README actualizado

CONFIGURACIÓN
☐ .env.production creado con todas las variables
☐ DEBUG = False en Django
☐ SECRET_KEY generado aleatoriamente
☐ ALLOWED_HOSTS configurado
☐ CORS_ALLOWED_ORIGINS correcto

DOCKER Y SERVICIOS
☐ Imágenes construidas localmente
☐ docker-compose.production.yml validado
☐ Volúmenes creados en servidor
☐ SSL/HTTPS certificados instalados
☐ Nginx configurado como reverse proxy

BASE DE DATOS
☐ PostgreSQL iniciada
☐ Base de datos creada (dealaai_prod)
☐ Migraciones ejecutadas
☐ Superusuario creado
☐ Static files recolectados

SERVICIOS VERIFICADOS
☐ Frontend responde (puerto 3000)
☐ Backend responde (puerto 8000)
☐ Nginx responde (puertos 80/443)
☐ PostgreSQL conecta
☐ Redis funciona
☐ Celery worker activo

VALIDACIONES FUNCIONALES
☐ Login funciona
☐ Sesión persiste en recarga
☐ Rutas protegidas redirigen correctamente
☐ Stock tabla carga datos
☐ Dashboard muestra info
☐ Logout limpia sesión
☐ URLs públicas accesibles

MONITOREO Y BACKUPS
☐ Script de backup creado
☐ CronTab backup configurado (3 AM diariamente)
☐ Healthcheck script creado
☐ CronTab healthcheck configurado (cada 5 min)
☐ Logging centralizado

DOCUMENTACIÓN
☐ PRODUCTION_ACCESS.md creado
☐ Credenciales documentadas de forma segura
☐ Proceso de update documentado
☐ Troubleshooting documentado

````

---

## 🆘 TROUBLESHOOTING EN PRODUCCIÓN

### Error 502 Bad Gateway

```bash
# 1. Verificar servicios
docker-compose -f docker-compose.production.yml ps

# 2. Ver logs de backend
docker-compose -f docker-compose.production.yml logs backend | tail -50

# 3. Conectar al backend
docker-compose -f docker-compose.production.yml exec backend bash
python manage.py check

# 4. Verificar migraciones
python manage.py migrate --plan

# 5. Si problema persiste, reiniciar
docker-compose -f docker-compose.production.yml restart backend
````

### Frontend no carga

```bash
# 1. Ver logs frontend
docker-compose -f docker-compose.production.yml logs frontend | tail -50

# 2. Verificar BUILD_ID
docker-compose -f docker-compose.production.yml exec frontend \
  cat .next/BUILD_ID

# 3. Rebuild si es necesario
docker-compose -f docker-compose.production.yml up -d --build frontend
```

### Static files no cargan

```bash
# 1. Ejecutar collectstatic
docker-compose -f docker-compose.production.yml exec backend \
  python manage.py collectstatic --noinput

# 2. Verificar permisos
docker volume inspect dealaai_backend_static

# 3. Limpiar y reconstruir
docker-compose -f docker-compose.production.yml exec backend \
  python manage.py collectstatic --noinput --clear
```

### Base de datos no conecta

```bash
# 1. Verificar estado de PostgreSQL
docker-compose -f docker-compose.production.yml exec db \
  pg_isready

# 2. Conectarse a DB
docker-compose -f docker-compose.production.yml exec db \
  psql -U postgres -d dealaai_prod

# 3. Verificar DATABASE_URL
echo $DATABASE_URL
```

---

## 📞 SOPORTE Y ESCALABILIDAD

### Para Agregar Más Funcionalidades

1. Desarrollar en rama `feature/`
2. Probar localmente
3. Hacer PR a `develop`
4. Mergear a `main`
5. Crear nuevo tag
6. Repetir PASO 7 y 9

### Monitoreo Avanzado

Considerá agregar en el futuro:

- Prometheus para métricas
- Grafana para dashboards
- Sentry para error tracking
- DataDog o New Relic para APM

### Escalabilidad Horizontal

Cuando crezca el tráfico:

- Agregar más workers Celery
- Usar load balancer (AWS ALB)
- Escalar base de datos (RDS)
- Usar CDN para assets estáticos

---

## 📅 PRÓXIMOS PASOS DESPUÉS DEL DEPLOY

1. **Monitorear en tiempo real**

   - Revisar logs diariamente
   - Verificar health checks
   - Monitorear performance

2. **Recopilar feedback**

   - Testing con usuarios reales
   - Bugs y issues encontrados

3. **Desarrollo Iterativo**

   - Bugfixes rápidos
   - Mejoras pequeñas
   - Optimización de performance

4. **Próxima Versión (v1.1.0)**
   - Sistema de leads completo
   - Chat con IA
   - Reportes avanzados

---

**Fecha**: 26 de Octubre, 2025
**Versión**: 1.0.0-mvp
**Status**: ✅ Listo para desplegar a producción
**Dominio**: https://mcp.jorgemg.es
