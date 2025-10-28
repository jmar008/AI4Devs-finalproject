# 🆘 Solución: Service is not reachable en EasyPanel

## ¿Por qué ocurre este error?

El error "Service is not reachable" significa que EasyPanel no puede determinar si tus servicios están funcionando correctamente. Esto puede ocurrir por varias razones:

1. **Health checks fallando** - Los servicios no están retornando respuestas "healthy"
2. **Servicios no iniciando correctamente** - Errores en migraciones, compilación, etc.
3. **Puertos incorrectos** - Los servicios escuchan en puertos diferentes a los esperados
4. **Volúmenes con permisos insuficientes** - Los contenedores no pueden escribir/leer
5. **Variables de entorno no configuradas** - Faltan datos críticos

---

## 🔧 Pasos Rápidos de Solución

### PASO 1: Verificar Localmente Primero

**Antes de desplegar en EasyPanel, asegúrate que funciona en tu máquina:**

```powershell
# Limpiar todo
docker-compose -f docker-compose.easypanel.yml down -v

# Reconstruir todo
docker-compose -f docker-compose.easypanel.yml build --no-cache

# Iniciar servicios
docker-compose -f docker-compose.easypanel.yml up -d

# Esperar 30 segundos y verificar estado
Start-Sleep -Seconds 30
docker-compose -f docker-compose.easypanel.yml ps

# Ver logs de cualquier error
docker-compose -f docker-compose.easypanel.yml logs
```

**Si ves algo así, está bien:**

```
STATUS
healthy (1)
```

**Si ves esto, hay problema:**

```
STATUS
unhealthy (1)
```

### PASO 2: Revisar Logs Específicos

```powershell
# Backend - Aquí es donde fallan las migraciones
docker-compose -f docker-compose.easypanel.yml logs backend

# Frontend - Aquí falla Next.js si hay problemas de build
docker-compose -f docker-compose.easypanel.yml logs frontend

# Nginx - Aquí falla el reverse proxy
docker-compose -f docker-compose.easypanel.yml logs nginx

# Database - Aquí falla PostgreSQL si hay permisos
docker-compose -f docker-compose.easypanel.yml logs db
```

### PASO 3: Soluciones por Servicio

#### 🗄️ PostgreSQL Falla

```powershell
# Ver logs
docker-compose -f docker-compose.easypanel.yml logs db

# Posibles problemas y soluciones:
# - Permisos: Ejecutar con docker run -u 0 (root)
# - Volumen corrupto: Usar docker volume rm

# Limpiar e intentar de nuevo
docker volume rm dealaai_finalproject_postgres_data 2>$null
docker-compose -f docker-compose.easypanel.yml up -d db
docker-compose -f docker-compose.easypanel.yml logs -f db
```

#### 🐍 Backend (Django) Falla

```powershell
# Ver logs
docker-compose -f docker-compose.easypanel.yml logs backend

# Problemas comunes:
# 1. Migraciones fallando
#    Solución: docker-compose exec backend python manage.py migrate

# 2. SECRET_KEY no configurado
#    Solución: Agregar SECRET_KEY a variables de entorno

# 3. Base de datos no responde
#    Solución: Esperar a que DB se inicie primero

# Reintentar manualmente
docker-compose -f docker-compose.easypanel.yml restart backend
docker-compose -f docker-compose.easypanel.yml logs -f backend

# Esperar a que veas "Starting development server at http://0.0.0.0:8000/"
```

#### ⚛️ Frontend (Next.js) Falla

```powershell
# Ver logs
docker-compose -f docker-compose.easypanel.yml logs frontend

# Problemas comunes:
# 1. Next.js tardando mucho en compilar (10+ minutos es normal)
# 2. Falta de espacio en disco
# 3. Node modules corrupto

# Soluciones:
docker-compose -f docker-compose.easypanel.yml exec frontend npm install
docker-compose -f docker-compose.easypanel.yml restart frontend

# Esperar a que veas "> ready on 0.0.0.0:3000"
```

#### 🌐 Nginx Falla

```powershell
# Ver logs
docker-compose -f docker-compose.easypanel.yml logs nginx

# Verificar configuración
docker-compose -f docker-compose.easypanel.yml exec nginx nginx -t

# Recargar configuración
docker-compose -f docker-compose.easypanel.yml exec nginx nginx -s reload
```

---

## 🚀 Desplegar en EasyPanel (Una Vez Todo Funciona Localmente)

### 1. Preparar Cambios en Git

```powershell
git add docker-compose.easypanel.yml .env.easypanel.example validate-for-easypanel.sh
git commit -m "Preparación para EasyPanel - docker-compose optimizado"
git push origin main
```

### 2. En EasyPanel - Configuración

**Ir a: Dashboard → Proyectos → Crear Nuevo Proyecto**

| Campo                   | Valor                          |
| ----------------------- | ------------------------------ |
| **Nombre**              | `dealaai`                      |
| **Tipo**                | `Docker Compose`               |
| **Repositorio**         | Tu URL de GitHub               |
| **Branch**              | `main`                         |
| **Docker Compose File** | `docker-compose.easypanel.yml` |

### 3. Configurar Variables de Entorno

En EasyPanel, ir a **Variables** y agregar (basado en `.env.easypanel.example`):

```
DB_NAME=dealaai_dev
DB_PASSWORD=TU_CONTRASEÑA_SEGURA
SECRET_KEY=TU_SECRET_KEY_GENERADO
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DEEPSEEK_API_KEY=tu-openrouter-key
NEXT_PUBLIC_API_URL=https://tu-dominio.com
PGADMIN_DEFAULT_EMAIL=admin@tu-dominio.com
PGADMIN_DEFAULT_PASSWORD=TU_CONTRASEÑA_PGADMIN
```

### 4. Configurar Puertos y Dominios

**En EasyPanel:**

| Servicio  | Puerto | Dominio        | Protocolo        |
| --------- | ------ | -------------- | ---------------- |
| **nginx** | 80     | tu-dominio.com | HTTP             |
| **nginx** | 443    | tu-dominio.com | HTTPS (SSL Auto) |

### 5. Desplegar

**Botón: DEPLOY**

**Esperado: 5-15 minutos según tamaño del proyecto**

---

## 📊 Monitorear el Despliegue

### En EasyPanel - Ver Progreso

1. Ve a **Servicios** → ver estado de cada uno
2. Espera a que todos muestren "✓ healthy"
3. Ver logs en cada servicio si algo falla

### Tiempos Esperados

| Servicio     | Tiempo  | Señal de Éxito                    |
| ------------ | ------- | --------------------------------- |
| **db**       | 10-20s  | `pg_isready` returns ok           |
| **redis**    | 5-10s   | `redis-cli ping` returns PONG     |
| **backend**  | 30-60s  | `curl /health/` returns 200       |
| **frontend** | 2-10min | `curl /` returns 200              |
| **nginx**    | 5-10s   | Inicia una vez backend está listo |

### Si Alguno Falla

1. **Revisa logs** en EasyPanel
2. **Copia el error exacto**
3. **Reinicia ese servicio**
4. **Espera 2 minutos**
5. **Verifica nuevamente**

---

## ✅ Verificar Que Funciona en Producción

Una vez que todos los servicios muestren "✓ healthy":

```powershell
# 1. Acceder a la app
curl https://tu-dominio.com

# 2. Acceder al admin
curl https://tu-dominio.com/admin/

# 3. Probar login (desde navegador)
# - Ir a https://tu-dominio.com/login
# - Abrir DevTools (F12)
# - Network tab
# - Intentar login
# - Ver que `/api/auth/users/login/` retorna 200

# 4. Revisar que es HTTPS
# - La barra debería mostrar 🔒
```

---

## 🐛 Errores Específicos y Soluciones

### Error: "Backend unhealthy - curl: (7) Failed to connect"

```
Causa: Backend no está respondiendo en puerto 8000
Solución:
1. Ver logs: docker-compose logs backend
2. Esperar a que inicialice (puede tardar 60s)
3. Si sigue fallando, revisar migraciones:
   docker-compose exec backend python manage.py migrate
```

### Error: "Frontend unhealthy - Connection refused"

```
Causa: Next.js no terminó de compilar
Solución:
1. Ver logs: docker-compose logs frontend
2. Esperar (puede tardar 10+ minutos si es primera ejecución)
3. Si falla, revisar node_modules:
   docker-compose exec frontend npm install
```

### Error: "Nginx unhealthy"

```
Causa: No puede conectar a backend/frontend
Solución:
1. Ver logs: docker-compose logs nginx
2. Verifica que backend y frontend estén healthy primero
3. Reinicia nginx: docker-compose restart nginx
```

### Error: "Database connection refused"

```
Causa: PostgreSQL no está listo
Solución:
1. Esperar (PostgreSQL tarda 20-30s en iniciar)
2. Ver logs: docker-compose logs db
3. Si está corrompido:
   docker volume rm dealaai_*_postgres_data
   docker-compose up -d db
```

---

## 📝 Checklist de Troubleshooting

### Antes de Desplegar

- [ ] Funciona localmente con `docker-compose.easypanel.yml`
- [ ] Todos los servicios muestran "healthy" localmente
- [ ] Variables de entorno configuradas localmente
- [ ] Git repo actualizado y limpio

### Después de Desplegar en EasyPanel

- [ ] Todos los servicios muestran "✓ healthy"
- [ ] Logs no muestran errores críticos
- [ ] Puedes acceder a https://tu-dominio.com
- [ ] Admin carga en https://tu-dominio.com/admin/
- [ ] Login funciona desde frontend
- [ ] Certificado SSL válido (🔒 aparece)

### Si Sigue Fallando

- [ ] Revisa la documentación de EasyPanel
- [ ] Prueba localmente primero
- [ ] Verifica todas las variables de entorno
- [ ] Asegúrate que los Dockerfiles son compatibles
- [ ] Verifica permisos de volúmenes
- [ ] Intenta reconstruir sin cache

---

## 💡 Consejos Útiles

1. **Comienza simple** - Desactiva PgAdmin si no lo necesitas
2. **Usa named volumes** - Evita problemas de permisos
3. **Health checks** - Son críticos, no los remuevas
4. **Logs** - La mejor herramienta de debugging
5. **Reinicia servicios** - A veces es lo más simple que funciona
6. **Espera pacientemente** - Primera ejecución puede tardar 15+ minutos

---

## 🎯 Próximo Paso

Si todo funciona localmente pero falla en EasyPanel:

1. Revisa exactamente qué error ves en logs
2. Busca ese error en este documento
3. Si no está, toma nota y contacta soporte

**¡La mayoría de problemas se resuelven revisando logs! 🔍**
