# 🔴 DIAGNÓSTICO FINAL: Loop Infinito Chat ITSE

## ❌ PROBLEMA CONFIRMADO

El chat ITSE está en **loop infinito** donde se envía el mismo mensaje múltiples veces al backend.

### Evidencia de Logs

**Frontend:**
```
📤 Enviando al backend: Object
🔄 Estado actualizado: Object
📤 Enviando al backend: Object
🔄 Estado actualizado: Object
... (se repite infinitamente)
```

**Backend:**
```
🤖 PILI ITSE - Mensaje: SALUD...
📊 Estado: None
🔍 Procesando etapa: inicial, mensaje: SALUD
✅ Resultado: success=True, cotizacion=False
```

---

## ✅ PRUEBA DE CAJA NEGRA

La caja negra `Pili_ChatBot/pili_itse_chatbot.py` **SÍ funciona correctamente**:

```bash
$ python -c "from Pili_ChatBot.pili_itse_chatbot import PILIITSEChatBot; bot = PILIITSEChatBot(); resultado = bot.procesar('SALUD', {'etapa': 'categoria'}); print('Etapa nueva:', resultado['estado']['etapa'])"

✅ Import exitoso
Resultado: True Etapa nueva: tipo
```

**Conclusión:** La lógica de la caja negra es correcta. El problema está en la integración.

---

## 🔍 CAUSA RAÍZ

El problema tiene **2 causas**:

### Causa 1: Estado `null` en el Segundo Click

Cuando el usuario hace click en "Salud":
1. ✅ Primera llamada: `{mensaje: 'SALUD', estado: null}` → Backend devuelve `{etapa: 'categoria'}`
2. ❌ Segunda llamada: `{mensaje: 'SALUD', estado: null}` → Backend devuelve `{etapa: 'categoria'}` (mismo resultado)
3. ❌ Loop infinito

**Por qué `estado` es `null`:**
- React no actualiza `conversationState` inmediatamente después de `setConversationState()`
- Cuando se hace click rápidamente, `conversationState` todavía es `null`

### Causa 2: Múltiples Clicks No Prevenidos

El botón no está deshabilitado durante el procesamiento, permitiendo múltiples clicks.

---

## 💡 SOLUCIÓN DEFINITIVA

### Opción 1: Agregar Debounce y Validación (RECOMENDADO)

Modificar `PiliITSEChat.jsx`:

```javascript
const handleButtonClick = async (value, label) => {
    // Prevenir múltiples clicks
    if (isTyping) {
        console.log('⏸️ Ya hay una petición en curso, ignorando click');
        return;
    }
    
    console.log('🖱️ CLICK EN BOTÓN:', { value, label, estadoActual: conversationState });
    
    addUserMessage(label);
    
    // Esperar un tick para que React actualice el estado
    await new Promise(resolve => setTimeout(resolve, 100));
    
    await enviarMensajeBackend(value);
};
```

**Cambios:**
1. ✅ Verificar `isTyping` antes de procesar
2. ✅ Agregar delay de 100ms para que React actualice el estado
3. ✅ Log para debugging

### Opción 2: Deshabilitar Botones Durante Procesamiento

```javascript
{msg.buttons && (
    <div style={{ marginTop: '15px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
        {msg.buttons.map((btn, btnIndex) => (
            <button
                key={btnIndex}
                onClick={() => handleButtonClick(btn.value, btn.text)}
                disabled={isTyping}  // ✅ AGREGAR ESTA LÍNEA
                style={{
                    background: 'white',
                    color: colors.primary,
                    // ... resto de estilos
                    opacity: isTyping ? 0.5 : 1,  // ✅ AGREGAR ESTA LÍNEA
                    cursor: isTyping ? 'not-allowed' : 'pointer'  // ✅ AGREGAR ESTA LÍNEA
                }}
            >
                {btn.text}
            </button>
        ))}
    </div>
)}
```

### Opción 3: Usar Callback con Estado Actualizado

```javascript
const enviarMensajeBackend = async (mensaje) => {
    setIsTyping(true);

    // Usar función callback para obtener el estado más reciente
    setConversationState(prevState => {
        console.log('📤 Enviando al backend:', { mensaje, conversationState: prevState });
        
        fetch('http://localhost:8000/api/chat/pili-itse', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                mensaje: mensaje,
                conversation_state: prevState  // ✅ Usar prevState en lugar de conversationState
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Actualizar estado
                setConversationState(data.state || data.conversation_state);
                
                // Agregar respuesta
                const botones = data.botones_sugeridos || data.botones || null;
                addBotMessage(data.respuesta, botones);
                
                // Notificar datos generados
                if (data.datos_generados && onDatosGenerados) {
                    onDatosGenerados(data.datos_generados);
                }
                
                // Habilitar botón finalizar
                if (data.cotizacion_generada) {
                    setHasQuote(true);
                    if (onCotizacionGenerada) {
                        onCotizacionGenerada(data.cotizacion_generada);
                    }
                }
            } else {
                addBotMessage('Lo siento, hubo un error. Por favor intenta de nuevo.');
            }
            setIsTyping(false);
        })
        .catch(error => {
            console.error('Error:', error);
            addBotMessage('Error de conexión. Verifica que el backend esté activo.');
            setIsTyping(false);
        });
        
        return prevState;  // No cambiar el estado aquí
    });
};
```

---

## 🎯 RECOMENDACIÓN FINAL

**Implementar Opción 1 + Opción 2:**

1. ✅ Agregar validación `if (isTyping) return` en `handleButtonClick`
2. ✅ Agregar delay de 100ms antes de enviar
3. ✅ Deshabilitar botones cuando `isTyping === true`

**Código completo para `handleButtonClick`:**

```javascript
const handleButtonClick = async (value, label) => {
    // VALIDACIÓN 1: Prevenir múltiples clicks
    if (isTyping) {
        console.log('⏸️ Ya hay una petición en curso, ignorando click');
        return;
    }
    
    console.log('🖱️ CLICK EN BOTÓN:', { value, label, estadoActual: conversationState });
    
    // Agregar mensaje del usuario
    addUserMessage(label);
    
    // VALIDACIÓN 2: Esperar que React actualice el estado
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Enviar al backend
    await enviarMensajeBackend(value);
};
```

**Código completo para botones:**

```javascript
<button
    key={btnIndex}
    onClick={() => handleButtonClick(btn.value, btn.text)}
    disabled={isTyping}
    style={{
        background: 'white',
        color: colors.primary,
        border: `1px solid ${colors.secondary}`,
        padding: '8px 16px',
        borderRadius: '20px',
        cursor: isTyping ? 'not-allowed' : 'pointer',
        fontWeight: '600',
        fontSize: '13px',
        transition: 'all 0.2s',
        boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
        opacity: isTyping ? 0.5 : 1
    }}
>
    {btn.text}
</button>
```

---

## 📋 PRÓXIMOS PASOS

1. ✅ Aplicar cambios en `PiliITSEChat.jsx`
2. ✅ Recargar página (Ctrl+F5)
3. ✅ Probar flujo completo: Salud → Hospital → 600 → 2
4. ✅ Verificar que NO haya loop infinito
5. ✅ Verificar que la cotización se genere correctamente

---

## 🔧 ARCHIVOS A MODIFICAR

### `frontend/src/components/PiliITSEChat.jsx`

**Líneas 88-91:** Reemplazar `handleButtonClick`
**Líneas 253-280:** Agregar `disabled={isTyping}` a botones

---

**Fin del diagnóstico.**
