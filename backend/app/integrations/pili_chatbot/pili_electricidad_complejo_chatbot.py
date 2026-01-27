"""
⚡ PILI ELECTRICIDAD COMPLEJO ChatBot v2.0
Cotización Compleja con Ingeniería de Detalle
"""
from typing import Dict, Optional
import math

class PILIElectricidadComplejoChatBot:
    def __init__(self):
        self.kb = {
            "tipos": {
                "RESIDENCIAL": {"nombre": "Instalación Residencial", "fd": 0.7, "fp": 0.9, "v": 220},
                "COMERCIAL": {"nombre": "Instalación Comercial", "fd": 0.85, "fp": 0.85, "v": 220},
                "INDUSTRIAL": {"nombre": "Instalación Industrial Trifásica", "fd": 0.95, "fp": 0.8, "v": 380}
            },
            "cables": {"2.5": {"cap": 21, "p": 2.5}, "4": {"cap": 28, "p": 3.8}, "6": {"cap": 36, "p": 5.2}, "10": {"cap": 50, "p": 8.5}, "16": {"cap": 68, "p": 13.5}, "25": {"cap": 89, "p": 21.0}},
            "prot": {"10A": 45, "16A": 48, "20A": 52, "25A": 58, "32A": 65, "40A": 75, "50A": 85, "63A": 95}
        }
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        if estado is None: estado = {"etapa": "inicial", "tipo": None, "area": None, "cargas": {}}
        etapa = estado.get("etapa", "inicial")
        
        if etapa == "inicial": return self._etapa_inicial(estado)
        elif etapa == "tipo": return self._etapa_tipo(mensaje, estado)
        elif etapa == "area": return self._etapa_area(mensaje, estado)
        elif etapa == "iluminacion": return self._etapa_iluminacion(mensaje, estado)
        elif etapa == "tomacorrientes": return self._etapa_tomacorrientes(mensaje, estado)
        elif etapa == "equipos": return self._etapa_equipos(mensaje, estado)
        elif etapa == "cotizacion": return self._etapa_cotizacion(mensaje, estado)
        return {'success': False, 'respuesta': 'Error', 'botones': None, 'estado': estado}
    
    def _etapa_inicial(self, estado: Dict) -> Dict:
        estado["etapa"] = "tipo"
        return {'success': True, 'respuesta': """¡Hola! 👋 Soy **Pili**, especialista en instalaciones eléctricas **COMPLEJAS**.

⚡ **COTIZACIÓN TÉCNICA DETALLADA**
✅ Cálculo de cargas eléctricas
✅ Dimensionamiento de cables
✅ Selección de protecciones
✅ Cronograma de 4 fases
✅ Memoria de cálculo

**¿Tipo de instalación?**""", 'botones': [{"text": "🏠 Residencial", "value": "RESIDENCIAL"}, {"text": "🏪 Comercial", "value": "COMERCIAL"}, {"text": "🏭 Industrial", "value": "INDUSTRIAL"}], 'estado': estado, 'cotizacion': None}
    
    def _etapa_tipo(self, mensaje: str, estado: Dict) -> Dict:
        estado["tipo"] = mensaje
        estado["etapa"] = "area"
        return {'success': True, 'respuesta': f"""**Tipo:** {self.kb['tipos'][mensaje]['nombre']}\n\n📐 **¿Área total en m²?**\n_Ejemplo: 150_""", 'botones': None, 'estado': estado}
    
    def _etapa_area(self, mensaje: str, estado: Dict) -> Dict:
        try:
            estado["area"] = float(mensaje)
            estado["etapa"] = "iluminacion"
            return {'success': True, 'respuesta': f"""Área: **{estado['area']} m²**\n\n💡 **¿Cuántos puntos de luz?**\n_Ejemplo: 25_""", 'botones': None, 'estado': estado}
        except: return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado}
    
    def _etapa_iluminacion(self, mensaje: str, estado: Dict) -> Dict:
        try:
            estado["cargas"]["luz"] = {"n": int(mensaje), "w": int(mensaje) * 18}
            estado["etapa"] = "tomacorrientes"
            return {'success': True, 'respuesta': f"""✅ Iluminación: {int(mensaje)} puntos\n\n🔌 **¿Cuántos tomacorrientes?**\n_Ejemplo: 30_""", 'botones': None, 'estado': estado}
        except: return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado}
    
    def _etapa_tomacorrientes(self, mensaje: str, estado: Dict) -> Dict:
        try:
            estado["cargas"]["toma"] = {"n": int(mensaje), "w": int(mensaje) * 180}
            estado["etapa"] = "equipos"
            return {'success': True, 'respuesta': f"""✅ Tomacorrientes: {int(mensaje)}\n\n⚙️ **¿Equipos especiales?**\n(Aires, hornos, motores)""", 'botones': [{"text": "✅ Sí", "value": "SI"}, {"text": "❌ No", "value": "NO"}], 'estado': estado}
        except: return {'success': False, 'respuesta': "Número inválido", 'botones': None, 'estado': estado}
    
    def _etapa_equipos(self, mensaje: str, estado: Dict) -> Dict:
        tipo = estado["tipo"]
        if mensaje == "SI":
            estado["cargas"]["eq"] = {"w": 3000 if tipo == "RESIDENCIAL" else 5000 if tipo == "COMERCIAL" else 10000}
        else:
            estado["cargas"]["eq"] = {"w": 0}
        return self._generar_cotizacion(estado)
    
    def _generar_cotizacion(self, estado: Dict) -> Dict:
        tipo, area, cargas = estado["tipo"], estado["area"], estado["cargas"]
        info = self.kb["tipos"][tipo]
        
        # Cálculos
        w_total = cargas["luz"]["w"] + cargas["toma"]["w"] + cargas["eq"]["w"]
        w_demanda = w_total * info["fd"]
        i_calc = w_demanda / (math.sqrt(3) * info["v"] * info["fp"]) if tipo == "INDUSTRIAL" else w_demanda / (info["v"] * info["fp"])
        cable = self._sel_cable(i_calc * 1.25)
        prot = self._sel_prot(i_calc)
        
        # Items
        items = [
            {"descripcion": f"Punto luz LED 18W + cable {cable}mm²", "cantidad": cargas["luz"]["n"], "unidad": "pto", "precio_unitario": 85.0},
            {"descripcion": f"Tomacorriente doble + cable {cable}mm²", "cantidad": cargas["toma"]["n"], "unidad": "pto", "precio_unitario": 95.0},
            {"descripcion": f"Tablero {'trifásico 380V' if tipo=='INDUSTRIAL' else 'monofásico 220V'} - {prot}", "cantidad": 1, "unidad": "und", "precio_unitario": 3500 if tipo=="INDUSTRIAL" else 1800 if tipo=="COMERCIAL" else 1200},
            {"descripcion": f"Cable THW {cable}mm²", "cantidad": area * 0.3, "unidad": "m", "precio_unitario": self.kb["cables"][cable]["p"]},
            {"descripcion": f"Interruptores {prot}", "cantidad": 8, "unidad": "und", "precio_unitario": self.kb["prot"][prot]},
            {"descripcion": "Mano de obra", "cantidad": (cargas["luz"]["n"] + cargas["toma"]["n"]) * 0.5, "unidad": "h", "precio_unitario": 45.0}
        ]
        
        subtotal = sum(i["cantidad"] * i["precio_unitario"] for i in items)
        igv, total = subtotal * 0.18, subtotal * 1.18
        
        # Cronograma
        total_ptos = cargas["luz"]["n"] + cargas["toma"]["n"]
        d_ing = max(3, min(10, int(area / 50)))
        d_adq = max(5, min(15, int(total_ptos / 10)))
        d_inst = max(3, int((total_ptos * 0.5) / 8))
        d_prue = 2 if tipo == "RESIDENCIAL" else 3 if tipo == "COMERCIAL" else 5
        
        # Descripción auto-generada
        desc = f"""Instalación eléctrica {info['nombre'].lower()} de {area}m² que comprende:

• Sistema de iluminación con {cargas['luz']['n']} puntos LED de bajo consumo
• Red de tomacorrientes con {cargas['toma']['n']} puntos con línea a tierra
• Tablero eléctrico con protecciones termomagnéticas
• Sistema de puesta a tierra según normativa
• Cableado con conductor THW {cable}mm²
• Carga total instalada: {round(w_total/1000, 2)}kW
• Carga de demanda: {round(w_demanda/1000, 2)}kW

El proyecto incluye ingeniería de detalle, suministro de materiales, instalación, pruebas y puesta en marcha."""
        
        datos_generados = {
            "proyecto": {"nombre": f"Instalación Eléctrica {info['nombre']}", "area_m2": area, "carga_total_kW": round(w_total/1000, 2)},
            "items": items, "subtotal": subtotal, "igv": igv, "total": total,
            "datos_tecnicos": {"carga_total_watts": w_total, "carga_demanda_watts": w_demanda, "corriente_A": round(i_calc, 2), "cable_mm2": cable, "proteccion": prot, "tension_V": info["v"]},
            "descripcion_proyecto": desc,
            "normativa_aplicable": "Código Nacional de Electricidad - Utilización 2011 (CNE)",
            "dias_ingenieria": d_ing, "dias_adquisiciones": d_adq, "dias_instalacion": d_inst, "dias_pruebas": d_prue,
            "tipo_documento": "COTIZACION_COMPLEJA"
        }
        
        estado["etapa"] = "cotizacion"
        return {'success': True, 'respuesta': f"""📊 **COTIZACIÓN TÉCNICA COMPLETA**

**DATOS TÉCNICOS:**
• Carga: {w_total}W ({round(w_total/1000,2)}kW)
• Corriente: {round(i_calc,2)}A
• Cable: {cable}mm² | Protección: {prot}

**CRONOGRAMA:**
• Ingeniería: {d_ing}d | Adquisiciones: {d_adq}d
• Instalación: {d_inst}d | Pruebas: {d_prue}d
**TOTAL: {d_ing+d_adq+d_inst+d_prue} días**

**INVERSIÓN:**
Subtotal: S/ {subtotal:.2f}
IGV: S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**

✅ Incluye: Ingeniería + Materiales + Instalación
📋 Normativa: CNE 2011

¿Qué deseas hacer?""", 'botones': [{"text": "📅 Agendar", "value": "AGENDAR"}, {"text": "🔄 Nueva", "value": "REINICIAR"}], 'estado': estado, 'cotizacion': datos_generados, 'datos_generados': datos_generados}
    
    def _sel_cable(self, i: float) -> str:
        for s, d in self.kb["cables"].items():
            if d["cap"] >= i: return s
        return "25"
    
    def _sel_prot(self, i: float) -> str:
        for p in ["10A", "16A", "20A", "25A", "32A", "40A", "50A", "63A"]:
            if int(p.replace("A", "")) >= i: return p
        return "63A"
    
    def _etapa_cotizacion(self, mensaje: str, estado: Dict) -> Dict:
        if mensaje == "REINICIAR": return self.procesar("", None)
        return {'success': True, 'respuesta': "¡Gracias!", 'botones': None, 'estado': estado}
