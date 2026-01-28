# 📋 CONFIRMACIÓN: Lógica Específica por Servicio

## ✅ LO QUE ENTIENDO AHORA

### **1. Cada servicio tiene lógica DIFERENTE**

**ITSE (5 etapas):**
1. Categoría (8 opciones)
2. Tipo específico (dinámico según categoría)
3. Área (input número)
4. Pisos (input número)
5. Cotización (cálculo automático de riesgo)

**Electricidad (7 etapas):**
1. Tipo instalación (3 opciones: Residencial/Comercial/Industrial)
2. Área (input número)
3. Pisos (input número)
4. Puntos de luz (input número)
5. Tomacorrientes (input número)
6. Tableros (input número)
7. Cotización (cálculo automático de items)

### **2. PILI pregunta lo necesario para RELLENAR LA PLANTILLA**

**Campos de la plantilla `COTIZACION_SIMPLE.html`:**
- `{{CLIENTE_NOMBRE}}` - Del sistema
- `{{PROYECTO_NOMBRE}}` - Generado automáticamente
- `{{AREA_M2}}` - PILI pregunta
- `{{SERVICIO_NOMBRE}}` - Del servicio seleccionado
- `{{DESCRIPCION_PROYECTO}}` - Generado automáticamente
- Items de tabla - PILI calcula automáticamente
- `{{SUBTOTAL}}`, `{{IGV}}`, `{{TOTAL}}` - PILI calcula
- `{{NORMATIVA_APLICABLE}}` - Del knowledge base

### **3. Cada YAML debe tener:**

```yaml
service: nombre_servicio
name: "Nombre Completo"

# PRECIOS REALES (del knowledge base)
precios:
  item1: 100.00
  item2: 200.00

# LÓGICA ESPECÍFICA DEL SERVICIO
etapas_conversacion:
  - id: etapa1
    type: buttons/input_number/input_text
    pregunta: "..."
    opciones: [...]
    validacion: {...}

# REGLAS DE CÁLCULO
reglas_calculo:
  formula1: "..."
  formula2: "..."

# MENSAJES PROFESIONALES
mensajes:
  presentacion: "..."
  confirmaciones: "..."
  cotizacion: "..."
```

---

## 📊 EJEMPLO CONCRETO: ELECTRICIDAD

### **Flujo de Conversación:**

```
PILI: ¿Qué tipo de instalación necesitas?
      [🏠 Residencial] [🏢 Comercial] [🏭 Industrial]

USER: Residencial

PILI: ¿Cuál es el área total del proyecto en m²?
      _Escribe el número (ejemplo: 120)_

USER: 120

PILI: ¿Cuántos pisos tiene el proyecto?
      _Escribe el número (ejemplo: 2)_

USER: 2

PILI: ¿Cuántos puntos de luz necesitas?
      _Escribe el número (ejemplo: 25)_

USER: 25

PILI: ¿Cuántos tomacorrientes?
      _Escribe el número (ejemplo: 15)_

USER: 15

PILI: ¿Cuántos tableros eléctricos?
      _Escribe el número (ejemplo: 2)_

USER: 2

PILI: [GENERA COTIZACIÓN AUTOMÁTICAMENTE]
      
      📊 COTIZACIÓN INSTALACIÓN ELÉCTRICA RESIDENCIAL
      
      📋 DATOS DEL PROYECTO:
      📏 Área: 120 m²
      🏢 Pisos: 2
      💡 Puntos de luz: 25
      🔌 Tomacorrientes: 15
      ⚡ Tableros: 2
      
      💰 ITEMS CALCULADOS:
      1. Puntos de luz empotrados (25 und)
         └ S/ 2,000.00
      
      2. Tomacorrientes dobles (15 und)
         └ S/ 900.00
      
      3. Tableros eléctricos (2 und)
         └ S/ 2,400.00
      
      4. Cable THW 2.5mm² (360m)
         └ S/ 900.00
      
      5. Tubería PVC 3/4" (288m)
         └ S/ 345.60
      
      📈 TOTALES:
      Subtotal: S/ 6,545.60
      IGV (18%): S/ 1,178.21
      TOTAL: S/ 7,723.81
      
      [📄 Generar Cotización] [🔄 Nueva consulta]
```

### **Datos que PILI genera para la plantilla:**

```python
{
  "proyecto": {
    "nombre": "Instalación Eléctrica Residencial",
    "area_m2": 120,
    "descripcion": "Instalación eléctrica residencial completa según CNE 2011"
  },
  "items": [
    {
      "descripcion": "Puntos de luz empotrados (25 und)",
      "cantidad": 25,
      "unidad": "und",
      "precio_unitario": 80.00,
      "total": 2000.00
    },
    {
      "descripcion": "Tomacorrientes dobles (15 und)",
      "cantidad": 15,
      "unidad": "und",
      "precio_unitario": 60.00,
      "total": 900.00
    },
    // ... más items
  ],
  "subtotal": 6545.60,
  "igv": 1178.21,
  "total": 7723.81,
  "normativa": "CNE Suministro 2011 - Sección 050",
  "tiempo_estimado": "5-7 días hábiles",
  "garantia": "1 año"
}
```

---

## 🎯 LO QUE VOY A CREAR

### **9 Archivos YAML Completos:**

1. **electricidad.yaml** (~600 líneas)
   - Precios por tipo (Residencial/Comercial/Industrial)
   - 7 etapas de conversación
   - Cálculo automático de items
   - Reglas de negocio

2. **pozo-tierra.yaml** (~500 líneas)
   - Tipos de suelo
   - Resistencia objetivo
   - Cálculo de varillas y materiales

3. **contraincendios.yaml** (~550 líneas)
   - Sistemas (Detección/Extinción/Completo)
   - Cálculo por área y pisos
   - Normativa NFPA

4. **domotica.yaml** (~500 líneas)
   - Niveles (Básico/Intermedio/Avanzado)
   - Dispositivos inteligentes
   - Protocolos

5. **cctv.yaml** (~550 líneas)
   - Tipos de cámaras (Analógica/IP)
   - Días de grabación
   - Cálculo de almacenamiento

6. **redes.yaml** (~500 líneas)
   - Tipos de cable (Cat5e/Cat6/Fibra)
   - Puntos de red
   - Certificación

7. **automatizacion-industrial.yaml** (~550 líneas)
   - Tipos de PLC
   - Equipos a automatizar
   - Programación

8. **expedientes.yaml** (~450 líneas)
   - Tipos de expediente
   - Área del proyecto
   - Memoria + Planos + Presupuesto

9. **saneamiento.yaml** (~500 líneas)
   - Tipos de instalación
   - Baños
   - Red de agua y desagüe

**Total:** ~4,700 líneas distribuidas en 9 archivos

---

## ✅ CONFIRMACIÓN FINAL

**¿Es correcto que:**

1. ✅ Cada YAML tenga su propia lógica de conversación (no todos iguales)
2. ✅ PILI pregunte solo lo necesario para rellenar la plantilla
3. ✅ Los cálculos sean automáticos basados en precios reales
4. ✅ Los mensajes sean profesionales y persuasivos
5. ✅ Cada servicio tenga diferente número de etapas según su complejidad

**Si es correcto, procedo a crear los 9 YAMLs completos ahora.**
