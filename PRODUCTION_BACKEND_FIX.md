# 🚨 FIX: Backend SECRET_KEY Error en Producción

## Problema

El backend en producción está fallando con el error:

```
decouple.UndefinedValueError: SECRET_KEY not found. Declare it as envvar or define a default value.
```

## Causa

El contenedor de backend no tiene acceso al archivo `.env` con las variables de entorno necesarias porque:

1. El `.dockerignore` excluye los archivos `.env`
2. Las variables no se están pasando correctamente desde docker-compose

## Solución

### Paso 1: Actualizar archivos en el VPS

Los siguientes archivos ya han sido corregidos en el repositorio:

1. **`docker/backend/Dockerfile.prod`** - Ahora copia `.env.production` como `.env`
2. **`backend/.env.production`** - Variables de producción actualizadas
3. **`docker-compose.production.yml`** - Corregido y simplificado
4. **`setup-production.sh`** - Script para configurar variables

### Paso 2: Ejecutar en el VPS

```bash
# 1. Ir al directorio del proyecto
cd ~/AI4Devs-finalproject

# 2. Hacer ejecutable el script de configuración
chmod +x setup-production.sh

# 3. Ejecutar el script de configuración (generará SECRET_KEY y configurará variables)
./setup-production.sh

# 4. Reconstruir y reiniciar los contenedores
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml build --no-cache
docker-compose -f docker-compose.production.yml up -d

# 5. Verificar el estado
docker-compose -f docker-compose.production.yml ps
docker logs dealaai_backend_prod --tail 50
```

### Paso 3: Verificar funcionamiento

```bash
# Verificar health check
curl -f http://localhost:8000/health/

# Verificar logs del backend
docker logs dealaai_backend_prod

# Verificar todos los servicios
docker-compose -f docker-compose.production.yml ps
```

## Variables configuradas por el script

El script `setup-production.sh` configura automáticamente:

- `SECRET_KEY`: Generada automáticamente (50 caracteres seguros)
- `DB_PASSWORD`: Contraseña para PostgreSQL
- `DEEPSEEK_API_KEY`: API key para OpenRouter
- `PGADMIN_PASSWORD`: Contraseña para pgAdmin

## Archivos modificados

1. **`.env.production`** - Variables globales de producción
2. **`backend/.env.production`** - Variables específicas del backend
3. **`docker-compose.production.yml`** - Configuración limpia y funcional
4. **`docker/backend/Dockerfile.prod`** - Copia `.env.production` al contenedor

## Comandos de verificación

```bash
# Estado de contenedores
docker-compose -f docker-compose.production.yml ps

# Logs del backend
docker logs dealaai_backend_prod --tail 50

# Health check manual
curl http://localhost:8000/health/

# Verificar variables en el contenedor
docker exec dealaai_backend_prod env | grep SECRET_KEY
```

## Próximos pasos

Una vez que el backend esté healthy:

1. Verificar que Nginx esté sirviendo correctamente
2. Probar el frontend
3. Verificar la conectividad con la base de datos
4. Probar las funcionalidades de la aplicación
