# 🎯 PLAN DE INTEGRACIÓN: pili_local_specialists.py

## ✅ LÓGICA ACTUAL REVISADA

### **Archivo: `pili_integrator.py` (Líneas clave)**

```python
# LÍNEA 369-407: _generar_respuesta_chat()
async def _generar_respuesta_chat(...):
    # 1. Intentar usar Gemini
    if self.estado_servicios["gemini"] and self.gemini_service:
        try:
            respuesta_gemini = await self.gemini_service.chat_conversacional(...)
            if respuesta_gemini.get("success"):
                return {"texto": ..., "agente": ...}
        except Exception as e:
            logger.warning(f"Error en Gemini, usando fallback: {e}")
    
    # 2. FALLBACK: generar respuesta con PILI Brain
    return self._generar_respuesta_pili_local(mensaje, servicio, agente, datos_acumulados)


# LÍNEA 409-550: _generar_respuesta_pili_local()
def _generar_respuesta_pili_local(...):
    """Genera respuesta guiada por la plantilla del documento editable"""
    
    # Extrae datos del mensaje
    datos_nuevos = self.pili_brain.extraer_datos(mensaje, servicio)
    datos = {**(datos_acumulados or {}), **datos_nuevos}
    
    # Genera respuesta básica (pregunta a pregunta)
    # ... lógica actual simple ...
```

### **Flujo Actual:**
```
Usuario → Chat
    ↓
¿Gemini disponible?
    ├─ SÍ → Gemini responde
    └─ NO → _generar_respuesta_pili_local() (simple, pregunta a pregunta)
```

---

## 🎯 INTEGRACIÓN DEL NUEVO ARCHIVO

### **1. Crear archivo nuevo:**

`backend/app/services/pili_local_specialists.py` (~3000 líneas)

### **2. Modificar `pili_integrator.py`:**

**LÍNEA 44-48 (después de import de gemini_service):**

```python
# Import condicional de Gemini
try:
    from app.services.gemini_service import gemini_service
    GEMINI_DISPONIBLE = True
except ImportError:
    GEMINI_DISPONIBLE = False
    gemini_service = None

# ✅ NUEVO: Import de especialistas locales
try:
    from app.services.pili_local_specialists import process_with_local_specialist
    ESPECIALISTAS_LOCALES_DISPONIBLES = True
except ImportError:
    ESPECIALISTAS_LOCALES_DISPONIBLES = False
    logger.warning("Especialistas locales no disponibles")
```

**LÍNEA 74-80 (en __init__, actualizar estado_servicios):**

```python
# Estado de servicios
self.estado_servicios = {
    "pili_brain": self.pili_brain is not None,
    "word_generator": self.word_generator is not None,
    "pdf_generator": self.pdf_generator is not None,
    "gemini": GEMINI_DISPONIBLE and validate_gemini_key(),
    "plantillas": SERVICIOS_DISPONIBLES,
    "especialistas_locales": ESPECIALISTAS_LOCALES_DISPONIBLES  # ✅ NUEVO
}
```

**LÍNEA 369-407 (reemplazar _generar_respuesta_chat completo):**

```python
async def _generar_respuesta_chat(
    self,
    mensaje: str,
    tipo_flujo: str,
    historial: List[Dict],
    servicio: str,
    datos_acumulados: Optional[Dict] = None
) -> Dict[str, str]:
    """
    Genera respuesta conversacional con sistema de fallback inteligente
    
    ORDEN DE PRIORIDAD:
    1. Gemini (IA de clase mundial) - PRODUCCIÓN
    2. Especialistas Locales (conversación inteligente) - FALLBACK PROFESIONAL
    3. PILI Brain Simple (pregunta a pregunta) - FALLBACK BÁSICO
    """
    
    # Determinar agente PILI
    agentes = {
        "cotizacion-simple": "PILI Cotizadora",
        "cotizacion-compleja": "PILI Analista",
        "proyecto-simple": "PILI Coordinadora",
        "proyecto-complejo": "PILI Project Manager",
        "informe-simple": "PILI Reportera",
        "informe-ejecutivo": "PILI Analista Senior"
    }
    agente = agentes.get(tipo_flujo, "PILI Asistente")
    
    # ═══════════════════════════════════════════════════════════
    # PRIORIDAD 1: Intentar usar Gemini (IA de clase mundial)
    # ═══════════════════════════════════════════════════════════
    if self.estado_servicios["gemini"] and self.gemini_service:
        try:
            logger.info("🚀 Intentando con Gemini (IA clase mundial)...")
            respuesta_gemini = await self.gemini_service.chat_conversacional(
                mensaje=mensaje,
                historial=historial,
                contexto=f"Tipo de servicio: {servicio}, Flujo: {tipo_flujo}"
            )
            if respuesta_gemini.get("success"):
                logger.info("✅ Respuesta generada con Gemini")
                return {
                    "texto": respuesta_gemini.get("respuesta", ""),
                    "agente": agente,
                    "modo": "GEMINI"
                }
        except Exception as e:
            logger.warning(f"⚠️ Gemini no disponible: {e}")
    
    # ═══════════════════════════════════════════════════════════
    # PRIORIDAD 2: Usar Especialistas Locales (conversación inteligente)
    # ═══════════════════════════════════════════════════════════
    if self.estado_servicios["especialistas_locales"]:
        try:
            logger.info("🔄 Usando Especialista Local (fallback profesional)...")
            respuesta_especialista = process_with_local_specialist(
                service_type=servicio,
                message=mensaje,
                conversation_state=datos_acumulados
            )
            
            if respuesta_especialista.get("texto"):
                logger.info("✅ Respuesta generada con Especialista Local")
                return {
                    "texto": respuesta_especialista["texto"],
                    "botones": respuesta_especialista.get("botones"),
                    "agente": agente,
                    "modo": "ESPECIALISTA_LOCAL",
                    "stage": respuesta_especialista.get("stage"),
                    "state": respuesta_especialista.get("state"),
                    "datos_generados": respuesta_especialista.get("datos_generados"),
                    "progreso": respuesta_especialista.get("progreso")
                }
        except Exception as e:
            logger.warning(f"⚠️ Error en Especialista Local: {e}")
    
    # ═══════════════════════════════════════════════════════════
    # PRIORIDAD 3: Fallback básico con PILI Brain simple
    # ═══════════════════════════════════════════════════════════
    logger.info("🔄 Usando PILI Brain simple (fallback básico)...")
    return self._generar_respuesta_pili_local(mensaje, servicio, agente, datos_acumulados)
```

**LÍNEA 338-347 (actualizar _determinar_modo_operacion):**

```python
def _determinar_modo_operacion(self) -> str:
    """Determina el modo de operacion actual"""
    if self.estado_servicios["gemini"]:
        return "ONLINE_GEMINI"
    elif self.estado_servicios["especialistas_locales"]:
        return "OFFLINE_ESPECIALISTAS"  # ✅ NUEVO
    elif self.estado_servicios["pili_brain"]:
        return "OFFLINE_PILI_BRAIN"
    elif self.estado_servicios["plantillas"]:
        return "FALLBACK_PLANTILLAS"
    else:
        return "ERROR_SIN_SERVICIOS"
```

---

## ✅ FLUJO FINAL INTEGRADO

```
Usuario → Chat → pili_integrator._generar_respuesta_chat()
    ↓
┌─────────────────────────────────────────────────────────┐
│ PRIORIDAD 1: ¿Gemini disponible?                       │
├─────────────────────────────────────────────────────────┤
│ SÍ → Gemini responde (IA clase mundial)                │
│ NO → Continuar ↓                                        │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ PRIORIDAD 2: ¿Especialistas Locales disponibles?       │
├─────────────────────────────────────────────────────────┤
│ SÍ → process_with_local_specialist()                   │
│      - Conversación por etapas                          │
│      - Botones dinámicos                                │
│      - Validación inteligente                           │
│      - Cálculo automático                               │
│      - Actualización tiempo real                        │
│ NO → Continuar ↓                                        │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ PRIORIDAD 3: PILI Brain simple (fallback básico)       │
├─────────────────────────────────────────────────────────┤
│ → _generar_respuesta_pili_local()                      │
│   - Pregunta a pregunta simple                          │
│   - Sin botones                                         │
│   - Validación básica                                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 GARANTÍAS DEL SISTEMA

### **1. NUNCA SE DETIENE**
- ✅ Si Gemini falla → Usa Especialistas Locales
- ✅ Si Especialistas fallan → Usa PILI Brain simple
- ✅ Si PILI Brain falla → Usa plantillas modelo
- ✅ **SIEMPRE hay respuesta**

### **2. DEGRADACIÓN ELEGANTE**
```
Gemini (100% calidad)
    ↓ (si falla)
Especialistas Locales (90% calidad)
    ↓ (si falla)
PILI Brain Simple (70% calidad)
    ↓ (si falla)
Plantillas Modelo (50% calidad)
```

### **3. LOGS CLAROS**
```
🚀 Intentando con Gemini...
✅ Respuesta generada con Gemini

⚠️ Gemini no disponible
🔄 Usando Especialista Local...
✅ Respuesta generada con Especialista Local

⚠️ Error en Especialista Local
🔄 Usando PILI Brain simple...
✅ Respuesta generada con PILI Brain
```

---

## 📋 CHECKLIST DE INTEGRACIÓN

- [ ] Crear `pili_local_specialists.py` (~3000 líneas)
- [ ] Agregar import en `pili_integrator.py` (línea 44-48)
- [ ] Actualizar `estado_servicios` (línea 74-80)
- [ ] Reemplazar `_generar_respuesta_chat()` (línea 369-407)
- [ ] Actualizar `_determinar_modo_operacion()` (línea 338-347)
- [ ] Probar flujo completo:
  - [ ] Con Gemini activo
  - [ ] Sin Gemini (fallback a especialistas)
  - [ ] Sin especialistas (fallback a PILI Brain)

---

## 🚀 PRÓXIMO PASO

**¿Procedo a:**
1. Crear `pili_local_specialists.py` con los 10 servicios profesionales
2. Modificar `pili_integrator.py` con la integración exacta

**SÍ o NO?**
