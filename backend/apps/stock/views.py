from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Stock, StockHistorico
from .serializers import StockListSerializer, StockDetailSerializer
import logging

logger = logging.getLogger(__name__)


class StandardResultsSetPagination(PageNumberPagination):
    """Paginación estándar para listas de Stock"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar y ver detalles de vehículos en stock.

    Endpoints:
    - GET /api/stock/ - Listar vehículos con paginación
    - GET /api/stock/{bastidor}/ - Detalles de un vehículo
    - GET /api/stock/search/ - Búsqueda avanzada
    - GET /api/stock/stats/ - Estadísticas del stock
    """

    queryset = Stock.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Campos para búsqueda
    search_fields = ['marca', 'modelo', 'bastidor', 'matricula', 'color', 'version']

    # Campos para ordenamiento
    ordering_fields = ['precio_venta', 'kilometros', 'anio_matricula', 'fecha_informe']
    ordering = ['-fecha_informe']  # Ordenamiento por defecto: más recientes primero

    # Campos para filtrado
    filterset_fields = {
        'marca': ['exact', 'icontains'],
        'modelo': ['exact', 'icontains'],
        'combustible': ['exact'],
        'transmision': ['exact'],
        'tipo_vehiculo': ['exact'],
        'anio_matricula': ['exact', 'gte', 'lte'],
        'precio_venta': ['gte', 'lte'],
        'kilometros': ['gte', 'lte'],
        'provincia': ['exact', 'icontains'],
        'color': ['exact', 'icontains'],
        'reservado': ['exact'],
        'publicado': ['exact'],
        'descripcion_estado': ['exact', 'icontains'],
    }

    def get_serializer_class(self):
        """Usa diferentes serializadores para list y detail"""
        if self.action == 'retrieve':
            return StockDetailSerializer
        return StockListSerializer

    @action(detail=False, methods=['post'])
    def search(self, request):
        """
        Búsqueda avanzada de vehículos

        Body JSON:
        {
            "query": "bmw 2020",
            "min_price": 10000,
            "max_price": 50000,
            "marca": "bmw"
        }
        """
        query = request.data.get('query', '')
        min_price = request.data.get('min_price')
        max_price = request.data.get('max_price')
        marca = request.data.get('marca')

        queryset = self.queryset

        if query:
            queryset = queryset.filter(
                Q(marca__icontains=query) |
                Q(modelo__icontains=query) |
                Q(bastidor__icontains=query) |
                Q(matricula__icontains=query) |
                Q(color__icontains=query)
            )

        if min_price is not None:
            queryset = queryset.filter(precio_venta__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(precio_venta__lte=max_price)

        if marca:
            queryset = queryset.filter(marca__iexact=marca)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = StockListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StockListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Obtener estadísticas del stock

        Devuelve:
        - Total de vehículos
        - Precio promedio
        - Vehículos por marca
        - Vehículos por tipo de combustible
        """
        total = self.queryset.count()
        disponibles = self.queryset.filter(reservado=False).count()
        reservados = self.queryset.filter(reservado=True).count()

        stats = {
            'total': total,
            'disponibles': disponibles,
            'reservados': reservados,
            'precio_promedio': None,
            'precio_minimo': None,
            'precio_maximo': None,
            'por_marca': {},
            'por_combustible': {},
            'por_tipo': {},
            'km_promedio': None,
        }

        # Calcular precios
        from django.db.models import Avg, Min, Max
        precio_stats = self.queryset.aggregate(
            avg_price=Avg('precio_venta'),
            min_price=Min('precio_venta'),
            max_price=Max('precio_venta'),
            avg_km=Avg('kilometros'),
        )

        stats['precio_promedio'] = precio_stats['avg_price']
        stats['precio_minimo'] = precio_stats['min_price']
        stats['precio_maximo'] = precio_stats['max_price']
        stats['km_promedio'] = precio_stats['avg_km']

        # Contar por marca
        marcas = self.queryset.values('marca').annotate(count=Count('id')).order_by('-count')
        stats['por_marca'] = {m['marca']: m['count'] for m in marcas[:10]}

        # Contar por combustible
        combustibles = self.queryset.values('combustible').annotate(count=Count('id'))
        stats['por_combustible'] = {c['combustible']: c['count'] for c in combustibles if c['combustible']}

        # Contar por tipo
        tipos = self.queryset.values('tipo_vehiculo').annotate(count=Count('id'))
        stats['por_tipo'] = {t['tipo_vehiculo']: t['count'] for t in tipos if t['tipo_vehiculo']}

        return Response(stats)

    @action(detail=False, methods=['get'])
    def export(self, request):
        """
        Exportar stock a CSV o Excel

        Query params:
        - format: 'csv' o 'excel' (default: 'csv')
        """
        format_type = request.query_params.get('format', 'csv')

        queryset = self.filter_queryset(self.get_queryset())

        if format_type == 'excel':
            import openpyxl
            from django.http import HttpResponse

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = 'Stock'

            # Headers
            headers = [
                'Bastidor', 'Marca', 'Modelo', 'Año', 'Precio', 'Km',
                'Color', 'Combustible', 'Transmisión', 'Estado'
            ]
            ws.append(headers)

            # Data
            for vehicle in queryset[:5000]:  # Límite para evitar timeout
                ws.append([
                    vehicle.bastidor,
                    vehicle.marca,
                    vehicle.modelo,
                    vehicle.anio_matricula,
                    vehicle.precio_venta,
                    vehicle.kilometros,
                    vehicle.color,
                    vehicle.combustible,
                    vehicle.transmision,
                    vehicle.descripcion_estado,
                ])

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="stock_export.xlsx"'
            wb.save(response)
            return response

        else:  # CSV
            import csv
            from django.http import HttpResponse

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="stock_export.csv"'

            writer = csv.writer(response)
            writer.writerow([
                'Bastidor', 'Marca', 'Modelo', 'Año', 'Precio', 'Km',
                'Color', 'Combustible', 'Transmisión', 'Estado'
            ])

            for vehicle in queryset[:5000]:
                writer.writerow([
                    vehicle.bastidor,
                    vehicle.marca,
                    vehicle.modelo,
                    vehicle.anio_matricula,
                    vehicle.precio_venta,
                    vehicle.kilometros,
                    vehicle.color,
                    vehicle.combustible,
                    vehicle.transmision,
                    vehicle.descripcion_estado,
                ])

            return response


from django.db.models import Count
