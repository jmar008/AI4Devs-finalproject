/**
 * Middleware - Proteger rutas y gestionar autenticación
 * Nota: La autenticación real se valida en el cliente con el token guardado en localStorage
 */

import type { NextRequest } from 'next/server'
import { NextResponse } from 'next/server'

// Rutas públicas que no requieren autenticación
const publicPaths = ['/', '/login', '/register', '/forgot-password', '/health']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Permitir rutas públicas
  if (publicPaths.includes(pathname)) {
    return NextResponse.next()
  }

  // Permitir acceso a rutas protegidas (la validación de token se hace en el cliente)
  // El middleware no puede acceder a localStorage (lado del servidor)
  // Por eso la protección real está en el lado del cliente

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public (public files)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|public).*)',
  ],
}
