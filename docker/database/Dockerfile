# Base de datos PostgreSQL con pgvector
FROM ankane/pgvector:latest

# Variables de entorno por defecto
ENV POSTGRES_DB=dealaai_dev
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Copiar scripts de inicialización
COPY ./init-scripts/ /docker-entrypoint-initdb.d/

# Exponer puerto
EXPOSE 5432
