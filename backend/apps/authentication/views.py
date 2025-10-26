from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    LoginSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios.
    
    Endpoints:
    - GET /api/users/ - Listar usuarios
    - POST /api/users/ - Crear usuario
    - GET /api/users/{id}/ - Detalle de usuario
    - PUT/PATCH /api/users/{id}/ - Actualizar usuario
    - DELETE /api/users/{id}/ - Eliminar usuario
    - POST /api/users/login/ - Login
    - POST /api/users/logout/ - Logout
    - POST /api/users/change_password/ - Cambiar contraseña
    - GET /api/users/me/ - Usuario actual
    """
    
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        elif self.action == 'login':
            return LoginSerializer
        return UserSerializer
    
    def get_permissions(self):
        """
        Permisos personalizados por acción
        """
        if self.action in ['create', 'login']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """
        Login de usuario y generación de token
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Obtener o crear token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Logout de usuario y eliminación de token
        """
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        logout(request)
        
        return Response({
            'message': 'Logout exitoso'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Obtener información del usuario actual
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Cambiar contraseña del usuario actual
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Verificar contraseña actual
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': 'Contraseña actual incorrecta.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Establecer nueva contraseña
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Contraseña cambiada exitosamente'
        }, status=status.HTTP_200_OK)
