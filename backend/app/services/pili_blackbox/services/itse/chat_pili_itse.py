"""
═══════════════════════════════════════════════════════════════════════════════
🎯 CHAT PILI ITSE - CAJA NEGRA
═══════════════════════════════════════════════════════════════════════════════
Versión: 1.0.0
Patrón: Black Box (Todo el servicio ITSE en 1 archivo)
Autor: Claude Code - Arquitectura Refactorizada
Fecha: 30 de Diciembre 2025

PRINCIPIO DE CAJA NEGRA:
- ENTRADA: mensaje (str) + historial (List[dict])
- SALIDA: Dict con respuesta, datos, y siguiente acción
- TODO sucede dentro de esta clase (auto-contenido)
═══════════════════════════════════════════════════════════════════════════════
"""

import re
import yaml
from typing import Dict, Any, List, Optional
from pathlib import Path


class ITSEChatPili:
    """
    Caja Negra para Servicio ITSE

    Maneja todo el flujo conversacional de certificados ITSE:
    1. Selección de categoría de establecimiento
    2. Selección de tipo específico
    3. Ingreso de área en m²
    4. Ingreso de número de pisos
    5. Cálculo de nivel de riesgo
    6. Generación de cotización con precios TUPA + Tesla
    7. Opciones de agendamiento

    TODO está auto-contenido en esta clase.
    """

    def __init__(self):
        """Inicializa el servicio ITSE cargando configuración"""
        # Cargar configuración YAML (auto-contenido)
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        # Cargar base de conocimiento (auto-contenido)
        from .knowledge import KB
        self.kb = KB

    # ═══════════════════════════════════════════════════════════════════════
    # 🎯 MÉTODO PRINCIPAL - INTERFAZ DE CAJA NEGRA
    # ═══════════════════════════════════════════════════════════════════════

    def procesar(self, mensaje: str, historial: List[Dict] = None) -> Dict[str, Any]:
        """
        MÉTODO PRINCIPAL - CAJA NEGRA

        ENTRADA:
            mensaje (str): Mensaje del usuario
            historial (List[Dict]): Conversación previa

        SALIDA:
            Dict con estructura:
            {
                "respuesta": str,           # Mensaje de respuesta
                "datos": Dict,              # Datos extraídos/generados
                "siguiente_accion": str,    # "recopilar_datos" | "generar_documento" | "agendar"
                "botones": List,            # Botones contextuales (opcional)
                "progreso": str             # "2/5" (opcional)
            }

        TODO el procesamiento sucede aquí (caja negra).
        """
        if historial is None:
            historial = []

        # Obtener estado actual de la conversación
        estado = self._obtener_estado(historial)

        # ETAPA 1: Seleccionar categoría
        if estado['etapa'] == 'inicial' or estado['etapa'] == 'categoria':
            return self._procesar_categoria(mensaje, estado)

        # ETAPA 2: Seleccionar tipo específico
        elif estado['etapa'] == 'tipo':
            return self._procesar_tipo(mensaje, estado)

        # ETAPA 3: Ingresar área
        elif estado['etapa'] == 'area':
            return self._procesar_area(mensaje, estado)

        # ETAPA 4: Ingresar pisos
        elif estado['etapa'] == 'pisos':
            return self._procesar_pisos(mensaje, estado)

        # ETAPA 5: Generar cotización
        elif estado['etapa'] == 'cotizacion':
            return self._generar_cotizacion(estado)

        # ETAPA 6+: Agendamiento (opcional)
        elif estado['etapa'] in ['agendar_nombre', 'agendar_telefono', 'agendar_direccion']:
            return self._procesar_agendamiento(mensaje, estado)

        # Default: Iniciar flujo
        else:
            return self._mensaje_bienvenida()

    # ═══════════════════════════════════════════════════════════════════════
    # 📊 PROCESAMIENTO POR ETAPAS
    # ═══════════════════════════════════════════════════════════════════════

    def _procesar_categoria(self, mensaje: str, estado: Dict) -> Dict[str, Any]:
        """Procesa selección de categoría"""
        # Detectar categoría del mensaje
        categoria = self._detectar_categoria(mensaje)

        if categoria:
            # Generar botones de tipos específicos
            tipos = self.kb['tipos'].get(categoria, [])
            botones = [{"text": t['icon'] + " " + t['name'], "value": t['value']} for t in tipos]

            mensaje_template = self.config['mensajes']['confirm_categoria']
            respuesta = mensaje_template.format(
                categoria=categoria.title()
            )

            return {
                "respuesta": respuesta,
                "datos": {"categoria": categoria},
                "siguiente_accion": "recopilar_datos",
                "botones": botones,
                "progreso": "2/5",
                "etapa_siguiente": "tipo"
            }

        # No detectó categoría → Mostrar botones
        return self._mensaje_bienvenida()

    def _procesar_tipo(self, mensaje: str, estado: Dict) -> Dict[str, Any]:
        """Procesa selección de tipo específico"""
        # Extraer tipo del mensaje
        tipo_valor = mensaje.upper().replace(" ", "_")
        categoria = estado.get('categoria', 'COMERCIO')

        # Validar que el tipo existe para esa categoría
        tipos_validos = [t['value'] for t in self.kb['tipos'].get(categoria, [])]

        if tipo_valor in tipos_validos:
            mensaje_template = self.config['mensajes']['ask_area']
            respuesta = mensaje_template.format(
                tipo=mensaje.title()
            )

            return {
                "respuesta": respuesta,
                "datos": {
                    **estado,
                    "tipo": tipo_valor
                },
                "siguiente_accion": "recopilar_datos",
                "progreso": "3/5",
                "etapa_siguiente": "area"
            }

        # Tipo no válido
        return {
            "respuesta": "Por favor selecciona un tipo válido de la lista.",
            "datos": estado,
            "siguiente_accion": "recopilar_datos",
            "etapa_siguiente": "tipo"
        }

    def _procesar_area(self, mensaje: str, estado: Dict) -> Dict[str, Any]:
        """Procesa ingreso de área en m²"""
        # Extraer número del mensaje
        area = self._extraer_numero(mensaje)

        if area and 10 <= area <= 10000:
            mensaje_template = self.config['mensajes']['ask_pisos']
            respuesta = mensaje_template.format(
                area=area
            )

            return {
                "respuesta": respuesta,
                "datos": {
                    **estado,
                    "area_m2": area
                },
                "siguiente_accion": "recopilar_datos",
                "progreso": "4/5",
                "etapa_siguiente": "pisos"
            }

        # Área no válida
        return {
            "respuesta": "Por favor ingresa un área válida entre 10 y 10,000 m². Ejemplo: 150",
            "datos": estado,
            "siguiente_accion": "recopilar_datos",
            "etapa_siguiente": "area"
        }

    def _procesar_pisos(self, mensaje: str, estado: Dict) -> Dict[str, Any]:
        """Procesa ingreso de número de pisos"""
        # Extraer número del mensaje
        pisos = self._extraer_numero(mensaje)

        if pisos and 1 <= pisos <= 50:
            # Ya tenemos todos los datos → Calcular y cotizar
            datos_completos = {
                **estado,
                "pisos": int(pisos)
            }

            return self._generar_cotizacion(datos_completos)

        # Pisos no válidos
        return {
            "respuesta": "Por favor ingresa un número de pisos válido entre 1 y 50. Ejemplo: 2",
            "datos": estado,
            "siguiente_accion": "recopilar_datos",
            "etapa_siguiente": "pisos"
        }

    def _generar_cotizacion(self, datos: Dict) -> Dict[str, Any]:
        """Genera cotización completa con cálculo de precios"""
        # 1. Calcular nivel de riesgo
        nivel_riesgo = self._calcular_nivel_riesgo(
            categoria=datos.get('categoria'),
            area=datos.get('area_m2'),
            pisos=datos.get('pisos')
        )

        # 2. Obtener precios
        precios_tupa = self.config['precios_municipales'][nivel_riesgo]
        precios_tesla = self.config['precios_tesla'][nivel_riesgo]

        # 3. Calcular totales
        costo_tupa = precios_tupa['precio']
        costo_tesla_min = precios_tesla['min']
        costo_tesla_max = precios_tesla['max']
        total_min = costo_tupa + costo_tesla_min
        total_max = costo_tupa + costo_tesla_max

        # 4. Formatear mensaje de cotización
        mensaje_template = self.config['mensajes']['cotizacion']
        respuesta = mensaje_template.format(
            riesgo=nivel_riesgo,
            costo_tupa=costo_tupa,
            costo_tesla_min=costo_tesla_min,
            costo_tesla_max=costo_tesla_max,
            incluye_tesla=precios_tesla['incluye'],
            total_min=total_min,
            total_max=total_max,
            dias=precios_tupa['dias']
        )

        # 5. Botones de acción
        botones = [
            {"text": "📅 Agendar visita", "value": "AGENDAR"},
            {"text": "💬 Más información", "value": "MAS_INFO"},
            {"text": "🔄 Nueva consulta", "value": "RESTART"}
        ]

        # 6. Datos estructurados para documento
        cotizacion_datos = {
            **datos,
            "nivel_riesgo": nivel_riesgo,
            "precios": {
                "tupa": costo_tupa,
                "tesla_min": costo_tesla_min,
                "tesla_max": costo_tesla_max,
                "total_min": total_min,
                "total_max": total_max
            },
            "items": [
                {
                    "descripcion": f"Certificado ITSE - Nivel {nivel_riesgo}",
                    "cantidad": 1,
                    "precio_unitario": costo_tupa,
                    "total": costo_tupa
                },
                {
                    "descripcion": f"Servicio Técnico Tesla - {precios_tesla['incluye']}",
                    "cantidad": 1,
                    "precio_unitario": costo_tesla_min,
                    "total": costo_tesla_min
                }
            ],
            "subtotal": total_min,
            "igv": total_min * 0.18,
            "total": total_min * 1.18
        }

        return {
            "respuesta": respuesta,
            "datos": cotizacion_datos,
            "siguiente_accion": "generar_documento",
            "botones": botones,
            "progreso": "5/5"
        }

    def _procesar_agendamiento(self, mensaje: str, estado: Dict) -> Dict[str, Any]:
        """Procesa flujo de agendamiento (nombre, teléfono, dirección)"""
        etapa = estado.get('etapa')

        if etapa == 'agendar_nombre':
            return {
                "respuesta": self.config['mensajes']['ask_telefono'].format(nombre=mensaje),
                "datos": {**estado, "nombre": mensaje},
                "siguiente_accion": "agendar",
                "etapa_siguiente": "agendar_telefono"
            }

        elif etapa == 'agendar_telefono':
            return {
                "respuesta": self.config['mensajes']['ask_direccion'],
                "datos": {**estado, "telefono": mensaje},
                "siguiente_accion": "agendar",
                "etapa_siguiente": "agendar_direccion"
            }

        elif etapa == 'agendar_direccion':
            datos_completos = {**estado, "direccion": mensaje}
            respuesta = self.config['mensajes']['confirmacion_final'].format(
                nombre=datos_completos.get('nombre'),
                telefono=datos_completos.get('telefono'),
                direccion=mensaje,
                tipo=datos_completos.get('tipo', 'N/A'),
                area=datos_completos.get('area_m2', 'N/A'),
                pisos=datos_completos.get('pisos', 'N/A'),
                riesgo=datos_completos.get('nivel_riesgo', 'N/A')
            )

            return {
                "respuesta": respuesta,
                "datos": datos_completos,
                "siguiente_accion": "completado",
                "botones": [{"text": "🏠 Inicio", "value": "RESTART"}]
            }

        return self._mensaje_bienvenida()

    # ═══════════════════════════════════════════════════════════════════════
    # 🧮 MÉTODOS DE CÁLCULO
    # ═══════════════════════════════════════════════════════════════════════

    def _calcular_nivel_riesgo(self, categoria: str, area: float, pisos: int) -> str:
        """Calcula nivel de riesgo según categoría, área y pisos"""
        reglas = self.config['reglas_calculo_riesgo'].get(categoria, [])

        for regla in reglas:
            condicion = regla['condicion']

            # Evaluar condición simple
            if self._evaluar_condicion(condicion, area, pisos):
                return regla['resultado']

        # Default: MEDIO
        return "MEDIO"

    def _evaluar_condicion(self, condicion: str, area: float, pisos: int) -> bool:
        """Evalúa condición de riesgo"""
        # Reemplazar variables
        condicion = condicion.replace("area", str(area))
        condicion = condicion.replace("pisos", str(pisos))

        try:
            return eval(condicion)
        except:
            return False

    # ═══════════════════════════════════════════════════════════════════════
    # 🔍 MÉTODOS AUXILIARES
    # ═══════════════════════════════════════════════════════════════════════

    def _obtener_estado(self, historial: List[Dict]) -> Dict[str, Any]:
        """Extrae el estado actual de la conversación del historial"""
        if not historial:
            return {"etapa": "inicial"}

        # Obtener último mensaje del asistente
        ultimo = historial[-1] if historial else {}
        datos = ultimo.get('datos', {})

        # Determinar etapa según datos disponibles
        if 'pisos' in datos:
            return {**datos, "etapa": "cotizacion"}
        elif 'area_m2' in datos:
            return {**datos, "etapa": "pisos"}
        elif 'tipo' in datos:
            return {**datos, "etapa": "area"}
        elif 'categoria' in datos:
            return {**datos, "etapa": "tipo"}
        else:
            return {"etapa": "categoria"}

    def _detectar_categoria(self, mensaje: str) -> Optional[str]:
        """Detecta categoría del establecimiento del mensaje"""
        mensaje_lower = mensaje.lower()

        # Buscar por keywords
        categorias_keywords = {
            "SALUD": ["salud", "hospital", "clinica", "medico", "consultorio", "laboratorio"],
            "EDUCACION": ["educacion", "colegio", "universidad", "instituto", "academia"],
            "HOSPEDAJE": ["hotel", "hostal", "hospedaje", "albergue"],
            "COMERCIO": ["tienda", "comercio", "supermercado", "bodega"],
            "RESTAURANTE": ["restaurante", "cafeteria", "bar", "discoteca"],
            "OFICINA": ["oficina", "coworking", "estudio"],
            "INDUSTRIAL": ["fabrica", "industrial", "planta", "taller", "almacen"],
            "ENCUENTRO": ["teatro", "cine", "auditorio", "gimnasio", "estadio"]
        }

        for categoria, keywords in categorias_keywords.items():
            if any(kw in mensaje_lower for kw in keywords):
                return categoria

        return None

    def _extraer_numero(self, mensaje: str) -> Optional[float]:
        """Extrae número del mensaje"""
        # Buscar patrón de número
        match = re.search(r'(\d+(?:\.\d+)?)', mensaje)
        if match:
            return float(match.group(1))
        return None

    def _mensaje_bienvenida(self) -> Dict[str, Any]:
        """Mensaje de bienvenida con botones de categorías"""
        botones = [
            {"text": cat['icon'] + " " + cat['name'], "value": cat['value']}
            for cat in self.kb['categorias']
        ]

        return {
            "respuesta": self.config['mensajes']['presentacion'],
            "datos": {},
            "siguiente_accion": "recopilar_datos",
            "botones": botones,
            "progreso": "1/5",
            "etapa_siguiente": "categoria"
        }
