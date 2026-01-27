"""📋 PILI ELECTRICIDAD PROYECTO SIMPLE v5.0 - EXHAUSTIVO"""
from typing import Dict, Optional
from datetime import datetime, timedelta

class PILIElectricidadProyectoSimpleChatBot:
    def __init__(self):
        self.contador = 1
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None: estado = {"etapa": "inicial"}
        etapa = estado.get("etapa", "inicial")
        
        # ============================================
        # ETAPA INICIAL: Auto-detectar datos del frontend
        # ============================================
        if etapa == "inicial":
            tiene_cliente = estado.get("cliente_nombre") is not None
            tiene_proyecto = estado.get("proyecto_nombre") is not None
            tiene_presupuesto = estado.get("presupuesto") is not None
            tiene_moneda = estado.get("moneda") is not None
            
            if tiene_cliente and tiene_proyecto and tiene_presupuesto:
                estado["etapa"] = "ubicacion"
                simbolo = {'PEN': 'S/', 'USD': '$', 'EUR': '€'}.get(estado.get('moneda', 'PEN'), 'S/')
                return {'success': True, 'respuesta': f"""¡Hola! 👋 **Pili** - Proyecto Simple Electricidad

📋 **GENERACIÓN DE PLAN DE PROYECTO PROFESIONAL**

He detectado los siguientes datos:
✅ Cliente: **{estado.get('cliente_nombre')}**
✅ Proyecto: **{estado.get('proyecto_nombre')}**
✅ Presupuesto: **{simbolo} {estado.get('presupuesto'):,.2f}**
✅ Moneda: **{estado.get('moneda', 'PEN')}**

Ahora necesito detalles técnicos específicos para crear un plan profesional.

📍 **¿Ubicación exacta del proyecto?**
_Ejemplo: Av. Principal 123, San Isidro, Lima_""", 'botones': None, 'estado': estado}
            else:
                estado["etapa"] = "cliente"
                return {'success': True, 'respuesta': """¡Hola! 👋 **Pili** - Proyecto Simple Electricidad

📋 **GENERACIÓN DE PLAN DE PROYECTO**

**¿Nombre del cliente?**
_Ejemplo: Constructora ABC S.A.C._""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Ubicación
        # ============================================
        elif etapa == "ubicacion":
            estado["ubicacion"] = mensaje
            estado["etapa"] = "area"
            return {'success': True, 'respuesta': f"""✅ Ubicación: **{mensaje}**

📐 **¿Área total del proyecto en m²?**
_Ejemplo: 250_""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Área
        # ============================================
        elif etapa == "area":
            try:
                estado["area"] = float(mensaje)
                estado["etapa"] = "descripcion"
                return {'success': True, 'respuesta': f"""✅ Área: **{mensaje} m²**

📝 **Descripción técnica detallada del proyecto:**
_Ejemplo: Instalación eléctrica completa para edificio de oficinas de 3 pisos, incluyendo tableros, cableado y sistema de puesta a tierra_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Número inválido. Por favor ingresa solo el número.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Descripción
        # ============================================
        elif etapa == "descripcion":
            estado["descripcion"] = mensaje
            estado["etapa"] = "normativa"
            return {'success': True, 'respuesta': f"""✅ Descripción guardada

📜 **¿Normativa aplicable?**""", 'botones': [
                {"text": "CNE Suministro 2011", "value": "CNE Suministro 2011"},
                {"text": "NEC", "value": "NEC"},
                {"text": "IEC", "value": "IEC"},
                {"text": "Otra", "value": "OTRA"}
            ], 'estado': estado}
        
        # ============================================
        # ETAPA: Normativa
        # ============================================
        elif etapa == "normativa":
            if mensaje == "OTRA":
                estado["etapa"] = "normativa_custom"
                return {'success': True, 'respuesta': "📜 **Especifica la normativa:**", 'botones': None, 'estado': estado}
            else:
                estado["normativa"] = mensaje
                estado["etapa"] = "fecha_inicio"
                return {'success': True, 'respuesta': f"""✅ Normativa: **{mensaje}**

📅 **¿Fecha de inicio estimada?**
_Formato: DD/MM/YYYY_
_Ejemplo: 15/01/2026_""", 'botones': None, 'estado': estado}
        
        elif etapa == "normativa_custom":
            estado["normativa"] = mensaje
            estado["etapa"] = "fecha_inicio"
            return {'success': True, 'respuesta': f"""✅ Normativa: **{mensaje}**

📅 **¿Fecha de inicio estimada?**
_Formato: DD/MM/YYYY_
_Ejemplo: 15/01/2026_""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Fecha de inicio
        # ============================================
        elif etapa == "fecha_inicio":
            try:
                fecha = datetime.strptime(mensaje, "%d/%m/%Y")
                estado["fecha_inicio"] = mensaje
                estado["etapa"] = "num_fases"
                return {'success': True, 'respuesta': f"""✅ Inicio: **{mensaje}**

🔢 **¿Cuántas fases tendrá el proyecto?**
_Recomendado: 3-7 fases_""", 'botones': [
                    {"text": "3 fases", "value": "3"},
                    {"text": "4 fases", "value": "4"},
                    {"text": "5 fases", "value": "5"},
                    {"text": "6 fases", "value": "6"},
                    {"text": "7 fases", "value": "7"}
                ], 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Fecha inválida. Usa formato DD/MM/YYYY (Ejemplo: 15/01/2026)", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Número de fases
        # ============================================
        elif etapa == "num_fases":
            try:
                num_fases = int(mensaje)
                if num_fases < 3 or num_fases > 7:
                    return {'success': False, 'respuesta': "❌ Por favor selecciona entre 3 y 7 fases", 'botones': None, 'estado': estado}
                
                # ✅ PILI GENERA LAS FASES AUTOMÁTICAMENTE
                fases_generadas = self._generar_fases_automaticas(num_fases, estado)
                estado["fases"] = fases_generadas
                estado["num_fases"] = num_fases
                
                # Mostrar fases generadas como confirmación
                mensaje_fases = f"""✅ Perfecto. Como experta en proyectos eléctricos, he planificado **{num_fases} fases** profesionales basadas en mejores prácticas.

Las fases aparecen arriba con todos los detalles. Puedes revisarlas y confirmar cuando estés listo.

Una vez que confirmes, continuaremos con la información del equipo del proyecto."""
                
                estado["etapa"] = "confirmar_fases"
                return {'success': True, 'respuesta': mensaje_fases, 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Número inválido", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Confirmar fases
        # ============================================
        elif etapa == "confirmar_fases":
            # Usuario confirmó las fases, continuar con jefe de proyecto
            estado["etapa"] = "jefe_proyecto"
            return {'success': True, 'respuesta': """✅ Perfecto. Las fases han sido confirmadas.

Ahora necesito información sobre el equipo del proyecto.

👤 **¿Nombre del Jefe de Proyecto?**
_Ejemplo: Ing. Carlos Rodríguez_""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Jefe de proyecto
        # ============================================
        elif etapa == "jefe_proyecto":
            estado["jefe_proyecto"] = mensaje
            estado["etapa"] = "recursos_humanos"
            return {'success': True, 'respuesta': f"""✅ Jefe de Proyecto: **{mensaje}**

👥 **Equipo humano necesario (separados por coma):**
_Ejemplo: Ingeniero Residente, Técnicos Electricistas (3), Inspector de Calidad_""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Recursos humanos
        # ============================================
        elif etapa == "recursos_humanos":
            recursos = [r.strip() for r in mensaje.split(',') if r.strip()]
            estado["recursos_humanos"] = recursos
            estado["etapa"] = "materiales"
            return {'success': True, 'respuesta': f"""✅ Equipo: **{len(recursos)} roles** definidos

🔧 **Materiales principales (separados por coma):**
_Ejemplo: Cables THW, Tableros eléctricos, Protecciones termomagnéticas, Sistema de puesta a tierra_""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Materiales
        # ============================================
        elif etapa == "materiales":
            materiales = [m.strip() for m in mensaje.split(',') if m.strip()]
            estado["materiales"] = materiales
            return self._generar_proyecto(estado)
        
        # ============================================
        # ETAPA: Proyecto generado
        # ============================================
        elif etapa == "proyecto":
            if mensaje == "REINICIAR": return self.procesar("", None)
            return {'success': True, 'respuesta': "¡Gracias!", 'botones': None, 'estado': estado}
        
        return {'success': False, 'respuesta': 'Error', 'botones': None, 'estado': estado}
    
    def _generar_fases_automaticas(self, num_fases: int, estado: dict) -> list:
        """Genera fases automáticamente según mejores prácticas"""
        
        # Templates de fases según número
        templates = {
            3: [
                {"nombre": "Ingeniería y Diseño", "descripcion": "Levantamiento de información, elaboración de planos eléctricos, cálculos de carga y especificaciones técnicas", "duracion": "10 días", "responsable": "Ingeniero Proyectista"},
                {"nombre": "Ejecución e Instalación", "descripcion": "Adquisición de materiales, montaje de tableros, tendido de cables, instalación de equipos y sistema de puesta a tierra", "duracion": "20 días", "responsable": "Ingeniero Residente"},
                {"nombre": "Pruebas y Entrega", "descripcion": "Pruebas eléctricas, mediciones, certificación, documentación as-built y capacitación al cliente", "duracion": "5 días", "responsable": "Inspector de Calidad"}
            ],
            4: [
                {"nombre": "Planificación y Diseño", "descripcion": "Levantamiento de información, elaboración de planos eléctricos y especificaciones técnicas", "duracion": "10 días", "responsable": "Ingeniero Proyectista"},
                {"nombre": "Adquisiciones", "descripcion": "Cotización, selección de proveedores, compra de materiales y recepción de equipos", "duracion": "7 días", "responsable": "Jefe de Compras"},
                {"nombre": "Instalación", "descripcion": "Montaje de tableros, tendido de cables, instalación de equipos y sistema de puesta a tierra", "duracion": "15 días", "responsable": "Ingeniero Residente"},
                {"nombre": "Pruebas y Cierre", "descripcion": "Pruebas eléctricas, certificación, documentación as-built y entrega formal", "duracion": "5 días", "responsable": "Inspector de Calidad"}
            ],
            5: [
                {"nombre": "Planificación y Diseño", "descripcion": "Levantamiento de información, elaboración de planos eléctricos, cálculos de carga y especificaciones técnicas", "duracion": "10 días", "responsable": "Ingeniero Proyectista"},
                {"nombre": "Adquisiciones", "descripcion": "Cotización de materiales, selección de proveedores, compra de equipos y recepción de materiales", "duracion": "7 días", "responsable": "Jefe de Compras"},
                {"nombre": "Instalación", "descripcion": "Montaje de tableros eléctricos, tendido de cables, instalación de equipos y sistema de puesta a tierra", "duracion": "15 días", "responsable": "Ingeniero Residente"},
                {"nombre": "Pruebas y Comisionamiento", "descripcion": "Pruebas eléctricas, mediciones de aislamiento, ajustes finales y certificación del sistema", "duracion": "5 días", "responsable": "Inspector de Calidad"},
                {"nombre": "Entrega y Cierre", "descripcion": "Documentación as-built, capacitación al cliente, entrega formal y activación de garantías", "duracion": "3 días", "responsable": "Jefe de Proyecto"}
            ],
            6: [
                {"nombre": "Ingeniería Básica", "descripcion": "Levantamiento de información y diseño conceptual del sistema eléctrico", "duracion": "5 días", "responsable": "Ingeniero Proyectista"},
                {"nombre": "Ingeniería de Detalle", "descripcion": "Planos ejecutivos, cálculos detallados y especificaciones técnicas completas", "duracion": "8 días", "responsable": "Ingeniero Proyectista"},
                {"nombre": "Adquisiciones", "descripcion": "Cotización, compra y recepción de materiales y equipos certificados", "duracion": "7 días", "responsable": "Jefe de Compras"},
                {"nombre": "Instalación", "descripcion": "Montaje de tableros, tendido de cables e instalación completa del sistema", "duracion": "15 días", "responsable": "Ingeniero Residente"},
                {"nombre": "Pruebas y Certificación", "descripcion": "Pruebas eléctricas completas, mediciones y certificación oficial", "duracion": "5 días", "responsable": "Inspector de Calidad"},
                {"nombre": "Entrega y Cierre", "descripcion": "Documentación final, capacitación y entrega formal del proyecto", "duracion": "3 días", "responsable": "Jefe de Proyecto"}
            ],
            7: [
                {"nombre": "Ingeniería Básica", "descripcion": "Levantamiento y diseño conceptual", "duracion": "5 días", "responsable": "Ingeniero Proyectista"},
                {"nombre": "Ingeniería de Detalle", "descripcion": "Planos ejecutivos y especificaciones completas", "duracion": "8 días", "responsable": "Ingeniero Proyectista"},
                {"nombre": "Adquisiciones", "descripcion": "Compra de materiales y equipos", "duracion": "7 días", "responsable": "Jefe de Compras"},
                {"nombre": "Obras Civiles", "descripcion": "Canalizaciones, zanjas y preparación de infraestructura", "duracion": "5 días", "responsable": "Capataz de Obra"},
                {"nombre": "Instalación Eléctrica", "descripcion": "Montaje de tableros, tendido de cables e instalación de equipos", "duracion": "12 días", "responsable": "Ingeniero Residente"},
                {"nombre": "Pruebas y Certificación", "descripcion": "Pruebas completas y certificación oficial", "duracion": "5 días", "responsable": "Inspector de Calidad"},
                {"nombre": "Entrega y Cierre", "descripcion": "Documentación, capacitación y entrega formal", "duracion": "3 días", "responsable": "Jefe de Proyecto"}
            ]
        }
        
        return templates.get(num_fases, templates[5])  # Default a 5 fases
        
    def _generar_proyecto(self, estado: Dict) -> Dict:
        # Datos del cliente y proyecto
        cliente = estado.get("cliente_nombre", "Cliente")
        nombre = estado.get("proyecto_nombre", "Proyecto")
        presupuesto = estado.get("presupuesto", 0)
        moneda = estado.get("moneda", "PEN")
        ubicacion = estado.get("ubicacion", "Por definir")
        area = estado.get("area", 0)
        descripcion = estado.get("descripcion", "Proyecto de instalación eléctrica")
        normativa = estado.get("normativa", "CNE Suministro 2011")
        jefe = estado.get("jefe_proyecto", "Por asignar")
        
        fecha_inicio = datetime.strptime(estado.get("fecha_inicio", "01/01/2026"), "%d/%m/%Y")
        
        # Calcular duración total
        fases = estado.get("fases", [])
        duracion_total = sum(int(''.join(filter(str.isdigit, f.get('duracion', '0')))) for f in fases)
        fecha_fin = fecha_inicio + timedelta(days=duracion_total)
        
        # Código proyecto
        codigo = f"PROY-ELEC-{fecha_inicio.year}-{self.contador:03d}"
        self.contador += 1
        
        # Símbolos de moneda
        simbolos_moneda = {'PEN': 'S/', 'USD': '$', 'EUR': '€'}
        
        # Resumen ejecutivo
        resumen = f"""{descripcion}

El proyecto se desarrollará en {ubicacion}, abarcando un área de {area}m².

ALCANCE:
• Diseño e ingeniería eléctrica según {normativa}
• Suministro de materiales certificados
• Instalación completa del sistema eléctrico
• Pruebas y puesta en marcha
• Documentación técnica (planos as-built)
• Capacitación al personal
• Garantía de 12 meses

Presupuesto estimado: {simbolos_moneda.get(moneda, 'S/')} {presupuesto:,.2f}
El proyecto cumplirá con {normativa}."""
        
        # Recursos
        recursos_humanos = estado.get("recursos_humanos", [
            "Jefe de Proyecto (25% dedicación)",
            "Ingeniero Residente (100% dedicación)",
            "Técnicos Instaladores (3 personas)",
            "Inspector de Calidad (50% dedicación)"
        ])
        
        materiales = estado.get("materiales", [
            "Cables eléctricos THW",
            "Tableros eléctricos",
            "Protecciones termomagnéticas",
            "Sistema de puesta a tierra",
            "Equipos de medición"
        ])
        
        # FORMATO EXACTO PARA EDITABLE_PROYECTO_SIMPLE
        datos_generados = {
            "numero": codigo,
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "cliente": {
                "nombre": estado.get("cliente_nombre", cliente),
                "ruc": estado.get("cliente_ruc", ""),
                "direccion": estado.get("cliente_direccion", ""),
                "telefono": estado.get("cliente_telefono", ""),
                "email": estado.get("cliente_email", "")
            },
            "nombre_proyecto": nombre,
            "resumen": resumen,
            "fases": fases,
            "cronograma": {
                "fecha_inicio": estado.get("fecha_inicio"),
                "fecha_fin": fecha_fin.strftime("%d/%m/%Y"),
                "duracion_total": f"{duracion_total} días"
            },
            "recursos": {
                "humanos": recursos_humanos,
                "materiales": materiales
            },
            # Metadata adicional
            "tipo_documento": "PROYECTO_SIMPLE",
            "servicio": "electricidad",
            "ubicacion": ubicacion,
            "area_m2": area,
            "presupuesto": presupuesto,
            "moneda": moneda,
            "normativa": normativa
        }
        
        estado["etapa"] = "proyecto"
        simbolo = {'PEN': 'S/', 'USD': '$', 'EUR': '€'}.get(moneda, 'S/')
        return {'success': True, 'respuesta': f"""📊 **PLAN DE PROYECTO GENERADO**

━━━━━━━━━━━━━━━━━━━━━━━
**INFORMACIÓN DEL PROYECTO:**
• Código: {codigo}
• Proyecto: {nombre}
• Cliente: {cliente}
• Ubicación: {ubicacion}
• Área: {area}m²
• Normativa: {normativa}

**CRONOGRAMA:**
• Duración: {duracion_total} días
• Inicio: {estado.get('fecha_inicio')}
• Fin: {fecha_fin.strftime("%d/%m/%Y")}

**PRESUPUESTO:**
• Total: {simbolo} {presupuesto:,.2f}

**FASES:** {len(fases)} fases detalladas
**RECURSOS:** {len(recursos_humanos)} roles, {len(materiales)} materiales
━━━━━━━━━━━━━━━━━━━━━━━

✅ Documento completo listo para generar

¿Qué deseas hacer?""", 'botones': [{"text": "📄 Generar documento", "value": "GENERAR"}, {"text": "🔄 Nueva", "value": "REINICIAR"}], 'estado': estado, 'cotizacion': datos_generados, 'datos_generados': datos_generados}
