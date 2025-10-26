-- Script de inicialización de la base de datos
-- Ejecutado automáticamente al crear el contenedor

-- Habilitar extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Crear esquemas si es necesario
CREATE SCHEMA IF NOT EXISTS public;

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Base de datos DealaAI inicializada correctamente';
    RAISE NOTICE 'Extensiones habilitadas: uuid-ossp, vector, pg_trgm, btree_gin';
END $$;
