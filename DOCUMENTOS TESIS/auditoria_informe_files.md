# 📋 Auditoría Completa: Archivos de Informe

## 🎯 Objetivo
Verificar el estado actual de todos los archivos relacionados con informes antes de renombrar `informe-tecnico` → `informe-simple`.

---

## 📁 Archivos Encontrados

### Frontend (React Components)
1. ✅ `EDITABLE_INFORME_TECNICO.jsx` - **A RENOMBRAR**
2. ✅ `EDITABLE_INFORME_EJECUTIVO.jsx` - **NO TOCAR**
3. ❓ `EDITABLE_INFORME_EJECUTIVO_COMPLETE.jsx` - **INVESTIGAR** (posible duplicado)

### Backend (Python Generators)
1. ✅ `informe_tecnico_generator.py` - **A RENOMBRAR**
2. ✅ `informe_ejecutivo_apa_generator.py` - **NO TOCAR**

---

## 🔍 Estado Actual de Archivos

### 1. Backend: `informe_tecnico_generator.py`

**Ubicación:** `backend/app/services/generators/informe_tecnico_generator.py`

**Estado:**
- ✅ Tiene encoding UTF-8 (`# -*- coding: utf-8 -*-`)
- ✅ Hereda de `BaseDocumentGenerator`
- ✅ Clase: `InformeTecnicoGenerator`
- ✅ Función de entrada: `generar_informe_tecnico(datos, ruta_salida, opciones=None)`

**Extracción de Cliente (líneas 56-57):**
```python
cliente_data = self.datos.get('cliente', {})
cliente = cliente_data.get('nombre', 'Cliente') if isinstance(cliente_data, dict) else str(cliente_data)
```
✅ **Correcto:** Extrae `cliente.nombre` del dict

**Secciones del Documento:**
- `_agregar_titulo()` - Título "INFORME TÉCNICO"
- `_agregar_info_general()` - Datos del cliente e informe
- `_agregar_resumen_ejecutivo()` - Resumen
- `_agregar_introduccion()` - Introducción
- `_agregar_analisis_tecnico()` - Análisis técnico
- `_agregar_resultados()` - Resultados
- `_agregar_conclusiones()` - Conclusiones
- `_agregar_recomendaciones()` - Recomendaciones

**Método generar():**
```python
def generar(self, ruta_salida):
    """Genera el documento completo"""
    self._agregar_header_basico()
    self._agregar_titulo()
    self._agregar_info_general()
    self._agregar_resumen_ejecutivo()
    self._agregar_introduccion()
    self._agregar_analisis_tecnico()
    self._agregar_resultados()
    self._agregar_conclusiones()
    self._agregar_recomendaciones()
    self._agregar_footer_basico()
    
    self.doc.save(str(ruta_salida))
    return ruta_salida
```

**Función de entrada:**
```python
def generar_informe_tecnico(datos, ruta_salida, opciones=None):
    """Función de entrada para generar informe técnico"""
    generator = InformeTecnicoGenerator(datos, opciones)
    return generator.generar(ruta_salida)
```

---

### 2. Backend: `html_to_word_generator.py`

**Ubicación:** `backend/app/services/html_to_word_generator.py`

**Método actual (líneas 352-380):**
```python
def generar_informe_tecnico(
    self,
    datos: Dict[str, Any],
    ruta_salida: Optional[Path] = None
) -> Path:
    """
    Generar informe técnico en Word
    """
    logger.info("🔄 Generando informe técnico...")

    html = self._cargar_plantilla("informe_tecnico")

    datos_completos = {
        "TITULO_INFORME": datos.get("titulo", "Informe Técnico Demo"),
        "CODIGO_INFORME": datos.get("codigo", "INF-000000"),
        "CLIENTE": self._extraer_nombre_cliente(datos.get("cliente")),
        "FECHA": datos.get("fecha", datetime.now().strftime("%d/%m/%Y")),
        "RESUMEN_EJECUTIVO": datos.get("resumen", "Resumen ejecutivo del informe técnico"),
        "SERVICIO_NOMBRE": datos.get("servicio_nombre", "Servicio Técnico"),
        "NORMATIVA_APLICABLE": datos.get("normativa", "CNE Suministro 2011")
    }

    html_procesado = self._reemplazar_variables(html, datos_completos)

    if ruta_salida is None:
        ruta_salida = Path("storage/generados") / f"INFORME_TECNICO_{datos_completos['CODIGO_INFORME']}.docx"

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    return self._convertir_html_a_word(html_procesado, ruta_salida)
```

**Estado:**
- ✅ Extrae `cliente.nombre` correctamente con `_extraer_nombre_cliente()`
- ✅ Usa código "INF-..." por defecto
- ⚠️ **Nombre del método:** `generar_informe_tecnico` - **A RENOMBRAR**

---

### 3. Backend: `generar_directo.py`

**Condición actual (línea 131):**
```python
elif "informe-tecnico" in tipo_plantilla or "informe-simple" in tipo_plantilla:
    ruta_generada = html_to_word_generator.generar_informe_tecnico(
        datos=datos,
        ruta_salida=filepath
    )
```

**Estado:**
- ⚠️ Acepta AMBOS nombres: `informe-tecnico` y `informe-simple`
- ⚠️ Llama a `generar_informe_tecnico()` - **A ACTUALIZAR**

---

### 4. Frontend: `VistaPreviaProfesional.jsx`

**Import actual:**
```javascript
import EDITABLE_INFORME_TECNICO from './EDITABLE_INFORME_TECNICO';
```

**Condición actual (línea 122):**
```javascript
if (tipoDocumento === 'informe-tecnico' || tipoDocumento === 'informe-simple') {
  console.log('✅ Renderizando EDITABLE_INFORME_TECNICO');
  return (
    <EDITABLE_INFORME_TECNICO
      datos={datosEditables}
      esquemaColores={esquemaColores}
      logoBase64={logoBase64}
      fuenteDocumento={fuenteDocumento}
      onDatosChange={handleDatosChange}
    />
  );
}
```

**Estado:**
- ⚠️ Acepta AMBOS nombres: `informe-tecnico` y `informe-simple`
- ⚠️ Usa componente `EDITABLE_INFORME_TECNICO` - **A RENOMBRAR**

---

### 5. Frontend: `App.jsx`

**Estructura de datos para informes (líneas 449-466):**
```javascript
if (tipoDocumento === 'informe') {
  // Estructura para INFORMES
  datosParaEnviar = {
    tipo_documento: tipoDocumento,
    titulo: entidad.titulo || "Informe Técnico",
    codigo: entidad.codigo || `INF-${Date.now()}`,
    cliente: entidad.cliente || { nombre: "[Cliente]" },
    fecha: entidad.fecha || new Date().toLocaleDateString('es-PE'),
    resumen: entidad.resumen || entidad.resumen_ejecutivo || "",
    introduccion: entidad.introduccion || "",
    analisis_tecnico: entidad.analisis_tecnico || "",
    resultados: entidad.resultados || "",
    conclusiones: entidad.conclusiones || "",
    recomendaciones: entidad.recomendaciones || [],
    normativa: entidad.normativa || "CNE Suministro 2011"
  };
}
```

**Estado:**
- ✅ Estructura correcta para informes
- ✅ Usa código "INF-..." por defecto
- ✅ NO necesita cambios (usa `tipoDocumento === 'informe'`)

---

## ✅ Verificación de Correcciones Previas

### UTF-8 Encoding
- ✅ `informe_tecnico_generator.py` tiene `# -*- coding: utf-8 -*-`
- ✅ `informe_ejecutivo_apa_generator.py` tiene `# -*- coding: utf-8 -*-`

### Extracción de Cliente
- ✅ `informe_tecnico_generator.py` extrae `cliente.nombre` correctamente (líneas 56-57)
- ✅ `html_to_word_generator.py` usa `_extraer_nombre_cliente()` (línea 367)

---

## 📝 Plan de Renombrado Seguro

### Paso 1: Renombrar Generador Python
**Archivo:** `informe_tecnico_generator.py` → `informe_simple_generator.py`

**Cambios internos:**
```python
# Clase
class InformeTecnicoGenerator → class InformeSimpleGenerator

# Función de entrada
def generar_informe_tecnico(...) → def generar_informe_simple(...)

# Docstrings
"Generador de Informe Técnico" → "Generador de Informe Simple"
```

### Paso 2: Actualizar `html_to_word_generator.py`
**Línea 352:**
```python
# Antes
def generar_informe_tecnico(self, datos, ruta_salida=None):

# Después
def generar_informe_simple(self, datos, ruta_salida=None):
```

**Línea 360:**
```python
# Antes
logger.info("🔄 Generando informe técnico...")

# Después
logger.info("🔄 Generando informe simple...")
```

**Línea 362:**
```python
# Antes
html = self._cargar_plantilla("informe_tecnico")

# Después
html = self._cargar_plantilla("informe_simple")
```

**Línea 365:**
```python
# Antes
"TITULO_INFORME": datos.get("titulo", "Informe Técnico Demo"),

# Después
"TITULO_INFORME": datos.get("titulo", "Informe Simple Demo"),
```

### Paso 3: Actualizar `generar_directo.py`
**Línea 131:**
```python
# Antes
elif "informe-tecnico" in tipo_plantilla or "informe-simple" in tipo_plantilla:
    ruta_generada = html_to_word_generator.generar_informe_tecnico(...)

# Después
elif "informe-simple" in tipo_plantilla:
    ruta_generada = html_to_word_generator.generar_informe_simple(...)
```

### Paso 4: Renombrar Componente React
**Archivo:** `EDITABLE_INFORME_TECNICO.jsx` → `EDITABLE_INFORME_SIMPLE.jsx`

**Cambios internos:**
```javascript
// Nombre del componente
const EDITABLE_INFORME_TECNICO → const EDITABLE_INFORME_SIMPLE

// Export
export default EDITABLE_INFORME_TECNICO → export default EDITABLE_INFORME_SIMPLE
```

### Paso 5: Actualizar `VistaPreviaProfesional.jsx`
**Línea 9:**
```javascript
// Antes
import EDITABLE_INFORME_TECNICO from './EDITABLE_INFORME_TECNICO';

// Después
import EDITABLE_INFORME_SIMPLE from './EDITABLE_INFORME_SIMPLE';
```

**Línea 122:**
```javascript
// Antes
if (tipoDocumento === 'informe-tecnico' || tipoDocumento === 'informe-simple') {
  return <EDITABLE_INFORME_TECNICO ... />

// Después
if (tipoDocumento === 'informe-simple') {
  return <EDITABLE_INFORME_SIMPLE ... />
```

---

## ⚠️ Archivos que NO se Tocan

1. ✅ `EDITABLE_INFORME_EJECUTIVO.jsx` - Es un tipo diferente (APA)
2. ✅ `informe_ejecutivo_apa_generator.py` - Es un tipo diferente (APA)
3. ❓ `EDITABLE_INFORME_EJECUTIVO_COMPLETE.jsx` - Investigar si es duplicado

---

## ✅ Checklist de Seguridad

Antes de renombrar, verificar:
- [x] `informe_tecnico_generator.py` tiene UTF-8
- [x] `informe_tecnico_generator.py` extrae cliente correctamente
- [x] `html_to_word_generator.py` usa `_extraer_nombre_cliente()`
- [x] `App.jsx` envía estructura correcta para informes
- [x] No hay otros archivos que importen `informe_tecnico_generator`
- [ ] Verificar si hay tests que usen `generar_informe_tecnico()`
- [ ] Verificar si hay otros routers que usen `informe-tecnico`

---

## 🎯 Resultado Esperado

**Antes del renombrado:**
- Frontend: `informe-simple` → Backend: `informe-tecnico` ❌ Inconsistente

**Después del renombrado:**
- Frontend: `informe-simple` → Backend: `informe-simple` ✅ Consistente
