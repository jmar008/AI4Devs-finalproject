import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Provincia, Concesionario, Perfil

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_provincia(db):
    """Crear una provincia de prueba"""
    return Provincia.objects.create(
        nombre='Madrid',
        codigo='28'
    )


@pytest.fixture
def test_concesionario(db, test_provincia):
    """Crear un concesionario de prueba"""
    return Concesionario.objects.create(
        nombre='Test Motors Madrid',
        direccion='Calle Test 123',
        telefono='915123456',
        email='test@testmotors.com',
        provincia=test_provincia
    )


@pytest.fixture
def test_user(db, test_provincia, test_concesionario):
    """Crear un usuario de prueba"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        profile=None,
        first_name='Test',
        last_name='User',
        provincia=test_provincia,
        concesionario=test_concesionario,
        movil='666123456',
        chat_ai_activo=True
    )


@pytest.fixture
def test_jefe(db, test_provincia, test_concesionario):
    """Crear un usuario jefe de prueba"""
    return User.objects.create_user(
        username='jefe',
        email='jefe@example.com',
        password='jefepass123',
        profile=None,
        first_name='Jefe',
        last_name='Test',
        provincia=test_provincia,
        concesionario=test_concesionario,
        movil='666654321',
        chat_ai_activo=True
    )


@pytest.fixture
def test_perfil(db):
    """Crear un perfil de prueba"""
    return Perfil.objects.create(codigo='AC', nombre='Agente Comercial')


@pytest.fixture
def authenticated_client(api_client, test_user):
    """Cliente autenticado"""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.mark.django_db
class TestProvinciaModel:
    """Tests para el modelo Provincia"""

    def test_create_provincia(self):
        """Test crear provincia"""
        provincia = Provincia.objects.create(
            nombre='Barcelona',
            codigo='08'
        )
        assert provincia.nombre == 'Barcelona'
        assert provincia.codigo == '08'
        assert str(provincia) == 'Barcelona'


@pytest.mark.django_db
class TestConcesionarioModel:
    """Tests para el modelo Concesionario"""

    def test_create_concesionario(self, test_provincia):
        """Test crear concesionario"""
        concesionario = Concesionario.objects.create(
            nombre='Barcelona Motors',
            direccion='Passeig de Gràcia 123',
            telefono='934567890',
            email='info@barcelonamotors.com',
            provincia=test_provincia
        )
        assert concesionario.nombre == 'Barcelona Motors'
        assert concesionario.provincia == test_provincia
        assert concesionario.activo is True
        assert 'Barcelona Motors' in str(concesionario)


@pytest.mark.django_db
class TestUserModel:
    """Tests para el modelo User"""

    def test_create_user_with_new_fields(self, test_provincia, test_concesionario):
        """Test crear usuario con los nuevos campos"""
        perfil = Perfil.objects.create(codigo='DC', nombre='Director Comercial')
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='password123',
            profile=perfil,
            provincia=test_provincia,
            concesionario=test_concesionario,
            movil='666789012',
            chat_ai_activo=False
        )
        assert user.username == 'newuser'
        assert user.provincia == test_provincia
        assert user.concesionario == test_concesionario
        assert user.movil == '666789012'
        assert user.chat_ai_activo is False

    def test_user_jerarquia(self, test_user, test_jefe):
        """Test jerarquía de usuarios"""
        test_user.jefe = test_jefe
        test_user.save()

        assert test_user.jefe == test_jefe
        assert test_user in test_jefe.subordinados.all()

        jerarquia = test_user.get_jerarquia()
        assert test_jefe in jerarquia

    def test_user_nombre_completo(self, test_user):
        """Test nombre completo del usuario"""
        assert test_user.nombre_completo == 'Test User'

    def test_user_tiene_subordinados(self, test_user, test_jefe):
        """Test verificar si tiene subordinados"""
        test_user.jefe = test_jefe
        test_user.save()

        assert test_jefe.tiene_subordinados() is True
        assert test_user.tiene_subordinados() is False


@pytest.mark.django_db
class TestProvinciaAPI:
    """Tests para la API de provincias"""

    def test_list_provincias(self, authenticated_client, test_provincia):
        """Test listar provincias"""
        response = authenticated_client.get('/api/auth/provincias/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_create_provincia_requires_admin(self, authenticated_client):
        """Test que crear provincia requiere permisos de admin"""
        data = {
            'nombre': 'Valencia',
            'codigo': '46'
        }
        response = authenticated_client.post('/api/auth/provincias/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestConcesionarioAPI:
    """Tests para la API de concesionarios"""

    def test_list_concesionarios(self, authenticated_client, test_concesionario):
        """Test listar concesionarios"""
        response = authenticated_client.get('/api/auth/concesionarios/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_filter_concesionarios_by_provincia(self, authenticated_client, test_concesionario):
        """Test filtrar concesionarios por provincia"""
        response = authenticated_client.get(f'/api/auth/concesionarios/?provincia={test_concesionario.provincia.id}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_create_concesionario_requires_admin(self, authenticated_client, test_provincia):
        """Test que crear concesionario requiere permisos de admin"""
        data = {
            'nombre': 'Nuevo Concesionario',
            'provincia': test_provincia.id
        }
        response = authenticated_client.post('/api/auth/concesionarios/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestUserAPI:
    """Tests para la API de usuarios"""

    def test_create_user_with_new_fields(self, api_client, test_provincia, test_concesionario):
        """Test crear usuario con nuevos campos via API"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User',
            'profile': None,
            'provincia': test_provincia.id,
            'concesionario': test_concesionario.id,
            'movil': '666999888',
            'chat_ai_activo': True
        }
        response = api_client.post('/api/auth/users/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['provincia'] == test_provincia.id
        assert response.data['concesionario'] == test_concesionario.id
        assert response.data['movil'] == '666999888'
        assert response.data['chat_ai_activo'] is True

    def test_user_cannot_be_own_boss(self, authenticated_client, test_user):
        """Test que un usuario no puede ser su propio jefe"""
        data = {
            'jefe': test_user.id
        }
        response = authenticated_client.patch(f'/api/auth/users/{test_user.id}/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_subordinados(self, authenticated_client, test_user, test_jefe):
        """Test obtener subordinados"""
        test_user.jefe = test_jefe
        test_user.save()

        # Autenticar como jefe
        authenticated_client.force_authenticate(user=test_jefe)
        response = authenticated_client.get('/api/auth/users/subordinados/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert response.data[0]['id'] == test_user.id

    def test_get_jerarquia(self, authenticated_client, test_user, test_jefe):
        """Test obtener jerarquía"""
        test_user.jefe = test_jefe
        test_user.save()

        response = authenticated_client.get('/api/auth/users/jerarquia/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert response.data[0]['id'] == test_jefe.id

    def test_filter_users_by_concesionario(self, authenticated_client, test_user):
        """Test filtrar usuarios por concesionario"""
        response = authenticated_client.get(f'/api/auth/users/?concesionario={test_user.concesionario.id}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_filter_users_by_provincia(self, authenticated_client, test_user):
        """Test filtrar usuarios por provincia"""
        response = authenticated_client.get(f'/api/auth/users/?provincia={test_user.provincia.id}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_search_users(self, authenticated_client, test_user):
        """Test buscar usuarios"""
        response = authenticated_client.get('/api/auth/users/?search=Test')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_login_success(self, api_client, test_user):
        """Test login exitoso"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post('/api/auth/users/login/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert 'user' in response.data
        assert response.data['user']['username'] == 'testuser'
        assert response.data['user']['chat_ai_activo'] is True

    def test_get_current_user_with_detailed_info(self, authenticated_client, test_user):
        """Test obtener usuario actual con información detallada"""
        response = authenticated_client.get('/api/auth/users/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == test_user.username
        assert response.data['provincia_info']['nombre'] == test_user.provincia.nombre
        assert response.data['concesionario_info']['nombre'] == test_user.concesionario.nombre
        assert response.data['movil'] == test_user.movil
        assert response.data['chat_ai_activo'] == test_user.chat_ai_activo
