
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Imports de N04_Binary_Factory
try:
    from modules.N04_Binary_Factory.html_to_word_generator import html_to_word_generator
    from modules.N04_Binary_Factory.excel_converter import TeslaExcelConverter
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from modules.N04_Binary_Factory.html_to_word_generator import html_to_word_generator
    from modules.N04_Binary_Factory.excel_converter import TeslaExcelConverter

logger = logging.getLogger(__name__)

class ExcelGenerator:
    """
    Generador de Excel V6 - Full Spectrum (6 Modelos)
    Soporte total para los 6 tipos de documentos, usando el motor HTML Twin.
    """
    
    def __init__(self):
        self.converter = TeslaExcelConverter()
        self.html_engine = html_to_word_generator

    def _render_and_convert(self, html_template_key: str, data_context: Dict[str, Any], output_path: str) -> str:
        """Helper centralizado para renderizar HTML y convertir a Excel"""
        try:
            # 1. Cargar Template HTML
            html_raw = self.html_engine._cargar_plantilla(html_template_key)
            
            # 2. Inyectar Datos (Jinja2)
            # Nota: html_to_word_generator._reemplazar_variables maneja BS4 y Jinja
            html_content = self.html_engine._reemplazar_variables(html_raw, data_context)
            
            # 3. Convertir a Excel
            self.converter.convert_html_string(html_content, output_path)
            
            return output_path
        except Exception as e:
            logger.error(f"❌ Error generando Excel ({html_template_key}): {e}")
            raise e

    def _extraer_nombre(self, cliente_data):
        return self.html_engine._extraer_nombre_cliente(cliente_data)

    # ========================================================================
    # 1. COTIZACIÓN SIMPLE
    # ========================================================================
    def generar_cotizacion_simple(self, datos: Dict[str, Any], ruta_salida: str) -> str:
        ctx = {
            "NUMERO_COTIZACION": datos.get("numero", "COT-000000"),
            "CLIENTE_NOMBRE": self._extraer_nombre(datos.get("cliente")),
            "PROYECTO_NOMBRE": datos.get("proyecto", "Proyecto Demo"),
            "AREA_M2": datos.get("area_m2", "100"),
            "FECHA_COTIZACION": datos.get("fecha", datetime.now().strftime("%d/%m/%Y")),
            "VIGENCIA": datos.get("vigencia", "30 días calendario"),
            "SERVICIO_NOMBRE": datos.get("servicio_nombre", "Servicio Eléctrico"),
            "DESCRIPCION_PROYECTO": datos.get("descripcion", "Descripción del proyecto"),
            "SUBTOTAL": f"{datos.get('subtotal', 0):,.2f}",
            "IGV": f"{datos.get('igv', 0):,.2f}",
            "TOTAL": f"{datos.get('total', 0):,.2f}",
            "NORMATIVA_APLICABLE": datos.get("normativa", "CNE Suministro 2011"),
            "items": datos.get("items", []) # Dynamic Items
        }
        return self._render_and_convert("cotizacion_simple", ctx, ruta_salida)

    # ========================================================================
    # 2. COTIZACIÓN COMPLEJA
    # ========================================================================
    def generar_cotizacion_compleja(self, datos: Dict[str, Any], ruta_salida: str) -> str:
        ctx = {
            "NUMERO_COTIZACION": datos.get("numero", "COT-000000-PRO"),
            "CLIENTE_NOMBRE": self._extraer_nombre(datos.get("cliente")),
            "PROYECTO_NOMBRE": datos.get("proyecto", "Proyecto Profesional"),
            "AREA_M2": datos.get("area_m2", "200"),
            "FECHA_COTIZACION": datos.get("fecha", datetime.now().strftime("%d/%m/%Y")),
            "VIGENCIA": datos.get("vigencia", "30 días calendario"),
            "SERVICIO_NOMBRE": datos.get("servicio_nombre", "Servicio Profesional"),
            "DESCRIPCION_PROYECTO": datos.get("descripcion", "Proyecto con ingeniería de detalle"),
            "SUBTOTAL": f"{datos.get('subtotal', 0):,.2f}",
            "IGV": f"{datos.get('igv', 0):,.2f}",
            "TOTAL": f"{datos.get('total', 0):,.2f}",
            "NORMATIVA_APLICABLE": datos.get("normativa", "CNE Suministro 2011"),
            "DIAS_INGENIERIA": datos.get("dias_ingenieria", "7"),
            "DIAS_ADQUISICIONES": datos.get("dias_adquisiciones", "7"),
            "DIAS_INSTALACION": datos.get("dias_instalacion", "15"),
            "DIAS_PRUEBAS": datos.get("dias_pruebas", "5"),
            "items": datos.get("items", [])
        }
        return self._render_and_convert("cotizacion_compleja", ctx, ruta_salida)

    # ========================================================================
    # 3. PROYECTO SIMPLE
    # ========================================================================
    def generar_proyecto_simple(self, datos: Dict[str, Any], ruta_salida: str) -> str:
        ctx = {
            "NOMBRE_PROYECTO": datos.get("nombre", "Proyecto Demo"),
            "CODIGO_PROYECTO": datos.get("codigo", "PROY-000000"),
            "CLIENTE": self._extraer_nombre(datos.get("cliente")),
            "DURACION_TOTAL": datos.get("duracion_total", "30"),
            "FECHA_INICIO": datos.get("fecha_inicio", datetime.now().strftime("%d/%m/%Y")),
            "FECHA_FIN": datos.get("fecha_fin", ""),
            "PRESUPUESTO": f"{datos.get('presupuesto', 50000):,.2f}",
            "ALCANCE_PROYECTO": datos.get("alcance", "Alcance del proyecto"),
            "NORMATIVA_APLICABLE": datos.get("normativa", "CNE Suministro 2011"),
            "DIAS_INGENIERIA": datos.get("dias_ingenieria", "7"),
            "DIAS_EJECUCION": datos.get("dias_ejecucion", "15")
        }
        return self._render_and_convert("proyecto_simple", ctx, ruta_salida)

    # ========================================================================
    # 4. PROYECTO COMPLEJO (PMI)
    # ========================================================================
    def generar_proyecto_complejo(self, datos: Dict[str, Any], ruta_salida: str) -> str:
        ctx = {
            "NOMBRE_PROYECTO": datos.get("nombre", "Proyecto PMI Demo"),
            "CODIGO_PROYECTO": datos.get("codigo", "PROY-000000-PMI"),
            "CLIENTE": self._extraer_nombre(datos.get("cliente")),
            "DURACION_TOTAL": datos.get("duracion_total", "45"),
            "FECHA_INICIO": datos.get("fecha_inicio", datetime.now().strftime("%d/%m/%Y")),
            "FECHA_FIN": datos.get("fecha_fin", ""),
            "PRESUPUESTO": f"{datos.get('presupuesto', 75000):,.2f}",
            "ALCANCE_PROYECTO": datos.get("alcance", "Alcance detallado del proyecto"),
            "NORMATIVA_APLICABLE": datos.get("normativa", "CNE Suministro 2011"),
            "SPI": datos.get("spi", "1.0"),
            "CPI": datos.get("cpi", "1.0"),
            "EV_K": f"{datos.get('ev', 37500) / 1000:.1f}",
            "PV_K": f"{datos.get('pv', 37500) / 1000:.1f}",
            "AC_K": f"{datos.get('ac', 37500) / 1000:.1f}",
            "DIAS_INGENIERIA": datos.get("dias_ingenieria", "12"),
            "DIAS_EJECUCION": datos.get("dias_ejecucion", "25")
        }
        return self._render_and_convert("proyecto_complejo", ctx, ruta_salida)

    # ========================================================================
    # 5. INFORME TÉCNICO
    # ========================================================================
    def generar_informe_tecnico(self, datos: Dict[str, Any], ruta_salida: str) -> str:
        ctx = {
            "TITULO_INFORME": datos.get("titulo", "Informe Técnico Demo"),
            "CODIGO_INFORME": datos.get("codigo", "INF-000000"),
            "CLIENTE": self._extraer_nombre(datos.get("cliente")),
            "FECHA": datos.get("fecha", datetime.now().strftime("%d/%m/%Y")),
            "RESUMEN_EJECUTIVO": datos.get("resumen", "Resumen ejecutivo del informe técnico"),
            "SERVICIO_NOMBRE": datos.get("servicio_nombre", "Servicio Técnico"),
            "NORMATIVA_APLICABLE": datos.get("normativa", "CNE Suministro 2011")
        }
        return self._render_and_convert("informe_tecnico", ctx, ruta_salida)

    # ========================================================================
    # 6. INFORME EJECUTIVO (APA)
    # ========================================================================
    def generar_informe_ejecutivo(self, datos: Dict[str, Any], ruta_salida: str) -> str:
        ctx = {
            "TITULO_PROYECTO": datos.get("titulo", "Proyecto Ejecutivo Demo"),
            "CODIGO_INFORME": datos.get("codigo", "INF-000000-EXE"),
            "CLIENTE": self._extraer_nombre(datos.get("cliente")),
            "FECHA": datos.get("fecha", datetime.now().strftime("%d/%m/%Y")),
            "RESUMEN_EJECUTIVO": datos.get("resumen", "Resumen ejecutivo del análisis de viabilidad"),
            "PRESUPUESTO": f"{datos.get('presupuesto', 50000):,.2f}",
            "ROI_ESTIMADO": datos.get("roi", "25"),
            "PAYBACK_MESES": datos.get("payback", "18"),
            "TIR_PROYECTADA": datos.get("tir", "30"),
            "AHORRO_ANUAL_K": f"{datos.get('ahorro_anual', 7500) / 1000:.1f}",
            "AHORRO_ENERGETICO": f"{datos.get('ahorro_energetico', 7500):,.2f}",
            "SERVICIO_NOMBRE": datos.get("servicio_nombre", "Servicio Ejecutivo"),
            "NORMATIVA_APLICABLE": datos.get("normativa", "CNE Suministro 2011"),
            "INVERSION_EQUIPOS": f"{datos.get('presupuesto', 50000) * 0.7:,.2f}",
            "INVERSION_MANO_OBRA": f"{datos.get('presupuesto', 50000) * 0.2:,.2f}",
            "CAPITAL_TRABAJO": f"{datos.get('presupuesto', 50000) * 0.1:,.2f}"
        }
        return self._render_and_convert("informe_ejecutivo", ctx, ruta_salida)

excel_generator = ExcelGenerator()
