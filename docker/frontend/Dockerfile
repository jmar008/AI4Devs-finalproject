# Frontend Next.js - Development
FROM node:18-alpine

# Variables de entorno
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1

# Instalar dependencias del sistema
RUN apk add --no-cache libc6-compat git

# Crear directorio de trabajo
WORKDIR /app

# Copiar package files
COPY package*.json ./
COPY pnpm-lock.yaml* ./
COPY yarn.lock* ./

# Instalar dependencias
RUN npm install

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 3000

# Comando por defecto
CMD ["npm", "run", "dev"]
