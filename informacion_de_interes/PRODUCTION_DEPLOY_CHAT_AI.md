# 📋 CONFIGURACIÓN PARA PRODUCCIÓN - Chat AI

## ✅ Cambios Realizados

### 1. **docker-compose.production.yml**

- ✅ Idéntico a desarrollo
- ✅ Usa los mismos servicios (db, redis, backend, frontend, celery_worker, celery_beat, nginx)
- ✅ Solo diferencias: nombres de contenedores (\_prod) y archivos .env

### 2. **backend/.env.production**

- ✅ Actualizado con `DEEPSEEK_API_KEY` en lugar de `OPENAI_API_KEY`
- ⚠️ **IMPORTANTE**: Reemplazar `your-production-deepseek-api-key` con tu API key real

### 3. **requirements.txt**

- ✅ Actualizado a `openai==1.55.0`

### 4. **settings/base.py**

- ✅ DEEPSEEK_API_BASE = `https://api.deepseek.com/v1` (corregido)

---

## 🚀 ANTES DE DESPLEGAR A PRODUCCIÓN

### **PASO 1: Configurar Variables de Entorno**

Edita `/workspace/backend/.env.production` y actualiza:

```bash
# CAMBIAR ESTOS VALORES:
SECRET_KEY=tu-secret-key-super-segura-generada-aleatoriamente
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DB_PASSWORD=tu-password-de-base-de-datos-segura
DEEPSEEK_API_KEY=sk-tu-api-key-de-deepseek-real
CORS_ALLOWED_ORIGINS=https://tu-dominio.com

# Email (opcional):
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-de-app
```

### **PASO 2: Configurar Frontend**

Edita `/workspace/frontend/.env.local.production`:

```bash
NEXT_PUBLIC_API_URL=https://tu-dominio.com/api
```

---

## 🔧 COMANDOS PARA DESPLEGAR

### **Desarrollo (local):**

```bash
# Reconstruir contenedores con nuevas dependencias
docker-compose down
docker-compose build --no-cache backend celery_worker celery_beat
docker-compose up -d

# Ver logs
docker-compose logs -f backend
```

### **Producción:**

```bash
# Reconstruir contenedores
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml build --no-cache backend celery_worker celery_beat
docker-compose -f docker-compose.production.yml up -d

# Ver logs
docker-compose -f docker-compose.production.yml logs -f backend
```

---

## 📊 Servicios que se Ejecutan

**Ambos entornos (dev y prod) ejecutan:**

1. **PostgreSQL** (con pgvector)

   - Puerto: 5432
   - Imagen: `ankane/pgvector:latest`

2. **Redis**

   - Puerto: 6379
   - Imagen: `redis:7-alpine`

3. **Backend (Django)**

   - Puerto: 8000
   - Comando: `python manage.py runserver 0.0.0.0:8000`
   - Incluye: API Chat IA con DeepSeek

4. **Frontend (Next.js)**

   - Puerto: 3000
   - Comando: `npm run dev`

5. **Celery Worker**

   - Tareas asíncronas
   - Migración diaria de stock

6. **Celery Beat**

   - Scheduler de tareas programadas
   - Ejecuta migración a las 01:00 AM

7. **Nginx**
   - Puerto: 80
   - Reverse proxy

---

## 🔍 Verificación Post-Despliegue

### **1. Verificar que todos los servicios están corriendo:**

```bash
docker-compose ps
# o en producción:
docker-compose -f docker-compose.production.yml ps
```

Todos deben mostrar `Up` y `healthy`.

### **2. Verificar logs del backend:**

```bash
docker-compose logs backend | grep -i "deepseek\|chat"
```

Deberías ver:

- ✅ No errores de importación de `openai`
- ✅ No errores de `DEEPSEEK_API_KEY`

### **3. Probar el Chat AI:**

1. Accede a la aplicación
2. Haz login
3. Verás el botón flotante azul en la esquina inferior derecha
4. Haz clic y envía un mensaje de prueba
5. La IA debería responder con información del stock

### **4. Verificar healthchecks:**

```bash
# Backend
curl http://localhost:8000/api/health/

# Frontend
curl http://localhost:3000
```

---

## ⚠️ TROUBLESHOOTING

### **Error: "DEEPSEEK_API_KEY no está configurada"**

- Verifica que `.env.production` contiene la key
- Reinicia el contenedor: `docker-compose restart backend`

### **Error: "Client.**init**() got an unexpected keyword argument 'proxies'"**

- Verifica que `openai==1.55.0` está en requirements.txt
- Reconstruye la imagen: `docker-compose build --no-cache backend`

### **Chat no aparece en el frontend**

- Verifica que el frontend está en una ruta protegida
- Revisa la consola del navegador (F12)
- Verifica que el backend responde: `curl http://localhost:8000/api/chat/stock-summary/`

### **Error de CORS**

- Verifica CORS_ALLOWED_ORIGINS en `.env.production`
- Debe incluir el dominio del frontend

---

## 📝 DIFERENCIAS DESARROLLO vs PRODUCCIÓN

| Aspecto              | Desarrollo           | Producción                      |
| -------------------- | -------------------- | ------------------------------- |
| Archivo compose      | `docker-compose.yml` | `docker-compose.production.yml` |
| Env backend          | `.env`               | `.env.production`               |
| Env frontend         | `.env.local`         | `.env.local.production`         |
| DEBUG                | `True`               | `False`                         |
| SECRET_KEY           | Simple               | Compleja y segura               |
| DB Password          | `postgres`           | Segura                          |
| Nombres contenedores | `dealaai_*`          | `dealaai_*_prod`                |
| HTTPS                | No                   | Sí (recomendado)                |

---

## 🎯 CHECKLIST PRE-DEPLOY

- [ ] API Key de DeepSeek obtenida y configurada
- [ ] SECRET_KEY generada (usar `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- [ ] DB_PASSWORD configurada
- [ ] ALLOWED_HOSTS actualizado con dominio real
- [ ] CORS_ALLOWED_ORIGINS actualizado
- [ ] Frontend .env actualizado con URL del backend
- [ ] Migraciones ejecutadas: `docker-compose exec backend python manage.py migrate`
- [ ] Archivos estáticos recolectados: `docker-compose exec backend python manage.py collectstatic --noinput`
- [ ] Superusuario creado: `docker-compose exec backend python manage.py createsuperuser`

---

## 🚀 DEPLOY RÁPIDO

```bash
# 1. Actualizar .env.production con tus credenciales reales

# 2. Desplegar
cd /workspace
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml build --no-cache
docker-compose -f docker-compose.production.yml up -d

# 3. Ejecutar migraciones
docker-compose -f docker-compose.production.yml exec backend python manage.py migrate

# 4. Crear superusuario
docker-compose -f docker-compose.production.yml exec backend python manage.py createsuperuser

# 5. Verificar
docker-compose -f docker-compose.production.yml ps
docker-compose -f docker-compose.production.yml logs -f backend
```

---

**✨ ¡Listo para producción con Chat AI integrado!**
