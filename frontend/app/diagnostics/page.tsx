'use client'

import { useEffect, useState } from 'react'

export default function DiagnosticsPage() {
  const [info, setInfo] = useState<any>({})

  useEffect(() => {
    const diagnostic = {
      timestamp: new Date().toISOString(),
      userAgent: typeof window !== 'undefined' ? navigator.userAgent : 'N/A',
      apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080',
      isDev: process.env.NODE_ENV === 'development',
      hasLocalStorage: typeof window !== 'undefined' && !!window.localStorage,
      storedToken:
        typeof window !== 'undefined'
          ? localStorage.getItem('auth_token')?.substring(0, 20) + '...'
          : 'N/A',
    }
    setInfo(diagnostic)
  }, [])

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-2xl">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold">System Diagnostics</h1>
          <p className="text-sm text-gray-600">Información del sistema</p>
        </div>

        <div className="rounded-lg bg-white p-8 shadow">
          <pre className="overflow-auto rounded bg-gray-100 p-4 text-sm">
            {JSON.stringify(info, null, 2)}
          </pre>

          <div className="mt-6 space-y-3">
            <h2 className="text-lg font-semibold">Verificaciones</h2>
            <div className="space-y-2">
              <div>
                <p className="text-sm">
                  ✅ API Base URL:{' '}
                  {process.env.NEXT_PUBLIC_API_URL || 'default'}
                </p>
              </div>
              <div>
                <p className="text-sm">
                  ✅ Environment:{' '}
                  {process.env.NODE_ENV === 'development' ? 'DEV' : 'PROD'}
                </p>
              </div>
              <div>
                <p className="text-sm">✅ React Client: OK</p>
              </div>
            </div>
          </div>

          <div className="mt-6 rounded border border-blue-200 bg-blue-50 p-4">
            <p className="text-xs text-blue-800">
              💡 Para testear el login, abre:{' '}
              <a href="/test-inputs" className="font-semibold underline">
                /test-inputs
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
