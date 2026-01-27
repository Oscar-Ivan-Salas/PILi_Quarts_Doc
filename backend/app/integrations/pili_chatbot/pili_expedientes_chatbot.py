"""📋 PILI EXPEDIENTES ChatBot"""
from typing import Dict, Optional

class PILIExpedientesChatBot:
    def __init__(self):
        self.kb = {"tipos": {"ARQUITECTURA": {"nombre": "Expediente Arquitectura", "precio": 2500.0}, "ESTRUCTURAS": {"nombre": "Expediente Estructuras", "precio": 3200.0}, "INSTALACIONES": {"nombre": "Expediente Instalaciones Eléctricas", "precio": 2800.0}}}
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None: estado = {"etapa": "inicial", "tipo": None, "area": None}
        etapa = estado.get("etapa", "inicial")
        
        if etapa == "inicial":
            estado["etapa"] = "tipo"
            return {'success': True, 'respuesta': """¡Hola! 👋 Soy **Pili**, especialista en expedientes técnicos.\n\n📋 Servicios:\n✅ Expediente de Arquitectura\n✅ Expediente de Estructuras\n✅ Expediente de Instalaciones Eléctricas\n\n**¿Qué necesitas?**""", 'botones': [{"text": "🏗️ Arquitectura", "value": "ARQUITECTURA"}, {"text": "🏢 Estructuras", "value": "ESTRUCTURAS"}, {"text": "⚡ Instalaciones", "value": "INSTALACIONES"}], 'estado': estado, 'cotizacion': None}
        elif etapa == "tipo":
            estado["tipo"] = mensaje
            estado["etapa"] = "area"
            return {'success': True, 'respuesta': f"""Expediente: **{self.kb['tipos'][mensaje]['nombre']}**\n\n📐 **¿Área del proyecto en m²?**\n_Escribe el número (ejemplo: 250)_""", 'botones': None, 'estado': estado, 'cotizacion': None}
        elif etapa == "area":
            try:
                area = float(mensaje)
                estado["area"] = area
                estado["etapa"] = "cotizacion"
                tipo = estado["tipo"]
                info = self.kb["tipos"][tipo]
                items = [{"descripcion": f"{info['nombre']} - Elaboración completa", "cantidad": 1, "unidad": "expediente", "precio_unitario": info["precio"]}, {"descripcion": "Planos y especificaciones técnicas", "cantidad": area, "unidad": "m²", "precio_unitario": 8.5}]
                subtotal = sum(i["cantidad"] * i["precio_unitario"] for i in items)
                igv = subtotal * 0.18
                total = subtotal + igv
                cotizacion = {"tipo": tipo, "area": area, "items": items, "subtotal": subtotal, "igv": igv, "total": total}
                datos_generados = {"proyecto": {"nombre": f"{info['nombre']}", "area_m2": area}, "items": items, "subtotal": subtotal, "igv": igv, "total": total}
                return {'success': True, 'respuesta': f"""📊 **COTIZACIÓN EXPEDIENTE TÉCNICO**\n\n**Tipo:** {info['nombre']}\n**Área:** {area} m²\n\n**💰 TOTAL:**\nSubtotal: S/ {subtotal:.2f}\nIGV (18%): S/ {igv:.2f}\n**TOTAL: S/ {total:.2f}**\n\n✅ Incluye planos y memoria\n⏱️ Entrega: 15-20 días\n\n¿Qué deseas hacer?""", 'botones': [{"text": "📅 Agendar", "value": "AGENDAR"}, {"text": "🔄 Nueva consulta", "value": "REINICIAR"}], 'estado': estado, 'cotizacion': cotizacion, 'datos_generados': datos_generados}
            except: return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado, 'cotizacion': None}
        elif etapa == "cotizacion":
            if mensaje == "REINICIAR": return self.procesar("", None)
            return {'success': True, 'respuesta': "¡Gracias!", 'botones': None, 'estado': estado, 'cotizacion': None}
        return {'success': False, 'respuesta': 'Error', 'botones': None, 'estado': estado, 'cotizacion': None}
