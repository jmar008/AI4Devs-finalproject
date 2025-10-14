"""
Tests para verificar la configuración inicial del proyecto Django.
"""

import pytest
from django.conf import settings
from django.db import connection
from django.test import TestCase


class TestDjangoSetup(TestCase):
    """Tests para verificar que Django está configurado correctamente."""

    def test_settings_loaded(self):
        """Verificar que los settings se cargan correctamente."""
        self.assertTrue(settings.SECRET_KEY)
        self.assertFalse(settings.DEBUG)  # DEBUG debe ser False en development
        self.assertIn('localhost', settings.ALLOWED_HOSTS)
        self.assertEqual(settings.LANGUAGE_CODE, 'es-es')
        self.assertEqual(settings.TIME_ZONE, 'Europe/Madrid')

    def test_database_connection(self):
        """Verificar que la base de datos está conectada."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

    def test_installed_apps(self):
        """Verificar que las apps necesarias están instaladas."""
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'corsheaders',
            'drf_spectacular',
        ]

        for app in required_apps:
            self.assertIn(app, settings.INSTALLED_APPS)

    def test_rest_framework_config(self):
        """Verificar configuración de Django REST Framework."""
        self.assertIn('rest_framework', settings.INSTALLED_APPS)
        self.assertIn('DEFAULT_AUTHENTICATION_CLASSES', settings.REST_FRAMEWORK)
        self.assertIn('DEFAULT_PERMISSION_CLASSES', settings.REST_FRAMEWORK)
        self.assertEqual(settings.REST_FRAMEWORK['PAGE_SIZE'], 20)

    def test_cors_config(self):
        """Verificar configuración de CORS."""
        self.assertIn('corsheaders', settings.INSTALLED_APPS)
        self.assertIn('corsheaders.middleware.CorsMiddleware', settings.MIDDLEWARE)
        self.assertIn('http://localhost:3000', settings.CORS_ALLOWED_ORIGINS)

    def test_static_media_config(self):
        """Verificar configuración de archivos estáticos y media."""
        self.assertEqual(settings.STATIC_URL, '/static/')
        self.assertEqual(settings.MEDIA_URL, '/media/')
        self.assertTrue(str(settings.STATIC_ROOT).endswith('staticfiles'))
        self.assertTrue(str(settings.MEDIA_ROOT).endswith('media'))


class TestEnvironmentVariables(TestCase):
    """Tests para verificar que las variables de entorno se cargan."""

    def test_secret_key_from_env(self):
        """Verificar que SECRET_KEY se carga desde variables de entorno."""
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, 'django-insecure-key')

    def test_database_config_from_env(self):
        """Verificar que la configuración de BD se carga desde env."""
        db_config = settings.DATABASES['default']
        self.assertEqual(db_config['ENGINE'], 'django.db.backends.postgresql')
        # En tests Django agrega prefijo 'test_' al nombre de la BD
        self.assertTrue(db_config['NAME'].endswith('dealaai_dev'))
        self.assertEqual(db_config['USER'], 'postgres')
        self.assertEqual(db_config['HOST'], 'localhost')