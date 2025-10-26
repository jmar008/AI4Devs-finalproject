/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configuración para desarrollo
  env: {
    CUSTOM_KEY: 'value',
  },

  // Configuración de imágenes
  images: {
    domains: ['localhost', 'mcp.jorgemg.es', 'cdn.dealaai.com'],
    formats: ['image/webp', 'image/avif'],
  },

  // Configuración de rewrites para API en desarrollo
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL + '/api/:path*',
      },
    ]
  },

  // Headers de seguridad
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
    ]
  },

  // Configuración de webpack para optimización
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Análisis de bundle si está habilitado
    if (process.env.ANALYZE === 'true') {
      const withBundleAnalyzer = require('@next/bundle-analyzer')({
        enabled: true,
      })
      return withBundleAnalyzer({})
    }

    return config
  },

  // Configuración de compilación
  compiler: {
    // Remove console logs in production
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // Configuración de output para deployment
  output: 'standalone',

  // Configuración de TypeScript
  typescript: {
    // Ignorar errores de TypeScript durante build en desarrollo
    ignoreBuildErrors: process.env.NODE_ENV === 'development',
  },

  // Configuración de ESLint
  eslint: {
    // Ignorar errores de ESLint durante build en desarrollo
    ignoreDuringBuilds: process.env.NODE_ENV === 'development',
  },
}

module.exports = nextConfig
