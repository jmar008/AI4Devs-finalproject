'use client'

import { useParams, useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { useAuthStore } from '@/store/authStore'
import { stockAPI } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { ChevronLeft } from 'lucide-react'

interface Stock {
  bastidor: string
  matricula?: string
  vehicle_key?: string
  id_internet?: string
  marca: string
  modelo: string
  anio_matricula: number
  color: string
  color_secundario?: string
  tipo_vehiculo?: string
  descripcion_tipo_vo?: string
  precio_venta: number
  precio_anterior?: number
  importe_compra?: number
  importe_costo?: number
  stock_benef_estimado?: number
  kilometros: number
  dias_stock?: number
  meses_en_stock?: string
  reservado: boolean
  descripcion_estado: string
  tipo_stock?: string
  nom_concesionario?: string
  provincia: string
  ubicacion?: string
  publicado?: boolean
  link_internet?: string
  internet_eurotax_venta?: number
  internet_anuncios?: number
  internet_precio_min?: number
  fecha_matriculacion?: string
  fecha_recepcion?: string
  fecha_informe?: number
}

export default function StockDetailPage() {
  const params = useParams()
  const router = useRouter()
  const { isAuthenticated, isLoading: authLoading } = useAuthStore()

  const [vehicle, setVehicle] = useState<Stock | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const bastidor = params?.id as string

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [authLoading, isAuthenticated, router])

  useEffect(() => {
    if (bastidor && isAuthenticated) {
      loadVehicle()
    }
  }, [bastidor, isAuthenticated])

  const loadVehicle = async () => {
    try {
      setLoading(true)
      const response = await stockAPI.detail(bastidor)

      if ('error' in response && response.error) {
        throw new Error(response.error)
      }

      setVehicle(response.data as Stock)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido')
    } finally {
      setLoading(false)
    }
  }

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR',
    }).format(price)
  }

  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin">
          <div className="h-12 w-12 rounded-full border-4 border-indigo-600 border-t-transparent" />
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin">
          <div className="h-8 w-8 rounded-full border-4 border-indigo-600 border-t-transparent" />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6 text-center">
        <p className="text-red-600">{error}</p>
        <Button onClick={() => router.back()} className="mt-4">
          Volver
        </Button>
      </div>
    )
  }

  if (!vehicle) {
    return (
      <div className="p-6 text-center">
        <p className="text-gray-500">Vehículo no encontrado</p>
        <Button onClick={() => router.push('/stock')} className="mt-4">
          Volver al stock
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button
          variant="outline"
          size="sm"
          onClick={() => router.push('/stock')}
        >
          <ChevronLeft size={16} className="mr-2" />
          Volver al stock
        </Button>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            {vehicle.marca} {vehicle.modelo}
          </h1>
          <p className="mt-1 font-mono text-gray-600">{vehicle.bastidor}</p>
        </div>
      </div>

      {/* Content */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Información básica */}
        <div className="rounded-lg border border-gray-200 bg-white p-6 shadow">
          <h2 className="mb-4 text-lg font-bold text-gray-900">Información Básica</h2>
          <div className="space-y-3">
            <DetailRow label="Matrícula" value={vehicle.matricula} />
            <DetailRow label="Bastidor" value={vehicle.bastidor} />
            <DetailRow label="Año" value={vehicle.anio_matricula} />
            <DetailRow label="Color" value={vehicle.color} />
            <DetailRow label="Tipo" value={vehicle.tipo_vehiculo} />
          </div>
        </div>

        {/* Información de precios */}
        <div className="rounded-lg border border-gray-200 bg-white p-6 shadow">
          <h2 className="mb-4 text-lg font-bold text-gray-900">Precios</h2>
          <div className="space-y-3">
            <DetailRow
              label="Precio Venta"
              value={formatPrice(vehicle.precio_venta)}
              className="text-indigo-600 font-semibold"
            />
            <DetailRow
              label="Precio Anterior"
              value={vehicle.precio_anterior ? formatPrice(vehicle.precio_anterior) : '-'}
            />
            <DetailRow
              label="Precio Compra"
              value={vehicle.importe_compra ? formatPrice(vehicle.importe_compra) : '-'}
            />
            <DetailRow
              label="Beneficio Estimado"
              value={vehicle.stock_benef_estimado ? formatPrice(vehicle.stock_benef_estimado) : '-'}
            />
          </div>
        </div>

        {/* Información de stock */}
        <div className="rounded-lg border border-gray-200 bg-white p-6 shadow">
          <h2 className="mb-4 text-lg font-bold text-gray-900">Stock</h2>
          <div className="space-y-3">
            <DetailRow label="Kilómetros" value={vehicle.kilometros.toLocaleString()} />
            <DetailRow label="Días en Stock" value={vehicle.dias_stock} />
            <DetailRow label="Tipo de Stock" value={vehicle.tipo_stock} />
            <DetailRow
              label="Estado"
              value={vehicle.reservado ? '🔒 Reservado' : '✓ Disponible'}
            />
            <DetailRow
              label="Publicado"
              value={vehicle.publicado ? '✓ Sí' : '✗ No'}
            />
          </div>
        </div>

        {/* Información de ubicación */}
        <div className="rounded-lg border border-gray-200 bg-white p-6 shadow">
          <h2 className="mb-4 text-lg font-bold text-gray-900">Ubicación</h2>
          <div className="space-y-3">
            <DetailRow label="Concesionario" value={vehicle.nom_concesionario} />
            <DetailRow label="Provincia" value={vehicle.provincia} />
            <DetailRow label="Ubicación" value={vehicle.ubicacion} />
          </div>
        </div>

        {/* Información de internet */}
        {vehicle.link_internet && (
          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow">
            <h2 className="mb-4 text-lg font-bold text-gray-900">Internet</h2>
            <div className="space-y-3">
              <DetailRow
                label="Publicado"
                value={
                  <a
                    href={vehicle.link_internet}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-700 hover:underline"
                  >
                    🌐 Ver publicación
                  </a>
                }
              />
              {vehicle.internet_precio_min && (
                <DetailRow
                  label="Precio Mínimo"
                  value={formatPrice(vehicle.internet_precio_min)}
                />
              )}
              {vehicle.internet_eurotax_venta && (
                <DetailRow
                  label="Eurotax Venta"
                  value={formatPrice(vehicle.internet_eurotax_venta)}
                />
              )}
            </div>
          </div>
        )}

        {/* Fechas importantes */}
        <div className="rounded-lg border border-gray-200 bg-white p-6 shadow">
          <h2 className="mb-4 text-lg font-bold text-gray-900">Fechas</h2>
          <div className="space-y-3">
            <DetailRow label="Matriculación" value={vehicle.fecha_matriculacion} />
            <DetailRow label="Recepción" value={vehicle.fecha_recepcion} />
            <DetailRow label="Informe" value={vehicle.fecha_informe} />
          </div>
        </div>
      </div>
    </div>
  )
}

function DetailRow({
  label,
  value,
  className = '',
}: {
  label: string
  value: React.ReactNode
  className?: string
}) {
  return (
    <div className="flex items-center justify-between border-b border-gray-100 pb-2">
      <span className="text-sm font-medium text-gray-600">{label}</span>
      <span className={`text-sm text-gray-900 ${className}`}>{value || '-'}</span>
    </div>
  )
}
