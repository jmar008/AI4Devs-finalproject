import { apiCall } from './api'

export interface SendMessageRequest {
  message: string
  conversation_id?: number
}

export interface SendMessageResponse {
  conversation_id: number
  user_message: {
    id: number
    role: string
    content: string
    created_at: string
  }
  assistant_message: {
    id: number
    role: string
    content: string
    created_at: string
    tokens_used?: number
    model_used?: string
  }
  tokens_used: number
}

export interface Conversation {
  id: number
  title: string
  created_at: string
  updated_at: string
  is_active: boolean
  message_count: number
  last_message?: {
    content: string
    created_at: string
    role: string
  }
}

export interface ConversationDetail {
  id: number
  title: string
  created_at: string
  updated_at: string
  is_active: boolean
  messages: Array<{
    id: number
    role: string
    content: string
    created_at: string
    tokens_used?: number
    model_used?: string
  }>
  message_count: number
}

export interface StockSummary {
  summary: {
    total_vehicles: number
    available: number
    reserved: number
    published: number
    avg_price: number
    avg_kilometers: number
    avg_days_in_stock: number
  }
  top_brands: Array<{
    brand: string
    total: number
    avg_price: number
    avg_km: number
  }>
}

const chatAPI = {
  /**
   * Envía un mensaje al chat
   */
  sendMessage: async (data: SendMessageRequest) => {
    return apiCall<SendMessageResponse>('/chat/send/', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  /**
   * Obtiene todas las conversaciones
   */
  getConversations: async () => {
    return apiCall<Conversation[]>('/chat/conversations/')
  },

  /**
   * Obtiene una conversación específica con sus mensajes
   */
  getConversation: async (id: number) => {
    return apiCall<ConversationDetail>(`/chat/conversation/${id}/`)
  },

  /**
   * Elimina una conversación
   */
  deleteConversation: async (id: number) => {
    return apiCall<void>(`/chat/conversation/${id}/delete/`, {
      method: 'DELETE',
    })
  },

  /**
   * Limpia todas las conversaciones
   */
  clearAll: async () => {
    return apiCall<void>('/chat/clear/', {
      method: 'POST',
    })
  },

  /**
   * Obtiene resumen del stock
   */
  getStockSummary: async () => {
    return apiCall<StockSummary>('/chat/stock-summary/')
  },
}

export default chatAPI
