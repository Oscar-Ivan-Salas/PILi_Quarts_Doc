"""🏭 PILI AUTOMATIZACIÓN ChatBot"""
from typing import Dict, Optional

class PILIAutomatizacionChatBot:
    def __init__(self):
        self.kb = {"tipos": {"PLC": {"nombre": "Control con PLC", "precio_base": 3500.0}, "SCADA": {"nombre": "Sistema SCADA", "precio_base": 8500.0}, "HMI": {"nombre": "Interfaz HMI", "precio_base": 2200.0}}}
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None: estado = {"etapa": "inicial", "tipo": None, "puntos": None}
        etapa = estado.get("etapa", "inicial")
        
        if etapa == "inicial":
            estado["etapa"] = "tipo"
            return {'success': True, 'respuesta': """¡Hola! 👋 Soy **Pili**, especialista en automatización industrial.\n\n🏭 Sistemas:\n✅ Control con PLC\n✅ Sistema SCADA\n✅ Interfaz HMI\n\n**¿Qué necesitas?**""", 'botones': [{"text": "⚙️ PLC", "value": "PLC"}, {"text": "🖥️ SCADA", "value": "SCADA"}, {"text": "📊 HMI", "value": "HMI"}], 'estado': estado, 'cotizacion': None}
        elif etapa == "tipo":
            estado["tipo"] = mensaje
            estado["etapa"] = "puntos"
            return {'success': True, 'respuesta': f"""Sistema: **{self.kb['tipos'][mensaje]['nombre']}**\n\n🔢 **¿Cuántos puntos I/O?**\n_Escribe el número (ejemplo: 32)_""", 'botones': None, 'estado': estado, 'cotizacion': None}
        elif etapa == "puntos":
            try:
                puntos = int(mensaje)
                estado["puntos"] = puntos
                estado["etapa"] = "cotizacion"
                tipo = estado["tipo"]
                info = self.kb["tipos"][tipo]
                items = [{"descripcion": f"{info['nombre']} - Sistema completo", "cantidad": 1, "unidad": "sistema", "precio_unitario": info["precio_base"]}, {"descripcion": "Módulos I/O", "cantidad": puntos, "unidad": "punto", "precio_unitario": 85.0}, {"descripcion": "Programación + Puesta en marcha", "cantidad": 1, "unidad": "servicio", "precio_unitario": 1500.0}]
                subtotal = sum(i["cantidad"] * i["precio_unitario"] for i in items)
                igv = subtotal * 0.18
                total = subtotal + igv
                cotizacion = {"tipo": tipo, "puntos": puntos, "items": items, "subtotal": subtotal, "igv": igv, "total": total}
                datos_generados = {"proyecto": {"nombre": f"Automatización {info['nombre']}", "puntos_io": puntos}, "items": items, "subtotal": subtotal, "igv": igv, "total": total}
                return {'success': True, 'respuesta': f"""📊 **COTIZACIÓN AUTOMATIZACIÓN**\n\n**Sistema:** {info['nombre']}\n**Puntos I/O:** {puntos}\n\n**💰 TOTAL:**\nSubtotal: S/ {subtotal:.2f}\nIGV (18%): S/ {igv:.2f}\n**TOTAL: S/ {total:.2f}**\n\n✅ Incluye programación\n⏱️ Implementación: 5-7 días\n\n¿Qué deseas hacer?""", 'botones': [{"text": "📅 Agendar", "value": "AGENDAR"}, {"text": "🔄 Nueva consulta", "value": "REINICIAR"}], 'estado': estado, 'cotizacion': cotizacion, 'datos_generados': datos_generados}
            except: return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado, 'cotizacion': None}
        elif etapa == "cotizacion":
            if mensaje == "REINICIAR": return self.procesar("", None)
            return {'success': True, 'respuesta': "¡Gracias!", 'botones': None, 'estado': estado, 'cotizacion': None}
        return {'success': False, 'respuesta': 'Error', 'botones': None, 'estado': estado, 'cotizacion': None}
