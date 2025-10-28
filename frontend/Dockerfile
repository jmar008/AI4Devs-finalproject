# Dockerfile para el frontend Next.js (desarrollo)
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Variables de entorno para desarrollo
# NO incluir /api porque se agrega en las rutas del código
ENV NEXT_PUBLIC_API_URL=http://localhost:8080
ENV NEXT_PUBLIC_ENVIRONMENT=development
ENV NODE_ENV=development

# Exponer puerto
EXPOSE 3000

# Comando para desarrollo (con hot reload)
CMD ["npm", "run", "dev"]
