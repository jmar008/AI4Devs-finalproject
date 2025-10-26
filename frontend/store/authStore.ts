/**
 * Auth Store (Zustand)
 * Gestiona el estado global de autenticación
 * - Token JWT
 * - Datos del usuario actual
 * - Login/Logout
 */

import { authAPI, clearToken, setToken } from '@/lib/api'
import { create } from 'zustand'

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  nombre_completo?: string
  phone?: string
  avatar?: string
  profile?: number
  profile_info?: {
    id: number
    codigo: string
    nombre: string
  }
  jefe?: number
  jefe_info?: {
    id: number
    username: string
    nombre_completo: string
    profile: number
    profile_info: {
      id: number
      codigo: string
      nombre: string
    }
  }
  concesionario?: number
  concesionario_info?: {
    id: number
    nombre: string
    direccion: string | null
    telefono: string | null
    email: string | null
    provincia: number
    provincia_nombre: string
    activo: boolean
    fecha_creacion: string
    fecha_actualizacion: string
  }
  provincia?: number
  provincia_info?: {
    id: number
    nombre: string
    codigo: string
  }
  chat_ai_activo?: boolean
  movil?: string
  fecha_nacimiento?: string
  fecha_incorporacion?: string
  activo?: boolean
  fecha_baja?: string | null
  is_active?: boolean
  is_staff?: boolean
  date_joined?: string
  last_login?: string | null
  subordinados_count?: number
}

interface AuthState {
  // Estado
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  // Acciones
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
  setUser: (user: User | null) => void
  setError: (error: string | null) => void
  clearError: () => void
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (username: string, password: string) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authAPI.login(username, password)

      if (response.error) {
        set({ error: response.error, isLoading: false })
        throw new Error(response.error)
      }

      const { data } = response as any

      if (data?.token && data?.user) {
        console.log('✅ Login exitoso para:', data.user.username)
        setToken(data.token)

        set({
          token: data.token,
          user: data.user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        })
      } else {
        throw new Error('Respuesta inválida del servidor')
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Error en login'
      set({ error: errorMessage, isLoading: false, isAuthenticated: false })
      throw error
    }
  },

  logout: async () => {
    set({ isLoading: true })
    try {
      await authAPI.logout()
    } catch (error) {
      console.error('Error al hacer logout:', error)
    } finally {
      clearToken()
      set({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      })
    }
  },

  checkAuth: async () => {
    set({ isLoading: true })
    try {
      // Obtener token del localStorage
      const tokenFromStorage = localStorage.getItem('auth_token')
      console.log('🔍 checkAuth: token en storage?', !!tokenFromStorage)

      if (!tokenFromStorage) {
        console.log('❌ checkAuth: sin token')
        set({ isAuthenticated: false, isLoading: false })
        return
      }

      // Verificar si el token sigue siendo válido llamando al endpoint /me
      console.log('📡 checkAuth: llamando a /me')
      const response = await authAPI.me()
      console.log('📡 checkAuth: respuesta de /me:', response)

      if (response.error) {
        console.error('❌ checkAuth error:', response.error)
        clearToken()
        set({
          isAuthenticated: false,
          user: null,
          token: null,
          isLoading: false,
        })
        return
      }

      const { data } = response as any
      const userData = data?.user || data
      console.log('✅ checkAuth: autenticado como', userData?.username)

      set({
        token: tokenFromStorage,
        user: userData,
        isAuthenticated: true,
        isLoading: false,
      })
    } catch (error) {
      console.error('❌ checkAuth exception:', error)
      clearToken()
      set({ isAuthenticated: false, isLoading: false })
    }
  },

  setUser: (user: User | null) => {
    set({ user })
  },

  setError: (error: string | null) => {
    set({ error })
  },

  clearError: () => {
    set({ error: null })
  },
}))

export default useAuthStore
