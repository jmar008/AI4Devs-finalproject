'use client'

import { Button } from '@/components/ui/button'
import useAuthStore from '@/store/authStore'
import { useChatStore } from '@/store/chatStore'
import {
  BarChart3,
  Car,
  ChevronRight,
  LogOut,
  MessageSquare,
  Users,
} from 'lucide-react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'

interface MenuItem {
  label: string
  href: string
  icon: any
  badge?: string
  isAction?: boolean
}

const menuItems: MenuItem[] = [
  {
    label: 'Dashboard',
    href: '/dashboard',
    icon: BarChart3,
  },
  {
    label: 'Stock',
    href: '/stock',
    icon: Car,
  },
  {
    label: 'Leads',
    href: '/leads',
    icon: Users,
    badge: 'Próx',
  },
  {
    label: 'Chat IA',
    href: '/chat',
    icon: MessageSquare,
    isAction: true, // Nueva propiedad para identificar que es una acción, no una ruta
  },
]

export function Sidebar() {
  const pathname = usePathname()
  const router = useRouter()
  const { logout } = useAuthStore()
  const { openChat } = useChatStore()

  const handleLogout = async () => {
    await logout()
    router.push('/login')
  }

  const handleMenuClick = (item: MenuItem) => {
    if (item.isAction && item.label === 'Chat IA') {
      console.log('🤖 Abriendo chat...')
      openChat()
    }
  }

  return (
    <aside className="w-64 overflow-y-auto bg-white shadow-lg">
      {/* Logo */}
      <div className="border-b border-gray-200 p-6">
        <h1 className="text-2xl font-bold text-indigo-600">DealaAI</h1>
        <p className="mt-1 text-xs text-gray-500">Gestor de Concesionarios</p>
      </div>

      {/* Navigation */}
      <nav className="space-y-2 p-4">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive =
            pathname === item.href || pathname.startsWith(item.href + '/')

          // Si es una acción (como Chat IA), renderizar como botón
          if (item.isAction) {
            return (
              <button
                key={item.label}
                onClick={() => handleMenuClick(item)}
                className={`flex w-full items-center justify-between rounded-lg px-4 py-2 transition-colors ${
                  isActive
                    ? 'border-l-4 border-indigo-600 bg-indigo-50 text-indigo-600'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon size={20} />
                  <span className="font-medium">{item.label}</span>
                </div>
                {item.badge && (
                  <span className="rounded bg-yellow-100 px-2 py-1 text-xs text-yellow-800">
                    {item.badge}
                  </span>
                )}
              </button>
            )
          }

          // Renderizar como Link normal
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center justify-between rounded-lg px-4 py-2 transition-colors ${
                isActive
                  ? 'border-l-4 border-indigo-600 bg-indigo-50 text-indigo-600'
                  : 'text-gray-700 hover:bg-gray-50'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon size={20} />
                <span className="font-medium">{item.label}</span>
              </div>
              {item.badge && (
                <span className="rounded bg-yellow-100 px-2 py-1 text-xs text-yellow-800">
                  {item.badge}
                </span>
              )}
              {isActive && <ChevronRight size={18} />}
            </Link>
          )
        })}
      </nav>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Logout Button */}
      <div className="border-t border-gray-200 p-4">
        <Button
          onClick={handleLogout}
          variant="outline"
          className="w-full justify-start text-red-600 hover:bg-red-50 hover:text-red-700"
        >
          <LogOut size={18} className="mr-2" />
          Cerrar sesión
        </Button>
      </div>
    </aside>
  )
}
