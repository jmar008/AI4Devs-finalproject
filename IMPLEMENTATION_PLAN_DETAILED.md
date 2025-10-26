# 🎯 PLAN DE ACCIÓN DETALLADO - PRÓXIMAS SEMANAS

## Fase 1: API Backend de Stock (Día 1-2)

### Tarea 1.1: Crear Serializers de Stock

**Archivo:** `/workspace/backend/apps/stock/serializers.py`

```python
from rest_framework import serializers
from .models import Stock, StockHistorico

class StockListSerializer(serializers.ModelSerializer):
    """Serializer para listado de stock (campos básicos)"""
    class Meta:
        model = Stock
        fields = [
            'bastidor', 'marca', 'modelo', 'matricula', 'anio_matricula',
            'precio_venta', 'dias_stock', 'publicado', 'reservado',
            'provincia', 'nom_concesionario', 'color', 'kilometros',
            'fecha_insert'
        ]

class StockDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalle de stock (todos los campos)"""
    class Meta:
        model = Stock
        fields = '__all__'
        read_only_fields = ['fecha_insert', 'fecha_actualizacion', 'bastidor']

class StockHistoricoSerializer(serializers.ModelSerializer):
    """Serializer para histórico de stock"""
    class Meta:
        model = StockHistorico
        fields = '__all__'
        read_only_fields = ['fecha_insert', 'fecha_actualizacion']
```

**Estimado:** 30 minutos

### Tarea 1.2: Crear ViewSet de Stock

**Archivo:** `/workspace/backend/apps/stock/views.py` (NUEVO)

```python
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Stock, StockHistorico
from .serializers import StockListSerializer, StockDetailSerializer, StockHistoricoSerializer

class StockViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar stock"""
    queryset = Stock.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['marca', 'modelo', 'provincia', 'publicado', 'reservado']
    search_fields = ['marca', 'modelo', 'matricula', 'bastidor', 'nom_concesionario']
    ordering_fields = ['precio_venta', 'dias_stock', 'fecha_insert']
    ordering = ['-fecha_insert']
    pagination_class = None  # Agregar paginación después

    def get_serializer_class(self):
        if self.action == 'list':
            return StockListSerializer
        return StockDetailSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Estadísticas de stock"""
        total = self.get_queryset().count()
        publicados = self.get_queryset().filter(publicado=True).count()
        reservados = self.get_queryset().filter(reservado=True).count()
        precio_promedio = self.get_queryset().aggregate(
            models.Avg('precio_venta')
        )['precio_venta__avg']

        return Response({
            'total_vehiculos': total,
            'publicados': publicados,
            'reservados': reservados,
            'precio_promedio': precio_promedio
        })

class StockHistoricoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consultar histórico de stock"""
    queryset = StockHistorico.objects.all()
    serializer_class = StockHistoricoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['bastidor', 'fecha_snapshot']
    ordering = ['-fecha_insert']
```

**Estimado:** 45 minutos

### Tarea 1.3: Registrar URLs

**Archivo:** `/workspace/backend/apps/stock/urls.py` (NUEVO)

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockViewSet, StockHistoricoViewSet

router = DefaultRouter()
router.register(r'', StockViewSet, basename='stock')
router.register(r'historico', StockHistoricoViewSet, basename='stock-historico')

urlpatterns = [
    path('', include(router.urls)),
]
```

**Estimado:** 15 minutos

### Tarea 1.4: Incluir en URLs principales

**Archivo:** `/workspace/backend/dealaai/urls.py`

Agregar:

```python
path("api/stock/", include("apps.stock.urls")),
```

**Estimado:** 5 minutos

### Tarea 1.5: Probar en Swagger

```bash
cd /workspace/backend
docker-compose up -d
python manage.py runserver
# Acceder a: http://localhost:8000/api/docs/
```

**Estimado:** 15 minutos

**Total Fase 1:** ~2 horas

---

## Fase 2: Frontend Autenticación (Día 2-3)

### Tarea 2.1: Crear Store de Autenticación

**Archivo:** `/workspace/frontend/store/authStore.ts` (NUEVO)

```typescript
import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface AuthUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile?: {
    id: number;
    codigo: string;
    nombre: string;
  };
}

interface AuthStore {
  user: AuthUser | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: AuthUser) => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (username, password) => {
        const response = await fetch("/api/auth/login/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });

        if (!response.ok) throw new Error("Login fallido");

        const data = await response.json();
        set({
          token: data.token,
          user: data.user,
          isAuthenticated: true,
        });
      },

      logout: () => {
        set({
          token: null,
          user: null,
          isAuthenticated: false,
        });
      },

      setUser: (user) => set({ user }),
    }),
    {
      name: "auth-storage",
    }
  )
);
```

**Estimado:** 30 minutos

### Tarea 2.2: Crear Página de Login

**Archivo:** `/workspace/frontend/app/login/page.tsx` (NUEVO)

```typescript
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/authStore";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const login = useAuthStore((state) => state.login);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await login(username, password);
      router.push("/dashboard");
    } catch (err) {
      setError("Usuario o contraseña incorrectos");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow-md p-8">
        <h1 className="text-3xl font-bold mb-6 text-center">DealaAI</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Usuario</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          {error && <div className="text-red-600 text-sm">{error}</div>}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Cargando..." : "Iniciar Sesión"}
          </button>
        </form>

        <p className="text-center text-sm mt-4">
          ¿No tienes cuenta?{" "}
          <a href="/register" className="text-blue-600 hover:underline">
            Regístrate aquí
          </a>
        </p>
      </div>
    </div>
  );
}
```

**Estimado:** 45 minutos

### Tarea 2.3: Crear Middleware de Rutas Protegidas

**Archivo:** `/workspace/frontend/middleware.ts` (NUEVO)

```typescript
import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth-storage")?.value;

  // Rutas protegidas
  if (
    request.nextUrl.pathname.startsWith("/dashboard") ||
    request.nextUrl.pathname.startsWith("/stock") ||
    request.nextUrl.pathname.startsWith("/leads")
  ) {
    if (!token) {
      return NextResponse.redirect(new URL("/login", request.url));
    }
  }

  // Redirigir login a dashboard si ya está autenticado
  if (request.nextUrl.pathname === "/login" && token) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/stock/:path*", "/leads/:path*", "/login"],
};
```

**Estimado:** 30 minutos

### Tarea 2.4: Crear Cliente API Helper

**Archivo:** `/workspace/frontend/lib/api.ts` (NUEVO)

```typescript
import { useAuthStore } from "@/store/authStore";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const token = useAuthStore.getState().token;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options?.headers,
  };

  if (token) {
    headers["Authorization"] = `Token ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}
```

**Estimado:** 20 minutos

**Total Fase 2:** ~2.5 horas

---

## Fase 3: Frontend Layout y Dashboard (Día 4)

### Tarea 3.1: Crear Layout Principal

**Archivo:** `/workspace/frontend/app/layout.tsx` (MODIFICAR)

### Tarea 3.2: Crear Sidebar

**Archivo:** `/workspace/frontend/components/Sidebar.tsx` (NUEVO)

### Tarea 3.3: Crear Topbar

**Archivo:** `/workspace/frontend/components/Topbar.tsx` (NUEVO)

### Tarea 3.4: Crear Dashboard Inicial

**Archivo:** `/workspace/frontend/app/dashboard/page.tsx` (NUEVO)

**Total Fase 3:** ~3 horas

---

## Fase 4: Stock Listing (Día 5-6)

### Tarea 4.1: Página de Listado

**Archivo:** `/workspace/frontend/app/stock/page.tsx`

- Tabla con vehículos
- Paginación
- Búsqueda
- Filtros

### Tarea 4.2: Detalle de Vehículo

**Archivo:** `/workspace/frontend/app/stock/[id]/page.tsx`

**Total Fase 4:** ~4 horas

---

## 📊 RESUMEN CRONOGRAMA

```
Día 1 (Hoy):
  ✅ Backend Stock API (2h)
  ✅ Probar en Swagger (30m)

Día 2:
  ✅ Frontend Auth Store (30m)
  ✅ Frontend Login Page (45m)
  ✅ Frontend Middleware (30m)
  ✅ API Helper (20m)

Día 3:
  ✅ Frontend Layout
  ✅ Sidebar y Topbar
  ✅ Dashboard inicial

Día 4-5:
  ✅ Stock Listing
  ✅ Stock Detail

Semana 2:
  ✅ Leads CRM
  ✅ Chat IA (básico)
  ✅ Reportes

Semana 3:
  ✅ Polish y optimizaciones
  ✅ Testing
  ✅ Deploy MVP
```

---

## 🔧 COMANDOS ÚTILES

```bash
# Frontend
cd /workspace/frontend
npm install  # Instalar dependencias
npm run dev  # Dev server en :3000

# Backend
cd /workspace/backend
python manage.py migrate  # Migraciones
python manage.py runserver  # Dev server en :8000

# Docker
docker-compose up -d  # Iniciar todos servicios
docker-compose logs -f backend  # Ver logs
docker-compose exec backend python manage.py shell  # Shell Django

# Swagger
# http://localhost:8000/api/docs/
```

---

## ✅ CHECKLIST DE COMPLETACIÓN

- [ ] API de Stock creada
- [ ] Endpoints probados en Swagger
- [ ] Store de autenticación creado
- [ ] Página de login funcional
- [ ] Middleware de rutas protegidas
- [ ] Layout base del app
- [ ] Sidebar y topbar
- [ ] Dashboard inicial
- [ ] Listado de stock
- [ ] Detalle de vehículo
- [ ] Búsqueda y filtros
- [ ] MVP Completo

---

**Creado:** 26 de Octubre, 2025  
**Versión:** 1.0  
**Estado:** PLAN DETALLADO
