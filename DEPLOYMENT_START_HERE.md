# 🚀 DESPLIEGUE A PRODUCCIÓN - DealaAI v1.0.0-MVP

> **¡IMPORTANTE!** Lee esto PRIMERO antes de desplegar

## 📍 Documentación Rápida

Si tienes **prisa**, sigue este orden:

1. **Empezar aquí** → [DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md) (5 min)
2. **Guía detallada** → [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) (seguir paso a paso)
3. **Referencia completa** → [DEPLOYMENT_GUIDE_PRODUCTION.md](./DEPLOYMENT_GUIDE_PRODUCTION.md)

---

## ⚡ 5 PASOS RÁPIDOS (2 horas)

```bash
# PASO 1: Git
git commit -am "feat: MVP v1.0.0"
git tag v1.0.0-mvp
git push origin main v1.0.0-mvp

# PASO 2: .env
cat > .env.production << 'EOF'
DEBUG=False
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')
ALLOWED_HOSTS=mcp.jorgemg.es,www.mcp.jorgemg.es
DATABASE_URL=postgresql://dealaai_user:PASSWORD@db:5432/dealaai_prod
REDIS_URL=redis://redis:6379/0
SECURE_SSL_REDIRECT=True
CORS_ALLOWED_ORIGINS=https://mcp.jorgemg.es,https://www.mcp.jorgemg.es
NEXT_PUBLIC_API_URL=https://mcp.jorgemg.es/api
EOF

# PASO 3: SSH & Setup
ssh usuario@mcp.jorgemg.es
cd /opt/dealaai
git clone <repo> && cd AI4Devs-finalproject
git checkout v1.0.0-mvp
# Copiar .env.production manualmente
sudo certbot certonly --standalone -d mcp.jorgemg.es

# PASO 4: Deploy
docker-compose -f docker-compose.production.yml up -d
sleep 60
docker-compose -f docker-compose.production.yml exec backend python manage.py migrate
docker-compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
docker-compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput

# PASO 5: Verificar
curl -I https://mcp.jorgemg.es/
# Abrir navegador: https://mcp.jorgemg.es/login
```

---

## 📋 Pre-Deploy Checklist

- [ ] Código en rama `main`
- [ ] Tag `v1.0.0-mvp` creado
- [ ] `.env.production` preparado (NO commitear)
- [ ] SSL/HTTPS certificados obtenidos
- [ ] Servidor accesible vía SSH
- [ ] Docker y Docker Compose instalados en servidor

---

## 🎯 Lo Que Incluye Este MVP

✅ Autenticación con JWT  
✅ Rutas protegidas  
✅ Dashboard  
✅ Tabla de stock (17 columnas)  
✅ Perfil de usuario  
✅ Persistencia de sesión  
✅ Nginx reverse proxy  
✅ SSL/HTTPS automático  
✅ PostgreSQL + Redis  
✅ Backups automáticos  
✅ Health checks

---

## 🔐 Seguridad

- ❌ No commitear `.env.production`
- ❌ No commitear contraseñas
- ✅ Usar `SECURE_SSL_REDIRECT=True`
- ✅ Usar `SESSION_COOKIE_SECURE=True`
- ✅ Usar `CSRF_COOKIE_SECURE=True`
- ✅ Cambiar `SECRET_KEY` a valor aleatorio

---

## 🆘 Primeros Pasos si Algo Falla

```bash
# Ver qué servicios están corriendo
docker-compose -f docker-compose.production.yml ps

# Ver logs
docker-compose -f docker-compose.production.yml logs -f

# Reiniciar servicios
docker-compose -f docker-compose.production.yml restart

# Full restart
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d
```

---

## 📞 Documentación por Tema

### Para Entender el Deploy

→ Ver [DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md)

### Para Hacerlo Paso a Paso

→ Ver [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)

### Para Referencias Completas

→ Ver [DEPLOYMENT_GUIDE_PRODUCTION.md](./DEPLOYMENT_GUIDE_PRODUCTION.md)

### Para Persistencia de Sesión

→ Ver [SESSION_PERSISTENCE_NOTES.md](./SESSION_PERSISTENCE_NOTES.md)

### Para Estructura del Proyecto

→ Ver [README.md](./README.md)

---

## 🎓 Script Automático (Opcional)

```bash
# Opcionalmente, puedes usar script de automatización
chmod +x deploy-production.sh
./deploy-production.sh
# Te guiará por validaciones y te dará instrucciones
```

---

## 📊 Timeline Estimado

| Fase                  | Tiempo       | Descripción           |
| --------------------- | ------------ | --------------------- |
| **Preparación Local** | 30 min       | Git, .env, validación |
| **Setup Servidor**    | 45 min       | SSH, directorios, SSL |
| **Deploy**            | 30 min       | docker-compose up     |
| **Verificación**      | 20 min       | Testing manual        |
| **Monitoreo**         | 15 min       | Backup, healthcheck   |
| **TOTAL**             | **~2 horas** | Primera vez           |

---

## 🌐 URLs Finales

```
Frontend:     https://mcp.jorgemg.es/
Login:        https://mcp.jorgemg.es/login
Dashboard:    https://mcp.jorgemg.es/dashboard
Stock:        https://mcp.jorgemg.es/stock
Admin:        https://mcp.jorgemg.es/admin/
API Health:   https://mcp.jorgemg.es/api/health/
```

---

## 📝 Credenciales de Superusuario

**CREAR DURANTE DEPLOYMENT** (Paso 3.5)

```
Usuario: admin
Email: admin@mcp.jorgemg.es
Password: [Tu contraseña fuerte]
```

---

## 🔄 Ciclo de Updates Futuros

Cuando hayas hecho cambios y quieras actualizar producción:

```bash
# En local
git commit -am "feat: nueva feature"
git push origin main
git tag v1.1.0
git push origin v1.1.0

# En servidor
git fetch origin
git checkout v1.1.0
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d --build
docker-compose -f docker-compose.production.yml exec backend python manage.py migrate
docker-compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput
```

---

## ✅ Estado Actual

| Componente                | Status   | Notas                                 |
| ------------------------- | -------- | ------------------------------------- |
| **Frontend (Next.js)**    | ✅ Ready | Rutas protegidas, persistencia sesión |
| **Backend (Django)**      | ✅ Ready | JWT, API health check                 |
| **Database (PostgreSQL)** | ✅ Ready | Migraciones listas                    |
| **Cache (Redis)**         | ✅ Ready | Para Celery y cache                   |
| **Nginx**                 | ✅ Ready | Reverse proxy, SSL                    |
| **Celery**                | ✅ Ready | Workers y beat programados            |
| **Backups**               | ✅ Ready | Script listo, agregar a cron          |
| **Monitoring**            | ✅ Ready | Healthcheck script listo              |

---

## 🎯 Próximas Versiones

**v1.1.0** (Después de validar MVP)

- [ ] Sistema completo de leads
- [ ] Chat con IA
- [ ] Reportes avanzados

**v1.2.0**

- [ ] Dashboard mejorado
- [ ] Export a Excel
- [ ] Notificaciones por email

---

## 💡 Tips

1. **Mantén los logs abiertos** mientras testeas

   ```bash
   docker-compose -f docker-compose.production.yml logs -f
   ```

2. **Prueba todo manualmente** en navegador:

   - Login/Logout
   - Recarga (F5) - sesión debe persistir
   - Stock table
   - Diferentes rutas

3. **Configura backups Y healthchecks** - son críticos

4. **Documenta todo** - accesos, contraseñas (seguro), procesos

---

## 🆘 Soporte

Si tienes dudas sobre algún paso:

1. Buscar en [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) - Sección "PROBLEMAS COMUNES"
2. Ver logs: `docker-compose -f docker-compose.production.yml logs`
3. Revisar [DEPLOYMENT_GUIDE_PRODUCTION.md](./DEPLOYMENT_GUIDE_PRODUCTION.md) - Sección "Troubleshooting"

---

## 📅 Fecha de Release

**v1.0.0-mvp**

- Release Date: 26 de Octubre, 2025
- Status: ✅ LISTO PARA PRODUCCIÓN
- Dominio: https://mcp.jorgemg.es

---

## 🎉 ¡BUENA SUERTE!

Tu MVP está listo para ir a producción.

**Sigue los pasos en [DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md) y estarás en vivo en ~2 horas.**

---

**Versión**: 1.0.0-mvp  
**Última Actualización**: 26 de Octubre, 2025  
**Status**: ✅ PRODUCCIÓN READY
