# 🚀 DealaAI - Guía Rápida

## Servicios en EasyPanel

| Servicio                       | Local (Dev Container)         | Producción (EasyPanel)          | Descripción               |
| ------------------------------ | ----------------------------- | ------------------------------- | ------------------------- |
| **Frontend (Next.js)**         | http://localhost:3000/        | https://mcp.jorgemg.es/         | Interfaz principal        |
| **API (Django MCP)**           | http://localhost:8000/api/v1/ | https://mcp.jorgemg.es/api/v1/  | Endpoints del backend     |
| **Django Admin**               | http://localhost:8000/admin/  | https://mcp.jorgemg.es/admin/   | Panel administrativo      |
| **Supabase Auth (GoTrue)**     | http://localhost:9999/auth/   | https://mcp.jorgemg.es/auth/    | API de autenticación JWT  |
| **pgAdmin**                    | http://localhost:5050/        | https://mcp.jorgemg.es/pgadmin/ | Cliente web de PostgreSQL |
| **Supabase Studio**            | http://localhost:3001/        | https://mcp.jorgemg.es/studio/  | Panel oficial de Supabase |
| **Base de datos (PostgreSQL)** | localhost:5432                | supabase-db:5432 (interno)      | Motor de base de datos    |
| **Nginx (Proxy)**              | http://localhost/             | https://mcp.jorgemg.es/         | Proxy inverso unificado   |

## 🔧 Desarrollo Local

### DevContainer (Recomendado)

1. Abrir VS Code
2. F1 → "Dev Containers: Reopen in Container"
3. Esperar setup automático
4. Acceder a http://localhost (Nginx) o servicios directos

### Docker Compose Manual

```bash
git clone <repo>
cd AI4Devs-finalproject
docker-compose up -d
```

## 🚀 Deployment en EasyPanel

### 1. Configurar Variables de Entorno

```env
SECRET_KEY=tu-secret-key-super-seguro
DB_PASSWORD=tu-password-postgresql
OPENAI_API_KEY=sk-tu-api-key
PGADMIN_PASSWORD=tu-password-pgadmin
```

### 2. Ejecutar Deployment

```bash
chmod +x scripts/deploy-easypanel.sh
./scripts/deploy-easypanel.sh
```

### 3. Verificar Servicios

- ✅ https://mcp.jorgemg.es → Frontend
- ✅ https://mcp.jorgemg.es/api/v1 → API
- ✅ https://mcp.jorgemg.es/admin → Django Admin
- ✅ https://mcp.jorgemg.es/pgadmin → pgAdmin

## 📝 Credenciales por Defecto

| Servicio     | Usuario              | Password            |
| ------------ | -------------------- | ------------------- |
| Django Admin | admin@mcp.jorgemg.es | admin123            |
| pgAdmin      | admin@mcp.jorgemg.es | ${PGADMIN_PASSWORD} |
| PostgreSQL   | postgres             | ${DB_PASSWORD}      |

## 🛠 Comandos Útiles

### Desarrollo

```bash
# Ver logs
docker-compose logs -f

# Django commands
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py shell

# Frontend
docker-compose exec frontend npm run dev
docker-compose exec frontend npm test
```

### Producción

```bash
# Estado de servicios
docker-compose -f docker-compose.production.yml ps

# Logs
docker-compose -f docker-compose.production.yml logs -f nginx
docker-compose -f docker-compose.production.yml logs -f backend

# Restart
docker-compose -f docker-compose.production.yml restart

# Full rebuild
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up --build -d
```

## 🔍 Troubleshooting

### Error 502 Bad Gateway

1. Verificar que servicios backend estén UP
2. Revisar logs de nginx
3. Comprobar variables de entorno

### Frontend no carga

1. Verificar variables NEXT*PUBLIC*\*
2. Revisar logs del frontend
3. Comprobar build process

### API no responde

1. Verificar conexión a base de datos
2. Revisar migraciones Django
3. Comprobar Redis connection

## 📁 Archivos Importantes

- `docker-compose.yml` → Desarrollo local
- `docker-compose.production.yml` → Producción EasyPanel
- `docker/nginx/nginx.conf` → Proxy config producción
- `docker/nginx/nginx.dev.conf` → Proxy config desarrollo
- `.env.production` → Variables de entorno ejemplo
- `EASYPANEL_SETUP.md` → Guía completa de EasyPanel

## 🎯 Next Steps

1. **Implementar backend Django** según tickets documentados
2. **Desarrollar frontend NextJS** con componentes definidos
3. **Configurar sistema de IA** (RAG + OpenAI)
4. **Testing y debugging**
5. **Deploy a producción**

---

**Dominio producción**: https://mcp.jorgemg.es  
**Documentación completa**: Ver README.md y EASYPANEL_SETUP.md
