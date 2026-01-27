"""💧 PILI SANEAMIENTO ChatBot"""
from typing import Dict, Optional

class PILISaneamientoChatBot:
    def __init__(self):
        self.kb = {"tipos": {"AGUA": {"nombre": "Sistema de Agua Potable", "precio_m": 45.0}, "DESAGUE": {"nombre": "Sistema de Desagüe", "precio_m": 55.0}, "PLUVIAL": {"nombre": "Sistema Pluvial", "precio_m": 50.0}}}
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None: estado = {"etapa": "inicial", "tipo": None, "metros": None}
        etapa = estado.get("etapa", "inicial")
        
        if etapa == "inicial":
            estado["etapa"] = "tipo"
            return {'success': True, 'respuesta': """¡Hola! 👋 Soy **Pili**, especialista en sistemas de saneamiento.\n\n💧 Servicios:\n✅ Sistema de Agua Potable\n✅ Sistema de Desagüe\n✅ Sistema Pluvial\n\n**¿Qué necesitas?**""", 'botones': [{"text": "💧 Agua", "value": "AGUA"}, {"text": "🚰 Desagüe", "value": "DESAGUE"}, {"text": "🌧️ Pluvial", "value": "PLUVIAL"}], 'estado': estado, 'cotizacion': None}
        elif etapa == "tipo":
            estado["tipo"] = mensaje
            estado["etapa"] = "metros"
            return {'success': True, 'respuesta': f"""Sistema: **{self.kb['tipos'][mensaje]['nombre']}**\n\n📏 **¿Metros lineales de tubería?**\n_Escribe el número (ejemplo: 80)_""", 'botones': None, 'estado': estado, 'cotizacion': None}
        elif etapa == "metros":
            try:
                metros = float(mensaje)
                estado["metros"] = metros
                estado["etapa"] = "cotizacion"
                tipo = estado["tipo"]
                info = self.kb["tipos"][tipo]
                items = [{"descripcion": f"{info['nombre']} - Tubería y accesorios", "cantidad": metros, "unidad": "metro", "precio_unitario": info["precio_m"]}, {"descripcion": "Excavación y relleno", "cantidad": metros, "unidad": "metro", "precio_unitario": 25.0}, {"descripcion": "Pruebas hidráulicas", "cantidad": 1, "unidad": "servicio", "precio_unitario": 350.0}]
                subtotal = sum(i["cantidad"] * i["precio_unitario"] for i in items)
                igv = subtotal * 0.18
                total = subtotal + igv
                cotizacion = {"tipo": tipo, "metros": metros, "items": items, "subtotal": subtotal, "igv": igv, "total": total}
                datos_generados = {"proyecto": {"nombre": f"{info['nombre']}", "metros_lineales": metros}, "items": items, "subtotal": subtotal, "igv": igv, "total": total}
                return {'success': True, 'respuesta': f"""📊 **COTIZACIÓN SANEAMIENTO**\n\n**Sistema:** {info['nombre']}\n**Metros:** {metros} ml\n\n**💰 TOTAL:**\nSubtotal: S/ {subtotal:.2f}\nIGV (18%): S/ {igv:.2f}\n**TOTAL: S/ {total:.2f}**\n\n✅ Incluye pruebas\n⏱️ Instalación: 4-6 días\n\n¿Qué deseas hacer?""", 'botones': [{"text": "📅 Agendar", "value": "AGENDAR"}, {"text": "🔄 Nueva consulta", "value": "REINICIAR"}], 'estado': estado, 'cotizacion': cotizacion, 'datos_generados': datos_generados}
            except: return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado, 'cotizacion': None}
        elif etapa == "cotizacion":
            if mensaje == "REINICIAR": return self.procesar("", None)
            return {'success': True, 'respuesta': "¡Gracias!", 'botones': None, 'estado': estado, 'cotizacion': None}
        return {'success': False, 'respuesta': 'Error', 'botones': None, 'estado': estado, 'cotizacion': None}
