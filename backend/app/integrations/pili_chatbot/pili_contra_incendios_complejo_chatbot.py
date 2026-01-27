"""🔥 PILI CONTRA INCENDIOS COMPLEJO v2.0"""
from typing import Dict, Optional

class PILIContraIncendiosComplejoChatBot:
    def __init__(self):
        self.kb = {"tipos": {"ROCIADORES": {"n": "Sistema de Rociadores", "p": 120, "norm": "NFPA 13", "u": "m²"}, "GABINETES": {"n": "Gabinetes Contra Incendios", "p": 850, "norm": "NFPA 14", "u": "und"}, "EXTINTORES": {"n": "Extintores Portátiles", "p": 180, "norm": "NFPA 10", "u": "und"}, "DETECCION": {"n": "Sistema de Detección", "p": 95, "norm": "NFPA 72", "u": "m²"}}}
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None: estado = {"etapa": "inicial"}
        etapa = estado.get("etapa")
        
        if etapa == "inicial":
            estado["etapa"] = "tipo"
            return {'success': True, 'respuesta': """¡Hola! 👋 **Pili** - Contra Incendios **COMPLEJO**

🔥 **COTIZACIÓN TÉCNICA DETALLADA**
✅ Diseño según NFPA
✅ Cálculo hidráulico
✅ Planos de instalación
✅ Cronograma de 4 fases

**¿Qué sistema necesitas?**""", 'botones': [{"text": "💧 Rociadores", "value": "ROCIADORES"}, {"text": "🚒 Gabinetes", "value": "GABINETES"}, {"text": "🧯 Extintores", "value": "EXTINTORES"}, {"text": "🔔 Detección", "value": "DETECCION"}], 'estado': estado}
        
        elif etapa == "tipo":
            estado["tipo"] = mensaje
            estado["etapa"] = "cantidad"
            info = self.kb["tipos"][mensaje]
            return {'success': True, 'respuesta': f"""**Sistema:** {info['n']}\n\n📏 **¿Cantidad en {info['u']}?**\n_Ejemplo: 200_""", 'botones': None, 'estado': estado}
        
        elif etapa == "cantidad":
            try:
                estado["cantidad"] = float(mensaje)
                estado["etapa"] = "riesgo"
                return {'success': True, 'respuesta': f"""✅ Cantidad: {float(mensaje)} {self.kb['tipos'][estado['tipo']]['u']}\n\n⚠️ **Nivel de riesgo:**""", 'botones': [{"text": "🟢 Bajo", "value": "BAJO"}, {"text": "🟡 Moderado", "value": "MODERADO"}, {"text": "🟠 Alto", "value": "ALTO"}], 'estado': estado}
            except: return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado}
        
        elif etapa == "riesgo":
            estado["riesgo"] = mensaje
            return self._generar_cotizacion(estado)
        
        elif etapa == "cotizacion":
            if mensaje == "REINICIAR": return self.procesar("", None)
            return {'success': True, 'respuesta': "¡Gracias!", 'botones': None, 'estado': estado}
        
        return {'success': False, 'respuesta': 'Error', 'botones': None, 'estado': estado}
    
    def _generar_cotizacion(self, estado: Dict) -> Dict:
        tipo, cantidad, riesgo = estado["tipo"], estado["cantidad"], estado["riesgo"]
        info = self.kb["tipos"][tipo]
        
        # Factor de riesgo
        factor = 1.0 if riesgo == "BAJO" else 1.2 if riesgo == "MODERADO" else 1.5
        
        items = [
            {"descripcion": f"{info['n']} - Instalación completa", "cantidad": cantidad, "unidad": info["u"], "precio_unitario": info["p"] * factor},
            {"descripcion": "Diseño hidráulico + Planos", "cantidad": 1, "unidad": "servicio", "precio_unitario": 800.0},
            {"descripcion": "Pruebas y certificación", "cantidad": 1, "unidad": "servicio", "precio_unitario": 500.0}
        ]
        
        subtotal = sum(i["cantidad"] * i["precio_unitario"] for i in items)
        igv, total = subtotal * 0.18, subtotal * 1.18
        
        # Cronograma
        d_ing = max(5, min(15, int(cantidad / 50)))
        d_adq = max(7, min(20, int(cantidad / 30)))
        d_inst = max(5, min(15, int(cantidad / 40)))
        d_prue = 3 if riesgo == "BAJO" else 5 if riesgo == "MODERADO" else 7
        
        desc = f"""Sistema contra incendios {info['n'].lower()} para edificación de riesgo {riesgo.lower()}:

• Cobertura: {cantidad} {info['u']}
• Diseño según normativa {info['norm']}
• Nivel de riesgo: {riesgo}
• Cálculo hidráulico completo
• Planos de instalación
• Pruebas y certificación
• Capacitación en uso del sistema

El proyecto incluye ingeniería de detalle, suministro de equipos, instalación, pruebas y certificación."""
        
        datos_generados = {
            "proyecto": {"nombre": f"Sistema Contra Incendios - {info['n']}", "cobertura": cantidad, "riesgo": riesgo},
            "items": items, "subtotal": subtotal, "igv": igv, "total": total,
            "datos_tecnicos": {"tipo_sistema": tipo, "cantidad": cantidad, "unidad": info["u"], "riesgo": riesgo, "normativa": info["norm"]},
            "descripcion_proyecto": desc,
            "normativa_aplicable": info["norm"],
            "dias_ingenieria": d_ing, "dias_adquisiciones": d_adq, "dias_instalacion": d_inst, "dias_pruebas": d_prue,
            "tipo_documento": "COTIZACION_COMPLEJA"
        }
        
        estado["etapa"] = "cotizacion"
        return {'success': True, 'respuesta': f"""📊 **COTIZACIÓN CONTRA INCENDIOS COMPLETA**

**SISTEMA:** {info['n']}
**COBERTURA:** {cantidad} {info['u']}
**RIESGO:** {riesgo}

**CRONOGRAMA:**
• Ingeniería: {d_ing}d | Adquisiciones: {d_adq}d
• Instalación: {d_inst}d | Pruebas: {d_prue}d
**TOTAL: {d_ing+d_adq+d_inst+d_prue} días**

**INVERSIÓN:**
Subtotal: S/ {subtotal:.2f}
IGV: S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**

✅ Incluye: Diseño + Instalación + Certificación
📋 Normativa: {info['norm']}

¿Qué deseas hacer?""", 'botones': [{"text": "📅 Agendar", "value": "AGENDAR"}, {"text": "🔄 Nueva", "value": "REINICIAR"}], 'estado': estado, 'cotizacion': datos_generados, 'datos_generados': datos_generados}
