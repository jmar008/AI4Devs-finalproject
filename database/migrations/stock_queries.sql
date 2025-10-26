-- Script SQL para gestión manual de Stock y StockHistorico
-- Este archivo contiene queries útiles para administradores de BD

-- ============================================
-- 1. CONSULTAS DE MONITOREO
-- ============================================

-- Ver cantidad total de registros
SELECT
    'Stock' as tabla,
    COUNT(*) as cantidad
FROM stock
UNION ALL
SELECT
    'StockHistorico' as tabla,
    COUNT(*) as cantidad
FROM stock_historico;

-- Ver últimos registros insertados
SELECT
    bastidor,
    marca,
    modelo,
    precio_venta,
    fecha_insert,
    'Stock' as fuente
FROM stock
ORDER BY fecha_insert DESC
LIMIT 10;

-- Ver histórico del último día
SELECT
    bastidor,
    marca,
    modelo,
    precio_venta,
    fecha_snapshot,
    fecha_insert
FROM stock_historico
WHERE fecha_insert > NOW() - INTERVAL '1 day'
ORDER BY fecha_insert DESC
LIMIT 10;

-- ============================================
-- 2. ESTADÍSTICAS DE STOCK
-- ============================================

-- Distribución por marca
SELECT
    marca,
    COUNT(*) as cantidad,
    AVG(precio_venta) as precio_promedio,
    COUNT(CASE WHEN reservado THEN 1 END) as reservados
FROM stock
GROUP BY marca
ORDER BY cantidad DESC;

-- Distribución por provincia
SELECT
    provincia,
    COUNT(*) as cantidad,
    COUNT(CASE WHEN publicado THEN 1 END) as publicados,
    COUNT(CASE WHEN flag_lead THEN 1 END) as con_leads
FROM stock
GROUP BY provincia
ORDER BY cantidad DESC;

-- Vehículos con más de 90 días en stock
SELECT
    bastidor,
    marca,
    modelo,
    dias_stock,
    precio_venta,
    fecha_insert
FROM stock
WHERE dias_stock > 90
ORDER BY dias_stock DESC;

-- ============================================
-- 3. ANÁLISIS FINANCIERO
-- ============================================

-- Análisis de márgenes
SELECT
    COUNT(*) as total_vehiculos,
    SUM(importe_compra) as total_compra,
    SUM(importe_costo) as total_costo,
    SUM(precio_venta) as total_venta,
    SUM(stock_benef_estimado) as beneficio_total,
    AVG(stock_benef_estimado) as beneficio_promedio
FROM stock;

-- Vehículos sin beneficio estimado
SELECT
    bastidor,
    marca,
    modelo,
    importe_compra,
    precio_venta,
    stock_benef_estimado
FROM stock
WHERE stock_benef_estimado <= 0 OR stock_benef_estimado IS NULL
ORDER BY bastidor;

-- ============================================
-- 4. ANÁLISIS INTERNET
-- ============================================

-- Análisis de visitas y leads
SELECT
    bastidor,
    marca,
    modelo,
    visitas_totales,
    llamadas_recibidas,
    emails_recibidos,
    flag_lead,
    CASE
        WHEN visitas_totales > 0 THEN ROUND((llamadas_recibidas + emails_recibidos)::float / visitas_totales * 100, 2)
        ELSE 0
    END as tasa_conversion_pct
FROM stock
WHERE publicado = TRUE
ORDER BY visitas_totales DESC
LIMIT 20;

-- Vehículos no publicados
SELECT
    bastidor,
    marca,
    modelo,
    fecha_insert,
    dias_stock
FROM stock
WHERE publicado = FALSE
ORDER BY fecha_insert DESC;

-- ============================================
-- 5. MANTENIMIENTO DE DATOS
-- ============================================

-- Buscar registros duplicados por bastidor
SELECT
    bastidor,
    COUNT(*) as cantidad
FROM stock
GROUP BY bastidor
HAVING COUNT(*) > 1;

-- Registros con datos incompletos
SELECT
    bastidor,
    marca,
    modelo,
    precio_venta,
    CASE
        WHEN marca IS NULL THEN 'marca'
        WHEN modelo IS NULL THEN 'modelo'
        WHEN precio_venta IS NULL THEN 'precio'
        WHEN kilometros IS NULL THEN 'km'
        ELSE 'completo'
    END as campo_faltante
FROM stock
WHERE marca IS NULL
   OR modelo IS NULL
   OR precio_venta IS NULL
   OR kilometros IS NULL;

-- ============================================
-- 6. LIMPIEZA Y ARCHIVADO
-- ============================================

-- Mover stock antiguo a histórico manualmente (si es necesario)
-- INSERT INTO stock_historico (
--     Select all fields from stock...
-- ) SELECT * FROM stock WHERE fecha_insert < NOW() - INTERVAL '1 day';
-- DELETE FROM stock WHERE fecha_insert < NOW() - INTERVAL '1 day';

-- Limpiar histórico muy antiguo (más de 1 año)
-- DELETE FROM stock_historico
-- WHERE fecha_insert < NOW() - INTERVAL '1 year';

-- ============================================
-- 7. BÚSQUEDAS ESPECÍFICAS
-- ============================================

-- Buscar por marca y modelo
SELECT
    bastidor,
    marca,
    modelo,
    precio_venta,
    dias_stock,
    reservado,
    publicado
FROM stock
WHERE marca ILIKE '%BMW%'
  AND modelo ILIKE '%X%'
ORDER BY precio_venta DESC;

-- Buscar por rango de precio
SELECT
    bastidor,
    marca,
    modelo,
    precio_venta,
    importe_costo,
    stock_benef_estimado
FROM stock
WHERE precio_venta BETWEEN 20000 AND 50000
ORDER BY precio_venta DESC;

-- Buscar por concesionario
SELECT
    bastidor,
    marca,
    modelo,
    nom_concesionario,
    precio_venta,
    dias_stock
FROM stock
WHERE id_concesionario = 'CON001'
ORDER BY fecha_insert DESC;

-- ============================================
-- 8. REPORTES
-- ============================================

-- Reporte diario
SELECT
    DATE(fecha_insert) as fecha,
    'Stock' as tabla,
    COUNT(*) as registros,
    COUNT(CASE WHEN publicado THEN 1 END) as publicados,
    COUNT(CASE WHEN reservado THEN 1 END) as reservados,
    AVG(precio_venta) as precio_promedio,
    SUM(visitas_totales) as visitas_total
FROM stock
GROUP BY DATE(fecha_insert)
ORDER BY fecha DESC;

-- Reporte histórico
SELECT
    DATE(fecha_insert) as fecha,
    COUNT(*) as registros_migrados,
    COUNT(DISTINCT id_concesionario) as concesionarios,
    AVG(dias_stock) as dias_promedio,
    SUM(stock_benef_estimado) as beneficio_total
FROM stock_historico
WHERE fecha_insert > NOW() - INTERVAL '30 days'
GROUP BY DATE(fecha_insert)
ORDER BY fecha DESC;

-- ============================================
-- 9. ÍNDICES ÚTILES
-- ============================================

-- Crear índices adicionales si es necesario
-- CREATE INDEX IF NOT EXISTS idx_stock_marca_modelo ON stock(marca, modelo);
-- CREATE INDEX IF NOT EXISTS idx_stock_provincia ON stock(provincia);
-- CREATE INDEX IF NOT EXISTS idx_stock_precio_rango ON stock(precio_venta);
-- CREATE INDEX IF NOT EXISTS idx_historico_fecha_snapshot ON stock_historico(fecha_snapshot);

-- Ver índices existentes
SELECT
    schemaname,
    tablename,
    indexname
FROM pg_indexes
WHERE tablename IN ('stock', 'stock_historico')
ORDER BY tablename, indexname;

-- ============================================
-- 10. ÚTILES PARA DESARROLLO
-- ============================================

-- Vaciar tabla stock (CUIDADO!)
-- TRUNCATE TABLE stock;

-- Vaciar tabla histórico (CUIDADO!)
-- TRUNCATE TABLE stock_historico;

-- Ver el tamaño de las tablas
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as tamaño
FROM pg_tables
WHERE tablename IN ('stock', 'stock_historico')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Ver estructura de la tabla
-- \d stock
-- \d stock_historico
