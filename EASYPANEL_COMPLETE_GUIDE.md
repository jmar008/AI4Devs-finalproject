# 🚀 Guía Completa: Despliegue en EasyPanel

## ⚠️ Problema: "Service is not reachable"

Este error ocurre cuando EasyPanel no puede acceder a los servicios. Las causas más comunes son:

1. **Healthchecks fallando** - Los contenedores no reportan estar "healthy"
2. **Puertos expuestos incorrectamente** - EasyPanel espera que los servicios escuchen en ciertos puertos
3. **Network issues** - Los contenedores no pueden comunicarse entre sí
4. **Volúmenes inaccesibles** - Permisos de archivos o rutas incorrectas

---

## 📋 Checklist Previo a Desplegar

### 1. Verificar Localmente

```powershell
# Desde la carpeta del proyecto
docker-compose -f docker-compose.easypanel.yml up -d

# Ver estado
docker-compose -f docker-compose.easypanel.yml ps

# Ver logs
docker-compose -f docker-compose.easypanel.yml logs -f
```

### 2. Validar Configuración

- ✅ El archivo `docker-compose.easypanel.yml` está en la raíz del proyecto
- ✅ Todos los Dockerfile existen y son válidos
- ✅ Las rutas de volúmenes son relativas (./backend, ./frontend, etc.)
- ✅ No hay caracteres especiales en nombres de servicios

---

## 🔧 Configuración de Variables de Entorno

En EasyPanel, debes establecer estas variables en el panel o crear un archivo `.env`:

```env
# Base de Datos
DB_NAME=dealaai_dev
DB_PASSWORD=postgres_secure_password_here
DB_USER=postgres

# Redis
REDIS_PASSWORD=redis_secure_password_here

# Django
SECRET_KEY=your-very-secure-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,api.your-domain.com
DEEPSEEK_API_KEY=sk-or-v1-your-api-key

# Frontend
NEXT_PUBLIC_API_URL=https://your-domain.com
NEXT_PUBLIC_ENVIRONMENT=production

# PgAdmin
PGADMIN_EMAIL=admin@dealaai.com
PGADMIN_PASSWORD=secure_pgadmin_password

# Django Settings
DJANGO_SETTINGS_MODULE=dealaai.settings.production
```

---

## 📝 Pasos de Despliegue en EasyPanel

### Paso 1: Preparar el Repositorio

```bash
# Asegúrate de que el proyecto esté en Git
git add .
git commit -m "Preparación para despliegue en EasyPanel"
git push origin main
```

### Paso 2: En EasyPanel - Crear Nuevo Proyecto

1. **Ir a Dashboard** → **Proyectos** → **+ Nuevo Proyecto**
2. **Seleccionar opción**: "Docker Compose"
3. **Conectar Repositorio Git**:
   - URL: `https://github.com/tu-usuario/AI4Devs-finalproject.git`
   - Branch: `main`
   - Token: Tu token de GitHub (si es privado)

### Paso 3: Configurar Docker Compose

1. **En EasyPanel**, selecciona:
   - **Docker Compose File**: `docker-compose.easypanel.yml`
   - **Nombre del Proyecto**: `dealaai`

### Paso 4: Configurar Variables de Entorno

1. **En EasyPanel**, ve a **Variables**
2. **Agrega todas las variables** del archivo `.env` anterior
3. **Importante**:
   - ✅ Cambiar `SECRET_KEY` por un valor seguro
   - ✅ Cambiar todas las contraseñas (`DB_PASSWORD`, `REDIS_PASSWORD`)
   - ✅ Establecer `DEBUG=False`
   - ✅ Configurar `ALLOWED_HOSTS` con tu dominio

### Paso 5: Configurar Puertos y Dominios

1. **Servicios Expuestos**:

   - **nginx** (Puerto 80 y 443)
     - Dominio: `your-domain.com` (ó apuntado por DNS)
   - **PgAdmin** (Puerto 5050 - opcional)

2. **En EasyPanel**:
   - Ve a **Puertos**
   - Configura nginx para puerto 80 (HTTP) y 443 (HTTPS)
   - SSL: Generar certificado Let's Encrypt

### Paso 6: Configurar Volúmenes

En EasyPanel, asegurate que estos volúmenes estén configurados:

```
postgres_data  → /var/lib/postgresql/data
redis_data     → /data
pgadmin_data   → /var/lib/pgadmin
```

### Paso 7: Desplegar

1. **Botón**: **Desplegar** o **Deploy**
2. **Esperar** a que todos los servicios se inicien (puede tomar 5-10 minutos)
3. **Ver logs** si algo falla

---

## 🔍 Solucionar "Service is not reachable"

### Opción 1: Revisar Logs

```bash
# En EasyPanel, en cada servicio:
# Abre la sección de Logs
# Busca errores como:
# - "Connection refused"
# - "Cannot find module"
# - "Migration failed"
```

### Opción 2: Verificar Healthchecks

```bash
# Los healthchecks deben pasar
# Ve a cada contenedor y verifica su estado:
# - "healthy" = ✅ OK
# - "unhealthy" = ❌ Problema
```

### Opción 3: Revisar Conectividad Entre Servicios

```bash
# Dentro de un contenedor:
docker exec dealaai_backend curl -f http://nginx/health/
docker exec dealaai_frontend curl -f http://backend:8000/health/
```

### Opción 4: Problemas Comunes

#### ❌ PostgreSQL no inicia

```
Solución:
- Verificar que postgres_data tiene permisos
- Ver logs: docker-compose logs db
```

#### ❌ Backend falla en migraciones

```
Solución:
- El backend ejecuta migraciones en startup
- Ver logs: docker-compose logs backend
- Esperar 1-2 minutos para que termine
```

#### ❌ Frontend no compila

```
Solución:
- Verificar que Node.js está disponible
- Ver logs: docker-compose logs frontend
- Podría tomar varios minutos en compilar Next.js
```

#### ❌ Nginx no puede contactar backend

```
Solución:
- Verificar que nginx.conf tiene upstreams correctos:
  upstream backend { server backend:8000; }
  upstream frontend { server frontend:3000; }
- Reiniciar nginx: docker-compose restart nginx
```

---

## 🆘 Comandos de Debugging en EasyPanel

### Ver Estado de Servicios

```bash
docker-compose -f docker-compose.easypanel.yml ps
```

### Ver Logs de Un Servicio

```bash
docker-compose -f docker-compose.easypanel.yml logs -f backend
docker-compose -f docker-compose.easypanel.yml logs -f frontend
docker-compose -f docker-compose.easypanel.yml logs -f nginx
```

### Acceder a Un Contenedor

```bash
docker-compose -f docker-compose.easypanel.yml exec backend bash
docker-compose -f docker-compose.easypanel.yml exec frontend sh
```

### Ejecutar Migraciones Manualmente

```bash
docker-compose -f docker-compose.easypanel.yml exec backend python manage.py migrate
docker-compose -f docker-compose.easypanel.yml exec backend python manage.py collectstatic --noinput
```

### Reiniciar un Servicio

```bash
docker-compose -f docker-compose.easypanel.yml restart backend
docker-compose -f docker-compose.easypanel.yml restart frontend
docker-compose -f docker-compose.easypanel.yml restart nginx
```

---

## 📊 Monitoreo en Producción

### Health Checks Configurados

Cada servicio tiene healthchecks que EasyPanel monitorea:

| Servicio     | Health Check     | Interval |
| ------------ | ---------------- | -------- |
| **db**       | `pg_isready`     | 10s      |
| **redis**    | `redis-cli ping` | 10s      |
| **backend**  | `curl /health/`  | 30s      |
| **frontend** | `curl /`         | 30s      |
| **nginx**    | `wget /`         | 30s      |

Si alguno falla 3 veces consecutivas, se marca como "unhealthy".

### Logs y Alertas

- **Logs**: Automáticamente guardados (max 10MB por archivo, 3 archivos)
- **Alertas**: Configura en EasyPanel si deseas notificaciones

---

## 🔐 Seguridad en Producción

### Cambios Obligatorios

1. **SECRET_KEY en Django**

   ```bash
   # Generar nuevo:
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **DEBUG=False**

   ```env
   DEBUG=False
   ```

3. **ALLOWED_HOSTS**

   ```env
   ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
   ```

4. **Contraseñas Seguras**

   - PostgreSQL: Cambiar `postgres` por contraseña fuerte
   - Redis: Establecer contraseña
   - PgAdmin: Cambiar credenciales

5. **SSL/TLS**

   - EasyPanel genera certificados Let's Encrypt automáticamente
   - Verificar que HTTPS está habilitado en nginx

6. **Firewall**
   - Solo exponer puertos 80 (HTTP) y 443 (HTTPS)
   - El puerto 5050 (PgAdmin) no debería estar público

---

## 🚀 Verificar Que Funciona

1. **Acceder a la aplicación**

   - https://tu-dominio.com
   - Debería cargar el frontend

2. **Login**

   - Ir a /login
   - Intentar login
   - Ver en Network → API calls si van a `/api/auth/users/login/`

3. **Admin Django**

   - https://tu-dominio.com/admin/
   - Debería cargar con estilos CSS

4. **Base de Datos**
   - https://tu-dominio.com:5050 (si PgAdmin está expuesto)
   - O acceder vía SSH + Port Forward

---

## 📞 Si Sigue Fallando

1. **Revisa logs** de cada contenedor
2. **Verifica networking** - ¿Los servicios pueden comunicarse?
3. **Chequea volúmenes** - ¿Hay permisos?
4. **Valida variables de entorno** - ¿Están todas configuradas?
5. **Prueba localmente primero** con `docker-compose.easypanel.yml`

---

## ✅ Checklist Final

- [ ] Docker Compose file: `docker-compose.easypanel.yml` ✓
- [ ] Variables de entorno configuradas en EasyPanel
- [ ] SECRET_KEY cambiado por valor seguro
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configurado
- [ ] Contraseñas cambiadas
- [ ] Dominio apuntando a EasyPanel (DNS A record)
- [ ] SSL/HTTPS habilitado
- [ ] Todos los servicios muestran "healthy"
- [ ] Frontend carga en dominio
- [ ] Login funciona
- [ ] Admin Django funciona

¡Una vez que tengas todo esto configurado, tu aplicación debería estar funcional en EasyPanel! 🎉
