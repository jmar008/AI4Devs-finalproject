# 🚀 REFERENCIA RÁPIDA - Desarrollo

## ⚡ Comandos Esenciales

### Iniciar Desarrollo

```powershell
cd c:\___apps___\all4devs\AI4Devs-finalproject
docker-compose up -d
```

### Ver Estado

```powershell
docker-compose ps
```

### Ver Logs

```powershell
docker-compose logs -f                # Todos
docker-compose logs -f backend        # Backend solo
docker-compose logs -f frontend       # Frontend solo
docker-compose logs -f nginx          # Nginx solo
```

### Parar Todo

```powershell
docker-compose down
```

### Limpiar (⚠️ borra base de datos)

```powershell
docker-compose down -v
```

---

## 🌐 Acceso a Servicios

| Servicio         | URL                          |
| ---------------- | ---------------------------- |
| **Aplicación**   | http://localhost:8080        |
| **Admin Django** | http://localhost:8080/admin/ |
| **PgAdmin**      | http://localhost:5050        |

---

## 🔑 Credenciales

| Servicio       | Usuario           | Contraseña |
| -------------- | ----------------- | ---------- |
| **Admin**      | admin             | admin123   |
| **PgAdmin**    | admin@dealaai.com | admin123   |
| **PostgreSQL** | postgres          | postgres   |

---

## 📝 Archivos `.env`

### Raíz (`.env`)

Variables globales para docker-compose. Se carga automáticamente.

### Backend (`backend/.env`)

Variables específicas de Django. Debe estar en `backend/` carpeta.

---

## 🤖 API Key OpenRouter

La key actual está **expirada**. Si necesitas chat:

1. https://openrouter.ai/keys
2. Crea nueva key
3. Actualiza `backend/.env`
4. `docker-compose restart backend`

---

## 🐳 Servicios

```
✅ PostgreSQL (db:5432)       → localhost:5433
✅ Redis (redis:6379)         → localhost:6380
✅ Django Backend (8000)      → interno
✅ Next.js Frontend (3000)    → interno
✅ Nginx (80/443)             → localhost:8080
✅ PgAdmin                    → localhost:5050
```

---

## ✅ Verificación Rápida

Todos deberían mostrar **healthy**:

```powershell
docker-compose ps
```

---

## 🐛 Problemas Comunes

### "Connection refused"

```powershell
docker-compose restart db
docker-compose restart backend
```

### "Port already in use"

Cambiar puerto en `docker-compose.yml` o matar proceso.

### "Frontend no carga"

```powershell
docker-compose up -d --build frontend
docker-compose logs frontend
```

### Variables de entorno no se cargan

```powershell
docker-compose down
docker-compose up -d
```

---

## 📚 Documentación

- `CONFIGURATION_SUMMARY.md` - Configuración completa
- `DEVELOPMENT_ENVIRONMENT_READY.md` - Estado del entorno
- `EASYPANEL_DEPLOYMENT_READY.md` - Desplegar en producción

---

## 💡 Tips

- **Hot reload**: Los cambios en código se reflejan automáticamente
- **Django admin**: Crear superusuario: `docker-compose exec backend python manage.py createsuperuser`
- **Base de datos**: Usar PgAdmin en http://localhost:5050
- **Migraciones**: `docker-compose exec backend python manage.py migrate`

---

**Cheat Sheet completo en `.env` comentado** 📄
