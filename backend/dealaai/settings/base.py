"""
Django settings for dealaai project.

Base settings shared across all environments.
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    # Django core
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
    'apps.authentication',
    'apps.stock',
    'apps.ai_chat',
    # 'apps.inventory',
    # 'apps.leads',
    # 'apps.sales',
    # 'apps.analytics',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dealaai.wsgi.application'

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

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # SessionAuthentication removido para evitar CSRF en API
        # Si necesitas usar el browsable API, puedes agregarlo solo en desarrollo
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
    # Habilitar orígenes locales comunes para desarrollo (puertos 3000/3001/3003)
    default='http://localhost:3000,http://localhost:3001,http://localhost:3003',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Permitir credentials de CORS (cookies / autenticación) en desarrollo
CORS_ALLOW_CREDENTIALS = True

# CSRF Configuration
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='http://localhost:8080,http://localhost:3000,http://localhost:3001,http://127.0.0.1:8080,http://127.0.0.1:3000,http://127.0.0.1:3001',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

CSRF_ALLOWED_ORIGINS = config(
    'CSRF_ALLOWED_ORIGINS',
    default='http://localhost:8080,http://localhost:3000,http://localhost:3001,http://127.0.0.1:8080,http://127.0.0.1:3000,http://127.0.0.1:3001',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Permitir CSRF desde localhost en desarrollo
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_HTTPONLY = False  # Permitir acceso desde JavaScript (necesario para Next.js)
CSRF_COOKIE_SAMESITE = 'Lax'  # Permite cookies en solicitudes same-site

# Internationalization
LANGUAGE_CODE = 'es-es'  # Español de España
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.User'

# OpenRouter AI Configuration (compatible con OpenAI SDK)
DEEPSEEK_API_KEY = config('DEEPSEEK_API_KEY', default='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')
DEEPSEEK_API_BASE = 'https://openrouter.ai/api/v1'  # OpenRouter endpoint
DEEPSEEK_MODEL = 'openai/gpt-oss-20b'  # Modelo principal - GPT-OSS-20B

# Lista de modelos de fallback (se intentarán en orden si el principal falla)
# Solo modelos verificados como disponibles en OpenRouter
DEEPSEEK_FALLBACK_MODELS = [
    'meta-llama/llama-3.3-70b-instruct:free',
    'deepseek/deepseek-r1-distill-llama-70b:free',
    'qwen/qwen-2.5-72b-instruct:free',
    'nousresearch/hermes-3-llama-3.1-405b:free',
    'qwen/qwen-2.5-coder-32b-instruct:free',
    'mistralai/mistral-small-3.2-24b-instruct:free',
    'cognitivecomputations/dolphin-mistral-24b-venice-edition:free',
    'deepseek/deepseek-chat-v3-0324:free',
    'deepseek/deepseek-r1-0528:free',
    'google/gemini-2.0-flash-exp:free',
    'qwen/qwen3-coder:free',
    'minimax/minimax-m2:free',
    'meta-llama/llama-3.3-8b-instruct:free',
    'mistralai/mistral-nemo:free',
    'google/gemma-3-12b-it:free',
    'qwen/qwen3-14b:free',
    'google/gemma-2-9b-it:free',
    'meta-llama/llama-3.2-3b-instruct:free',
    'mistralai/mistral-7b-instruct:free',
]
