'use client'

import { Button } from '@/components/ui/button'
import useAuthStore from '@/store/authStore'
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

const menuItems = [
  {
    label: 'Dashboard',
    href: '/dashboard',
    icon: BarChart3,
  },
  {
    label: 'Stock',
    href: '/dashboard/stock',
    icon: Car,
  },
  {
    label: 'Leads',
    href: '/dashboard/leads',
    icon: Users,
    badge: 'Próx',
  },
  {
    label: 'Chat IA',
    href: '/dashboard/chat',
    icon: MessageSquare,
    badge: 'Próx',
  },
]

export function Sidebar() {
  const pathname = usePathname()
  const router = useRouter()
  const { logout } = useAuthStore()

  const handleLogout = async () => {
    await logout()
    router.push('/login')
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
