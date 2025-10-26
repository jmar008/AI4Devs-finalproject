'use client'

import { useEffect, useRef } from 'react'

/**
 * Este guard está deprecado y solo redirige a login
 * El dashboard layout maneja la autenticación directamente
 */
export function DashboardAuthGuard() {
  const hasRun = useRef(false)

  useEffect(() => {
    if (hasRun.current) return
    hasRun.current = true

    // Redirigir a login sin hacer nada
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }, [])

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="animate-spin">
        <div className="h-12 w-12 rounded-full border-4 border-indigo-600 border-t-transparent" />
      </div>
    </div>
  )
}
