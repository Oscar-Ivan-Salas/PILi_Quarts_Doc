"""
🔥 PILI CONTRA INCENDIOS ChatBot
Versión: 1.0
"""

from typing import Dict, List, Optional

class PILIContraIncendiosChatBot:
    """Caja negra para chat de Sistemas Contra Incendios"""
    
    def __init__(self):
        self.knowledge_base = {
            "tipos": {
                "ROCIADORES": {"nombre": "Sistema de Rociadores", "precio_m2": 85.0},
                "GABINETES": {"nombre": "Gabinetes Contra Incendios", "precio_unidad": 1200.0},
                "EXTINTORES": {"nombre": "Red de Extintores", "precio_unidad": 180.0},
                "DETECCION": {"nombre": "Sistema de Detección", "precio_m2": 45.0}
            }
        }
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None:
            estado = {"etapa": "inicial", "tipo": None, "area": None, "unidades": None}
        
        etapa = estado.get("etapa", "inicial")
        
        if etapa == "inicial":
            return self._etapa_inicial(estado)
        elif etapa == "tipo":
            return self._etapa_tipo(mensaje, estado)
        elif etapa == "area":
            return self._etapa_area(mensaje, estado)
        elif etapa == "unidades":
            return self._etapa_unidades(mensaje, estado)
        elif etapa == "cotizacion":
            return self._etapa_cotizacion(mensaje, estado)
        
        return {'success': False, 'respuesta': 'Error', 'botones': None, 'estado': estado, 'cotizacion': None}
    
    def _etapa_inicial(self, estado: Dict) -> Dict:
        estado["etapa"] = "tipo"
        return {
            'success': True,
            'respuesta': """¡Hola! 👋 Soy **Pili**, tu especialista en sistemas contra incendios de **Tesla Electricidad**.

🔥 Sistemas disponibles:""",
            'botones': [
                {"text": "💧 Rociadores", "value": "ROCIADORES"},
                {"text": "🚪 Gabinetes", "value": "GABINETES"},
                {"text": "🧯 Extintores", "value": "EXTINTORES"},
                {"text": "🔔 Detección", "value": "DETECCION"}
            ],
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_tipo(self, mensaje: str, estado: Dict) -> Dict:
        estado["tipo"] = mensaje
        estado["etapa"] = "area"
        return {
            'success': True,
            'respuesta': f"""Sistema: **{self.knowledge_base['tipos'][mensaje]['nombre']}**

📐 **¿Cuál es el área a proteger en m²?**
_Escribe el número (ejemplo: 200)_""",
            'botones': None,
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_area(self, mensaje: str, estado: Dict) -> Dict:
        try:
            area = float(mensaje)
            estado["area"] = area
            estado["etapa"] = "unidades"
            
            tipo = estado["tipo"]
            if tipo in ["ROCIADORES", "DETECCION"]:
                estado["etapa"] = "cotizacion"
                return self._generar_cotizacion_final(estado)
            
            return {
                'success': True,
                'respuesta': f"""Área: **{area} m²**

🔢 **¿Cuántas unidades necesitas?**
_Escribe el número_""",
                'botones': None,
                'estado': estado,
                'cotizacion': None
            }
        except:
            return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado, 'cotizacion': None}
    
    def _etapa_unidades(self, mensaje: str, estado: Dict) -> Dict:
        try:
            estado["unidades"] = int(mensaje)
            estado["etapa"] = "cotizacion"
            return self._generar_cotizacion_final(estado)
        except:
            return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado, 'cotizacion': None}
    
    def _generar_cotizacion_final(self, estado: Dict) -> Dict:
        tipo = estado["tipo"]
        area = estado["area"]
        unidades = estado.get("unidades", 0)
        
        items = []
        info = self.knowledge_base["tipos"][tipo]
        
        if tipo in ["ROCIADORES", "DETECCION"]:
            precio_total = area * info["precio_m2"]
            items.append({
                "descripcion": f"{info['nombre']} - Instalación completa",
                "cantidad": area,
                "unidad": "m²",
                "precio_unitario": info["precio_m2"]
            })
        else:
            precio_total = unidades * info["precio_unidad"]
            items.append({
                "descripcion": f"{info['nombre']}",
                "cantidad": unidades,
                "unidad": "unidad",
                "precio_unitario": info["precio_unidad"]
            })
        
        subtotal = sum(i["cantidad"] * i["precio_unitario"] for i in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        cotizacion = {
            "tipo": tipo,
            "area": area,
            "items": items,
            "subtotal": subtotal,
            "igv": igv,
            "total": total
        }
        
        datos_generados = {
            "proyecto": {"nombre": f"Sistema Contra Incendios - {info['nombre']}", "area_m2": area},
            "items": items,
            "subtotal": subtotal,
            "igv": igv,
            "total": total
        }
        
        return {
            'success': True,
            'respuesta': f"""📊 **COTIZACIÓN SISTEMA CONTRA INCENDIOS**

**Total: S/ {total:.2f}**

¿Qué deseas hacer?""",
            'botones': [
                {"text": "📅 Agendar", "value": "AGENDAR"},
                {"text": "🔄 Nueva consulta", "value": "REINICIAR"}
            ],
            'estado': estado,
            'cotizacion': cotizacion,
            'datos_generados': datos_generados
        }
    
    def _etapa_cotizacion(self, mensaje: str, estado: Dict) -> Dict:
        if mensaje == "REINICIAR":
            return self.procesar("", None)
        return {'success': True, 'respuesta': "¡Gracias!", 'botones': None, 'estado': estado, 'cotizacion': None}
