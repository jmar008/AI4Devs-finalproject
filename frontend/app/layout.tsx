import { Metadata } from 'next'
import './globals.css'
import { Providers } from './providers'

// Nota: next/font deshabilitado temporalmente para evitar problemas de SSL en Docker
// Se puede reactivar en producción o usando fuentes locales
// const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'DealaAI - Sistema de Gestión para Concesionarios',
  description:
    'Sistema de gestión integral para concesionarios con IA, desarrollado con Next.js, Django y PostgreSQL',
  keywords: 'concesionario, gestión, IA, vehículos, CRM, inventario',
  authors: [{ name: 'Jorge Martín García' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
  openGraph: {
    title: 'DealaAI - Sistema de Gestión para Concesionarios',
    description: 'Sistema de gestión integral para concesionarios con IA',
    type: 'website',
    locale: 'es_ES',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body>
        <Providers>
          <div id="root">{children}</div>
        </Providers>
      </body>
    </html>
  )
}
