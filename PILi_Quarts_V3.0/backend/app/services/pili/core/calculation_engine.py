"""
💰 CALCULATION ENGINE - Motor de Cálculos Reutilizable
Maneja toda la lógica de cálculos y generación de cotizaciones
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class CalculationEngine:
    """Motor de cálculos reutilizable para todos los especialistas"""
    
    def calculate_itse_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula cotización para ITSE
        
        Args:
            data: Datos recopilados (categoria, tipo, area, pisos)
        
        Returns:
            Diccionario con costos calculados
        """
        # Obtener datos
        categoria = data.get('categoria', '')
        tipo = data.get('tipo', '')
        area = data.get('area', 0)
        pisos = data.get('pisos', 1)
        
        # Calcular riesgo
        riesgo = self._calculate_itse_risk(categoria, area, pisos)
        
        # Costo TUPA (fijo según categoría y riesgo)
        costo_tupa = self._get_itse_tupa_cost(categoria, riesgo)
        
        # Costo servicio (según riesgo y área)
        costo_servicio = self._calculate_itse_service_cost(area, pisos, riesgo)
        
        # Totales
        subtotal = costo_tupa + costo_servicio
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            'categoria': categoria,
            'tipo': tipo,
            'area': area,
            'pisos': pisos,
            'riesgo': riesgo,
            'costo_tupa': round(costo_tupa, 2),
            'costo_servicio': round(costo_servicio, 2),
            'subtotal': round(subtotal, 2),
            'igv': round(igv, 2),
            'total': round(total, 2),
            'tiempo_entrega': '7 días hábiles',
            'condiciones': 'Visita técnica GRATUITA',
            'garantia': '100% aprobación'
        }
    
    def _calculate_itse_risk(self, categoria: str, area: float, pisos: int) -> str:
        """Calcula nivel de riesgo para ITSE"""
        # Categorías de alto riesgo
        if categoria in ['SALUD', 'INDUSTRIAL', 'ENCUENTRO']:
            return 'ALTO'
        
        # Área grande o muchos pisos = riesgo medio
        if area > 500 or pisos > 3:
            return 'MEDIO'
        
        return 'BAJO'
    
    def _get_itse_tupa_cost(self, categoria: str, riesgo: str) -> float:
        """Obtiene costo TUPA según categoría y riesgo"""
        # Costos TUPA oficiales Huancayo 2024
        costos = {
            'SALUD': {'ALTO': 703.00, 'MEDIO': 550.00, 'BAJO': 450.00},
            'EDUCACION': {'ALTO': 550.00, 'MEDIO': 450.00, 'BAJO': 350.00},
            'HOSPEDAJE': {'ALTO': 650.00, 'MEDIO': 550.00, 'BAJO': 450.00},
            'COMERCIO': {'ALTO': 500.00, 'MEDIO': 400.00, 'BAJO': 300.00},
            'RESTAURANTE': {'ALTO': 600.00, 'MEDIO': 500.00, 'BAJO': 400.00},
            'OFICINA': {'ALTO': 450.00, 'MEDIO': 350.00, 'BAJO': 250.00},
            'INDUSTRIAL': {'ALTO': 800.00, 'MEDIO': 650.00, 'BAJO': 500.00},
            'ENCUENTRO': {'ALTO': 700.00, 'MEDIO': 600.00, 'BAJO': 500.00}
        }
        
        return costos.get(categoria, {}).get(riesgo, 500.00)
    
    def _calculate_itse_service_cost(self, area: float, pisos: int, riesgo: str) -> float:
        """Calcula costo del servicio técnico"""
        # Base según riesgo
        base_costs = {
            'ALTO': 1000.00,
            'MEDIO': 700.00,
            'BAJO': 500.00
        }
        
        base = base_costs.get(riesgo, 700.00)
        
        # Costo por m²
        cost_per_m2 = {
            'ALTO': 0.80,
            'MEDIO': 0.50,
            'BAJO': 0.30
        }
        
        area_cost = area * cost_per_m2.get(riesgo, 0.50)
        
        # Costo por piso adicional
        if pisos > 1:
            floor_cost = (pisos - 1) * 150.00
        else:
            floor_cost = 0
        
        return base + area_cost + floor_cost
    
    def calculate_electricidad_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula cotización para instalaciones eléctricas
        
        Args:
            data: Datos recopilados
        
        Returns:
            Diccionario con costos calculados
        """
        tipo = data.get('tipo', 'RESIDENCIAL')
        area = data.get('area', 0)
        puntos = data.get('puntos', 0)
        potencia = data.get('potencia', 0)
        
        # Costo por punto
        cost_per_point = {
            'RESIDENCIAL': 80.00,
            'COMERCIAL': 120.00,
            'INDUSTRIAL': 180.00
        }
        
        costo_puntos = puntos * cost_per_point.get(tipo, 100.00)
        
        # Costo por potencia (tableros, cables gruesos)
        costo_potencia = potencia * 15.00
        
        # Materiales (estimado)
        costo_materiales = (area * 25.00) + (puntos * 35.00)
        
        # Mano de obra
        costo_mano_obra = (puntos * 45.00) + (area * 12.00)
        
        subtotal = costo_puntos + costo_potencia + costo_materiales + costo_mano_obra
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            'tipo': tipo,
            'area': area,
            'puntos': puntos,
            'potencia': potencia,
            'costo_puntos': round(costo_puntos, 2),
            'costo_potencia': round(costo_potencia, 2),
            'costo_materiales': round(costo_materiales, 2),
            'costo_mano_obra': round(costo_mano_obra, 2),
            'subtotal': round(subtotal, 2),
            'igv': round(igv, 2),
            'total': round(total, 2),
            'tiempo_entrega': '10-15 días hábiles',
            'garantia': '1 año en instalación'
        }
    
    def calculate_pozo_tierra_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula cotización para pozo a tierra"""
        tipo = data.get('tipo', 'SIMPLE')
        resistencia_objetivo = data.get('resistencia', 25)
        
        # Costos base
        costos_base = {
            'SIMPLE': 800.00,
            'COMPUESTO': 1500.00,
            'MALLA': 2500.00
        }
        
        costo_base = costos_base.get(tipo, 1000.00)
        
        # Ajuste por resistencia objetivo (más bajo = más caro)
        if resistencia_objetivo < 10:
            ajuste = 500.00
        elif resistencia_objetivo < 25:
            ajuste = 200.00
        else:
            ajuste = 0
        
        subtotal = costo_base + ajuste
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            'tipo': tipo,
            'resistencia_objetivo': resistencia_objetivo,
            'costo_base': round(costo_base, 2),
            'ajuste_resistencia': round(ajuste, 2),
            'subtotal': round(subtotal, 2),
            'igv': round(igv, 2),
            'total': round(total, 2),
            'tiempo_entrega': '5-7 días hábiles',
            'garantia': '2 años'
        }
    
    def calculate_contraincendios_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula cotización para sistemas contraincendios"""
        tipo = data.get('tipo', 'DETECCION')
        area = data.get('area', 0)
        pisos = data.get('pisos', 1)
        
        # Costos por tipo
        costo_deteccion = area * 15.00
        costo_extincion = area * 25.00 if tipo in ['ROCIADORES', 'COMPLETO'] else 0
        costo_accesorios = pisos * 300.00
        
        subtotal = costo_deteccion + costo_extincion + costo_accesorios
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            'tipo': tipo,
            'area': area,
            'pisos': pisos,
            'costo_deteccion': round(costo_deteccion, 2),
            'costo_extincion': round(costo_extincion, 2),
            'costo_accesorios': round(costo_accesorios, 2),
            'subtotal': round(subtotal, 2),
            'igv': round(igv, 2),
            'total': round(total, 2),
            'tiempo_entrega': '15-20 días hábiles',
            'garantia': '1 año'
        }
    
    def calculate_domotica_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula cotización para domótica"""
        tipo = data.get('tipo', 'BASICO')
        area = data.get('area', 0)
        dispositivos = data.get('dispositivos', 0)
        
        # Costos
        costos_hub = {'BASICO': 800.00, 'INTERMEDIO': 1500.00, 'AVANZADO': 3000.00}
        costo_hub = costos_hub.get(tipo, 1500.00)
        costo_dispositivos = dispositivos * 150.00
        costo_instalacion = area * 10.00 + dispositivos * 50.00
        
        subtotal = costo_hub + costo_dispositivos + costo_instalacion
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            'tipo': tipo,
            'area': area,
            'dispositivos': dispositivos,
            'costo_hub': round(costo_hub, 2),
            'costo_dispositivos': round(costo_dispositivos, 2),
            'costo_instalacion': round(costo_instalacion, 2),
            'subtotal': round(subtotal, 2),
            'igv': round(igv, 2),
            'total': round(total, 2),
            'tiempo_entrega': '10-12 días hábiles',
            'garantia': '1 año'
        }
    
    def calculate_cctv_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula cotización para CCTV"""
        tipo = data.get('tipo', 'IP')
        camaras = data.get('camaras', 0)
        grabacion = data.get('grabacion', '15')
        
        # Costos por cámara
        costos_camara = {'ANALOGICO': 300.00, 'IP': 500.00, 'HIBRIDO': 400.00}
        costo_camaras = camaras * costos_camara.get(tipo, 400.00)
        
        # Costo grabación
        dias = int(grabacion)
        costo_grabacion = 800.00 + (dias * 20.00)
        
        # Instalación
        costo_instalacion = camaras * 100.00
        
        subtotal = costo_camaras + costo_grabacion + costo_instalacion
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            'tipo': tipo,
            'camaras': camaras,
            'grabacion': grabacion,
            'costo_camaras': round(costo_camaras, 2),
            'costo_grabacion': round(costo_grabacion, 2),
            'costo_instalacion': round(costo_instalacion, 2),
            'subtotal': round(subtotal, 2),
            'igv': round(igv, 2),
            'total': round(total, 2),
            'tiempo_entrega': '7-10 días hábiles',
            'garantia': '1 año'
        }
    
    def calculate_redes_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula cotización para redes de datos"""
        tipo = data.get('tipo', 'CAT6')
        puntos = data.get('puntos', 0)
        
        # Costos por punto
        costos_punto = {'CAT5E': 80.00, 'CAT6': 120.00, 'FIBRA': 200.00}
        costo_puntos = puntos * costos_punto.get(tipo, 120.00)
        
        # Equipamiento activo
        costo_equipos = 1500.00 + (puntos * 15.00)
        
        # Certificación
        costo_certificacion = puntos * 20.00
        
        subtotal = costo_puntos + costo_equipos + costo_certificacion
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            'tipo': tipo,
            'puntos': puntos,
            'costo_puntos': round(costo_puntos, 2),
            'costo_equipos': round(costo_equipos, 2),
            'costo_certificacion': round(costo_certificacion, 2),
            'subtotal': round(subtotal, 2),
            'igv': round(igv, 2),
            'total': round(total, 2),
            'tiempo_entrega': '12-15 días hábiles',
            'garantia': '10 años en cableado'
        }
    
    def calculate_automatizacion_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula cotización para automatización industrial"""
        tipo = data.get('tipo', 'PLC')
        equipos = data.get('equipos', 0)
        
        # Costos por equipo
        costos_equipo = {'PLC': 3000.00, 'VARIADORES': 2000.00, 'COMPLETO': 5000.00}
        costo_equipos = equipos * costos_equipo.get(tipo, 3000.00)
        
        # Programación
        costo_programacion = equipos * 800.00
        
        # Puesta en marcha
        costo_puesta_marcha = equipos * 500.00
        
        subtotal = costo_equipos + costo_programacion + costo_puesta_marcha
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            'tipo': tipo,
            'equipos': equipos,
            'costo_equipos': round(costo_equipos, 2),
            'costo_programacion': round(costo_programacion, 2),
            'costo_puesta_marcha': round(costo_puesta_marcha, 2),
            'subtotal': round(subtotal, 2),
            'igv': round(igv, 2),
            'total': round(total, 2),
            'tiempo_entrega': '20-30 días hábiles',
            'garantia': '1 año'
        }
    
    def calculate_expedientes_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula cotización para expedientes técnicos"""
        tipo = data.get('tipo', 'ELECTRICO')
        area = data.get('area', 0)
        
        # Costos base
        costo_memoria = 1500.00
        costo_planos = area * 5.00
        costo_presupuesto = 800.00
        
        subtotal = costo_memoria + costo_planos + costo_presupuesto
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            'tipo': tipo,
            'area': area,
            'costo_memoria': round(costo_memoria, 2),
            'costo_planos': round(costo_planos, 2),
            'costo_presupuesto': round(costo_presupuesto, 2),
            'subtotal': round(subtotal, 2),
            'igv': round(igv, 2),
            'total': round(total, 2),
            'tiempo_entrega': '15-20 días hábiles',
            'garantia': 'Revisiones incluidas'
        }
    
    def calculate_saneamiento_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula cotización para saneamiento"""
        tipo = data.get('tipo', 'COMPLETO')
        area = data.get('area', 0)
        banos = data.get('banos', 0)
        
        # Costos
        costo_agua = area * 20.00
        costo_desague = area * 18.00
        costo_accesorios = banos * 500.00
        
        subtotal = costo_agua + costo_desague + costo_accesorios
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            'tipo': tipo,
            'area': area,
            'banos': banos,
            'costo_agua': round(costo_agua, 2),
            'costo_desague': round(costo_desague, 2),
            'costo_accesorios': round(costo_accesorios, 2),
            'subtotal': round(subtotal, 2),
            'igv': round(igv, 2),
            'total': round(total, 2),
            'tiempo_entrega': '12-15 días hábiles',
            'garantia': '1 año'
        }
