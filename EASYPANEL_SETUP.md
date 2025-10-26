# 🚀 DealaAI - Configuración para EasyPanel

Este archivo contiene toda la información necesaria para configurar DealaAI en EasyPanel con la arquitectura unificada bajo el dominio `mcp.jorgemg.es`.

## 🏗 Arquitectura del Sistema

```
https://mcp.jorgemg.es/
├── /                    → Frontend (Next.js)
├── /api/v1/            → Backend (Django REST API)
├── /admin/             → Django Admin Panel
├── /auth/              → Supabase Auth (GoTrue)
├── /pgadmin/           → pgAdmin Web Client
└── /studio/            → Supabase Studio
```

## 📦 Servicios en EasyPanel

### 1. Nginx (Reverse Proxy)

- **Puerto**: 80/443
- **Archivo de configuración**: `docker/nginx/nginx.conf`
- **Función**: Enrutar todas las peticiones a los servicios correspondientes

### 2. Frontend (Next.js)

- **Puerto interno**: 3000
- **Dockerfile**: `docker/frontend/Dockerfile.prod`
- **Variables de entorno necesarias**:
  ```env
  NODE_ENV=production
  NEXT_PUBLIC_API_URL=https://mcp.jorgemg.es/api/v1
  NEXT_PUBLIC_WS_URL=wss://mcp.jorgemg.es/ws
  NEXT_PUBLIC_DOMAIN=mcp.jorgemg.es
  ```

### 3. Backend (Django)

- **Puerto interno**: 8000
- **Dockerfile**: `docker/backend/Dockerfile.prod`
- **Variables de entorno necesarias**:
  ```env
  DJANGO_SETTINGS_MODULE=dealaai.settings.production
  DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/dealaai_prod
  REDIS_URL=redis://redis:6379/0
  SECRET_KEY=${SECRET_KEY}
  OPENAI_API_KEY=${OPENAI_API_KEY}
  ALLOWED_HOSTS=mcp.jorgemg.es,backend
  CORS_ALLOWED_ORIGINS=https://mcp.jorgemg.es
  DEBUG=False
  ```

### 4. PostgreSQL + pgvector

- **Puerto interno**: 5432
- **Imagen**: `ankane/pgvector:v0.5.1`
- **Variables de entorno**:
  ```env
  POSTGRES_DB=dealaai_prod
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=${DB_PASSWORD}
  ```

### 5. Redis

- **Puerto interno**: 6379
- **Imagen**: `redis:7.2-alpine`
- **Configuración**: `docker/redis/redis.conf`

### 6. Celery Worker & Beat

- **Función**: Tareas asíncronas y programadas
- **Misma imagen que el backend**

### 7. pgAdmin

- **Puerto interno**: 80
- **Ruta**: `/pgadmin/`
- **Variables de entorno**:
  ```env
  PGADMIN_DEFAULT_EMAIL=admin@mcp.jorgemg.es
  PGADMIN_DEFAULT_PASSWORD=${PGADMIN_PASSWORD}
  SCRIPT_NAME=/pgadmin
  ```

## 🔧 Configuración en EasyPanel

### Variables de Entorno Críticas

Configurar estas variables en el panel de control de EasyPanel:

```env
# Seguridad
SECRET_KEY=tu-secret-key-super-seguro-para-produccion
DB_PASSWORD=tu-password-postgresql-seguro
PGADMIN_PASSWORD=tu-password-pgadmin-seguro

# APIs
OPENAI_API_KEY=sk-tu-api-key-de-openai

# Opcionales para OAuth
GOOGLE_CLIENT_ID=tu-google-client-id
GOOGLE_CLIENT_SECRET=tu-google-client-secret
JWT_SECRET=tu-jwt-secret-super-seguro
```

### Comandos de Deployment

1. **Subir archivos del proyecto** a EasyPanel
2. **Configurar variables de entorno** en el panel
3. **Ejecutar deployment**:
   ```bash
   chmod +x scripts/deploy-easypanel.sh
   ./scripts/deploy-easypanel.sh
   ```

### Configuración de Dominio

1. **Configurar DNS** para que `mcp.jorgemg.es` apunte a tu servidor EasyPanel
2. **Habilitar SSL/TLS** automático en EasyPanel (Let's Encrypt)
3. **Verificar proxy settings** en EasyPanel para el puerto 80

## 🔍 Health Checks y Monitoreo

### Endpoints de Health Check

- **Nginx**: `https://mcp.jorgemg.es/health`
- **Frontend**: `https://mcp.jorgemg.es/` (página principal)
- **Backend**: `https://mcp.jorgemg.es/api/health/`
- **pgAdmin**: `https://mcp.jorgemg.es/pgadmin/`

### Logs de Servicios

```bash
# Ver logs de todos los servicios
docker-compose -f docker-compose.production.yml logs -f

# Logs específicos
docker-compose -f docker-compose.production.yml logs -f nginx
docker-compose -f docker-compose.production.yml logs -f backend
docker-compose -f docker-compose.production.yml logs -f frontend
```

## 🚨 Troubleshooting

### Problemas Comunes

1. **Error 502 Bad Gateway**

   - Verificar que los servicios internos estén corriendo
   - Revisar logs de nginx: `docker logs dealaai_nginx_prod`

2. **Frontend no carga**

   - Verificar variables de entorno de Next.js
   - Comprobar build: `docker-compose logs frontend`

3. **API no responde**

   - Verificar conexión a base de datos
   - Revisar migraciones: `docker-compose exec backend python manage.py showmigrations`

4. **pgAdmin no accesible**
   - Verificar variable `SCRIPT_NAME=/pgadmin`
   - Comprobar configuración de proxy en nginx

### Comandos de Diagnóstico

```bash
# Estado de servicios
docker-compose -f docker-compose.production.yml ps

# Test de conectividad interna
docker-compose -f docker-compose.production.yml exec nginx curl http://frontend:3000
docker-compose -f docker-compose.production.yml exec nginx curl http://backend:8000/api/health/

# Verificar base de datos
docker-compose -f docker-compose.production.yml exec db psql -U postgres -d dealaai_prod -c "\dt"

# Test de Redis
docker-compose -f docker-compose.production.yml exec redis redis-cli ping
```

## 📋 Checklist de Deployment

### Pre-deployment

- [ ] Variables de entorno configuradas en EasyPanel
- [ ] DNS configurado para `mcp.jorgemg.es`
- [ ] SSL/TLS habilitado
- [ ] Archivos del proyecto subidos

### Deployment

- [ ] Ejecutar `./scripts/deploy-easypanel.sh`
- [ ] Verificar que todos los servicios están UP
- [ ] Probar health checks
- [ ] Verificar acceso a todas las rutas

### Post-deployment

- [ ] Crear superusuario Django
- [ ] Configurar pgAdmin
- [ ] Cargar datos de ejemplo (opcional)
- [ ] Configurar monitoreo/alertas
- [ ] Backup inicial de base de datos

## 🔐 Seguridad

### Medidas Implementadas

- HTTPS obligatorio con redirección automática
- Headers de seguridad configurados en Nginx
- Rate limiting en APIs
- CORS restrictivo
- Cookies seguras
- Passwords hasheados con bcrypt
- Variables de entorno para secretos

### Recomendaciones Adicionales

1. **Cambiar passwords por defecto** inmediatamente
2. **Configurar backups automáticos** de la base de datos
3. **Habilitar logging y monitoreo** de seguridad
4. **Actualizar dependencias** regularmente
5. **Configurar alertas** para errores críticos

## 📞 Soporte

Si tienes problemas con la configuración:

1. Revisar los logs de servicios
2. Verificar variables de entorno
3. Comprobar conectividad de red entre contenedores
4. Consultar documentación de EasyPanel

---

**Última actualización**: Octubre 2025  
**Autor**: Jorge Martín García  
**Dominio**: mcp.jorgemg.es
