"""
🤖 PILI ITSE ChatBot - Caja Negra Independiente
Versión: 1.0 SIMPLE

CONCEPTO: Módulo autocontenido tipo "transformer"
- INPUT: mensaje + estado
- OUTPUT: respuesta + nuevo_estado + cotización

NO depende de backend/frontend existente
El backend existente LLAMA a este módulo
"""

from typing import Dict, List, Optional, Tuple

class PILIITSEChatBot:
    """
    Caja negra para chat ITSE
    
    Uso desde backend existente:
        chatbot = PILIITSEChatBot()
        resultado = chatbot.procesar(mensaje, estado)
    """
    
    def __init__(self):
        """Inicializa la base de conocimiento"""
        self.knowledge_base = {
            "precios_municipales": {
                "BAJO": {"precio": 168.30, "renovacion": 90.30, "dias": 7},
                "MEDIO": {"precio": 208.60, "renovacion": 109.40, "dias": 7},
                "ALTO": {"precio": 703.00, "renovacion": 417.40, "dias": 7},
                "MUY_ALTO": {"precio": 1084.60, "renovacion": 629.20, "dias": 7}
            },
            "precios_tesla": {
                "BAJO": {"min": 300, "max": 500},
                "MEDIO": {"min": 450, "max": 650},
                "ALTO": {"min": 800, "max": 1200},
                "MUY_ALTO": {"min": 1200, "max": 1800}
            },
            "categorias": {
                "SALUD": {
                    "tipos": ["Hospital", "Clínica", "Centro Médico", "Consultorio", "Laboratorio"],
                    "riesgo_base": "ALTO"
                },
                "EDUCACION": {
                    "tipos": ["Colegio", "Universidad", "Instituto", "Academia", "Guardería"],
                    "riesgo_base": "MEDIO"
                },
                "HOSPEDAJE": {
                    "tipos": ["Hotel", "Hostal", "Residencia", "Apart-hotel"],
                    "riesgo_base": "MEDIO"
                },
                "COMERCIO": {
                    "tipos": ["Tienda", "Supermercado", "Centro Comercial", "Galería"],
                    "riesgo_base": "MEDIO"
                },
                "RESTAURANTE": {
                    "tipos": ["Restaurante", "Cafetería", "Bar", "Discoteca"],
                    "riesgo_base": "MEDIO"
                },
                "OFICINA": {
                    "tipos": ["Oficina", "Estudio", "Coworking"],
                    "riesgo_base": "BAJO"
                },
                "INDUSTRIAL": {
                    "tipos": ["Fábrica", "Taller", "Almacén", "Planta"],
                    "riesgo_base": "ALTO"
                },
                "ENCUENTRO": {
                    "tipos": ["Auditorio", "Cine", "Teatro", "Iglesia", "Gimnasio"],
                    "riesgo_base": "ALTO"
                }
            }
        }
    
    def procesar(self, mensaje: str, estado: Optional[Dict] = None) -> Dict:
        """
        MÉTODO PRINCIPAL - CAJA NEGRA
        
        Args:
            mensaje: Mensaje del usuario
            estado: Estado actual de la conversación (opcional)
        
        Returns:
            {
                'success': bool,
                'respuesta': str,
                'botones': List[Dict] | None,
                'estado': Dict,
                'cotizacion': Dict | None
            }
        """
        
        # Inicializar estado si no existe
        if estado is None:
            estado = {
                "etapa": "inicial",
                "categoria": None,
                "tipo": None,
                "area": None,
                "pisos": None,
                "riesgo": None
            }
        
        etapa = estado.get("etapa", "inicial")
        
        # Delegar a método específico según etapa
        if etapa == "inicial":
            return self._etapa_inicial(estado)
        elif etapa == "categoria":
            return self._etapa_categoria(mensaje, estado)
        elif etapa == "tipo":
            return self._etapa_tipo(mensaje, estado)
        elif etapa == "area":
            return self._etapa_area(mensaje, estado)
        elif etapa == "pisos":
            return self._etapa_pisos(mensaje, estado)
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
        """Etapa 1: Mostrar categorías"""
        estado["etapa"] = "categoria"
        
        botones = [
            {"text": "🏥 Salud", "value": "SALUD"},
            {"text": "🎓 Educación", "value": "EDUCACION"},
            {"text": "🏨 Hospedaje", "value": "HOSPEDAJE"},
            {"text": "🏪 Comercio", "value": "COMERCIO"},
            {"text": "🍽️ Restaurante", "value": "RESTAURANTE"},
            {"text": "🏢 Oficina", "value": "OFICINA"},
            {"text": "🏭 Industrial", "value": "INDUSTRIAL"},
            {"text": "🎭 Encuentro", "value": "ENCUENTRO"}
        ]
        
        return {
            'success': True,
            'respuesta': """¡Hola! 👋 Soy **Pili**, tu especialista en certificados ITSE de **Tesla Electricidad - Huancayo**.

🎯 Te ayudo a obtener tu certificado ITSE con:
✅ Visita técnica GRATUITA
✅ Precios oficiales TUPA Huancayo
✅ Trámite 100% gestionado
✅ Entrega en 7 días hábiles

**Selecciona tu tipo de establecimiento:**""",
            'botones': botones,
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_categoria(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 2: Procesar categoría y mostrar tipos"""
        categoria = mensaje
        estado["categoria"] = categoria
        estado["etapa"] = "tipo"
        
        tipos = self.knowledge_base["categorias"][categoria]["tipos"]
        botones = [{"text": t, "value": t} for t in tipos]
        
        return {
            'success': True,
            'respuesta': f"Perfecto, sector **{categoria}**. ¿Qué tipo específico es?",
            'botones': botones,
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_tipo(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 3: Procesar tipo y pedir área"""
        tipo = mensaje
        estado["tipo"] = tipo
        estado["etapa"] = "area"
        
        return {
            'success': True,
            'respuesta': f"Entendido, es un **{tipo}**.\n\n¿Cuál es el área total en m²?\n\n_Escribe el número (ejemplo: 150)_",
            'botones': None,
            'estado': estado,
            'cotizacion': None
        }
    
    def _etapa_area(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 4: Procesar área y pedir pisos"""
        try:
            area = float(mensaje)
            if area <= 0:
                return {
                    'success': False,
                    'respuesta': "Por favor ingresa un número válido de área en m²",
                    'botones': None,
                    'estado': estado,
                    'cotizacion': None
                }
            
            estado["area"] = area
            estado["etapa"] = "pisos"
            
            return {
                'success': True,
                'respuesta': f"📐 Área: **{area} m²**\n\n¿Cuántos pisos tiene el establecimiento?\n\n_Escribe el número (ejemplo: 2)_",
                'botones': None,
                'estado': estado,
                'cotizacion': None
            }
        except ValueError:
            return {
                'success': False,
                'respuesta': "Por favor ingresa un número válido de área en m²",
                'botones': None,
                'estado': estado,
                'cotizacion': None
            }
    
    def _etapa_pisos(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 5: Procesar pisos y generar cotización"""
        try:
            pisos = int(mensaje)
            if pisos <= 0:
                return {
                    'success': False,
                    'respuesta': "Por favor ingresa un número válido de pisos",
                    'botones': None,
                    'estado': estado,
                    'cotizacion': None
                }
            
            estado["pisos"] = pisos
            
            # Calcular riesgo
            riesgo = self._calcular_riesgo(
                estado["categoria"],
                estado["area"],
                pisos
            )
            estado["riesgo"] = riesgo
            estado["etapa"] = "cotizacion"
            
            # Generar cotización
            cotizacion = self._generar_cotizacion(
                riesgo,
                estado["categoria"],
                estado["tipo"],
                estado["area"],
                pisos
            )
            
            # Formatear respuesta
            respuesta = f"""📊 **COTIZACIÓN ITSE - NIVEL {riesgo.replace('_', ' ')}**

━━━━━━━━━━━━━━━━━━━━━━━
**💰 COSTOS DESGLOSADOS:**

🏛️ **Derecho Municipal (TUPA):**
└ S/ {cotizacion['costo_tupa']:.2f}

⚡ **Servicio Técnico TESLA:**
└ S/ {cotizacion['costo_tesla_min']} - {cotizacion['costo_tesla_max']}
└ Incluye: Evaluación + Planos + Gestión + Seguimiento

━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTAL ESTIMADO:**
**S/ {cotizacion['total_min']:.2f} - {cotizacion['total_max']:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

⏱️ **Tiempo:** {cotizacion['dias']} días hábiles
🎁 **Visita técnica:** GRATUITA
✅ **Garantía:** 100% aprobación

¿Qué deseas hacer?"""
            
            botones = [
                {"text": "📅 Agendar visita", "value": "AGENDAR"},
                {"text": "💬 Más información", "value": "INFO"},
                {"text": "🔄 Nueva consulta", "value": "REINICIAR"}
            ]
            
            # ✅ Preparar datos_generados para frontend
            datos_generados = {
                "proyecto": {
                    "nombre": f"Certificado ITSE - {estado.get('categoria', 'COMERCIO')}",
                    "area_m2": estado.get("area", 0),
                    "pisos": pisos,
                    "nivel_riesgo": estado.get("riesgo", "MEDIO")
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
                'datos_generados': datos_generados  # ✅ PARA TABLA FRONTEND
            }
            
        except ValueError:
            return {
                'success': False,
                'respuesta': "Por favor ingresa un número válido de pisos",
                'botones': None,
                'estado': estado,
                'cotizacion': None
            }
    
    def _etapa_cotizacion(self, mensaje: str, estado: Dict) -> Dict:
        """Etapa 6: Post-cotización"""
        if mensaje == "REINICIAR":
            return self.procesar("", None)
        elif mensaje == "INFO":
            return {
                'success': True,
                'respuesta': """📞 **Puedes contactarnos:**

**WhatsApp:** 906 315 961
**Email:** ingenieria.teslaelectricidad@gmail.com
**Dirección:** Jr. Los Narcisos Mz H lote 4, Huancayo

¿Deseas agendar la visita técnica?""",
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

Nos comunicaremos contigo en las próximas 2 horas para coordinar la visita técnica GRATUITA.

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
    
    def _calcular_riesgo(self, categoria: str, area: float, pisos: int) -> str:
        """Calcula el nivel de riesgo ITSE"""
        if categoria == "SALUD":
            return "MUY_ALTO" if (area > 500 or pisos >= 2) else "ALTO"
        elif categoria == "EDUCACION":
            return "ALTO" if (area > 1000 or pisos >= 3) else "MEDIO"
        elif categoria == "HOSPEDAJE":
            return "ALTO" if (area > 500 or pisos >= 3) else "MEDIO"
        elif categoria == "COMERCIO":
            return "ALTO" if area > 500 else "MEDIO"
        elif categoria == "RESTAURANTE":
            return "ALTO" if area > 300 else "MEDIO"
        elif categoria == "OFICINA":
            return "MEDIO" if area > 500 else "BAJO"
        elif categoria == "INDUSTRIAL":
            return "ALTO"
        elif categoria == "ENCUENTRO":
            return "MUY_ALTO" if area > 500 else "ALTO"
        
        return self.knowledge_base["categorias"][categoria]["riesgo_base"]
    
    def _generar_cotizacion(self, riesgo: str, categoria: str, tipo: str, area: float, pisos: int) -> Dict:
        """Genera la cotización ITSE con items para tabla"""
        municipal = self.knowledge_base["precios_municipales"][riesgo]
        tesla = self.knowledge_base["precios_tesla"][riesgo]

        # Usar precio promedio Tesla
        precio_tesla = (tesla["min"] + tesla["max"]) / 2

        # ✅ GENERAR ITEMS para tabla "Detalle de la Cotización"
        items = [
            {
                "descripcion": f"Certificado ITSE - Nivel {riesgo.replace('_', ' ')}",
                "cantidad": 1,
                "unidad": "servicio",
                "precio_unitario": municipal["precio"]
            },
            {
                "descripcion": "Servicio técnico profesional - Evaluación + Planos + Gestión",
                "cantidad": 1,
                "unidad": "servicio",
                "precio_unitario": precio_tesla
            },
            {
                "descripcion": "Visita técnica gratuita",
                "cantidad": 1,
                "unidad": "servicio",
                "precio_unitario": 0.0
            }
        ]

        # Calcular totales
        subtotal = sum(item["cantidad"] * item["precio_unitario"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv

        total_min = municipal["precio"] + tesla["min"]
        total_max = municipal["precio"] + tesla["max"]

        return {
            "categoria": categoria,
            "tipo": tipo,
            "area": area,
            "pisos": pisos,
            "riesgo": riesgo,
            "costo_tupa": municipal["precio"],
            "costo_tesla_min": tesla["min"],
            "costo_tesla_max": tesla["max"],
            "total_min": total_min,
            "total_max": total_max,
            "dias": municipal["dias"],
            # ✅ NUEVOS CAMPOS para tabla
            "items": items,
            "subtotal": subtotal,
            "igv": igv,
            "total": total
        }


# ═══════════════════════════════════════════════════════════
# 🎯 EJEMPLO DE USO (para testing)
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Crear instancia
    chatbot = PILIITSEChatBot()
    
    # Simular conversación
    print("=== TEST PILI ITSE ChatBot ===\n")
    
    # Paso 1: Inicio
    resultado = chatbot.procesar("", None)
    print(f"Bot: {resultado['respuesta']}\n")
    print(f"Botones: {[b['text'] for b in resultado['botones']]}\n")
    
    # Paso 2: Seleccionar SALUD
    resultado = chatbot.procesar("SALUD", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    print(f"Botones: {[b['text'] for b in resultado['botones']]}\n")
    
    # Paso 3: Seleccionar Hospital
    resultado = chatbot.procesar("Hospital", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    
    # Paso 4: Ingresar área
    resultado = chatbot.procesar("600", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    
    # Paso 5: Ingresar pisos
    resultado = chatbot.procesar("2", resultado['estado'])
    print(f"Bot: {resultado['respuesta']}\n")
    print(f"Cotización: {resultado['cotizacion']}\n")
