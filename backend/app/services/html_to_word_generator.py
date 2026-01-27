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
- Reemplazo de variables {{VARIABLE}} con datos reales
- Conversión HTML → Word con formato preservado
- Colores azules Tesla mantenidos
- Tablas, listas y estilos profesionales
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
import re

from docx import Document
from htmldocx import HtmlToDocx

logger = logging.getLogger(__name__)


class HTMLToWordGenerator:
    """
    Generador de documentos Word profesionales desde plantillas HTML
    """

    def __init__(self):
        """Inicializar el generador"""
        # Ruta base de plantillas
        self.plantillas_dir = Path(__file__).parent.parent.parent.parent / "DOCUMENTOS TESIS"

        # Mapeo de plantillas
        self.plantillas = {
            "cotizacion_simple": "PLANTILLA_HTML_COTIZACION_SIMPLE.html",
            "cotizacion_compleja": "PLANTILLA_HTML_COTIZACION_COMPLEJA.html",
            "proyecto_simple": "PLANTILLA_HTML_PROYECTO_SIMPLE.html",
            "proyecto_complejo": "PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html",
            "informe_tecnico": "PLANTILLA_HTML_INFORME_TECNICO.html",
            "informe_ejecutivo": "PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html"
        }

        logger.info(f"✅ HTMLToWordGenerator inicializado")
        logger.info(f"📁 Plantillas en: {self.plantillas_dir}")

    def _cargar_plantilla(self, tipo_plantilla: str) -> str:
        """
        Cargar plantilla HTML desde archivo

        Args:
            tipo_plantilla: Tipo de plantilla (cotizacion_simple, etc.)

        Returns:
            Contenido HTML de la plantilla
        """
        if tipo_plantilla not in self.plantillas:
            raise ValueError(f"Plantilla no encontrada: {tipo_plantilla}")

        archivo_plantilla = self.plantillas_dir / self.plantillas[tipo_plantilla]

        if not archivo_plantilla.exists():
            raise FileNotFoundError(f"Archivo de plantilla no existe: {archivo_plantilla}")

        with open(archivo_plantilla, 'r', encoding='utf-8') as f:
            contenido = f.read()

        logger.info(f"✅ Plantilla cargada: {archivo_plantilla.name}")
        return contenido

    def _reemplazar_variables(self, html: str, datos: Dict[str, Any]) -> str:
        """
        Reemplazar variables {{VARIABLE}} con datos reales

        Args:
            html: Contenido HTML con variables
            datos: Diccionario con valores para reemplazar

        Returns:
            HTML con variables reemplazadas
        """
        html_procesado = html

        # Reemplazar todas las variables {{VARIABLE}}
        for clave, valor in datos.items():
            # Convertir valor a string
            valor_str = str(valor) if valor is not None else ""

            # Reemplazar en HTML
            patron = r'\{\{' + clave + r'\}\}'
            html_procesado = re.sub(patron, valor_str, html_procesado)

        # Reemplazar variables no encontradas con vacío
        html_procesado = re.sub(r'\{\{[A-Z_0-9]+\}\}', '', html_procesado)

        logger.debug(f"✅ Variables reemplazadas: {len(datos)} variables")
        return html_procesado

    def _convertir_html_a_word(self, html: str, ruta_salida: Path) -> Path:
        """
        Convertir HTML a documento Word

        Args:
            html: Contenido HTML procesado
            ruta_salida: Ruta donde guardar el documento Word

        Returns:
            Path al documento Word generado
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
        """
        Extraer nombre del cliente desde string u objeto
        
        Args:
            cliente_data: Puede ser string o dict con {nombre, ruc, ...}
            
        Returns:
            Nombre del cliente como string
        """
        logger.info(f"🔍 DEBUG _extraer_nombre_cliente - Tipo recibido: {type(cliente_data)}")
        logger.info(f"🔍 DEBUG _extraer_nombre_cliente - Valor: {cliente_data}")
        
        if isinstance(cliente_data, dict):
            # Si es un objeto, extraer el campo 'nombre'
            nombre = cliente_data.get('nombre', 'Cliente Demo')
            logger.info(f"✅ Extraído nombre de dict: {nombre}")
            return nombre
        elif isinstance(cliente_data, str):
            # Si ya es string, usarlo directamente
            nombre = cliente_data if cliente_data else 'Cliente Demo'
            logger.info(f"✅ Usando string directamente: {nombre}")
            return nombre
        else:
            # Fallback
            logger.warning(f"⚠️ Tipo no reconocido, usando fallback: Cliente Demo")
            return 'Cliente Demo'

    # ========================================================================
    # GENERADORES ESPECÍFICOS POR TIPO DE DOCUMENTO
    # ========================================================================

    def generar_cotizacion_simple(
        self,
        datos: Dict[str, Any],
        ruta_salida: Optional[Path] = None
    ) -> Path:
        """
        Generar cotización simple en Word desde plantilla HTML

        Args:
            datos: Datos de la cotización
                - NUMERO_COTIZACION: Número de cotización
                - CLIENTE_NOMBRE: Nombre del cliente
                - PROYECTO_NOMBRE: Nombre del proyecto
                - AREA_M2: Área en m²
                - FECHA_COTIZACION: Fecha
                - VIGENCIA: Vigencia (ej: "30 días calendario")
                - SERVICIO_NOMBRE: Nombre del servicio
                - DESCRIPCION_PROYECTO: Descripción
                - SUBTOTAL: Subtotal
                - IGV: IGV
                - TOTAL: Total
                - NORMATIVA_APLICABLE: Normativa
            ruta_salida: Ruta personalizada (opcional)

        Returns:
            Path al documento Word generado
        """
        logger.info("🔄 Generando cotización simple...")
        
        # 🔍 DEBUG: Ver qué items recibimos
        items_recibidos = datos.get('items', [])
        logger.info(f"🔍 DEBUG generar_cotizacion_simple - Items recibidos: {len(items_recibidos)}")
        for i, item in enumerate(items_recibidos[:3]):  # Solo primeros 3 para no saturar logs
            logger.info(f"  Item {i+1}: {item}")

        # Cargar plantilla
        html = self._cargar_plantilla("cotizacion_simple")

        # Valores por defecto
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
            "NORMATIVA_APLICABLE": datos.get("normativa", "CNE Suministro 2011")
        }

        # Reemplazar variables
        html_procesado = self._reemplazar_variables(html, datos_completos)

        # Ruta de salida
        if ruta_salida is None:
            ruta_salida = Path("storage/generados") / f"COTIZACION_{datos_completos['NUMERO_COTIZACION']}.docx"

        # Crear directorio si no existe
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)

        # Convertir a Word
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_cotizacion_compleja(
        self,
        datos: Dict[str, Any],
        ruta_salida: Optional[Path] = None
    ) -> Path:
        """
        Generar cotización compleja en Word desde plantilla HTML

        Incluye: cronograma, garantías, condiciones de pago
        """
        logger.info("🔄 Generando cotización compleja...")

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
            "DIAS_PRUEBAS": datos.get("dias_pruebas", "5")
        }

        html_procesado = self._reemplazar_variables(html, datos_completos)

        if ruta_salida is None:
            ruta_salida = Path("storage/generados") / f"COTIZACION_COMPLEJA_{datos_completos['NUMERO_COTIZACION']}.docx"

        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_proyecto_simple(
        self,
        datos: Dict[str, Any],
        ruta_salida: Optional[Path] = None
    ) -> Path:
        """
        Generar plan de proyecto simple en Word
        """
        logger.info("🔄 Generando proyecto simple...")

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

        if ruta_salida is None:
            ruta_salida = Path("storage/generados") / f"PROYECTO_{datos_completos['CODIGO_PROYECTO']}.docx"

        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_proyecto_complejo(
        self,
        datos: Dict[str, Any],
        ruta_salida: Optional[Path] = None
    ) -> Path:
        """
        Generar Project Charter PMI en Word
        """
        logger.info("🔄 Generando proyecto complejo PMI...")

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

        if ruta_salida is None:
            ruta_salida = Path("storage/generados") / f"PROJECT_CHARTER_{datos_completos['CODIGO_PROYECTO']}.docx"

        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_informe_tecnico(
        self,
        datos: Dict[str, Any],
        ruta_salida: Optional[Path] = None
    ) -> Path:
        """
        Generar informe técnico en Word
        """
        logger.info("🔄 Generando informe técnico...")

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

        if ruta_salida is None:
            ruta_salida = Path("storage/generados") / f"INFORME_TECNICO_{datos_completos['CODIGO_INFORME']}.docx"

        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)

    def generar_informe_ejecutivo(
        self,
        datos: Dict[str, Any],
        ruta_salida: Optional[Path] = None
    ) -> Path:
        """
        Generar informe ejecutivo en formato APA
        """
        logger.info("🔄 Generando informe ejecutivo APA...")

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

        if ruta_salida is None:
            ruta_salida = Path("storage/generados") / f"INFORME_EJECUTIVO_{datos_completos['CODIGO_INFORME']}.docx"

        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        return self._convertir_html_a_word(html_procesado, ruta_salida)


# ============================================================================
# INSTANCIA GLOBAL
# ============================================================================

html_to_word_generator = HTMLToWordGenerator()

logger.info("✅ HTMLToWordGenerator disponible globalmente")
