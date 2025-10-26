'use client'

import { Button } from '@/components/ui/button'
import chatAPI from '@/lib/chatAPI'
import { useChatStore } from '@/store/chatStore'
import { Loader2, MessageSquare, Minus, Send, Trash2, X } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { toast } from 'react-hot-toast'

export function ChatWidget() {
  const {
    isOpen,
    isMinimized,
    isLoading,
    messages,
    currentConversation,
    openChat,
    closeChat,
    toggleMinimize,
    setLoading,
    addMessage,
    setMessages,
    clearMessages,
    setCurrentConversation,
  } = useChatStore()

  const [inputMessage, setInputMessage] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  // Debug: Log cuando cambia isOpen
  useEffect(() => {
    console.log('🔄 ChatWidget: isOpen changed to', isOpen)
  }, [isOpen])

  // Auto-scroll al último mensaje
  useEffect(() => {
    if (messagesEndRef.current && !isMinimized) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isMinimized])

  // Focus en input cuando se abre
  useEffect(() => {
    if (isOpen && !isMinimized && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen, isMinimized])

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessageText = inputMessage.trim()
    setInputMessage('')
    setLoading(true)

    try {
      const response = await chatAPI.sendMessage({
        message: userMessageText,
        conversation_id: currentConversation?.id,
      })

      if (response.error) {
        toast.error(response.error)
        setInputMessage(userMessageText) // Restaurar mensaje
        return
      }

      if (response.data) {
        // Actualizar conversación actual si es nueva
        if (!currentConversation) {
          setCurrentConversation({
            id: response.data.conversation_id,
            title: userMessageText.slice(0, 50),
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            is_active: true,
          })
        }

        // Añadir mensajes
        addMessage({
          ...response.data.user_message,
          id: response.data.user_message.id,
          role: 'user',
          content: response.data.user_message.content,
          created_at: response.data.user_message.created_at,
        })

        addMessage({
          ...response.data.assistant_message,
          id: response.data.assistant_message.id,
          role: 'assistant',
          content: response.data.assistant_message.content,
          created_at: response.data.assistant_message.created_at,
          tokens_used: response.data.assistant_message.tokens_used,
          model_used: response.data.assistant_message.model_used,
        })
      }
    } catch (error) {
      console.error('Error sending message:', error)
      toast.error('Error al enviar el mensaje')
      setInputMessage(userMessageText)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleClearChat = async () => {
    if (!confirm('¿Estás seguro de que quieres limpiar esta conversación?'))
      return

    clearMessages()
    toast.success('Conversación limpiada')
  }

  // Botón flotante para abrir el chat
  if (!isOpen) {
    console.log('🔵 Renderizando botón flotante')
    return (
      <button
        onClick={() => {
          console.log('🔵 Click en botón flotante')
          openChat()
        }}
        className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-indigo-600 text-white shadow-lg transition-all hover:scale-110 hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-300"
        aria-label="Abrir chat IA"
      >
        <MessageSquare size={24} />
      </button>
    )
  }

  // Widget del chat
  console.log('💬 Renderizando widget completo')
  return (
    <div
      className={`fixed bottom-6 right-6 z-50 flex flex-col bg-white shadow-2xl transition-all duration-300 ${
        isMinimized ? 'h-14 w-80' : 'h-[600px] w-96'
      } rounded-lg border border-gray-200`}
    >
      {/* Header */}
      <div className="flex items-center justify-between rounded-t-lg bg-indigo-600 px-4 py-3 text-white">
        <div className="flex items-center gap-2">
          <MessageSquare size={20} />
          <h3 className="font-semibold">Chat IA - DealaAI</h3>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={handleClearChat}
            className="rounded p-1 hover:bg-indigo-700"
            title="Limpiar conversación"
          >
            <Trash2 size={18} />
          </button>
          <button
            onClick={toggleMinimize}
            className="rounded p-1 hover:bg-indigo-700"
            title={isMinimized ? 'Maximizar' : 'Minimizar'}
          >
            <Minus size={18} />
          </button>
          <button
            onClick={closeChat}
            className="rounded p-1 hover:bg-indigo-700"
            title="Cerrar"
          >
            <X size={18} />
          </button>
        </div>
      </div>

      {/* Contenido (solo visible cuando no está minimizado) */}
      {!isMinimized && (
        <>
          {/* Messages Area */}
          <div className="flex-1 space-y-4 overflow-y-auto p-4">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center text-center text-gray-500">
                <MessageSquare size={48} className="mb-4 text-gray-300" />
                <p className="font-medium">¡Hola! Soy tu asistente IA</p>
                <p className="mt-2 text-sm">
                  Pregúntame sobre el stock de vehículos
                </p>
                <div className="mt-4 space-y-2 text-left text-xs">
                  <p>• ¿Cuántos vehículos tenemos?</p>
                  <p>• Muéstrame los BMW disponibles</p>
                  <p>• ¿Cuál es el precio promedio?</p>
                </div>
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg px-4 py-2 ${
                        message.role === 'user'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <p className="whitespace-pre-wrap text-sm">
                        {message.content}
                      </p>
                      <p className="mt-1 text-xs opacity-70">
                        {new Date(message.created_at).toLocaleTimeString(
                          'es-ES',
                          {
                            hour: '2-digit',
                            minute: '2-digit',
                          }
                        )}
                      </p>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="rounded-lg bg-gray-100 px-4 py-2">
                      <Loader2 className="h-5 w-5 animate-spin text-indigo-600" />
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-4">
            <div className="flex gap-2">
              <input
                ref={inputRef}
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Escribe tu mensaje..."
                disabled={isLoading}
                className="flex-1 rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200 disabled:bg-gray-100"
              />
              <Button
                onClick={handleSendMessage}
                disabled={isLoading || !inputMessage.trim()}
                size="sm"
                className="bg-indigo-600 hover:bg-indigo-700"
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Send size={16} />
                )}
              </Button>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
