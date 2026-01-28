# 🔬 DIAGNÓSTICO EXHAUSTIVO - PROBLEMA ITSE

## 📋 SÍNTOMAS OBSERVADOS

**Comportamiento Actual:**
- Usuario inicia chat ITSE
- Usuario escribe "Hola"
- Sistema responde: "¡Excelente! He analizado tu solicitud para **Instalaciones Eléctricas Residenciales**"
- La vista previa muestra "Instalaciones Eléctricas" en lugar de "ITSE"

**Comportamiento Esperado:**
- Sistema debe responder con menú de categorías ITSE (Salud, Educación, etc.)
- Vista previa debe mostrar "Certificado de Inspección Técnica (ITSE)"

---

## 🔍 ANÁLISIS DEL FLUJO COMPLETO

### PASO 1: Frontend (`PiliITSEChat.jsx`)

**Ubicación:** `e:\TESLA_COTIZADOR-V3.0\frontend\src\components\PiliITSEChat.jsx`

**Payload enviado al backend:**
```javascript
{
    tipo_flujo: 'cotizacion-simple',
    mensaje: 'Hola',
    historial: [...],
    contexto_adicional: 'Servicio: itse',  // ← CRÍTICO
    generar_html: true,
    conversation_state: null
}
```

**✅ VERIFICADO:** El frontend SÍ envía `contexto_adicional: 'Servicio: itse'`

---

### PASO 2: Backend Router (`chat.py`)

**Endpoint:** `POST /api/chat/chat-contextualizado`

**Código de detección ITSE:**
```python
servicio_forzado = None
ctx_safe = (contexto_adicional or "").lower()
if "itse" in ctx_safe:
    servicio_forzado = "itse"
    logger.info("🔒 Contexto ITSE detectado: Forzando servicio a 'itse'")
```

**✅ VERIFICADO:** El código está correcto y debería detectar "itse"

**⚠️ PUNTO DE FALLO POTENCIAL:**
- ¿El parámetro `contexto_adicional` realmente llega del frontend?
- ¿FastAPI lo está parseando correctamente?

---

### PASO 3: PILIIntegrator (`pili_integrator.py`)

**Método:** `procesar_solicitud_completa()`

**Flujo de decisión:**
```python
# 0. DETECTAR SERVICIO
servicio = servicio_forzado if servicio_forzado else pili_brain.detectar_servicio(mensaje)

# 1. NIVEL 1: Gemini (APAGADO)
if self.gemini_service and ... and servicio != 'itse':  # ← Bypass ITSE
    # NO SE EJECUTA para ITSE

# 2. NIVEL 2: Nueva Arquitectura
if servicio in SERVICIOS_MIGRADOS:  # ← "itse" está en la lista
    # Intenta UniversalSpecialist
    # Si falla → Nivel 3

# 3. NIVEL 3: Especialistas Locales
if ESPECIALISTAS_LOCALES_DISPONIBLES:
    service_mapping = {"itse": "itse"}  # ← Mapeo correcto
    process_with_local_specialist("itse", ...)
    # Llama a ITSESpecialist

# 4. NIVEL 4: PiliBrain Legacy (FALLBACK FINAL)
# Solo se ejecuta si TODOS los niveles anteriores fallan
```

**⚠️ PUNTOS DE FALLO POTENCIALES:**
1. `servicio_forzado` llega como `None` → `servicio = pili_brain.detectar_servicio("Hola")` → `"electrico-residencial"`
2. Nivel 2 falla silenciosamente → Nivel 3 no se ejecuta
3. Nivel 3 retorna `None` → Cae a Nivel 4 (PiliBrain)

---

### PASO 4: ITSESpecialist (`pili_local_specialists.py`)

**Clase:** `ITSESpecialist`

**Método inicial:**
```python
def _process_itse(self, message: str) -> Dict:
    stage = self.conversation_state["stage"]
    
    if stage == "initial":
        return {
            "texto": """¡Hola! 👋 Soy **Pili**...""",
            "botones": [...categorías...],
            "stage": "initial"
        }
```

**✅ VERIFICADO:** El código está implementado correctamente

---

## 🎯 HIPÓTESIS PRINCIPAL

**El problema está en uno de estos 3 puntos:**

### HIPÓTESIS A: `servicio_forzado` NO llega al integrador
- `chat.py` no detecta "itse" en `contexto_adicional`
- O `contexto_adicional` llega como `None`/vacío desde el frontend

### HIPÓTESIS B: Nivel 2 falla y Nivel 3 no se ejecuta
- `UniversalSpecialist` lanza excepción
- Pero el código de Nivel 3 tiene un bug que impide su ejecución

### HIPÓTESIS C: `ITSESpecialist` retorna `None` o estructura incorrecta
- El método `process_message` no retorna lo esperado
- O `process_with_local_specialist` no maneja bien la respuesta

---

## 🔧 PLAN DE ACCIÓN

### 1. VERIFICAR LOGS DEL BACKEND
Necesitamos ver qué está pasando REALMENTE. Los logs deberían mostrar:
```
🔒 Contexto ITSE detectado: Forzando servicio a 'itse'
🏗️ NIVEL 2: Usando NUEVA ARQUITECTURA para itse
❌ NIVEL 2: Error CRÍTICO...
📚 NIVEL 3: Usando ESPECIALISTAS LOCALES LEGACY para itse
✅ NIVEL 3: Especialistas locales legacy respondieron exitosamente
```

### 2. AGREGAR LOGGING EXHAUSTIVO
Insertar logs en CADA punto crítico para rastrear el flujo exacto

### 3. VERIFICAR RESPUESTA DE `ITSESpecialist`
Asegurar que retorna estructura válida con `texto` y `botones`

---

## 📊 PRÓXIMOS PASOS

1. ✅ Revisar logs del backend (último reinicio)
2. ✅ Agregar logging exhaustivo en puntos críticos **← COMPLETADO**
3. ⏳ **ACCIÓN REQUERIDA:** Probar chat ITSE y capturar logs
4. ⏳ Identificar punto exacto de fallo
5. ⏳ Aplicar fix quirúrgico

---

## 🔧 LOGGING EXHAUSTIVO IMPLEMENTADO

Se han agregado logs **CRÍTICOS** (nivel más alto) en:

### Punto 1: Detección de Servicio Forzado
```python
logger.critical(f"🔒🔒🔒 SERVICIO FORZADO DETECTADO: {servicio} 🔒🔒🔒")
```
**Qué verifica:** Si `servicio_forzado="itse"` llega correctamente desde `chat.py`

### Punto 2: Respuesta de Nivel 3
```python
logger.critical(f"🔍 NIVEL 3: Respuesta recibida: {respuesta}")
```
**Qué verifica:** Qué retorna exactamente `ITSESpecialist.process_message()`

### Punto 3: Éxito o Fallo de Nivel 3
```python
logger.critical("✅✅✅ NIVEL 3: ÉXITO - Retornando respuesta de especialista local ✅✅✅")
# O
logger.critical(f"⚠️⚠️⚠️ NIVEL 3: FALLO - Respuesta inválida o vacía. Cayendo a Nivel 4. Respuesta={respuesta} ⚠️⚠️⚠️")
```
**Qué verifica:** Si la respuesta tiene campo `texto` válido

### Punto 4: Activación de Nivel 4
```python
logger.critical(f"🧠🧠🧠 NIVEL 4: FALLBACK FINAL - Usando PILI BRAIN para servicio={servicio} 🧠🧠🧠")
```
**Qué verifica:** Confirmación de que cayó al fallback legacy

---

## 📋 INSTRUCCIONES PARA EL USUARIO

### Paso 1: Reiniciar Backend
```bash
# Detener el servidor actual (Ctrl+C en la terminal)
# Reiniciar:
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Paso 2: Probar Chat ITSE
1. Abrir navegador en `http://localhost:3001`
2. Ir al Chat ITSE
3. Escribir "Hola"
4. **NO CERRAR LA TERMINAL DEL BACKEND**

### Paso 3: Capturar Logs
Los logs aparecerán en la terminal del backend con formato:
```
🔒🔒🔒 SERVICIO FORZADO DETECTADO: itse 🔒🔒🔒
🔍 NIVEL 3: Respuesta recibida: {...}
✅✅✅ NIVEL 3: ÉXITO ...
```

### Paso 4: Compartir Logs
Copiar los logs que contengan los emojis 🔒, 🔍, ✅ o ⚠️ y compartirlos

---

## 🎯 ESCENARIOS POSIBLES

### Escenario A: NO aparece "🔒🔒🔒 SERVICIO FORZADO"
**Causa:** `servicio_forzado` NO llega desde `chat.py`
**Solución:** Verificar que `PiliITSEChat.jsx` envía `contexto_adicional`

### Escenario B: Aparece "⚠️⚠️⚠️ NIVEL 3: FALLO"
**Causa:** `ITSESpecialist` retorna estructura inválida o vacía
**Solución:** Revisar método `_process_itse` en `pili_local_specialists.py`

### Escenario C: Aparece "🧠🧠🧠 NIVEL 4: FALLBACK FINAL"
**Causa:** Todos los niveles anteriores fallaron
**Solución:** Depende de qué logs aparecieron antes

