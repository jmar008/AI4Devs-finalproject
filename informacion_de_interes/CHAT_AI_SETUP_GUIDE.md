# 🤖 Chat AI con DeepSeek - Guía Completa

## 📋 Resumen de Implementación

Se ha implementado un **chat AI flotante** en la esquina inferior derecha que permite consultar sobre el stock de vehículos usando la API de **DeepSeek**.

---

## ✅ Componentes Implementados

### **Backend (Django)**

#### 1. **Nueva App: `ai_chat`**

- **Ubicación**: `/workspace/backend/apps/ai_chat/`
- **Modelos**:
  - `ChatConversation`: Almacena conversaciones de usuarios
  - `ChatMessage`: Almacena mensajes individuales (usuario y asistente)

#### 2. **Servicios**

- **`StockQueryService`** (`services.py`):

  - Consulta el stock de la base de datos
  - Genera estadísticas y resúmenes
  - Búsqueda avanzada de vehículos
  - Genera contexto para la IA

- **`DeepSeekService`** (`deepseek_service.py`):
  - Maneja la comunicación con DeepSeek AI
  - Prepara mensajes con contexto del stock
  - Procesa respuestas de la IA

#### 3. **API Endpoints**

Base URL: `/api/chat/`

- **`POST /api/chat/send/`**: Enviar mensaje al chat

  ```json
  {
    "message": "¿Cuántos coches tenemos?",
    "conversation_id": 1 // Opcional
  }
  ```

- **`GET /api/chat/conversations/`**: Listar todas las conversaciones
- **`GET /api/chat/conversation/{id}/`**: Obtener conversación específica
- **`DELETE /api/chat/conversation/{id}/delete/`**: Eliminar conversación
- **`POST /api/chat/clear/`**: Limpiar todas las conversaciones
- **`GET /api/chat/stock-summary/`**: Resumen directo del stock

### **Frontend (Next.js/React)**

#### 1. **ChatStore** (Zustand)

- **Ubicación**: `/workspace/frontend/store/chatStore.ts`
- Gestiona estado del chat (abierto, minimizado, mensajes, conversaciones)

#### 2. **ChatWidget Component**

- **Ubicación**: `/workspace/frontend/components/ChatWidget.tsx`
- Widget flotante en esquina inferior derecha
- Funcionalidades:
  - Minimizar/Maximizar
  - Historial de mensajes
  - Indicador de carga
  - Limpiar conversación

#### 3. **Chat API Client**

- **Ubicación**: `/workspace/frontend/lib/chatAPI.ts`
- Cliente TypeScript para comunicarse con el backend

---

## 🚀 Configuración e Instalación

### **Paso 1: Obtener API Key de DeepSeek**

1. Visita: https://platform.deepseek.com/
2. Regístrate o inicia sesión
3. Ve a la sección de API Keys
4. Genera una nueva API Key
5. Copia la key (formato: `sk-...`)

### **Paso 2: Configurar Variables de Entorno**

Edita el archivo `/workspace/backend/.env` y añade:

```bash
DEEPSEEK_API_KEY=sk-tu-api-key-aqui
```

### **Paso 3: Instalar Dependencias Backend**

```bash
cd /workspace/backend
pip install -r requirements.txt
```

Esto instalará:

- `openai==1.54.3` (compatible con DeepSeek)

### **Paso 4: Ejecutar Migraciones**

```bash
# Crear migraciones
python manage.py makemigrations ai_chat

# Aplicar migraciones
python manage.py migrate
```

### **Paso 5: Verificar Instalación**

```bash
# Iniciar backend
python manage.py runserver 0.0.0.0:8000

# En otro terminal, iniciar frontend
cd /workspace/frontend
npm run dev
```

---

## 💡 Uso del Chat AI

### **Acceso**

1. Inicia sesión en la aplicación
2. Verás un **botón flotante azul** con icono de chat en la esquina inferior derecha
3. Haz clic para abrir el chat
4. También puedes hacer clic en **"Chat IA"** en el sidebar

### **Ejemplos de Preguntas**

#### Consultas Generales:

- "¿Cuántos vehículos tenemos en stock?"
- "¿Cuál es el precio promedio de los coches?"
- "Muéstrame las marcas disponibles"

#### Búsquedas Específicas:

- "¿Tienes algún BMW disponible?"
- "Muéstrame coches de menos de 20.000€"
- "¿Qué Audi tenemos con menos de 50.000 km?"

#### Estadísticas:

- "¿Cuántos coches reservados tenemos?"
- "¿Cuál es la marca con más vehículos?"
- "Dime el rango de precios de nuestro stock"

#### Comparaciones:

- "Compara los precios de BMW y Mercedes"
- "¿Qué marca tiene el kilometraje más bajo?"

---

## 🎨 Funcionalidades del Widget

### **Botón Flotante**

- Siempre visible en esquina inferior derecha
- Color: Azul índigo (brand color)
- Icono: MessageSquare
- Hover: Escala y cambia color

### **Widget Expandido**

- **Tamaño**: 384px × 600px
- **Header**:
  - Título: "Chat IA - DealaAI"
  - Botones: Limpiar, Minimizar, Cerrar
- **Área de mensajes**:
  - Scroll automático
  - Mensajes del usuario: Azul (derecha)
  - Mensajes del asistente: Gris (izquierda)
  - Timestamps
- **Input**:
  - Placeholder: "Escribe tu mensaje..."
  - Enter para enviar
  - Botón de envío con icono

### **Estados**

- ✅ Normal
- 🔄 Cargando (spinner)
- 📦 Vacío (mensaje de bienvenida)
- ➖ Minimizado

---

## 🏗️ Arquitectura

### **Flujo de Datos**

```
Usuario → ChatWidget → chatAPI → Backend ViewSet
                                      ↓
                                  DeepSeekService
                                      ↓
                                StockQueryService → Base de Datos (Stock)
                                      ↓
                                  DeepSeek AI API
                                      ↓
                                  Respuesta → ChatMessage → Frontend
```

### **Contexto Enviado a DeepSeek**

Para cada mensaje, se envía:

1. **System Prompt**: Instrucciones de comportamiento de la IA
2. **Contexto del Stock**:
   - Resumen general (total vehículos, disponibles, reservados)
   - Top 10 marcas con estadísticas
   - Distribución por rangos de precio
3. **Historial de Conversación**: Últimos 10 mensajes
4. **Mensaje del Usuario**: Pregunta actual

---

## 🔧 Personalización

### **Cambiar Modelo de IA**

Edita `/workspace/backend/dealaai/settings/base.py`:

```python
DEEPSEEK_MODEL = 'deepseek-chat'  # o 'deepseek-coder'
```

### **Ajustar Temperatura**

En `/workspace/backend/apps/ai_chat/views.py`, método `send_message`:

```python
ai_response = deepseek.chat(
    messages=messages,
    temperature=0.7,  # 0 = determinístico, 2 = muy creativo
)
```

### **Cambiar Límite de Tokens**

```python
ai_response = deepseek.chat(
    messages=messages,
    max_tokens=2000,  # Máximo de tokens en respuesta
)
```

### **Modificar System Prompt**

Edita `/workspace/backend/apps/ai_chat/deepseek_service.py`, método `create_system_message`.

---

## 🐛 Troubleshooting

### **Error: "DEEPSEEK_API_KEY no está configurada"**

**Solución**:

1. Verifica que `.env` contiene `DEEPSEEK_API_KEY=sk-...`
2. Reinicia el servidor Django

### **Error: "No se ha podido resolver la importación openai"**

**Solución**:

```bash
pip install openai==1.54.3
```

### **Chat no aparece en el frontend**

**Solución**:

1. Verifica que estás en una ruta protegida (`/dashboard`, `/stock`)
2. Recarga la página (Ctrl+R)
3. Revisa la consola del navegador para errores

### **Mensajes no se envían**

**Solución**:

1. Abre DevTools → Network
2. Verifica que la request a `/api/chat/send/` se completa
3. Revisa el token de autenticación
4. Comprueba los logs del backend: `python manage.py runserver`

### **Respuestas lentas**

Esto es normal, DeepSeek puede tardar 3-10 segundos dependiendo de:

- Longitud del contexto
- Complejidad de la pregunta
- Carga del servidor de DeepSeek

---

## 📊 Base de Datos

### **Tablas Creadas**

#### `ai_chat_conversations`

```sql
- id (PK)
- user_id (FK)
- title
- created_at
- updated_at
- is_active
```

#### `ai_chat_messages`

```sql
- id (PK)
- conversation_id (FK)
- role (user/assistant/system)
- content (TEXT)
- created_at
- tokens_used
- model_used
```

### **Consultas Útiles**

```sql
-- Total de conversaciones
SELECT COUNT(*) FROM ai_chat_conversations;

-- Mensajes por conversación
SELECT conversation_id, COUNT(*)
FROM ai_chat_messages
GROUP BY conversation_id;

-- Tokens usados por usuario
SELECT u.email, SUM(m.tokens_used) as total_tokens
FROM ai_chat_messages m
JOIN ai_chat_conversations c ON m.conversation_id = c.id
JOIN authentication_user u ON c.user_id = u.id
WHERE m.tokens_used IS NOT NULL
GROUP BY u.email;
```

---

## 🔐 Seguridad

### **Autenticación**

- ✅ Requiere token JWT válido
- ✅ Solo acceso a conversaciones propias
- ✅ Validación en cada endpoint

### **Rate Limiting**

⚠️ **Recomendación**: Implementar rate limiting para evitar abuso de la API de DeepSeek

Ejemplo con Django REST Framework Throttling:

```python
# En settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '100/hour',  # 100 requests por hora
    }
}
```

---

## 💰 Costos Estimados

DeepSeek es muy económico comparado con GPT-4:

- **Entrada**: ~$0.14 por millón de tokens
- **Salida**: ~$0.28 por millón de tokens

**Ejemplo**:

- Conversación promedio: 1.500 tokens
- Costo: ~$0.0004 USD
- 1000 mensajes: ~$0.40 USD

---

## 📈 Mejoras Futuras

### **Corto Plazo**

- [ ] Streaming de respuestas (respuesta en tiempo real)
- [ ] Historial de conversaciones en el widget
- [ ] Búsqueda en conversaciones pasadas
- [ ] Exportar conversaciones

### **Mediano Plazo**

- [ ] Sugerencias de preguntas frecuentes
- [ ] Análisis de sentimiento en mensajes
- [ ] Notificaciones de nuevos mensajes
- [ ] Compartir conversaciones entre usuarios

### **Largo Plazo**

- [ ] Voice input (reconocimiento de voz)
- [ ] Integración con WhatsApp/Telegram
- [ ] Analytics de uso del chat
- [ ] Fine-tuning del modelo con datos propios

---

## 📚 Recursos

### **DeepSeek**

- Documentación: https://platform.deepseek.com/docs
- API Reference: https://platform.deepseek.com/api-docs
- Pricing: https://platform.deepseek.com/pricing

### **OpenAI SDK (compatible)**

- Docs: https://platform.openai.com/docs/api-reference
- GitHub: https://github.com/openai/openai-python

---

## 🎯 Testing

### **Backend Tests**

```bash
cd /workspace/backend
pytest apps/ai_chat/tests.py -v
```

### **Frontend Tests**

```bash
cd /workspace/frontend
npm test ChatWidget
```

### **Manual Testing**

1. ✅ Abrir chat desde botón flotante
2. ✅ Abrir chat desde sidebar
3. ✅ Enviar mensaje simple
4. ✅ Enviar pregunta sobre stock
5. ✅ Minimizar/Maximizar
6. ✅ Cerrar y reabrir
7. ✅ Limpiar conversación
8. ✅ Verificar persistencia de mensajes

---

## 👨‍💻 Desarrollador

**Jorge Martín García**

- Proyecto: DealaAI
- Fecha: Octubre 2025
- Versión: 1.0.0

---

## 📝 Notas Finales

Este chat AI está diseñado específicamente para consultas sobre el **stock de vehículos**. El contexto se actualiza en cada mensaje con los datos más recientes de la base de datos.

Para soporte técnico o dudas, contacta al equipo de desarrollo.

---

**¡Disfruta del nuevo Chat AI! 🚀🤖**
