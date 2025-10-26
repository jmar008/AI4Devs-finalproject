'use client'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { stockAPI } from '@/lib/api'
import { useAuthStore } from '@/store/authStore'
import { ChevronLeft, ChevronRight, Filter, Search } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'

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

interface StockDetail extends Stock {}

interface PaginatedResponse {
  count: number
  next: string | null
  previous: string | null
  results: Stock[]
}

const ITEMS_PER_PAGE = 10

export default function StockPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading: authLoading } = useAuthStore()

  const [vehicles, setVehicles] = useState<Stock[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [totalCount, setTotalCount] = useState(0)
  const [expandedRow, setExpandedRow] = useState<string | null>(null)
  const [detailsData, setDetailsData] = useState<Record<string, StockDetail>>(
    {}
  )

  // Estados de filtro
  const [filterMarca, setFilterMarca] = useState('')
  const [filterTipo, setFilterTipo] = useState('')
  const [filterPrecioMin, setFilterPrecioMin] = useState('')
  const [filterPrecioMax, setFilterPrecioMax] = useState('')

  // Cargar datos del stock
  const loadStockData = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await stockAPI.list({
        page: currentPage,
        page_size: ITEMS_PER_PAGE,
        marca__icontains: searchTerm || undefined,
        marca: filterMarca || undefined,
        tipo_vehiculo: filterTipo || undefined,
        precio_venta__gte: filterPrecioMin || undefined,
        precio_venta__lte: filterPrecioMax || undefined,
      })

      if ('error' in response && response.error) {
        throw new Error(response.error)
      }

      const data = response.data as any

      // Manejar respuesta paginada o directa
      if (data.results) {
        setVehicles(data.results)
        setTotalCount(data.count || 0)
      } else if (Array.isArray(data)) {
        setVehicles(data)
        setTotalCount(data.length)
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Error desconocido'
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  // Cargar detalles de un vehículo
  const loadStockDetails = async (bastidor: string) => {
    if (detailsData[bastidor]) return

    try {
      const response = await stockAPI.detail(bastidor)

      if ('error' in response && response.error) {
        throw new Error(response.error)
      }

      const data = response.data as StockDetail
      setDetailsData((prev) => ({
        ...prev,
        [bastidor]: data,
      }))
    } catch (err) {
      console.error('Error loading details:', err)
      toast.error('Error al cargar detalles del vehículo')
    }
  }

  // Cargar al montar y cuando cambia la búsqueda o filtros
  useEffect(() => {
    if (isAuthenticated) {
      setCurrentPage(1)
      loadStockData()
    }
  }, [
    isAuthenticated,
    searchTerm,
    filterMarca,
    filterTipo,
    filterPrecioMin,
    filterPrecioMax,
  ])

  // Cargar cuando cambia la página
  useEffect(() => {
    if (isAuthenticated && currentPage > 1) {
      loadStockData()
    }
  }, [currentPage, isAuthenticated])

  // Redirigir si no está autenticado
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [authLoading, isAuthenticated, router])

  const handleViewDetails = (bastidor: string) => {
    router.push(`/stock/${bastidor}`)
  }

  const totalPages = Math.ceil(totalCount / ITEMS_PER_PAGE)

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR',
    }).format(price)
  }

  const formatKm = (km: number) => {
    return new Intl.NumberFormat('es-ES').format(km)
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Stock de Vehículos</h1>
        <p className="mt-1 text-gray-600">
          Total:{' '}
          <span className="font-semibold text-indigo-600">{totalCount}</span>{' '}
          vehículos
        </p>
      </div>

      {/* Search and Filters */}
      <div className="space-y-4 rounded-lg bg-white p-4 shadow">
        <div className="flex gap-4">
          <div className="relative flex-1">
            <Search
              size={18}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            />
            <Input
              placeholder="Buscar por marca, modelo, bastidor..."
              value={searchTerm}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setSearchTerm(e.target.value)
              }
              className="pl-10"
            />
          </div>
          <Button variant="outline" className="flex items-center gap-2">
            <Filter size={18} />
            Más filtros
          </Button>
        </div>

        {/* Filter Tags */}
        <div className="flex flex-wrap gap-2">
          {filterMarca && (
            <button
              onClick={() => setFilterMarca('')}
              className="flex items-center gap-2 rounded-full bg-indigo-100 px-3 py-1 text-sm text-indigo-700 hover:bg-indigo-200"
            >
              Marca: {filterMarca}
              <span>×</span>
            </button>
          )}
          {filterTipo && (
            <button
              onClick={() => setFilterTipo('')}
              className="flex items-center gap-2 rounded-full bg-indigo-100 px-3 py-1 text-sm text-indigo-700 hover:bg-indigo-200"
            >
              Tipo: {filterTipo}
              <span>×</span>
            </button>
          )}
          {filterPrecioMin && (
            <button
              onClick={() => setFilterPrecioMin('')}
              className="flex items-center gap-2 rounded-full bg-indigo-100 px-3 py-1 text-sm text-indigo-700 hover:bg-indigo-200"
            >
              Precio mín: €{filterPrecioMin}
              <span>×</span>
            </button>
          )}
          {filterPrecioMax && (
            <button
              onClick={() => setFilterPrecioMax('')}
              className="flex items-center gap-2 rounded-full bg-indigo-100 px-3 py-1 text-sm text-indigo-700 hover:bg-indigo-200"
            >
              Precio máx: €{filterPrecioMax}
              <span>×</span>
            </button>
          )}
        </div>
      </div>

      {/* Table */}
      <div className="overflow-hidden rounded-lg bg-white shadow">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin">
              <div className="h-8 w-8 rounded-full border-4 border-indigo-600 border-t-transparent" />
            </div>
          </div>
        ) : error ? (
          <div className="p-6 text-center">
            <p className="text-red-600">{error}</p>
            <Button onClick={loadStockData} className="mt-4">
              Reintentar
            </Button>
          </div>
        ) : vehicles.length === 0 ? (
          <div className="p-6 text-center">
            <p className="text-gray-500">No se encontraron vehículos</p>
          </div>
        ) : (
          <>
            <table className="w-full text-xs">
              <thead className="sticky top-0 border-b-2 border-gray-300 bg-gray-100">
                <tr>
                  <th className="px-2 py-2 text-left font-semibold text-gray-700">
                    Fecha
                  </th>
                  <th className="px-2 py-2 text-left font-semibold text-gray-700">
                    Origen
                  </th>
                  <th className="px-2 py-2 text-left font-semibold text-gray-700">
                    Matrícula
                  </th>
                  <th className="px-2 py-2 text-left font-semibold text-gray-700">
                    Marca
                  </th>
                  <th className="px-2 py-2 text-left font-semibold text-gray-700">
                    Modelo
                  </th>
                  <th className="px-2 py-2 text-center font-semibold text-gray-700">
                    Año
                  </th>
                  <th className="px-2 py-2 text-right font-semibold text-gray-700">
                    Km
                  </th>
                  <th className="px-2 py-2 text-left font-semibold text-gray-700">
                    Color
                  </th>
                  <th className="px-2 py-2 text-right font-semibold text-gray-700">
                    Precio Anterior
                  </th>
                  <th className="px-2 py-2 text-right font-semibold text-gray-700">
                    Precio Actual
                  </th>
                  <th className="px-2 py-2 text-right font-semibold text-gray-700">
                    Diferencia
                  </th>
                  <th className="px-2 py-2 text-right font-semibold text-gray-700">
                    Días Stock
                  </th>
                  <th className="px-2 py-2 text-left font-semibold text-gray-700">
                    Tipo
                  </th>
                  <th className="px-2 py-2 text-center font-semibold text-gray-700">
                    Estado
                  </th>
                  <th className="px-2 py-2 text-left font-semibold text-gray-700">
                    Provincia
                  </th>
                  <th className="px-2 py-2 text-center font-semibold text-gray-700">
                    Internet
                  </th>
                  <th className="px-2 py-2 text-center font-semibold text-gray-700"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {vehicles.map((vehicle) => {
                  const priceDiff =
                    (vehicle.precio_venta || 0) - (vehicle.precio_anterior || 0)

                  return (
                    <tr key={vehicle.bastidor} className="hover:bg-gray-50">
                      <td className="whitespace-nowrap px-2 py-1.5 text-gray-600">
                        {new Date().toISOString().split('T')[0]}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-xs text-gray-600">
                        {vehicle.nom_concesionario?.slice(0, 8) || '-'}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 font-mono font-semibold text-gray-900">
                        {vehicle.matricula || '-'}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-gray-900">
                        {vehicle.marca}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-gray-900">
                        {vehicle.modelo}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-center text-gray-900">
                        {vehicle.anio_matricula}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-right text-gray-900">
                        {formatKm(vehicle.kilometros)}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-xs text-gray-900">
                        {vehicle.color}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-right text-gray-900">
                        {vehicle.precio_anterior
                          ? formatPrice(vehicle.precio_anterior)
                          : '-'}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-right font-semibold text-gray-900">
                        {formatPrice(vehicle.precio_venta)}
                      </td>
                      <td
                        className={`whitespace-nowrap px-2 py-1.5 text-right font-semibold ${priceDiff > 0 ? 'text-green-600' : 'text-red-600'}`}
                      >
                        {formatPrice(priceDiff)}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-right text-gray-900">
                        {vehicle.dias_stock || '-'}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5">
                        <span
                          className={`rounded px-2 py-0.5 text-xs font-semibold ${
                            vehicle.tipo_stock === 'PROMOCION'
                              ? 'bg-blue-100 text-blue-800'
                              : vehicle.tipo_stock === 'SPECIAL'
                                ? 'bg-purple-100 text-purple-800'
                                : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {vehicle.tipo_stock?.slice(0, 8) || '-'}
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-center">
                        <span
                          className={`rounded px-2 py-0.5 text-xs font-semibold ${
                            vehicle.reservado
                              ? 'bg-red-100 text-red-800'
                              : 'bg-green-100 text-green-800'
                          }`}
                        >
                          {vehicle.reservado ? '🔒' : '✓'}
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-xs text-gray-900">
                        {vehicle.provincia}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-center">
                        {vehicle.publicado ? (
                          <span className="font-bold text-green-600">✓</span>
                        ) : (
                          <span className="font-bold text-red-600">✗</span>
                        )}
                      </td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-center">
                        <button
                          onClick={() => {
                            if (expandedRow === vehicle.bastidor) {
                              setExpandedRow(null)
                            } else {
                              setExpandedRow(vehicle.bastidor)
                              loadStockDetails(vehicle.bastidor)
                            }
                          }}
                          className="text-sm font-bold text-indigo-600 hover:text-indigo-700"
                          title="Ver detalles completos"
                        >
                          {expandedRow === vehicle.bastidor ? '▼' : '▶'}
                        </button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>

            {/* Filas expandidas con detalles */}
            {vehicles.map(
              (vehicle) =>
                expandedRow === vehicle.bastidor && (
                  <div
                    key={`detail-${vehicle.bastidor}`}
                    className="border-t-2 border-gray-300 bg-gray-50"
                  >
                    <div className="p-4">
                      <DetailsPanel
                        data={detailsData[vehicle.bastidor] || vehicle}
                        loading={!detailsData[vehicle.bastidor]}
                      />
                    </div>
                  </div>
                )
            )}

            {/* Pagination */}
            <div className="flex items-center justify-between border-t border-gray-200 px-6 py-4">
              <div className="text-sm text-gray-600">
                Mostrando {(currentPage - 1) * ITEMS_PER_PAGE + 1} a{' '}
                {Math.min(currentPage * ITEMS_PER_PAGE, totalCount)} de{' '}
                {totalCount}
              </div>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                >
                  <ChevronLeft size={16} className="mr-1" />
                  Anterior
                </Button>
                <div className="flex items-center gap-1">
                  {Array.from({ length: Math.min(5, totalPages) }).map(
                    (_, i) => {
                      const pageNum = i + 1
                      return (
                        <Button
                          key={pageNum}
                          variant={
                            pageNum === currentPage ? 'default' : 'outline'
                          }
                          size="sm"
                          onClick={() => setCurrentPage(pageNum)}
                        >
                          {pageNum}
                        </Button>
                      )
                    }
                  )}
                  {totalPages > 5 && <span className="px-2">...</span>}
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() =>
                    setCurrentPage(Math.min(totalPages, currentPage + 1))
                  }
                  disabled={currentPage === totalPages}
                >
                  Siguiente
                  <ChevronRight size={16} className="ml-1" />
                </Button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

// Componente para mostrar detalles expandidos
function DetailsPanel({
  data,
  loading,
}: {
  data: StockDetail
  loading: boolean
}) {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR',
    }).format(price)
  }

  if (loading) {
    return (
      <div className="p-6 text-center">
        <div className="inline-block animate-spin">
          <div className="h-6 w-6 rounded-full border-2 border-indigo-600 border-t-transparent" />
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Información básica */}
      <div>
        <h4 className="mb-3 text-sm font-bold uppercase text-gray-700">
          Identificación
        </h4>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
          <DetailItem label="Matrícula" value={data.matricula} />
          <DetailItem label="Vehicle Key" value={data.vehicle_key} />
          <DetailItem label="ID Internet" value={data.id_internet} />
          <DetailItem label="Bastidor" value={data.bastidor} />
        </div>
      </div>

      {/* Información de vehículo */}
      <div>
        <h4 className="mb-3 text-sm font-bold uppercase text-gray-700">
          Detalles del Vehículo
        </h4>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
          <DetailItem label="Tipo Vehículo" value={data.descripcion_tipo_vo} />
          <DetailItem label="Color Secundario" value={data.color_secundario} />
          <DetailItem label="Concesionario" value={data.nom_concesionario} />
          <DetailItem label="Ubicación" value={data.ubicacion} />
        </div>
      </div>

      {/* Información financiera */}
      <div>
        <h4 className="mb-3 text-sm font-bold uppercase text-gray-700">
          Información Financiera
        </h4>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
          <DetailItem
            label="Precio Anterior"
            value={
              data.precio_anterior ? formatPrice(data.precio_anterior) : '-'
            }
          />
          <DetailItem
            label="Precio Compra"
            value={data.importe_compra ? formatPrice(data.importe_compra) : '-'}
          />
          <DetailItem
            label="Importe Costo"
            value={data.importe_costo ? formatPrice(data.importe_costo) : '-'}
          />
          <DetailItem
            label="Beneficio Estimado"
            value={
              data.stock_benef_estimado
                ? formatPrice(data.stock_benef_estimado)
                : '-'
            }
            className={
              (data.stock_benef_estimado || 0) > 0
                ? 'text-green-600'
                : 'text-red-600'
            }
          />
        </div>
      </div>

      {/* Información de stock */}
      <div>
        <h4 className="mb-3 text-sm font-bold uppercase text-gray-700">
          Stock & Disponibilidad
        </h4>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
          <DetailItem label="Días en Stock" value={data.dias_stock} />
          <DetailItem label="Meses en Stock" value={data.meses_en_stock} />
          <DetailItem label="Tipo de Stock" value={data.tipo_stock} />
          <DetailItem
            label="Publicado"
            value={data.publicado ? '✓ Sí' : '✗ No'}
            className={data.publicado ? 'text-green-600' : 'text-gray-500'}
          />
        </div>
      </div>

      {/* Información de internet */}
      <div>
        <h4 className="mb-3 text-sm font-bold uppercase text-gray-700">
          Información de Internet
        </h4>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
          <DetailItem
            label="Precio Mínimo"
            value={
              data.internet_precio_min
                ? formatPrice(data.internet_precio_min)
                : '-'
            }
          />
          <DetailItem
            label="Eurotax Venta"
            value={
              data.internet_eurotax_venta
                ? formatPrice(data.internet_eurotax_venta)
                : '-'
            }
          />
          {data.link_internet && (
            <DetailItem
              label="URL Internet"
              value={
                <a
                  href={data.link_internet}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="truncate font-medium text-blue-600 hover:text-blue-700"
                >
                  🌐 Ver publicación
                </a>
              }
            />
          )}
        </div>
      </div>

      {/* Fechas importantes */}
      <div>
        <h4 className="mb-3 text-sm font-bold uppercase text-gray-700">
          Fechas
        </h4>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
          <DetailItem label="Matriculación" value={data.fecha_matriculacion} />
          <DetailItem label="Recepción" value={data.fecha_recepcion} />
          <DetailItem label="Informe" value={data.fecha_informe} />
        </div>
      </div>
    </div>
  )
}

// Componente auxiliar para mostrar items de detalle
function DetailItem({
  label,
  value,
  className = '',
}: {
  label: string
  value: React.ReactNode
  className?: string
}) {
  return (
    <div className="rounded-lg border border-gray-100 bg-white p-3">
      <p className="mb-1 text-xs font-semibold uppercase text-gray-600">
        {label}
      </p>
      <p className={`text-sm font-medium text-gray-900 ${className}`}>
        {value || '-'}
      </p>
    </div>
  )
}
