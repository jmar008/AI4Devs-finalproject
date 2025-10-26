'use client'

import { Button } from '@/components/ui/button'
import useAuthStore from '@/store/authStore'
import { BarChart3, Car, TrendingUp, Users } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

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

export default function DashboardPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading, checkAuth, user } = useAuthStore()

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isLoading, isAuthenticated, router])

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

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => {
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
            <div className="flex items-center gap-4 border-b border-gray-200 pb-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-indigo-100 text-indigo-600">
                🚗
              </div>
              <div className="flex-1">
                <p className="font-medium text-gray-900">
                  Nuevo vehículo agregado
                </p>
                <p className="text-sm text-gray-600">
                  BMW Serie 3 - Hace 2 horas
                </p>
              </div>
              <span className="rounded bg-blue-100 px-2 py-1 text-xs text-blue-700">
                Nuevo
              </span>
            </div>
            <div className="flex items-center gap-4 border-b border-gray-200 pb-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-100 text-green-600">
                ✅
              </div>
              <div className="flex-1">
                <p className="font-medium text-gray-900">Vehículo vendido</p>
                <p className="text-sm text-gray-600">Audi A4 - Hace 5 horas</p>
              </div>
              <span className="rounded bg-green-100 px-2 py-1 text-xs text-green-700">
                Vendido
              </span>
            </div>
            <div className="flex items-center gap-4 border-b border-gray-200 pb-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-100 text-purple-600">
                👤
              </div>
              <div className="flex-1">
                <p className="font-medium text-gray-900">Nuevo lead</p>
                <p className="text-sm text-gray-600">
                  Juan García interesado en BMW - Hace 1 día
                </p>
              </div>
              <span className="rounded bg-purple-100 px-2 py-1 text-xs text-purple-700">
                Lead
              </span>
            </div>
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
