'use client'

import useAuthStore from '@/store/authStore'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function HomePage() {
  const router = useRouter()
  const { isAuthenticated, isLoading } = useAuthStore()

  useEffect(() => {
    // Esperar a que termine de cargar el estado de autenticación
    if (!isLoading) {
      if (isAuthenticated) {
        // Si tiene sesión activa, redirigir al dashboard
        router.push('/dashboard')
      } else {
        // Si no tiene sesión, redirigir al login
        router.push('/login')
      }
    }
  }, [isAuthenticated, isLoading, router])

  // Mostrar un loader mientras se verifica la sesión
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="text-center">
        <div className="mb-4 inline-block h-12 w-12 animate-spin rounded-full border-b-2 border-indigo-600"></div>
        <p className="text-gray-600">Cargando...</p>
      </div>
    </div>
  )
}
