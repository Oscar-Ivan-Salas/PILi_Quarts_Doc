"""
🌐 PILI REDES ChatBot
Versión: 1.0
"""

from typing import Dict, Optional

class PILIRedesChatBot:
    def __init__(self):
        self.kb = {
            "tipos": {
                "ESTRUCTURADA": {"nombre": "Red Estructurada Cat6", "precio_punto": 85.0},
                "FIBRA": {"nombre": "Fibra Óptica", "precio_punto": 180.0},
                "WIFI": {"nombre": "Red WiFi Empresarial", "precio_ap": 450.0}
            }
        }
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None:
            estado = {"etapa": "inicial", "tipo": None, "puntos": None}
        
        etapa = estado.get("etapa", "inicial")
        
        if etapa == "inicial":
            estado["etapa"] = "tipo"
            return {'success': True, 'respuesta': """¡Hola! 👋 Soy **Pili**, tu especialista en redes de **Tesla Electricidad**.

🌐 Servicios disponibles:
✅ Red estructurada Cat6
✅ Fibra óptica
✅ WiFi empresarial

**¿Qué necesitas?**""", 'botones': [{"text": "🔌 Red Cat6", "value": "ESTRUCTURADA"}, {"text": "💡 Fibra Óptica", "value": "FIBRA"}, {"text": "📶 WiFi", "value": "WIFI"}], 'estado': estado, 'cotizacion': None}
        
        elif etapa == "tipo":
            estado["tipo"] = mensaje
            estado["etapa"] = "puntos"
            info = self.kb["tipos"][mensaje]
            pregunta = "📍 **¿Cuántos puntos de red?**" if mensaje != "WIFI" else "📶 **¿Cuántos access points?**"
            return {'success': True, 'respuesta': f"""Sistema: **{info['nombre']}**\n\n{pregunta}\n_Escribe el número (ejemplo: 20)_""", 'botones': None, 'estado': estado, 'cotizacion': None}
        
        elif etapa == "puntos":
            try:
                puntos = int(mensaje)
                estado["puntos"] = puntos
                estado["etapa"] = "cotizacion"
                
                tipo = estado["tipo"]
                info = self.kb["tipos"][tipo]
                
                items = []
                if tipo == "WIFI":
                    items.append({"descripcion": f"Access Point empresarial + instalación", "cantidad": puntos, "unidad": "unidad", "precio_unitario": info["precio_ap"]})
                    items.append({"descripcion": "Switch PoE 24 puertos", "cantidad": 1, "unidad": "unidad", "precio_unitario": 1200.0})
                else:
                    items.append({"descripcion": f"{info['nombre']} - Punto de red completo", "cantidad": puntos, "unidad": "punto", "precio_unitario": info["precio_punto"]})
                    items.append({"descripcion": "Switch 24 puertos Gigabit", "cantidad": 1, "unidad": "unidad", "precio_unitario": 850.0})
                    items.append({"descripcion": "Rack + Patch Panel", "cantidad": 1, "unidad": "unidad", "precio_unitario": 650.0})
                
                items.append({"descripcion": "Configuración + Certificación", "cantidad": 1, "unidad": "servicio", "precio_unitario": 450.0})
                
                subtotal = sum(i["cantidad"] * i["precio_unitario"] for i in items)
                igv = subtotal * 0.18
                total = subtotal + igv
                
                cotizacion = {"tipo": tipo, "puntos": puntos, "items": items, "subtotal": subtotal, "igv": igv, "total": total}
                datos_generados = {"proyecto": {"nombre": f"Red {info['nombre']}", "puntos": puntos}, "items": items, "subtotal": subtotal, "igv": igv, "total": total}
                
                return {'success': True, 'respuesta': f"""📊 **COTIZACIÓN RED DE DATOS**\n\n**Sistema:** {info['nombre']}\n**Puntos:** {puntos}\n\n**💰 TOTAL:**\nSubtotal: S/ {subtotal:.2f}\nIGV (18%): S/ {igv:.2f}\n**TOTAL: S/ {total:.2f}**\n\n✅ Incluye certificación\n⏱️ Instalación: 3-5 días\n\n¿Qué deseas hacer?""", 'botones': [{"text": "📅 Agendar", "value": "AGENDAR"}, {"text": "🔄 Nueva consulta", "value": "REINICIAR"}], 'estado': estado, 'cotizacion': cotizacion, 'datos_generados': datos_generados}
            except:
                return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado, 'cotizacion': None}
        
        elif etapa == "cotizacion":
            if mensaje == "REINICIAR":
                return self.procesar("", None)
            return {'success': True, 'respuesta': "¡Gracias!", 'botones': None, 'estado': estado, 'cotizacion': None}
        
        return {'success': False, 'respuesta': 'Error', 'botones': None, 'estado': estado, 'cotizacion': None}
