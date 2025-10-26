from django.contrib import admin
from .models import Stock, StockHistorico


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'bastidor',
        'marca',
        'modelo',
        'matricula',
        'nom_concesionario',
        'provincia',
        'precio_venta',
        'dias_stock',
        'reservado',
        'publicado',
        'fecha_insert'
    )
    list_filter = (
        'marca',
        'modelo',
        'provincia',
        'reservado',
        'publicado',
        'flag_lead',
        'internet_autorizado',
        'fecha_insert',
    )
    search_fields = (
        'bastidor',
        'matricula',
        'nom_concesionario',
        'nom_proveedor',
        'marca',
        'modelo',
        'id_concesionario',
    )
    readonly_fields = (
        'fecha_insert',
        'fecha_actualizacion',
    )

    fieldsets = (
        ('Identificadores', {
            'fields': ('bastidor', 'idv', 'vehicle_key', 'vehicle_key2')
        }),
        ('Concesionario', {
            'fields': ('id_concesionario', 'nom_concesionario', 'dealer_corto', 'provincia')
        }),
        ('Vehículo', {
            'fields': (
                'matricula', 'fecha_matriculacion', 'marca', 'modelo',
                'modelo_comercial', 'anio_matricula', 'color', 'kilometros'
            )
        }),
        ('Estado', {
            'fields': ('id_estado', 'descripcion_estado', 'tipo_stock', 'reservado')
        }),
        ('Stock', {
            'fields': (
                'dias_stock', 'meses_en_stock', 'dias_stock_fin_mes',
                'uds_disponibles_stock', 'uds_reservadas_stock', 'stock_uds'
            )
        }),
        ('Financiero', {
            'fields': (
                'importe_compra', 'importe_costo', 'precio_venta',
                'precio_anterior', 'precio_nuevo', 'stock_benef_estimado'
            )
        }),
        ('Internet', {
            'fields': (
                'publicado', 'id_internet', 'link_internet',
                'precio_internet', 'internet_autorizado'
            )
        }),
        ('Metadatos', {
            'fields': ('fecha_snapshot', 'fecha_insert', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StockHistorico)
class StockHistoricoAdmin(admin.ModelAdmin):
    list_display = (
        'bastidor',
        'marca',
        'modelo',
        'matricula',
        'nom_concesionario',
        'provincia',
        'precio_venta',
        'dias_stock',
        'fecha_snapshot',
        'fecha_insert'
    )
    list_filter = (
        'marca',
        'modelo',
        'provincia',
        'reservado',
        'publicado',
        'flag_lead',
        'fecha_snapshot',
        'fecha_insert',
    )
    search_fields = (
        'bastidor',
        'matricula',
        'nom_concesionario',
        'nom_proveedor',
        'marca',
        'modelo',
    )
    readonly_fields = (
        'fecha_actualizacion',
    )

    fieldsets = (
        ('Identificadores', {
            'fields': ('bastidor', 'idv', 'vehicle_key', 'vehicle_key2')
        }),
        ('Concesionario', {
            'fields': ('id_concesionario', 'nom_concesionario', 'dealer_corto', 'provincia')
        }),
        ('Vehículo', {
            'fields': (
                'matricula', 'fecha_matriculacion', 'marca', 'modelo',
                'modelo_comercial', 'anio_matricula', 'color', 'kilometros'
            )
        }),
        ('Estado', {
            'fields': ('id_estado', 'descripcion_estado', 'tipo_stock', 'reservado')
        }),
        ('Stock', {
            'fields': (
                'dias_stock', 'meses_en_stock', 'dias_stock_fin_mes',
                'uds_disponibles_stock', 'uds_reservadas_stock', 'stock_uds'
            )
        }),
        ('Financiero', {
            'fields': (
                'importe_compra', 'importe_costo', 'precio_venta',
                'precio_anterior', 'precio_nuevo', 'stock_benef_estimado'
            )
        }),
        ('Internet', {
            'fields': (
                'publicado', 'id_internet', 'link_internet',
                'precio_internet', 'internet_autorizado'
            )
        }),
        ('Metadatos', {
            'fields': ('fecha_snapshot', 'fecha_insert', 'fecha_actualizacion'),
        }),
    )
