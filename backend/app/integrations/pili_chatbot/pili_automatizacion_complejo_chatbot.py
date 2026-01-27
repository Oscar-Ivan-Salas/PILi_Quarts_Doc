"""🏭 PILI AUTOMATIZACIÓN INDUSTRIAL COMPLEJO v2.0"""
from typing import Dict, Optional

class PILIAutomatizacionComplejoChatBot:
    def __init__(self):
        self.kb = {"tipos": {"PLC": {"n": "Control con PLC", "p": 3500, "norm": "IEC 61131-3"}, "SCADA": {"n": "Sistema SCADA", "p": 8500, "norm": "ISA-95"}, "HMI": {"n": "Interfaz HMI", "p": 2200, "norm": "IEC 62264"}}}
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None: estado = {"etapa": "inicial"}
        etapa = estado.get("etapa")
        
        if etapa == "inicial":
            estado["etapa"] = "tipo"
            return {'success': True, 'respuesta': """¡Hola! 👋 **Pili** - Automatización Industrial **COMPLEJA**

🏭 **COTIZACIÓN TÉCNICA DETALLADA**
✅ Diseño de lógica de control
✅ Programación PLC/SCADA
✅ Integración de sistemas
✅ Cronograma de 4 fases

**¿Qué sistema necesitas?**""", 'botones': [{"text": "⚙️ PLC", "value": "PLC"}, {"text": "🖥️ SCADA", "value": "SCADA"}, {"text": "📊 HMI", "value": "HMI"}], 'estado': estado}
        
        elif etapa == "tipo":
            estado["tipo"] = mensaje
            estado["etapa"] = "puntos"
            return {'success': True, 'respuesta': f"""**Sistema:** {self.kb['tipos'][mensaje]['n']}\n\n🔢 **¿Cuántos puntos I/O?**\n_Ejemplo: 32_""", 'botones': None, 'estado': estado}
        
        elif etapa == "puntos":
            try:
                estado["puntos"] = int(mensaje)
                estado["etapa"] = "proceso"
                return {'success': True, 'respuesta': f"""✅ Puntos I/O: {int(mensaje)}\n\n📋 **Describe el proceso a automatizar:**\n_Ejemplo: Control de temperatura en línea de producción_""", 'botones': None, 'estado': estado}
            except: return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado}
        
        elif etapa == "proceso":
            estado["proceso"] = mensaje
            return self._generar_cotizacion(estado)
        
        elif etapa == "cotizacion":
            if mensaje == "REINICIAR": return self.procesar("", None)
            return {'success': True, 'respuesta': "¡Gracias!", 'botones': None, 'estado': estado}
        
        return {'success': False, 'respuesta': 'Error', 'botones': None, 'estado': estado}
    
    def _generar_cotizacion(self, estado: Dict) -> Dict:
        tipo, puntos, proceso = estado["tipo"], estado["puntos"], estado["proceso"]
        info = self.kb["tipos"][tipo]
        
        items = [
            {"descripcion": f"{info['n']} - Sistema completo", "cantidad": 1, "unidad": "sistema", "precio_unitario": info["p"]},
            {"descripcion": "Módulos I/O", "cantidad": puntos, "unidad": "punto", "precio_unitario": 85.0},
            {"descripcion": "Programación + Puesta en marcha", "cantidad": 1, "unidad": "servicio", "precio_unitario": 1500.0}
        ]
        
        subtotal = sum(i["cantidad"] * i["precio_unitario"] for i in items)
        igv, total = subtotal * 0.18, subtotal * 1.18
        
        # Cronograma
        d_ing = max(10, min(20, int(puntos / 5)))
        d_adq = max(15, min(30, int(puntos / 3)))
        d_prog = max(10, min(15, int(puntos / 4)))
        d_prue = max(5, min(10, int(puntos / 8)))
        
        desc = f"""Sistema de automatización industrial {info['n'].lower()} para: {proceso}

• {puntos} puntos de entrada/salida (I/O)
• Programación según normativa {info['norm']}
• Integración con sistemas existentes
• Pruebas y puesta en marcha
• Capacitación al personal operativo
• Documentación técnica completa

El proyecto incluye diseño de lógica de control, programación, instalación, pruebas y capacitación."""
        
        datos_generados = {
            "proyecto": {"nombre": f"Automatización Industrial - {info['n']}", "puntos_io": puntos, "proceso": proceso},
            "items": items, "subtotal": subtotal, "igv": igv, "total": total,
            "datos_tecnicos": {"tipo_sistema": tipo, "puntos_io": puntos, "normativa": info["norm"]},
            "descripcion_proyecto": desc,
            "normativa_aplicable": info["norm"],
            "dias_ingenieria": d_ing, "dias_adquisiciones": d_adq, "dias_instalacion": d_prog, "dias_pruebas": d_prue,
            "tipo_documento": "COTIZACION_COMPLEJA"
        }
        
        estado["etapa"] = "cotizacion"
        return {'success': True, 'respuesta': f"""📊 **COTIZACIÓN AUTOMATIZACIÓN COMPLETA**

**SISTEMA:** {info['n']}
**PROCESO:** {proceso}
**PUNTOS I/O:** {puntos}

**CRONOGRAMA:**
• Ingeniería: {d_ing}d | Adquisiciones: {d_adq}d
• Programación: {d_prog}d | Pruebas: {d_prue}d
**TOTAL: {d_ing+d_adq+d_prog+d_prue} días**

**INVERSIÓN:**
Subtotal: S/ {subtotal:.2f}
IGV: S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**

✅ Incluye: Diseño + Programación + Capacitación
📋 Normativa: {info['norm']}

¿Qué deseas hacer?""", 'botones': [{"text": "📅 Agendar", "value": "AGENDAR"}, {"text": "🔄 Nueva", "value": "REINICIAR"}], 'estado': estado, 'cotizacion': datos_generados, 'datos_generados': datos_generados}
