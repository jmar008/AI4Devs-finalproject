from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Perfil, Provincia, Concesionario


class ProvinciaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Provincia"""

    class Meta:
        model = Provincia
        fields = ['id', 'nombre', 'codigo']


class ConcesionarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Concesionario"""

    provincia_nombre = serializers.CharField(source='provincia.nombre', read_only=True)

    class Meta:
        model = Concesionario
        fields = [
            'id', 'nombre', 'direccion', 'telefono', 'email',
            'provincia', 'provincia_nombre', 'activo',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']


class UserBasicSerializer(serializers.ModelSerializer):
    """Serializer básico para usuario (para referencias anidadas)"""

    nombre_completo = serializers.ReadOnlyField()
    profile_info = serializers.SerializerMethodField()

    def get_profile_info(self, obj):
        if obj.profile:
            return {"id": obj.profile.id, "codigo": obj.profile.codigo, "nombre": obj.profile.nombre}
        return None

    class Meta:
        model = User
        fields = ['id', 'username', 'nombre_completo', 'profile', 'profile_info']


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User"""
    profile_info = serializers.SerializerMethodField()
    nombre_completo = serializers.ReadOnlyField()
    jefe_info = UserBasicSerializer(source='jefe', read_only=True)
    concesionario_info = ConcesionarioSerializer(source='concesionario', read_only=True)
    provincia_info = ProvinciaSerializer(source='provincia', read_only=True)
    subordinados_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'nombre_completo',
            'profile', 'profile_info', 'jefe', 'jefe_info', 'concesionario',
            'concesionario_info', 'provincia', 'provincia_info', 'chat_ai_activo',
            'movil', 'fecha_nacimiento', 'fecha_incorporacion', 'activo',
            'fecha_baja',
            'is_active', 'is_staff', 'date_joined', 'last_login', 'subordinados_count'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'subordinados_count']

    def get_subordinados_count(self, obj):
        """Devuelve el número de subordinados"""
        return obj.subordinados.count()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear usuarios"""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'profile', 'jefe', 'concesionario',
            'provincia', 'chat_ai_activo', 'movil', 'fecha_nacimiento',
            'fecha_incorporacion'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def validate_jefe(self, value):
        """Validar que el jefe no sea el mismo usuario"""
        if value and self.instance and value.id == self.instance.id:
            raise serializers.ValidationError("Un usuario no puede ser su propio jefe.")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar usuarios"""

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'profile', 'jefe',
            'concesionario', 'provincia', 'chat_ai_activo', 'movil',
            'fecha_nacimiento', 'fecha_incorporacion', 'activo', 'fecha_baja'
        ]

    def validate_jefe(self, value):
        """Validar que el jefe no sea el mismo usuario"""
        if value and self.instance and value.id == self.instance.id:
            raise serializers.ValidationError("Un usuario no puede ser su propio jefe.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar contraseña"""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Las contraseñas no coinciden."})
        return attrs


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Credenciales inválidas.')
            if not user.is_active:
                raise serializers.ValidationError('Usuario inactivo.')
        else:
            raise serializers.ValidationError('Debe incluir "username" y "password".')

        attrs['user'] = user
        return attrs


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['id', 'codigo', 'nombre', 'descripcion', 'activo']
