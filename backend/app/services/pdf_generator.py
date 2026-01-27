"""
═══════════════════════════════════════════════════════════════
PDF GENERATOR - Generador de Documentos PDF Profesionales
═══════════════════════════════════════════════════════════════

PROPÓSITO:
Generar documentos PDF profesionales para cotizaciones,
informes de proyectos, y reportes técnicos usando ReportLab.

FUNCIONES PRINCIPALES:
- generar_cotizacion() → Cotizaciones de venta
- generar_informe_proyecto() → Informes ejecutivos de proyectos
- generar_informe_simple() → Informes básicos

CARACTERÍSTICAS:
- Soporte para logo personalizado
- Tablas dinámicas
- Formato profesional
- Estilos Tesla (rojo, dorado, negro)
- No editable (seguridad)

═══════════════════════════════════════════════════════════════
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import logging
import base64
from io import BytesIO

logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    Generador profesional de documentos PDF usando ReportLab
    """
    
    def __init__(self):
        """Inicializar generador"""
        # Colores Tesla
        self.COLOR_ROJO = colors.Color(139/255, 0/255, 0/255)      # #8B0000
        self.COLOR_DORADO = colors.Color(218/255, 165/255, 32/255)  # #DAA520
        self.COLOR_NEGRO = colors.black
        self.COLOR_GRIS = colors.grey
        self.COLOR_BLANCO = colors.white
        
        # Estilos
        self.styles = getSampleStyleSheet()
        self._crear_estilos_personalizados()
        
        logger.info("PDFGenerator inicializado")
    
    def _crear_estilos_personalizados(self):
        """Crear estilos personalizados para el documento"""
        
        # Título principal
        self.styles.add(ParagraphStyle(
            name='TituloTesla',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.COLOR_ROJO,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='SubtituloTesla',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=self.COLOR_ROJO,
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Encabezado de sección
        self.styles.add(ParagraphStyle(
            name='SeccionTesla',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=self.COLOR_ROJO,
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal centrado
        self.styles.add(ParagraphStyle(
            name='NormalCentrado',
            parent=self.styles['Normal'],
            alignment=TA_CENTER,
            fontSize=10
        ))
        
        # Texto pequeño
        self.styles.add(ParagraphStyle(
            name='Pequeno',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=self.COLOR_GRIS
        ))
    
    # ════════════════════════════════════════════════════════
    # FUNCIÓN PRINCIPAL - COTIZACIÓN
    # ════════════════════════════════════════════════════════
    
    def generar_cotizacion(
        self,
        datos: Dict[str, Any],
        ruta_salida: str,
        opciones: Optional[Dict[str, bool]] = None,
        logo_base64: Optional[str] = None
    ) -> str:
        """
        Generar documento PDF de cotización
        
        Args:
            datos: Datos de la cotización
            ruta_salida: Ruta donde guardar el PDF
            opciones: Opciones de visualización
            logo_base64: Logo en base64 (opcional)
        
        Returns:
            Ruta del documento generado
        """
        
        try:
            logger.info(f"Generando PDF cotización: {datos.get('numero', 'N/A')}")
            
            # Configurar opciones
            opts = {
                'mostrar_precios': True,
                'mostrar_igv': True,
                'mostrar_observaciones': True,
                'mostrar_logo': True
            }
            
            if opciones:
                opts.update(opciones)
            
            # Crear directorio si no existe
            Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
            
            # Crear documento
            doc = SimpleDocTemplate(
                ruta_salida,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Contenido
            elementos = []
            
            # 1. Logo
            if logo_base64 and opts['mostrar_logo']:
                logo_img = self._decodificar_logo(logo_base64)
                if logo_img:
                    elementos.append(logo_img)
                    elementos.append(Spacer(1, 12))
            
            # 2. Encabezado empresa
            elementos.append(Paragraph(
                'TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.',
                self.styles['NormalCentrado']
            ))
            elementos.append(Paragraph(
                'RUC: 20601138787',
                self.styles['Pequeno']
            ))
            elementos.append(Spacer(1, 20))
            
            # 3. Título
            elementos.append(Paragraph('COTIZACIÓN', self.styles['TituloTesla']))
            elementos.append(Paragraph(
                datos.get('numero', 'COT-XXXX-XXXX'),
                self.styles['SubtituloTesla']
            ))
            elementos.append(Spacer(1, 20))
            
            # 4. Información del cliente
            info_cliente = [
                f"<b>Cliente:</b> {datos.get('cliente', 'N/A')}",
                f"<b>Proyecto:</b> {datos.get('proyecto', 'N/A')}",
                f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y')}"
            ]
            
            if datos.get('descripcion'):
                info_cliente.append(f"<b>Descripción:</b> {datos.get('descripcion')}")
            
            for info in info_cliente:
                elementos.append(Paragraph(info, self.styles['Normal']))
            
            elementos.append(Spacer(1, 20))
            
            # 5. Tabla de items
            if datos.get('items'):
                elementos.append(Paragraph('DETALLE DE LA COTIZACIÓN', self.styles['SeccionTesla']))
                tabla_items = self._crear_tabla_items(datos['items'], opts)
                elementos.append(tabla_items)
                elementos.append(Spacer(1, 20))
            
            # 6. Totales
            if opts['mostrar_precios']:
                tabla_totales = self._crear_tabla_totales(datos)
                elementos.append(tabla_totales)
                elementos.append(Spacer(1, 20))
            
            # 7. Observaciones
            if opts['mostrar_observaciones'] and datos.get('observaciones'):
                elementos.append(Paragraph('OBSERVACIONES', self.styles['SeccionTesla']))
                elementos.append(Paragraph(datos.get('observaciones'), self.styles['Normal']))
                elementos.append(Spacer(1, 20))
            
            # 8. Condiciones
            elementos.append(Paragraph('CONDICIONES GENERALES', self.styles['SeccionTesla']))
            condiciones = [
                f"• Vigencia de la cotización: {datos.get('vigencia', '30 días')}",
                "• Precios en Soles (S/)",
                "• Incluye IGV",
                "• Condiciones de pago: Por definir"
            ]
            
            for cond in condiciones:
                elementos.append(Paragraph(cond, self.styles['Normal']))
            
            elementos.append(Spacer(1, 40))
            
            # 9. Firma
            elementos.append(Paragraph('_' * 50, self.styles['NormalCentrado']))
            elementos.append(Paragraph('<b>Gerente General</b>', self.styles['NormalCentrado']))
            elementos.append(Paragraph(
                'TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.',
                self.styles['NormalCentrado']
            ))
            
            # Construir PDF
            doc.build(elementos)
            
            logger.info(f"✅ PDF cotización generado: {ruta_salida}")
            
            return ruta_salida
            
        except Exception as e:
            logger.error(f"Error al generar PDF cotización: {str(e)}")
            raise Exception(f"Error al generar PDF: {str(e)}")
    
    # ════════════════════════════════════════════════════════
    # FUNCIÓN PRINCIPAL - INFORME DE PROYECTO (NUEVO)
    # ════════════════════════════════════════════════════════
    
    def generar_informe_proyecto(
        self,
        datos: Dict[str, Any],
        ruta_salida: str,
        opciones: Optional[Dict[str, bool]] = None,
        logo_base64: Optional[str] = None
    ) -> str:
        """
        Generar informe ejecutivo de proyecto en PDF
        
        MODO COMPLEJO - Para proyectos complejos
        
        Args:
            datos: Datos del proyecto
            ruta_salida: Ruta donde guardar el PDF
            opciones: Opciones de visualización
            logo_base64: Logo en base64 (opcional)
        
        Returns:
            Ruta del documento generado
        """
        
        try:
            logger.info(f"Generando PDF informe proyecto: {datos.get('nombre', 'N/A')}")
            
            # Configurar opciones
            opts = {
                'mostrar_logo': True,
                'incluir_cotizaciones': True,
                'incluir_documentos': True,
                'incluir_estadisticas': True
            }
            
            if opciones:
                opts.update(opciones)
            
            # Crear directorio si no existe
            Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
            
            # Crear documento
            doc = SimpleDocTemplate(
                ruta_salida,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Contenido
            elementos = []
            
            # ═══ PORTADA ═══
            
            # Logo
            if logo_base64 and opts['mostrar_logo']:
                logo_img = self._decodificar_logo(logo_base64)
                if logo_img:
                    elementos.append(logo_img)
                    elementos.append(Spacer(1, 20))
            
            # Título
            elementos.append(Paragraph(
                'INFORME EJECUTIVO DE PROYECTO',
                self.styles['TituloTesla']
            ))
            elementos.append(Spacer(1, 12))
            
            # Nombre del proyecto
            elementos.append(Paragraph(
                datos.get('nombre', 'Proyecto Sin Nombre'),
                self.styles['SubtituloTesla']
            ))
            elementos.append(Spacer(1, 8))
            
            # Número y fecha
            elementos.append(Paragraph(
                f"Proyecto #{datos.get('id', 'N/A')}",
                self.styles['NormalCentrado']
            ))
            elementos.append(Paragraph(
                datetime.now().strftime('%d de %B de %Y'),
                self.styles['Pequeno']
            ))
            
            elementos.append(PageBreak())
            
            # ═══ RESUMEN EJECUTIVO ═══
            
            elementos.append(Paragraph('1. RESUMEN EJECUTIVO', self.styles['SeccionTesla']))
            elementos.append(Spacer(1, 12))
            
            # Tabla de información general
            datos_tabla = [
                ['Campo', 'Valor'],
                ['Cliente', datos.get('cliente', 'N/A')],
                ['Proyecto', datos.get('nombre', 'N/A')],
                ['Estado', datos.get('estado', 'N/A').upper()],
                ['Fecha Inicio', self._formatear_fecha(datos.get('fecha_inicio'))],
                ['Fecha Fin', self._formatear_fecha(datos.get('fecha_fin')) or 'En curso'],
                ['Valor Total', f"S/ {float(datos.get('valor_total', 0)):,.2f}"]
            ]
            
            tabla_resumen = Table(datos_tabla, colWidths=[2*inch, 4*inch])
            tabla_resumen.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.COLOR_ROJO),
                ('TEXTCOLOR', (0, 0), (-1, 0), self.COLOR_BLANCO),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (0, -1), colors.Color(0.95, 0.95, 0.95)),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (1, 1), (-1, -1), [colors.white, colors.Color(0.98, 0.98, 0.98)])
            ]))
            
            elementos.append(tabla_resumen)
            elementos.append(Spacer(1, 20))
            
            # Descripción
            if datos.get('descripcion'):
                elementos.append(Paragraph('<b>Descripción del Proyecto:</b>', self.styles['Normal']))
                elementos.append(Paragraph(datos.get('descripcion'), self.styles['Normal']))
                elementos.append(Spacer(1, 20))
            
            # ═══ ESTADÍSTICAS ═══
            
            if opts['incluir_estadisticas']:
                elementos.append(Paragraph('2. ESTADÍSTICAS DEL PROYECTO', self.styles['SeccionTesla']))
                elementos.append(Spacer(1, 12))
                
                # Obtener cotizaciones para calcular estadísticas
                cotizaciones = datos.get('cotizaciones', [])
                total_cot = len(cotizaciones)
                aprobadas = sum(1 for c in cotizaciones if c.get('estado') == 'aprobada')
                valor_total = sum(c.get('total', 0) for c in cotizaciones if c.get('estado') == 'aprobada')
                
                stats_data = [
                    ['Métrica', 'Valor'],
                    ['Total de Cotizaciones', str(total_cot)],
                    ['Cotizaciones Aprobadas', str(aprobadas)],
                    ['Total de Documentos', str(len(datos.get('documentos', [])))],
                    ['Subtotal', f"S/ {valor_total:,.2f}"],
                    ['IGV (18%)', f"S/ {valor_total * 0.18:,.2f}"],
                    ['Total General', f"S/ {valor_total * 1.18:,.2f}"]
                ]
                
                tabla_stats = Table(stats_data, colWidths=[3*inch, 3*inch])
                tabla_stats.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), self.COLOR_ROJO),
                    ('TEXTCOLOR', (0, 0), (-1, 0), self.COLOR_BLANCO),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (0, -1), colors.Color(0.95, 0.95, 0.95)),
                    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
                    ('TEXTCOLOR', (-1, -1), (-1, -1), self.COLOR_ROJO),
                    ('FONTSIZE', (-1, -1), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
                ]))
                
                elementos.append(tabla_stats)
                elementos.append(Spacer(1, 20))
            
            # ═══ COTIZACIONES ASOCIADAS ═══
            
            if opts['incluir_cotizaciones'] and datos.get('cotizaciones'):
                elementos.append(Paragraph('3. COTIZACIONES ASOCIADAS', self.styles['SeccionTesla']))
                elementos.append(Spacer(1, 12))
                
                cotizaciones = datos.get('cotizaciones', [])
                
                if cotizaciones:
                    # Crear tabla
                    cot_data = [['Número', 'Estado', 'Fecha', 'Total']]
                    
                    for cot in cotizaciones:
                        cot_data.append([
                            cot.get('numero', 'N/A'),
                            cot.get('estado', 'N/A').upper(),
                            self._formatear_fecha_str(cot.get('fecha_creacion')),
                            f"S/ {float(cot.get('total', 0)):,.2f}"
                        ])
                    
                    tabla_cot = Table(cot_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
                    tabla_cot.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), self.COLOR_ROJO),
                        ('TEXTCOLOR', (0, 0), (-1, 0), self.COLOR_BLANCO),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.98, 0.98, 0.98)])
                    ]))
                    
                    elementos.append(tabla_cot)
                else:
                    elementos.append(Paragraph('No hay cotizaciones asociadas.', self.styles['Normal']))
                
                elementos.append(Spacer(1, 20))
            
            # ═══ DOCUMENTOS ═══
            
            if opts['incluir_documentos'] and datos.get('documentos'):
                elementos.append(Paragraph('4. DOCUMENTOS DEL PROYECTO', self.styles['SeccionTesla']))
                elementos.append(Spacer(1, 12))
                
                documentos = datos.get('documentos', [])
                
                if documentos:
                    doc_data = [['Nombre', 'Tipo', 'Fecha']]
                    
                    for doc_item in documentos:
                        doc_data.append([
                            doc_item.get('nombre', 'N/A')[:40],  # Limitar longitud
                            doc_item.get('tipo', 'N/A'),
                            self._formatear_fecha_str(doc_item.get('fecha'))
                        ])
                    
                    tabla_docs = Table(doc_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
                    tabla_docs.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), self.COLOR_ROJO),
                        ('TEXTCOLOR', (0, 0), (-1, 0), self.COLOR_BLANCO),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.98, 0.98, 0.98)])
                    ]))
                    
                    elementos.append(tabla_docs)
                else:
                    elementos.append(Paragraph('No hay documentos asociados.', self.styles['Normal']))
                
                elementos.append(Spacer(1, 20))
            
            # ═══ CONCLUSIONES ═══
            
            elementos.append(Paragraph('5. CONCLUSIONES Y RECOMENDACIONES', self.styles['SeccionTesla']))
            elementos.append(Spacer(1, 12))
            
            conclusiones = Paragraph(
                'El proyecto se encuentra en desarrollo según lo planificado. '
                'Se recomienda mantener el seguimiento de los hitos establecidos '
                'y asegurar la comunicación constante con el cliente.',
                self.styles['Normal']
            )
            elementos.append(conclusiones)
            
            elementos.append(Spacer(1, 40))
            
            # ═══ FIRMA ═══
            
            elementos.append(Paragraph('_' * 60, self.styles['NormalCentrado']))
            elementos.append(Paragraph('<b>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</b>', self.styles['NormalCentrado']))
            elementos.append(Paragraph('RUC: 20601138787', self.styles['Pequeno']))
            
            # Construir PDF
            doc.build(elementos)
            
            logger.info(f"✅ PDF informe proyecto generado: {ruta_salida}")
            
            return ruta_salida
            
        except Exception as e:
            logger.error(f"Error al generar PDF informe: {str(e)}")
            raise Exception(f"Error al generar PDF informe: {str(e)}")
    
    # ════════════════════════════════════════════════════════
    # FUNCIONES AUXILIARES
    # ════════════════════════════════════════════════════════
    
    def _decodificar_logo(self, logo_base64: str) -> Optional[Image]:
        """Decodificar logo desde base64 y crear objeto Image"""
        try:
            # Decodificar base64
            if ',' in logo_base64:
                logo_base64 = logo_base64.split(',')[1]
            
            imagen_bytes = base64.b64decode(logo_base64)
            imagen_io = BytesIO(imagen_bytes)
            
            # Crear imagen
            img = Image(imagen_io, width=2*inch, height=1*inch)
            img.hAlign = 'CENTER'
            
            return img
            
        except Exception as e:
            logger.warning(f"No se pudo decodificar logo: {str(e)}")
            return None
    
    def _crear_tabla_items(self, items: List[Dict], opciones: Dict[str, bool]) -> Table:
        """Crear tabla de items para cotización"""
        
        # Encabezados
        if opciones.get('mostrar_precios', True):
            data = [['Descripción', 'Cant.', 'P. Unit.', 'Total']]
            col_widths = [3*inch, 1*inch, 1.25*inch, 1.25*inch]
        else:
            data = [['Descripción', 'Cantidad']]
            col_widths = [4.5*inch, 1.5*inch]
        
        # Items
        for item in items:
            cantidad = float(item.get('cantidad', 0))
            
            if opciones.get('mostrar_precios', True):
                precio = float(item.get('precio_unitario', 0))
                total = cantidad * precio
                
                data.append([
                    item.get('descripcion', ''),
                    f"{cantidad:.2f}",
                    f"S/ {precio:,.2f}",
                    f"S/ {total:,.2f}"
                ])
            else:
                data.append([
                    item.get('descripcion', ''),
                    f"{cantidad:.2f}"
                ])
        
        # Crear tabla
        tabla = Table(data, colWidths=col_widths)
        
        # Estilo
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLOR_ROJO),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.COLOR_BLANCO),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.98, 0.98, 0.98)])
        ]))
        
        return tabla
    
    def _crear_tabla_totales(self, datos: Dict) -> Table:
        """Crear tabla de totales"""
        
        subtotal = float(datos.get('subtotal', 0))
        igv = float(datos.get('igv', 0))
        total = float(datos.get('total', 0))
        
        data = [
            ['Subtotal:', f"S/ {subtotal:,.2f}"],
            ['IGV (18%):', f"S/ {igv:,.2f}"],
            ['TOTAL:', f"S/ {total:,.2f}"]
        ]
        
        tabla = Table(data, colWidths=[4*inch, 2*inch])
        
        tabla.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (0, 2), (1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (1, 2), 12),
            ('TEXTCOLOR', (0, 2), (1, 2), self.COLOR_ROJO),
            ('LINEABOVE', (0, 2), (-1, 2), 2, self.COLOR_ROJO),
        ]))
        
        return tabla
    
    def _formatear_fecha(self, fecha) -> str:
        """Formatear fecha a string"""
        if not fecha:
            return 'N/A'
        
        if isinstance(fecha, str):
            return fecha
        
        try:
            return fecha.strftime('%d/%m/%Y')
        except:
            return str(fecha)
    
    def _formatear_fecha_str(self, fecha_str: str) -> str:
        """Formatear fecha desde string"""
        if not fecha_str or fecha_str == 'N/A':
            return 'N/A'
        return fecha_str
    
    def generar_informe_simple(
        self,
        datos: Dict[str, Any],
        ruta_salida: str
    ) -> str:
        """
        Generar informe simple (versión básica)
        
        Args:
            datos: Datos del informe
            ruta_salida: Ruta donde guardar
        
        Returns:
            Ruta del archivo generado
        """
        
        try:
            logger.info("Generando informe simple")
            
            # Crear directorio
            Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
            
            # Crear documento
            doc = SimpleDocTemplate(ruta_salida, pagesize=letter)
            
            elementos = []
            
            # Título
            elementos.append(Paragraph('INFORME SIMPLE', self.styles['TituloTesla']))
            elementos.append(Spacer(1, 20))
            
            # Contenido
            for clave, valor in datos.items():
                elementos.append(Paragraph(f"<b>{clave}:</b> {valor}", self.styles['Normal']))
            
            # Construir
            doc.build(elementos)
            
            logger.info(f"✅ Informe simple generado: {ruta_salida}")
            
            return ruta_salida
            
        except Exception as e:
            logger.error(f"Error al generar informe simple: {str(e)}")
            raise Exception(f"Error: {str(e)}")

# ════════════════════════════════════════════════════════
# INSTANCIA GLOBAL
# ════════════════════════════════════════════════════════

pdf_generator = PDFGenerator()