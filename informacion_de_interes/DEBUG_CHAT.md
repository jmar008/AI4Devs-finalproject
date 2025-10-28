# 🔧 DEBUG - Chat Widget

## Pasos para verificar el problema

### 1. Abre la consola del navegador (F12)

### 2. Deberías ver estos logs cuando cargas la página:

```
🔄 ChatWidget: isOpen changed to false
🔵 Renderizando botón flotante
```

### 3. Cuando haces click en "Chat IA" en el sidebar, deberías ver:

```
🤖 Abriendo chat...
📱 ChatStore: openChat called
🔄 ChatWidget: isOpen changed to true
💬 Renderizando widget completo
```

### 4. Si ves estos logs, el problema es de CSS/z-index

### 5. Si NO ves los logs, el problema es que:

- El ChatWidget no se está renderizando
- El botón del sidebar no está llamando a openChat()

## Solución rápida

Si el widget no aparece pero ves los logs, prueba esto:

1. Abre DevTools
2. Inspecciona el elemento del botón flotante
3. Verifica que el z-index sea 50
4. Verifica que position sea fixed
5. Verifica que esté al final del DOM (después del main content)

## Test manual

Abre la consola y ejecuta:

```javascript
// Verificar estado del store
const chatStore = window.__ZUSTAND_STORES__?.chatStore;
console.log("isOpen:", chatStore?.getState().isOpen);

// Forzar apertura
chatStore?.getState().openChat();
```
