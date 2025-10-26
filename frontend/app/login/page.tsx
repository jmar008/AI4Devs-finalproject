'use client'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import useAuthStore from '@/store/authStore'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'

interface LoginFormData {
  username: string
  password: string
}

export default function LoginPage() {
  const router = useRouter()
  const { login, isLoading, error, clearError } = useAuthStore()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>()
  const [showPassword, setShowPassword] = useState(false)

  // Limpiar error cuando el componente se monta
  useEffect(() => {
    clearError()
  }, [clearError])

  const onSubmit = async (data: LoginFormData) => {
    try {
      await login(data.username, data.password)
      toast.success('¡Sesión iniciada correctamente!')

      // Delay para asegurar que el token se guarda en localStorage antes de redirigir
      setTimeout(() => {
        router.push('/dashboard')
      }, 500)
    } catch (err) {
      toast.error(error || 'Error al iniciar sesión')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="mb-2 text-4xl font-bold text-gray-900">DealaAI</h1>
          <p className="text-gray-600">
            Gestor inteligente para concesionarios
          </p>
        </div>

        {/* Login Card */}
        <div className="rounded-lg bg-white p-8 shadow-lg">
          <h2 className="mb-6 text-2xl font-bold text-gray-900">
            Inicia sesión
          </h2>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {/* Username Field */}
            <div>
              <label
                htmlFor="username"
                className="mb-1 block text-sm font-medium text-gray-700"
              >
                Usuario
              </label>
              <Input
                id="username"
                type="text"
                placeholder="nombre_usuario"
                {...register('username', {
                  required: 'El usuario es requerido',
                })}
                disabled={isLoading}
                className="w-full"
              />
              {errors.username && (
                <p className="mt-1 text-sm text-red-500">
                  {errors.username.message}
                </p>
              )}
            </div>

            {/* Password Field */}
            <div>
              <label
                htmlFor="password"
                className="mb-1 block text-sm font-medium text-gray-700"
              >
                Contraseña
              </label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="••••••••"
                  {...register('password', {
                    required: 'La contraseña es requerida',
                    minLength: {
                      value: 6,
                      message: 'La contraseña debe tener al menos 6 caracteres',
                    },
                  })}
                  disabled={isLoading}
                  className="w-full pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-500">
                  {errors.password.message}
                </p>
              )}
            </div>

            {/* Error General */}
            {error && (
              <div className="rounded border border-red-200 bg-red-50 p-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <Button
              type="submit"
              disabled={isLoading}
              className="mt-6 w-full bg-indigo-600 hover:bg-indigo-700"
            >
              {isLoading ? 'Conectando...' : 'Iniciar sesión'}
            </Button>
          </form>

          {/* Info de desarrollo */}
          <div className="mt-6 border-t border-gray-200 pt-6">
            <details className="text-xs text-gray-500">
              <summary className="cursor-pointer hover:text-gray-700">
                📝 Credenciales de prueba
              </summary>
              <div className="mt-3 space-y-1 rounded bg-gray-50 p-3 text-gray-600">
                <p>
                  👤 Usuario:{' '}
                  <code className="rounded bg-gray-200 px-1">admin</code>
                </p>
                <p>
                  🔐 Contraseña:{' '}
                  <code className="rounded bg-gray-200 px-1">admin123</code>
                </p>
                <p className="mt-2 text-xs italic">
                  Puedes crear más usuarios desde el panel de admin
                </p>
              </div>
            </details>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>
            ¿Primera vez aquí?{' '}
            <button
              onClick={() => router.push('/register')}
              className="font-medium text-indigo-600 hover:text-indigo-700"
            >
              Solicita acceso
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}
