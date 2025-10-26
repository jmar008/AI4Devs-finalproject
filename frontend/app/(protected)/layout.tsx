'use client'

import { ChatWidget } from '@/components/ChatWidget'
import { Sidebar } from '@/components/Sidebar'
import { Topbar } from '@/components/Topbar'
import useAuthStore from '@/store/authStore'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

// Lista de rutas que requieren layout protegido
const PROTECTED_ROUTES = [
  '/dashboard',
  '/stock',
  '/profile',
  '/settings',
  '/leads',
  '/chat',
]

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { isAuthenticated, token } = useAuthStore()
  const [mounted, setMounted] = useState(false)
  const [currentPath, setCurrentPath] = useState('')

  useEffect(() => {
    setMounted(true)
    setCurrentPath(window.location.pathname)
  }, [])

  const isProtectedRoute = PROTECTED_ROUTES.some((route) =>
    currentPath.startsWith(route)
  )

  // Si no está montado, no renderizar nada
  if (!mounted) {
    return children
  }

  // Si no es una ruta protegida, renderizar sin layout
  if (!isProtectedRoute) {
    return children
  }

  // Si no hay token, redirigir a login
  if (!token || !isAuthenticated) {
    if (mounted) {
      router.push('/login')
    }
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin">
          <div className="h-12 w-12 rounded-full border-4 border-indigo-600 border-t-transparent" />
        </div>
      </div>
    )
  }

  // Mostrar el layout protegido
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Topbar */}
        <Topbar />

        {/* Content */}
        <main className="flex-1 overflow-auto bg-gray-100">
          <div className="container mx-auto px-4 py-8">{children}</div>
        </main>
      </div>

      {/* Chat Widget flotante */}
      <ChatWidget />
    </div>
  )
}
