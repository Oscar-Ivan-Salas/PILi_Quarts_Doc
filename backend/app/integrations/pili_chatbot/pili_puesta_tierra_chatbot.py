"""
🤖 PILI PUESTA A TIERRA ChatBot - Caja Negra
Versión: 1.0
Patrón: Basado en ITSE y Electricidad
"""

from typing import Dict, List, Optional

class PILIPuestaTierraChatBot:
    """Caja negra para chat de Puesta a Tierra"""
    
    def __init__(self):
        """Inicializa la base de conocimiento de puesta a tierra"""
        self.knowledge_base = {
            "tipos_instalacion": {
                "RESIDENCIAL": {
                    "icon": "🏠",
                    "nombre": "Residencial",
                    "precio_pozo": 1760.0,
                    "precio_varilla": 85.0,
                    "precio_cable_m": 12.0
                },
                "COMERCIAL": {
                    "icon": "🏪",
                    "nombre": "Comercial",
                    "precio_pozo": 2200.0,
                    "precio_varilla": 85.0,
                    "precio_cable_m": 12.0
                },
                "INDUSTRIAL": {
                    "icon": "🏭",
                    "nombre": "Industrial",
                    "precio_pozo": 3500.0,
                    "precio_varilla": 85.0,
                    "precio_cable_m": 15.0
                }
            }
        }
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None:
            estado = {
                "etapa": "inicial",
                "tipo": None,
                "pozos": None,
                "varillas_por_pozo": None
            }
        
        etapa = estado.get("etapa", "inicial")
        
        if etapa == "inicial":
            return self._etapa_inicial(estado)
        elif etapa == "tipo":
            return self._etapa_tipo(mensaje, estado)
        elif etapa == "pozos":
            return self._etapa_pozos(mensaje, estado)
        elif etapa == "varillas":
            return self._etapa_varillas(mensaje, estado)
        elif etapa == "cotizacion":
            return self._etapa_cotizacion(mensaje, estado)
        else:
            return {'success': False, 'respuesta': 'Error: Etapa desconocida', 'botones': None, 'estado': estado, 'cotizacion': None}
    
    def _etapa_inicial(self, estado: Dict) -> Dict:
        estado["etapa"] = "tipo"
        
        botones = [
            {"text": "🏠 Residencial", "value": "RESIDENCIAL"},
            {"text": "🏪 Comercial", "value": "COMERCIAL"},
            {"text": "🏭 Industrial", "value": "INDUSTRIAL"}
        ]
        
        return {
            'success': True,
            'respuesta': """¡Hola! 👋 Soy **Pili**, tu especialista en sistemas de puesta a tierra de **Tesla Electricidad - Huancayo**.

🔌 Te ayudo a cotizar tu sistema de puesta a tierra con:
✅ Pozos de tierra profesionales
✅ Varillas copperweld de alta calidad
✅ Medición de resistividad incluida
✅ Certificado de conformidad

**¿Qué tipo de instalación necesitas?**""",
            'botones': botones,
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_tipo(self, mensaje: str, estado: Dict) -> Dict:
        tipo = mensaje
        estado["tipo"] = tipo
        estado["etapa"] = "pozos"
        
        info = self.knowledge_base["tipos_instalacion"][tipo]
        
        return {
            'success': True,
            'respuesta': f"""Perfecto, instalación **{info['nombre']}** {info['icon']}

🔧 **¿Cuántos pozos de tierra necesitas?**

_Sugerencia: 1 pozo para instalaciones pequeñas, 2-3 para medianas, 4+ para grandes_
_Escribe el número (ejemplo: 2)_""",
            'botones': None,
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_pozos(self, mensaje: str, estado: Dict) -> Dict:
        try:
            pozos = int(mensaje)
            if pozos <= 0:
                return {'success': False, 'respuesta': "Por favor ingresa un número válido de pozos", 'botones': None, 'estado': estado, 'cotizacion': None}
            
            estado["pozos"] = pozos
            estado["etapa"] = "varillas"
            
            return {
                'success': True,
                'respuesta': f"""🔧 Pozos de tierra: **{pozos}**

⚡ **¿Cuántas varillas copperweld por pozo?**

_Sugerencia: 1-2 varillas para suelos de baja resistividad, 3-4 para alta resistividad_
_Escribe el número (ejemplo: 3)_""",
                'botones': None,
                'estado': estado,
                'cotizacion': None
            }
        except ValueError:
            return {'success': False, 'respuesta': "Por favor ingresa un número válido", 'botones': None, 'estado': estado, 'cotizacion': None}
    
    def _etapa_varillas(self, mensaje: str, estado: Dict) -> Dict:
        try:
            varillas = int(mensaje)
            if varillas <= 0:
                return {'success': False, 'respuesta': "Por favor ingresa un número válido de varillas", 'botones': None, 'estado': estado, 'cotizacion': None}
            
            estado["varillas_por_pozo"] = varillas
            estado["etapa"] = "cotizacion"
            
            cotizacion = self._generar_cotizacion(estado)
            
            respuesta = f"""📊 **COTIZACIÓN SISTEMA PUESTA A TIERRA**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 RESUMEN DEL PROYECTO:**

🏠 Tipo: **{self.knowledge_base['tipos_instalacion'][estado['tipo']]['nombre']}**
🔧 Pozos de tierra: **{estado['pozos']}**
⚡ Varillas por pozo: **{estado['varillas_por_pozo']}**

━━━━━━━━━━━━━━━━━━━━━━━
**💰 TOTAL:**

Subtotal: S/ {cotizacion['subtotal']:.2f}
IGV (18%): S/ {cotizacion['igv']:.2f}
**TOTAL: S/ {cotizacion['total']:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

⏱️ **Tiempo de instalación:** 2-3 días
✅ **Garantía:** 3 años
🎁 **Incluye:** Medición de resistividad + Certificado

¿Qué deseas hacer?"""
            
            botones = [
                {"text": "📅 Agendar instalación", "value": "AGENDAR"},
                {"text": "💬 Más información", "value": "INFO"},
                {"text": "🔄 Nueva consulta", "value": "REINICIAR"}
            ]
            
            datos_generados = {
                "proyecto": {
                    "nombre": f"Sistema Puesta a Tierra {estado['tipo'].title()}",
                    "pozos": estado["pozos"],
                    "varillas_por_pozo": varillas
                },
                "items": cotizacion["items"],
                "subtotal": cotizacion["subtotal"],
                "igv": cotizacion["igv"],
                "total": cotizacion["total"]
            }
            
            return {
                'success': True,
                'respuesta': respuesta,
                'botones': botones,
                'estado': estado,
                'cotizacion': cotizacion,
                'datos_generados': datos_generados
            }
        except ValueError:
            return {'success': False, 'respuesta': "Por favor ingresa un número válido", 'botones': None, 'estado': estado, 'cotizacion': None}
    
    def _etapa_cotizacion(self, mensaje: str, estado: Dict) -> Dict:
        if mensaje == "REINICIAR":
            return self.procesar("", None)
        elif mensaje == "INFO":
            return {
                'success': True,
                'respuesta': """📞 **Puedes contactarnos:**

**WhatsApp:** 906 315 961
**Email:** ingenieria.teslaelectricidad@gmail.com
**Dirección:** Jr. Los Narcisos Mz H lote 4, Huancayo

⚡ **Nuestros servicios incluyen:**
✅ Diseño del sistema de puesta a tierra
✅ Instalación completa con materiales de primera
✅ Medición de resistividad del terreno
✅ Certificado de conformidad
✅ Garantía de 3 años

¿Deseas agendar la instalación?""",
                'botones': [
                    {"text": "✅ Sí, agendar", "value": "AGENDAR"},
                    {"text": "🔄 Nueva consulta", "value": "REINICIAR"}
                ],
                'estado': estado,
                'cotizacion': None
            }
        elif mensaje == "AGENDAR":
            return {
                'success': True,
                'respuesta': """✅ **¡Excelente decisión!**

Nos comunicaremos contigo en las próximas 2 horas para coordinar la visita técnica y medición de resistividad.

📞 WhatsApp: 906 315 961

¡Gracias por confiar en Tesla Electricidad! ⚡""",
                'botones': [{"text": "🏠 Inicio", "value": "REINICIAR"}],
                'estado': estado,
                'cotizacion': None
            }
        
        return {'success': False, 'respuesta': "Opción no válida", 'botones': None, 'estado': estado, 'cotizacion': None}
    
    def _generar_cotizacion(self, estado: Dict) -> Dict:
        tipo = estado["tipo"]
        pozos = estado["pozos"]
        varillas_por_pozo = estado["varillas_por_pozo"]
        
        info = self.knowledge_base["tipos_instalacion"][tipo]
        
        items = []
        
        # Pozos de tierra
        items.append({
            "descripcion": f"Pozo de tierra completo (excavación, material conductivo, compactación)",
            "cantidad": pozos,
            "unidad": "unidad",
            "precio_unitario": info["precio_pozo"]
        })
        
        # Varillas
        total_varillas = pozos * varillas_por_pozo
        items.append({
            "descripcion": "Varilla copperweld 5/8\" x 2.4m",
            "cantidad": total_varillas,
            "unidad": "unidad",
            "precio_unitario": info["precio_varilla"]
        })
        
        # Cable
        cable_metros = pozos * 15  # 15m de cable por pozo
        items.append({
            "descripcion": "Cable desnudo de cobre temple suave",
            "cantidad": cable_metros,
            "unidad": "metro",
            "precio_unitario": info["precio_cable_m"]
        })
        
        # Mano de obra
        mano_obra = pozos * 350  # S/ 350 por pozo
        items.append({
            "descripcion": "Mano de obra especializada (instalación + medición)",
            "cantidad": pozos,
            "unidad": "pozo",
            "precio_unitario": 350.0
        })
        
        subtotal = sum(item["cantidad"] * item["precio_unitario"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            "tipo": tipo,
            "pozos": pozos,
            "varillas_por_pozo": varillas_por_pozo,
            "items": items,
            "subtotal": subtotal,
            "igv": igv,
            "total": total
        }


if __name__ == "__main__":
    chatbot = PILIPuestaTierraChatBot()
    
    print("=== TEST PILI PUESTA A TIERRA ChatBot ===\n")
    
    resultado = chatbot.procesar("", None)
    print(f"Bot: {resultado['respuesta']}\n")
    
    resultado = chatbot.procesar("COMERCIAL", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    
    resultado = chatbot.procesar("2", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    
    resultado = chatbot.procesar("3", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    print(f"Total: S/ {resultado['cotizacion']['total']:.2f}")
