from django.db import models
from django.utils import timezone


class Stock(models.Model):
    """
    Tabla principal de stock con los datos actuales de vehículos.
    Se vacía diariamente a las 01:00 y se rellena con nuevos datos.
    """

    # Identificadores principales
    idv = models.IntegerField(null=True, blank=True, db_index=True)
    fecha_informe = models.IntegerField(null=True, blank=True)
    bastidor = models.CharField(
        max_length=50,
        primary_key=True,
        db_index=True,
        verbose_name="Bastidor (VIN)"
    )
    vehicle_key = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    vehicle_key2 = models.CharField(max_length=100, null=True, blank=True)

    # Datos del concesionario y proveedor
    id_concesionario = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    nom_concesionario = models.CharField(max_length=255, null=True, blank=True)
    id_proveedor = models.CharField(max_length=100, null=True, blank=True)
    nom_proveedor = models.CharField(max_length=255, null=True, blank=True)
    dealer_corto = models.CharField(max_length=100, null=True, blank=True)
    provincia = models.CharField(max_length=100, null=True, blank=True, db_index=True)

    # Datos del vehículo
    matricula = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    fecha_matriculacion = models.DateField(null=True, blank=True)
    fecha_recepcion = models.DateField(null=True, blank=True)
    marca = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    modelo = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    modelo_comercial = models.CharField(max_length=100, null=True, blank=True)
    id_modelo = models.CharField(max_length=100, null=True, blank=True)
    modelo_qbi = models.CharField(max_length=100, null=True, blank=True)
    descripcion_modelo_qbi = models.CharField(max_length=100, null=True, blank=True)
    modelo_bastidor = models.CharField(max_length=100, null=True, blank=True)

    anio_matricula = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    color_secundario = models.CharField(max_length=100, null=True, blank=True)
    cod_color = models.CharField(max_length=50, null=True, blank=True)
    id_color = models.CharField(max_length=100, null=True, blank=True)

    kilometros = models.IntegerField(null=True, blank=True)
    ubicacion = models.CharField(max_length=100, null=True, blank=True)


    # Datos técnicos adicionales para API
    version = models.CharField(max_length=255, null=True, blank=True)
    combustible = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    transmision = models.CharField(max_length=50, null=True, blank=True)
    cilindrada = models.IntegerField(null=True, blank=True)
    potencia = models.IntegerField(null=True, blank=True)
    peso = models.IntegerField(null=True, blank=True)
    puertas = models.IntegerField(null=True, blank=True)
    plazas = models.IntegerField(null=True, blank=True)
    
    # Multimedia
    imagen_principal = models.URLField(null=True, blank=True)
    imagenes = models.JSONField(default=list, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)

    # Datos de tipo de vehículo y estado
    id_tipo_vo = models.CharField(max_length=50, null=True, blank=True)
    descripcion_tipo_vo = models.CharField(max_length=100, null=True, blank=True)
    id_estado = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    descripcion_estado = models.CharField(max_length=100, null=True, blank=True)
    tipo_stock = models.CharField(max_length=50, null=True, blank=True)

    # Datos de stock y reserva
    reservado = models.BooleanField(default=False, db_index=True)
    dias_stock = models.IntegerField(null=True, blank=True)
    intervalo_dias = models.CharField(max_length=50, null=True, blank=True)
    meses_en_stock = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dias_stock_fin_mes = models.IntegerField(null=True, blank=True)
    intervalo_dias_fin_mes = models.CharField(max_length=50, null=True, blank=True)
    intervalo_dias_vo = models.CharField(max_length=50, null=True, blank=True)
    intervalo_dias_vo_new = models.CharField(max_length=50, null=True, blank=True)
    intervalo_km = models.CharField(max_length=50, null=True, blank=True)
    interv_km_id = models.CharField(max_length=100, null=True, blank=True)

    uds_disponibles_stock = models.IntegerField(null=True, blank=True)
    uds_reservadas_stock = models.IntegerField(null=True, blank=True)
    stock_uds = models.IntegerField(null=True, blank=True)

    # Datos de pedido y entrada
    pedido = models.CharField(max_length=100, null=True, blank=True)
    categoria = models.CharField(max_length=100, null=True, blank=True)
    canal_entrada_vo = models.CharField(max_length=100, null=True, blank=True)
    concepto_compra = models.CharField(max_length=100, null=True, blank=True)

    # Datos financieros
    importe_compra = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    importe_rectificativas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    importe_reacon = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    importe_vales = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    importe_costo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    importe_coste_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_anterior = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_nuevo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    diferencia_precios = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock_benef_estimado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Datos de internet
    publicado = models.BooleanField(default=False, db_index=True)
    id_internet = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    link_internet = models.TextField(null=True, blank=True)
    internet_eurotax_compra = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    internet_eurotax_venta = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    internet_anuncios = models.IntegerField(null=True, blank=True)
    internet_precio_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    internet_precio_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_internet = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    internet_fotos = models.IntegerField(null=True, blank=True)
    internet_autorizado = models.BooleanField(default=False)
    status_imaweb = models.CharField(max_length=100, null=True, blank=True)
    status_car_imaweb = models.CharField(max_length=100, null=True, blank=True)

    # Datos de publicación y anuncios
    fecha_primera_publicacion = models.DateField(null=True, blank=True)
    fecha_ultima_publicacion = models.DateField(null=True, blank=True)
    antiguedad_anuncio = models.IntegerField(null=True, blank=True)
    dias_primera_public = models.IntegerField(null=True, blank=True)
    uc_dias = models.IntegerField(null=True, blank=True)
    internet_dias_public = models.IntegerField(null=True, blank=True)
    tmaimg = models.CharField(max_length=100, null=True, blank=True)
    tiene_video = models.BooleanField(default=False)

    # Datos de interacción
    visitas_totales = models.IntegerField(null=True, blank=True)
    llamadas_recibidas = models.IntegerField(null=True, blank=True)
    emails_recibidos = models.IntegerField(null=True, blank=True)
    visitas_cambio = models.IntegerField(null=True, blank=True)
    leads_cambio = models.IntegerField(null=True, blank=True)
    visitas_cambio_dias = models.IntegerField(null=True, blank=True)
    leads_cambio_dias = models.IntegerField(null=True, blank=True)

    # Datos de lead y predicción
    flag_lead = models.BooleanField(default=False, db_index=True)
    stock_leads = models.IntegerField(null=True, blank=True)
    prediction = models.CharField(max_length=100, null=True, blank=True)

    # Datos de venta y unidades
    uds_mes = models.IntegerField(null=True, blank=True)
    uds_3mes = models.IntegerField(null=True, blank=True)
    uds_ano = models.IntegerField(null=True, blank=True)

    # Datos de cambios y QBI
    ultimo_cambio = models.CharField(max_length=100, null=True, blank=True)
    ult_cambio = models.CharField(max_length=100, null=True, blank=True)
    fecha_ultimo_cambio = models.DateField(null=True, blank=True)
    fecha_ultimo_cambio_2 = models.DateField(null=True, blank=True)
    fecha_ult_cambio = models.DateField(null=True, blank=True)
    dias_desde_ult_cambio = models.BigIntegerField(null=True, blank=True)
    bastidor_qbi = models.CharField(max_length=100, null=True, blank=True)

    # Datos de fotos y óptipix
    id_calidad_marca = models.CharField(max_length=36, null=True, blank=True)  # UUID
    fecha_ultima_foto_optipix = models.DateTimeField(null=True, blank=True)
    id_vehiculo_foto_optipix = models.CharField(max_length=36, null=True, blank=True)  # UUID
    dias_desde_foto_optipix = models.IntegerField(null=True, blank=True)
    status_foto = models.CharField(max_length=100, null=True, blank=True)

    # Datos de pospuesto
    id_veces_pospuesto = models.CharField(max_length=36, null=True, blank=True)  # UUID
    veces_pospuesto = models.IntegerField(null=True, blank=True)

    # Otros
    xxx = models.CharField(max_length=100, null=True, blank=True)

    # Metadatos
    fecha_snapshot = models.DateField(null=True, blank=True)
    fecha_insert = models.DateTimeField(auto_now_add=True, db_index=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stock'
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        indexes = [
            models.Index(fields=['bastidor']),
            models.Index(fields=['id_concesionario']),
            models.Index(fields=['marca']),
            models.Index(fields=['modelo']),
            models.Index(fields=['matricula']),
            models.Index(fields=['publicado']),
            models.Index(fields=['reservado']),
            models.Index(fields=['flag_lead']),
            models.Index(fields=['fecha_insert']),
        ]

    def __str__(self):
        return f"{self.bastidor} - {self.marca} {self.modelo}"


class StockHistorico(models.Model):
    """
    Tabla de histórico de stock que recibe diariamente a las 01:00
    todos los datos de la tabla stock antes de ser vaciada.
    """

    # Identificadores principales
    idv = models.IntegerField(null=True, blank=True, db_index=True)
    fecha_informe = models.IntegerField(null=True, blank=True)
    bastidor = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name="Bastidor (VIN)"
    )
    vehicle_key = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    vehicle_key2 = models.CharField(max_length=100, null=True, blank=True)

    # Datos del concesionario y proveedor
    id_concesionario = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    nom_concesionario = models.CharField(max_length=255, null=True, blank=True)
    id_proveedor = models.CharField(max_length=100, null=True, blank=True)
    nom_proveedor = models.CharField(max_length=255, null=True, blank=True)
    dealer_corto = models.CharField(max_length=100, null=True, blank=True)
    provincia = models.CharField(max_length=100, null=True, blank=True, db_index=True)

    # Datos del vehículo
    matricula = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    fecha_matriculacion = models.DateField(null=True, blank=True)
    fecha_recepcion = models.DateField(null=True, blank=True)
    marca = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    modelo = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    modelo_comercial = models.CharField(max_length=100, null=True, blank=True)
    id_modelo = models.CharField(max_length=100, null=True, blank=True)
    modelo_qbi = models.CharField(max_length=100, null=True, blank=True)
    descripcion_modelo_qbi = models.CharField(max_length=100, null=True, blank=True)
    modelo_bastidor = models.CharField(max_length=100, null=True, blank=True)

    anio_matricula = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    color_secundario = models.CharField(max_length=100, null=True, blank=True)
    cod_color = models.CharField(max_length=50, null=True, blank=True)
    id_color = models.CharField(max_length=100, null=True, blank=True)

    kilometros = models.IntegerField(null=True, blank=True)
    ubicacion = models.CharField(max_length=100, null=True, blank=True)

    # Datos de tipo de vehículo y estado
    id_tipo_vo = models.CharField(max_length=50, null=True, blank=True)
    descripcion_tipo_vo = models.CharField(max_length=100, null=True, blank=True)
    id_estado = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    descripcion_estado = models.CharField(max_length=100, null=True, blank=True)
    tipo_stock = models.CharField(max_length=50, null=True, blank=True)

    # Datos de stock y reserva
    reservado = models.BooleanField(default=False, db_index=True)
    dias_stock = models.IntegerField(null=True, blank=True)
    intervalo_dias = models.CharField(max_length=50, null=True, blank=True)
    meses_en_stock = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dias_stock_fin_mes = models.IntegerField(null=True, blank=True)
    intervalo_dias_fin_mes = models.CharField(max_length=50, null=True, blank=True)
    intervalo_dias_vo = models.CharField(max_length=50, null=True, blank=True)
    intervalo_dias_vo_new = models.CharField(max_length=50, null=True, blank=True)
    intervalo_km = models.CharField(max_length=50, null=True, blank=True)
    interv_km_id = models.CharField(max_length=100, null=True, blank=True)

    uds_disponibles_stock = models.IntegerField(null=True, blank=True)
    uds_reservadas_stock = models.IntegerField(null=True, blank=True)
    stock_uds = models.IntegerField(null=True, blank=True)

    # Datos de pedido y entrada
    pedido = models.CharField(max_length=100, null=True, blank=True)
    categoria = models.CharField(max_length=100, null=True, blank=True)
    canal_entrada_vo = models.CharField(max_length=100, null=True, blank=True)
    concepto_compra = models.CharField(max_length=100, null=True, blank=True)

    # Datos financieros
    importe_compra = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    importe_rectificativas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    importe_reacon = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    importe_vales = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    importe_costo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    importe_coste_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_anterior = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_nuevo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    diferencia_precios = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock_benef_estimado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Datos de internet
    publicado = models.BooleanField(default=False, db_index=True)
    id_internet = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    link_internet = models.TextField(null=True, blank=True)
    internet_eurotax_compra = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    internet_eurotax_venta = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    internet_anuncios = models.IntegerField(null=True, blank=True)
    internet_precio_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    internet_precio_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_internet = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    internet_fotos = models.IntegerField(null=True, blank=True)
    internet_autorizado = models.BooleanField(default=False)
    status_imaweb = models.CharField(max_length=100, null=True, blank=True)
    status_car_imaweb = models.CharField(max_length=100, null=True, blank=True)

    # Datos de publicación y anuncios
    fecha_primera_publicacion = models.DateField(null=True, blank=True)
    fecha_ultima_publicacion = models.DateField(null=True, blank=True)
    antiguedad_anuncio = models.IntegerField(null=True, blank=True)
    dias_primera_public = models.IntegerField(null=True, blank=True)
    uc_dias = models.IntegerField(null=True, blank=True)
    internet_dias_public = models.IntegerField(null=True, blank=True)
    tmaimg = models.CharField(max_length=100, null=True, blank=True)
    tiene_video = models.BooleanField(default=False)

    # Datos de interacción
    visitas_totales = models.IntegerField(null=True, blank=True)
    llamadas_recibidas = models.IntegerField(null=True, blank=True)
    emails_recibidos = models.IntegerField(null=True, blank=True)
    visitas_cambio = models.IntegerField(null=True, blank=True)
    leads_cambio = models.IntegerField(null=True, blank=True)
    visitas_cambio_dias = models.IntegerField(null=True, blank=True)
    leads_cambio_dias = models.IntegerField(null=True, blank=True)

    # Datos de lead y predicción
    flag_lead = models.BooleanField(default=False, db_index=True)
    stock_leads = models.IntegerField(null=True, blank=True)
    prediction = models.CharField(max_length=100, null=True, blank=True)

    # Datos de venta y unidades
    uds_mes = models.IntegerField(null=True, blank=True)
    uds_3mes = models.IntegerField(null=True, blank=True)
    uds_ano = models.IntegerField(null=True, blank=True)

    # Datos de cambios y QBI
    ultimo_cambio = models.CharField(max_length=100, null=True, blank=True)
    ult_cambio = models.CharField(max_length=100, null=True, blank=True)
    fecha_ultimo_cambio = models.DateField(null=True, blank=True)
    fecha_ultimo_cambio_2 = models.DateField(null=True, blank=True)
    fecha_ult_cambio = models.DateField(null=True, blank=True)
    dias_desde_ult_cambio = models.BigIntegerField(null=True, blank=True)
    bastidor_qbi = models.CharField(max_length=100, null=True, blank=True)

    # Datos de fotos y óptipix
    id_calidad_marca = models.CharField(max_length=36, null=True, blank=True)  # UUID
    fecha_ultima_foto_optipix = models.DateTimeField(null=True, blank=True)
    id_vehiculo_foto_optipix = models.CharField(max_length=36, null=True, blank=True)  # UUID
    dias_desde_foto_optipix = models.IntegerField(null=True, blank=True)
    status_foto = models.CharField(max_length=100, null=True, blank=True)

    # Datos de pospuesto
    id_veces_pospuesto = models.CharField(max_length=36, null=True, blank=True)  # UUID
    veces_pospuesto = models.IntegerField(null=True, blank=True)

    # Otros
    xxx = models.CharField(max_length=100, null=True, blank=True)

    # Metadatos - La fecha de snapshot original es importante para tracking histórico
    fecha_snapshot = models.DateField(null=True, blank=True, db_index=True)
    fecha_insert = models.DateTimeField(db_index=True, verbose_name="Fecha de inserción en histórico")
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stock_historico'
        verbose_name = 'Stock Histórico'
        verbose_name_plural = 'Stocks Históricos'
        indexes = [
            models.Index(fields=['bastidor']),
            models.Index(fields=['fecha_snapshot']),
            models.Index(fields=['id_concesionario']),
            models.Index(fields=['marca']),
            models.Index(fields=['modelo']),
            models.Index(fields=['matricula']),
            models.Index(fields=['publicado']),
            models.Index(fields=['reservado']),
            models.Index(fields=['flag_lead']),
            models.Index(fields=['fecha_insert']),
        ]

    def __str__(self):
        return f"{self.bastidor} - {self.marca} {self.modelo} (Histórico: {self.fecha_snapshot})"
