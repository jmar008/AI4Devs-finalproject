'use client'

import { Toaster } from 'react-hot-toast'
import { AuthInitializer } from './auth-initializer'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <>
      <AuthInitializer />
      {children}
      <Toaster position="top-right" />
    </>
  )
}
