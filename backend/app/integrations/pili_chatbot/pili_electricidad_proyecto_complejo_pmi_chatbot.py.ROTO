"""
PILI ChatBot - Proyecto Complejo PMI (Electricidad)
Versión: 1.0
Metodología: PMI PMBOK 7th Edition

Genera PROJECT CHARTER profesional con:
- KPIs de gestión (SPI, CPI, EV, PV, AC)
- Cronograma Gantt (6 fases)
- Registro de Stakeholders
- Matriz RACI
- Registro de Riesgos (Top 5)
- 13 Entregables principales
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

class PILIElectricidadProyectoComplejoPMIChatBot:
    def __init__(self):
        self.version = "1.0 - PMI PMBOK 7th"
        self.contador = 1
        
    def procesar(self, mensaje: str, estado: Dict) -> Dict:
        """Procesa el mensaje del usuario y retorna respuesta"""
        
        # Inicializar estado si es necesario
        if not estado:
            estado = {}
        
        etapa = estado.get("etapa", "inicial")
        
        # ============================================
        # ETAPA: Inicial - Bienvenida
        # ============================================
        if etapa == "inicial":
            # Auto-detectar datos del frontend
            cliente_nombre = estado.get("cliente_nombre")
            proyecto_nombre = estado.get("proyecto_nombre")
            presupuesto = estado.get("presupuesto")
            moneda = estado.get("moneda", "USD")
            duracion_meses = estado.get("duracion_meses")
            
            # ✅ FLUJO NORMAL: Preguntar todo paso a paso
            estado["etapa"] = "ubicacion"
            return {'success': True, 'respuesta': f"""¡Hola! 👋 Soy **PILI**, tu asistente de proyectos eléctricos PMI.

━━━━━━━━━━━━━━━━━━━━━━━
**DATOS DETECTADOS DEL FORMULARIO**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Cliente: **{cliente_nombre or 'No especificado'}**
✅ Proyecto: **{proyecto_nombre or 'No especificado'}**
✅ Presupuesto: **{moneda} {presupuesto:,.2f if presupuesto else 'No especificado'}**
✅ Duración: **{duracion_meses} meses** if duracion_meses else 'No especificado'

Ahora necesito información adicional para crear el Project Charter completo.

━━━━━━━━━━━━━━━━━━━━━━━
**UBICACIÓN DEL PROYECTO**
━━━━━━━━━━━━━━━━━━━━━━━

📍 **¿Dónde se realizará el proyecto?**
_Ejemplo: Lima, Perú / Concepción, Chile_""", 'botones': None, 'estado': estado}
        
        # ============================================
                    {
                        "id": "R01",
                        "descripcion": "Retrasos en entrega de equipos importados",
                        "probabilidad": "Media",
                        "impacto": "Alto",
                        "severidad": "Alta",
                        "mitigacion": "Compra anticipada con proveedores alternativos certificados"
                    },
                    {
                        "id": "R02",
                        "descripcion": "Cambios en alcance solicitados por cliente",
                        "probabilidad": "Media",
                        "impacto": "Medio",
                        "severidad": "Media",
                        "mitigacion": "Control de cambios formal con aprobación escrita y ajuste de cronograma"
                    },
                    {
                        "id": "R03",
                        "descripcion": "Condiciones climáticas adversas",
                        "probabilidad": "Baja",
                        "impacto": "Medio",
                        "severidad": "Baja",
                        "mitigacion": "Planificación de actividades críticas en temporada seca"
                    }
                ]
                
                # Recursos por defecto
                estado["recursos_humanos"] = ["Project Manager PMI", "Ing. Residente", "Ing. Eléctrico", "Técnicos (3)", "Inspector QA"]
                estado["materiales"] = ["Tableros eléctricos certificados", "Cables THW/THHN", "Protecciones termomagnéticas", "Sistema de puesta a tierra", "Luminarias LED"]
                
                # ✅ GENERAR PROYECTO DIRECTAMENTE
                simbolo = {'PEN': 'S/', 'USD': '$', 'EUR': '€', 'GBP': '£'}.get(moneda, '$')
                return {
                    'success': True,
                    'respuesta': f"""🎉 **PROJECT CHARTER GENERADO AUTOMÁTICAMENTE**

━━━━━━━━━━━━━━━━━━━━━━━
**DATOS DETECTADOS DEL FORMULARIO**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Cliente: **{cliente_nombre}**
✅ Proyecto: **{proyecto_nombre}**
✅ Presupuesto: **{simbolo} {presupuesto:,.2f}**
✅ Duración: **{duracion_meses} meses ({duracion_dias} días)**

━━━━━━━━━━━━━━━━━━━━━━━
**PROYECTO COMPLETO GENERADO**
━━━━━━━━━━━━━━━━━━━━━━━

He creado un PROJECT CHARTER profesional con:
• ✅ KPIs PMI optimizados (SPI: 1.05, CPI: 0.98)
• ✅ Cronograma Gantt (6 fases, {duracion_dias} días)
• ✅ 3 Stakeholders principales
• ✅ Top 3 Riesgos identificados
• ✅ Equipo de 5 roles + Materiales certificados

**KPIs CALCULADOS:**
• EV: {simbolo}{estado['ev_k']}K | PV: {simbolo}{estado['pv_k']}K | AC: {simbolo}{estado['ac_k']}K

✅ **Documento listo para generar**

Haz clic en "Finalizar" para ver la vista previa y generar el PROJECT CHARTER en Word/PDF.""",
                    'botones': None,
                    'estado': estado,
                    'datos_generados': self._generar_proyecto(estado)['datos_generados']
                }
            
            # Modo manual si faltan datos
            if cliente_nombre and proyecto_nombre and presupuesto:
                estado["etapa"] = "ubicacion"
                simbolo = {'PEN': 'S/', 'USD': '$', 'EUR': '€', 'GBP': '£'}.get(moneda, '$')
                return {'success': True, 'respuesta': f"""¡Hola! 👋 **PILI** - Proyecto Complejo PMI

📋 **GENERACIÓN DE PROJECT CHARTER PROFESIONAL**
_Según metodología PMI PMBOK 7th Edition_

He detectado los siguientes datos:
✅ Cliente: **{cliente_nombre}**
✅ Proyecto: **{proyecto_nombre}**
✅ Presupuesto: **{simbolo} {presupuesto:,.2f}**
✅ Moneda: **{moneda}**

Vamos a crear un PROJECT CHARTER completo con:
• KPIs de gestión (SPI, CPI, EV, PV, AC)
• Cronograma Gantt (6 fases)
• Registro de Stakeholders
• Matriz RACI
• Registro de Riesgos (Top 5)
• 13 Entregables principales

━━━━━━━━━━━━━━━━━━━━━━━
**INFORMACIÓN TÉCNICA DEL PROYECTO**
━━━━━━━━━━━━━━━━━━━━━━━

📍 **¿Ubicación exacta del proyecto?**
_Ejemplo: Av. Principal 123, San Isidro, Lima_""", 'botones': None, 'estado': estado}
            else:
                estado["etapa"] = "ubicacion"
                return {'success': True, 'respuesta': """¡Hola! 👋 **PILI** - Proyecto Complejo PMI

📋 **GENERACIÓN DE PROJECT CHARTER PROFESIONAL**

Necesito información básica del proyecto.

📍 **¿Ubicación exacta del proyecto?**""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Ubicación
        # ============================================
        elif etapa == "ubicacion":
            estado["ubicacion"] = mensaje
            estado["etapa"] = "area"
            return {'success': True, 'respuesta': f"""✅ Ubicación: **{mensaje}**

📐 **¿Área total del proyecto (m²)?**
_Ejemplo: 5000_""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Área
        # ============================================
        elif etapa == "area":
            try:
                area = float(mensaje.replace(',', ''))
                estado["area_m2"] = area
                estado["etapa"] = "descripcion"
                return {'success': True, 'respuesta': f"""✅ Área: **{area:,.0f} m²**

📝 **Descripción técnica detallada del proyecto:**
_Incluye: tipo de instalación, sistemas, equipos principales, etc._
_Ejemplo: Sistema eléctrico industrial completo con subestación de 1000 KVA, tableros de distribución, sistema de automatización SCADA, iluminación LED, sistema de respaldo UPS_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Área inválida. Por favor ingresa solo números.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Descripción
        # ============================================
        elif etapa == "descripcion":
            estado["descripcion"] = mensaje
            estado["etapa"] = "normativa"
            return {'success': True, 'respuesta': f"""✅ Descripción guardada

📋 **Normativa aplicable:**
_Selecciona la normativa principal_

[CNE Suministro 2011] [NEC 2020] [IEC] [Otra]""", 'botones': [
                {'text': 'CNE Suministro 2011', 'value': 'CNE Suministro 2011'},
                {'text': 'NEC 2020', 'value': 'NEC 2020'},
                {'text': 'IEC', 'value': 'IEC'},
                {'text': 'Otra', 'value': 'OTRA'}
            ], 'estado': estado}
        
        # ============================================
        # ETAPA: Normativa
        # ============================================
        elif etapa == "normativa":
            if mensaje == "OTRA":
                estado["etapa"] = "normativa_otra"
                return {'success': True, 'respuesta': "📋 **Especifica la normativa:**", 'botones': None, 'estado': estado}
            else:
                estado["normativa"] = mensaje
                estado["etapa"] = "fecha_inicio"
                return {'success': True, 'respuesta': f"""✅ Normativa: **{mensaje}**

📅 **Fecha de inicio estimada (DD/MM/YYYY):**
_Ejemplo: 01/02/2026_""", 'botones': None, 'estado': estado}
        
        elif etapa == "normativa_otra":
            estado["normativa"] = mensaje
            estado["etapa"] = "fecha_inicio"
            return {'success': True, 'respuesta': f"""✅ Normativa: **{mensaje}**

📅 **Fecha de inicio estimada (DD/MM/YYYY):**""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Fecha inicio
        # ============================================
        elif etapa == "fecha_inicio":
            try:
                fecha = datetime.strptime(mensaje, "%d/%m/%Y")
                estado["fecha_inicio"] = mensaje
                estado["etapa"] = "kpi_spi"
                return {'success': True, 'respuesta': f"""✅ Fecha inicio: **{mensaje}**

━━━━━━━━━━━━━━━━━━━━━━━
**KPIs DE GESTIÓN PMI**
━━━━━━━━━━━━━━━━━━━━━━━

Como proyecto complejo PMI, necesitamos definir los KPIs de gestión.
Te ayudaré con valores recomendados según mejores prácticas.

📊 **SPI (Schedule Performance Index)**
_Mide el desempeño del cronograma_

Valores:
• **1.0** = En tiempo (recomendado)
• > 1.0 = Adelantado
• < 1.0 = Retrasado

Rango válido: 0.8 - 1.2

**¿Valor de SPI?**
_Ejemplo: 1.0_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Formato de fecha inválido. Usa DD/MM/YYYY", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: KPI - SPI
        # ============================================
        elif etapa == "kpi_spi":
            try:
                spi = float(mensaje)
                if spi < 0.5 or spi > 1.5:
                    return {'success': False, 'respuesta': "⚠️ SPI fuera de rango razonable (0.5-1.5). Por favor verifica.", 'botones': None, 'estado': estado}
                estado["spi"] = spi
                estado["etapa"] = "kpi_cpi"
                return {'success': True, 'respuesta': f"""✅ SPI: **{spi}**

📊 **CPI (Cost Performance Index)**
_Mide el desempeño del costo_

Valores:
• **1.0** = En presupuesto (recomendado)
• > 1.0 = Bajo presupuesto
• < 1.0 = Sobre presupuesto

Rango válido: 0.8 - 1.2

**¿Valor de CPI?**
_Ejemplo: 1.05_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa un número decimal (ej: 1.0)", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: KPI - CPI
        # ============================================
        elif etapa == "kpi_cpi":
            try:
                cpi = float(mensaje)
                if cpi < 0.5 or cpi > 1.5:
                    return {'success': False, 'respuesta': "⚠️ CPI fuera de rango razonable (0.5-1.5). Por favor verifica.", 'botones': None, 'estado': estado}
                estado["cpi"] = cpi
                estado["etapa"] = "kpi_ev"
                
                presupuesto = estado.get("presupuesto", 100000)
                sugerencia_ev = int(presupuesto * 0.70 / 1000)
                
                return {'success': True, 'respuesta': f"""✅ CPI: **{cpi}**

📊 **EV (Earned Value)**
_Valor ganado del proyecto en miles_

Sugerencia: **${sugerencia_ev}K** (70% del presupuesto)

**¿Valor de EV en miles?**
_Ejemplo: {sugerencia_ev}_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa un número decimal (ej: 1.05)", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: KPI - EV
        # ============================================
        elif etapa == "kpi_ev":
            try:
                ev = int(mensaje)
                estado["ev_k"] = ev
                estado["etapa"] = "kpi_pv"
                
                presupuesto = estado.get("presupuesto", 100000)
                sugerencia_pv = int(presupuesto * 0.75 / 1000)
                
                return {'success': True, 'respuesta': f"""✅ EV: **${ev}K**

📊 **PV (Planned Value)**
_Valor planificado del proyecto en miles_

Sugerencia: **${sugerencia_pv}K** (75% del presupuesto)

**¿Valor de PV en miles?**
_Ejemplo: {sugerencia_pv}_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa un número entero.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: KPI - PV
        # ============================================
        elif etapa == "kpi_pv":
            try:
                pv = int(mensaje)
                estado["pv_k"] = pv
                estado["etapa"] = "kpi_ac"
                
                presupuesto = estado.get("presupuesto", 100000)
                sugerencia_ac = int(presupuesto * 0.65 / 1000)
                
                return {'success': True, 'respuesta': f"""✅ PV: **${pv}K**

📊 **AC (Actual Cost)**
_Costo real del proyecto en miles_

Sugerencia: **${sugerencia_ac}K** (65% del presupuesto)

**¿Valor de AC en miles?**
_Ejemplo: {sugerencia_ac}_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa un número entero.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: KPI - AC
        # ============================================
        elif etapa == "kpi_ac":
            try:
                ac = int(mensaje)
                estado["ac_k"] = ac
                estado["etapa"] = "alcance"
                
                return {'success': True, 'respuesta': f"""✅ AC: **${ac}K**

━━━━━━━━━━━━━━━━━━━━━━━
✅ **KPIs PMI COMPLETADOS**
━━━━━━━━━━━━━━━━━━━━━━━

SPI: {estado.get('spi')} | CPI: {estado.get('cpi')}
EV: ${estado.get('ev_k')}K | PV: ${estado.get('pv_k')}K | AC: ${ac}K

━━━━━━━━━━━━━━━━━━━━━━━
**ALCANCE DEL PROYECTO**
━━━━━━━━━━━━━━━━━━━━━━━

📋 **Descripción detallada del alcance (WBS Level 1):**

Incluye todos los entregables principales del proyecto.

_Ejemplo:_
_• Diseño e ingeniería eléctrica completa_
_• Suministro de materiales certificados_
_• Instalación de sistema eléctrico_
_• Sistema de automatización y control SCADA_
_• Pruebas FAT/SAT_
_• Documentación técnica as-built_
_• Capacitación al personal_
_• Garantía de 24 meses_

**Tu alcance:**""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa un número entero.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Alcance
        # ============================================
        elif etapa == "alcance":
            estado["alcance"] = mensaje
            estado["etapa"] = "dias_ingenieria"
            
            # 🎯 ENVIAR FORMULARIO DE ENTREGABLES
            return {
                'success': True, 
                'respuesta': """✅ Alcance definido

━━━━━━━━━━━━━━━━━━━━━━━
**ENTREGABLES DEL PROYECTO**
━━━━━━━━━━━━━━━━━━━━━━━

📦 **Selecciona los entregables necesarios:**""",
                'botones': None,
                'estado': estado,
                # ✨ FORMULARIO: Entregables
                'formulario': {
                    'tipo': 'entregables',
                    'tipoProyecto': estado.get('tipo_proyecto', 'industrial'),
                    'presupuesto': estado.get('presupuesto', 0),
                    'area': estado.get('area_m2', 0)
                }
            }
        
        # ============================================
        # ETAPA: Días Ingeniería
        # ============================================
        elif etapa == "dias_ingenieria":
            try:
                dias = int(mensaje)
                if dias < 5 or dias > 90:
                    return {'success': False, 'respuesta': "⚠️ Duración fuera de rango razonable (5-90 días).", 'botones': None, 'estado': estado}
                estado["dias_ingenieria"] = dias
                estado["etapa"] = "dias_ejecucion"
                return {'success': True, 'respuesta': f"""✅ Ingeniería y Diseño: **{dias} días**

⏱️ **Días para Ejecución:**
_Sugerencia: 40-60 días_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa solo el número de días.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Días Ejecución
        # ============================================
        elif etapa == "dias_ejecucion":
            try:
                dias = int(mensaje)
                if dias < 10 or dias > 180:
                    return {'success': False, 'respuesta': "⚠️ Duración fuera de rango razonable (10-180 días).", 'botones': None, 'estado': estado}
                estado["dias_ejecucion"] = dias
                
                # Calcular duración total
                duracion_total = 10 + 3 + estado.get("dias_ingenieria", 25) + dias + 8 + 5
                estado["duracion_total"] = duracion_total
                
                estado["etapa"] = "riesgo1_desc"
                return {'success': True, 'respuesta': f"""✅ Ejecución: **{dias} días**

━━━━━━━━━━━━━━━━━━━━━━━
✅ **CRONOGRAMA COMPLETADO**
━━━━━━━━━━━━━━━━━━━━━━━

Duración total: **{duracion_total} días**

1. Inicio y Planificación: 10 días
2. Gestión Stakeholders: 3 días
3. Ingeniería y Diseño: {estado.get('dias_ingenieria')} días
4. Ejecución: {dias} días
5. Pruebas y Puesta en Marcha: 8 días
6. Cierre: 5 días

━━━━━━━━━━━━━━━━━━━━━━━
**REGISTRO DE RIESGOS (TOP 5)**
━━━━━━━━━━━━━━━━━━━━━━━

Identificaremos los 5 riesgos principales del proyecto.

Para cada riesgo necesito:
• Descripción
• Probabilidad (Alta/Media/Baja)
• Impacto (Alto/Medio/Bajo)
• Plan de Mitigación

━━━━━━━━━━━━━━━━━━━━━━━
**RIESGO 1 de 5**
━━━━━━━━━━━━━━━━━━━━━━━

📝 **Descripción del riesgo:**
_Ejemplo: Retrasos en entrega de equipos importados_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa solo el número de días.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Riesgos (Loop de 5)
        # ============================================
        elif etapa.startswith("riesgo"):
            return self._procesar_riesgo(mensaje, estado)
        
        # ============================================
        # ETAPA: Recursos Humanos
        # ============================================
        elif etapa == "recursos_humanos":
            recursos = [r.strip() for r in mensaje.split(',') if r.strip()]
            estado["recursos_humanos"] = recursos
            estado["etapa"] = "materiales"
            return {'success': True, 'respuesta': f"""✅ Equipo: **{len(recursos)} roles** definidos

🔧 **Materiales principales (separados por coma):**
_Ejemplo: Tableros eléctricos, Cables THW, Protecciones termomagnéticas, Sistema SCADA, UPS_""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Materiales
        # ============================================
        elif etapa == "materiales":
            materiales = [m.strip() for m in mensaje.split(',') if m.strip()]
            estado["materiales"] = materiales
            return self._generar_proyecto(estado)
        
        return {'success': False, 'respuesta': "❌ Etapa no reconocida", 'botones': None, 'estado': estado}
    
    def _procesar_riesgo(self, mensaje: str, estado: Dict) -> Dict:
        """Procesa el loop de 5 riesgos"""
        etapa = estado.get("etapa")
        
        # Inicializar lista de riesgos si no existe
        if "riesgos" not in estado:
            estado["riesgos"] = []
        
        # Extraer número de riesgo y campo
        partes = etapa.split("_")
        num_riesgo = int(partes[0].replace("riesgo", ""))
        campo = "_".join(partes[1:])
        
        # Inicializar riesgo temporal si no existe
        if "riesgo_temp" not in estado:
            estado["riesgo_temp"] = {}
        
        if campo == "desc":
            estado["riesgo_temp"]["descripcion"] = mensaje
            estado["etapa"] = f"riesgo{num_riesgo}_prob"
            return {'success': True, 'respuesta': f"""✅ Descripción: **{mensaje}**

📊 **Probabilidad del riesgo:**

[Alta] [Media] [Baja]""", 'botones': [
                {'text': 'Alta', 'value': 'Alta'},
                {'text': 'Media', 'value': 'Media'},
                {'text': 'Baja', 'value': 'Baja'}
            ], 'estado': estado}
        
        elif campo == "prob":
            estado["riesgo_temp"]["probabilidad"] = mensaje
            estado["etapa"] = f"riesgo{num_riesgo}_imp"
            return {'success': True, 'respuesta': f"""✅ Probabilidad: **{mensaje}**

💥 **Impacto del riesgo:**

[Alto] [Medio] [Bajo]""", 'botones': [
                {'text': 'Alto', 'value': 'Alto'},
                {'text': 'Medio', 'value': 'Medio'},
                {'text': 'Bajo', 'value': 'Bajo'}
            ], 'estado': estado}
        
        elif campo == "imp":
            estado["riesgo_temp"]["impacto"] = mensaje
            estado["etapa"] = f"riesgo{num_riesgo}_mit"
            
            # Calcular severidad
            prob = estado["riesgo_temp"]["probabilidad"]
            imp = mensaje
            severidad = self._calcular_severidad(prob, imp)
            estado["riesgo_temp"]["severidad"] = severidad
            
            return {'success': True, 'respuesta': f"""✅ Impacto: **{mensaje}**
✅ Severidad calculada: **{severidad}**

🛡️ **Plan de Mitigación:**
_Describe las acciones para reducir o eliminar el riesgo_
_Ejemplo: Compra anticipada de equipos críticos con proveedores alternativos_""", 'botones': None, 'estado': estado}
        
        elif campo == "mit":
            estado["riesgo_temp"]["mitigacion"] = mensaje
            estado["riesgo_temp"]["id"] = f"R{num_riesgo:02d}"
            
            # Guardar riesgo completo
            estado["riesgos"].append(estado["riesgo_temp"].copy())
            estado.pop("riesgo_temp")
            
            # Verificar si hay más riesgos
            if num_riesgo < 5:
                estado["etapa"] = f"riesgo{num_riesgo + 1}_desc"
                return {'success': True, 'respuesta': f"""✅ Plan de mitigación guardado

━━━━━━━━━━━━━━━━━━━━━━━
✅ **RIESGO {num_riesgo} COMPLETADO**
━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━
**RIESGO {num_riesgo + 1} de 5**
━━━━━━━━━━━━━━━━━━━━━━━

📝 **Descripción del riesgo:**""", 'botones': None, 'estado': estado}
            else:
                # Todos los riesgos completados
                estado["etapa"] = "recursos_humanos"
                
                # 🎯 ENVIAR FORMULARIO en lugar de texto libre
                return {
                    'success': True, 
                    'respuesta': """✅ Plan de mitigación guardado

━━━━━━━━━━━━━━━━━━━━━━━
✅ **TODOS LOS RIESGOS COMPLETADOS**
━━━━━━━━━━━━━━━━━━━━━━━

Ahora necesito información sobre los recursos del proyecto.

👥 **Selecciona el equipo profesional necesario:**""",
                    'botones': None,
                    'estado': estado,
                    # ✨ NUEVO: Enviar formulario interactivo
                    'formulario': {
                        'tipo': 'profesionales',
                        'tipoProyecto': estado.get('tipo_proyecto', 'industrial'),
                        'presupuesto': estado.get('presupuesto', 0),
                        'area': estado.get('area_m2', 0)
                    }
                }
        
        return {'success': False, 'respuesta': "❌ Campo de riesgo no reconocido", 'botones': None, 'estado': estado}
    
    def _calcular_severidad(self, probabilidad: str, impacto: str) -> str:
        """Calcula la severidad del riesgo según probabilidad e impacto"""
        matriz = {
            ('Alta', 'Alto'): 'Alta',
            ('Alta', 'Medio'): 'Alta',
            ('Alta', 'Bajo'): 'Media',
            ('Media', 'Alto'): 'Alta',
            ('Media', 'Medio'): 'Media',
            ('Media', 'Bajo'): 'Baja',
            ('Baja', 'Alto'): 'Media',
            ('Baja', 'Medio'): 'Baja',
            ('Baja', 'Bajo'): 'Baja'
        }
        return matriz.get((probabilidad, impacto), 'Media')
    
    def _generar_proyecto(self, estado: Dict) -> Dict:
        """Genera el proyecto completo con todos los datos"""
        
        # Datos del cliente y proyecto
        cliente = estado.get("cliente_nombre", "Cliente")
        nombre = estado.get("proyecto_nombre", "Proyecto Eléctrico")
        ubicacion = estado.get("ubicacion", "Lima, Perú")
        area = estado.get("area_m2", 1000)
        descripcion = estado.get("descripcion", "Proyecto eléctrico")
        normativa = estado.get("normativa", "CNE Suministro 2011")
        presupuesto = estado.get("presupuesto", 100000)
        moneda = estado.get("moneda", "USD")
        
        # Fechas y duración
        fecha_inicio = datetime.strptime(estado.get("fecha_inicio", "01/01/2026"), "%d/%m/%Y")
        duracion_total = estado.get("duracion_total", 100)
        fecha_fin = fecha_inicio + timedelta(days=duracion_total)
        
        # Código proyecto
        codigo = f"PROY-PMI-{fecha_inicio.year}-{self.contador:03d}"
        self.contador += 1
        
        # KPIs
        spi = estado.get("spi", 1.0)
        cpi = estado.get("cpi", 1.0)
        ev_k = estado.get("ev_k", 70)
        pv_k = estado.get("pv_k", 75)
        ac_k = estado.get("ac_k", 65)
        
        # Alcance
        alcance = estado.get("alcance", "Alcance del proyecto")
        
        # Cronograma
        dias_ingenieria = estado.get("dias_ingenieria", 25)
        dias_ejecucion = estado.get("dias_ejecucion", 50)
        
        # Stakeholders (siempre los 3 básicos)
        stakeholders = [
            {
                "nombre": cliente,
                "rol": "Cliente / Patrocinador Principal",
                "poder": "Alto",
                "interes": "Alto"
            },
            {
                "nombre": "Jefe de Proyecto",
                "rol": "Project Manager / Responsable de Ejecución",
                "poder": "Alto",
                "interes": "Alto"
            },
            {
                "nombre": "Equipo Técnico",
                "rol": "Ingenieros y Técnicos Instaladores",
                "poder": "Medio",
                "interes": "Alto"
            }
        ]
        
        # Riesgos
        riesgos = estado.get("riesgos", [])
        
        # Recursos
        recursos_humanos = estado.get("recursos_humanos", ["Project Manager", "Ing. Residente", "Técnicos"])
        materiales = estado.get("materiales", ["Tableros eléctricos", "Cables", "Protecciones"])
        
        # Generar datos completos
        datos_generados = {
            "codigo": codigo,
            "nombre": nombre,
            "cliente": {
                "nombre": estado.get("cliente_nombre", cliente),
                "ruc": estado.get("cliente_ruc"),
                "direccion": estado.get("cliente_direccion"),
                "telefono": estado.get("cliente_telefono"),
                "email": estado.get("cliente_email")
            },
            "ubicacion": ubicacion,
            "area_m2": area,
            "descripcion": descripcion,
            "normativa": normativa,
            "cronograma": {
                "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
                "fecha_fin": fecha_fin.strftime("%d/%m/%Y"),
                "duracion_total": duracion_total
            },
            "presupuesto": presupuesto,
            "moneda": moneda,
            "kpis": {
                "spi": spi,
                "cpi": cpi,
                "ev_k": ev_k,
                "pv_k": pv_k,
                "ac_k": ac_k
            },
            "alcance": alcance,
            "fases_gantt": [
                {"nombre": "Inicio y Planificación", "duracion": 10},
                {"nombre": "Gestión Stakeholders", "duracion": 3},
                {"nombre": "Ingeniería y Diseño", "duracion": dias_ingenieria},
                {"nombre": "Ejecución", "duracion": dias_ejecucion},
                {"nombre": "Pruebas y Puesta en Marcha", "duracion": 8},
                {"nombre": "Cierre", "duracion": 5}
            ],
            "stakeholders": stakeholders,
            "riesgos": riesgos,
            "recursos": {
                "humanos": recursos_humanos,
                "materiales": materiales
            }
        }
        
        simbolo = {'PEN': 'S/', 'USD': '$', 'EUR': '€', 'GBP': '£'}.get(moneda, '$')
        
        return {
            'success': True,
            'respuesta': f"""🎉 **PROJECT CHARTER GENERADO**

━━━━━━━━━━━━━━━━━━━━━━━
**RESUMEN DEL PROYECTO**
━━━━━━━━━━━━━━━━━━━━━━━

📋 **Código:** {codigo}
🏢 **Cliente:** {cliente}
📍 **Ubicación:** {ubicacion}
📐 **Área:** {area:,.0f} m²

**CRONOGRAMA:**
• Inicio: {fecha_inicio.strftime("%d/%m/%Y")}
• Fin: {fecha_fin.strftime("%d/%m/%Y")}
• Duración: {duracion_total} días

**PRESUPUESTO:**
• Total: {simbolo} {presupuesto:,.2f}

**KPIs PMI:**
• SPI: {spi} | CPI: {cpi}
• EV: ${ev_k}K | PV: ${pv_k}K | AC: ${ac_k}K

**RIESGOS:** {len(riesgos)} identificados
**STAKEHOLDERS:** {len(stakeholders)} registrados

✅ **Documento listo para generar**

Haz clic en "Finalizar" para ver la vista previa y generar el PROJECT CHARTER en Word/PDF.""",
            'botones': None,
            'estado': estado,
            'datos_generados': datos_generados
        }
