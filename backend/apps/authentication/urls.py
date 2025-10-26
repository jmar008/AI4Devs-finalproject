from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProvinciaViewSet, ConcesionarioViewSet, PerfilViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'provincias', ProvinciaViewSet, basename='provincia')
router.register(r'concesionarios', ConcesionarioViewSet, basename='concesionario')
router.register(r'perfiles', PerfilViewSet, basename='perfil')

urlpatterns = [
    path('', include(router.urls)),
    # Alias de login para compatibilidad
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login-alias'),
]
