# Prompts Utilizados en el Desarrollo de DealaAI

> Detalla en esta sección los prompts principales utilizados durante la creación del proyecto, que justifiquen el uso de asistentes de código en todas las fases del ciclo de vida del desarrollo. Esperamos un máximo de 3 por sección, principalmente los de creación inicial o los de corrección o adición de funcionalidades que consideres más relevantes.

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

**Prompt 1:**
```
Como analista de producto especializado en el sector automotriz, necesito definir las características principales de una aplicación web de gestión para concesionarios de coches que incluya:

1. Gestión de inventario de vehículos con especificaciones detalladas
2. Sistema CRM para leads y seguimiento de clientes potenciales  
3. Módulo de ventas con pipeline visual
4. Chatbot IA que pueda consultar la base de datos usando RAG

El sistema debe integrarse con tecnologías modernas (NextJS, Django, Supabase) y estar orientado a mejorar la eficiencia operacional del concesionario. 

Genera una descripción detallada del producto que incluya:
- Propósito y valor diferencial
- Funcionalidades específicas por módulo
- Beneficios cuantificables esperados
- Público objetivo detallado
- Casos de uso principales

Enfócate en problemas reales que resuelve y cómo la IA mejora la experiencia.
```

**Prompt 2:**
```
Necesito diseñar la experiencia de usuario (UX) para una aplicación de gestión de concesionarios. El sistema debe ser intuitivo para usuarios con diferentes niveles técnicos: gerentes, vendedores y personal administrativo.

Crea un flujo de usuario que describa:

1. Dashboard principal personalizable por rol
2. Navegación entre módulos (inventario, leads, ventas, chat IA)
3. Proceso de búsqueda y filtrado de vehículos
4. Workflow de gestión de leads desde captura hasta conversión
5. Interfaz de chat IA conversacional

Considera:
- Responsive design para móvil y desktop
- Tiempos de respuesta <2 segundos
- Accesibilidad WCAG 2.1
- Progressive Web App (PWA) capabilities

Describe cada pantalla principal con sus elementos clave y interacciones.
```

**Prompt 3:**
```
Como Product Manager, necesito crear las instrucciones de instalación técnicas para desarrolladores que quieran deployar este sistema de gestión de concesionarios localmente.

El stack tecnológico incluye:
- Frontend: NextJS 13+ con TypeScript
- Backend: Django 4.2 + Django REST Framework  
- Base de datos: Supabase (PostgreSQL + pgvector)
- Containerización: Docker y Docker Compose
- IA: OpenAI GPT-4 + RAG con embeddings

Genera instrucciones paso a paso que incluyan:
1. Prerrequisitos y dependencias
2. Setup con Docker (método recomendado)
3. Instalación manual alternativa
4. Configuración de variables de entorno
5. Inicialización de base de datos y migraciones
6. Comandos para cargar datos de prueba
7. Verificación de que todo funciona correctamente

Incluye comandos específicos, archivos de configuración y troubleshooting común.
```

---

## 2. Arquitectura del Sistema

### **2.1. Diagrama de arquitectura:**

**Prompt 1:**
```
Como arquitecto de software, necesito diseñar una arquitectura de microservicios para una aplicación de gestión de concesionarios que debe manejar:

- Frontend NextJS con Server-Side Rendering
- Backend Django REST API
- Base de datos PostgreSQL con capacidades vectoriales (Supabase)
- Sistema de IA con RAG para chatbot
- Despliegue en contenedores Docker

Describe una arquitectura que incluya:
1. Separación clara de responsabilidades entre capas
2. Patrones de comunicación entre servicios
3. Estrategia de escalabilidad horizontal
4. Load balancing y reverse proxy
5. Manejo de estado y caching
6. Integración con servicios externos (OpenAI, CDN, etc.)

Justifica las decisiones arquitectónicas explicando beneficios y trade-offs. Considera aspectos de performance, mantenibilidad y costos.
```

**Prompt 2:**
```
Necesito crear un diagrama de componentes detallado para el sistema, enfocándome en las tecnologías específicas y sus interacciones.

Componentes principales:
- NextJS Frontend (puerto 3000): React components, API routes, SSR
- Nginx Load Balancer (puerto 80/443): Reverse proxy, SSL termination
- Django Backend (puerto 8000): REST API, business logic, admin
- Supabase Database: PostgreSQL + pgvector, real-time subscriptions
- AI Layer: RAG system, OpenAI integration, vector embeddings

Para cada componente describe:
1. Tecnologías específicas utilizadas
2. Responsabilidades principales  
3. Interfaces de comunicación (REST, WebSocket, etc.)
4. Dependencias y conexiones
5. Consideraciones de seguridad

Crea también un flujo de datos que muestre cómo se procesa una consulta típica del usuario desde el frontend hasta la respuesta del chatbot IA.
```

**Prompt 3:**
```
Como DevOps engineer, necesito documentar la infraestructura de despliegue y los procesos de CI/CD para esta aplicación de concesionarios.

Entornos requeridos:
- Desarrollo: Docker Compose local
- Staging: Réplica de producción para testing
- Producción: Cloud deployment con alta disponibilidad

Diseña:
1. Pipeline de CI/CD con GitHub Actions
2. Estrategia de deployment (blue/green, rolling, canary)
3. Configuración de monitoreo y alertas
4. Backup y disaster recovery procedures
5. Security scanning y vulnerability assessment
6. Performance monitoring y optimization

Incluye:
- Scripts de automatización específicos
- Configuración de Docker y Docker Compose
- Variables de entorno por ambiente
- Métricas clave a monitorear
- Procedimientos de rollback

Focus en DevOps best practices y reliability.
```

### **2.2. Descripción de componentes principales:**

**Prompt 1:**
```
Como desarrollador senior, necesito documentar técnicamente cada componente del sistema de gestión de concesionarios.

Para el Frontend NextJS:
- Describe la estructura de carpetas siguiendo App Router (Next 13+)
- Explica el uso de Server Components vs Client Components
- Detalla la gestión de estado con Zustand
- Documenta el sistema de routing y layouts
- Describe la integración con APIs y manejo de errores

Para cada aspecto incluye:
- Código de ejemplo representativo
- Patrones de diseño utilizados
- Optimizaciones de performance implementadas
- Consideraciones de SEO y accesibilidad
- Testing strategy (unit, integration, e2e)

Focus en decisiones técnicas que justifican el uso de cada tecnología.
```

**Prompt 2:**
```
Documenta el backend Django REST Framework con enfoque en la arquitectura API-first:

Estructura del proyecto:
1. Organización en apps Django por dominio de negocio
2. Configuración de Django REST Framework 
3. Sistema de autenticación JWT + permissions
4. Serializers y ViewSets personalizados
5. Integración con Celery para tareas asíncronas
6. Middleware custom para logging y monitoring

Para cada app (inventory, leads, sales, ai_chat):
- Modelos de datos y relaciones
- Views y endpoints API
- Business logic y validaciones
- Tests unitarios y de integración
- Documentation automática con OpenAPI

Incluye ejemplos de código que muestren:
- Custom permissions classes
- Complex queries optimization
- Error handling patterns
- API versioning strategy
```

**Prompt 3:**
```
Como especialista en AI/ML, documenta la implementación del sistema RAG (Retrieval-Augmented Generation) para el chatbot:

Componentes del sistema de IA:
1. Generación de embeddings con Sentence Transformers
2. Almacenamiento vectorial en Supabase (pgvector)
3. Búsqueda semántica con similarity search
4. Integración con OpenAI GPT-4 para generación de respuestas
5. Context window management para conversaciones

Aspectos técnicos a documentar:
- Proceso de embedding de contenido del concesionario
- Algoritmos de búsqueda vectorial utilizados
- Strategies para optimizar performance de queries
- Manejo de contexto conversacional
- Rate limiting y cost optimization para OpenAI API
- Fallback mechanisms cuando AI services no están disponibles

Incluye métricas de performance y calidad de respuestas esperadas.
```

### **2.3. Descripción de alto nivel del proyecto y estructura de ficheros**

**Prompt 1:**
```
Como Technical Lead, necesito crear una estructura de proyecto monorepo clara y escalable para el sistema de gestión de concesionarios.

Organización del proyecto:
- Monorepo con frontend y backend separados
- Shared utilities y types
- Docker configuration para desarrollo y producción
- Documentation y scripts de automatización

Crea una estructura de carpetas detallada que incluya:
1. Frontend NextJS con App Router structure
2. Backend Django con apps por dominio
3. Database migrations y fixtures
4. Docker configurations
5. CI/CD pipelines
6. Documentation folders
7. Testing utilities

Para cada carpeta principal explica:
- Su propósito específico
- Archivos importantes que contiene
- Patrones de naming conventions
- Relación con otros módulos
- Best practices aplicados

Focus en mantenibilidad y developer experience.
```

**Prompt 2:**
```
Documenta los patrones arquitectónicos y principios de diseño aplicados en el proyecto:

Patrones implementados:
1. Domain-Driven Design (DDD) en la organización
2. Clean Architecture con separación de capas
3. Repository Pattern para acceso a datos
4. Factory Pattern para objetos complejos
5. Observer Pattern para notificaciones
6. Strategy Pattern para diferentes tipos de reports

Para cada patrón explica:
- Cómo se implementa específicamente en el código
- Beneficios que aporta al proyecto
- Ejemplos concretos de uso
- Trade-offs considerados

Incluye también:
- Coding standards y linting rules
- Error handling conventions
- Logging y debugging strategies
- Security patterns aplicados
```

**Prompt 3:**
```
Como desarrollador senior, crea una guía de contribución al proyecto que explique:

Workflow de desarrollo:
1. Git branching strategy (GitFlow modificado)
2. Code review process y requirements
3. Testing requirements antes de merge
4. Documentation expectations
5. Performance benchmarks a mantener

Development environment setup:
- VS Code configuration con extensions recomendadas
- Dev containers setup para consistency
- Pre-commit hooks configuration
- Local testing procedures

Architectural decisions recording:
- Cómo documentar ADRs (Architecture Decision Records)
- Template para nuevas features
- Code quality gates
- Refactoring guidelines

Focus en developer onboarding y team collaboration efficiency.
```

### **2.4. Infraestructura y despliegue**

**Prompt 1:**
```
Como Cloud Architect, diseña la infraestructura completa de deployment para la aplicación de concesionarios:

Entornos cloud:
- Development: Docker Compose local + mock services
- Staging: Cloud deployment idéntico a producción
- Production: Multi-region setup con alta disponibilidad

Servicios cloud requeridos:
1. Frontend hosting con CDN global (Vercel)
2. Backend containerized deployment (Railway/AWS)
3. Database managed service (Supabase)
4. File storage y CDN para imágenes (Cloudinary)
5. Monitoring y logging (Sentry, DataDog)
6. CI/CD pipelines (GitHub Actions)

Para cada servicio define:
- Configuración específica y sizing
- Networking y security groups
- Backup y disaster recovery
- Monitoring y alerting rules
- Cost optimization strategies

Incluye diagramas de infraestructura y network topology.
```

**Prompt 2:**
```
Crea un pipeline de CI/CD completo usando GitHub Actions que maneje:

Pipeline stages:
1. Code quality checks (linting, type checking)
2. Automated testing (unit, integration, e2e)
3. Security scanning (dependencies, container images)
4. Build optimizations (bundle analysis, compression)
5. Deployment strategies por ambiente
6. Post-deployment verification
7. Rollback procedures

Configuración específica:
- Workflow files para diferentes triggers
- Environment-specific configurations
- Secrets management
- Artifact caching strategies
- Parallel job execution
- Notifications y reporting

Include specific GitHub Actions configuration files y scripts.
Focus on reliability, speed, y developer experience.
```

**Prompt 3:**
```
Como SRE specialist, diseña la estrategia completa de monitoring y observability:

Monitoring stack:
1. Application Performance Monitoring (APM)
2. Infrastructure monitoring (CPU, memory, network)
3. Database performance monitoring
4. User experience monitoring (RUM)
5. Business metrics tracking
6. Security monitoring (SIEM)

Key metrics to track:
- SLA/SLI definitions para cada servicio
- Error rates y response times
- Database query performance
- User engagement metrics
- Cost metrics por servicio
- Security incident detection

Alerting strategy:
- Alert fatigue prevention
- Escalation procedures
- On-call rotation setup
- Incident response playbooks
- Post-incident review processes

Incluye dashboard configurations y runbook examples.
```

### **2.5. Seguridad**

**Prompt 1:**
```
Como Security Engineer, diseña una estrategia de seguridad integral para el sistema de gestión de concesionarios:

Authentication & Authorization:
1. JWT-based authentication con refresh tokens
2. Role-Based Access Control (RBAC) granular
3. OAuth2 integration para social login
4. Multi-factor authentication (MFA) opcional
5. Session management y timeout policies
6. Password policies y secure storage

Implementación técnica:
- Custom Django permission classes
- Frontend route protection
- API endpoint security
- Token refresh mechanisms
- Secure cookie configuration
- CORS policies

Para cada aspecto incluye:
- Código de implementación específico
- Threat models considerados
- Compliance requirements (GDPR, etc.)
- Security testing procedures
```

**Prompt 2:**
```
Documenta las prácticas de Data Security y Privacy implementadas:

Data Protection:
1. Encryption at rest (database, files)
2. Encryption in transit (TLS 1.3)
3. PII data handling y anonymization
4. Data retention policies
5. Secure data backup procedures
6. GDPR compliance measures

API Security:
- Input validation y sanitization
- SQL injection prevention
- XSS protection mechanisms
- CSRF token implementation
- Rate limiting per user/endpoint
- API key management

Include specific code examples:
- Django security middleware configuration
- Input validation decorators
- Secure headers implementation
- Logging security events
- Audit trail mechanisms
```

**Prompt 3:**
```
Como Cybersecurity specialist, crea un plan de Security Monitoring y Incident Response:

Security Monitoring:
1. Intrusion Detection System (IDS) setup
2. Anomaly detection para user behavior
3. Failed login attempts tracking
4. Suspicious API usage patterns
5. File integrity monitoring
6. Vulnerability scanning automation

Incident Response:
- Security incident classification
- Response team roles y responsibilities
- Communication protocols
- Evidence preservation procedures
- Recovery procedures
- Post-incident analysis

Threat Intelligence:
- Common attack vectors en aplicaciones web
- Industry-specific threats (automotive sector)
- Zero-day vulnerability procedures
- Security patch management
- Penetration testing schedule

Include incident response playbooks y automated response scripts.
```

### **2.6. Tests**

**Prompt 1:**
```
Como QA Engineer, diseña una estrategia completa de testing para la aplicación:

Testing Pyramid Strategy:
1. Unit Tests (70%): Componentes y funciones individuales
2. Integration Tests (20%): APIs y database interactions  
3. E2E Tests (10%): User workflows críticos
4. Performance Tests: Load y stress testing

Para cada nivel define:
- Tools y frameworks específicos (Jest, Pytest, Playwright)
- Coverage requirements y métricas
- Test data management
- CI/CD integration
- Parallel execution strategies

Backend Testing (Django):
- Model testing con factories
- API endpoint testing
- Business logic validation
- Database query optimization tests
- Async task testing (Celery)

Frontend Testing (NextJS):
- Component testing con React Testing Library
- Hook testing strategies
- API integration mocking
- Accessibility testing
- Visual regression testing
```

**Prompt 2:**
```
Crea tests específicos para el sistema de IA (RAG/Chatbot):

AI System Testing:
1. Embedding generation accuracy tests
2. Vector similarity search validation
3. Context window management testing
4. OpenAI API integration mocking
5. Response quality assessment
6. Performance benchmarking

Test scenarios específicos:
- Diferentes tipos de queries del usuario
- Edge cases (empty results, API failures)
- Context overflow handling
- Multilingual support validation
- Response time requirements
- Cost optimization validation

Include:
- Mock data para embeddings
- Test fixtures para conversaciones
- Performance benchmarks
- Quality metrics definitions
- A/B testing framework setup

Considera también:
- Ethical AI testing (bias detection)
- Hallucination detection
- Source attribution validation
```

**Prompt 3:**
```
Como Test Automation Engineer, diseña tests de Performance y Reliability:

Performance Testing:
1. Load testing scenarios (normal, peak, stress)
2. Database performance under load
3. API response time validation
4. Frontend performance metrics
5. Memory leak detection
6. Resource utilization optimization

Test Tools Setup:
- K6 scripts para load testing
- Lighthouse CI para web performance
- Memory profiling tools
- Database query analysis
- CDN performance validation

Reliability Testing:
- Chaos engineering experiments
- Failure injection testing
- Recovery time measurement
- Data consistency validation
- Backup/restore procedures testing

Include specific test scripts:
- Load testing scenarios
- Performance regression detection
- Automated performance reporting
- Alert thresholds configuration
- Continuous performance monitoring setup
```

---

## 3. Modelo de Datos

**Prompt 1:**
```
Como Data Architect especializado en sistemas automotrices, diseña un modelo de datos comprehensivo para un sistema de gestión de concesionarios:

Entidades principales requeridas:
1. Usuarios del sistema (staff del concesionario)
2. Clientes y prospects
3. Inventario de vehículos con especificaciones detalladas
4. Leads y pipeline de ventas
5. Transacciones de venta completadas
6. Sistema de chat IA con historial
7. Actividades y seguimiento (audit trail)

Para cada entidad define:
- Atributos específicos con tipos de datos precisos
- Claves primarias y foráneas
- Restricciones e índices requeridos
- Relaciones entre entidades (1:1, 1:N, N:M)
- Consideraciones de performance para consultas frecuentes

Usa PostgreSQL con extensión pgvector para embeddings vectoriales. Considera escalabilidad para 10,000+ vehículos y 100,000+ leads.
```

**Prompt 2:**
```
Crea un diagrama Mermaid ERD (Entity Relationship Diagram) que represente visualmente el modelo de datos:

Especificaciones del diagrama:
- Usar sintaxis mermaid erDiagram
- Incluir todos los atributos con sus tipos
- Mostrar relaciones con cardinalidad
- Destacar claves primarias y foráneas
- Incluir restricciones importantes (UNIQUE, NOT NULL)

Entidades específicas a modelar:
1. USERS (sistema de roles jerárquico)
2. CUSTOMERS (datos completos del cliente)
3. VEHICLES (inventario con JSON para características flexibles)
4. LEADS (pipeline de ventas con scoring)
5. SALES (transacciones completadas)
6. CHAT_SESSIONS y CHAT_MESSAGES (sistema IA)
7. INVENTORY_MOVEMENTS (trazabilidad)
8. LEAD_ACTIVITIES (CRM activities)

Include comentarios descriptivos para campos complejos y considera particionamiento para tablas que crecen rápidamente.
```

**Prompt 3:**
```
Como Database Administrator, documenta las optimizaciones y consideraciones avanzadas del modelo de datos:

Performance Optimizations:
1. Estrategias de indexing (B-tree, GIN, HNSW para vectores)
2. Particionamiento de tablas por fecha
3. Materialized views para reporting
4. Query optimization patterns
5. Connection pooling configuration

Data Integrity:
- Triggers para validaciones complejas
- Stored procedures para operaciones críticas
- Audit trail automático
- Soft delete patterns
- Data archival policies

Scalability Considerations:
- Horizontal partitioning strategies
- Read replica configuration
- Caching layers (Redis integration)
- Backup y recovery procedures
- Migration strategies

Include specific SQL scripts:
- Table creation with optimizations
- Index creation strategies  
- Performance monitoring queries
- Maintenance procedures
- Data seeding scripts for testing
```

---

## 4. Especificación de la API

**Prompt 1:**
```
Como API Designer, crea una especificación OpenAPI 3.0 completa para el endpoint de gestión de vehículos del concesionario:

Endpoint: /api/v1/vehicles/
Métodos: GET (list with filters), POST (create), PUT (update), DELETE

Especificaciones requeridas:
1. Filtros avanzados (make, model, year range, price range, status)
2. Búsqueda full-text
3. Paginación con cursor-based y offset-based options
4. Sorting múltiple 
5. Field selection (sparse fieldsets)
6. Error handling comprehensivo
7. Authentication requirements

Para cada endpoint incluye:
- Parámetros de entrada con validaciones
- Schemas de respuesta detallados
- Códigos de error específicos con mensajes
- Ejemplos de request/response
- Rate limiting information
- Deprecation policies

Focus en RESTful best practices y developer experience.
```

**Prompt 2:**
```
Diseña la API específica del sistema de Chat IA con RAG:

Endpoints principales:
1. POST /api/v1/chat/sessions/ (crear nueva sesión)
2. GET /api/v1/chat/sessions/{id}/ (obtener historial)
3. POST /api/v1/chat/sessions/{id}/messages/ (enviar mensaje)
4. GET /api/v1/chat/search/ (búsqueda semántica directa)

Especificaciones técnicas:
- Request/response formats para conversación
- Context window management
- Source attribution en respuestas
- Streaming responses para mejor UX
- Error handling para AI service failures
- Rate limiting específico por usuario
- Metadata tracking (tokens used, response time, model version)

Include:
- WebSocket alternative para real-time chat
- Conversation export/import functionality
- Analytics endpoints para chat performance
- Content moderation integration
- Multi-language support considerations
```

**Prompt 3:**
```
Como Senior Backend Developer, crea la especificación del endpoint de Analytics/Dashboard:

Endpoint: /api/v1/analytics/dashboard/
Propósito: Métricas ejecutivas en tiempo real

Métricas requeridas:
1. Sales metrics (revenue, units, conversion rates)
2. Inventory metrics (total vehicles, turnover rate, aging)
3. Lead metrics (pipeline status, source attribution, conversion funnel)
4. Performance metrics (top salespeople, best-selling models)

Technical requirements:
- Time period filtering (today, week, month, quarter, year)
- Comparison with previous periods
- Real-time updates (consider WebSocket)
- Role-based data filtering
- Export functionality (PDF, Excel)
- Caching strategy for expensive calculations

Response structure:
- Nested JSON with logical grouping
- Include metadata (last_updated, calculation_time)
- Trend indicators (+/- percentage change)
- Drill-down capabilities
- Visualization-ready data formats

Include performance considerations for complex aggregations.
```

---

## 5. Historias de Usuario

**Prompt 1:**
```
Como Product Owner especializado en software automotriz, redacta una historia de usuario completa para la funcionalidad de "Gestión Inteligente de Inventario":

Context: Los gerentes de concesionarios necesitan visibilidad proactiva sobre vehículos que no se venden rápidamente para optimizar pricing y marketing.

Formato de historia:
- Como [persona]
- Quiero [objetivo]  
- Para [beneficio]

Incluye también:
1. Criterios de aceptación específicos (Given/When/Then)
2. Tareas técnicas detalladas (backend, frontend, database)
3. Definición de "Hecho" (Definition of Done)
4. Escenarios edge cases considerados
5. Métricas de éxito cuantificables

Focus en valor de negocio real y implementación técnica factible con IA para análisis predictivo de inventario.
```

**Prompt 2:**
```
Crea una historia de usuario avanzada para el "Chat IA con RAG":

Necesidad del negocio: Los vendedores necesitan acceso rápido a información específica sobre inventario, precios, y datos de clientes sin navegar múltiples pantallas.

Historia completa debe incluir:
1. Diferentes roles de usuarios (vendedores, gerentes, BDC)
2. Tipos de consultas que debe manejar el IA
3. Context-aware responses basado en historial
4. Integración con sistemas existentes
5. Fallback mechanisms cuando IA no puede responder

Escenarios específicos:
- Consultas sobre disponibilidad y pricing
- Análisis comparativo entre modelos
- Historial de ventas y trends
- Lead qualification assistance
- Inventory recommendations

Include ejemplos de conversaciones reales esperadas y cómo el sistema debe manejar ambiguity y follow-up questions.
```

**Prompt 3:**
```
Como Business Analyst, diseña la historia de usuario para "Pipeline Automatizado de Leads":

Business need: Optimizar la asignación automática de leads a vendedores basado en especialización, carga de trabajo y performance histórica.

Historia comprehensiva:
1. Lead assignment logic (algoritmo de scoring)
2. Escalation procedures para leads no contactados
3. Performance tracking y optimization
4. Integration con sistemas de marketing
5. Notification systems para vendedores

Criterios técnicos:
- Real-time lead scoring algorithms
- Automatic reassignment triggers
- Performance analytics dashboard
- A/B testing framework para optimization
- CRM integration requirements

Metrics de éxito:
- Tiempo promedio de primera respuesta
- Conversion rates por vendedor
- Lead distribution equity
- Customer satisfaction scores
- Revenue impact measurement

Include implementation phases y rollout strategy.
```

---

## 6. Tickets de Trabajo

**Prompt 1:**
```
Como Technical Lead, crea un ticket de trabajo detallado para implementar el "Sistema de Embeddings Vectoriales para Chat IA":

Ticket Type: Epic - Backend Feature
Story Points: 8 (2-3 días)
Priority: High

Technical requirements:
1. Embedding service using sentence-transformers
2. pgvector integration en Supabase
3. Similarity search optimization  
4. Batch processing para contenido existente
5. API endpoints para semantic search

Detailed tasks breakdown:
- Service class implementation
- Database schema changes
- Management commands para initial processing
- Unit y integration tests
- Performance benchmarking
- API documentation

Include:
- Acceptance criteria técnicos
- Performance requirements específicos
- Error handling strategies
- Security considerations
- Monitoring y logging requirements
- Definition of Done checklist

Code snippets esperados para key components.
```

**Prompt 2:**
```
Crea un ticket frontend para "Dashboard Responsivo con Métricas en Tiempo Real":

Ticket Details:
- Type: Feature - Frontend
- Estimation: 13 Story Points (3-4 días)  
- Dependencies: Analytics API endpoint

Technical Implementation:
1. Responsive grid layout con drag-and-drop
2. Real-time data updates con WebSocket/polling
3. Interactive charts con Chart.js/D3
4. Customizable widgets por user role
5. Export functionality (PDF/Excel)
6. Dark/light theme support

Component architecture:
- Dashboard container component
- Reusable metric cards
- Chart components library
- Data fetching hooks
- State management strategy

Performance requirements:
- First Contentful Paint < 2s
- Interactive ready < 3s
- Smooth 60fps animations
- Memory usage optimization
- Bundle size considerations

Include testing strategy (unit, integration, visual regression).
```

**Prompt 3:**
```
Como Database Specialist, crea un ticket para "Optimización de Consultas y Particionamiento":

Technical Debt Ticket:
- Priority: High (performance degradation en production)
- Effort: 5 Story Points (2 días)
- Impact: Critical system performance

Performance issues identificadas:
1. Inventory searches con multiple filters (800ms → target 100ms)
2. Dashboard analytics queries (2.3s → target 500ms)
3. Lead search performance (1.2s → target 200ms)
4. Vector similarity search optimization

Optimization strategies:
- Composite indexes para filtros frecuentes
- Partitioning de tablas grandes por fecha
- Materialized views para reporting
- Query optimization y rewrite
- Connection pooling configuration

Deliverables:
- SQL migration scripts
- Performance benchmark results
- Monitoring queries para ongoing optimization
- Documentation de new indexes
- Rollback procedures

Include before/after performance metrics y monitoring setup.
```

---

## 7. Pull Requests

**Prompt 1:**
```
Como Senior Developer, crea un Pull Request comprehensivo para la implementación del "Sistema RAG para Chat IA":

PR Details:
- Branch: feature/rag-chat-implementation → develop
- Files changed: ~15 files (backend principalmente)
- Lines added: ~800, deleted: ~50

Descripción completa debe incluir:
1. Feature summary y business value
2. Technical implementation details
3. Breaking changes (si los hay)
4. Performance implications
5. Security considerations
6. Testing coverage report

Code changes breakdown:
- New services y models
- API endpoints implementation  
- Database migrations
- Configuration changes
- Test files additions

Include:
- Before/after performance benchmarks
- Screenshot/demo de funcionalidad
- Deployment notes específicas
- Environment variables requeridas
- Migration instructions

PR checklist:
- Tests passing
- Code review completed
- Documentation updated
- Performance within targets
- Security review approved
```

**Prompt 2:**
```
Crea un Hotfix PR para resolver "Memory Leak en WebSocket Connections":

Emergency PR Details:
- Type: Hotfix Critical
- Branch: hotfix/websocket-memory-leak → main
- Impact: Production performance degradation

Incident context:
- Memory usage growing 50MB/hour per server
- Requiring server restarts every 4-6 hours
- Affecting ~200 usuarios durante peak times
- Root cause: Improper WebSocket cleanup

Technical fix:
1. Proper event listener cleanup en frontend
2. Connection tracking y cleanup en backend  
3. Memory monitoring improvements
4. Graceful disconnection handling
5. Connection pooling optimization

Fix validation:
- Memory leak tests
- Load testing results
- Production monitoring setup
- Rollback procedures documented

Include:
- Root cause analysis detallado
- Before/after metrics
- Monitoring improvements
- Prevention measures for future
- Post-incident review plan
```

**Prompt 3:**
```
Como Frontend Lead, documenta un PR para "Migración de Class Components a React Hooks":

Large Refactoring PR:
- Scope: 15 components migrados
- Bundle size impact: -23KB (-12%)
- Performance improvement: ~15% faster renders
- Code reduction: -340 lines total

Migration details:
1. Class components → functional components
2. Lifecycle methods → useEffect hooks
3. State management → useState/useReducer
4. Custom hooks extraction para reusable logic
5. Performance optimizations con useMemo/useCallback

Technical improvements:
- Better TypeScript integration
- Easier testing con React Testing Library
- Improved developer experience
- Modern React patterns adoption
- Code maintainability improvements

Quality assurance:
- Unit tests updated
- Integration tests passing
- Visual regression testing
- Cross-browser compatibility
- Performance benchmarking
- Accessibility compliance

Include migration strategy, rollback plan, y team training considerations.
```