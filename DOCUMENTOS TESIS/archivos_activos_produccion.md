# 🔍 ANÁLISIS DE ARCHIVOS ACTIVOS EN PRODUCCIÓN

## 🎯 Objetivo
Identificar qué archivos de `backend/app/services/` están siendo usados activamente para:
1. **Generación de documentos** (Word/PDF)
2. **Vista previa HTML**
3. **Integración con BD**

---

## 📊 ARCHIVOS ACTIVOS (Usados en Routers)

### 1. **Generación de Documentos Word**

#### Archivo: `word_generator.py` ✅ ACTIVO
**Usado en:**
- `cotizaciones.py` línea 22
- `documentos.py` línea 562
- `proyectos.py` línea 407

**Función:** Generación principal de documentos Word

---

#### Archivo: `word_generator_v2.py` ⚠️ USADO PARCIALMENTE
**Usado en:**
- `generar_directo.py` línea 226

**Función:** Versión experimental, solo en endpoint de generación directa

**Decisión:** ⚠️ NO ELIMINAR (se usa en generar_directo.py)

---

### 2. **Generación de Documentos PDF**

#### Archivo: `pdf_generator.py` ✅ ACTIVO
**Usado en:**
- `cotizaciones.py` línea 23
- `documentos.py` línea 664
- `generar_directo.py` línea 164
- `proyectos.py` línea 586

**Función:** Generación principal de PDFs

---

#### Archivo: `pdf_generator_v2.py` ⚠️ USADO PARCIALMENTE
**Usado en:**
- `generar_directo.py` línea 227

**Función:** Versión experimental, solo en endpoint de generación directa

**Decisión:** ⚠️ NO ELIMINAR (se usa en generar_directo.py)

---

### 3. **Generadores Especializados** (Carpeta `generators/`)

#### ✅ TODOS ACTIVOS - Usados en `generar_directo.py`

| Archivo | Línea | Función |
|---------|-------|---------|
| `cotizacion_simple_generator.py` | 112, 334 | Cotización simple |
| `cotizacion_compleja_generator.py` | 118, 325 | Cotización compleja |
| `proyecto_simple_generator.py` | 124, 315 | Proyecto simple |
| `proyecto_complejo_pmi_generator.py` | 130, 307 | Proyecto complejo PMI |
| `informe_tecnico_generator.py` | 139, 296 | Informe técnico |
| `informe_ejecutivo_apa_generator.py` | 146, 287 | Informe ejecutivo APA |

**Decisión:** ✅ MANTENER TODOS (son esenciales para generación de documentos)

---

### 4. **Procesamiento de Plantillas y HTML**

#### Archivo: `template_processor.py` ✅ ACTIVO
**Usado en:**
- `chat.py` líneas 3233, 3294, 3413, 3506
- `proyectos.py` línea 416

**Función:** Procesamiento de plantillas para vista previa HTML

---

#### Archivo: `html_parser.py` ✅ ACTIVO
**Usado en:**
- `generar_directo.py` línea 62

**Función:** Parseo de HTML para conversión

---

#### Archivo: `html_to_word_generator.py` ✅ ACTIVO
**Usado en:**
- `generar_directo.py` línea 105

**Función:** Conversión HTML → Word

---

### 5. **Reportes**

#### Archivo: `report_generator.py` ✅ ACTIVO
**Usado en:**
- `proyectos.py` líneas 339, 545, 685

**Función:** Generación de reportes de proyectos

---

### 6. **Procesamiento de Archivos**

#### Archivo: `file_processor.py` ✅ ACTIVO
**Usado en:**
- `documentos.py` línea 19

**Función:** Procesamiento de archivos subidos

---

### 7. **Lógica de Chat y Servicios**

#### Archivo: `pili_integrator.py` ✅ ACTIVO
**Usado en:**
- `chat.py` línea 48

**Función:** Integrador principal de PILI

---

#### Archivo: `pili_brain.py` ✅ ACTIVO
**Usado en:**
- `chat.py` línea 47

**Función:** Cerebro de PILI (detección de servicios)

---

#### Archivo: `pili_local_specialists.py` ✅ ACTIVO
**Usado en:**
- `chat.py` línea 2894 (bypass ITSE)

**Función:** Especialistas locales (10 servicios)

---

### 8. **Servicios de IA** (Desactivados pero importados)

#### Archivo: `gemini_service.py` ⚠️ IMPORTADO PERO DESACTIVADO
**Usado en:**
- `chat.py` línea 46
- `documentos.py` línea 21

**Función:** Servicio Gemini (desactivado globalmente)

**Decisión:** ⚠️ MANTENER (importado, aunque desactivado)

---

#### Archivo: `rag_service.py` ⚠️ IMPORTADO
**Usado en:**
- `documentos.py` línea 20

**Función:** RAG service

**Decisión:** ⚠️ MANTENER (importado en documentos.py)

---

#### Archivo: `token_manager.py` ⚠️ IMPORTADO
**Usado en:**
- `admin.py` línea 23

**Función:** Gestión de tokens

**Decisión:** ⚠️ MANTENER (usado en admin)

---

#### Archivo: `vector_db.py` ⚠️ IMPORTADO
**Usado en:**
- `generar_directo.py` línea 228

**Función:** Base de datos vectorial

**Decisión:** ⚠️ MANTENER (usado en generar_directo)

---

## ❌ ARCHIVOS NO USADOS (Candidatos a Eliminar)

### 1. Orquestadores Duplicados

| Archivo | Líneas | ¿Usado? | Decisión |
|---------|--------|---------|----------|
| `pili_orchestrator.py` | 489 | ❌ NO | ✅ ELIMINAR |
| `multi_ia_orchestrator.py` | 286 | ❌ NO | ✅ ELIMINAR |
| `multi_ia_service.py` | 372 | ❌ NO | ✅ ELIMINAR |

**Total a eliminar:** 1,147 líneas

---

### 2. Otros Archivos

| Archivo | Líneas | ¿Usado? | Decisión |
|---------|--------|---------|----------|
| `template_renderer.py` | 343 | ❌ NO | ⚠️ VERIFICAR (podría usarse internamente) |
| `pili_template_fields.py` | 190 | ❌ NO | ⚠️ VERIFICAR (podría usarse internamente) |

---

## ✅ RESUMEN - ARCHIVOS A MANTENER (ESENCIALES)

### Generación de Documentos (100% activos)
- ✅ `word_generator.py` (1,058 líneas)
- ✅ `word_generator_v2.py` (530 líneas) - Usado en generar_directo
- ✅ `pdf_generator.py` (712 líneas)
- ✅ `pdf_generator_v2.py` (85 líneas) - Usado en generar_directo
- ✅ `report_generator.py` (692 líneas)
- ✅ `html_to_word_generator.py` (428 líneas)
- ✅ **Carpeta `generators/`** (todos los archivos)

### Procesamiento (100% activos)
- ✅ `template_processor.py` (786 líneas)
- ✅ `html_parser.py` (335 líneas)
- ✅ `file_processor.py` (805 líneas)

### Lógica de Chat (100% activos)
- ✅ `pili_integrator.py` (1,248 líneas)
- ✅ `pili_brain.py` (1,614 líneas)
- ✅ `pili_local_specialists.py` (3,880 líneas)

### Servicios de IA (Importados)
- ⚠️ `gemini_service.py` (963 líneas) - Desactivado pero importado
- ⚠️ `rag_service.py` (228 líneas) - Importado en documentos.py
- ⚠️ `token_manager.py` (223 líneas) - Usado en admin.py
- ⚠️ `vector_db.py` (145 líneas) - Usado en generar_directo.py

---

## ❌ ARCHIVOS SEGUROS PARA ELIMINAR

| Archivo | Líneas | Razón |
|---------|--------|-------|
| `pili_orchestrator.py` | 489 | No importado en ningún router |
| `multi_ia_orchestrator.py` | 286 | No importado en ningún router |
| `multi_ia_service.py` | 372 | No importado en ningún router |

**Total eliminación segura:** 1,147 líneas (8% del total)

---

## ⚠️ ARCHIVOS A VERIFICAR INTERNAMENTE

Estos archivos NO están importados en routers, pero podrían ser usados internamente por otros servicios:

| Archivo | Posible Uso Interno |
|---------|---------------------|
| `template_renderer.py` | Usado por template_processor.py? |
| `pili_template_fields.py` | Usado por pili_integrator.py? |

**Acción:** Verificar imports internos antes de eliminar

---

## 🎯 CONCLUSIÓN CRÍTICA

### ✅ NO TOCAR (Esenciales para funcionalidad actual)

**Generación de Documentos:**
- `word_generator.py` ✅
- `word_generator_v2.py` ✅ (usado en generar_directo)
- `pdf_generator.py` ✅
- `pdf_generator_v2.py` ✅ (usado en generar_directo)
- `generators/` (carpeta completa) ✅

**Vista Previa HTML:**
- `template_processor.py` ✅
- `html_parser.py` ✅
- `html_to_word_generator.py` ✅

**Integración BD:**
- `file_processor.py` ✅
- `report_generator.py` ✅

**Chat PILI:**
- `pili_integrator.py` ✅
- `pili_brain.py` ✅
- `pili_local_specialists.py` ✅

### ❌ ELIMINAR SEGURO (No usados)

- `pili_orchestrator.py` ❌
- `multi_ia_orchestrator.py` ❌
- `multi_ia_service.py` ❌

### ⚠️ MANTENER POR AHORA (Importados aunque no usados activamente)

- `gemini_service.py` (importado en chat.py y documentos.py)
- `rag_service.py` (importado en documentos.py)
- `token_manager.py` (usado en admin.py)
- `vector_db.py` (usado en generar_directo.py)

---

## 📋 RECOMENDACIÓN FINAL

**Reducción conservadora y segura:**

1. **Eliminar SOLO estos 3 archivos:**
   - `pili_orchestrator.py`
   - `multi_ia_orchestrator.py`
   - `multi_ia_service.py`

2. **Ahorro:** 1,147 líneas (8% del total)

3. **Riesgo:** CERO (no están importados en ningún lugar)

4. **Mantener TODO lo demás** hasta confirmar que no se usa internamente

¿Procedo con la eliminación de estos 3 archivos únicamente?
