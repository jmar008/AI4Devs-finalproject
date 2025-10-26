from rest_framework import serializers
from .models import Stock, StockHistorico


class StockListSerializer(serializers.ModelSerializer):
    """Serializer para listar vehículos con todos los campos disponibles"""

    class Meta:
        model = Stock
        fields = [
            # Identificadores
            'bastidor',
            'matricula',
            'vehicle_key',
            'id_internet',
            # Vehículo
            'marca',
            'modelo',
            'anio_matricula',
            'color',
            'color_secundario',
            'tipo_vehiculo',
            'descripcion_tipo_vo',
            # Datos financieros
            'precio_venta',
            'precio_anterior',
            'importe_compra',
            'importe_costo',
            'stock_benef_estimado',
            # Stock
            'kilometros',
            'dias_stock',
            'meses_en_stock',
            'reservado',
            'descripcion_estado',
            'tipo_stock',
            # Concesionario
            'nom_concesionario',
            'provincia',
            'ubicacion',
            # Internet
            'publicado',
            'link_internet',
            'internet_eurotax_venta',
            'internet_anuncios',
            'internet_precio_min',
            # Fechas
            'fecha_matriculacion',
            'fecha_recepcion',
            'fecha_informe',
        ]
        read_only_fields = fields


class StockDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para ver un vehículo individual"""

    class Meta:
        model = Stock
        fields = [
            # Identificadores
            'bastidor',
            'matricula',
            'vehicle_key',
            'id_internet',
            # Vehículo
            'marca',
            'modelo',
            'anio_matricula',
            'color',
            'color_secundario',
            'tipo_vehiculo',
            'descripcion_tipo_vo',
            # Datos financieros
            'precio_venta',
            'precio_anterior',
            'importe_compra',
            'importe_costo',
            'stock_benef_estimado',
            # Stock
            'kilometros',
            'dias_stock',
            'meses_en_stock',
            'reservado',
            'descripcion_estado',
            'tipo_stock',
            # Concesionario
            'nom_concesionario',
            'provincia',
            'ubicacion',
            # Internet
            'publicado',
            'link_internet',
            'internet_eurotax_venta',
            'internet_anuncios',
            'internet_precio_min',
            # Fechas
            'fecha_matriculacion',
            'fecha_recepcion',
            'fecha_informe',
        ]
        read_only_fields = fields


class StockHistoricoSerializer(serializers.ModelSerializer):
    """Serializer para el histórico de vehículos"""

    class Meta:
        model = StockHistorico
        fields = [
            'bastidor',
            'marca',
            'modelo',
            'anio_matricula',
            'precio_venta',
            'kilometros',
            'color',
            'tipo_vehiculo',
            'descripcion_estado',
            'fecha_snapshot',
        ]
        read_only_fields = fields
