# 🔄 FLUJO COMPLETO: Generación de Documentos Profesionales

## 📋 PROCESO PASO A PASO

---

## ETAPA 1: Conversación con PILI 💬

**Usuario**: Conversa naturalmente con PILI
```
Usuario: "Necesito una cotización para instalación eléctrica en oficina de 150m²"
```

**PILI (IA Inteligente)**:
- 🧠 Extrae información clave de la conversación
- 📊 Identifica tipo de documento (cotización, proyecto, informe)
- 💾 Guarda datos en Base de Datos (ChromaDB)
- 🎯 Auto-rellena campos del documento

**Datos Extraídos**:
```javascript
{
  tipo_documento: "cotizacion-compleja",
  cliente: "Empresa XYZ",
  proyecto: "Instalación Eléctrica Oficinas",
  area_m2: 150,
  items: [
    {descripcion: "Tablero eléctrico", cantidad: 1, precio: 450},
    {descripcion: "Circuitos", cantidad: 6, precio: 120},
    // ... PILI rellena automáticamente
  ],
  cronograma: {
    ingenieria: 5,
    adquisiciones: 7,
    instalacion: 10,
    pruebas: 3
  }
}
```

---

## ETAPA 2: Vista Previa EDITABLE 📝

**HTML Estático → Documento Editable**

**ANTES** (HTML estático):
```html
<p>Cliente: {{CLIENTE_NOMBRE}}</p>
<td>{{DESCRIPCION_ITEM}}</td>
```

**DESPUÉS** (Editable con React):
```jsx
<input 
  value={datos.cliente} 
  onChange={(e) => setDatos({...datos, cliente: e.target.value})}
/>
<textarea 
  value={item.descripcion}
  onChange={(e) => actualizarItem(index, 'descripcion', e.target.value)}
/>
```

**Usuario ve**:
- ✅ Documento profesional con diseño de plantilla HTML
- ✅ Todos los campos EDITABLES inline
- ✅ Datos pre-llenados por PILI
- ✅ Puede corregir, agregar, eliminar información

**Acciones del Usuario**:
```
✏️ Edita "Empresa XYZ" → "Empresa ABC S.A.C."
✏️ Agrega item: "Sistema de puesta a tierra"
✏️ Modifica cantidad de circuitos: 6 → 8
✏️ Corrige área: 150m² → 180m²
```

---

## ETAPA 3: Confirmación y Finalización ✅

**Usuario**: Hace clic en botón **"Finalizar"**

**Sistema**:
- 💾 Guarda datos editados en BD
- 🔄 Prepara vista de personalización
- ➡️ Avanza a siguiente etapa

---

## ETAPA 4: Personalización (Logo y Colores) 🎨

**Vista Previa FINAL con Personalización**

**Usuario ve**:
- 📄 Mismo documento editable (ahora en modo lectura)
- 🎨 Panel lateral de personalización

**Opciones de Personalización**:

1. **Esquema de Colores**:
   - 🔵 Azul Tesla (default)
   - 🔴 Rojo Energía
   - 🟢 Verde Ecológico
   - 🟡 Dorado Premium
   - 🟣 Personalizado

2. **Logo Empresarial**:
   - 📤 Subir logo (PNG, JPG)
   - 🔄 Se convierte a base64
   - 👁️ Vista previa en documento

3. **Fuente**:
   - Calibri (default)
   - Arial
   - Times New Roman

**Cambios en Tiempo Real**:
```
Usuario selecciona: Verde Ecológico
  ↓
Vista previa actualiza INMEDIATAMENTE:
  - Header: Gradiente verde
  - Títulos: Color verde
  - Bordes: Verde
  - Totales: Fondo verde
```

---

## ETAPA 5: Generación Word/PDF 📄

**Usuario**: Hace clic en **"Generar Word"** o **"Generar PDF"**

### Flujo Backend:

```
1. Frontend envía:
   POST /api/generar-documento-v2
   {
     tipo_documento: "cotizacion-compleja",
     datos: {cliente, items, totales, cronograma, ...},
     personalizacion: {
       esquema_colores: "verde-ecologico",
       logo_base64: "data:image/png;base64,iVBOR...",
       fuente: "Calibri"
     }
   }

2. Backend: word_generator_v2.py
   - Detecta tipo: "cotizacion-compleja"
   - Convierte logo base64 → archivo temporal
   - Prepara opciones de personalización

3. Backend: cotizacion_compleja_generator.py
   - Crea Document() con python-docx
   - Aplica colores del esquema verde
   - Inserta logo en header
   - Genera tabla de items
   - Aplica formato profesional
   - Calcula totales
   - Agrega cronograma visual
   - Guarda .docx

4. Si formato = PDF:
   - Convierte .docx → .pdf
   - Usa LibreOffice o similar

5. Frontend:
   - Descarga archivo
   - Usuario recibe documento
```

---

## ✅ RESULTADO FINAL

**Documento Word/PDF Generado**:
- ✅ **IDÉNTICO** a la vista previa
- ✅ Mismo diseño profesional del HTML
- ✅ Colores personalizados aplicados
- ✅ Logo insertado
- ✅ Todos los datos editados por usuario
- ✅ Formato profesional mantenido

---

## 🔄 FLUJO VISUAL COMPLETO

```
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 1: CONVERSACIÓN CON PILI                              │
│                                                              │
│ Usuario: "Necesito cotización para oficina 150m²"           │
│    ↓                                                         │
│ PILI: Extrae info → Guarda en BD → Auto-rellena             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 2: VISTA PREVIA EDITABLE                              │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 🏢 TESLA ELECTRICIDAD                    RUC: 20601...  │ │
│ │ ═══════════════════════════════════════════════════════ │ │
│ │                                                         │ │
│ │        COTIZACIÓN PROFESIONAL                           │ │
│ │        Versión Completa con Ingeniería                  │ │
│ │                                                         │ │
│ │ Cliente: [Empresa ABC S.A.C.] ← EDITABLE                │ │
│ │ Proyecto: [Instalación Eléctrica] ← EDITABLE            │ │
│ │                                                         │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ ITEM │ DESCRIPCIÓN        │ CANT │ P.UNIT │ TOTAL  │ │ │
│ │ ├──────┼────────────────────┼──────┼────────┼────────┤ │ │
│ │ │ 01   │ [Tablero...]  ←EDIT│  1   │  450   │  450   │ │ │
│ │ │ 02   │ [Circuitos...] ←ED │  8   │  120   │  960   │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ │                                                         │ │
│ │ Usuario edita, agrega, modifica...                      │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                              │
│ [Finalizar] ← Usuario hace clic                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 3: PERSONALIZACIÓN                                    │
│                                                              │
│ ┌──────────────────┐  ┌────────────────────────────────┐   │
│ │ PANEL LATERAL    │  │ VISTA PREVIA FINAL             │   │
│ │                  │  │                                │   │
│ │ 🎨 Colores:      │  │ [Documento con colores         │   │
│ │ ○ Azul Tesla     │  │  aplicados en tiempo real]     │   │
│ │ ● Verde Ecológico│  │                                │   │
│ │ ○ Rojo Energía   │  │  - Header verde ✓              │   │
│ │                  │  │  - Títulos verdes ✓            │   │
│ │ 📤 Logo:         │  │  - Totales fondo verde ✓       │   │
│ │ [Subir archivo]  │  │  - Logo insertado ✓            │   │
│ │ [logo.png] ✓     │  │                                │   │
│ │                  │  │                                │   │
│ │ 🔤 Fuente:       │  │                                │   │
│ │ [Calibri ▼]      │  │                                │   │
│ └──────────────────┘  └────────────────────────────────┘   │
│                                                              │
│ [Generar Word] [Generar PDF] ← Usuario hace clic            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 4: GENERACIÓN BACKEND                                 │
│                                                              │
│ Backend recibe:                                              │
│   - Datos editados                                           │
│   - Esquema de colores: verde-ecologico                      │
│   - Logo base64                                              │
│   - Fuente: Calibri                                          │
│                                                              │
│ cotizacion_compleja_generator.py:                            │
│   1. Crea Document()                                         │
│   2. Aplica colores VERDES                                   │
│   3. Inserta LOGO                                            │
│   4. Genera tabla con datos EDITADOS                         │
│   5. Aplica formato PROFESIONAL                              │
│   6. Guarda cotizacion_001.docx                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 5: DESCARGA                                            │
│                                                              │
│ Usuario recibe: cotizacion_001.docx                          │
│                                                              │
│ Documento IDÉNTICO a vista previa:                           │
│   ✅ Colores verdes                                          │
│   ✅ Logo insertado                                          │
│   ✅ Datos editados                                          │
│   ✅ Formato profesional                                     │
│   ✅ Cronograma visual                                       │
│   ✅ Totales calculados                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 COMPONENTES CLAVE

### 1. HTML Template (Estático)
**Ubicación**: `backend/app/templates/documentos/PLANTILLA_HTML_COTIZACION_COMPLEJA.html`
**Propósito**: Diseño profesional base

### 2. Vista Previa Editable (React)
**Componente**: `VistaPreviaProfesional.jsx`
**Propósito**: Convertir HTML estático en editable

### 3. Generador Profesional (Python)
**Archivo**: `cotizacion_compleja_generator.py`
**Propósito**: Generar Word con mismo diseño

---

## ✅ CONFIRMACIÓN

¿Este es el flujo correcto que necesitas implementar?

**SI** → Procedo a convertir HTML a JSX editable  
**NO** → Corrígeme donde me equivoqué
