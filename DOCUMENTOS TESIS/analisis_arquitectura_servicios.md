# 🏗️ ANÁLISIS PROFESIONAL: Arquitectura de Servicios Backend

## 📊 RESUMEN EJECUTIVO

**Total de archivos analizados:** 42 archivos Python
**Servicios principales:** 6 servicios core + 16 servicios auxiliares
**Líneas de código totales:** ~15,000 líneas
**Arquitectura:** Modular con patrón de capas

---

## 🎯 SERVICIOS PRINCIPALES (Core)

### **1. PILIBrain** (`pili_brain.py`)
- **Líneas:** 1,615
- **Función:** Cerebro inteligente 100% offline sin APIs
- **Responsabilidades:**
  - Detectar servicio requerido por el usuario
  - Extraer datos técnicos del mensaje
  - Generar cotizaciones con cálculos realistas
  - Generar proyectos e informes
  - Funcionar como fallback cuando no hay APIs

**Métodos clave:**
```python
detectar_servicio(mensaje: str) -> str
extraer_datos(mensaje: str, servicio: str) -> Dict
generar_cotizacion(mensaje, servicio, complejidad) -> Dict
generar_proyecto(mensaje, servicio, complejidad) -> Dict
generar_informe(mensaje, servicio, complejidad) -> Dict
```

**Servicios que maneja:** 10 servicios eléctricos
- electrico-residencial, electrico-comercial, electrico-industrial
- itse, pozo-tierra, contraincendios
- domotica, cctv, redes, automatizacion

---

### **2. PILIIntegrator** (`pili_integrator.py`)
- **Líneas:** 1,144
- **Función:** Orquestador central que conecta todos los componentes
- **Responsabilidades:**
  - Recibir solicitudes del usuario
  - Generar respuestas conversacionales con fallback de 3 niveles
  - Coordinar PILIBrain, Gemini, Especialistas Locales
  - Generar documentos finales (Word/PDF)
  - Gestionar plantillas y datos

**Sistema de Fallback:**
```
1. Gemini (IA clase mundial) - PRODUCCIÓN
   ↓ si falla
2. Especialistas Locales (conversación inteligente) - FALLBACK PROFESIONAL
   ↓ si falla
3. PILI Brain Simple (pregunta a pregunta) - FALLBACK BÁSICO
```

**Métodos clave:**
```python
procesar_solicitud_completa(mensaje, tipo_flujo, historial, generar_documento, datos_acumulados) -> Dict
_generar_respuesta_chat(mensaje, tipo_flujo, historial, servicio, datos_acumulados) -> Dict
generar_cotizacion(mensaje, servicio, complejidad, formato, logo, opciones) -> Dict
generar_proyecto(...) -> Dict
generar_informe(...) -> Dict
```

---

### **3. GeminiService** (`gemini_service.py`)
- **Líneas:** 963
- **Función:** Integración con Google Gemini AI
- **Responsabilidades:**
  - Procesar solicitudes con IA de clase mundial
  - Generar respuestas contextuales inteligentes
  - Analizar documentos con OCR
  - Búsqueda RAG en proyectos históricos
  - Especialización por agente PILI

**Agentes PILI:**
- PILI Cotizadora (cotizacion-simple)
- PILI Analista (cotizacion-compleja)
- PILI Coordinadora (proyecto-simple)
- PILI Project Manager (proyecto-complejo)
- PILI Reportera (informe-simple)
- PILI Analista Senior (informe-ejecutivo)

**Métodos clave:**
```python
procesar_con_pili(mensaje, tipo_servicio, contexto, historial, datos_archivos) -> Dict
chat_conversacional(mensaje, historial, contexto) -> Dict
analizar_documento(contenido, tipo) -> Dict
buscar_contexto_rag(consulta, tipo_servicio, limite) -> List
```

---

### **4. WordGenerator** (`word_generator.py`)
- **Líneas:** 1,058
- **Función:** Generador profesional de documentos Word
- **Responsabilidades:**
  - Generar documentos .docx desde JSON
  - Aplicar esquemas de colores (azul-tesla, rojo-energia, verde-ecologico)
  - Insertar tablas, imágenes, headers, footers
  - Formatear cotizaciones, proyectos, informes
  - Integración con plantillas profesionales

**Esquemas de colores:**
```python
azul-tesla: #1E3A8A (azul oscuro) + #FFC107 (dorado)
rojo-energia: #8B0000 (rojo oscuro) + #FFC107 (dorado)
verde-ecologico: #065F46 (verde oscuro) + #FFC107 (dorado)
```

**Métodos clave:**
```python
generar_desde_json_pili(datos_json, tipo_documento, opciones, logo, ruta_salida) -> str
_generar_cotizacion_pili(datos, agente, opciones, logo, ruta) -> str
_generar_proyecto_pili(...) -> str
_generar_informe_pili(...) -> str
```

---

### **5. PDFGenerator** (`pdf_generator.py`)
- **Líneas:** 712
- **Función:** Generador profesional de documentos PDF
- **Responsabilidades:**
  - Generar PDFs desde datos estructurados
  - Aplicar colores corporativos Tesla
  - Crear tablas, gráficos, headers, footers
  - Formatear cotizaciones e informes
  - Insertar logos y elementos visuales

**Métodos clave:**
```python
generar_cotizacion(datos, ruta_salida, opciones, logo) -> str
generar_informe_proyecto(datos, ruta_salida, opciones, logo) -> str
generar_informe_simple(datos, ruta_salida) -> str
```

---

### **6. TemplateProcessor** (`template_processor.py`)
- **Líneas:** 786
- **Función:** Procesador de plantillas Word personalizadas
- **Responsabilidades:**
  - Procesar plantillas .docx con marcadores {{variable}}
  - Reemplazar marcadores con datos reales
  - Insertar tablas dinámicas de items
  - Procesar logos e imágenes
  - Validar plantillas

**Marcadores soportados:**
```
{{numero_cotizacion}}, {{fecha}}, {{cliente_nombre}}
{{items_tabla}}, {{logo}}, {{subtotal}}, {{igv}}, {{total}}
```

**Métodos clave:**
```python
procesar_plantilla_con_pili(ruta_plantilla, datos_json, ruta_salida, opciones) -> str
validar_plantilla(ruta_plantilla) -> Dict
extraer_marcadores(ruta_plantilla) -> List
```

---

## 🔗 SERVICIOS AUXILIARES

### **7. pili_local_specialists.py** (3,276 líneas)
- **Función:** Especialistas locales para 10 servicios eléctricos
- **Conversación profesional por etapas**
- **Botones dinámicos y validación en tiempo real**

### **8. pili_template_fields.py** (8,995 bytes)
- **Función:** Mapeo de campos de plantillas
- **Define qué datos necesita cada tipo de documento**

### **9. pili_orchestrator.py** (20,179 bytes)
- **Función:** Orquestador de múltiples IAs
- **Coordina Gemini + otros servicios**

### **10. file_processor.py** (34,744 bytes)
- **Función:** Procesamiento de archivos subidos
- **OCR, extracción de texto, análisis de planos**

### **11. html_parser.py** (13,991 bytes)
- **Función:** Parser de HTML a estructuras de datos**

### **12. template_renderer.py** (12,911 bytes)
- **Función:** Renderizado de plantillas HTML**

### **13. report_generator.py** (29,084 bytes)
- **Función:** Generador especializado de informes**

### **14-16. Servicios RAG:**
- `rag_service.py` (7,976 bytes)
- `vector_db.py` (5,582 bytes)
- `token_manager.py` (8,512 bytes)

---

## 📁 CARPETAS ESPECIALIZADAS

### **generators/** (9 archivos)
- `base_generator.py` - Clase base para generadores
- `cotizacion_simple_generator.py` - Generador cotización simple
- `cotizacion_compleja_generator.py` - Generador cotización compleja
- `proyecto_simple_generator.py` - Generador proyecto simple
- `proyecto_complejo_pmi_generator.py` - Generador proyecto PMI
- `informe_tecnico_generator.py` - Generador informe técnico
- `informe_ejecutivo_apa_generator.py` - Generador informe APA
- `pdf_converter.py` - Convertidor a PDF

### **professional/** (11 archivos)
- `charts/chart_engine.py` - Motor de gráficos
- `generators/document_generator_pro.py` - Generador profesional
- `ml/ml_engine.py` - Motor de machine learning
- `processors/file_processor_pro.py` - Procesador profesional
- `rag/rag_engine.py` - Motor RAG profesional

---

## 🔄 FLUJO DE DATOS COMPLETO

```
┌─────────────────────────────────────────────────────────────┐
│  USUARIO envía mensaje desde Frontend                       │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  ROUTER (chat.py) recibe solicitud                          │
│  - Llama a PILIIntegrator.procesar_solicitud_completa()     │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  PILIIntegrator orquesta el flujo                           │
│  1. Detecta servicio con PILIBrain.detectar_servicio()      │
│  2. Genera respuesta con _generar_respuesta_chat()          │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  FALLBACK NIVEL 1: Intenta con Gemini                       │
│  - GeminiService.chat_conversacional()                      │
│  - Si funciona → Retorna respuesta IA                       │
│  - Si falla → Continúa a Nivel 2                            │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  FALLBACK NIVEL 2: Especialistas Locales                    │
│  - process_with_local_specialist()                          │
│  - Conversación profesional por etapas                      │
│  - Botones dinámicos                                        │
│  - Si funciona → Retorna respuesta + botones                │
│  - Si falla → Continúa a Nivel 3                            │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  FALLBACK NIVEL 3: PILI Brain Simple                        │
│  - PILIBrain.extraer_datos()                                │
│  - PILIBrain.generar_cotizacion()                           │
│  - Pregunta a pregunta básico                               │
│  - Siempre funciona (offline)                               │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  GENERACIÓN DE DOCUMENTO (si se solicita)                   │
│  1. PILIIntegrator._generar_json_estructurado()             │
│  2. PILIIntegrator._generar_documento_final()               │
│     - WordGenerator.generar_desde_json_pili() → .docx       │
│     - PDFGenerator.generar_cotizacion() → .pdf              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  RETORNO AL FRONTEND                                        │
│  - Respuesta conversacional                                 │
│  - Botones (si hay)                                         │
│  - Datos generados (si hay)                                 │
│  - Documento (si se generó)                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 ANÁLISIS PARA IMPLEMENTACIÓN PILI ITSE

### **Archivos que DEBEMOS modificar:**

#### **1. pili_local_specialists.py** (CRÍTICO)
**Modificación:** Mejorar `ITSESpecialist._process_itse()`
- Agregar presentación profesional
- Agregar confirmaciones en cada etapa
- Mejorar cotización visual
- Agregar llamados a la acción

**Impacto:** ALTO - Es el corazón de la conversación

#### **2. App.jsx** (Frontend - CRÍTICO)
**Modificación:** Sincronizar datos del cliente
```javascript
// Después de recibir respuesta de PILI
if (respuesta.datos_generados) {
  setDatosEditables(prev => ({
    ...prev,
    cliente: datosCliente,  // ← Sincronizar
    ...respuesta.datos_generados
  }));
  setTieneCotizacion(true);
}
```

**Impacto:** ALTO - Conecta datos con vista previa

### **Archivos que NO necesitamos modificar:**

- ✅ PILIBrain - Ya funciona bien
- ✅ PILIIntegrator - Ya tiene el fallback correcto
- ✅ GeminiService - Funciona independientemente
- ✅ WordGenerator - Genera documentos correctamente
- ✅ PDFGenerator - Genera PDFs correctamente
- ✅ TemplateProcessor - Procesa plantillas correctamente

---

## 📋 DEPENDENCIAS ENTRE SERVICIOS

```
PILIIntegrator (orquestador central)
├── PILIBrain (detección + extracción + generación)
├── GeminiService (IA opcional)
├── pili_local_specialists (conversación profesional)
├── WordGenerator (generación Word)
│   └── TemplateProcessor (plantillas)
├── PDFGenerator (generación PDF)
└── pili_template_fields (mapeo de campos)

GeminiService
├── rag_service (búsqueda histórica)
└── vector_db (almacenamiento vectorial)

WordGenerator
└── generators/ (generadores especializados)
    ├── cotizacion_simple_generator
    ├── cotizacion_compleja_generator
    ├── proyecto_simple_generator
    └── ...

file_processor
├── html_parser (parsing HTML)
└── professional/processors/file_processor_pro
```

---

## ✅ RECOMENDACIONES FINALES

### **Para implementar PILI ITSE profesional:**

1. **MODIFICAR SOLO 2 ARCHIVOS:**
   - `pili_local_specialists.py` (backend)
   - `App.jsx` (frontend)

2. **NO TOCAR:**
   - PILIBrain
   - PILIIntegrator
   - GeminiService
   - Generadores

3. **ESTRATEGIA:**
   - Mejorar mensajes de ITSESpecialist
   - Sincronizar datos del cliente en frontend
   - Probar flujo completo
   - Replicar a otros 9 servicios si funciona

4. **TIEMPO ESTIMADO:**
   - 2-3 horas de modificación
   - 30 minutos de pruebas
   - Bajo riesgo

---

## 🎯 CONCLUSIÓN

**Arquitectura actual:** Sólida, modular, bien organizada

**Problema identificado:** Solo necesita mejorar la PRESENTACIÓN de mensajes en especialistas locales

**Solución:** Modificación incremental en lugar de reescritura completa

**Beneficio:** Experiencia profesional como el artefacto ITSE sin romper lo que funciona

**Riesgo:** Bajo - Solo modificamos strings de mensajes

---

**¿Procedemos con la modificación de ITSESpecialist?**
