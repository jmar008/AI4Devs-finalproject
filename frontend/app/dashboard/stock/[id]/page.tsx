'use client'

import { Button } from '@/components/ui/button'
import { stockAPI } from '@/lib/api'
import { useAuthStore } from '@/store/authStore'
import { ArrowLeft, Download, Mail, Phone, Share2 } from 'lucide-react'
import { useParams, useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'

interface StockDetail {
  bastidor: string
  marca: string
  modelo: string
  version: string
  año: number
  precio: number
  kilometros: number
  estado: string
  color: string
  transmision: string
  combustible: string
  tipo_vehiculo: string
  potencia: number
  cilindrada: number
  peso: number
  plazas: number
  puertas: number
  imagen_principal?: string
  imagenes?: string[]
  description?: string
  created_at?: string
  updated_at?: string
  [key: string]: any // Para campos adicionales dinámicos
}

export default function StockDetailPage() {
  const router = useRouter()
  const params = useParams()
  const bastidor = params.id as string

  const { isAuthenticated, isLoading: authLoading } = useAuthStore()

  const [vehicle, setVehicle] = useState<StockDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Cargar detalles del vehículo
  useEffect(() => {
    if (!isAuthenticated || !bastidor) return

    const loadVehicleDetail = async () => {
      setLoading(true)
      setError(null)

      try {
        const response = await stockAPI.detail(bastidor)

        if (response.error) {
          setError(response.error)
          toast.error('Error al cargar el vehículo')
          return
        }

        setVehicle(response.data as StockDetail)
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'Error desconocido'
        setError(errorMessage)
        toast.error(errorMessage)
      } finally {
        setLoading(false)
      }
    }

    loadVehicleDetail()
  }, [isAuthenticated, bastidor])

  // Redirigir si no está autenticado
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [authLoading, isAuthenticated, router])

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR',
    }).format(price)
  }

  const formatKm = (km: number) => {
    return new Intl.NumberFormat('es-ES').format(km)
  }

  if (authLoading || loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin">
          <div className="h-12 w-12 rounded-full border-4 border-indigo-600 border-t-transparent" />
        </div>
      </div>
    )
  }

  if (error || !vehicle) {
    return (
      <div className="space-y-4">
        <Button
          variant="outline"
          onClick={() => router.back()}
          className="flex items-center gap-2"
        >
          <ArrowLeft size={18} />
          Volver
        </Button>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-center">
          <p className="text-red-700">{error || 'Vehículo no encontrado'}</p>
          <Button
            onClick={() => router.push('/dashboard/stock')}
            className="mt-4"
          >
            Ir al stock
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <Button
            variant="outline"
            onClick={() => router.back()}
            className="mb-4"
          >
            <ArrowLeft size={18} className="mr-2" />
            Volver
          </Button>
          <h1 className="text-3xl font-bold text-gray-900">
            {vehicle.marca} {vehicle.modelo}
          </h1>
          <p className="mt-1 text-gray-600">{vehicle.version}</p>
        </div>
        <div className="text-right">
          <p className="text-4xl font-bold text-indigo-600">
            {formatPrice(vehicle.precio)}
          </p>
          <p className="mt-1 text-sm text-gray-500">Precio</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Image Section */}
        <div className="lg:col-span-2">
          <div className="overflow-hidden rounded-lg bg-white shadow">
            <div className="flex aspect-video items-center justify-center bg-gray-200">
              {vehicle.imagen_principal ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img
                  src={vehicle.imagen_principal}
                  alt={`${vehicle.marca} ${vehicle.modelo}`}
                  className="h-full w-full object-cover"
                />
              ) : (
                <div className="text-center text-gray-400">
                  <p>No hay imagen disponible</p>
                </div>
              )}
            </div>

            {/* Image Gallery */}
            {vehicle.imagenes && vehicle.imagenes.length > 0 && (
              <div className="grid grid-cols-4 gap-2 border-t border-gray-200 bg-gray-50 p-4">
                {vehicle.imagenes.map((img, idx) => (
                  <div
                    key={idx}
                    className="aspect-square cursor-pointer rounded bg-gray-200 transition-opacity hover:opacity-75"
                  >
                    {/* Gallery thumbnails would go here */}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Specifications */}
          <div className="mt-6 rounded-lg bg-white p-6 shadow">
            <h2 className="mb-4 text-xl font-bold text-gray-900">
              Especificaciones
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">Año</p>
                <p className="text-lg font-semibold text-gray-900">
                  {vehicle.año}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Kilómetros</p>
                <p className="text-lg font-semibold text-gray-900">
                  {formatKm(vehicle.kilometros)} km
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Combustible</p>
                <p className="text-lg font-semibold text-gray-900">
                  {vehicle.combustible}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Transmisión</p>
                <p className="text-lg font-semibold text-gray-900">
                  {vehicle.transmision}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Color</p>
                <p className="text-lg font-semibold text-gray-900">
                  {vehicle.color}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Tipo</p>
                <p className="text-lg font-semibold text-gray-900">
                  {vehicle.tipo_vehiculo}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Potencia</p>
                <p className="text-lg font-semibold text-gray-900">
                  {vehicle.potencia || 'N/A'} CV
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Cilindrada</p>
                <p className="text-lg font-semibold text-gray-900">
                  {vehicle.cilindrada || 'N/A'} cc
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Puertas</p>
                <p className="text-lg font-semibold text-gray-900">
                  {vehicle.puertas || 'N/A'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Plazas</p>
                <p className="text-lg font-semibold text-gray-900">
                  {vehicle.plazas || 'N/A'}
                </p>
              </div>
            </div>
          </div>

          {/* Description */}
          {vehicle.description && (
            <div className="mt-6 rounded-lg bg-white p-6 shadow">
              <h2 className="mb-4 text-xl font-bold text-gray-900">
                Descripción
              </h2>
              <p className="whitespace-pre-line text-gray-700">
                {vehicle.description}
              </p>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          {/* Status Card */}
          <div className="rounded-lg bg-white p-6 shadow">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="font-semibold text-gray-900">Estado</h3>
              <span
                className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ${
                  vehicle.estado === 'disponible'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}
              >
                {vehicle.estado}
              </span>
            </div>
            <p className="text-sm text-gray-600">
              Bastidor:{' '}
              <code className="rounded bg-gray-100 px-2 py-1">
                {vehicle.bastidor}
              </code>
            </p>
          </div>

          {/* Actions */}
          <div className="space-y-2">
            <Button className="w-full bg-indigo-600 hover:bg-indigo-700">
              <Phone size={18} className="mr-2" />
              Contactar
            </Button>
            <Button variant="outline" className="w-full">
              <Mail size={18} className="mr-2" />
              Email
            </Button>
          </div>

          {/* Download Card */}
          <div className="rounded-lg bg-white p-6 shadow">
            <h3 className="mb-3 font-semibold text-gray-900">Descargar</h3>
            <Button variant="outline" className="w-full justify-start text-sm">
              <Download size={16} className="mr-2" />
              Ficha técnica (PDF)
            </Button>
          </div>

          {/* Share Card */}
          <div className="rounded-lg bg-white p-6 shadow">
            <h3 className="mb-3 font-semibold text-gray-900">Compartir</h3>
            <div className="flex gap-2">
              <button className="flex-1 rounded border border-gray-200 p-2 hover:bg-gray-50">
                📘
              </button>
              <button className="flex-1 rounded border border-gray-200 p-2 hover:bg-gray-50">
                𝕏
              </button>
              <button className="flex-1 rounded border border-gray-200 p-2 hover:bg-gray-50">
                <Share2 size={16} />
              </button>
            </div>
          </div>

          {/* Timeline */}
          <div className="rounded-lg bg-white p-6 shadow">
            <h3 className="mb-3 font-semibold text-gray-900">Información</h3>
            <div className="space-y-2 text-sm text-gray-600">
              {vehicle.created_at && (
                <p>
                  Creado:{' '}
                  {new Date(vehicle.created_at).toLocaleDateString('es-ES')}
                </p>
              )}
              {vehicle.updated_at && (
                <p>
                  Actualizado:{' '}
                  {new Date(vehicle.updated_at).toLocaleDateString('es-ES')}
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
