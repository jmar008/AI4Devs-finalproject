# Configuración de URLs del Backend para diferentes entornos

## 🚀 Configuración por Entorno

### Desarrollo Local (Docker Compose)

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_WS_URL=ws://localhost:8080/ws
```

### Desarrollo con Backend Directo

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

### Servidor de Desarrollo/Testing

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://192.168.1.100:8080
NEXT_PUBLIC_WS_URL=ws://192.168.1.100:8080/ws
```

_Reemplaza `192.168.1.100` con la IP de tu servidor_

### Producción

```bash
# .env.local.production
NEXT_PUBLIC_API_URL=https://tu-dominio.com
NEXT_PUBLIC_WS_URL=wss://tu-dominio.com/ws
```

_Reemplaza `tu-dominio.com` con tu dominio real_

## 🔧 Cómo Cambiar la Configuración

### Opción 1: Variables de Entorno

1. Copia `.env.example` a `.env.local`
2. Modifica `NEXT_PUBLIC_API_URL` según tu entorno
3. Reinicia el contenedor frontend:

```bash
docker-compose restart frontend
```

### Opción 2: Build con Variables

```bash
# Construir con variables específicas
docker build --build-arg API_URL=http://tu-servidor:8080 -t frontend ./frontend
```

## 📋 Checklist de Configuración

- [ ] Verificar que el backend esté corriendo en el puerto correcto
- [ ] Confirmar que Nginx esté proxyeando correctamente
- [ ] Probar conectividad desde el navegador: `http://tu-servidor:8080/api/health/`
- [ ] Verificar que no haya problemas de CORS
- [ ] Probar login y funcionalidades básicas

## 🐛 Troubleshooting

### Error: "Failed to fetch" / "Network Error"

- Verificar que `NEXT_PUBLIC_API_URL` apunte al servidor correcto
- Confirmar que Nginx esté corriendo en el puerto 8080
- Revisar logs de Nginx: `docker-compose logs nginx`

### Error CORS

- Asegurarse de que las requests vayan a través de Nginx (puerto 8080)
- Verificar configuración CORS en `docker/nginx/nginx.conf`

### Error 502 Bad Gateway

- Backend no está respondiendo
- Verificar que el contenedor backend esté saludable
- Revisar logs: `docker-compose logs backend`
