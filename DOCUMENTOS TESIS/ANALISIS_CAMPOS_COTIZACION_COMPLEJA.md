# 📋 ANÁLISIS: CAMPOS REQUERIDOS PARA COTIZACIÓN COMPLEJA

**Problema identificado:** El chatbot complejo debe recopilar información adicional que la plantilla compleja requiere.

---

## 🔍 COMPARATIVA DE CAMPOS

### Cotización Simple (Campos)
```
- CLIENTE_NOMBRE
- PROYECTO_NOMBRE
- AREA_M2
- SERVICIO_NOMBRE
- FECHA_COTIZACION
- VIGENCIA
- ITEMS[] (descripcion, cantidad, unidad, precio_unitario)
- SUBTOTAL
- IGV
- TOTAL
```

### Cotización Compleja (Campos ADICIONALES)
```
+ DESCRIPCION_PROYECTO (texto largo, alcance detallado)
+ NORMATIVA_APLICABLE (CNE-Utilización, NFPA, etc.)
+ DIAS_INGENIERIA (cronograma fase 1)
+ DIAS_ADQUISICIONES (cronograma fase 2)
+ DIAS_INSTALACION (cronograma fase 3)
+ DIAS_PRUEBAS (cronograma fase 4)
+ Sección "Alcance del Proyecto"
+ Cronograma de 4 fases
+ Garantías detalladas
+ Condiciones de pago
+ Observaciones técnicas
```

---

## ⚡ EJEMPLO: ELECTRICIDAD COMPLEJA

### Preguntas ADICIONALES necesarias:

1. **Descripción del Proyecto**
   - Pregunta: "Describe brevemente el proyecto (tipo de edificación, uso, características especiales)"
   - Respuesta ejemplo: "Instalación eléctrica completa para edificio comercial de 3 pisos, incluye iluminación, tomacorrientes, tableros, y sistema de emergencia"

2. **Normativa Aplicable**
   - Auto-detectado: "CNE-Utilización 2011" (para Perú)
   - Puede ser fijo por tipo de servicio

3. **Cronograma** (auto-calculado basado en complejidad)
   - Ingeniería: 5-10 días (según área y complejidad)
   - Adquisiciones: 7-15 días
   - Instalación: Calculado por puntos (1 punto = 0.5 días)
   - Pruebas: 2-5 días

---

## 🏭 EJEMPLO: AUTOMATIZACIÓN INDUSTRIAL COMPLEJA

### Preguntas ADICIONALES:

1. **Descripción del Proceso**
   - "¿Qué proceso industrial vas a automatizar?"
   - Ejemplo: "Control de temperatura y presión en línea de producción de alimentos"

2. **Tipo de Control**
   - PLC: Normativa IEC 61131
   - SCADA: Normativa ISA-95
   - HMI: Normativa IEC 62264

3. **Cronograma**
   - Ingeniería: 10-20 días (diseño de lógica)
   - Adquisiciones: 15-30 días (importación equipos)
   - Programación: 10-15 días
   - Pruebas: 5-10 días

---

## 🔥 EJEMPLO: CONTRA INCENDIOS COMPLEJA

### Preguntas ADICIONALES:

1. **Nivel de Riesgo**
   - "¿Qué nivel de riesgo tiene la edificación?"
   - Opciones: Bajo, Moderado, Alto, Muy Alto

2. **Normativa**
   - NFPA 13 (Rociadores)
   - NFPA 72 (Detección)
   - NFPA 10 (Extintores)

3. **Cálculo Hidráulico**
   - Presión requerida
   - Caudal
   - Reserva de agua

---

## 🎯 ESTRATEGIA DE IMPLEMENTACIÓN

### Opción A: Preguntas Explícitas (RECOMENDADO)
El chatbot pregunta explícitamente por cada campo adicional:

```python
def _etapa_descripcion_proyecto(self, mensaje: str, estado: Dict):
    estado["descripcion_proyecto"] = mensaje
    estado["etapa"] = "cronograma"
    return {
        'respuesta': """Descripción guardada ✅
        
Ahora voy a calcular el cronograma estimado..."""
    }
```

### Opción B: Auto-generación Inteligente
El chatbot genera automáticamente los campos basándose en las respuestas:

```python
def _generar_descripcion_automatica(self, estado: Dict) -> str:
    tipo = estado["tipo"]
    area = estado["area"]
    puntos = estado["cargas"]["iluminacion"]["puntos"]
    
    return f"""Instalación eléctrica {tipo.lower()} de {area}m² que incluye:
- {puntos} puntos de iluminación LED
- Sistema de tableros y protecciones
- Puesta a tierra según CNE
- Pruebas y certificación"""
```

---

## 💡 RECOMENDACIÓN FINAL

**Para los 3 servicios complejos, usar HÍBRIDO:**

1. **Campos técnicos:** Auto-generados (normativa, cronograma)
2. **Descripción proyecto:** Pregunta opcional al usuario
3. **Datos de cálculo:** Recopilados en el flujo normal

### Flujo Propuesto:

```
1. Tipo instalación → Auto-detecta normativa
2. Área + cargas → Calcula cronograma automático
3. [OPCIONAL] "¿Quieres agregar detalles al proyecto?" 
   - Sí → Pregunta descripción
   - No → Genera descripción automática
4. Genera cotización compleja con todos los campos
```

---

## 📝 CAMPOS POR SERVICIO

### Electricidad Compleja
- Normativa: "CNE-Utilización 2011"
- Descripción: Auto-generada o manual
- Cronograma: Auto-calculado por puntos

### Automatización Industrial Compleja
- Normativa: "IEC 61131-3 (PLC)" o "ISA-95 (SCADA)"
- Descripción: **Pregunta obligatoria** (proceso a automatizar)
- Cronograma: Auto-calculado por puntos I/O

### Contra Incendios Compleja
- Normativa: "NFPA 13/72/10" (según tipo)
- Descripción: Auto-generada
- Cronograma: Auto-calculado por área/unidades

---

## ✅ CONCLUSIÓN

**NO es solo copiar y pegar.** Necesito:

1. ✅ Agregar etapas adicionales al chatbot para campos complejos
2. ✅ Implementar auto-generación inteligente de descripción
3. ✅ Calcular cronograma basado en complejidad
4. ✅ Asignar normativa según tipo de servicio
5. ✅ Generar `datos_generados` con TODOS los campos de la plantilla compleja

**Próximo paso:** Revisar y corregir `pili_electricidad_complejo_chatbot.py` para incluir TODOS los campos necesarios.

---

**Archivo:** `ANALISIS_CAMPOS_COTIZACION_COMPLEJA.md`  
**Estado:** Análisis completo - Listo para corrección
