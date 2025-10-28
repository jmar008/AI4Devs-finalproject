# Prompts Utilizados en el Desarrollo de DealaAI

> Documentación de los prompts principales utilizados durante la creación del proyecto DealaAI, un sistema de gestión inteligente para concesionarios de automóviles. Los prompts reflejan el trabajo real realizado, incluyendo la implementación de autenticación JWT, gestión de inventario, dashboard frontend y generación de datos jerárquicos.

## Índice

1. [Descripción general del producto](#1-descripción-general-del-producto)
2. [Arquitectura del sistema](#2-arquitectura-del-sistema)
3. [Modelo de datos](#3-modelo-de-datos)
4. [Especificación de la API](#4-especificación-de-la-api)
5. [Historias de usuario](#5-historias-de-usuario)
6. [Tickets de trabajo](#6-tickets-de-trabajo)
7. [Pull requests](#7-pull-requests)

---

## 1. Descripción general del producto

**Prompt 1: Definición del Producto MVP**

```
📘 CONTEXTO
Estoy desarrollando un sistema de gestión para concesionarios de automóviles que necesita integrar gestión de inventario, autenticación de usuarios y un dashboard básico. El proyecto usa Next.js para frontend y Django para backend.

🎯 OBJETIVO
Crear una descripción completa del producto MVP que incluya funcionalidades clave, stack tecnológico y valor para concesionarios.

📋 REQUISITOS
- Enfocarse en funcionalidades implementables en 15 horas
- Incluir gestión de 1000+ vehículos con datos reales
- Sistema de autenticación jerárquica con 46 usuarios
- Dashboard responsive con métricas básicas
- Documentación técnica completa

🧠 ROL DEL ASISTENTE
Actúa como **Product Manager** especializado en software para el sector automotriz.

💡 FORMATO DE RESPUESTA
- Descripción del producto en formato markdown
- Lista de funcionalidades por módulo
- Stack tecnológico detallado
- Beneficios cuantificables
- Público objetivo específico
```

**Prompt 2: Diseño de UX para Dashboard**

```
📘 CONTEXTO
Necesito diseñar la experiencia de usuario para un dashboard de gestión de concesionarios que debe ser intuitivo para diferentes roles: administradores, gerentes y vendedores.

🎯 OBJETIVO
Crear un flujo de usuario completo que describa las pantallas principales y interacciones del sistema MVP.

📋 REQUISITOS
- Dashboard con métricas de inventario y usuarios
- Páginas de login, listado de stock y detalle de vehículos
- Diseño responsive (mobile, tablet, desktop)
- Navegación clara entre módulos
- Estados de carga y manejo de errores

🧠 ROL DEL ASISTENTE
Actúa como **UX Designer** con experiencia en aplicaciones B2B.

💡 FORMATO DE RESPUESTA
- Descripción de cada pantalla principal
- Flujo de navegación entre páginas
- Elementos de UI clave por pantalla
- Consideraciones de accesibilidad
- Mockups textuales detallados
```

**Prompt 3: Instrucciones de Instalación**

```
📘 CONTEXTO
He implementado un sistema full-stack con Next.js frontend, Django backend y PostgreSQL, containerizado con Docker. Necesito crear instrucciones de instalación para desarrolladores.

🎯 OBJETIVO
Generar una guía completa de instalación y configuración del entorno de desarrollo.

📋 REQUISITOS
- Setup con Docker Compose (método recomendado)
- Instalación manual como alternativa
- Configuración de variables de entorno
- Comandos para inicializar base de datos
- Verificación de funcionamiento
- Troubleshooting común

🧠 ROL DEL ASISTENTE
Actúa como **DevOps Engineer** especializado en entornos de desarrollo.

💡 FORMATO DE RESPUESTA
- Guía paso a paso en markdown
- Comandos específicos para cada paso
- Variables de entorno requeridas
- Comandos de verificación
- Soluciones a problemas comunes
```

---

## 2. Arquitectura del Sistema

### **2.1. Diagrama de arquitectura:**

**Prompt 1: Arquitectura General del Sistema**

```
📘 CONTEXTO
Estoy diseñando la arquitectura para un sistema de gestión de concesionarios con frontend Next.js, backend Django y base de datos PostgreSQL con Docker.

🎯 OBJETIVO
Crear una arquitectura clara que separe responsabilidades y permita escalabilidad futura.

📋 REQUISITOS
- Separación frontend/backend clara
- API REST con Django REST Framework
- Base de datos PostgreSQL con pgvector
- Containerización completa con Docker
- Nginx como reverse proxy
- Justificación de decisiones técnicas

🧠 ROL DEL ASISTENTE
Actúa como **Software Architect** con experiencia en aplicaciones web modernas.

💡 FORMATO DE RESPUESTA
- Diagrama de arquitectura en texto
- Descripción de cada componente
- Flujo de datos entre componentes
- Beneficios y trade-offs de la arquitectura
- Consideraciones de escalabilidad
```

**Prompt 2: Componentes Técnicos Detallados**

```
📘 CONTEXTO
Necesito documentar técnicamente los componentes principales del sistema DealaAI: Next.js frontend, Django backend y PostgreSQL con pgvector.

🎯 OBJETIVO
Crear documentación técnica detallada de cada componente del sistema.

📋 REQUISITOS
- Descripción de tecnologías específicas
- Responsabilidades de cada componente
- Interfaces de comunicación
- Configuraciones importantes
- Consideraciones de seguridad

🧠 ROL DEL ASISTENTE
Actúa como **Technical Lead** con experiencia en full-stack development.

💡 FORMATO DE RESPUESTA
- Documentación por componente
- Código de ejemplo representativo
- Configuraciones específicas
- Decisiones técnicas justificadas
- Consideraciones de performance
```

**Prompt 3: Infraestructura de Despliegue**

```
📘 CONTEXTO
He implementado un sistema containerizado con Docker que necesita desplegarse en producción. El stack incluye Next.js, Django, PostgreSQL y Nginx.

🎯 OBJETIVO
Diseñar la infraestructura de despliegue para desarrollo, staging y producción.

📋 REQUISITOS
- Docker Compose para desarrollo local
- Configuración de Nginx como reverse proxy
- Estrategias de deployment
- Variables de entorno por ambiente
- Monitoreo básico
- Backup y recovery

🧠 ROL DEL ASISTENTE
Actúa como **DevOps Architect** especializado en containerización.

💡 FORMATO DE RESPUESTA
- Configuración de Docker Compose
- Archivo de configuración Nginx
- Scripts de deployment
- Variables de entorno documentadas
- Estrategias de backup
- Consideraciones de seguridad
```

### **2.2. Descripción de componentes principales:**

**Prompt 1: Documentación Frontend Next.js**

```
📘 CONTEXTO
He implementado un frontend Next.js con App Router que incluye autenticación, dashboard y gestión de stock. Necesito documentar la arquitectura técnica.

🎯 OBJETIVO
Crear documentación técnica completa del frontend Next.js implementado.

📋 REQUISITOS
- Estructura de carpetas del proyecto
- Uso de App Router vs Pages Router
- Gestión de estado con Zustand
- Componentes implementados
- Integración con APIs
- Optimizaciones de performance

🧠 ROL DEL ASISTENTE
Actúa como **Senior Frontend Developer** especializado en Next.js.

💡 FORMATO DE RESPUESTA
- Estructura de archivos detallada
- Explicación de patrones utilizados
- Código de ejemplo de componentes clave
- Configuraciones importantes
- Decisiones técnicas justificadas
```

**Prompt 2: Documentación Backend Django**

```
📘 CONTEXTO
He desarrollado un backend Django con REST Framework que incluye modelos de usuarios, stock, autenticación JWT y APIs REST. Necesito documentar la implementación.

🎯 OBJETIVO
Crear documentación técnica del backend Django implementado.

📋 REQUISITOS
- Estructura de apps Django
- Modelos de datos implementados
- Sistema de autenticación JWT
- Endpoints API desarrollados
- Configuraciones de seguridad
- Manejo de errores

🧠 ROL DEL ASISTENTE
Actúa como **Senior Backend Developer** especializado en Django.

💡 FORMATO DE RESPUESTA
- Estructura del proyecto Django
- Modelos y relaciones de datos
- Configuración de DRF
- Endpoints implementados
- Código de ejemplo representativo
- Consideraciones de seguridad
```

**Prompt 3: Estructura del Proyecto Monorepo**

```
📘 CONTEXTO
He organizado el proyecto como monorepo con frontend y backend separados, más configuración Docker y documentación. Necesito documentar la estructura completa.

🎯 OBJETIVO
Crear una guía clara de la estructura del proyecto y organización de archivos.

📋 REQUISITOS
- Estructura de carpetas completa
- Propósito de cada directorio
- Archivos importantes por carpeta
- Patrones de organización
- Convenciones de naming
- Best practices aplicadas

🧠 ROL DEL ASISTENTE
Actúa como **Technical Lead** responsable de la arquitectura del proyecto.

💡 FORMATO DE RESPUESTA
- Árbol de directorios completo
- Descripción de cada carpeta principal
- Archivos clave identificados
- Patrones de organización explicados
- Guía para nuevos desarrolladores
```

---

## 3. Modelo de Datos

**Prompt 1: Diseño del Modelo de Datos**

```
📘 CONTEXTO
Necesito diseñar el modelo de datos para un sistema de gestión de concesionarios que incluya usuarios jerárquicos, inventario de vehículos y autenticación.

🎯 OBJETIVO
Crear un modelo de datos completo para PostgreSQL que soporte todas las funcionalidades del sistema.

📋 REQUISITOS
- Usuarios con jerarquía organizacional
- Vehículos con 140+ campos técnicos
- Sistema de autenticación JWT
- Relaciones entre entidades
- Índices para performance
- Consideraciones de escalabilidad

🧠 ROL DEL ASISTENTE
Actúa como **Data Architect** especializado en PostgreSQL.

💡 FORMATO DE RESPUESTA
- Diagrama ERD en Mermaid
- Descripción detallada de entidades
- Atributos con tipos de datos precisos
- Relaciones y cardinalidad
- Índices y restricciones
- Consideraciones de performance
```

**Prompt 2: Implementación de Modelos Django**

```
📘 CONTEXTO
He implementado modelos Django para usuarios, stock y autenticación. Necesito documentar los modelos creados con sus campos y relaciones.

🎯 OBJETIVO
Crear documentación completa de los modelos Django implementados.

📋 REQUISITOS
- Modelos User, Profile, Stock
- Campos con tipos específicos
- Relaciones ForeignKey y ManyToMany
- Métodos importantes
- Validaciones implementadas
- Configuraciones Meta

🧠 ROL DEL ASISTENTE
Actúa como **Django Developer** especializado en modelado de datos.

💡 FORMATO DE RESPUESTA
- Código completo de cada modelo
- Explicación de campos complejos
- Relaciones entre modelos
- Métodos de instancia y clase
- Configuraciones de Meta
- Consideraciones de performance
```

**Prompt 3: Optimizaciones de Base de Datos**

```
📘 CONTEXTO
He implementado una base de datos PostgreSQL con modelos complejos. Necesito optimizaciones para consultas frecuentes en inventario y usuarios.

🎯 OBJETIVO
Implementar optimizaciones de base de datos para mejorar performance.

📋 REQUISITOS
- Índices compuestos para búsquedas
- Optimización de consultas complejas
- Configuración de pgvector si es necesario
- Estrategias de particionamiento
- Monitoring de performance
- Backup y recovery

🧠 ROL DEL ASISTENTE
Actúa como **Database Administrator** especializado en PostgreSQL.

💡 FORMATO DE RESPUESTA
- Scripts SQL de optimización
- Índices recomendados
- Consultas optimizadas
- Estrategias de monitoring
- Procedimientos de mantenimiento
- Consideraciones de escalabilidad
```

---

## 4. Especificación de la API

**Prompt 1: API de Gestión de Stock**

```
📘 CONTEXTO
He implementado una API REST con Django REST Framework para gestión de inventario de vehículos. Necesito documentar los endpoints creados.

🎯 OBJETIVO
Crear especificación completa de la API de stock implementada.

📋 REQUISITOS
- Endpoints CRUD para vehículos
- Filtros avanzados (marca, modelo, precio)
- Paginación implementada
- Autenticación JWT requerida
- Manejo de errores
- Formatos de respuesta

🧠 ROL DEL ASISTENTE
Actúa como **API Designer** especializado en REST APIs.

💡 FORMATO DE RESPUESTA
- Especificación OpenAPI 3.0
- Endpoints documentados
- Parámetros y respuestas
- Ejemplos de uso
- Códigos de error
- Consideraciones de seguridad
```

**Prompt 2: API de Autenticación**

```
📘 CONTEXTO
He implementado un sistema de autenticación JWT con Django. Necesito documentar los endpoints de login, registro y gestión de tokens.

🎯 OBJETIVO
Crear documentación completa de la API de autenticación implementada.

📋 REQUISITOS
- Endpoint de login
- Refresh de tokens
- Verificación de tokens
- Manejo de errores de autenticación
- Rate limiting
- Seguridad de contraseñas

🧠 ROL DEL ASISTENTE
Actúa como **Security Engineer** especializado en autenticación web.

💡 FORMATO DE RESPUESTA
- Endpoints documentados
- Flujo de autenticación explicado
- Configuraciones de seguridad
- Manejo de errores
- Ejemplos de requests/responses
- Consideraciones de seguridad
```

**Prompt 3: Endpoint de Estadísticas**

```
📘 CONTEXTO
He creado un endpoint para estadísticas del dashboard que proporciona métricas de usuarios, stock y sistema. Necesito documentarlo completamente.

🎯 OBJETIVO
Crear especificación del endpoint de analytics implementado.

📋 REQUISITOS
- Endpoint GET para métricas
- Filtros por período
- Datos de usuarios, stock y sistema
- Formato de respuesta estructurado
- Caching implementado
- Performance optimizada

🧠 ROL DEL ASISTENTE
Actúa como **Backend Developer** especializado en APIs de analytics.

💡 FORMATO DE RESPUESTA
- Especificación del endpoint
- Parámetros de consulta
- Estructura de respuesta
- Ejemplos de uso
- Consideraciones de performance
- Estrategias de caching
```

---

## 5. Historias de Usuario

**Prompt 1: Historia de Autenticación Jerárquica**

```
📘 CONTEXTO
Como desarrollador, necesito implementar un sistema de autenticación que soporte una jerarquía organizacional completa para un concesionario de automóviles.

🎯 OBJETIVO
Crear una historia de usuario completa para el sistema de autenticación implementado.

📋 REQUISITOS
- Jerarquía CEO → Directores → Gerentes → Seniors → Juniors
- 46 usuarios generados automáticamente
- Roles con permisos granulares
- Autenticación JWT persistente
- Dashboard personalizado por rol

🧠 ROL DEL ASISTENTE
Actúa como **Product Owner** especializado en sistemas de gestión empresarial.

💡 FORMATO DE RESPUESTA
- Historia de usuario en formato estándar
- Criterios de aceptación detallados
- Tareas técnicas específicas
- Definición de "Hecho"
- Métricas de éxito
- Escenarios de uso
```

**Prompt 2: Historia de Gestión de Inventario**

```
📘 CONTEXTO
Como gerente de concesionario, necesito gestionar un inventario de 1000+ vehículos con datos técnicos detallados y búsquedas avanzadas.

🎯 OBJETIVO
Crear una historia de usuario para la gestión de inventario implementada.

📋 REQUISITOS
- 140+ campos por vehículo
- Búsqueda por múltiples criterios
- Interfaz responsive
- Paginación optimizada
- Imágenes y descripciones
- API REST completa

🧠 ROL DEL ASISTENTE
Actúa como **Business Analyst** especializado en el sector automotriz.

💡 FORMATO DE RESPUESTA
- Historia de usuario completa
- Criterios de aceptación
- Tareas técnicas por componente
- Métricas cuantificables
- Casos de uso específicos
- Beneficios de negocio
```

**Prompt 3: Historia de Dashboard Ejecutivo**

```
📘 CONTEXTO
Como ejecutivo de concesionario, necesito un dashboard que me proporcione métricas clave del negocio en tiempo real.

🎯 OBJETIVO
Crear una historia de usuario para el dashboard implementado.

📋 REQUISITOS
- Métricas de usuarios y stock
- Interfaz responsive
- Actualización automática
- Filtros por período
- Visualizaciones claras
- Acceso basado en roles

🧠 ROL DEL ASISTENTE
Actúa como **UX Researcher** especializado en dashboards ejecutivos.

💡 FORMATO DE RESPUESTA
- Historia de usuario detallada
- Personas y escenarios de uso
- Requisitos funcionales y no funcionales
- Criterios de aceptación
- Métricas de éxito
- Consideraciones de UX
```

---

## 6. Tickets de Trabajo

**Prompt 1: Ticket de Generación de Usuarios Jerárquicos**

```
📘 CONTEXTO
Necesito implementar un comando Django que genere 46 usuarios con estructura jerárquica completa para testing del sistema de autenticación.

🎯 OBJETIVO
Crear un management command que genere usuarios realistas con relaciones jerárquicas.

📋 REQUISITOS
- 5 ejecutivos predefinidos
- 40 usuarios jerárquicos (5 niveles)
- 5 usuarios inactivos
- Relaciones jefe-subordinado
- Datos realistas (nombres, emails)
- Preservar usuario admin existente

🧠 ROL DEL ASISTENTE
Actúa como **Backend Developer** especializado en Django.

💡 FORMATO DE RESPUESTA
- Código completo del management command
- Lógica de generación jerárquica
- Manejo de relaciones de modelo
- Validaciones implementadas
- Comandos de ejecución
- Verificación de resultados
```

**Prompt 2: Ticket de Dashboard con Datos Reales**

```
📘 CONTEXTO
He implementado un dashboard básico con datos hardcodeados. Necesito conectarlo con datos reales de la API backend.

🎯 OBJETIVO
Modificar el dashboard para mostrar métricas reales del sistema.

📋 REQUISITOS
- Endpoint de estadísticas en backend
- Conexión API en frontend
- Actualización automática de datos
- Manejo de estados de carga
- Error handling apropiado
- Testing de integración

🧠 ROL DEL ASISTENTE
Actúa como **Full-Stack Developer** especializado en Next.js y Django.

💡 FORMATO DE RESPUESTA
- Código del endpoint backend
- Modificaciones del componente frontend
- Configuración de API client
- Estados de loading y error
- Tests de integración
- Documentación de cambios
```

**Prompt 3: Ticket de Optimización de Consultas**

```
📘 CONTEXTO
Las consultas de inventario están siendo lentas debido a la falta de índices apropiados en PostgreSQL.

🎯 OBJETIVO
Optimizar las consultas de base de datos para mejorar performance.

📋 REQUISITOS
- Análisis de consultas problemáticas
- Creación de índices compuestos
- Optimización de queries Django
- Medición de mejoras de performance
- Documentación de cambios
- Testing de regression

🧠 ROL DEL ASISTENTE
Actúa como **Database Specialist** especializado en PostgreSQL y Django.

💡 FORMATO DE RESPUESTA
- Análisis de consultas lentas
- Scripts SQL de índices
- Optimizaciones de código Django
- Resultados de benchmarking
- Estrategias de monitoring
- Plan de rollback
```

---

## 7. Pull Requests

**Prompt 1: PR de Implementación de Autenticación**

```
📘 CONTEXTO
He implementado un sistema completo de autenticación JWT con modelos de usuario jerárquicos. Necesito crear un Pull Request para merge a main.

🎯 OBJETIVO
Crear un PR completo que documente la implementación de autenticación.

📋 REQUISITOS
- Modelos User, Profile, Concesionario
- Sistema JWT completo
- Middleware de rutas protegidas
- Componentes de login frontend
- Testing básico
- Documentación actualizada

🧠 ROL DEL ASISTENTE
Actúa como **Senior Developer** creando un PR profesional.

💡 FORMATO DE RESPUESTA
- Descripción completa del PR
- Cambios técnicos detallados
- Testing realizado
- Screenshots de funcionalidad
- Breaking changes identificados
- Checklist de revisión
```

**Prompt 2: PR de Dashboard y Stock**

```
📘 CONTEXTO
He implementado el dashboard principal y la gestión de stock con API backend. Necesito documentar estos cambios en un PR.

🎯 OBJETIVO
Crear PR que documente la implementación del dashboard y módulo de stock.

📋 REQUISITOS
- Componentes de dashboard
- Páginas de listado y detalle de stock
- API endpoints de stock
- Modelo Stock con 140+ campos
- Testing de componentes
- Documentación de API

🧠 ROL DEL ASISTENTE
Actúa como **Frontend Developer** especializado en React/Next.js.

💡 FORMATO DE RESPUESTA
- Descripción técnica detallada
- Arquitectura de componentes
- Cambios en modelos backend
- Testing implementado
- Performance considerations
- Screenshots de UI
```

**Prompt 3: PR de Generación de Datos**

```
📘 CONTEXTO
He creado un management command que genera 46 usuarios jerárquicos realistas. Necesito documentar esta funcionalidad en un PR.

🎯 OBJETIVO
Crear PR para la implementación del sistema de generación de datos de prueba.

📋 REQUISITOS
- Management command completo
- Lógica de jerarquía organizacional
- Datos realistas generados
- Verificación de integridad
- Documentación de uso
- Testing del command

🧠 ROL DEL ASISTENTE
Actúa como **Backend Developer** especializado en Django.

💡 FORMATO DE RESPUESTA
- Descripción de la funcionalidad
- Código del management command
- Resultados de ejecución
- Testing realizado
- Impacto en base de datos
- Instrucciones de uso
```
