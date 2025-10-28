'use client'

import { Button } from '@/components/ui/button'
import { stockAPI } from '@/lib/api'
import useAuthStore from '@/store/authStore'
import { BarChart3, Car, TrendingUp, Users } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

const stats = [
  {
    label: 'Total Vehículos',
    value: '1,000+',
    icon: Car,
    color: 'bg-blue-500',
  },
  {
    label: 'Vehículos Disponibles',
    value: '850',
    icon: BarChart3,
    color: 'bg-green-500',
  },
  {
    label: 'Leads Este Mes',
    value: '24',
    icon: Users,
    color: 'bg-purple-500',
  },
  {
    label: 'Crecimiento',
    value: '+12.5%',
    icon: TrendingUp,
    color: 'bg-orange-500',
  },
]

interface DashboardStats {
  total_vehiculos: number
  vehiculos_disponibles: number
  vehiculos_publicados: number
  vehiculos_reservados: number
  precio_promedio: number
  por_provincia: Record<string, number>
  actividad_reciente: Array<{
    tipo: string
    descripcion: string
    fecha: string
    estado: string
  }>
}

interface StockVehicle {
  bastidor: string
  marca: string
  modelo: string
  precio_venta: number
  reservado: boolean
  publicado: boolean
  provincia: string
  fecha_recepcion?: string
  descripcion_estado: string
}

export default function DashboardPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading, checkAuth, user } = useAuthStore()
  const [dashboardData, setDashboardData] = useState<DashboardStats | null>(
    null
  )
  const [dataLoading, setDataLoading] = useState(true)
  const [dataError, setDataError] = useState<string | null>(null)

  // Función para cargar datos del dashboard
  const loadDashboardData = async () => {
    try {
      setDataLoading(true)
      setDataError(null)

      // Obtener todos los vehículos usando el endpoint /api/stock
      const response = await stockAPI.list({ page_size: 1000 }) // Obtener hasta 1000 vehículos

      if (response.error) {
        throw new Error(response.error)
      }

      const data = response.data as any
      const vehicles: StockVehicle[] = data.results || []

      // Calcular estadísticas en el frontend
      const total_vehiculos = vehicles.length
      const vehiculos_disponibles = vehicles.filter((v) => !v.reservado).length
      const vehiculos_publicados = vehicles.filter((v) => v.publicado).length
      const vehiculos_reservados = total_vehiculos - vehiculos_disponibles
      const valor_total_stock = vehicles.reduce(
        (sum, v) => sum + (v.precio_venta || 0),
        0
      )
      const precio_promedio =
        total_vehiculos > 0 ? valor_total_stock / total_vehiculos : 0

      // Calcular vehículos por provincia
      const provinciaCount: Record<string, number> = {}
      vehicles.forEach((vehicle) => {
        const provincia = vehicle.provincia || 'Sin provincia'
        provinciaCount[provincia] = (provinciaCount[provincia] || 0) + 1
      })

      // Obtener top 5 provincias
      const por_provincia = Object.entries(provinciaCount)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 5)
        .reduce(
          (acc, [provincia, count]) => {
            acc[provincia] = count
            return acc
          },
          {} as Record<string, number>
        )

      // Calcular actividad reciente (últimos 10 vehículos por fecha de recepción)
      const actividad_reciente = vehicles
        .filter((v) => v.fecha_recepcion)
        .sort(
          (a, b) =>
            new Date(b.fecha_recepcion!).getTime() -
            new Date(a.fecha_recepcion!).getTime()
        )
        .slice(0, 10)
        .map((vehicle) => ({
          tipo: 'nuevo',
          descripcion: `${vehicle.marca} ${vehicle.modelo}`,
          fecha: vehicle.fecha_recepcion
            ? new Date(vehicle.fecha_recepcion).toLocaleDateString('es-ES')
            : 'Fecha desconocida',
          estado: vehicle.reservado ? 'Reservado' : 'Disponible',
        }))

      const stats: DashboardStats = {
        total_vehiculos,
        vehiculos_disponibles,
        vehiculos_publicados,
        vehiculos_reservados,
        precio_promedio,
        por_provincia,
        actividad_reciente,
      }

      setDashboardData(stats)
    } catch (error) {
      console.error('Error loading dashboard data:', error)
      setDataError('Error al cargar los datos del dashboard')
    } finally {
      setDataLoading(false)
    }
  }

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isLoading, isAuthenticated, router])

  useEffect(() => {
    if (isAuthenticated && !isLoading) {
      loadDashboardData()
    }
  }, [isAuthenticated, isLoading])

  // Crear estadísticas dinámicas basadas en datos reales
  const dynamicStats = dashboardData
    ? [
        {
          label: 'Total Vehículos',
          value: dashboardData.total_vehiculos.toLocaleString(),
          icon: Car,
          color: 'bg-blue-500',
        },
        {
          label: 'Vehículos Disponibles',
          value: dashboardData.vehiculos_disponibles.toLocaleString(),
          icon: BarChart3,
          color: 'bg-green-500',
        },
        {
          label: 'Vehículos Publicados',
          value: dashboardData.vehiculos_publicados.toLocaleString(),
          icon: TrendingUp,
          color: 'bg-purple-500',
        },
        {
          label: 'Vehículos Reservados',
          value: dashboardData.vehiculos_reservados.toLocaleString(),
          icon: Users,
          color: 'bg-orange-500',
        },
      ]
    : stats

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin">
          <div className="h-12 w-12 rounded-full border-4 border-indigo-600 border-t-transparent" />
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          Bienvenido, {user?.first_name || user?.username}! 👋
        </h1>
        <p className="mt-2 text-gray-600">
          Aquí está tu resumen del negocio. Puedes ver el estado de tu
          inventario y leads.
        </p>
      </div>

      {/* Error Message */}
      {dataError && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-700">⚠️ {dataError}</p>
        </div>
      )}

      {/* Loading Indicator */}
      {dataLoading && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin">
            <div className="h-8 w-8 rounded-full border-4 border-indigo-600 border-t-transparent" />
          </div>
          <span className="ml-2 text-gray-600">
            Cargando datos del dashboard...
          </span>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
        {dynamicStats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.label} className="rounded-lg bg-white p-6 shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">
                    {stat.label}
                  </p>
                  <p className="mt-2 text-3xl font-bold text-gray-900">
                    {stat.value}
                  </p>
                </div>
                <div className={`${stat.color} rounded-lg p-3 text-white`}>
                  <Icon size={24} />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Recent Activity */}
        <div className="rounded-lg bg-white p-6 shadow lg:col-span-2">
          <h2 className="mb-4 text-xl font-bold text-gray-900">
            Actividad Reciente
          </h2>
          <div className="space-y-4">
            {dashboardData?.actividad_reciente &&
            dashboardData.actividad_reciente.length > 0 ? (
              dashboardData.actividad_reciente.map((actividad, index) => {
                const getActivityIcon = (tipo: string) => {
                  switch (tipo.toLowerCase()) {
                    case 'nuevo':
                      return '🚗'
                    case 'vendido':
                      return '✅'
                    case 'lead':
                      return '👤'
                    default:
                      return '📝'
                  }
                }

                const getActivityColor = (tipo: string) => {
                  switch (tipo.toLowerCase()) {
                    case 'nuevo':
                      return 'bg-indigo-100 text-indigo-600'
                    case 'vendido':
                      return 'bg-green-100 text-green-600'
                    case 'lead':
                      return 'bg-purple-100 text-purple-600'
                    default:
                      return 'bg-gray-100 text-gray-600'
                  }
                }

                const getStatusColor = (estado: string) => {
                  switch (estado.toLowerCase()) {
                    case 'nuevo':
                      return 'bg-blue-100 text-blue-700'
                    case 'vendido':
                      return 'bg-green-100 text-green-700'
                    case 'lead':
                      return 'bg-purple-100 text-purple-700'
                    default:
                      return 'bg-gray-100 text-gray-700'
                  }
                }

                return (
                  <div
                    key={index}
                    className="flex items-center gap-4 border-b border-gray-200 pb-4 last:border-b-0"
                  >
                    <div
                      className={`flex h-10 w-10 items-center justify-center rounded-full ${getActivityColor(actividad.tipo)}`}
                    >
                      {getActivityIcon(actividad.tipo)}
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">
                        {actividad.descripcion}
                      </p>
                      <p className="text-sm text-gray-600">{actividad.fecha}</p>
                    </div>
                    <span
                      className={`rounded px-2 py-1 text-xs ${getStatusColor(actividad.estado)}`}
                    >
                      {actividad.estado}
                    </span>
                  </div>
                )
              })
            ) : (
              <div className="py-8 text-center text-gray-500">
                {dataLoading
                  ? 'Cargando actividad...'
                  : 'No hay actividad reciente'}
              </div>
            )}
          </div>
          <Button variant="outline" className="mt-4 w-full">
            Ver todo
          </Button>
        </div>

        {/* Quick Actions */}
        <div className="rounded-lg bg-white p-6 shadow">
          <h2 className="mb-4 text-xl font-bold text-gray-900">
            Acciones Rápidas
          </h2>
          <div className="space-y-2">
            <Button
              onClick={() => router.push('/stock')}
              className="w-full justify-start bg-indigo-600 hover:bg-indigo-700"
            >
              <Car size={18} className="mr-2" />
              Ver Stock
            </Button>
            <Button variant="outline" className="w-full justify-start" disabled>
              <Users size={18} className="mr-2" />
              Gestionar Leads (Próx)
            </Button>
            <Button variant="outline" className="w-full justify-start" disabled>
              <BarChart3 size={18} className="mr-2" />
              Reportes (Próx)
            </Button>
          </div>

          {/* Tips Section */}
          <div className="mt-6 rounded-lg border border-blue-200 bg-blue-50 p-4">
            <p className="mb-2 text-sm font-medium text-blue-900">
              💡 Tip del día
            </p>
            <p className="text-xs text-blue-700">
              Actualiza regularmente tu stock de vehículos para mejorar la
              precisión de búsquedas
            </p>
          </div>
        </div>
      </div>

      {/* Footer Info */}
      <div className="rounded-lg border border-indigo-200 bg-gradient-to-r from-indigo-50 to-blue-50 p-6">
        <p className="text-sm text-gray-700">
          <span className="font-semibold">Próximas actualizaciones:</span>{' '}
          Gestión de Leads, Chat con IA, Reportes avanzados y mucho más.
          ¡Estamos trabajando duro para mejorar tu experiencia!
        </p>
      </div>
    </div>
  )
}
