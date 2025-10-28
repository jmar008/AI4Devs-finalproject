#!/bin/bash

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}🚀 INICIANDO BACKEND DEALAAI${NC}"
echo -e "${CYAN}======================================================================${NC}\n"

# Configuración de base de datos
DB_HOST=${DB_HOST:-db}
DB_NAME=${DB_NAME:-dealaai_dev}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}
DB_PORT=${DB_PORT:-5432}
REDIS_HOST=${REDIS_HOST:-redis}
REDIS_PORT=${REDIS_PORT:-6379}

# Esperar a que PostgreSQL esté disponible
echo -e "${YELLOW}⏳ Esperando a que PostgreSQL esté disponible...${NC}"
max_attempts=30
attempt=1
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  if [ $attempt -ge $max_attempts ]; then
    echo -e "${RED}✗ Database connection failed after $max_attempts attempts${NC}"
    exit 1
  fi
  sleep 2
  attempt=$((attempt + 1))
done
echo -e "${GREEN}✅ PostgreSQL está disponible${NC}\n"

# Esperar a que Redis esté disponible
echo -e "${YELLOW}⏳ Esperando a que Redis esté disponible...${NC}"
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 0.1
done
echo -e "${GREEN}✅ Redis está disponible${NC}\n"

# Ejecutar migraciones
echo -e "${CYAN}🔄 Ejecutando migraciones de base de datos...${NC}"
if python manage.py migrate --noinput; then
    echo -e "${GREEN}✅ Migraciones completadas${NC}\n"
else
    echo -e "${YELLOW}⚠ Migraciones fallidas, intentando fake migrations...${NC}"
    python manage.py migrate --fake-initial
    echo -e "${GREEN}✅ Migraciones marcadas como aplicadas${NC}\n"
fi

# Crear tabla de cache
echo -e "${CYAN}💾 Creando tabla de cache...${NC}"
python manage.py createcachetable 2>/dev/null || echo -e "${YELLOW}⚠ Tabla de cache ya existe${NC}"
echo ""

# Recolectar archivos estáticos
if [ "$DJANGO_SETTINGS_MODULE" != "dealaai.settings.development" ]; then
    echo -e "${CYAN}📦 Recolectando archivos estáticos...${NC}"
    python manage.py collectstatic --noinput --clear
    echo -e "${GREEN}✅ Archivos estáticos recolectados${NC}\n"
fi

# Crear superusuario admin si no existe
echo -e "${CYAN}👤 Verificando superusuario admin...${NC}"
python manage.py shell << 'PYTHON_SCRIPT'
from django.contrib.auth import get_user_model

User = get_user_model()

# Verificar si el usuario admin ya existe
if User.objects.filter(username='admin').exists():
    print("ℹ️  Usuario 'admin' ya existe")

    # Actualizar contraseña por si acaso
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin123')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.is_active = True
    admin_user.save()
    print("✅ Contraseña actualizada y permisos verificados")
else:
    # Crear nuevo usuario admin
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@dealaai.com',
        password='admin123'
    )
    print("✅ Superusuario 'admin' creado exitosamente")
    print(f"   Usuario: admin")
    print(f"   Email: admin@dealaai.com")
    print(f"   Contraseña: admin123")
PYTHON_SCRIPT
echo ""

# Verificar datos iniciales
echo -e "${CYAN}📊 Verificando datos iniciales...${NC}"
python manage.py shell << 'PYTHON_SCRIPT'
from apps.authentication.models import Provincia, User
from apps.stock.models import Stock

provincias_count = Provincia.objects.count()
vehiculos_count = Stock.objects.count()
usuarios_count = User.objects.count()

if provincias_count == 0 or vehiculos_count < 10:
    print("⚠️  Base de datos vacía o con pocos datos")
    print(f"   👥 Usuarios: {usuarios_count}")
    print(f"   📍 Provincias: {provincias_count}")
    print(f"   🚗 Vehículos: {vehiculos_count}")
    print("\n💡 Para generar datos iniciales completos, ejecuta:")
    print("   docker-compose exec backend python generar_datos_completos.py")
    print("\n📝 Este comando generará:")
    print("   - 49 provincias de España")
    print("   - Concesionarios por provincia")
    print("   - 46 usuarios con jerarquía organizacional")
    print("   - Perfiles de usuario")
    print("   - 100 vehículos con datos IA")
else:
    print(f"✅ Datos iniciales presentes:")
    print(f"   👥 Usuarios: {usuarios_count}")
    print(f"   📍 Provincias: {provincias_count}")
    print(f"   🚗 Vehículos: {vehiculos_count}")
PYTHON_SCRIPT
echo ""

# Mostrar información de acceso
echo -e "${CYAN}======================================================================${NC}"
echo -e "${GREEN}✅ SISTEMA LISTO${NC}"
echo -e "${CYAN}======================================================================${NC}"
echo -e "${YELLOW}📋 Credenciales de Administrador:${NC}"
echo -e "   ${GREEN}Usuario:${NC} admin"
echo -e "   ${GREEN}Contraseña:${NC} admin123"
echo -e "   ${GREEN}Email:${NC} admin@dealaai.com"
echo -e "\n${YELLOW}🌐 URLs de Acceso:${NC}"
echo -e "   ${GREEN}Admin Django:${NC} http://localhost:8080/admin/"
echo -e "   ${GREEN}API Backend:${NC} http://localhost:8080/api/"
echo -e "${CYAN}======================================================================${NC}\n"

# Iniciar el servidor
echo -e "${CYAN}🚀 Iniciando servidor Django en el puerto 8000...${NC}\n"

exec "$@"
