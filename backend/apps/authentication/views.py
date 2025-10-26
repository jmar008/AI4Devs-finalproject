from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.db.models import Q
from .models import User, Perfil, Provincia, Concesionario
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    ProvinciaSerializer,
    ConcesionarioSerializer,
    PerfilSerializer
)


class ProvinciaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar provincias.

    Endpoints:
    - GET /api/provincias/ - Listar provincias
    - POST /api/provincias/ - Crear provincia
    - GET /api/provincias/{id}/ - Detalle de provincia
    - PUT/PATCH /api/provincias/{id}/ - Actualizar provincia
    - DELETE /api/provincias/{id}/ - Eliminar provincia
    """

    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """Solo staff puede crear, actualizar o eliminar"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class ConcesionarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar concesionarios.

    Endpoints:
    - GET /api/concesionarios/ - Listar concesionarios
    - POST /api/concesionarios/ - Crear concesionario
    - GET /api/concesionarios/{id}/ - Detalle de concesionario
    - PUT/PATCH /api/concesionarios/{id}/ - Actualizar concesionario
    - DELETE /api/concesionarios/{id}/ - Eliminar concesionario
    """

    queryset = Concesionario.objects.select_related('provincia').all()
    serializer_class = ConcesionarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """Solo staff puede crear, actualizar o eliminar"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Filtrar concesionarios por parámetros"""
        queryset = super().get_queryset()
        provincia_id = self.request.query_params.get('provincia', None)
        activo = self.request.query_params.get('activo', None)

        if provincia_id:
            queryset = queryset.filter(provincia_id=provincia_id)

        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')

        return queryset


class PerfilViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar perfiles (permitir añadir/modificar igual que grupos).
    """
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


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
    - GET /api/users/subordinados/ - Subordinados del usuario actual
    - GET /api/users/jerarquia/ - Jerarquía del usuario actual
    """

    queryset = User.objects.select_related('jefe', 'concesionario', 'provincia').all()
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

    def get_queryset(self):
        """Filtrar usuarios por parámetros"""
        queryset = super().get_queryset()
        concesionario_id = self.request.query_params.get('concesionario', None)
        provincia_id = self.request.query_params.get('provincia', None)
        profile = self.request.query_params.get('profile', None)
        jefe_id = self.request.query_params.get('jefe', None)
        chat_ai_activo = self.request.query_params.get('chat_ai_activo', None)
        search = self.request.query_params.get('search', None)

        if concesionario_id:
            queryset = queryset.filter(concesionario_id=concesionario_id)

        if provincia_id:
            queryset = queryset.filter(provincia_id=provincia_id)

        if profile:
            queryset = queryset.filter(profile=profile)

        if jefe_id:
            queryset = queryset.filter(jefe_id=jefe_id)

        if chat_ai_activo is not None:
            queryset = queryset.filter(chat_ai_activo=chat_ai_activo.lower() == 'true')

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(movil__icontains=search)
            )

        return queryset

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

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def set_password(self, request, pk=None):
        """Permite a un admin establecer la contraseña de otro usuario.

        Payload: {"new_password": "...", "new_password_confirm": "..."}
        """
        user = self.get_object()
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')

        if not new_password or not new_password_confirm:
            return Response({'detail': 'new_password y new_password_confirm son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != new_password_confirm:
            return Response({'detail': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)

        # validar contraseña con los validadores de Django
        from django.contrib.auth.password_validation import validate_password
        try:
            validate_password(new_password, user=user)
        except Exception as exc:
            # exc puede ser ValidationError
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Contraseña actualizada por admin.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def subordinados(self, request):
        """
        Obtener subordinados del usuario actual
        """
        subordinados = request.user.subordinados.all()
        serializer = self.get_serializer(subordinados, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def jerarquia(self, request):
        """
        Obtener jerarquía del usuario actual
        """
        jerarquia = request.user.get_jerarquia()
        serializer = self.get_serializer(jerarquia, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def subordinados_detail(self, request, pk=None):
        """
        Obtener subordinados de un usuario específico
        """
        user = self.get_object()
        subordinados = user.subordinados.all()
        serializer = self.get_serializer(subordinados, many=True)
        return Response(serializer.data)
