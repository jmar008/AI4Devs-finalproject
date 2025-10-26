'use client'

import useAuthStore from '@/store/authStore'
import { useEffect, useRef } from 'react'

export function AuthInitializer() {
  const { checkAuth } = useAuthStore()
  const hasChecked = useRef(false)

  useEffect(() => {
    // Solo verificar una sola vez al iniciar la app
    if (!hasChecked.current) {
      hasChecked.current = true
      console.log('🚀 AuthInitializer: Verificando autenticación inicial')
      checkAuth()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return null
}
