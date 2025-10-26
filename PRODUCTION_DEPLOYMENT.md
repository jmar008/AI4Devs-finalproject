╔══════════════════════════════════════════════════════════════════════════════╗
║ GUÍA DE DESPLIEGUE PRODUCCIÓN ║
║ EasyPanel + Docker ║
╚══════════════════════════════════════════════════════════════════════════════╝

🚀 DESPLIEGUE EN EASYPANEL - PASO A PASO
════════════════════════════════════════════════════════════════════════════════

REQUISITOS:
✅ Servidor con Docker y Docker Compose instalados
✅ Acceso a EasyPanel o CLI de Docker
✅ Dominio configurado (dealaai.com)
✅ SSL/HTTPS habilitado
✅ Base de datos PostgreSQL

1️⃣ PREPARAR ARCHIVO docker-compose.production.yml
════════════════════════════════════════════════════════════════════════════════

📁 /workspace/docker-compose.production.yml

El archivo ya existe con la configuración correcta:
• Backend (Django) en puerto 8000 (detrás de Nginx)
• Frontend (Next.js) en puerto 3000 (detrás de Nginx)
• PostgreSQL en puerto 5432 (no expuesto públicamente)
• Redis en puerto 6379 (no expuesto públicamente)
• Nginx en puerto 80/443

Variables de entorno a configurar:
• DJANGO_SETTINGS_MODULE=dealaai.settings.production
• DATABASE_URL=postgresql://user:password@db:5432/dealaai_prod
• REDIS_URL=redis://redis:6379/0
• SECRET_KEY=<GENERAR CON secrets.token_urlsafe()>
• DEBUG=False
• ALLOWED_HOSTS=dealaai.com,www.dealaai.com

2️⃣ CONFIGURAR VARIABLES DE ENTORNO
════════════════════════════════════════════════════════════════════════════════

Backend (.env.production):

DEBUG=False
SECRET_KEY=generado-con-secrets
ALLOWED_HOSTS=dealaai.com,www.dealaai.com
DJANGO_SETTINGS_MODULE=dealaai.settings.production

# Database

DATABASE_URL=postgresql://user:password@db:5432/dealaai_prod
DB_ENGINE=django.db.backends.postgresql
DB_NAME=dealaai_prod
DB_USER=dealaai_user
DB_PASSWORD=strong_password_here
DB_HOST=db
DB_PORT=5432

# Cache & Broker

REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0

# Security

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True

# CORS

CORS_ALLOWED_ORIGINS=https://dealaai.com,https://www.dealaai.com

# Email (para notificaciones)

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@dealaai.com
EMAIL_HOST_PASSWORD=app_password_here

# Celery Beat Schedule

CELERY_BEAT_SCHEDULE_STOCK_SCRAPER=True

Frontend (.env.production):

NEXT_PUBLIC_API_URL=https://api.dealaai.com/api
NEXT_PUBLIC_APP_NAME=DealaAI
NEXT_PUBLIC_APP_VERSION=1.0.0
NODE_ENV=production

3️⃣ CONFIGURAR NGINX COMO REVERSE PROXY
════════════════════════════════════════════════════════════════════════════════

📁 /workspace/docker/nginx/nginx.conf

Debe estar configurado para:

```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:3000;
}

server {
    listen 80;
    server_name dealaai.com www.dealaai.com;

    # Redirigir HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name dealaai.com www.dealaai.com;

    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/dealaai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dealaai.com/privkey.pem;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    gzip_min_length 1000;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts para uploads/scraping
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # Admin
    location /admin/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files (opcional)
    location /static/ {
        alias /app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files (opcional)
    location /media/ {
        alias /app/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
}
```

4️⃣ CERTIFICADOS SSL
════════════════════════════════════════════════════════════════════════════════

Opción 1: Let's Encrypt con Certbot (Recomendado)

```bash
# Instalar Certbot
apt-get install certbot python3-certbot-nginx

# Generar certificado
certbot certonly --standalone -d dealaai.com -d www.dealaai.com

# Auto-renovación
certbot renew --dry-run  # Test
certbot renew            # Real
```

Opción 2: Certificado Wildcard

```bash
certbot certonly --dns-cloudflare \
  -d "*.dealaai.com" \
  -d "dealaai.com"
```

Los certificados se guardarán en:
/etc/letsencrypt/live/dealaai.com/

5️⃣ CONFIGURAR BASE DE DATOS POSTGRESQL
════════════════════════════════════════════════════════════════════════════════

En el servidor:

```bash
# Crear base de datos
sudo -u postgres psql << EOF
CREATE DATABASE dealaai_prod;
CREATE USER dealaai_user WITH PASSWORD 'strong_password';
ALTER ROLE dealaai_user SET client_encoding TO 'utf8';
ALTER ROLE dealaai_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE dealaai_user SET default_transaction_deferrable TO on;
ALTER ROLE dealaai_user SET default_transaction_deferrable TO off;
ALTER ROLE dealaai_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE dealaai_prod TO dealaai_user;
ALTER DATABASE dealaai_prod OWNER TO dealaai_user;
\q
EOF

# Instalar pgvector para búsquedas de IA
psql -U dealaai_user -d dealaai_prod << EOF
CREATE EXTENSION IF NOT EXISTS vector;
\q
EOF
```

6️⃣ DEPLOYAR CON DOCKER COMPOSE
════════════════════════════════════════════════════════════════════════════════

```bash
# Descargar código
cd /home/dealaai
git clone https://github.com/jmar008/AI4Devs-finalproject.git
cd AI4Devs-finalproject

# Configurar variables de entorno
cp .env.example .env.production
# Editar .env.production con valores reales

# Crear directorios necesarios
mkdir -p static media logs

# Descargar imagen más reciente
docker-compose -f docker-compose.production.yml pull

# Levantar servicios
docker-compose -f docker-compose.production.yml up -d

# Ejecutar migraciones
docker-compose -f docker-compose.production.yml exec backend \
  python manage.py migrate --noinput

# Crear superusuario
docker-compose -f docker-compose.production.yml exec backend \
  python manage.py createsuperuser

# Recolectar static files
docker-compose -f docker-compose.production.yml exec backend \
  python manage.py collectstatic --noinput

# Ver logs
docker-compose -f docker-compose.production.yml logs -f
```

7️⃣ CONFIGURAR CELERY BEAT (Scraping automático)
════════════════════════════════════════════════════════════════════════════════

Celery Beat ejecutará automáticamente el scraper a las 01:00 AM.

En settings/production.py:

```python
CELERY_BEAT_SCHEDULE = {
    'scrape-stock-daily': {
        'task': 'apps.stock.tasks.scrape_stock_task',
        'schedule': crontab(hour=1, minute=0),  # 01:00 AM
        'args': (10, 1000)  # paginas, cantidad
    },
}
```

Verificar que Celery Beat está corriendo:

```bash
docker-compose -f docker-compose.production.yml logs celery_beat | tail -20
```

8️⃣ CONFIGURAR BACKUPS
════════════════════════════════════════════════════════════════════════════════

Script de backup automático (backup.sh):

```bash
#!/bin/bash

BACKUP_DIR="/backups/dealaai"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup Database
docker-compose -f docker-compose.production.yml exec -T db \
  pg_dump -U dealaai_user dealaai_prod | \
  gzip > "$BACKUP_DIR/db_$TIMESTAMP.sql.gz"

# Backup Media Files
tar -czf "$BACKUP_DIR/media_$TIMESTAMP.tar.gz" media/

# Cleanup old backups (keep last 30 days)
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete

echo "Backup completado: $TIMESTAMP"
```

CronTab (ejecutar diariamente a las 3 AM):

```
0 3 * * * cd /home/dealaai/AI4Devs-finalproject && bash backup.sh
```

9️⃣ MONITOREO Y ALERTAS
════════════════════════════════════════════════════════════════════════════════

Health Check Script:

```bash
#!/bin/bash

BACKEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
FRONTEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/health)

if [ "$BACKEND_HEALTH" != "200" ] || [ "$FRONTEND_HEALTH" != "200" ]; then
    # Enviar alerta por email
    echo "ALERTA: Servicios Down" | \
    mail -s "DealaAI Health Alert" admin@dealaai.com

    # Reiniciar servicios
    docker-compose -f docker-compose.production.yml restart
fi
```

CronTab (cada 5 minutos):

```
*/5 * * * * cd /home/dealaai/AI4Devs-finalproject && bash health_check.sh
```

🔟 ACTUALIZAR A NUEVA VERSIÓN
════════════════════════════════════════════════════════════════════════════════

```bash
cd /home/dealaai/AI4Devs-finalproject

# Detener servicios
docker-compose -f docker-compose.production.yml down

# Descargar cambios
git pull origin main

# Reconstruir imágenes
docker-compose -f docker-compose.production.yml build --no-cache

# Aplicar migraciones
docker-compose -f docker-compose.production.yml run --rm backend \
  python manage.py migrate

# Recolectar static files
docker-compose -f docker-compose.production.yml run --rm backend \
  python manage.py collectstatic --noinput

# Levantar servicios
docker-compose -f docker-compose.production.yml up -d

# Verificar
docker-compose -f docker-compose.production.yml ps
```

📊 CHECKLIST PRE-PRODUCCIÓN
════════════════════════════════════════════════════════════════════════════════

[ ] DEBUG = False en Django
[ ] SECRET_KEY generada aleatoriamente
[ ] ALLOWED_HOSTS configurado
[ ] SECURE_SSL_REDIRECT = True
[ ] CSRF_COOKIE_SECURE = True
[ ] SESSION_COOKIE_SECURE = True
[ ] Base de datos PostgreSQL creada
[ ] Certificados SSL/HTTPS instalados
[ ] Nginx reverse proxy configurado
[ ] Migraciones ejecutadas
[ ] Static files recolectados
[ ] Superusuario creado
[ ] Celery Beat corriendo
[ ] Backups configurados
[ ] Health checks configurados
[ ] Logs centralizados
[ ] Monitoreo activo

🆘 TROUBLESHOOTING PRODUCCIÓN
════════════════════════════════════════════════════════════════════════════════

❌ "502 Bad Gateway"
✅ Soluciones:

- Backend no está corriendo: docker-compose ps
- Migraciones pendientes: docker-compose exec backend python manage.py migrate
- Puertos incorrectos: verificar docker-compose.yml

❌ "Connection refused"
✅ Soluciones:

- PostgreSQL no conecta: verificar DATABASE_URL
- Redis no disponible: docker-compose exec redis redis-cli ping
- Firewall bloqueando: permitir puertos 80, 443

❌ "Static files not loading"
✅ Soluciones:

- Ejecutar: python manage.py collectstatic --noinput
- Verificar permisos: chmod -R 755 static/
- Nginx configurado para /static/

❌ "CORS errors"
✅ Soluciones:

- Verificar CORS_ALLOWED_ORIGINS en settings
- Frontend URL debe coincidir exactamente
- Cambiar a http://localhost:3000 en desarrollo

📝 LOGS
════════════════════════════════════════════════════════════════════════════════

Ver logs en tiempo real:

```bash
# Todos
docker-compose -f docker-compose.production.yml logs -f

# Backend
docker-compose -f docker-compose.production.yml logs -f backend

# Frontend
docker-compose -f docker-compose.production.yml logs -f frontend

# Nginx
docker-compose -f docker-compose.production.yml logs -f nginx

# Database
docker-compose -f docker-compose.production.yml logs -f db
```

🎯 URLS FINALES EN PRODUCCIÓN
════════════════════════════════════════════════════════════════════════════════

Frontend: https://dealaai.com
Login: https://dealaai.com/login
Dashboard: https://dealaai.com/dashboard
Stock: https://dealaai.com/dashboard/stock

API Swagger: https://dealaai.com/api/docs/
API ReDoc: https://dealaai.com/api/redoc/
Admin Panel: https://dealaai.com/admin/

════════════════════════════════════════════════════════════════════════════════
Fecha: 26 de Octubre, 2025
Versión: 1.0.0
Estado: ✅ LISTO PARA PRODUCCIÓN
════════════════════════════════════════════════════════════════════════════════
