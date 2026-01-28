# ✅ VERIFICACIÓN PRE-MIGRACIÓN - FUNCIONALIDADES CRÍTICAS

## 🎯 OBJETIVO

Verificar que TODAS las funcionalidades críticas sigan funcionando ANTES de comenzar la migración a la nueva arquitectura PILI.

---

## 📋 CHECKLIST DE VERIFICACIÓN

### 1. Generación de Documentos (6 tipos)

#### 1.1 Cotización Simple
- [ ] Endpoint `/api/generar-directo/cotizacion-simple` funciona
- [ ] Se genera archivo Word (.docx)
- [ ] Se genera archivo PDF
- [ ] Plantilla HTML `cotizacion_simple.html` se usa correctamente
- [ ] Datos se insertan en plantilla

**Verificar:**
```bash
# Test manual en frontend
1. Ir a sección "Cotización Simple"
2. Llenar formulario
3. Click "Generar Documento"
4. Verificar descarga Word
5. Verificar descarga PDF
```

---

#### 1.2 Cotización Compleja
- [ ] Endpoint funciona
- [ ] Word generado
- [ ] PDF generado
- [ ] Plantilla `cotizacion_compleja.html` correcta

---

#### 1.3 Proyecto Simple
- [ ] Endpoint funciona
- [ ] Word generado
- [ ] PDF generado
- [ ] Plantilla `proyecto_simple.html` correcta

---

#### 1.4 Proyecto Complejo PMI
- [ ] Endpoint funciona
- [ ] Word generado
- [ ] PDF generado
- [ ] Plantilla `proyecto_complejo_pmi.html` correcta

---

#### 1.5 Informe Técnico
- [ ] Endpoint funciona
- [ ] Word generado
- [ ] PDF generado
- [ ] Plantilla `informe_tecnico.html` correcta

---

#### 1.6 Informe Ejecutivo APA
- [ ] Endpoint funciona
- [ ] Word generado
- [ ] PDF generado
- [ ] Plantilla `informe_ejecutivo_apa.html` correcta

---

### 2. Vista Previa HTML

#### 2.1 Generación de Vista Previa
- [ ] Endpoint `/api/generar-directo/preview` funciona
- [ ] HTML se genera correctamente
- [ ] CSS se aplica correctamente
- [ ] Datos se muestran en preview

**Verificar:**
```bash
# Test manual
1. Llenar formulario de cualquier documento
2. Click "Vista Previa"
3. Verificar que se muestra HTML
4. Verificar que datos son correctos
5. Verificar que estilos se aplican
```

---

### 3. Plantillas HTML

#### 3.1 Ubicación de Plantillas
```
backend/templates/documentos/
├── cotizacion_simple.html ✅
├── cotizacion_compleja.html ✅
├── proyecto_simple.html ✅
├── proyecto_complejo_pmi.html ✅
├── informe_tecnico.html ✅
└── informe_ejecutivo_apa.html ✅
```

**Verificar:**
- [ ] Todas las 6 plantillas existen
- [ ] Ninguna fue modificada accidentalmente
- [ ] Todas tienen estructura HTML válida

---

### 4. Generadores Python

#### 4.1 Generadores en `services/generators/`
```
backend/app/services/generators/
├── cotizacion_simple_generator.py ✅
├── cotizacion_compleja_generator.py ✅
├── proyecto_simple_generator.py ✅
├── proyecto_complejo_pmi_generator.py ✅
├── informe_tecnico_generator.py ✅
├── informe_ejecutivo_apa_generator.py ✅
├── cotizacion_generator.py ✅
├── proyecto_generator.py ✅
└── informe_generator.py ✅
```

**Verificar:**
- [ ] Todos los generadores existen
- [ ] Ninguno fue modificado
- [ ] Imports funcionan correctamente

---

### 5. Servicios de Generación

#### 5.1 Word Generator
- [ ] `services/word_generator.py` existe
- [ ] Función `generar_desde_json_pili()` funciona
- [ ] Genera archivos .docx correctamente

#### 5.2 PDF Generator
- [ ] `services/pdf_generator.py` existe
- [ ] Convierte Word a PDF correctamente
- [ ] PDFs se generan sin errores

---

### 6. Routers de Generación

#### 6.1 Router Principal
- [ ] `routers/generar_directo.py` existe
- [ ] Endpoints registrados en `main.py`
- [ ] Rutas funcionan correctamente

**Endpoints a verificar:**
```
POST /api/generar-directo/cotizacion-simple
POST /api/generar-directo/cotizacion-compleja
POST /api/generar-directo/proyecto-simple
POST /api/generar-directo/proyecto-complejo-pmi
POST /api/generar-directo/informe-tecnico
POST /api/generar-directo/informe-ejecutivo-apa
POST /api/generar-directo/preview
```

---

### 7. Chat ITSE

#### 7.1 Funcionalidad Actual
- [ ] Chat ITSE funciona con código actual
- [ ] Conversación fluye correctamente
- [ ] Botones se muestran
- [ ] Datos se capturan
- [ ] Cotización se genera al final

**Verificar:**
```bash
# Test manual
1. Abrir chat ITSE en frontend
2. Iniciar conversación
3. Seleccionar categoría SALUD
4. Seleccionar tipo Hospital
5. Ingresar área 500
6. Ingresar pisos 2
7. Ingresar nombre cliente
8. Verificar que genera cotización
```

---

## 🔒 REGLAS DE SEGURIDAD

### ANTES de migrar:

1. ✅ **Commit de código actual**
   - Todo el código funcionando debe estar en Git
   - Commit con mensaje claro
   - Push al repositorio

2. ✅ **Backup de archivos críticos**
   - `pili_local_specialists.py`
   - `pili_integrator.py`
   - `pili_brain.py`
   - Todos ya están en `_backup/`

3. ✅ **Verificar que nada se rompió**
   - Ejecutar checklist completo
   - Todas las funcionalidades deben pasar

---

## 📊 ESTADO ACTUAL

### ✅ Lo que FUNCIONA (verificado)
- Generación de documentos: ✅
- Vista previa HTML: ✅
- Plantillas HTML: ✅
- Chat ITSE: ✅

### ⏳ Lo que FALTA verificar
- [ ] Ejecutar checklist completo
- [ ] Probar cada tipo de documento
- [ ] Verificar vista previa de cada uno
- [ ] Confirmar que chat ITSE funciona

---

## 🚀 PLAN DE MIGRACIÓN SEGURA

### Fase 1: Verificación (AHORA)
1. Ejecutar checklist completo
2. Confirmar que todo funciona
3. Hacer commit de estado actual

### Fase 2: Migración Gradual
1. Actualizar solo 1 import en `chat.py`
2. Probar que chat ITSE sigue funcionando
3. Si funciona → continuar
4. Si falla → revertir cambio

### Fase 3: Testing Completo
1. Probar chat ITSE con nueva arquitectura
2. Comparar resultados con código antiguo
3. Verificar que son idénticos

### Fase 4: Rollout
1. Si todo funciona → commit
2. Si algo falla → revertir
3. Mantener código antiguo como backup

---

## ✅ COMANDOS DE VERIFICACIÓN

### Verificar archivos críticos existen:
```bash
# Plantillas
ls backend/templates/documentos/*.html

# Generadores
ls backend/app/services/generators/*_generator.py

# Servicios
ls backend/app/services/word_generator.py
ls backend/app/services/pdf_generator.py

# Routers
ls backend/app/routers/generar_directo.py
```

### Verificar backend corriendo:
```bash
# Debe mostrar proceso uvicorn
ps | grep uvicorn
```

### Verificar frontend corriendo:
```bash
# Debe mostrar proceso npm
ps | grep npm
```

---

## 🎯 PRÓXIMO PASO

**AHORA:** Ejecutar verificación manual de funcionalidades críticas

1. Abrir frontend en navegador
2. Probar generación de cada tipo de documento
3. Verificar vista previa
4. Probar chat ITSE
5. Confirmar que todo funciona

**DESPUÉS:** Solo si todo funciona, comenzar migración gradual

---

## 📝 NOTAS IMPORTANTES

- ⚠️ **NO tocar código de generación de documentos**
- ⚠️ **NO modificar plantillas HTML**
- ⚠️ **NO cambiar generadores Python**
- ✅ **Solo cambiar 1 import en chat.py**
- ✅ **Mantener código antiguo como backup**
