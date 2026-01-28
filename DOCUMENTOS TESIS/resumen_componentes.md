# 📋 RESUMEN: 6 Componentes Editables

## ✅ 1. EDITABLE_COTIZACION_SIMPLE.jsx - COMPLETADO

**Secciones**:
- Header (logo + empresa)
- Título + número
- Datos cliente + cotización
- Tabla items (editable)
- Totales (auto-calculados)
- Observaciones
- Footer

**Campos Editables**:
- `numero`, `cliente.nombre`, `proyecto`, `area_m2`, `vigencia`, `servicio`
- `items[]`: `descripcion`, `cantidad`, `unidad`, `precio_unitario`

---

## 🔄 2. EDITABLE_COTIZACION_COMPLEJA.jsx - EN PROGRESO

**Secciones Adicionales** (vs Simple):
- ✅ Alcance del Proyecto (textarea editable)
- ✅ Cronograma Estimado (4 fases: Ingeniería, Adquisiciones, Instalación, Pruebas)
- ✅ Garantías (grid 3 columnas)
- ✅ Condiciones de Pago (lista)

**Campos Editables Adicionales**:
- `descripcion_proyecto` (textarea)
- `normativa_aplicable`
- `cronograma.dias_ingenieria`, `dias_adquisiciones`, `dias_instalacion`, `dias_pruebas`

---

## 🔄 3. EDITABLE_PROYECTO_SIMPLE.jsx - PENDIENTE

**Secciones Únicas**:
- Resumen del Proyecto (textarea)
- Fases del Proyecto (lista editable)
- Cronograma (fecha inicio, fin, duración)
- Recursos (humanos, materiales)
- Entregables

**Campos Editables**:
- `resumen`
- `fases[]`: `descripcion`, `duracion`, `responsable`
- `cronograma.fecha_inicio`, `fecha_fin`, `duracion_total`
- `recursos.humanos[]`, `recursos.materiales[]`

---

## 🔄 4. EDITABLE_PROYECTO_COMPLEJO.jsx - PENDIENTE

**Secciones Únicas** (PMI):
- Métricas PMI (alcance, tiempo, costo, calidad)
- Matriz de Riesgos (identificación, probabilidad, impacto, mitigación)
- Plan de Calidad
- Stakeholders
- Comunicaciones

**Campos Editables**:
- `metricas_pmi.alcance`, `tiempo`, `costo`, `calidad`
- `riesgos[]`: `descripcion`, `probabilidad`, `impacto`, `mitigacion`
- `plan_calidad`
- `stakeholders[]`

---

## 🔄 5. EDITABLE_INFORME_TECNICO.jsx - PENDIENTE

**Secciones Únicas**:
- Resumen Ejecutivo (textarea)
- 1. Introducción (textarea)
- 2. Análisis Técnico (textarea)
- 3. Resultados (textarea)
- 4. Conclusiones (textarea)
- 5. Recomendaciones (lista)

**Campos Editables**:
- `resumen_ejecutivo`
- `introduccion`
- `analisis_tecnico`
- `resultados`
- `conclusiones`
- `recomendaciones[]`

---

## 🔄 6. EDITABLE_INFORME_EJECUTIVO.jsx - PENDIENTE

**Secciones Únicas** (APA):
- Abstract (textarea)
- Metodología (textarea)
- Resultados (textarea)
- Discusión (textarea)
- Referencias (lista editable)
- Anexos

**Campos Editables**:
- `abstract`
- `metodologia`
- `resultados`
- `discusion`
- `referencias[]`: `autor`, `titulo`, `año`, `fuente`

---

## 🎨 Características Comunes (Todos)

**Props**:
```javascript
{
  datos,              // Objeto con datos del documento
  esquemaColores,     // 'azul-tesla', 'rojo-energia', 'verde-ecologico', 'dorado-premium'
  logoBase64,         // Logo en base64
  fuenteDocumento,    // 'Calibri', 'Arial', 'Times New Roman'
  onDatosChange       // Callback para notificar cambios
}
```

**State Management**:
- `useState` para datos editables
- `useEffect` para notificar cambios al padre
- Funciones helper para actualizar arrays

**Estilos**:
- Inline styles con colores dinámicos
- Diseño idéntico a plantillas HTML
- Responsive (max-width: 210mm)

---

## 📊 Progreso

- [x] 1/6 EDITABLE_COTIZACION_SIMPLE.jsx
- [ ] 2/6 EDITABLE_COTIZACION_COMPLEJA.jsx
- [ ] 3/6 EDITABLE_PROYECTO_SIMPLE.jsx
- [ ] 4/6 EDITABLE_PROYECTO_COMPLEJO.jsx
- [ ] 5/6 EDITABLE_INFORME_TECNICO.jsx
- [ ] 6/6 EDITABLE_INFORME_EJECUTIVO.jsx

**Tiempo Estimado**: ~30 minutos para los 5 restantes
