/**
 * API Client Helper
 * Maneja todas las requests a la API del backend con autenticación
 * Compatible con desarrollo (localhost:8000) y producción (EasyPanel)
 */

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

interface ApiRequestOptions extends RequestInit {
  headers?: Record<string, string>
}

interface ApiResponse<T> {
  data?: T
  error?: string
  detail?: string
  message?: string
}

/**
 * Obtiene el token JWT del almacenamiento local
 */
export const getToken = (): string | null => {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('auth_token')
}

/**
 * Guarda el token JWT en el almacenamiento local
 */
export const setToken = (token: string): void => {
  if (typeof window === 'undefined') return
  localStorage.setItem('auth_token', token)
}

/**
 * Elimina el token JWT
 */
export const clearToken = (): void => {
  if (typeof window === 'undefined') return
  localStorage.removeItem('auth_token')
}

/**
 * Realiza una petición a la API
 * Automáticamente incluye el token JWT en los headers
 */
export const apiCall = async <T = any>(
  endpoint: string,
  options: ApiRequestOptions = {}
): Promise<ApiResponse<T>> => {
  const url = `${API_BASE_URL}${endpoint}`
  const token = getToken()

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (token) {
    headers['Authorization'] = `Token ${token}`
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    })

    // Parsear la respuesta
    let data
    try {
      data = await response.json()
    } catch {
      data = null
    }

    // Si la respuesta no es OK
    if (!response.ok) {
      // Manejo especial de errores 401 (no autorizado)
      if (response.status === 401) {
        clearToken()
        // Trigger de evento para que middleware redirija a login
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new Event('unauthorized'))
        }
      }

      return {
        error:
          data?.detail ||
          data?.error ||
          data?.message ||
          'Error en la solicitud',
      }
    }

    return { data }
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : 'Error de conexión',
    }
  }
}

/**
 * Endpoints de autenticación
 */
export const authAPI = {
  login: (username: string, password: string) =>
    apiCall('/auth/users/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),

  logout: () =>
    apiCall('/auth/users/logout/', {
      method: 'POST',
    }),

  me: () => apiCall('/auth/users/me/'),

  changePassword: (oldPassword: string, newPassword: string) =>
    apiCall('/auth/users/change_password/', {
      method: 'POST',
      body: JSON.stringify({
        old_password: oldPassword,
        new_password: newPassword,
      }),
    }),
}

/**
 * Endpoints de stock/vehículos
 */
export const stockAPI = {
  // Listar vehículos con paginación y filtros
  list: (params?: Record<string, any>) => {
    const queryParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          queryParams.append(key, String(value))
        }
      })
    }
    const query = queryParams.toString()
    return apiCall(`/stock/?${query}`)
  },

  // Obtener detalles de un vehículo
  detail: (bastidor: string) => apiCall(`/stock/${bastidor}/`),

  // Búsqueda de vehículos
  search: (query: string) =>
    apiCall('/stock/search/', {
      method: 'POST',
      body: JSON.stringify({ query }),
    }),

  // Obtener estadísticas
  stats: () => apiCall('/stock/stats/'),

  // Exportar a CSV
  export: (format: 'csv' | 'excel' = 'csv') =>
    apiCall(`/stock/export/?format=${format}`),
}

/**
 * Endpoints de usuarios
 */
export const usersAPI = {
  list: (params?: Record<string, any>) => {
    const queryParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          queryParams.append(key, String(value))
        }
      })
    }
    const query = queryParams.toString()
    return apiCall(`/auth/users/?${query}`)
  },

  detail: (id: number) => apiCall(`/auth/users/${id}/`),

  subordinados: (id: number) => apiCall(`/auth/users/${id}/subordinados/`),

  jerarquia: (id: number) => apiCall(`/auth/users/${id}/jerarquia/`),

  create: (data: any) =>
    apiCall('/auth/users/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: any) =>
    apiCall(`/auth/users/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  delete: (id: number) =>
    apiCall(`/auth/users/${id}/`, {
      method: 'DELETE',
    }),
}

/**
 * Endpoints de provincias
 */
export const provinciasAPI = {
  list: () => apiCall('/auth/provincias/'),
  detail: (id: number) => apiCall(`/auth/provincias/${id}/`),
}

/**
 * Endpoints de concesionarios
 */
export const concesionariosAPI = {
  list: () => apiCall('/auth/concesionarios/'),
  detail: (id: number) => apiCall(`/auth/concesionarios/${id}/`),
}

export default apiCall
