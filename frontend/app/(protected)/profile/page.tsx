'use client'

import { Button } from '@/components/ui/button'
import { authAPI } from '@/lib/api'
import { useAuthStore } from '@/store/authStore'
import { ChevronLeft } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'

interface User {
  id?: number
  username?: string
  email?: string
  first_name?: string
  last_name?: string
  avatar?: string
  perfil?: {
    nombre?: string
  }
  is_active?: boolean
  date_joined?: string
}

export default function ProfilePage() {
  const router = useRouter()
  const {
    isAuthenticated,
    isLoading: authLoading,
    user: storeUser,
  } = useAuthStore()

  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [authLoading, isAuthenticated, router])

  useEffect(() => {
    if (isAuthenticated) {
      loadUserProfile()
    }
  }, [isAuthenticated])

  const loadUserProfile = async () => {
    try {
      setLoading(true)
      const result = await authAPI.me()

      if (result.error) {
        throw new Error(result.error)
      }

      setUser(result.data)
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Error desconocido'
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const handleEditProfile = () => {
    // Redirigir a http://localhost:/admin/
    window.location.href = '/admin/'
  }

  const handleChangePassword = () => {
    if (user?.id) {
      // Redirigir a /admin/authentication/user/{id_usuario}/password/
      window.location.href = `/admin/authentication/user/${user.id}/password/`
    }
  }

  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin">
          <div className="h-12 w-12 rounded-full border-4 border-indigo-600 border-t-transparent" />
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin">
          <div className="h-8 w-8 rounded-full border-4 border-indigo-600 border-t-transparent" />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6 text-center">
        <p className="text-red-600">{error}</p>
        <Button onClick={loadUserProfile} className="mt-4">
          Reintentar
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button
          variant="outline"
          size="sm"
          onClick={() => router.push('/dashboard')}
        >
          <ChevronLeft size={16} className="mr-2" />
          Volver
        </Button>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Mi Perfil</h1>
          <p className="mt-1 text-gray-600">Información personal del usuario</p>
        </div>
      </div>

      {/* Profile Card */}
      <div className="max-w-2xl rounded-lg border border-gray-200 bg-white shadow">
        <div className="space-y-6 p-6">
          {/* Header info */}
          <div className="flex items-center gap-6 border-b border-gray-200 pb-6">
            <div className="flex h-20 w-20 items-center justify-center rounded-full bg-indigo-100 text-3xl font-bold text-indigo-600">
              {user?.first_name?.[0]?.toUpperCase() || 'U'}
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {user?.first_name} {user?.last_name}
              </h2>
              <p className="text-gray-600">@{user?.username}</p>
            </div>
          </div>

          {/* User information */}
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <label className="block text-sm font-semibold text-gray-700">
                Email
              </label>
              <p className="mt-1 text-gray-900">{user?.email}</p>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700">
                Usuario
              </label>
              <p className="mt-1 text-gray-900">{user?.username}</p>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700">
                Nombre
              </label>
              <p className="mt-1 text-gray-900">{user?.first_name || '-'}</p>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700">
                Apellido
              </label>
              <p className="mt-1 text-gray-900">{user?.last_name || '-'}</p>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700">
                Perfil
              </label>
              <p className="mt-1 text-gray-900">
                {user?.perfil?.nombre || '-'}
              </p>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700">
                Estado
              </label>
              <p className="mt-1">
                <span
                  className={`inline-block rounded-full px-3 py-1 text-sm font-semibold ${
                    user?.is_active
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  }`}
                >
                  {user?.is_active ? '✓ Activo' : '✗ Inactivo'}
                </span>
              </p>
            </div>
            {user?.date_joined && (
              <div>
                <label className="block text-sm font-semibold text-gray-700">
                  Fecha de registro
                </label>
                <p className="mt-1 text-gray-900">
                  {new Date(user.date_joined).toLocaleDateString('es-ES')}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-3 border-t border-gray-200 bg-gray-50 px-6 py-4">
          <Button
            onClick={handleEditProfile}
            className="bg-indigo-600 text-white hover:bg-indigo-700"
          >
            ✏️ Editar Perfil
          </Button>
          <Button
            onClick={handleChangePassword}
            variant="outline"
            className="text-red-600"
          >
            Cambiar Contraseña
          </Button>
        </div>
      </div>
    </div>
  )
}
