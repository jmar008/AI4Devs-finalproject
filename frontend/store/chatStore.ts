import { create } from 'zustand'

export interface ChatMessage {
  id: number
  role: 'user' | 'assistant' | 'system'
  content: string
  created_at: string
  tokens_used?: number
  model_used?: string
}

export interface ChatConversation {
  id: number
  title: string
  created_at: string
  updated_at: string
  is_active: boolean
  messages?: ChatMessage[]
  message_count?: number
}

interface ChatState {
  // Estado del widget
  isOpen: boolean
  isMinimized: boolean
  isLoading: boolean

  // Conversación actual
  currentConversation: ChatConversation | null
  messages: ChatMessage[]

  // Todas las conversaciones
  conversations: ChatConversation[]

  // Acciones
  openChat: () => void
  closeChat: () => void
  toggleMinimize: () => void
  setLoading: (loading: boolean) => void

  // Mensajes
  addMessage: (message: ChatMessage) => void
  setMessages: (messages: ChatMessage[]) => void
  clearMessages: () => void

  // Conversaciones
  setCurrentConversation: (conversation: ChatConversation | null) => void
  setConversations: (conversations: ChatConversation[]) => void
  addConversation: (conversation: ChatConversation) => void
}

export const useChatStore = create<ChatState>((set) => ({
  // Estado inicial
  isOpen: false,
  isMinimized: false,
  isLoading: false,

  currentConversation: null,
  messages: [],
  conversations: [],

  // Acciones del widget
  openChat: () => {
    console.log('📱 ChatStore: openChat called')
    set({ isOpen: true, isMinimized: false })
  },
  closeChat: () => {
    console.log('📱 ChatStore: closeChat called')
    set({ isOpen: false })
  },
  toggleMinimize: () =>
    set((state) => {
      console.log('📱 ChatStore: toggleMinimize called', !state.isMinimized)
      return { isMinimized: !state.isMinimized }
    }),
  setLoading: (loading) => {
    console.log('📱 ChatStore: setLoading', loading)
    set({ isLoading: loading })
  },

  // Acciones de mensajes
  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  setMessages: (messages) => set({ messages }),

  clearMessages: () => set({ messages: [], currentConversation: null }),

  // Acciones de conversaciones
  setCurrentConversation: (conversation) =>
    set({
      currentConversation: conversation,
      messages: conversation?.messages || [],
    }),

  setConversations: (conversations) => set({ conversations }),

  addConversation: (conversation) =>
    set((state) => ({
      conversations: [conversation, ...state.conversations],
    })),
}))
