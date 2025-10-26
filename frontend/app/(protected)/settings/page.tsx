'use client'

import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/store/authStore'
import { ChevronLeft } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function SettingsPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading: authLoading } = useAuthStore()

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [authLoading, isAuthenticated, router])

  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin">
          <div className="h-12 w-12 rounded-full border-4 border-indigo-600 border-t-transparent" />
        </div>
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
          <h1 className="text-3xl font-bold text-gray-900">Configuración</h1>
          <p className="mt-1 text-gray-600">
            Administra la configuración de tu cuenta
          </p>
        </div>
      </div>

      {/* Coming soon */}
      <div className="rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 p-12 text-center">
        <div className="inline-block rounded-lg bg-yellow-100 p-3 text-4xl">
          🚀
        </div>
        <h2 className="mt-4 text-2xl font-bold text-gray-900">
          Configuración próximamente
        </h2>
        <p className="mt-2 text-gray-600">
          La página de configuración estará disponible en breve.
        </p>
        <p className="mt-4 text-sm text-gray-500">
          Por el momento, puedes volver a la página principal.
        </p>
        <Button onClick={() => router.push('/dashboard')} className="mt-6">
          Ir al Dashboard
        </Button>
      </div>
    </div>
  )
}
