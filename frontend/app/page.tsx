export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🚗 DealaAI
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Sistema de Gestión Inteligente para Concesionarios con IA
          </p>
          <div className="mt-8">
            <span className="inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              ✅ DevContainer Configurado
            </span>
          </div>
        </div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {/* Frontend */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">⚛️</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold">Frontend</h3>
                <p className="text-sm text-gray-500">Next.js + TypeScript</p>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Puerto:</span>
                <span className="text-sm font-mono">3000</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Estado:</span>
                <span className="text-sm text-green-600">● En línea</span>
              </div>
            </div>
          </div>

          {/* Backend */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🐍</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold">Backend</h3>
                <p className="text-sm text-gray-500">Django REST API</p>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Puerto:</span>
                <span className="text-sm font-mono">8000</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Estado:</span>
                <span className="text-sm text-yellow-600">● Configurando</span>
              </div>
            </div>
          </div>

          {/* Database */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🗄️</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold">Base de Datos</h3>
                <p className="text-sm text-gray-500">PostgreSQL + pgvector</p>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Puerto:</span>
                <span className="text-sm font-mono">5432</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Estado:</span>
                <span className="text-sm text-green-600">● En línea</span>
              </div>
            </div>
          </div>

          {/* Redis */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">📊</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold">Redis</h3>
                <p className="text-sm text-gray-500">Cache + Celery</p>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Puerto:</span>
                <span className="text-sm font-mono">6379</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Estado:</span>
                <span className="text-sm text-green-600">● En línea</span>
              </div>
            </div>
          </div>

          {/* Nginx */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🔀</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold">Nginx</h3>
                <p className="text-sm text-gray-500">Proxy Reverso</p>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Puerto:</span>
                <span className="text-sm font-mono">80</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Estado:</span>
                <span className="text-sm text-green-600">● En línea</span>
              </div>
            </div>
          </div>

          {/* IA Chat */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🤖</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold">Chat IA</h3>
                <p className="text-sm text-gray-500">OpenAI + RAG</p>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Modelo:</span>
                <span className="text-sm font-mono">GPT-4</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Estado:</span>
                <span className="text-sm text-yellow-600">● Pendiente</span>
              </div>
            </div>
          </div>
        </div>

        {/* Next Steps */}
        <div className="bg-white rounded-lg shadow-md p-8 border border-gray-200">
          <h2 className="text-2xl font-bold mb-6">🚀 Próximos Pasos</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4">Desarrollo Backend</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Configurar modelos Django</li>
                <li>• Implementar APIs REST</li>
                <li>• Sistema de autenticación</li>
                <li>• Integración con IA</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Desarrollo Frontend</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Dashboard principal</li>
                <li>• Gestión de inventario</li>
                <li>• CRM de leads</li>
                <li>• Chat con IA</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Documentation Links */}
        <div className="mt-16 text-center">
          <h3 className="text-lg font-semibold mb-4">📚 Documentación</h3>
          <div className="flex flex-wrap justify-center gap-4">
            <a
              href="/README.md"
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              README
            </a>
            <a
              href="/DEVELOPMENT.md"
              className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              Desarrollo
            </a>
            <a
              href="/EASYPANEL_SETUP.md"
              className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              EasyPanel
            </a>
            <a
              href="/QUICKSTART_EASYPANEL.md"
              className="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors"
            >
              Quick Start
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
