# 🚀 Arquitectura de Producción Simplificada

## 📊 Comparación: Antes vs Ahora

### ❌ Arquitectura Anterior (Compleja)

```
┌─────────────────────────────────────────┐
│  Nginx Reverse Proxy                    │
│  ↓                                       │
│  ├── Frontend (Next.js)                 │
│  ├── Backend (Django + Gunicorn)        │
│  ├── PostgreSQL + pgvector              │
│  ├── Redis (cache + broker)             │
│  ├── Celery Worker                      │
│  ├── Celery Beat                        │
│  ├── pgAdmin                            │
│  ├── Supabase Auth                      │
│  ├── Supabase Studio                    │
│  └── Prometheus (métricas)              │
└─────────────────────────────────────────┘
Total: 11 servicios
Memoria: ~3GB
Build time: ~8 min
```

### ✅ Arquitectura Actual (Simplificada)

```
┌─────────────────────────────────────────┐
│  EasyPanel (Reverse Proxy + SSL)        │
│  ↓                                       │
│  ├── Frontend (Next.js) - Port 3000    │
│  ├── Backend (Django) - Port 8000      │
│  ├── PostgreSQL - Port 5432            │
│  └── pgAdmin - Port 5050 (opcional)    │
└─────────────────────────────────────────┘
Total: 4 servicios (3 esenciales)
Memoria: ~1GB
Build time: ~3 min
```

## 🎯 Servicios Eliminados y Razones

### 1. ❌ Nginx

- **Razón**: EasyPanel ya proporciona reverse proxy
- **Ahora**: Frontend y Backend exponen puertos directamente
- **Beneficio**: Menos configuración, logs más claros

### 2. ❌ Redis

- **Razón**: No necesitamos cache distribuido para MVP
- **Ahora**: Django usa cache en PostgreSQL
- **Beneficio**: Un servicio menos, menos RAM
- **Trade-off**: Cache ligeramente más lento (imperceptible para MVP)

### 3. ❌ Celery Worker + Beat

- **Razón**: No tenemos tareas asíncronas críticas aún
- **Ahora**: Tareas síncronas o polling simple
- **Beneficio**: 2 servicios menos, arquitectura más simple
- **Cuándo agregar**: Si necesitas envío masivo de emails, scraping, etc.

### 4. ❌ Supabase Auth + Studio

- **Razón**: Usamos autenticación Django nativa
- **Ahora**: Django REST Framework JWT
- **Beneficio**: 2 servicios menos, menos complejidad

### 5. ❌ Prometheus

- **Razón**: No necesitamos métricas avanzadas en MVP
- **Ahora**: Logs de Django + EasyPanel monitoring
- **Beneficio**: 1 servicio menos
- **Cuándo agregar**: Cuando necesites métricas personalizadas

## 📦 Servicios Actuales

### Frontend (Next.js) - Puerto 3000

```yaml
- Single-stage build (más simple)
- npm start (modo producción)
- Health check en /health
- Variables: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_DOMAIN
```

### Backend (Django) - Puerto 8000

```yaml
- Gunicorn WSGI server
- Cache en base de datos
- Static files servidos por Gunicorn
- Health check en /api/health/
```

### PostgreSQL - Puerto 5432

```yaml
- pgvector para embeddings
- Cache table para Django
- Backups automáticos (EasyPanel)
```

### pgAdmin - Puerto 5050 (Opcional)

```yaml
- Interface web para PostgreSQL
- Útil para debugging
- Puede deshabilitarse en producción
```

## 🔧 Configuración en EasyPanel

### 1. Variables de Entorno

Copia de `.env.production.example`:

```bash
DB_PASSWORD=<genera-con-secrets>
SECRET_KEY=<genera-con-secrets>
ALLOWED_HOSTS=mcp.jorgemg.es,backend,localhost
CORS_ALLOWED_ORIGINS=https://mcp.jorgemg.es
```

Generar claves:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 2. Configurar Dominios

- **Dominio Principal** → `frontend:3000`
- **Subdominio `/api`** → `backend:8000` (opcional)
- **Subdominio `/pgadmin`** → `pgadmin:80` (opcional)

### 3. Deploy

```bash
# Merge a main
git checkout main
git merge feature/TICK-002-user-auth
git push origin main

# En EasyPanel → Redeploy
```

## 🚀 Ventajas de la Simplificación

| Aspecto         | Antes      | Ahora    | Mejora            |
| --------------- | ---------- | -------- | ----------------- |
| **Servicios**   | 11         | 4        | ✅ -64%           |
| **RAM**         | ~3GB       | ~1GB     | ✅ -67%           |
| **Build time**  | ~8 min     | ~3 min   | ✅ -62%           |
| **Complejidad** | Alta       | Baja     | ✅ 80% más simple |
| **Debugging**   | Difícil    | Fácil    | ✅ Logs directos  |
| **Costos**      | $15-20/mes | $5-8/mes | ✅ -60%           |

## 📈 Cuándo Agregar Servicios

### Agregar Redis cuando:

- Más de 1000 usuarios concurrentes
- Cache distribuido necesario
- WebSockets en tiempo real
- Sesiones compartidas entre múltiples backends

### Agregar Celery cuando:

- Envío masivo de emails (>100/día)
- Procesamiento de archivos pesados
- Scraping/crawling de datos
- Tareas programadas complejas

### Agregar Nginx cuando:

- Necesitas configuración de proxy personalizada
- Rate limiting avanzado
- Load balancing entre múltiples backends
- EasyPanel no cubre tus necesidades

## 🔄 Cómo Agregar Redis Después

Si necesitas Redis en el futuro:

1. **Agregar servicio al docker-compose:**

```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
```

2. **Actualizar settings:**

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
    }
}
```

3. **Agregar al requirements.txt:**

```
redis==5.0.1
django-redis==5.4.0
```

## ✅ Checklist de Deployment

- [ ] Variables de entorno configuradas en EasyPanel
- [ ] Dominio apuntando a EasyPanel
- [ ] Merge a branch `main`
- [ ] Redeploy en EasyPanel
- [ ] Verificar frontend: https://mcp.jorgemg.es
- [ ] Verificar backend: https://mcp.jorgemg.es/api/health/
- [ ] Crear superusuario: `docker exec -it dealaai_backend_prod python manage.py createsuperuser`
- [ ] Verificar login funciona
- [ ] Verificar dashboard carga
- [ ] Verificar stock table funciona
- [ ] Configurar backups automáticos

## 🐛 Troubleshooting

### Error: "Database not ready"

```bash
# Verificar que DB_PASSWORD esté configurado
docker logs dealaai_db_prod
```

### Error: "Static files not found"

```bash
# El entrypoint ejecuta collectstatic automáticamente
# Si falla, revisar logs:
docker logs dealaai_backend_prod
```

### Error: Frontend no carga

```bash
# Verificar build de Next.js
docker logs dealaai_frontend_prod

# Verificar variables de entorno
echo $NEXT_PUBLIC_API_URL
```

### Error: "Cache table not found"

```bash
# Ejecutar manualmente
docker exec -it dealaai_backend_prod python manage.py createcachetable
```

## 📝 Notas Importantes

1. **No exponer puertos en docker-compose** - EasyPanel maneja el routing
2. **Variables de entorno** - Configurar en EasyPanel, no en docker-compose
3. **SSL/HTTPS** - EasyPanel lo maneja automáticamente
4. **Backups** - Configurar en EasyPanel para PostgreSQL
5. **Logs** - Disponibles en EasyPanel dashboard

## 🎓 Resumen Ejecutivo

Esta simplificación reduce la arquitectura de **11 servicios a 4**, manteniendo toda la funcionalidad del MVP:

- ✅ Autenticación JWT
- ✅ Dashboard y Stock Table
- ✅ API REST completa
- ✅ Persistencia de sesiones
- ✅ Manejo de archivos estáticos
- ✅ Base de datos con pgvector

**Trade-offs aceptables para MVP:**

- Cache ligeramente más lento (PostgreSQL vs Redis)
- No hay tareas asíncronas (Celery)
- Sin métricas avanzadas (Prometheus)

**Puedes agregar** cualquiera de estos servicios después cuando realmente los necesites, sin necesidad de reescribir código.

---

**Última actualización**: 26 de octubre de 2025
**Commit**: `8ca45a4` - Simplificación completa
