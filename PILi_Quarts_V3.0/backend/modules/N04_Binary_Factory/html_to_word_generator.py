"""
HTML TO WORD GENERATOR - Conversor de Plantillas HTML a Word Profesionales
===========================================================================

PROPÓSITO:
Convertir las plantillas HTML profesionales a documentos Word (.docx)
preservando el formato, colores y estructura visual.

UBICACIÓN: backend/app/services/html_to_word_generator.py

PLANTILLAS DISPONIBLES:
1. PLANTILLA_HTML_COTIZACION_SIMPLE.html
2. PLANTILLA_HTML_COTIZACION_COMPLEJA.html
3. PLANTILLA_HTML_PROYECTO_SIMPLE.html
4. PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html
5. PLANTILLA_HTML_INFORME_TECNICO.html
6. PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html

CARACTERÍSTICAS:
- Reemplazo de variables {{VARIABLE}} con datos reales usando JINJA2
- Soporte para bucles en tablas (Items dinámicos)
- Conversión HTML → Word con formato preservado
- Colores azules Tesla mantenidos
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
import re
import json

from docx import Document
from htmldocx import HtmlToDocx
from jinja2 import Template

logger = logging.getLogger(__name__)


class HTMLToWordGenerator:
    """
    Generador de documentos Word profesionales desde plantillas HTML
    """

    def __init__(self):
        """Inicializar el generador"""
        # Ruta base de plantillas (AUTOCONTENIDO en workspace-modern)
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

        logger.info(f"✅ HTMLToWordGenerator inicializado (Engine: Jinja2)")
        logger.info(f"📁 Plantillas en: {self.plantillas_dir}")

    def _cargar_plantilla(self, tipo_plantilla: str) -> str:
        """
        Cargar plantilla HTML desde archivo (MODO SENIOR: CLONACIÓN EXACTA)
        """
        if tipo_plantilla not in self.plantillas:
            raise ValueError(f"Plantilla no encontrada: {tipo_plantilla}")

        archivo_plantilla = self.plantillas_dir / self.plantillas[tipo_plantilla]

        if not archivo_plantilla.exists():
            raise FileNotFoundError(f"Archivo de plantilla no existe: {archivo_plantilla}")

        with open(archivo_plantilla, 'r', encoding='utf-8') as f:
            contenido = f.read()

        logger.info(f"✅ Plantilla cargada (Source Identity): {archivo_plantilla.name}")
        return contenido

    def _reemplazar_variables(self, html: str, datos: Dict[str, Any]) -> str:
        """
        Inyección de Datos Inteligente (Sincronización ADN)
        Usa BeautifulSoup para manipular el DOM sin romper estilos.
        """
        from bs4 import BeautifulSoup
        import copy

        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 1. INYECCIÓN DE VARIABLES SIMPLES (TEXTO)
            # Buscamos nodos de texto que contengan {{VARIABLE}}
            # Esto respeta los estilos de los spans/divs padres
            for element in soup.find_all(string=re.compile(r'\{\{.*?\}\}')):
                texto_original = element.string
                # Reemplazar variables conocidas
                texto_nuevo = texto_original
                for k, v in datos.items():
                    if isinstance(v, (str, int, float)) and k != "items":
                         # Solo reemplazar si la variable está presente en el string
                         if f"{{{{{k}}}}}" in texto_nuevo:
                             texto_nuevo = texto_nuevo.replace(f"{{{{{k}}}}}", str(v))
                
                # Reemplazar lo que no se encontró por cadena vacía (Limpieza)
                texto_nuevo = re.sub(r'\{\{[A-Z_0-9]+\}\}', '', texto_nuevo)
                
                element.replace_with(texto_nuevo)

            # 2. INYECCIÓN DE TABLA (ITEMS DINÁMICOS)
            # Estrategia: Encontrar la tabla de items, clonar la primera fila de datos,
            # borrar las filas dummy originales, e insertar las reales.
            items = datos.get("items", [])
            if items:
                # Buscar la tabla que tiene headers de items (Item, Descripción, etc.)
                tablas = soup.find_all('table')
                tabla_items = None
                
                for tabla in tablas:
                    headers_text = tabla.get_text().upper()
                    if "DESCRIPCIÓN" in headers_text and "TOTAL" in headers_text:
                        tabla_items = tabla
                        break
                
                if tabla_items and tabla_items.find('tbody'):
                    tbody = tabla_items.find('tbody')
                    filas_originales = tbody.find_all('tr')
                    
                    if filas_originales:
                        # Usar la primera fila como "Molde" (DNA Cloning)
                        molde_fila = copy.copy(filas_originales[0])
                        
                        # Limpiar tbody (Borrar datos dummy del HTML original)
                        tbody.clear()
                        
                        # Generar filas reales
                        for i, item in enumerate(items, 1):
                            nueva_fila = copy.copy(molde_fila)
                            celdas = nueva_fila.find_all('td')
                            
                            # Asumimos estructura estándar del HTML Original Tesla:
                            # 0: Item, 1: Desc, 2: Cant, 3: Und, 4: PU, 5: Total
                            if len(celdas) >= 6:
                                celdas[0].string = str(i).zfill(2)
                                celdas[1].string = item.get('descripcion', '')
                                celdas[2].string = f"{item.get('cantidad', 0):.2f}"
                                celdas[3].string = item.get('unidad', 'und')
                                celdas[4].string = f"$ {item.get('precio_unitario', 0):,.2f}"
                                celdas[5].string = f"$ {item.get('cantidad', 0) * item.get('precio_unitario', 0):,.2f}"
                            
                            tbody.append(nueva_fila)
                        
                        logger.info(f"✅ Tabla inyectada con {len(items)} items reales (ADN conservado).")

            return str(soup)

        except Exception as e:
            logger.error(f"❌ Error en Inyección Inteligente: {e}", exc_info=True)
            # Fallback a reemplazo simple si BS4 falla
            for k, v in datos.items():
                if isinstance(v, (str, int, float)):
                    html = html.replace(f"{{{{{k}}}}}", str(v))
            return html

    def _convertir_html_a_word(self, html: str, ruta_salida: Path) -> Path:
        """
        Convertir HTML a documento Word
        """
        # Crear documento Word vacío
        doc = Document()

        # Crear instancia de HtmlToDocx
        parser = HtmlToDocx()

        # Parsear HTML y agregar al documento
        parser.add_html_to_document(html, doc)

        # Guardar documento
        doc.save(str(ruta_salida))

        logger.info(f"✅ Documento Word generado: {ruta_salida}")
        return ruta_salida

    def _extraer_nombre_cliente(self, cliente_data: Any) -> str:
        """Extraer nombre del cliente"""
        if isinstance(cliente_data, dict):
            return cliente_data.get('nombre', 'Cliente Demo')
        elif isinstance(cliente_data, str):
            return cliente_data if cliente_data else 'Cliente Demo'
        return 'Cliente Demo'

    # ========================================================================
    # GENERADORES ESPECÍFICOS POR TIPO DE DOCUMENTO
    # ========================================================================

    def generar_cotizacion_simple(
        self,
        datos: Dict[str, Any],
        ruta_salida: Optional[Path] = None
    ) -> Path:
        """Generar cotización simple"""
        logger.info("🔄 Generando cotización simple (Jinja2)...")
        
        html = self._cargar_plantilla("cotizacion_simple")

        datos_completos = {
            "NUMERO_COTIZACION": datos.get("numero", "COT-000000"),
            "CLIENTE_NOMBRE": self._extraer_nombre_cliente(datos.get("cliente")),
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
            "ITEMS_LIST": datos.get("items", []) # Dynamic Items
        }

        html_procesado = self._reemplazar_variables(html, datos_completos)

        if ruta_salida is None:
            ruta_salida = Path("storage/generados") / f"COTIZACION_{datos_completos['NUMERO_COTIZACION']}.docx"

        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_cotizacion_compleja(
        self,
        datos: Dict[str, Any],
        ruta_salida: Optional[Path] = None
    ) -> Path:
        """Generar cotización compleja (Professional)"""
        logger.info("🔄 Generando cotización compleja (Jinja2)...")

        html = self._cargar_plantilla("cotizacion_compleja")

        datos_completos = {
            "NUMERO_COTIZACION": datos.get("numero", "COT-000000-PRO"),
            "CLIENTE_NOMBRE": self._extraer_nombre_cliente(datos.get("cliente")),
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
            "ITEMS_LIST": datos.get("items", []) # Dynamic Items for Table
        }

        html_procesado = self._reemplazar_variables(html, datos_completos)

        if ruta_salida is None:
            ruta_salida = Path("storage/generados") / f"COTIZACION_COMPLEJA_{datos_completos['NUMERO_COTIZACION']}.docx"

        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_proyecto_simple(self, datos: Dict[str, Any], ruta_salida: Optional[Path] = None) -> Path:
        html = self._cargar_plantilla("proyecto_simple")
        datos_completos = {
            "NOMBRE_PROYECTO": datos.get("nombre", "Proyecto Demo"),
            "CODIGO_PROYECTO": datos.get("codigo", "PROY-000000"),
            "CLIENTE": self._extraer_nombre_cliente(datos.get("cliente")),
            "DURACION_TOTAL": datos.get("duracion_total", "30"),
            "FECHA_INICIO": datos.get("fecha_inicio", datetime.now().strftime("%d/%m/%Y")),
            "FECHA_FIN": datos.get("fecha_fin", ""),
            "PRESUPUESTO": f"{datos.get('presupuesto', 50000):,.2f}",
            "ALCANCE_PROYECTO": datos.get("alcance", "Alcance del proyecto"),
            "NORMATIVA_APLICABLE": datos.get("normativa", "CNE Suministro 2011"),
            "DIAS_INGENIERIA": datos.get("dias_ingenieria", "7"),
            "DIAS_EJECUCION": datos.get("dias_ejecucion", "15")
        }
        html_procesado = self._reemplazar_variables(html, datos_completos)
        if ruta_salida is None: ruta_salida = Path("storage/generados") / f"PROYECTO_{datos_completos['CODIGO_PROYECTO']}.docx"
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_proyecto_complejo(self, datos: Dict[str, Any], ruta_salida: Optional[Path] = None) -> Path:
        html = self._cargar_plantilla("proyecto_complejo")
        datos_completos = {
            "NOMBRE_PROYECTO": datos.get("nombre", "Proyecto PMI Demo"),
            "CODIGO_PROYECTO": datos.get("codigo", "PROY-000000-PMI"),
            "CLIENTE": self._extraer_nombre_cliente(datos.get("cliente")),
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
        html_procesado = self._reemplazar_variables(html, datos_completos)
        if ruta_salida is None: ruta_salida = Path("storage/generados") / f"PROJECT_CHARTER_{datos_completos['CODIGO_PROYECTO']}.docx"
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_informe_tecnico(self, datos: Dict[str, Any], ruta_salida: Optional[Path] = None) -> Path:
        html = self._cargar_plantilla("informe_tecnico")
        datos_completos = {
            "TITULO_INFORME": datos.get("titulo", "Informe Técnico Demo"),
            "CODIGO_INFORME": datos.get("codigo", "INF-000000"),
            "CLIENTE": self._extraer_nombre_cliente(datos.get("cliente")),
            "FECHA": datos.get("fecha", datetime.now().strftime("%d/%m/%Y")),
            "RESUMEN_EJECUTIVO": datos.get("resumen", "Resumen ejecutivo del informe técnico"),
            "SERVICIO_NOMBRE": datos.get("servicio_nombre", "Servicio Técnico"),
            "NORMATIVA_APLICABLE": datos.get("normativa", "CNE Suministro 2011")
        }
        html_procesado = self._reemplazar_variables(html, datos_completos)
        if ruta_salida is None: ruta_salida = Path("storage/generados") / f"INFORME_TECNICO_{datos_completos['CODIGO_INFORME']}.docx"
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_informe_ejecutivo(self, datos: Dict[str, Any], ruta_salida: Optional[Path] = None) -> Path:
        html = self._cargar_plantilla("informe_ejecutivo")
        datos_completos = {
            "TITULO_PROYECTO": datos.get("titulo", "Proyecto Ejecutivo Demo"),
            "CODIGO_INFORME": datos.get("codigo", "INF-000000-EXE"),
            "CLIENTE": self._extraer_nombre_cliente(datos.get("cliente")),
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
        html_procesado = self._reemplazar_variables(html, datos_completos)
        if ruta_salida is None: ruta_salida = Path("storage/generados") / f"INFORME_EJECUTIVO_{datos_completos['CODIGO_INFORME']}.docx"
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)


# ============================================================================
# INSTANCIA GLOBAL
# ============================================================================

html_to_word_generator = HTMLToWordGenerator()

logger.info("✅ HTMLToWordGenerator disponible globalmente")
