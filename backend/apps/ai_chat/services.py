"""
Servicio para consultar el stock y generar contexto para la IA
"""
from django.db.models import Count, Avg, Sum, Q
from apps.stock.models import Stock
from typing import Dict, List, Any
import json


class StockQueryService:
    """
    Servicio que maneja las consultas al stock y genera
    información contextual para la IA.
    """

    @staticmethod
    def get_stock_summary() -> Dict[str, Any]:
        """
        Obtiene un resumen general del stock
        """
        total_vehicles = Stock.objects.count()
        available = Stock.objects.filter(reservado=False).count()
        reserved = Stock.objects.filter(reservado=True).count()
        published = Stock.objects.filter(publicado=True).count()

        avg_price = Stock.objects.aggregate(Avg('precio_venta'))['precio_venta__avg']
        avg_km = Stock.objects.aggregate(Avg('kilometros'))['kilometros__avg']
        avg_days_stock = Stock.objects.aggregate(Avg('dias_stock'))['dias_stock__avg']

        return {
            'total_vehicles': total_vehicles,
            'available': available,
            'reserved': reserved,
            'published': published,
            'avg_price': round(avg_price, 2) if avg_price else 0,
            'avg_kilometers': round(avg_km, 2) if avg_km else 0,
            'avg_days_in_stock': round(avg_days_stock, 2) if avg_days_stock else 0,
        }

    @staticmethod
    def get_brands_summary() -> List[Dict[str, Any]]:
        """
        Obtiene resumen por marca
        """
        brands = Stock.objects.values('marca').annotate(
            total=Count('bastidor'),
            avg_price=Avg('precio_venta'),
            avg_km=Avg('kilometros')
        ).filter(marca__isnull=False).order_by('-total')[:10]

        return [
            {
                'brand': brand['marca'],
                'total': brand['total'],
                'avg_price': round(brand['avg_price'], 2) if brand['avg_price'] else 0,
                'avg_km': round(brand['avg_km'], 2) if brand['avg_km'] else 0,
            }
            for brand in brands
        ]

    @staticmethod
    def get_models_summary(brand: str = None) -> List[Dict[str, Any]]:
        """
        Obtiene resumen por modelo, opcionalmente filtrado por marca
        """
        queryset = Stock.objects.all()
        if brand:
            queryset = queryset.filter(marca__iexact=brand)

        models = queryset.values('marca', 'modelo').annotate(
            total=Count('bastidor'),
            avg_price=Avg('precio_venta'),
            avg_km=Avg('kilometros')
        ).filter(modelo__isnull=False).order_by('-total')[:10]

        return [
            {
                'brand': model['marca'],
                'model': model['modelo'],
                'total': model['total'],
                'avg_price': round(model['avg_price'], 2) if model['avg_price'] else 0,
                'avg_km': round(model['avg_km'], 2) if model['avg_km'] else 0,
            }
            for model in models
        ]

    @staticmethod
    def search_vehicles(query_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Busca vehículos según parámetros específicos
        """
        queryset = Stock.objects.all()

        # Filtrar por marca
        if 'brand' in query_params and query_params['brand']:
            queryset = queryset.filter(marca__icontains=query_params['brand'])

        # Filtrar por modelo
        if 'model' in query_params and query_params['model']:
            queryset = queryset.filter(modelo__icontains=query_params['model'])

        # Filtrar por rango de precio
        if 'min_price' in query_params and query_params['min_price']:
            queryset = queryset.filter(precio_venta__gte=query_params['min_price'])
        if 'max_price' in query_params and query_params['max_price']:
            queryset = queryset.filter(precio_venta__lte=query_params['max_price'])

        # Filtrar por kilómetros
        if 'max_km' in query_params and query_params['max_km']:
            queryset = queryset.filter(kilometros__lte=query_params['max_km'])

        # Filtrar por año
        if 'min_year' in query_params and query_params['min_year']:
            queryset = queryset.filter(anio_matricula__gte=query_params['min_year'])

        # Filtrar por color
        if 'color' in query_params and query_params['color']:
            queryset = queryset.filter(color__icontains=query_params['color'])

        # Filtrar por disponibilidad
        if 'available_only' in query_params and query_params['available_only']:
            queryset = queryset.filter(reservado=False)

        # Limitar resultados
        limit = query_params.get('limit', 10)
        vehicles = queryset.order_by('-fecha_insert')[:limit]

        return [
            {
                'vin': v.bastidor,
                'brand': v.marca,
                'model': v.modelo,
                'year': v.anio_matricula,
                'color': v.color,
                'kilometers': v.kilometros,
                'price': float(v.precio_venta) if v.precio_venta else 0,
                'reserved': v.reservado,
                'published': v.publicado,
                'days_in_stock': v.dias_stock,
                'license_plate': v.matricula,
            }
            for v in vehicles
        ]

    @staticmethod
    def get_price_range_summary() -> List[Dict[str, Any]]:
        """
        Obtiene distribución de vehículos por rango de precio
        """
        ranges = [
            (0, 10000, '0-10k'),
            (10000, 20000, '10k-20k'),
            (20000, 30000, '20k-30k'),
            (30000, 50000, '30k-50k'),
            (50000, 999999, '50k+'),
        ]

        result = []
        for min_price, max_price, label in ranges:
            count = Stock.objects.filter(
                precio_venta__gte=min_price,
                precio_venta__lt=max_price
            ).count()
            if count > 0:
                result.append({
                    'range': label,
                    'count': count,
                })

        return result

    @staticmethod
    def get_context_for_ai() -> str:
        """
        Genera un contexto completo del stock para la IA
        """
        summary = StockQueryService.get_stock_summary()
        brands = StockQueryService.get_brands_summary()
        price_ranges = StockQueryService.get_price_range_summary()

        context = f"""
INFORMACIÓN DEL STOCK ACTUAL:

Resumen General:
- Total de vehículos: {summary['total_vehicles']}
- Disponibles: {summary['available']}
- Reservados: {summary['reserved']}
- Publicados en internet: {summary['published']}
- Precio promedio: {summary['avg_price']:,.2f} €
- Kilómetros promedio: {summary['avg_kilometers']:,.0f} km
- Días promedio en stock: {summary['avg_days_in_stock']:.0f} días

Marcas Principales (Top 10):
"""
        for brand in brands:
            context += f"- {brand['brand']}: {brand['total']} unidades, precio medio {brand['avg_price']:,.2f} €\n"

        context += "\nDistribución por Precio:\n"
        for price_range in price_ranges:
            context += f"- {price_range['range']}: {price_range['count']} vehículos\n"

        context += """
Puedes ayudar al usuario a:
1. Buscar vehículos por marca, modelo, precio, kilómetros, año, color
2. Obtener estadísticas del stock
3. Comparar vehículos
4. Sugerir vehículos según criterios
5. Información sobre disponibilidad y precios
"""
        return context
