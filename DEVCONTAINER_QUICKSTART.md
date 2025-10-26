# 🐳 DevContainer - Guía de Inicio Rápido

## 🚀 Inicio Rápido

### 1. Abrir en DevContainer

1. Abre VS Code
2. Instala la extensión "Dev Containers" si no la tienes
3. Abre este proyecto en VS Code
4. VS Code debería detectar el `.devcontainer` y preguntarte si quieres abrir en container
5. Si no aparece, usa `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"

### 2. Configuración Automática

Una vez en el DevContainer, ejecuta:

```bash
./scripts/devcontainer-setup.sh
```

Este script:

- ✅ Instala dependencias del backend (Python/Django)
- ✅ Instala dependencias del frontend (Node.js/Next.js)
- ✅ Inicia servicios de base de datos (PostgreSQL + Redis)
- ✅ Ejecuta migraciones de Django
- ✅ Verifica configuración

### 3. Iniciar Desarrollo

**Opción A: Usar tareas de VS Code**

- `Ctrl+Shift+P` → "Tasks: Run Task"
- Selecciona: "🚀 Iniciar Frontend (Next.js)" o "🐍 Iniciar Backend (Django)"

**Opción B: Terminal manual**

```bash
# Terminal 1 - Backend
cd backend
python manage.py runserver 0.0.0.0:8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## 🌐 URLs de Desarrollo

| Servicio     | URL                         | Descripción              |
| ------------ | --------------------------- | ------------------------ |
| Frontend     | http://localhost:3000       | Aplicación Next.js       |
| Backend API  | http://localhost:8000       | API Django REST          |
| Admin Django | http://localhost:8000/admin | Panel administrativo     |
| PgAdmin      | http://localhost:5050       | Administrador PostgreSQL |

## 🛠️ Herramientas Disponibles

### Backend (Python/Django)

```bash
# Migraciones
python manage.py makemigrations
python manage.py migrate

# Tests
pytest

# Shell interactivo
python manage.py shell

# Crear superusuario
python manage.py createsuperuser

# Formatear código
black .
isort .
```

### Frontend (Node.js/Next.js)

```bash
# Desarrollo
npm run dev

# Tests
npm test

# Formatear código
npm run format

# Build de producción
npm run build
```

### Docker Services

```bash
# Ver servicios corriendo
docker-compose ps

# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Parar servicios
docker-compose down
```

## 🐛 Debug

### Debug con VS Code

1. Ve a la pestaña "Run and Debug" (`Ctrl+Shift+D`)
2. Selecciona una configuración:
   - "🐍 Debug Django Backend"
   - "⚛️ Debug Next.js Frontend"
   - "🚀 Full Stack Debug" (ambos)

### Logs y Troubleshooting

```bash
# Ver logs de servicios
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Conectar a base de datos
psql -h localhost -U postgres -d dealaai_dev

# Verificar estado de servicios
docker-compose ps
```

## 📦 Estructura del Proyecto

```
.devcontainer/          # Configuración DevContainer
├── devcontainer.json   # Configuración principal
└── docker-compose.yml  # Servicios para desarrollo

backend/               # API Django
├── apps/             # Aplicaciones Django
├── core/             # Lógica de negocio
├── dealaai/          # Configuración proyecto
└── requirements/     # Dependencias Python

frontend/             # Aplicación Next.js
├── app/             # App Router (Next.js 14)
├── components/      # Componentes React
├── lib/            # Utilidades
└── types/          # Definiciones TypeScript

docker/              # Configuraciones Docker
└── nginx/           # Configuración Nginx (producción)
```

## ⚡ Comandos Frecuentes

```bash
# Reinicio completo del entorno
docker-compose down -v
docker-compose up -d
./scripts/devcontainer-setup.sh

# Instalar nueva dependencia Python
cd backend
pip install nueva-dependencia
pip freeze > requirements/development.txt

# Instalar nueva dependencia Node.js
cd frontend
npm install nueva-dependencia

# Crear nueva app Django
cd backend
python manage.py startapp nueva_app

# Generar componente Next.js (manual)
cd frontend/components
mkdir nuevo-componente
```

## 🔧 Configuración Avanzada

### Variables de Entorno

- Las variables están configuradas en `.devcontainer/devcontainer.json`
- Para producción, ver `docker-compose.production.yml`

### Extensiones VS Code

El DevContainer incluye automáticamente:

- Python
- JavaScript/TypeScript
- Docker
- PostgreSQL
- Git
- Thunder Client (testing API)

### Personalizar DevContainer

Edita `.devcontainer/devcontainer.json` para:

- Agregar más extensiones
- Cambiar configuración de VS Code
- Agregar más herramientas

## 🆘 Solución de Problemas

### Error: Puerto ya en uso

```bash
# Ver qué proceso usa el puerto
lsof -i :3000  # o :8000
# Parar servicios Docker
docker-compose down
```

### Error: Base de datos no conecta

```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps db
# Reiniciar servicio
docker-compose restart db
```

### Error: Dependencias no instaladas

```bash
# Reinstalar dependencias
cd backend && pip install -r requirements/development.txt
cd frontend && npm install
```

### DevContainer no inicia

1. Verifica que Docker Desktop esté corriendo
2. Actualiza la extensión "Dev Containers"
3. Intenta: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"

## 📚 Recursos Útiles

- [Documentación DevContainers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Django Documentation](https://docs.djangoproject.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Docker Compose Reference](https://docs.docker.com/compose/)

---

¡Listo para desarrollar! 🎉 Si tienes problemas, revisa los logs o consulta la documentación específica de cada herramienta.
