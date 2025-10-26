"""
Staging settings for dealaai project.
"""

from decouple import config
from .production import *

# Override production settings for staging
DEBUG = config('DEBUG', default=True, cast=bool)

# Allow staging domain
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=['staging.dealaai.com'], cast=lambda v: [s.strip() for s in v.split(',')])

# Database (staging database)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='dealaai_staging'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# CORS for staging
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='https://staging.dealaai.com',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Email backend for staging (console for testing)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'