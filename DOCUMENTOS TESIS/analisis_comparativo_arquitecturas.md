# 📊 ANÁLISIS COMPARATIVO: Arquitectura Antigua vs Nueva

## 🎯 OBJETIVO

Identificar por qué la refactorización modular NO funciona completamente, comparando:
- **Arquitectura Antigua:** 11 archivos que FUNCIONAN
- **Arquitectura Nueva:** Carpeta `pili/` que NO funciona completamente

---

## 📁 PARTE 1: LOS 11 ARCHIVOS ANTIGUOS (QUE FUNCIONAN)

### 1. `chat.py` (Router Principal)
**Ubicación:** `backend/app/routers/chat.py`
**Líneas:** ~4,639
**Funcionalidad:**
- ✅ Endpoint `/chat-contextualizado` (línea 2831)
- ✅ Detección de `tipo_flujo == 'itse'` (línea 2894)
- ✅ Bypass directo a `LocalSpecialistFactory` (línea 2897-2921)
- ✅ Retorna `cotizacion_generada`, `datos_generados`, `html_preview`
- ✅ Maneja 10 servicios con botones contextuales (línea 92-102)

**Estado:** ✅ FUNCIONA - Es el orquestador principal

---

### 2. `pili_integrator.py` (Orquestador Multi-IA)
**Ubicación:** `backend/app/services/pili_integrator.py`
**Líneas:** ~700
**Funcionalidad:**
- ✅ Sistema Multi-IA con fallback (Gemini → Claude → GPT-4 → PILIBrain)
- ✅ Generación de respuestas conversacionales
- ✅ Detección de servicios
- ✅ Generación de JSON estructurado
- ✅ Creación de documentos Word/PDF
- ✅ Vista previa HTML editable

**Estado:** ⚠️ PARCIALMENTE USADO - Solo para otros servicios, NO para ITSE

---

### 3. `pili_brain.py` (Fallback Local)
**Ubicación:** `backend/app/services/pili_brain.py`
**Líneas:** ~500
**Funcionalidad:**
- ✅ Respuestas profesionales sin IA
- ✅ Extracción de datos de mensajes
- ✅ Detección de servicios
- ✅ Plantillas de respuesta
- ✅ Cálculos básicos

**Estado:** ⚠️ PARCIALMENTE USADO - Fallback cuando Gemini falla

---

### 4. `pili_local_specialists.py` (Especialistas por Servicio)
**Ubicación:** `backend/app/services/pili_local_specialists.py`
**Líneas:** ~3,881
**Funcionalidad:**
- ✅ 10 especialistas (ITSE, Electricidad, Pozo Tierra, etc.)
- ✅ Conocimiento base detallado por servicio
- ✅ Plantillas de respuesta especializadas
- ✅ Cálculos específicos por servicio
- ✅ Flujos conversacionales

**Estado:** ⚠️ NO USADO PARA ITSE - Reemplazado por nueva arquitectura

---

### 5. `pili_template_fields.py` (Campos de Plantillas)
**Ubicación:** `backend/app/services/pili_template_fields.py`
**Líneas:** ~8,995
**Funcionalidad:**
- ✅ Definición de campos para cada tipo de documento
- ✅ Validaciones de campos
- ✅ Valores por defecto
- ✅ Mapeo de datos a plantillas Word

**Estado:** ✅ USADO - Para generación de documentos

---

### 6-11. **Archivos de Generación de Documentos**

#### 6. `document_generators/cotizacion_generator.py`
- ✅ Genera cotizaciones Word/PDF
- ✅ Aplica estilos y formato
- ✅ Inserta tablas y cálculos

#### 7. `document_generators/proyecto_generator.py`
- ✅ Genera proyectos con Gantt
- ✅ Cronogramas y entregables

#### 8. `document_generators/informe_generator.py`
- ✅ Genera informes técnicos
- ✅ Formato APA

#### 9. `document_generators/base_generator.py`
- ✅ Clase base para todos los generadores
- ✅ Funciones comunes de formato

#### 10. `utils/word_utils.py`
- ✅ Utilidades para manipular Word
- ✅ Estilos, tablas, imágenes

#### 11. `utils/pdf_utils.py`
- ✅ Conversión Word → PDF
- ✅ Optimización de PDFs

**Estado:** ✅ TODOS FUNCIONAN - Generación de documentos OK

---

## 📁 PARTE 2: NUEVA ARQUITECTURA MODULAR `pili/`

### Estructura Creada:
```
pili/
├── core/
│   ├── config_loader.py          # ✅ Carga YAMLs
│   ├── multi_ia_manager.py       # ✅ Multi-IA (Gemini, Claude, GPT-4)
│   ├── fallback_manager.py       # ✅ Gestión de fallbacks
│   └── __init__.py
├── specialists/
│   ├── universal_specialist.py   # ⚠️ PROBLEMA AQUÍ
│   ├── specialist_factory.py     # ✅ Factory pattern
│   └── __init__.py
├── adapters/
│   └── legacy_adapter.py         # ✅ Adaptador para compatibilidad
├── utils/
│   ├── validators.py             # ✅ Validaciones
│   ├── formatters.py             # ✅ Formateo
│   └── calculators.py            # ⚠️ PROBLEMA AQUÍ
├── config/
│   └── itse.yaml                 # ✅ Configuración ITSE
└── knowledge/
    └── (vacío - pendiente)
```

---

## 🔴 PARTE 3: PROBLEMAS IDENTIFICADOS

### Problema 1: `universal_specialist.py` NO ejecuta calculadora
**Código actual (líneas 318-359):**
```python
def _process_quote_stage(self, stage: Dict, message: str) -> Dict:
    try:
        from ..utils import calculate_itse_quote
        data = self.conversation_state.get('data', {})
        quote_data = calculate_itse_quote(data)  # ← FALLA AQUÍ
        mensaje = self._render_message_with_data('cotizacion', quote_data)
        return {'texto': mensaje, 'cotizacion_generada': True}
    except Exception as e:
        return {'texto': f'Error: {str(e)}'}  # ← RETORNA ESTO
```

**Problema:** La excepción se ejecuta pero NO se loguea el error real.

---

### Problema 2: `calculators.py` NO tiene logging
**Código actual (líneas 90-195):**
```python
def calculate_itse_quote(data: Dict[str, Any]) -> Dict[str, Any]:
    import yaml
    config_path = Path(__file__).parent.parent / 'config' / 'itse.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    # ... resto del código
```

**Problema:** Si falla, NO sabemos por qué (falta logging).

---

### Problema 3: Datos NO se pasan correctamente
**Frontend envía:**
```javascript
conversation_state: {
    stage: 'area',
    data: {
        categoria: 'SALUD',
        tipo: 'Hospital',
        area: 60,
        pisos: 2
    }
}
```

**Backend recibe pero NO usa:**
- `UniversalSpecialist` SÍ restaura estado (línea 116-130)
- Pero calculadora recibe `data` vacío o incompleto

---

## ✅ PARTE 4: FUNCIONALIDADES QUE SÍ FUNCIONAN

1. ✅ **Conversación ITSE** - Flujo de preguntas OK
2. ✅ **10 servicios** - Botones contextuales OK
3. ✅ **Estado de conversación** - Se mantiene entre mensajes
4. ✅ **Singleton pattern** - No se reinicia el especialista
5. ✅ **Integración Gemini** - Respuestas inteligentes OK

---

## ❌ PARTE 5: FUNCIONALIDADES QUE NO FUNCIONAN

1. ❌ **Cálculo de cotización** - Calculadora falla silenciosamente
2. ❌ **Vista previa** - Muestra placeholders sin reemplazar
3. ❌ **Botón Finalizar** - No se habilita (`cotizacion_generada: false`)
4. ❌ **Generación de documento** - No se puede generar Word/PDF
5. ❌ **Logging de errores** - No sabemos qué falla exactamente

---

## 🎯 PARTE 6: PLAN DE ACCIÓN

### Paso 1: Agregar Logging Exhaustivo
```python
# En calculators.py
import logging
logger = logging.getLogger(__name__)

def calculate_itse_quote(data: Dict[str, Any]) -> Dict[str, Any]:
    logger.info(f"🧮 INICIO calculate_itse_quote")
    logger.info(f"📊 Datos recibidos: {data}")
    
    try:
        # ... código existente ...
        logger.info(f"✅ Cotización calculada: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ ERROR en calculadora: {e}", exc_info=True)
        raise
```

### Paso 2: Verificar Paso de Datos
```python
# En universal_specialist.py
def _process_quote_stage(self, stage: Dict, message: str) -> Dict:
    data = self.conversation_state.get('data', {})
    logger.info(f"📦 Datos para calculadora: {data}")
    logger.info(f"🔑 Keys disponibles: {list(data.keys())}")
    
    if not data:
        logger.error("❌ conversation_state.data está VACÍO")
```

### Paso 3: Comparar con Arquitectura Antigua
- Revisar cómo `pili_local_specialists.py` hace cálculos
- Copiar lógica que funciona
- Adaptar a nueva arquitectura

---

## 📋 PRÓXIMOS PASOS INMEDIATOS

1. **Agregar logging a calculadora** ← PRIMERO
2. **Probar flujo ITSE completo** ← Ver logs
3. **Identificar error exacto** ← Basado en logs
4. **Corregir error** ← Según diagnóstico
5. **Verificar integración completa** ← Prueba E2E

---

## 🔍 CONCLUSIÓN PRELIMINAR

**Hipótesis:** La calculadora ITSE está fallando por:
1. Datos incompletos (`data` vacío o sin keys necesarias)
2. Error en carga de YAML (ruta incorrecta o permisos)
3. Error en lógica de cálculo de riesgo
4. Excepción silenciosa que no se loguea

**Solución:** Agregar logging exhaustivo para identificar causa raíz.
