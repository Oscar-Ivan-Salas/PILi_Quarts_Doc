"""
🤖 PILI ELECTRICIDAD ChatBot - Caja Negra Independiente
Versión: 1.0
Autor: Basado en patrón ITSE exitoso

CONCEPTO: Módulo autocontenido para cotizaciones de instalaciones eléctricas
- INPUT: mensaje + estado
- OUTPUT: respuesta + nuevo_estado + cotización
"""

from typing import Dict, List, Optional

class PILIElectricidadChatBot:
    """
    Caja negra para chat de Instalaciones Eléctricas
    
    Uso:
        chatbot = PILIElectricidadChatBot()
        resultado = chatbot.procesar(mensaje, estado)
    """
    
    def __init__(self):
        """Inicializa la base de conocimiento de electricidad"""
        self.knowledge_base = {
            "tipos_instalacion": {
                "RESIDENCIAL": {
                    "icon": "🏠",
                    "nombre": "Residencial",
                    "descripcion": "Casa, departamento, vivienda",
                    "precio_base_m2": 45.0,  # S/ por m²
                    "items_comunes": ["Puntos de luz", "Tomacorrientes", "Tablero eléctrico", "Cable THW"]
                },
                "COMERCIAL": {
                    "icon": "🏪",
                    "nombre": "Comercial",
                    "descripcion": "Tienda, oficina, local comercial",
                    "precio_base_m2": 65.0,
                    "items_comunes": ["Puntos de luz LED", "Tomacorrientes dobles", "Tablero trifásico", "Cable THW", "Luminarias"]
                },
                "INDUSTRIAL": {
                    "icon": "🏭",
                    "nombre": "Industrial",
                    "descripcion": "Fábrica, taller, planta",
                    "precio_base_m2": 95.0,
                    "items_comunes": ["Tablero industrial", "Cable NYY", "Luminarias industriales", "Sistema trifásico"]
                }
            },
            "precios_items": {
                # Puntos eléctricos
                "punto_luz_empotrado": {"precio": 15.0, "unidad": "punto"},
                "punto_luz_adosado": {"precio": 12.0, "unidad": "punto"},
                "tomacorriente_simple": {"precio": 15.0, "unidad": "punto"},
                "tomacorriente_doble": {"precio": 18.0, "unidad": "punto"},
                "interruptor_simple": {"precio": 12.0, "unidad": "punto"},
                "interruptor_doble": {"precio": 18.0, "unidad": "punto"},
                "interruptor_conmutado": {"precio": 25.0, "unidad": "punto"},
                
                # Tableros
                "tablero_monofasico_6_circuitos": {"precio": 450.0, "unidad": "unidad"},
                "tablero_monofasico_12_circuitos": {"precio": 650.0, "unidad": "unidad"},
                "tablero_trifasico_12_circuitos": {"precio": 1200.0, "unidad": "unidad"},
                "tablero_trifasico_24_circuitos": {"precio": 2200.0, "unidad": "unidad"},
                
                # Cables (por metro)
                "cable_thw_2.5mm": {"precio": 2.0, "unidad": "metro"},
                "cable_thw_4mm": {"precio": 3.08, "unidad": "metro"},
                "cable_thw_6mm": {"precio": 4.5, "unidad": "metro"},
                "cable_nyyy_10mm": {"precio": 8.5, "unidad": "metro"},
                
                # Luminarias
                "luminaria_led_18w": {"precio": 45.0, "unidad": "unidad"},
                "luminaria_led_36w": {"precio": 75.0, "unidad": "unidad"},
                "reflector_led_50w": {"precio": 120.0, "unidad": "unidad"},
                
                # Mano de obra
                "mano_obra_residencial": {"precio": 25.0, "unidad": "m²"},
                "mano_obra_comercial": {"precio": 35.0, "unidad": "m²"},
                "mano_obra_industrial": {"precio": 50.0, "unidad": "m²"}
            }
        }
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        """
        MÉTODO PRINCIPAL - CAJA NEGRA
        
        Args:
            mensaje: Mensaje del usuario
            estado: Estado actual de la conversación
        
        Returns:
            {
                'success': bool,
                'respuesta': str,
                'botones': List[Dict] | None,
                'estado': Dict,
                'cotizacion': Dict | None,
                'datos_generados': Dict | None
            }
        """
        
        # Inicializar estado
        if estado is None:
            estado = {
                "etapa": "inicial",
                "tipo_instalacion": None,
                "area": None,
                "puntos_luz": None,
                "tomacorrientes": None,
                "tablero": None
            }
        
        etapa = estado.get("etapa", "inicial")
        
        # Delegar según etapa
        if etapa == "inicial":
            return self._etapa_inicial(estado)
        elif etapa == "tipo":
            return self._etapa_tipo(mensaje, estado)
        elif etapa == "area":
            return self._etapa_area(mensaje, estado)
        elif etapa == "puntos_luz":
            return self._etapa_puntos_luz(mensaje, estado)
        elif etapa == "tomacorrientes":
            return self._etapa_tomacorrientes(mensaje, estado)
        elif etapa == "tablero":
            return self._etapa_tablero(mensaje, estado)
        elif etapa == "cotizacion":
            return self._etapa_cotizacion(mensaje, estado)
        else:
            return {
                'success': False,
                'respuesta': 'Error: Etapa desconocida',
                'botones': None,
                'estado': estado,
                'cotizacion': None
            }
    
    def _etapa_inicial(self, estado: Dict) -> Dict:
        """Etapa 1: Seleccionar tipo de instalación"""
        estado["etapa"] = "tipo"
        
        botones = [
            {"text": "🏠 Residencial", "value": "RESIDENCIAL"},
            {"text": "🏪 Comercial", "value": "COMERCIAL"},
            {"text": "🏭 Industrial", "value": "INDUSTRIAL"}
        ]
        
        return {
            'success': True,
            'respuesta': """¡Hola! 👋 Soy **Pili**, tu especialista en instalaciones eléctricas de **Tesla Electricidad - Huancayo**.

⚡ Te ayudo a cotizar tu proyecto eléctrico con:
✅ Precios competitivos
✅ Materiales de primera calidad
✅ Garantía de 2 años
✅ Personal certificado

**¿Qué tipo de instalación necesitas?**""",
            'botones': botones,
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_tipo(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 2: Procesar tipo y pedir área"""
        tipo = mensaje
        estado["tipo_instalacion"] = tipo
        estado["etapa"] = "area"
        
        info = self.knowledge_base["tipos_instalacion"][tipo]
        
        return {
            'success': True,
            'respuesta': f"""Perfecto, instalación **{info['nombre']}** {info['icon']}

{info['descripcion']}

📐 **¿Cuál es el área total a instalar en m²?**

_Escribe el número (ejemplo: 120)_""",
            'botones': None,
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_area(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 3: Procesar área y pedir puntos de luz"""
        try:
            area = float(mensaje)
            if area <= 0:
                return {
                    'success': False,
                    'respuesta': "Por favor ingresa un área válida en m²",
                    'botones': None,
                    'estado': estado,
                    'cotizacion': None
                }
            
            estado["area"] = area
            estado["etapa"] = "puntos_luz"
            
            # Sugerir cantidad basada en área
            puntos_sugeridos = int(area / 12)  # 1 punto cada 12m²
            
            return {
                'success': True,
                'respuesta': f"""📐 Área: **{area} m²**

💡 **¿Cuántos puntos de luz necesitas?**

_Sugerencia: {puntos_sugeridos} puntos (1 cada 12m²)_
_Escribe el número (ejemplo: {puntos_sugeridos})_""",
                'botones': None,
                'estado': estado,
                'cotizacion': None
            }
        except ValueError:
            return {
                'success': False,
                'respuesta': "Por favor ingresa un número válido de área",
                'botones': None,
                'estado': estado,
                'cotizacion': None
            }
    
    def _etapa_puntos_luz(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 4: Procesar puntos de luz y pedir tomacorrientes"""
        try:
            puntos_luz = int(mensaje)
            if puntos_luz < 0:
                return {
                    'success': False,
                    'respuesta': "Por favor ingresa un número válido de puntos de luz",
                    'botones': None,
                    'estado': estado,
                    'cotizacion': None
                }
            
            estado["puntos_luz"] = puntos_luz
            estado["etapa"] = "tomacorrientes"
            
            # Sugerir tomacorrientes
            tomas_sugeridos = int(estado["area"] / 15)  # 1 toma cada 15m²
            
            return {
                'success': True,
                'respuesta': f"""💡 Puntos de luz: **{puntos_luz}**

🔌 **¿Cuántos tomacorrientes necesitas?**

_Sugerencia: {tomas_sugeridos} tomacorrientes (1 cada 15m²)_
_Escribe el número (ejemplo: {tomas_sugeridos})_""",
                'botones': None,
                'estado': estado,
                'cotizacion': None
            }
        except ValueError:
            return {
                'success': False,
                'respuesta': "Por favor ingresa un número válido",
                'botones': None,
                'estado': estado,
                'cotizacion': None
            }
    
    def _etapa_tomacorrientes(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 5: Procesar tomacorrientes y pedir tipo de tablero"""
        try:
            tomacorrientes = int(mensaje)
            if tomacorrientes < 0:
                return {
                    'success': False,
                    'respuesta': "Por favor ingresa un número válido de tomacorrientes",
                    'botones': None,
                    'estado': estado,
                    'cotizacion': None
                }
            
            estado["tomacorrientes"] = tomacorrientes
            estado["etapa"] = "tablero"
            
            # Sugerir tablero según tipo
            tipo = estado["tipo_instalacion"]
            if tipo == "RESIDENCIAL":
                botones = [
                    {"text": "📦 Tablero 6 circuitos", "value": "tablero_monofasico_6_circuitos"},
                    {"text": "📦 Tablero 12 circuitos", "value": "tablero_monofasico_12_circuitos"}
                ]
            elif tipo == "COMERCIAL":
                botones = [
                    {"text": "📦 Tablero 12 circuitos", "value": "tablero_trifasico_12_circuitos"},
                    {"text": "📦 Tablero 24 circuitos", "value": "tablero_trifasico_24_circuitos"}
                ]
            else:  # INDUSTRIAL
                botones = [
                    {"text": "📦 Tablero 24 circuitos", "value": "tablero_trifasico_24_circuitos"}
                ]
            
            return {
                'success': True,
                'respuesta': f"""🔌 Tomacorrientes: **{tomacorrientes}**

📦 **¿Qué tipo de tablero eléctrico necesitas?**""",
                'botones': botones,
                'estado': estado,
                'cotizacion': None
            }
        except ValueError:
            return {
                'success': False,
                'respuesta': "Por favor ingresa un número válido",
                'botones': None,
                'estado': estado,
                'cotizacion': None
            }
    
    def _etapa_tablero(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 6: Procesar tablero y generar cotización"""
        tablero = mensaje
        estado["tablero"] = tablero
        estado["etapa"] = "cotizacion"
        
        # Generar cotización
        cotizacion = self._generar_cotizacion(estado)
        
        # Formatear respuesta
        respuesta = f"""📊 **COTIZACIÓN INSTALACIÓN ELÉCTRICA**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 RESUMEN DEL PROYECTO:**

🏠 Tipo: **{self.knowledge_base['tipos_instalacion'][estado['tipo_instalacion']]['nombre']}**
📐 Área: **{estado['area']} m²**
💡 Puntos de luz: **{estado['puntos_luz']}**
🔌 Tomacorrientes: **{estado['tomacorrientes']}**

━━━━━━━━━━━━━━━━━━━━━━━
**💰 COSTOS DESGLOSADOS:**

📦 Materiales: S/ {cotizacion['costo_materiales']:.2f}
👷 Mano de obra: S/ {cotizacion['costo_mano_obra']:.2f}

━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTAL:**

Subtotal: S/ {cotizacion['subtotal']:.2f}
IGV (18%): S/ {cotizacion['igv']:.2f}
**TOTAL: S/ {cotizacion['total']:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

⏱️ **Tiempo de instalación:** {cotizacion['dias_estimados']} días
✅ **Garantía:** 2 años
🎁 **Incluye:** Certificado de conformidad

¿Qué deseas hacer?"""
        
        botones = [
            {"text": "📅 Agendar instalación", "value": "AGENDAR"},
            {"text": "💬 Más información", "value": "INFO"},
            {"text": "🔄 Nueva consulta", "value": "REINICIAR"}
        ]
        
        # Preparar datos_generados para frontend
        datos_generados = {
            "proyecto": {
                "nombre": f"Instalación Eléctrica {estado['tipo_instalacion'].title()}",
                "area_m2": estado["area"],
                "tipo": estado["tipo_instalacion"]
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
    
    def _etapa_cotizacion(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 7: Post-cotización"""
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
✅ Diseño de planos eléctricos
✅ Instalación completa
✅ Certificado de conformidad
✅ Garantía de 2 años

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

Nos comunicaremos contigo en las próximas 2 horas para coordinar la visita técnica y el inicio de la instalación.

📞 WhatsApp: 906 315 961

¡Gracias por confiar en Tesla Electricidad! ⚡""",
                'botones': [
                    {"text": "🏠 Inicio", "value": "REINICIAR"}
                ],
                'estado': estado,
                'cotizacion': None
            }
        
        return {
            'success': False,
            'respuesta': "Opción no válida",
            'botones': None,
            'estado': estado,
            'cotizacion': None
        }
    
    def _generar_cotizacion(self, estado: Dict) -> Dict:
        """Genera la cotización con items detallados"""
        tipo = estado["tipo_instalacion"]
        area = estado["area"]
        puntos_luz = estado["puntos_luz"]
        tomacorrientes = estado["tomacorrientes"]
        tablero = estado["tablero"]
        
        items = []
        
        # 1. Puntos de luz
        if puntos_luz > 0:
            items.append({
                "descripcion": "Punto de luz empotrado (incluye cable, caja, interruptor)",
                "cantidad": puntos_luz,
                "unidad": "punto",
                "precio_unitario": self.knowledge_base["precios_items"]["punto_luz_empotrado"]["precio"]
            })
        
        # 2. Tomacorrientes
        if tomacorrientes > 0:
            items.append({
                "descripcion": "Tomacorriente doble con línea a tierra",
                "cantidad": tomacorrientes,
                "unidad": "punto",
                "precio_unitario": self.knowledge_base["precios_items"]["tomacorriente_doble"]["precio"]
            })
        
        # 3. Tablero eléctrico
        items.append({
            "descripcion": f"Tablero eléctrico {tablero.replace('_', ' ').replace('tablero ', '')}",
            "cantidad": 1,
            "unidad": "unidad",
            "precio_unitario": self.knowledge_base["precios_items"][tablero]["precio"]
        })
        
        # 4. Cable (estimado)
        cable_metros = area * 3  # 3 metros de cable por m²
        items.append({
            "descripcion": "Cable THW 2.5mm² (instalación completa)",
            "cantidad": cable_metros,
            "unidad": "metro",
            "precio_unitario": self.knowledge_base["precios_items"]["cable_thw_2.5mm"]["precio"]
        })
        
        # 5. Luminarias LED (si hay puntos de luz)
        if puntos_luz > 0:
            items.append({
                "descripcion": "Luminaria LED 18W (incluida)",
                "cantidad": puntos_luz,
                "unidad": "unidad",
                "precio_unitario": self.knowledge_base["precios_items"]["luminaria_led_18w"]["precio"]
            })
        
        # 6. Mano de obra
        mano_obra_key = f"mano_obra_{tipo.lower()}"
        costo_mano_obra = area * self.knowledge_base["precios_items"][mano_obra_key]["precio"]
        items.append({
            "descripcion": f"Mano de obra especializada ({tipo.lower()})",
            "cantidad": area,
            "unidad": "m²",
            "precio_unitario": self.knowledge_base["precios_items"][mano_obra_key]["precio"]
        })
        
        # Calcular totales
        subtotal = sum(item["cantidad"] * item["precio_unitario"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        # Estimar días
        dias_estimados = max(3, int(area / 50))  # Mínimo 3 días, 1 día por cada 50m²
        
        return {
            "tipo_instalacion": tipo,
            "area": area,
            "puntos_luz": puntos_luz,
            "tomacorrientes": tomacorrientes,
            "tablero": tablero,
            "items": items,
            "costo_materiales": subtotal - costo_mano_obra,
            "costo_mano_obra": costo_mano_obra,
            "subtotal": subtotal,
            "igv": igv,
            "total": total,
            "dias_estimados": dias_estimados
        }


# ═══════════════════════════════════════════════════════════
# 🎯 EJEMPLO DE USO (para testing)
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    chatbot = PILIElectricidadChatBot()
    
    print("=== TEST PILI ELECTRICIDAD ChatBot ===\n")
    
    # Paso 1: Inicio
    resultado = chatbot.procesar("", None)
    print(f"Bot: {resultado['respuesta']}\n")
    print(f"Botones: {[b['text'] for b in resultado['botones']]}\n")
    
    # Paso 2: Seleccionar COMERCIAL
    resultado = chatbot.procesar("COMERCIAL", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    
    # Paso 3: Ingresar área
    resultado = chatbot.procesar("120", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    
    # Paso 4: Puntos de luz
    resultado = chatbot.procesar("10", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    
    # Paso 5: Tomacorrientes
    resultado = chatbot.procesar("8", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    print(f"Botones: {[b['text'] for b in resultado['botones']]}\n")
    
    # Paso 6: Tablero
    resultado = chatbot.procesar("tablero_trifasico_12_circuitos", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    print(f"\nCotización generada:")
    print(f"Total: S/ {resultado['cotizacion']['total']:.2f}")
    print(f"Items: {len(resultado['cotizacion']['items'])} items")
