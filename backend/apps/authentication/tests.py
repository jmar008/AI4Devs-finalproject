import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    """Crear un usuario de prueba"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        profile='AC',  # Agente Comercial
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def authenticated_client(api_client, test_user):
    """Cliente autenticado"""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.mark.django_db
class TestUserModel:
    """Tests para el modelo User"""
    
    def test_create_user(self):
        """Test crear usuario básico"""
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='password123',
            profile='DC'
        )
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.profile == 'DC'
        assert user.check_password('password123')
    
    def test_user_str_representation(self):
        """Test representación string del usuario"""
        user = User.objects.create_user(
            username='testuser',
            password='pass123',
            profile='GC'
        )
        assert 'testuser' in str(user)
        assert 'Gerente Gerente' in str(user)
    
    def test_user_profile_choices(self):
        """Test que los perfiles válidos funcionan"""
        profiles = ['DC', 'GC', 'AC', 'TAS']
        for profile in profiles:
            user = User.objects.create_user(
                username=f'user_{profile}',
                password='pass123',
                profile=profile
            )
            assert user.profile == profile


@pytest.mark.django_db
class TestUserAPI:
    """Tests para la API de usuarios"""
    
    def test_create_user_api(self, api_client):
        """Test crear usuario via API"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User',
            'profile': 'AC'
        }
        response = api_client.post('/api/auth/users/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'password' not in response.data
        assert response.data['username'] == 'newuser'
        assert response.data['profile'] == 'AC'
    
    def test_create_user_password_mismatch(self, api_client):
        """Test error cuando las contraseñas no coinciden"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'DifferentPass123!',
            'profile': 'AC'
        }
        response = api_client.post('/api/auth/users/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
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
    
    def test_login_invalid_credentials(self, api_client, test_user):
        """Test login con credenciales inválidas"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = api_client.post('/api/auth/users/login/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_logout(self, authenticated_client):
        """Test logout"""
        response = authenticated_client.post('/api/auth/users/logout/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_get_current_user(self, authenticated_client, test_user):
        """Test obtener usuario actual"""
        response = authenticated_client.get('/api/auth/users/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == test_user.username
        assert response.data['email'] == test_user.email
    
    def test_change_password(self, authenticated_client, test_user):
        """Test cambiar contraseña"""
        data = {
            'old_password': 'testpass123',
            'new_password': 'NewSecurePass123!',
            'new_password_confirm': 'NewSecurePass123!'
        }
        response = authenticated_client.post('/api/auth/users/change_password/', data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que la nueva contraseña funciona
        test_user.refresh_from_db()
        assert test_user.check_password('NewSecurePass123!')
    
    def test_change_password_wrong_old_password(self, authenticated_client):
        """Test cambiar contraseña con contraseña antigua incorrecta"""
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'NewSecurePass123!',
            'new_password_confirm': 'NewSecurePass123!'
        }
        response = authenticated_client.post('/api/auth/users/change_password/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_list_users_requires_authentication(self, api_client):
        """Test que listar usuarios requiere autenticación"""
        response = api_client.get('/api/auth/users/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_users_authenticated(self, authenticated_client, test_user):
        """Test listar usuarios autenticado"""
        response = authenticated_client.get('/api/auth/users/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
