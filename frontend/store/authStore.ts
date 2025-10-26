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
  phone?: string
  avatar?: string
  perfil?: {
    id: number
    nombre: string
    descripcion: string
  }
  concesionario?: {
    id: number
    nombre: string
  }
  provincia?: {
    id: number
    nombre: string
  }
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
  isLoading: true,
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

      if (!tokenFromStorage) {
        set({ isAuthenticated: false, isLoading: false })
        return
      }

      // Verificar si el token sigue siendo válido
      const response = await authAPI.me()

      if (response.error) {
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
      set({
        token: tokenFromStorage,
        user: data?.user || data,
        isAuthenticated: true,
        isLoading: false,
      })
    } catch (error) {
      console.error('Error al verificar autenticación:', error)
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
