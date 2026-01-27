"""
🏠 PILI DOMÓTICA ChatBot
Versión: 1.0
"""

from typing import Dict, List, Optional

class PILIDomoticaChatBot:
    """Caja negra para chat de Sistemas de Domótica"""
    
    def __init__(self):
        self.knowledge_base = {
            "sistemas": {
                "ILUMINACION": {"nombre": "Control de Iluminación", "precio_punto": 120.0},
                "CLIMATIZACION": {"nombre": "Control de Climatización", "precio_zona": 450.0},
                "SEGURIDAD": {"nombre": "Sistema de Seguridad Inteligente", "precio_sensor": 180.0},
                "CORTINAS": {"nombre": "Cortinas Automatizadas", "precio_motor": 350.0},
                "COMPLETO": {"nombre": "Sistema Completo Integrado", "precio_m2": 95.0}
            }
        }
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None:
            estado = {"etapa": "inicial", "sistema": None, "cantidad": None}
        
        etapa = estado.get("etapa", "inicial")
        
        if etapa == "inicial":
            return self._etapa_inicial(estado)
        elif etapa == "sistema":
            return self._etapa_sistema(mensaje, estado)
        elif etapa == "cantidad":
            return self._etapa_cantidad(mensaje, estado)
        elif etapa == "cotizacion":
            return self._etapa_cotizacion(mensaje, estado)
        
        return {'success': False, 'respuesta': 'Error', 'botones': None, 'estado': estado, 'cotizacion': None}
    
    def _etapa_inicial(self, estado: Dict) -> Dict:
        estado["etapa"] = "sistema"
        return {
            'success': True,
            'respuesta': """¡Hola! 👋 Soy **Pili**, tu especialista en domótica de **Tesla Electricidad**.

🏠 Sistemas disponibles:
✅ Control de iluminación inteligente
✅ Climatización automatizada
✅ Seguridad con sensores IoT
✅ Cortinas motorizadas
✅ Sistema completo integrado

**¿Qué sistema necesitas?**""",
            'botones': [
                {"text": "💡 Iluminación", "value": "ILUMINACION"},
                {"text": "❄️ Climatización", "value": "CLIMATIZACION"},
                {"text": "🔒 Seguridad", "value": "SEGURIDAD"},
                {"text": "🪟 Cortinas", "value": "CORTINAS"},
                {"text": "🏠 Sistema Completo", "value": "COMPLETO"}
            ],
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_sistema(self, mensaje: str, estado: Dict) -> Dict:
        estado["sistema"] = mensaje
        estado["etapa"] = "cantidad"
        
        info = self.knowledge_base["sistemas"][mensaje]
        
        if mensaje == "COMPLETO":
            pregunta = "📐 **¿Cuál es el área total en m²?**\n_Escribe el número (ejemplo: 150)_"
        elif mensaje == "ILUMINACION":
            pregunta = "💡 **¿Cuántos puntos de luz quieres automatizar?**\n_Escribe el número (ejemplo: 15)_"
        elif mensaje == "CLIMATIZACION":
            pregunta = "❄️ **¿Cuántas zonas de climatización?**\n_Escribe el número (ejemplo: 3)_"
        elif mensaje == "SEGURIDAD":
            pregunta = "🔒 **¿Cuántos sensores necesitas?**\n_Escribe el número (ejemplo: 8)_"
        else:  # CORTINAS
            pregunta = "🪟 **¿Cuántas cortinas a motorizar?**\n_Escribe el número (ejemplo: 6)_"
        
        return {
            'success': True,
            'respuesta': f"""Sistema: **{info['nombre']}**

{pregunta}""",
            'botones': None,
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_cantidad(self, mensaje: str, estado: Dict) -> Dict:
        try:
            cantidad = float(mensaje)
            estado["cantidad"] = cantidad
            estado["etapa"] = "cotizacion"
            
            sistema = estado["sistema"]
            info = self.knowledge_base["sistemas"][sistema]
            
            # Calcular precio
            if sistema == "COMPLETO":
                precio_unitario = info["precio_m2"]
                unidad = "m²"
            elif sistema == "ILUMINACION":
                precio_unitario = info["precio_punto"]
                unidad = "punto"
            elif sistema == "CLIMATIZACION":
                precio_unitario = info["precio_zona"]
                unidad = "zona"
            elif sistema == "SEGURIDAD":
                precio_unitario = info["precio_sensor"]
                unidad = "sensor"
            else:  # CORTINAS
                precio_unitario = info["precio_motor"]
                unidad = "motor"
            
            items = [{
                "descripcion": f"{info['nombre']} - Instalación completa",
                "cantidad": cantidad,
                "unidad": unidad,
                "precio_unitario": precio_unitario
            }]
            
            # Agregar central de control
            items.append({
                "descripcion": "Central de control domótico + App móvil",
                "cantidad": 1,
                "unidad": "unidad",
                "precio_unitario": 850.0
            })
            
            subtotal = sum(i["cantidad"] * i["precio_unitario"] for i in items)
            igv = subtotal * 0.18
            total = subtotal + igv
            
            cotizacion = {
                "sistema": sistema,
                "cantidad": cantidad,
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            }
            
            datos_generados = {
                "proyecto": {"nombre": f"Sistema Domótico - {info['nombre']}", "cantidad": cantidad},
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            }
            
            return {
                'success': True,
                'respuesta': f"""📊 **COTIZACIÓN SISTEMA DOMÓTICO**

━━━━━━━━━━━━━━━━━━━━━━━
**Sistema:** {info['nombre']}
**Cantidad:** {cantidad} {unidad}

**💰 TOTAL:**
Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye central de control + App móvil
⏱️ Instalación: 3-5 días
🎁 Capacitación incluida

¿Qué deseas hacer?""",
                'botones': [
                    {"text": "📅 Agendar", "value": "AGENDAR"},
                    {"text": "🔄 Nueva consulta", "value": "REINICIAR"}
                ],
                'estado': estado,
                'cotizacion': cotizacion,
                'datos_generados': datos_generados
            }
        except:
            return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado, 'cotizacion': None}
    
    def _etapa_cotizacion(self, mensaje: str, estado: Dict) -> Dict:
        if mensaje == "REINICIAR":
            return self.procesar("", None)
        return {'success': True, 'respuesta': "¡Gracias por tu interés!", 'botones': None, 'estado': estado, 'cotizacion': None}
