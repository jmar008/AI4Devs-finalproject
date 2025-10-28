# 🚀 Quick Start - DealaAI

## Opción 1: DevContainer (Recomendado - Más Fácil)

### Prerequisitos

- ✅ VS Code instalado
- ✅ Docker Desktop instalado y corriendo
- ✅ Extensión "Dev Containers" instalada en VS Code

### Pasos

1. **Abrir el proyecto en VS Code**

   ```bash
   cd AI4Devs-finalproject
   code .
   ```

2. **Reabrir en Container**

   - VS Code mostrará una notificación: "Reopen in Container"
   - O presiona `F1` y selecciona: `Dev Containers: Reopen in Container`

3. **Esperar** (primera vez ~5-10 minutos)

   - Se construye la imagen del container
   - Se instalan todas las dependencias automáticamente
   - Se ejecuta el script de setup

4. **¡Listo!** 🎉

   - Todas las herramientas instaladas
   - Todas las extensiones configuradas
   - Base de datos inicializada
   - Redis funcionando

5. **Verificar servicios**

   ```bash
   # Dentro del devcontainer (terminal integrada)
   docker-compose ps
   ```

6. **Iniciar desarrollo**

   ```bash
   # Backend
   cd backend && source venv/bin/activate
   python manage.py runserver 0.0.0.0:8000

   # Frontend (nueva terminal)
   cd frontend
   npm run dev
   ```

7. **Acceder a la aplicación**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Admin: http://localhost:8000/admin

---

## Opción 2: Docker Compose (Sin DevContainer)

### Prerequisitos

- ✅ Docker Desktop instalado
- ✅ Git instalado

### Pasos

1. **Clonar el repositorio**

   ```bash
   git clone <repository-url>
   cd AI4Devs-finalproject
   ```

2. **Dar permisos a scripts** (Linux/Mac)

   ```bash
   chmod +x scripts/*.sh
   ```

3. **Ejecutar setup**

   ```bash
   # Linux/Mac
   ./scripts/setup.sh

   # Windows (PowerShell)
   .\scripts\setup.sh
   ```

4. **Configurar variables de entorno**

   Edita `backend/.env`:

   ```env
   OPENAI_API_KEY=sk-tu-api-key-aqui
   ```

5. **Iniciar servicios**

   ```bash
   docker-compose up -d
   ```

6. **Ver logs**

   ```bash
   docker-compose logs -f
   ```

7. **Acceder a la aplicación**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin

---

## Opción 3: Desarrollo Local (Sin Docker)

### Prerequisitos

- ✅ Python 3.11+ instalado
- ✅ Node.js 18+ instalado
- ✅ PostgreSQL 15+ instalado
- ✅ Redis instalado

### Backend Setup

1. **Crear entorno virtual**

   ```bash
   cd backend
   python -m venv venv

   # Activar
   # Linux/Mac:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   ```

2. **Instalar dependencias**

   ```bash
   pip install -r requirements/development.txt
   ```

3. **Configurar PostgreSQL**

   ```sql
   CREATE DATABASE dealaai_dev;
   CREATE USER postgres WITH PASSWORD 'postgres';
   GRANT ALL PRIVILEGES ON DATABASE dealaai_dev TO postgres;
   ```

4. **Habilitar extensión pgvector**

   ```sql
   \c dealaai_dev
   CREATE EXTENSION vector;
   ```

5. **Configurar .env**

   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dealaai_dev
   REDIS_URL=redis://localhost:6379/0
   OPENAI_API_KEY=sk-tu-api-key
   ```

6. **Ejecutar migraciones**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. **Iniciar servidor**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Instalar dependencias**

   ```bash
   cd frontend
   npm install
   ```

2. **Configurar .env.local**

   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Iniciar desarrollo**
   ```bash
   npm run dev
   ```

---

## 🎯 Verificación Rápida

### ¿Todo funciona?

1. **Backend Health Check**

   ```bash
   curl http://localhost:8000/api/health/
   # Debería devolver: {"status": "ok"}
   ```

2. **Frontend Loading**

   ```bash
   curl http://localhost:3000
   # Debería devolver HTML
   ```

3. **PostgreSQL**

   ```bash
   docker-compose exec db psql -U postgres -d dealaai_dev -c "SELECT version();"
   # Debería mostrar versión de PostgreSQL
   ```

4. **Redis**
   ```bash
   docker-compose exec redis redis-cli ping
   # Debería devolver: PONG
   ```

---

## 📝 Siguientes Pasos

1. **Crear superusuario**

   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

2. **Acceder al admin**
   http://localhost:8000/admin

3. **Explorar la API**
   http://localhost:8000/api/docs/

4. **Ver documentación**
   - [DEVELOPMENT.md](DEVELOPMENT.md) - Guía completa
   - [COMMANDS.md](COMMANDS.md) - Comandos útiles
   - [STRUCTURE.md](STRUCTURE.md) - Estructura del proyecto

---

## 🆘 Problemas Comunes

### Puerto 3000 ocupado

```bash
# Ver qué proceso lo usa
# Windows
netstat -ano | findstr :3000

# Linux/Mac
lsof -i :3000

# Matar el proceso
# Windows
taskkill /PID <PID> /F

# Linux/Mac
kill -9 <PID>
```

### Docker no inicia

```bash
# Verificar Docker
docker --version
docker ps

# Reiniciar Docker Desktop
# Windows: Reiniciar desde la bandeja del sistema
# Linux: sudo systemctl restart docker
```

### Base de datos no conecta

```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Reiniciar
docker-compose restart db

# Ver logs
docker-compose logs db
```

### Dependencias no se instalan

```bash
# Backend
docker-compose exec backend pip install --upgrade pip
docker-compose exec backend pip install -r requirements/development.txt

# Frontend
docker-compose exec frontend npm install
```

---

## 💡 Comandos Útiles

### Con Make (recomendado)

```bash
make help           # Ver todos los comandos
make start          # Iniciar servicios
make stop           # Detener servicios
make logs           # Ver logs
make migrate        # Ejecutar migraciones
make test           # Ejecutar tests
make shell-backend  # Django shell
make shell-db       # PostgreSQL shell
```

### Con Scripts

```bash
./scripts/dev.sh start
./scripts/dev.sh stop
./scripts/dev.sh logs
./scripts/dev.sh migrate
./scripts/dev.sh shell
```

### Con Docker Compose

```bash
docker-compose up -d
docker-compose down
docker-compose logs -f
docker-compose ps
docker-compose exec backend python manage.py shell
```

---

## 🎓 Recursos de Aprendizaje

- **Django**: https://docs.djangoproject.com/
- **Next.js**: https://nextjs.org/docs
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Docker**: https://docs.docker.com/
- **pgvector**: https://github.com/pgvector/pgvector

---

## ✅ Checklist Inicial

- [ ] Docker Desktop instalado y corriendo
- [ ] VS Code instalado
- [ ] Extensión "Dev Containers" instalada
- [ ] Proyecto clonado
- [ ] Abierto en DevContainer (o servicios iniciados con Docker Compose)
- [ ] Variables de entorno configuradas
- [ ] Servicios corriendo (backend, frontend, db, redis)
- [ ] Superusuario creado
- [ ] Acceso al admin verificado

---

**¿Todo listo? ¡Comienza a desarrollar! 🚀**

Si tienes problemas, consulta:

- [DEVELOPMENT.md](DEVELOPMENT.md) para más detalles
- [COMMANDS.md](COMMANDS.md) para referencia de comandos
- GitHub Issues para reportar problemas
