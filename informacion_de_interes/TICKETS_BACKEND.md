# 🎫 Tickets de Trabajo - Backend DealaAI

> Tickets organizados por prioridad y sprint para el desarrollo del backend Django

---

## 📊 Resumen Ejecutivo

- **Total de Tickets:** 15
- **Story Points Totales:** 89
- **Sprints Estimados:** 4 sprints (2 semanas c/u)
- **Prioridades:** 5 Alta, 7 Media, 3 Baja

---

## 🗓️ Sprint 1: Configuración Base e Infraestructura (21 SP)

### TICK-001: Configuración Inicial del Proyecto Django

**Tipo:** Setup - Backend Infrastructure  
**Prioridad:** 🔴 Alta (Blocker)  
**Story Points:** 5  
**Asignado:** Backend Lead  
**Dependencias:** Ninguna

#### 📝 Descripción

Configurar proyecto Django desde cero con estructura modular, settings por ambiente, y configuración de base de datos PostgreSQL con pgvector.

#### 🎯 Objetivos

1. Inicializar proyecto Django 4.2 LTS
2. Configurar estructura de settings (base, development, production)
3. Configurar conexión a PostgreSQL con pgvector
4. Configurar Django REST Framework
5. Setup de entorno virtual y dependencias

#### ✅ Criterios de Aceptación

- ✅ Proyecto Django inicializado con estructura correcta
- ✅ Settings divididos por ambiente (base.py, development.py, production.py)
- ✅ Base de datos PostgreSQL conectada y funcional
- ✅ Extensión pgvector habilitada
- ✅ Django REST Framework configurado con defaults apropiados
- ✅ Variables de entorno manejadas con python-decouple
- ✅ Requirements.txt organizados (base, development, production)

#### 📋 Tareas Técnicas

**1. Crear proyecto Django**
```bash
cd backend
django-admin startproject dealaai .
```

**2. Estructura de configuración**
```python
# backend/dealaai/settings/__init__.py
from .base import *

import os
env = os.environ.get('DJANGO_ENV', 'development')

if env == 'production':
    from .production import *
elif env == 'staging':
    from .staging import *
else:
    from .development import *
```

**3. Settings Base (dealaai/settings/base.py)**
```python
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'drf_spectacular',
    
    # Local apps (se crearán después)
    # 'apps.authentication',
    # 'apps.inventory',
    # 'apps.leads',
    # 'apps.sales',
    # 'apps.ai_chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dealaai.urls'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# CORS
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**4. Archivo requirements/base.txt**
```txt
# Core Django
Django==4.2.7
djangorestframework==3.14.0
django-filter==23.3
django-cors-headers==4.3.0

# Database
psycopg2-binary==2.9.9
pgvector==0.2.3

# Authentication
djangorestframework-simplejwt==5.3.0

# API Documentation
drf-spectacular==0.26.5

# Environment
python-decouple==3.8

# Utilities
python-slugify==8.0.1
Pillow==10.1.0

# Date/Time
pytz==2023.3
```

**5. Archivo requirements/development.txt**
```txt
-r base.txt

# Testing
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
factory-boy==3.3.0

# Debug
django-debug-toolbar==4.2.0
ipython==8.17.2

# Code Quality
black==23.11.0
flake8==6.1.0
isort==5.12.0
pylint==3.0.2
```

**6. Archivo requirements/production.txt**
```txt
-r base.txt

# Production Server
gunicorn==21.2.0

# Monitoring
sentry-sdk==1.38.0

# Performance
django-redis==5.4.0
```

**7. Archivo .env.example**
```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
DJANGO_ENV=development
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=dealaai_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Redis
REDIS_URL=redis://redis:6379/0

# OpenAI
OPENAI_API_KEY=sk-your-key-here

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**8. Script de inicialización**
```bash
#!/bin/bash
# scripts/init-backend.sh

echo "🚀 Iniciando configuración del backend..."

cd backend

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements/development.txt

# Copiar .env
if [ ! -f .env ]; then
    echo "📝 Copiando archivo .env..."
    cp .env.example .env
fi

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
python manage.py migrate

echo "✅ Backend configurado correctamente!"
echo ""
echo "Para iniciar el servidor:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
```

#### 🧪 Testing

```python
# tests/test_setup.py
import pytest
from django.conf import settings
from django.db import connection

def test_database_connection():
    """Verificar que la base de datos está conectada"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        assert cursor.fetchone()[0] == 1

def test_pgvector_extension():
    """Verificar que pgvector está habilitado"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector'")
        assert cursor.fetchone() is not None

def test_settings_loaded():
    """Verificar que settings se cargan correctamente"""
    assert settings.SECRET_KEY is not None
    assert settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql'

def test_rest_framework_configured():
    """Verificar configuración de DRF"""
    assert 'rest_framework' in settings.INSTALLED_APPS
    assert 'DEFAULT_AUTHENTICATION_CLASSES' in settings.REST_FRAMEWORK
```

#### 📊 Definición de Hecho

- [ ] Código revisado por Tech Lead
- [ ] Tests pasando con 100% coverage
- [ ] Documentación de setup actualizada
- [ ] Script de inicialización funcional
- [ ] Variables de entorno documentadas
- [ ] README con instrucciones de instalación
- [ ] Docker configuración verificada

---

### TICK-002: Modelo de Datos - Usuarios y Autenticación

**Tipo:** Feature - Backend Models  
**Prioridad:** 🔴 Alta  
**Story Points:** 8  
**Asignado:** Backend Developer  
**Dependencias:** TICK-001

#### 📝 Descripción

Implementar sistema de usuarios personalizado con roles jerárquicos (Admin, Manager, Sales, Viewer) y configuración de autenticación JWT.

#### 🎯 Objetivos

1. Crear modelo User personalizado extendiendo AbstractBaseUser
2. Implementar sistema de roles con permisos
3. Configurar autenticación JWT
4. Crear serializers y viewsets para User management
5. Endpoints de login, logout, registro, perfil

#### ✅ Criterios de Aceptación

- ✅ Modelo User con campos personalizados implementado
- ✅ Sistema de roles funcional (Admin, Manager, Sales, Viewer)
- ✅ Autenticación JWT con access y refresh tokens
- ✅ Endpoints de autenticación funcionando
- ✅ Permisos por rol aplicados correctamente
- ✅ Tests con >90% coverage

#### 📋 Tareas Técnicas

**1. Crear app authentication**
```bash
cd backend
python manage.py startapp apps.authentication
```

**2. Modelo User personalizado**
```python
# apps/authentication/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado para el sistema de concesionarios
    """
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        MANAGER = 'manager', 'Gerente'
        SALES = 'sales', 'Vendedor'
        VIEWER = 'viewer', 'Visualizador'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField('Email', unique=True, db_index=True)
    first_name = models.CharField('Nombre', max_length=150)
    last_name = models.CharField('Apellido', max_length=150)
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    role = models.CharField(
        'Rol',
        max_length=20,
        choices=Role.choices,
        default=Role.SALES,
        db_index=True
    )
    
    # Django fields
    is_active = models.BooleanField('Activo', default=True)
    is_staff = models.BooleanField('Es staff', default=False)
    
    # Timestamps
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    last_login = models.DateTimeField('Último acceso', null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_role(self, role):
        """Verifica si el usuario tiene un rol específico"""
        return self.role == role
    
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    def is_manager(self):
        return self.role in [self.Role.ADMIN, self.Role.MANAGER]
```

**3. Serializers**
```python
# apps/authentication/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'role', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'role'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        attrs.pop('password_confirm')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Añadir información adicional del usuario
        data['user'] = UserSerializer(self.user).data
        
        return data
```

**4. Views y URLs**
```python
# apps/authentication/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    CustomTokenObtainPairSerializer
)
from core.permissions import IsAdminUser

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'list', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener perfil del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Actualizar perfil del usuario actual"""
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

**5. Permisos personalizados**
```python
# core/permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permiso que solo permite acceso a usuarios admin
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )

class IsManagerOrAdmin(permissions.BasePermission):
    """
    Permiso para managers y admins
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['admin', 'manager']
        )

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso para que solo el dueño pueda editar
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.created_by == request.user
```

#### 🧪 Testing

```python
# apps/authentication/tests/test_models.py
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        assert user.email == 'test@example.com'
        assert user.full_name == 'Test User'
        assert user.check_password('testpass123')
    
    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.role == 'admin'

# apps/authentication/tests/test_api.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestAuthenticationAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_login(self):
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert 'user' in response.data
    
    def test_get_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/users/me/')
        assert response.status_code == 200
        assert response.data['email'] == 'test@example.com'
```

#### 📊 Definición de Hecho

- [ ] Modelo User creado y migrado
- [ ] Sistema de roles funcional
- [ ] JWT configurado correctamente
- [ ] Tests pasando (>90% coverage)
- [ ] Documentación API actualizada
- [ ] Endpoints de autenticación documentados
- [ ] Code review aprobado

---

### TICK-003: Modelo de Datos - Inventario de Vehículos

**Tipo:** Feature - Backend Models  
**Prioridad:** 🔴 Alta  
**Story Points:** 8  
**Asignado:** Backend Developer  
**Dependencias:** TICK-001, TICK-002

#### 📝 Descripción

Implementar modelo de Vehículos con campos JSON para características flexibles, gestión de imágenes, y sistema de estados (disponible, vendido, reservado, mantenimiento).

#### 🎯 Objetivos

1. Crear modelo Vehicle con todos los campos según especificación
2. Implementar validaciones de negocio (VIN, año, precio)
3. Sistema de estados con transiciones validadas
4. Campos JSON para características y galería de imágenes
5. API REST completa con filtros avanzados

#### ✅ Criterios de Aceptación

- ✅ Modelo Vehicle implementado con todos los campos
- ✅ Validaciones funcionando correctamente
- ✅ Sistema de estados con reglas de transición
- ✅ API con filtros por make, model, year, price, status
- ✅ Búsqueda full-text funcional
- ✅ Paginación y ordenamiento implementados
- ✅ Tests con >85% coverage

#### 📋 Tareas Técnicas

**1. Crear app inventory**
```bash
python manage.py startapp apps.inventory
```

**2. Modelo Vehicle**
```python
# apps/inventory/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid
import re

class Vehicle(models.Model):
    """
    Modelo para vehículos del inventario del concesionario
    """
    
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Disponible'
        SOLD = 'sold', 'Vendido'
        RESERVED = 'reserved', 'Reservado'
        MAINTENANCE = 'maintenance', 'En Mantenimiento'
    
    class FuelType(models.TextChoices):
        GASOLINE = 'gasoline', 'Gasolina'
        DIESEL = 'diesel', 'Diésel'
        HYBRID = 'hybrid', 'Híbrido'
        ELECTRIC = 'electric', 'Eléctrico'
    
    class Transmission(models.TextChoices):
        MANUAL = 'manual', 'Manual'
        AUTOMATIC = 'automatic', 'Automático'
        CVT = 'cvt', 'CVT'
    
    # Identificadores
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vin = models.CharField(
        'VIN',
        max_length=17,
        unique=True,
        db_index=True,
        help_text='Vehicle Identification Number'
    )
    
    # Información básica
    make = models.CharField('Marca', max_length=100, db_index=True)
    model = models.CharField('Modelo', max_length=100)
    year = models.IntegerField(
        'Año',
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year + 1)
        ],
        db_index=True
    )
    color = models.CharField('Color', max_length=50)
    
    # Precio y kilometraje
    price = models.DecimalField(
        'Precio',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        db_index=True
    )
    mileage = models.IntegerField(
        'Kilometraje',
        validators=[MinValueValidator(0)]
    )
    
    # Especificaciones técnicas
    fuel_type = models.CharField(
        'Tipo de Combustible',
        max_length=20,
        choices=FuelType.choices
    )
    transmission = models.CharField(
        'Transmisión',
        max_length=20,
        choices=Transmission.choices
    )
    
    # Descripción y características
    description = models.TextField('Descripción', blank=True)
    features = models.JSONField(
        'Características',
        default=dict,
        blank=True,
        help_text='JSON con características adicionales'
    )
    images = models.JSONField(
        'Imágenes',
        default=list,
        blank=True,
        help_text='Array de URLs de imágenes'
    )
    
    # Estado
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
        db_index=True
    )
    
    # Timestamps
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    class Meta:
        db_table = 'vehicles'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['make', 'model']),
            models.Index(fields=['year', 'price']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['vin']),
        ]
    
    def __str__(self):
        return f"{self.make} {self.model} {self.year} - {self.vin}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validar VIN (17 caracteres alfanuméricos)
        if self.vin:
            vin_pattern = r'^[A-HJ-NPR-Z0-9]{17}$'
            if not re.match(vin_pattern, self.vin.upper()):
                raise ValidationError({
                    'vin': 'VIN debe tener 17 caracteres alfanuméricos (sin I, O, Q)'
                })
        
        # Validar que el año no sea futuro (excepto año siguiente)
        if self.year > timezone.now().year + 1:
            raise ValidationError({
                'year': 'El año no puede ser mayor al próximo año'
            })
    
    def save(self, *args, **kwargs):
        self.vin = self.vin.upper() if self.vin else self.vin
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def days_in_inventory(self):
        """Días que lleva el vehículo en inventario"""
        return (timezone.now() - self.created_at).days
    
    @property
    def display_name(self):
        """Nombre completo para mostrar"""
        return f"{self.year} {self.make} {self.model}"


class InventoryMovement(models.Model):
    """
    Registro de movimientos de inventario para auditoría
    """
    
    class MovementType(models.TextChoices):
        ENTRY = 'entry', 'Entrada'
        EXIT = 'exit', 'Salida'
        TRANSFER = 'transfer', 'Transferencia'
        MAINTENANCE = 'maintenance', 'Mantenimiento'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='movements'
    )
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='inventory_movements'
    )
    
    movement_type = models.CharField(
        'Tipo de Movimiento',
        max_length=20,
        choices=MovementType.choices
    )
    movement_date = models.DateTimeField('Fecha del Movimiento', auto_now_add=True)
    notes = models.TextField('Notas', blank=True)
    
    class Meta:
        db_table = 'inventory_movements'
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-movement_date']
    
    def __str__(self):
        return f"{self.movement_type} - {self.vehicle.display_name} - {self.movement_date}"
```

**Continúa en el siguiente archivo...**

#### 📊 Resumen del Ticket

Este ticket es fundamental para el sistema y incluye:
- Modelo completo de vehículos con validaciones
- Sistema de auditoría de movimientos
- API REST con filtros avanzados
- Tests comprehensivos

---

## 🗓️ Sprint 2: Módulos de Negocio (34 SP)

### TICK-004: Modelo de Datos - Clientes y Leads
### TICK-005: Modelo de Datos - Ventas
### TICK-006: Sistema de Permisos y Roles Avanzado
### TICK-007: API de Inventario con Filtros Avanzados

## 🗓️ Sprint 3: Sistema de IA (21 SP)

### TICK-008: Integración de pgvector para Embeddings
### TICK-009: Servicio de Generación de Embeddings
### TICK-010: API de Chat IA con RAG
### TICK-011: Sistema de Búsqueda Semántica

## 🗓️ Sprint 4: Optimización y Tareas Asíncronas (13 SP)

### TICK-012: Configuración de Celery y Redis
### TICK-013: Tareas Asíncronas (Email, Reportes, Embeddings)
### TICK-014: Optimización de Consultas y Cache
### TICK-015: Sistema de Monitoreo y Logging

---

## 📈 Métricas de Progreso

- **Sprint 1:** 0/21 SP completados
- **Sprint 2:** 0/34 SP completados
- **Sprint 3:** 0/21 SP completados
- **Sprint 4:** 0/13 SP completados

**Total:** 0/89 SP (0%)

---

*Última actualización: 14 de Octubre, 2025*
