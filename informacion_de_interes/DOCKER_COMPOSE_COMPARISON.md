# 📊 Comparación: docker-compose.yml vs docker-compose.easypanel.yml

## 🎯 Diferencias Principales

### Propósito

| Aspecto         | `docker-compose.yml` | `docker-compose.easypanel.yml` |
| --------------- | -------------------- | ------------------------------ |
| **Uso**         | Desarrollo local     | Producción en EasyPanel        |
| **Debug**       | Máximo (DEBUG=True)  | Deshabilitado (DEBUG=False)    |
| **Performance** | Desarrollo           | Optimizado                     |
| **Logs**        | Ilimitados           | Limitados (10MB max)           |

---

## 🔍 Cambios Específicos

### 1. Puertos (Networking)

#### docker-compose.yml (Desarrollo)

```yaml
# Frontend: 3000 del contenedor → 3001 del host
ports:
  - "3001:3000"

# Backend: 8000 del contenedor → 8000 del host
ports:
  - "8000:8000"

# Nginx: 80 del contenedor →  del host
ports:
  - ":80"
  - "8443:443"

# PgAdmin: 80 del contenedor → 5050 del host
ports:
  - "5050:80"
```

#### docker-compose.easypanel.yml (Producción)

```yaml
# Frontend: Solo expose (sin ports)
expose:
  - "3000"

# Backend: Solo expose (sin ports)
expose:
  - "8000"

# Nginx: Puerto 80 y 443 directamente
ports:
  - "80:80"
  - "443:443"

# PgAdmin: Solo expose
expose:
  - "80"
```

**¿Por qué el cambio?**

- Desarrollo: Necesitas acceso directo desde localhost
- Producción: Todo va a través de nginx (puerto 80/443)
- EasyPanel: Gestiona los puertos automáticamente

### 2. Variables de Entorno

#### docker-compose.yml (Desarrollo)

```yaml
environment:
  - DJANGO_SETTINGS_MODULE=dealaai.settings.development # Configuración DEV
  - DATABASE_URL=postgresql://...@db:5432/...
  - DEBUG=True # ✅ Debug habilitado
  - NEXT_PUBLIC_API_URL=http://localhost: # Localhost
```

#### docker-compose.easypanel.yml (Producción)

```yaml
environment:
  - DJANGO_SETTINGS_MODULE=dealaai.settings.production # Configuración PROD
  - DATABASE_URL=postgresql://...@db:5432/...
  - DEBUG=${DEBUG:-False} # ✅ Debug deshabilitado por defecto
  - ALLOWED_HOSTS=${ALLOWED_HOSTS:-localhost} # Configurable
  - SECRET_KEY=${SECRET_KEY:-...} # Obligatorio cambiar
  - NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL:-...} # Desde variable
```

### 3. Health Checks

#### docker-compose.yml (Desarrollo)

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
  interval: 30s
  timeout: 10s
  retries: 3
  # sin start_period
```

#### docker-compose.easypanel.yml (Producción)

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s # ✅ Tiempo para inicializar
```

**¿Por qué el cambio?**

- En EasyPanel, los servicios necesitan más tiempo para iniciar
- `start_period` evita falsos positivos de "unhealthy" durante el inicio

### 4. Volúmenes

#### docker-compose.yml (Desarrollo)

```yaml
volumes:
  - ./backend:/app:cached # Todo sincronizado
  - ./frontend:/app:cached # Hot reload habilitado
  - postgres-data:/var/lib/postgresql/data
  - redis-data:/data
```

#### docker-compose.easypanel.yml (Producción)

```yaml
volumes:
  - ./backend:/app:cached # Sincronizado (pueden cambiar archivos)
  - ./frontend:/app:cached # Sincronizado
  - postgres_data:/var/lib/postgresql/data # Sin "_"
  - redis_data:/data # Sin "_"
  - /app/.next # Cache de Next.js
  - /app/node_modules # Dependencias node
```

**¿Por qué el cambio?**

- EasyPanel gestiona volúmenes de forma diferente
- Nombres simples evitan conflictos
- Se agregan volúmenes para caché (performance)

### 5. Restart Policy

#### docker-compose.yml (Desarrollo)

```yaml
restart: unless-stopped
```

#### docker-compose.easypanel.yml (Producción)

```yaml
restart: always
```

**¿Por qué el cambio?**

- Producción: Recuperarse de fallos automáticamente
- EasyPanel: El `always` es más confiable

### 6. Logging

#### docker-compose.yml (Desarrollo)

```yaml
# Sin configuración explícita
# Logs ilimitados, todo va a stdout/stderr
```

#### docker-compose.easypanel.yml (Producción)

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

**¿Por qué el cambio?**

- Desarrollo: Logs ilimitados = más debugging
- Producción: Rotación automática = evita llenar el disco

### 7. Dependencias

#### docker-compose.yml (Desarrollo)

```yaml
depends_on:
  db:
    condition: service_healthy # Espera a health check
  redis:
    condition: service_healthy
```

#### docker-compose.easypanel.yml (Producción)

```yaml
depends_on:
  db:
    condition: service_healthy # Igual
  redis:
    condition: service_healthy
```

**No cambió**, pero es crítico que esté presente

### 8. Container Names

#### docker-compose.yml

```yaml
container_name: dealaai_frontend
container_name: dealaai_backend
container_name: dealaai_db
```

#### docker-compose.easypanel.yml

```yaml
container_name: dealaai_frontend  # Igual
container_name: dealaai_backend
container_name: dealaai_db
```

**Mismo** - Los nombres facilitan debugging

---

## 📋 Checklist de Cambios

Cuando migres de desarrollo a producción, verifica:

### Archivos Sincronizados

- [ ] `docker-compose.yml` - Desarrollo
- [ ] `docker-compose.easypanel.yml` - Producción
- [ ] `.env.development` - Desarrollo local
- [ ] `.env.easypanel.example` - Plantilla producción

### Variables de Entorno

- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` diferente en producción
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] `NEXT_PUBLIC_API_URL` apunta al dominio público

### Seguridad

- [ ] SSL/HTTPS configurado
- [ ] Contraseñas fuertes (DB, Redis, PgAdmin)
- [ ] Puertos privados expuestos solo donde necesario
- [ ] Database backups configurados

### Performance

- [ ] Logging limitado
- [ ] Health checks configurados
- [ ] Restart policies apropiadas
- [ ] Volúmenes optimizados

---

## 🚀 Cuándo Usar Cada Uno

### Usa `docker-compose.yml` Si:

- ✅ Estás desarrollando localmente
- ✅ Necesitas hot reload
- ✅ Quieres ver todos los logs
- ✅ Cambios frecuentes en código

```bash
docker-compose -f docker-compose.yml up -d
```

### Usa `docker-compose.easypanel.yml` Si:

- ✅ Desplegando en EasyPanel
- ✅ Ambiente de producción
- ✅ Necesitas performance optimizado
- ✅ Seguridad crítica

```bash
docker-compose -f docker-compose.easypanel.yml up -d
```

---

## 🔄 Sincronización de Cambios

Si cambias la arquitectura, **recuerda actualizar ambos archivos**:

1. **Cambio en `docker-compose.yml`** (desarrollo)

   ```bash
   # Copia el cambio a docker-compose.easypanel.yml
   # Pero adapta para producción
   ```

2. **Cambio en servicios/puertos/volúmenes**

   ```bash
   # Necesita estar en ambos archivos
   ```

3. **Cambio en variables de entorno**
   ```bash
   # Actualiza ambos
   # Y actualiza .env.easypanel.example
   ```

---

## 💡 Migración: Dev → Prod

Pasos para migrar correctamente:

### 1. Testear en Development

```bash
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml ps  # Todo debe estar healthy
```

### 2. Copiar Cambios a Production

```bash
# Toma los cambios del docker-compose.yml
# Adáptalos para producción
# Crea docker-compose.easypanel.yml
```

### 3. Testear Production Localmente

```bash
docker-compose -f docker-compose.easypanel.yml up -d
docker-compose -f docker-compose.easypanel.yml ps  # Todo debe estar healthy
```

### 4. Actualizar Variables

```bash
# Copia .env a .env.production
# Cambia:
# - DEBUG=False
# - SECRET_KEY (nueva)
# - ALLOWED_HOSTS (tu dominio)
# - Contraseñas (más fuertes)
```

### 5. Desplegar en EasyPanel

```bash
# Git push
# EasyPanel deploy
# Monitorear logs
```

---

## 🎓 Resumen

| Criterio          | Desarrollo             | Producción                     |
| ----------------- | ---------------------- | ------------------------------ |
| **Archivo**       | `docker-compose.yml`   | `docker-compose.easypanel.yml` |
| **DEBUG**         | True                   | False                          |
| **Puertos**       | , 3001, 8000, etc. | 80, 443                        |
| **Logs**          | Ilimitados             | Rotados                        |
| **Health Checks** | Sin start_period       | Con start_period               |
| **Restart**       | unless-stopped         | always                         |
| **Acceso**        | localhost:         | dominio.com                    |

**Ambos archivos son necesarios** - Cada uno optimizado para su caso de uso.
