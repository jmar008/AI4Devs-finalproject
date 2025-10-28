╔══════════════════════════════════════════════════════════════════════════════╗
║ GUÍA DE INICIO RÁPIDO - DESARROLLO ║
║ MVP DealaAI - 26 de Octubre 2025 ║
╚══════════════════════════════════════════════════════════════════════════════╝

🚀 INICIANDO EL PROYECTO (DEVCONTAINER)
════════════════════════════════════════════════════════════════════════════════

PASO 1: Verificar Docker Compose
─────────────────────────────────

```bash
# Ir al directorio raíz
cd /workspace

# Ver estado de contenedores
docker-compose ps

# Debería mostrar:
# CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS
# backend        ...       running
# frontend       ...       running
# db             ...       running
# redis          ...       running
# nginx          ...       running
```

PASO 2: Crear Base de Datos y Ejecutar Migraciones
────────────────────────────────────────────────────

```bash
# Crear superusuario (ya lo hiciste)
# docker-compose exec backend python manage.py createsuperuser

# Ejecutar migraciones (ya las ejecutaste)
docker-compose exec backend python manage.py migrate

# Verificar que el stock está en la BD
docker-compose exec db psql -U postgres -d dealaai_dev -c "SELECT COUNT(*) FROM stock;"
```

PASO 3: Verificar que Todo Funciona
────────────────────────────────────

```bash
# Ejecutar script de validación
bash /workspace/test_mvp.sh

# Debería mostrar: ✓ TODAS LAS PRUEBAS PASARON
```

📱 ACCEDER A LA APLICACIÓN
════════════════════════════════════════════════════════════════════════════════

FRONTEND (http://localhost:3000)
────────────────────────────────

1. Abre: http://localhost:3000
2. Verás página de inicio
3. Click en "Login" o accede directamente: http://localhost:3000/login
4. Ingresa:
   Usuario: admin
   Contraseña: admin123
5. ✅ Serás redirigido a /dashboard

PANEL DE CONTROL
────────────────

Una vez logueado, verás:

📊 Dashboard (/dashboard)
• Estadísticas de stock
• Actividad reciente
• Acciones rápidas
• Tips del día

🚗 Stock (/dashboard/stock)
• Tabla de 1000+ vehículos
• Búsqueda en tiempo real
• Filtros por marca, combustible, transmisión
• Paginación (10 items/página)
• Detalle por click

📋 Detalle de Vehículo (/dashboard/stock/{bastidor})
• Todos los 140+ campos del vehículo
• Imagen (placeholder)
• Especificaciones técnicas
• Opciones: contactar, email, descargar, compartir

API (http://localhost:8000/api)
──────────────────────────────────

Swagger (documentación interactiva):
→ http://localhost:8000/api/docs/

ReDoc (documentación alternativa):
→ http://localhost:8000/api/redoc/

Endpoints principales:
• POST /api/auth/login/ → Iniciar sesión
• GET /api/stock/ → Listar vehículos
• GET /api/stock/{bastidor}/ → Detalle vehículo
• GET /api/stock/stats/ → Estadísticas
• POST /api/stock/search/ → Búsqueda avanzada

🔧 DESARROLLO
════════════════════════════════════════════════════════════════════════════════

MODIFICAR BACKEND
─────────────────

1. Editar archivos en /workspace/backend/apps/stock/
   • views.py - Lógica de endpoints
   • serializers.py - Formato de respuestas
   • models.py - Modelos de datos

2. Crear migraciones:
   docker-compose exec backend python manage.py makemigrations

3. Aplicar migraciones:
   docker-compose exec backend python manage.py migrate

4. Ver cambios en:
   http://localhost:8000/api/docs/

MODIFICAR FRONTEND
──────────────────

1. Editar archivos en /workspace/frontend/

2. Los cambios se aplican automáticamente (hot reload)

3. Ver en: http://localhost:3000

4. Si hay errores, revisar console del navegador (F12)

EDITAR COMPONENTES
───────────────────

Componentes reutilizables en /workspace/frontend/components/

Ejemplo: Botón
Ubicación: /workspace/frontend/components/ui/button.tsx
Uso:
import { Button } from '@/components/ui/button';
<Button className="bg-indigo-600">Click me</Button>

CREAR NUEVAS PÁGINAS
─────────────────────

Estructura Next.js:
/workspace/frontend/app/
├── page.tsx → /
├── login/
│ └── page.tsx → /login
├── dashboard/
│ ├── page.tsx → /dashboard
│ ├── layout.tsx → Layout protegido
│ ├── stock/
│ │ ├── page.tsx → /dashboard/stock
│ │ └── [id]/
│ │ └── page.tsx → /dashboard/stock/{id}

Para crear una nueva página:

1. Crear carpeta: /workspace/frontend/app/nueva-ruta/
2. Crear archivo: page.tsx
3. Exportar componente default
4. Acceder en: http://localhost:3000/nueva-ruta

📊 GESTIONAR DATOS
════════════════════════════════════════════════════════════════════════════════

ADMIN PANEL
────────────

Acceder a: http://localhost:8000/admin/
Usa credenciales: admin / admin123

Aquí puedes:
• Ver/editar vehículos en stock
• Ver histórico de stock
• Gestionar usuarios
• Crear provincias/concesionarios

BASE DE DATOS
───────────────

Conectar directamente a PostgreSQL:

```bash
docker-compose exec db psql -U postgres -d dealaai_dev
```

Comandos útiles:

```sql
-- Ver tabla de stock
SELECT COUNT(*) FROM stock;

-- Ver primeros 5 vehículos
SELECT bastidor, marca, modelo, precio_venta FROM stock LIMIT 5;

-- Ver histórico
SELECT COUNT(*) FROM stock_historico;

-- Ver usuarios
SELECT username, email FROM auth_user;

-- Buscar por marca
SELECT * FROM stock WHERE marca = 'BMW' LIMIT 5;

-- Salir
\q
```

SCRAPER MANUAL
───────────────

Ejecutar scraper manualmente (en cualquier momento):

```bash
docker-compose exec backend python manage.py migrate_stock_and_scrape \
  --paginas 10 \
  --cantidad 1000 \
  --debug
```

Parámetros:
--paginas N → Número de páginas a descargar (defecto: 10)
--cantidad N → Cantidad de vehículos a generar (defecto: 1000)
--debug → Modo debug (muestra más detalles)

El scraper se ejecuta automáticamente a las 01:00 AM.

🧪 TESTING
════════════════════════════════════════════════════════════════════════════════

PROBAR API MANUAL
──────────────────

Con curl:

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.token')

echo "Token: $TOKEN"

# 2. Listar stock
curl -X GET http://localhost:8000/api/stock/ \
  -H "Authorization: Bearer $TOKEN"

# 3. Ver estadísticas
curl -X GET http://localhost:8000/api/stock/stats/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Buscar
curl -X POST http://localhost:8000/api/stock/search/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query":"BMW 2020","min_price":20000,"max_price":50000}'
```

CON POSTMAN
────────────

1. Descargar Postman: https://www.postman.com/downloads/
2. Importar colección desde: /workspace/backend/api.postman_collection.json
3. Reemplazar {{token}} en requests
4. Usar {{api_url}} = http://localhost:8000/api

TESTS AUTOMÁTICOS (PRÓXIMAMENTE)
─────────────────────────────────

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
cd /workspace/frontend && npm test

# E2E tests
cd /workspace/frontend && npm run test:e2e
```

📝 LOGS Y DEBUGGING
════════════════════════════════════════════════════════════════════════════════

VER LOGS EN TIEMPO REAL
────────────────────────

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend

# Solo database
docker-compose logs -f db

# Filtrar por palabra clave
docker-compose logs -f | grep ERROR

# Últimas 100 líneas
docker-compose logs --tail=100
```

DEBUGGING CON BREAKPOINTS
──────────────────────────

Backend (Django):

1. Añadir import pdb: import pdb
2. Agregar breakpoint: pdb.set_trace()
3. Acceder a la funcionalidad en el navegador
4. En terminal verás el prompt (Pdb)
5. Comandos: n (next), s (step), c (continue), l (list)

Frontend (React):

1. Abrir DevTools: F12
2. Ir a Sources
3. Buscar archivo
4. Hacer click en número de línea para agregar breakpoint
5. Reproducir acción

VERIFICAR ERRORES
──────────────────

Backend:
• Logs: docker-compose logs -f backend
• Admin: http://localhost:8000/admin/ (buscar errores en Events)
• Shell: docker-compose exec backend python manage.py shell

Frontend:
• Console: F12 → Console tab
• Network: F12 → Network tab (para ver requests)
• Local Storage: F12 → Application → Local Storage (ver token)

🔑 VARIABLES DE ENTORNO
════════════════════════════════════════════════════════════════════════════════

ARCHIVO: /workspace/backend/.env (crear si no existe)

```
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=dealaai.settings.development
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/dealaai_dev

# Redis
REDIS_URL=redis://redis:6379/0

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

ARCHIVO: /workspace/frontend/.env.local

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NODE_ENV=development
```

🛠️ COMANDOS ÚTILES
════════════════════════════════════════════════════════════════════════════════

Backend
───────

docker-compose exec backend python manage.py shell
→ Acceder al shell interactivo de Django

docker-compose exec backend python manage.py createsuperuser
→ Crear nuevo superusuario

docker-compose exec backend python manage.py makemigrations
→ Crear migraciones nuevas

docker-compose exec backend python manage.py migrate
→ Aplicar migraciones

docker-compose exec backend python manage.py runserver 0.0.0.0:8000
→ Ejecutar servidor (dentro del contenedor)

Frontend
────────

cd /workspace/frontend && npm run dev
→ Iniciar servidor de desarrollo

cd /workspace/frontend && npm run build
→ Compilar para producción

cd /workspace/frontend && npm run lint
→ Verificar errores de código

Docker
──────

docker-compose ps
→ Ver estado de contenedores

docker-compose logs -f
→ Ver logs en tiempo real

docker-compose restart
→ Reiniciar todos los servicios

docker-compose down
→ Detener y remover contenedores

docker-compose up -d
→ Levantar todos los servicios en background

docker-compose exec <servicio> <comando>
→ Ejecutar comando en un servicio

📊 ESTRUCTURA DE CARPETAS
════════════════════════════════════════════════════════════════════════════════

/workspace/
├── backend/
│ ├── apps/
│ │ ├── authentication/ → Autenticación (completado)
│ │ └── stock/ → Stock (✅ COMPLETADO HOY)
│ ├── dealaai/
│ │ ├── settings/
│ │ │ ├── base.py → Configuración común
│ │ │ ├── development.py → Desarrollo
│ │ │ ├── production.py → Producción
│ │ │ └── staging.py → Staging
│ │ └── urls.py → URLs (✅ ACTUALIZADO)
│ ├── manage.py
│ └── requirements/
│ ├── base.txt
│ ├── development.txt
│ └── production.txt
│
├── frontend/
│ ├── app/
│ │ ├── page.tsx → Inicio (/)
│ │ ├── login/ → Login (/login) ✅ NUEVO
│ │ ├── dashboard/ → Dashboard protegido ✅ NUEVO
│ │ └── health/ → Health check
│ ├── components/
│ │ ├── Sidebar.tsx → Navegación ✅ NUEVO
│ │ ├── Topbar.tsx → Barra superior ✅ NUEVO
│ │ └── ui/ → Componentes reutilizables
│ ├── lib/
│ │ ├── api.ts → Cliente API ✅ NUEVO
│ │ └── utils.ts
│ ├── store/
│ │ └── authStore.ts → Estado Zustand ✅ NUEVO
│ ├── middleware.ts → Protección de rutas ✅ NUEVO
│ └── .env.local → Variables entorno
│
├── docker/
│ ├── backend/
│ │ ├── Dockerfile
│ │ └── Dockerfile.prod
│ ├── frontend/
│ │ ├── Dockerfile
│ │ └── Dockerfile.prod
│ ├── nginx/
│ │ ├── nginx.conf
│ │ └── nginx.dev.conf
│ └── database/
│ └── Dockerfile
│
├── database/
│ ├── backups/
│ ├── fixtures/
│ ├── init/
│ │ └── 01-init.sql
│ └── migrations/
│ └── stock_queries.sql
│
├── docker-compose.yml → Desarrollo (devcontainer)
├── docker-compose.production.yml → Producción
│
└── DOCUMENTACIÓN/
├── FRONTEND_MVP_COMPLETED.md ← Lee esto
├── MVP_FINAL_SUMMARY.md ← Lee esto
├── PRODUCTION_DEPLOYMENT.md ← Para producción
└── test_mvp.sh ← Script de pruebas

🎯 PRÓXIMOS PASOS
════════════════════════════════════════════════════════════════════════════════

1. TESTING
   • Probar login/logout
   • Verificar paginación en stock
   • Clickear en vehículos para ver detalles
   • Probar búsqueda y filtros

2. OPTIMIZACIONES
   • Agregar infinite scroll (opcional)
   • Caché de datos con React Query
   • Compresión de imágenes
   • Tests unitarios

3. FEATURES ADICIONALES (Fase 2)
   • Leads CRM Module
   • Chat con IA
   • Reportes avanzados
   • Notificaciones

4. PRODUCCIÓN
   • Revisar /workspace/PRODUCTION_DEPLOYMENT.md
   • Configurar EasyPanel
   • Deployar en servidor

🆘 TROUBLESHOOTING COMÚN
════════════════════════════════════════════════════════════════════════════════

❌ "Cannot connect to Docker daemon"
✅ Solución: Reiniciar Docker
sudo systemctl restart docker

❌ "Port 8000 already in use"
✅ Solución: Liberar puerto
docker-compose down
netstat -tlnp | grep 8000
kill -9 <PID>

❌ "Database connection refused"
✅ Solución: Reiniciar base de datos
docker-compose restart db
docker-compose exec backend python manage.py migrate

❌ "Frontend no actualiza cambios"
✅ Solución:
cd /workspace/frontend
npm run dev
Abrir http://localhost:3000

❌ "Token inválido en API"
✅ Solución:
• Limpiar localStorage: F12 → Application → Local Storage → Clear
• Hacer login nuevamente
• Verificar que token se guarda

❌ "Static files not loading"
✅ Solución:
docker-compose exec backend python manage.py collectstatic
docker-compose restart nginx

════════════════════════════════════════════════════════════════════════════════
¡LISTO PARA COMENZAR! 🚀
════════════════════════════════════════════════════════════════════════════════

Próximo paso: Abre http://localhost:3000/login

Username: admin
Password: admin123

¡Bienvenido al MVP de DealaAI!

════════════════════════════════════════════════════════════════════════════════
