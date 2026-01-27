"""
📹 PILI CCTV ChatBot
Versión: 1.0
"""

from typing import Dict, List, Optional

class PILICCTVChatBot:
    """Caja negra para chat de Sistemas CCTV"""
    
    def __init__(self):
        self.knowledge_base = {
            "tipos": {
                "ANALOGICO": {"nombre": "Sistema Analógico HD", "precio_camara": 280.0, "dvr_4ch": 450.0, "dvr_8ch": 650.0, "dvr_16ch": 1200.0},
                "IP": {"nombre": "Sistema IP (Red)", "precio_camara": 420.0, "nvr_4ch": 650.0, "nvr_8ch": 950.0, "nvr_16ch": 1800.0},
                "HIBRIDO": {"nombre": "Sistema Híbrido", "precio_camara": 350.0, "hvr_8ch": 850.0, "hvr_16ch": 1500.0}
            }
        }
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None:
            estado = {"etapa": "inicial", "tipo": None, "camaras": None}
        
        etapa = estado.get("etapa", "inicial")
        
        if etapa == "inicial":
            return self._etapa_inicial(estado)
        elif etapa == "tipo":
            return self._etapa_tipo(mensaje, estado)
        elif etapa == "camaras":
            return self._etapa_camaras(mensaje, estado)
        elif etapa == "cotizacion":
            return self._etapa_cotizacion(mensaje, estado)
        
        return {'success': False, 'respuesta': 'Error', 'botones': None, 'estado': estado, 'cotizacion': None}
    
    def _etapa_inicial(self, estado: Dict) -> Dict:
        estado["etapa"] = "tipo"
        return {
            'success': True,
            'respuesta': """¡Hola! 👋 Soy **Pili**, tu especialista en sistemas CCTV de **Tesla Electricidad**.

📹 Sistemas disponibles:
✅ Analógico HD (económico, calidad Full HD)
✅ IP en Red (alta resolución, acceso remoto)
✅ Híbrido (combina analógico + IP)

**¿Qué sistema necesitas?**""",
            'botones': [
                {"text": "📹 Analógico HD", "value": "ANALOGICO"},
                {"text": "🌐 IP (Red)", "value": "IP"},
                {"text": "🔄 Híbrido", "value": "HIBRIDO"}
            ],
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_tipo(self, mensaje: str, estado: Dict) -> Dict:
        estado["tipo"] = mensaje
        estado["etapa"] = "camaras"
        info = self.knowledge_base["tipos"][mensaje]
        return {
            'success': True,
            'respuesta': f"""Sistema: **{info['nombre']}**

📹 **¿Cuántas cámaras necesitas?**
_Escribe el número (ejemplo: 8)_""",
            'botones': None,
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_camaras(self, mensaje: str, estado: Dict) -> Dict:
        try:
            camaras = int(mensaje)
            if camaras <= 0:
                return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado, 'cotizacion': None}
            
            estado["camaras"] = camaras
            estado["etapa"] = "cotizacion"
            
            tipo = estado["tipo"]
            info = self.knowledge_base["tipos"][tipo]
            
            # Determinar grabador según cantidad de cámaras
            if camaras <= 4:
                grabador_key = "dvr_4ch" if tipo == "ANALOGICO" else ("nvr_4ch" if tipo == "IP" else "hvr_8ch")
                canales = "4 canales" if tipo != "HIBRIDO" else "8 canales"
            elif camaras <= 8:
                grabador_key = "dvr_8ch" if tipo == "ANALOGICO" else ("nvr_8ch" if tipo == "IP" else "hvr_8ch")
                canales = "8 canales"
            else:
                grabador_key = "dvr_16ch" if tipo == "ANALOGICO" else ("nvr_16ch" if tipo == "IP" else "hvr_16ch")
                canales = "16 canales"
            
            items = [
                {
                    "descripcion": f"Cámara {info['nombre']} con instalación",
                    "cantidad": camaras,
                    "unidad": "unidad",
                    "precio_unitario": info["precio_camara"]
                },
                {
                    "descripcion": f"Grabador {canales} + Disco 1TB",
                    "cantidad": 1,
                    "unidad": "unidad",
                    "precio_unitario": info[grabador_key]
                },
                {
                    "descripcion": "Cable UTP/Coaxial + Conectores (por cámara)",
                    "cantidad": camaras,
                    "unidad": "punto",
                    "precio_unitario": 45.0
                },
                {
                    "descripcion": "Configuración + App móvil",
                    "cantidad": 1,
                    "unidad": "servicio",
                    "precio_unitario": 250.0
                }
            ]
            
            subtotal = sum(i["cantidad"] * i["precio_unitario"] for i in items)
            igv = subtotal * 0.18
            total = subtotal + igv
            
            cotizacion = {
                "tipo": tipo,
                "camaras": camaras,
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            }
            
            datos_generados = {
                "proyecto": {"nombre": f"Sistema CCTV {info['nombre']}", "camaras": camaras},
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            }
            
            return {
                'success': True,
                'respuesta': f"""📊 **COTIZACIÓN SISTEMA CCTV**

━━━━━━━━━━━━━━━━━━━━━━━
**Sistema:** {info['nombre']}
**Cámaras:** {camaras}
**Grabador:** {canales}

**💰 TOTAL:**
Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Instalación + Configuración + App
⏱️ Instalación: 2-3 días
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
        return {'success': True, 'respuesta': "¡Gracias!", 'botones': None, 'estado': estado, 'cotizacion': None}
