# 🛠️ Funcionalidades y Comandos - DealaAI

Este documento recopila todos los comandos disponibles en el proyecto DealaAI, organizados por categorías y con explicaciones detalladas.

---

## 📋 Tabla de Contenidos

1. [Inicialización del Proyecto](#inicialización-del-proyecto)
2. [Gestión de Contenedores Docker](#gestión-de-contenedores-docker)
3. [Migraciones de Base de Datos](#migraciones-de-base-de-datos)
4. [Generación de Datos](#generación-de-datos)
5. [Gestión de Usuarios](#gestión-de-usuarios)
6. [Gestión de Stock/Inventario](#gestión-de-stockinventario)
7. [Testing y Verificación](#testing-y-verificación)
8. [Administración del Sistema](#administración-del-sistema)
9. [Comandos de Desarrollo](#comandos-de-desarrollo)

---

## 🚀 Inicialización del Proyecto

### Levantar el proyecto completo

```bash
docker-compose up -d
```

**Qué hace:**
- Inicia todos los servicios (backend, frontend, base de datos, Redis, Nginx, pgAdmin)
- Modo detached (-d) para ejecutar en segundo plano

### Detener el proyecto

```bash
docker-compose down
```

**Qué hace:**
- Detiene y elimina todos los contenedores
- Preserva los volúmenes de datos

### Detener y limpiar todo

```bash
docker-compose down -v
```

**Qué hace:**
- Detiene contenedores
- Elimina volúmenes (⚠️ BORRA TODOS LOS DATOS)

---

## 🐳 Gestión de Contenedores Docker

### Ver estado de contenedores

```bash
docker-compose ps
```

**Qué hace:**
- Muestra el estado de todos los servicios
- Indica si están corriendo o detenidos

### Ver logs de un servicio específico

```bash
# Backend
docker-compose logs backend

# Frontend
docker-compose logs frontend

# Base de datos
docker-compose logs db

# Todos los servicios
docker-compose logs
```

**Qué hace:**
- Muestra los logs del servicio especificado
- Útil para debugging

### Reiniciar un servicio

```bash
# Reiniciar backend
docker-compose restart backend

# Reiniciar frontend
docker-compose restart frontend

# Reiniciar todos
docker-compose restart
```

**Qué hace:**
- Reinicia el servicio sin reconstruir la imagen
- Útil después de cambios en variables de entorno

### Reconstruir y reiniciar

```bash
# Reconstruir backend
docker-compose up -d --build backend

# Reconstruir todo
docker-compose up -d --build
```

**Qué hace:**
- Reconstruye la imagen Docker desde el Dockerfile
- Útil después de cambios en dependencias

---

## 🗄️ Migraciones de Base de Datos

### Crear migraciones

```bash
docker-compose exec backend python manage.py makemigrations
```

**Qué hace:**
- Detecta cambios en los modelos de Django
- Crea archivos de migración en `apps/*/migrations/`

### Aplicar migraciones

```bash
docker-compose exec backend python manage.py migrate
```

**Qué hace:**
- Aplica todas las migraciones pendientes a la base de datos
- Crea/modifica tablas según los modelos

### Ver estado de migraciones

```bash
docker-compose exec backend python manage.py showmigrations
```

**Qué hace:**
- Muestra qué migraciones están aplicadas (✅) y cuáles no (❌)

### Migración específica de una app

```bash
docker-compose exec backend python manage.py migrate authentication
docker-compose exec backend python manage.py migrate stock
```

**Qué hace:**
- Aplica migraciones solo de la app especificada

---

## 📊 Generación de Datos

### Script Maestro - Generar TODOS los datos

```bash
docker-compose exec backend python generar_datos_completos.py
```

**Qué hace:**
- ✅ Genera 49 provincias de España
- ✅ Genera concesionarios (1-3 por provincia)
- ✅ Genera 46 usuarios con jerarquía organizacional
- ✅ Genera perfiles de usuario
- ✅ Genera 100 vehículos con IA
- ⏱️ Duración: ~10-15 minutos

### Generar solo Provincias

```bash
docker-compose exec backend python manage.py generar_provincias_solo
```

**Qué hace:**
- Genera las 49 provincias de España
- Con códigos oficiales (01-50)
- ⏱️ Duración: ~5 segundos

### Generar solo Concesionarios

```bash
docker-compose exec backend python manage.py generar_concesionarios
```

**Qué hace:**
- Genera 1-3 concesionarios por provincia
- Con nombres, direcciones, teléfonos y emails
- ⏱️ Duración: ~10 segundos

### Generar solo Usuarios

```bash
docker-compose exec backend python manage.py generar_usuarios_completos --no-borrar-admin
```

**Qué hace:**
- Genera 46 usuarios con jerarquía organizacional
- 5 ejecutivos predefinidos (CEO, COO, CFO, CTO, CMO)
- 41 empleados en diferentes niveles
- Preserva el usuario admin
- ⏱️ Duración: ~20 segundos

---

## 🚗 Gestión de Stock/Inventario

### Generar vehículos con IA (recomendado)

```bash
# 100 vehículos
docker-compose exec backend python manage.py migrate_stock_and_scrape --usar-ia --cantidad 100

# 1000 vehículos
docker-compose exec backend python manage.py migrate_stock_and_scrape --usar-ia --cantidad 1000
```

**Qué hace:**
- Usa el modelo `openai/gpt-oss-20b` de OpenRouter
- Genera datos realistas de vehículos
- 140+ campos por vehículo
- Precios de mercado españoles
- Descripciones detalladas
- ⏱️ Duración: ~5-10 minutos por cada 100 vehículos

### Generar vehículos sin IA (más rápido)

```bash
docker-compose exec backend python manage.py migrate_stock_and_scrape --cantidad 100
```

**Qué hace:**
- Genera datos aleatorios pero coherentes
- Más rápido que con IA
- Menos realista
- ⏱️ Duración: ~1-2 minutos

### Script manual de migración de stock

```bash
docker-compose exec backend python run_stock_migration.py --cantidad 100
```

**Qué hace:**
- Script alternativo para migrar stock
- Incluye scraping de coches.net (opcional)
- Más opciones de configuración

### Opciones adicionales para generación de stock

```bash
# Con scraping de páginas
docker-compose exec backend python manage.py migrate_stock_and_scrape --paginas 5 --cantidad 100

# Modo debug
docker-compose exec backend python manage.py migrate_stock_and_scrape --usar-ia --cantidad 10 --debug

# Limpiar stock antes de generar
docker-compose exec backend python manage.py migrate_stock_and_scrape --usar-ia --cantidad 100 --limpiar
```

---

## 👥 Gestión de Usuarios

### Crear superusuario manualmente

```bash
docker-compose exec backend python manage.py createsuperuser
```

**Qué hace:**
- Solicita username, email y password
- Crea un usuario con permisos de administrador

### Crear superusuario admin/admin123 automático

```bash
docker-compose exec backend python manage.py createsuperuser --username admin --email admin@dealaai.com --noinput
docker-compose exec backend python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u = User.objects.get(username='admin'); u.set_password('admin123'); u.save()"
```

**Qué hace:**
- Crea usuario admin con contraseña admin123
- Útil para desarrollo rápido

### Ver todos los usuarios

```bash
docker-compose exec backend python manage.py shell -c "from apps.authentication.models import User; print([f'{u.username} - {u.email}' for u in User.objects.all()])"
```

**Qué hace:**
- Lista todos los usuarios del sistema
- Muestra username y email

### Cambiar contraseña de un usuario

```bash
docker-compose exec backend python manage.py changepassword admin
```

**Qué hace:**
- Solicita nueva contraseña para el usuario especificado

---

## 🧪 Testing y Verificación

### Verificar modelos de OpenRouter disponibles

```bash
docker-compose exec backend python verificar_modelos_openrouter.py
```

**Qué hace:**
- Lista todos los modelos disponibles en OpenRouter
- Verifica que la API key sea válida
- Muestra precios por modelo

### Probar generación de vehículos con IA

```bash
docker-compose exec backend python test_ai_generator.py
```

**Qué hace:**
- Genera 1 vehículo de prueba con IA
- Muestra el JSON generado
- Útil para debugging

### Probar generación masiva

```bash
docker-compose exec backend python test_generacion_masiva.py
```

**Qué hace:**
- Genera múltiples vehículos
- Mide tiempos de generación
- Muestra métricas de rendimiento

### Comparar generadores (IA vs Aleatorio)

```bash
docker-compose exec backend python comparar_generadores.py
```

**Qué hace:**
- Compara calidad entre IA y generación aleatoria
- Muestra diferencias en datos generados
- Métricas de coherencia

### Verificar márgenes de precios

```bash
docker-compose exec backend python verificar_margenes.py
```

**Qué hace:**
- Valida que los precios de venta/compra sean coherentes
- Detecta márgenes negativos
- Reporta anomalías

---

## ⚙️ Administración del Sistema

### Acceder al shell de Django

```bash
docker-compose exec backend python manage.py shell
```

**Qué hace:**
- Abre shell interactivo de Python con Django configurado
- Puedes ejecutar queries, crear objetos, etc.

### Ejecutar comandos SQL directos

```bash
docker-compose exec backend python manage.py dbshell
```

**Qué hace:**
- Abre psql conectado a la base de datos
- Útil para queries SQL directas

### Ver configuración de Django

```bash
docker-compose exec backend python manage.py diffsettings
```

**Qué hace:**
- Muestra todas las configuraciones de Django
- Diferencias con valores por defecto

### Recolectar archivos estáticos

```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

**Qué hace:**
- Recopila archivos CSS/JS del admin de Django
- Los coloca en `staticfiles/`

### Limpiar sesiones expiradas

```bash
docker-compose exec backend python manage.py clearsessions
```

**Qué hace:**
- Elimina sesiones expiradas de la base de datos
- Libera espacio

---

## 🔧 Comandos de Desarrollo

### Acceder al contenedor del backend

```bash
docker-compose exec backend bash
```

**Qué hace:**
- Abre shell bash dentro del contenedor backend
- Útil para debugging y exploración

### Acceder al contenedor del frontend

```bash
docker-compose exec frontend sh
```

**Qué hace:**
- Abre shell sh dentro del contenedor frontend (Alpine Linux)

### Instalar dependencias nuevas en backend

```bash
# Agregar al requirements.txt primero, luego:
docker-compose up -d --build backend
```

**Qué hace:**
- Reconstruye la imagen con las nuevas dependencias
- Actualiza el contenedor

### Instalar dependencias nuevas en frontend

```bash
# Agregar al package.json primero, luego:
docker-compose exec frontend npm install
docker-compose restart frontend
```

**Qué hace:**
- Instala las nuevas dependencias de npm
- Reinicia el servicio

### Ver uso de recursos

```bash
docker stats
```

**Qué hace:**
- Muestra uso de CPU, memoria, red por contenedor
- Se actualiza en tiempo real

### Limpiar caché de Docker

```bash
docker system prune -a
```

**Qué hace:**
- Elimina contenedores detenidos
- Elimina imágenes no usadas
- Libera espacio en disco

---

## 📊 Verificación de Datos

### Contar registros en base de datos

```bash
docker-compose exec backend python manage.py shell << 'PYTHON'
from apps.authentication.models import Provincia, Concesionario, User, Profile
from apps.stock.models import Stock

print(f"📍 Provincias: {Provincia.objects.count()}")
print(f"🏢 Concesionarios: {Concesionario.objects.count()}")
print(f"👥 Usuarios: {User.objects.count()}")
print(f"📋 Perfiles: {Profile.objects.count()}")
print(f"🚗 Vehículos: {Stock.objects.count()}")
PYTHON
```

**Qué hace:**
- Cuenta registros en cada tabla principal
- Verifica que los datos se generaron correctamente

### Ver últimos vehículos agregados

```bash
docker-compose exec backend python manage.py shell -c "from apps.stock.models import Stock; [print(f'{v.marca} {v.modelo} - {v.precio_venta}€') for v in Stock.objects.order_by('-fecha_recepcion')[:10]]"
```

**Qué hace:**
- Muestra los últimos 10 vehículos agregados
- Con marca, modelo y precio

### Ver usuarios por nivel jerárquico

```bash
docker-compose exec backend python manage.py shell -c "from apps.authentication.models import User; from collections import Counter; print(Counter([u.nivel for u in User.objects.all()]))"
```

**Qué hace:**
- Cuenta usuarios por nivel jerárquico
- Muestra distribución organizacional

---

## 🌐 URLs Importantes

### Acceso a servicios

- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8080/api/
- **Admin Django**: http://localhost:8080/admin/
- **pgAdmin**: http://localhost:5050
- **API Docs**: http://localhost:8080/api/docs/
- **Health Check**: http://localhost:8080/health/

### Credenciales por defecto

**Admin Django:**
- Usuario: `admin`
- Contraseña: `admin123`

**pgAdmin:**
- Email: `admin@dealaai.com`
- Contraseña: `admin123`

**Base de datos PostgreSQL:**
- Host: `localhost` (o `db` dentro de Docker)
- Puerto: `5432`
- Usuario: `postgres`
- Contraseña: `postgres`
- Base de datos: `dealaai_dev`

---

## 🆘 Troubleshooting

### Contenedor no inicia

```bash
# Ver logs detallados
docker-compose logs backend

# Reconstruir la imagen
docker-compose up -d --build backend
```

### Error de permisos en entrypoint.sh

```bash
# En Git Bash o WSL
chmod +x backend/entrypoint.sh

# Reconstruir
docker-compose up -d --build backend
```

### Base de datos corrupta

```bash
# Detener todo
docker-compose down -v

# Volver a levantar
docker-compose up -d

# Generar datos
docker-compose exec backend python generar_datos_completos.py
```

### Puerto ocupado

```bash
# Ver qué está usando el puerto 8080
netstat -ano | findstr :8080

# Cambiar puerto en .env
NGINX_PORT=8081
```

### API Key de OpenRouter inválida

```bash
# Verificar en .env
cat .env | grep DEEPSEEK_API_KEY

# Actualizar
echo "DEEPSEEK_API_KEY=sk-or-v1-nueva-key" >> .env

# Reiniciar backend
docker-compose restart backend
```

---

## 📝 Notas Importantes

1. **Orden de Generación**: Siempre genera en este orden:
   - Provincias → Concesionarios → Usuarios → Perfiles → Vehículos

2. **API Key**: La generación con IA requiere una API key válida de OpenRouter

3. **Tiempo**: La generación masiva con IA puede tardar varios minutos

4. **Preservar Admin**: Usa `--no-borrar-admin` al generar usuarios

5. **Docker**: Siempre ejecuta comandos con `docker-compose exec backend`

---

## 🎯 Flujos de Trabajo Comunes

### Primer Setup Completo

```bash
# 1. Levantar servicios
docker-compose up -d

# 2. Esperar a que estén listos (30 segundos)
sleep 30

# 3. Generar todos los datos
docker-compose exec backend python generar_datos_completos.py

# 4. Acceder a http://localhost:8080/admin/
```

### Desarrollo Diario

```bash
# Levantar servicios
docker-compose up -d

# Ver logs mientras trabajas
docker-compose logs -f backend

# Hacer cambios en código...

# Reiniciar si cambias .env
docker-compose restart backend

# Reconstruir si cambias dependencias
docker-compose up -d --build backend
```

### Resetear Todo y Empezar Limpio

```bash
# 1. Detener y limpiar
docker-compose down -v

# 2. Eliminar caché de Docker
docker system prune -a

# 3. Levantar de nuevo
docker-compose up -d --build

# 4. Generar datos
docker-compose exec backend python generar_datos_completos.py
```

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisa logs**: `docker-compose logs backend`
2. **Verifica variables**: `cat .env`
3. **Reconstruye**: `docker-compose up -d --build`
4. **Limpia y reinicia**: Ver sección "Resetear Todo"

---

**Última actualización**: 2025-01-29  
**Versión**: 1.0.0  
**Proyecto**: DealaAI - Sistema de Gestión de Inventario de Vehículos
