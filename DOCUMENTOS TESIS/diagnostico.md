# Auditoría Rápida - Problemas Críticos Identificados

**Fecha**: 20 de Diciembre, 2025  
**Auditor**: Antigravity AI  
**Severidad**: 🔴 ALTA - Afecta funcionalidad core

---

## 🚨 Problemas Críticos Identificados

### Problema 1: Todos los Documentos Generan como "Cotización"
**Severidad**: 🔴 CRÍTICA  
**Impacto**: Los 6 tipos de documentos no tienen formatos diferenciados

**Evidencia**:
- Usuario reporta que proyectos e informes se generan como cotizaciones
- No hay diferenciación visual entre tipos de documento
- Títulos y estructura son idénticos

**Causa Probable**:
- `word_generator_v2.py` detecta `tipo_documento` pero no aplica formatos diferentes
- Falta implementación de plantillas específicas por tipo

### Problema 2: Vistas Previas de Otros Tipos Tienen Bugs
**Severidad**: 🔴 CRÍTICA  
**Impacto**: Proyectos e informes no muestran datos en tablas

**Evidencia**:
- Solo se corrigió `cotizacion-simple`
- Proyectos e informes usan componentes diferentes
- Mismo problema de `precio_unitario` vs `precioUnitario`

**Causa Probable**:
- Solo se actualizó vista de cotización
- Faltan actualizar vistas de proyecto e informe

---

## 📊 Diagnóstico Detallado

### Archivos a Revisar

1. **Backend - Generación de Documentos**
   - `word_generator_v2.py` - ¿Diferencia entre tipos?
   - Método `generar_cotizacion` - ¿Es genérico o específico?

2. **Frontend - Vistas Previas**
   - Vista de proyecto - ¿Usa `precioUnitario`?
   - Vista de informe - ¿Usa `precioUnitario`?
   - Componentes específicos por tipo

---

## 🎯 Plan de Acción Prioritizado

### Prioridad 1: Auditar Generación de Documentos
1. Revisar `word_generator_v2.py`
2. Verificar si detecta `tipo_documento`
3. Confirmar si aplica formatos diferentes

### Prioridad 2: Auditar Vistas Previas
1. Identificar componentes de vista de proyecto
2. Identificar componentes de vista de informe
3. Verificar uso de campos `precio_unitario`

### Prioridad 3: Implementar Fixes
1. Diferenciar formatos de documento en backend
2. Corregir vistas previas de proyecto e informe
3. Testing de los 6 tipos

---

## 📝 Próximos Pasos

1. ✅ Auditar `word_generator_v2.py`
2. ✅ Auditar vistas de proyecto e informe
3. ⏳ Crear plan de implementación
4. ⏳ Aplicar fixes sistemáticamente
5. ⏳ Testing completo de 6 tipos

---

**Tiempo Estimado**: 1-2 horas  
**Complejidad**: Media-Alta
