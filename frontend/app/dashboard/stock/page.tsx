'use client'

import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Input } from '@/components/ui/input'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { stockAPI } from '@/lib/api'
import { useAuthStore } from '@/store/authStore'
import {
  ChevronLeft,
  ChevronRight,
  Download,
  Eye,
  Filter,
  MoreVertical,
  Search,
} from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'

interface Stock {
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
  imagen_principal?: string
}

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

  // Estados de filtro
  const [filterMarca, setFilterMarca] = useState('')
  const [filterCombustible, setFilterCombustible] = useState('')
  const [filterTransmision, setFilterTransmision] = useState('')

  // Cargar datos del stock
  const loadStockData = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await stockAPI.list({
        page: currentPage,
        page_size: ITEMS_PER_PAGE,
        search: searchTerm || undefined,
        marca: filterMarca || undefined,
        combustible: filterCombustible || undefined,
        transmision: filterTransmision || undefined,
      })

      if (response.error) {
        setError(response.error)
        toast.error('Error al cargar los vehículos')
        return
      }

      const data = response.data as PaginatedResponse
      setVehicles(data.results || [])
      setTotalCount(data.count || 0)
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Error desconocido'
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setLoading(false)
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
    filterCombustible,
    filterTransmision,
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
    router.push(`/dashboard/stock/${bastidor}`)
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
              onChange={(e) => setSearchTerm(e.target.value)}
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
          {filterCombustible && (
            <button
              onClick={() => setFilterCombustible('')}
              className="flex items-center gap-2 rounded-full bg-indigo-100 px-3 py-1 text-sm text-indigo-700 hover:bg-indigo-200"
            >
              Combustible: {filterCombustible}
              <span>×</span>
            </button>
          )}
          {filterTransmision && (
            <button
              onClick={() => setFilterTransmision('')}
              className="flex items-center gap-2 rounded-full bg-indigo-100 px-3 py-1 text-sm text-indigo-700 hover:bg-indigo-200"
            >
              Transmisión: {filterTransmision}
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
            <Table>
              <TableHeader>
                <TableRow className="bg-gray-50">
                  <TableHead>Vehículo</TableHead>
                  <TableHead>Año</TableHead>
                  <TableHead>Km</TableHead>
                  <TableHead>Precio</TableHead>
                  <TableHead>Combustible</TableHead>
                  <TableHead>Transmisión</TableHead>
                  <TableHead>Estado</TableHead>
                  <TableHead className="text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {vehicles.map((vehicle) => (
                  <TableRow key={vehicle.bastidor} className="hover:bg-gray-50">
                    <TableCell>
                      <div>
                        <p className="font-medium text-gray-900">
                          {vehicle.marca} {vehicle.modelo}
                        </p>
                        <p className="text-sm text-gray-500">
                          {vehicle.version}
                        </p>
                      </div>
                    </TableCell>
                    <TableCell>{vehicle.año}</TableCell>
                    <TableCell>{formatKm(vehicle.kilometros)}</TableCell>
                    <TableCell>
                      <span className="font-semibold text-gray-900">
                        {formatPrice(vehicle.precio)}
                      </span>
                    </TableCell>
                    <TableCell>
                      <span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800">
                        {vehicle.combustible}
                      </span>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm text-gray-600">
                        {vehicle.transmision}
                      </span>
                    </TableCell>
                    <TableCell>
                      <span
                        className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                          vehicle.estado === 'disponible'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {vehicle.estado}
                      </span>
                    </TableCell>
                    <TableCell className="text-right">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm">
                            <MoreVertical size={16} />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem
                            onClick={() => handleViewDetails(vehicle.bastidor)}
                          >
                            <Eye size={16} className="mr-2" />
                            Ver detalles
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            <Download size={16} className="mr-2" />
                            Descargar ficha
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>

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
