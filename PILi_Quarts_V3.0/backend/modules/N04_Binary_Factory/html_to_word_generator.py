"""
HTML TO WORD GENERATOR - Conversor de Plantillas HTML a Word Profesionales
===========================================================================
Versión Restaurada (Protocolo Gold - 14 Dic 2025)
Propósito: Mantener la fidelidad absoluta de los 6 modelos soberanos.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
import re
import os

from docx import Document
from htmldocx import HtmlToDocx

logger = logging.getLogger(__name__)

class HTMLToWordGenerator:
    """
    Generador de documentos Word profesionales desde plantillas HTML
    """

    def __init__(self):
        """Inicializar el generador adaptado para el módulo N04 aislado"""
        # En N04 aislado, las plantillas están en ./templates/html
        self.plantillas_dir = Path(__file__).parent / "templates" / "html"

        # Mapeo de plantillas
        self.plantillas = {
            "cotizacion_simple": "PLANTILLA_HTML_COTIZACION_SIMPLE.html",
            "cotizacion_compleja": "PLANTILLA_HTML_COTIZACION_COMPLEJA.html",
            "proyecto_simple": "PLANTILLA_HTML_PROYECTO_SIMPLE.html",
            "proyecto_complejo": "PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html",
            "informe_tecnico": "PLANTILLA_HTML_INFORME_TECNICO.html",
            "informe_ejecutivo": "PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html"
        }

        logger.info(f"✅ HTMLToWordGenerator (Modo SOBERANO) inicializado")
        logger.info(f"📁 Plantillas en: {self.plantillas_dir}")

    def _cargar_plantilla(self, tipo_plantilla: str) -> str:
        """Cargar plantilla HTML desde archivo"""
        if tipo_plantilla not in self.plantillas:
            raise ValueError(f"Plantilla no encontrada: {tipo_plantilla}")

        archivo_plantilla = self.plantillas_dir / self.plantillas[tipo_plantilla]

        if not archivo_plantilla.exists():
            # Fallback a DOCUMENTOS TESIS si no está en el módulo
            archivo_plantilla = Path(r"e:\PILi_Quarts\DOCUMENTOS TESIS") / self.plantillas[tipo_plantilla]
            
        if not archivo_plantilla.exists():
            raise FileNotFoundError(f"Archivo de plantilla no existe: {archivo_plantilla}")

        with open(archivo_plantilla, 'r', encoding='utf-8') as f:
            contenido = f.read()

        return contenido

    def _reemplazar_variables(self, html: str, datos: Dict[str, Any]) -> str:
        """Reemplazar variables {{VARIABLE}} con datos reales"""
        html_procesado = html
        for clave, valor in datos.items():
            valor_str = str(valor) if valor is not None else ""
            patron = r'\{\{' + clave + r'\}\}'
            html_procesado = re.sub(patron, valor_str, html_procesado)
        
        # También manejar minúsculas por si acaso
        for clave, valor in datos.items():
            valor_str = str(valor) if valor is not None else ""
            patron = r'\{\{' + clave.lower() + r'\}\}'
            html_procesado = re.sub(patron, valor_str, html_procesado)

        return html_procesado

    def _convertir_html_a_word(self, html: str, ruta_salida: Path) -> Path:
        """Convertir HTML a documento Word preservando el Master Tesla como base"""
        # Intentar cargar master_tesla para mantener márgenes y logos de fondo si existen
        master_path = Path(__file__).parent / "templates" / "master_tesla.docx"
        if master_path.exists():
            doc = Document(str(master_path))
        else:
            doc = Document()

        parser = HtmlToDocx()
        parser.add_html_to_document(html, doc)
        doc.save(str(ruta_salida))
        return ruta_salida

    def _extraer_nombre_cliente(self, cliente_data: Any) -> str:
        if isinstance(cliente_data, dict):
            return cliente_data.get('nombre', 'Cliente Demo')
        return str(cliente_data) if cliente_data else 'Cliente Demo'

    # Generadores específicos (Restauración del 14 dic)
    
    def generar_cotizacion_simple(self, datos: Dict[str, Any], ruta_salida: Optional[Path] = None) -> Path:
        html = self._cargar_plantilla("cotizacion_simple")
        datos_completos = {
            "NUMERO_COTIZACION": datos.get("numero", "COT-000000"),
            "CLIENTE_NOMBRE": self._extraer_nombre_cliente(datos.get("cliente")),
            "PROYECTO_NOMBRE": datos.get("proyecto", "Proyecto Demo"),
            "FECHA_COTIZACION": datos.get("fecha", datetime.now().strftime("%d/%m/%Y")),
            "VIGENCIA": datos.get("vigencia", "30 días calendario"),
            "SUBTOTAL": f"{datos.get('subtotal', 0):,.2f}" if isinstance(datos.get('subtotal'), (int, float)) else datos.get('subtotal', "0.00"),
            "IGV": f"{datos.get('igv', 0):,.2f}" if isinstance(datos.get('igv'), (int, float)) else datos.get('igv', "0.00"),
            "TOTAL": f"{datos.get('total', 0):,.2f}" if isinstance(datos.get('total'), (int, float)) else datos.get('total', "0.00"),
            "NORMATIVA_APLICABLE": datos.get("normativa", "CNE Suministro 2011")
        }
        html_procesado = self._reemplazar_variables(html, datos_completos)
        if not ruta_salida: ruta_salida = Path("storage/generados") / f"COT_{datos_completos['NUMERO_COTIZACION']}.docx"
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_cotizacion_compleja(self, datos: Dict[str, Any], ruta_salida: Optional[Path] = None) -> Path:
        html = self._cargar_plantilla("cotizacion_compleja")
        datos_completos = {
            "NUMERO_COTIZACION": datos.get("numero", "COT-PRO-000"),
            "CLIENTE_NOMBRE": self._extraer_nombre_cliente(datos.get("cliente")),
            "PROYECTO_NOMBRE": datos.get("proyecto", "Proyecto Profesional"),
            "FECHA_COTIZACION": datos.get("fecha", datetime.now().strftime("%d/%m/%Y")),
            "SUBTOTAL": f"{datos.get('subtotal', 0):,.2f}",
            "IGV": f"{datos.get('igv', 0):,.2f}",
            "TOTAL": f"{datos.get('total', 0):,.2f}"
        }
        # Inyectar campos dinámicos
        for k, v in datos.items():
            if k.upper() not in datos_completos: datos_completos[k.upper()] = v

        html_procesado = self._reemplazar_variables(html, datos_completos)
        if not ruta_salida: ruta_salida = Path("storage/generados") / f"COT_COMPLEJA_{datos_completos['NUMERO_COTIZACION']}.docx"
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_proyecto_simple(self, datos: Dict[str, Any], ruta_salida: Optional[Path] = None) -> Path:
        html = self._cargar_plantilla("proyecto_simple")
        datos_completos = {
            "NOMBRE_PROYECTO": datos.get("nombre", datos.get("proyecto", "Proyecto")),
            "CODIGO_PROYECTO": datos.get("codigo", "PRO-000"),
            "CLIENTE": self._extraer_nombre_cliente(datos.get("cliente")),
            "FECHA_INICIO": datos.get("fecha_inicio", datetime.now().strftime("%d/%m/%Y")),
            "PRESUPUESTO": f"{datos.get('presupuesto', 0):,.2f}"
        }
        html_procesado = self._reemplazar_variables(html, datos_completos)
        if not ruta_salida: ruta_salida = Path("storage/generados") / f"PROY_{datos_completos['CODIGO_PROYECTO']}.docx"
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_proyecto_complejo(self, datos: Dict[str, Any], ruta_salida: Optional[Path] = None) -> Path:
        html = self._cargar_plantilla("proyecto_complejo")
        datos_completos = {
            "NOMBRE_PROYECTO": datos.get("nombre", "Proyecto PMI"),
            "CODIGO_PROYECTO": datos.get("codigo", "PMI-000"),
            "CLIENTE": self._extraer_nombre_cliente(datos.get("cliente")),
            "SPI": datos.get("spi", "1.0"),
            "CPI": datos.get("cpi", "1.0")
        }
        html_procesado = self._reemplazar_variables(html, datos_completos)
        if not ruta_salida: ruta_salida = Path("storage/generados") / f"PMI_{datos_completos['CODIGO_PROYECTO']}.docx"
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_informe_tecnico(self, datos: Dict[str, Any], ruta_salida: Optional[Path] = None) -> Path:
        html = self._cargar_plantilla("informe_tecnico")
        datos_completos = {
            "TITULO_INFORME": datos.get("titulo", "Informe Técnico"),
            "CODIGO_INFORME": datos.get("codigo", "INF-000"),
            "CLIENTE": self._extraer_nombre_cliente(datos.get("cliente")),
            "FECHA": datos.get("fecha", datetime.now().strftime("%d/%m/%Y"))
        }
        html_procesado = self._reemplazar_variables(html, datos_completos)
        if not ruta_salida: ruta_salida = Path("storage/generados") / f"INF_{datos_completos['CODIGO_INFORME']}.docx"
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_informe_ejecutivo(self, datos: Dict[str, Any], ruta_salida: Optional[Path] = None) -> Path:
        html = self._cargar_plantilla("informe_ejecutivo")
        datos_completos = {
            "TITULO_PROYECTO": datos.get("titulo", "Análisis Ejecutivo"),
            "CODIGO_INFORME": datos.get("codigo", "EXE-000"),
            "CLIENTE": self._extraer_nombre_cliente(datos.get("cliente")),
            "ROI_ESTIMADO": datos.get("roi", "0")
        }
        html_procesado = self._reemplazar_variables(html, datos_completos)
        if not ruta_salida: ruta_salida = Path("storage/generados") / f"EXE_{datos_completos['CODIGO_INFORME']}.docx"
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

html_to_word_generator = HTMLToWordGenerator()
