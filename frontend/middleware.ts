/**
 * Middleware - Proteger rutas y gestionar autenticación
 * Redirige a /login si no está autenticado
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

  // Obtener el token de la cookie o header
  const token = request.cookies.get('auth_token')?.value

  // Si no hay token y la ruta requiere autenticación, redirigir a login
  if (!token && !publicPaths.includes(pathname)) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('from', pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Permitir acceso a la ruta
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
