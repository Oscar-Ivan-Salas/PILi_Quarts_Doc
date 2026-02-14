"""
Document Generator Module - PDF Generator
Enterprise-grade PDF generation using ReportLab
Following clean-code and python-patterns skills
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from typing import Dict, List, Any, Optional
from datetime import datetime
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


class PDFGenerator:
    """
    Professional PDF generator using ReportLab.
    
    Features:
    - Custom headers/footers
    - Tables with styling
    - Images
    - Multi-page support
    - Professional formatting
    
    Following clean-code: Single Responsibility
    """
    
    def __init__(self, page_size=letter):
        """
        Initialize PDF generator.
        
        Args:
            page_size: Page size (letter, A4, etc.)
        """
        self.page_size = page_size
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        logger.info(f"PDF Generator initialized with page size: {page_size}")
    
    def _setup_custom_styles(self):
        """
        Setup custom paragraph styles.
        
        Following clean-code: Separation of concerns
        """
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=10,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#374151'),
            spaceAfter=6,
            leading=14
        ))
        
        # Footer text
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            alignment=TA_CENTER
        ))
    
    def generate_cotizacion(
        self,
        data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate professional quotation PDF.
        
        Following python-patterns: Type hints for clarity
        
        Args:
            data: Quotation data (cliente, items, totales, etc.)
            output_path: Optional file path to save PDF
        
        Returns:
            BytesIO buffer with PDF content
        """
        logger.info("Generating quotation PDF")
        
        # Create buffer
        buffer = BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            buffer if not output_path else output_path,
            pagesize=self.page_size,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )
        
        # Build content
        story = []
        
        # Header
        story.extend(self._build_header(data))
        
        # Client info
        story.extend(self._build_client_info(data.get('cliente', {})))
        
        # Items table
        story.extend(self._build_items_table(data.get('items', [])))
        
        # Totals
        story.extend(self._build_totals(data.get('totales', {})))
        
        # Terms and conditions
        if 'terminos' in data:
            story.extend(self._build_terms(data['terminos']))
        
        # Footer
        story.extend(self._build_footer(data))
        
        # Build PDF
        doc.build(story)
        
        # Reset buffer position
        buffer.seek(0)
        
        logger.info("Quotation PDF generated successfully")
        return buffer
    
    def _build_header(self, data: Dict) -> List:
        """
        Build PDF header.
        
        Following clean-code: Small functions
        """
        elements = []
        
        # Company logo (if provided)
        if 'logo_path' in data:
            try:
                logo = Image(data['logo_path'], width=2*inch, height=1*inch)
                elements.append(logo)
                elements.append(Spacer(1, 0.2*inch))
            except Exception as e:
                logger.warning(f"Could not load logo: {e}")
        
        # Title
        title = Paragraph("COTIZACIÓN", self.styles['CustomTitle'])
        elements.append(title)
        
        # Document info
        doc_info = f"""
        <b>No. Cotización:</b> {data.get('numero', 'N/A')}<br/>
        <b>Fecha:</b> {data.get('fecha', datetime.now().strftime('%d/%m/%Y'))}<br/>
        <b>Válida hasta:</b> {data.get('valida_hasta', 'N/A')}
        """
        elements.append(Paragraph(doc_info, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _build_client_info(self, cliente: Dict) -> List:
        """Build client information section"""
        elements = []
        
        elements.append(Paragraph("DATOS DEL CLIENTE", self.styles['SectionHeader']))
        
        client_data = [
            ['Nombre:', cliente.get('nombre', 'N/A')],
            ['Empresa:', cliente.get('empresa', 'N/A')],
            ['Email:', cliente.get('email', 'N/A')],
            ['Teléfono:', cliente.get('telefono', 'N/A')],
            ['Dirección:', cliente.get('direccion', 'N/A')],
        ]
        
        table = Table(client_data, colWidths=[1.5*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1f2937')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#374151')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _build_items_table(self, items: List[Dict]) -> List:
        """
        Build items table with professional styling.
        
        Following clean-code: Clear data transformation
        """
        elements = []
        
        elements.append(Paragraph("DETALLE DE SERVICIOS", self.styles['SectionHeader']))
        
        # Table headers
        table_data = [
            ['#', 'Descripción', 'Cantidad', 'Precio Unit.', 'Subtotal']
        ]
        
        # Add items
        for idx, item in enumerate(items, 1):
            table_data.append([
                str(idx),
                item.get('descripcion', ''),
                str(item.get('cantidad', 0)),
                f"${item.get('precio_unitario', 0):,.2f}",
                f"${item.get('subtotal', 0):,.2f}"
            ])
        
        # Create table
        table = Table(
            table_data,
            colWidths=[0.5*inch, 3*inch, 1*inch, 1.25*inch, 1.25*inch]
        )
        
        # Style table
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Body styling
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Index column
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Numbers right-aligned
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _build_totals(self, totales: Dict) -> List:
        """Build totals section"""
        elements = []
        
        totals_data = [
            ['Subtotal:', f"${totales.get('subtotal', 0):,.2f}"],
            ['IVA (16%):', f"${totales.get('iva', 0):,.2f}"],
            ['', ''],  # Separator
            ['TOTAL:', f"${totales.get('total', 0):,.2f}"],
        ]
        
        table = Table(totals_data, colWidths=[4.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, 2), 'Helvetica-Bold'),
            ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 2), 11),
            ('FONTSIZE', (0, 3), (-1, 3), 14),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('TEXTCOLOR', (0, 3), (-1, 3), colors.HexColor('#1e40af')),
            ('LINEABOVE', (0, 3), (-1, 3), 2, colors.HexColor('#1e40af')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _build_terms(self, terminos: str) -> List:
        """Build terms and conditions section"""
        elements = []
        
        elements.append(Paragraph("TÉRMINOS Y CONDICIONES", self.styles['SectionHeader']))
        elements.append(Paragraph(terminos, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _build_footer(self, data: Dict) -> List:
        """Build document footer"""
        elements = []
        
        footer_text = f"""
        Generado por PILi Quarts - {datetime.now().strftime('%d/%m/%Y %H:%M')}<br/>
        {data.get('empresa_nombre', 'PILi Engineering')} | {data.get('empresa_contacto', 'contacto@pili.com')}
        """
        
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(footer_text, self.styles['Footer']))
        
        return elements
    
        return buffer

    def generate_informe(
        self,
        data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate technical report PDF.
        """
        logger.info("Generating generic report PDF")
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer if not output_path else output_path,
            pagesize=self.page_size,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Title
        story.append(Paragraph(data.get('titulo', 'INFORME'), self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Sections
        for section in data.get('secciones', []):
            story.append(Paragraph(section.get('titulo', ''), self.styles['SectionHeader']))
            story.append(Paragraph(section.get('contenido', ''), self.styles['CustomBody']))
            story.append(Spacer(1, 0.2*inch))
        
        # Build
        doc.build(story)
        buffer.seek(0)
        
        logger.info("Generic report PDF generated successfully")
        return buffer

    def generate_proyecto_simple(self, data: Dict[str, Any], output_path: Optional[str] = None) -> BytesIO:
        """Generate Simple Project PDF description"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
             buffer if not output_path else output_path,
             pagesize=self.page_size,
             rightMargin=1*inch, leftMargin=1*inch,
             topMargin=1*inch, bottomMargin=1*inch
        )
        story = []
        
        # Header
        story.append(Paragraph("FICHA DE PROYECTO", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # Details Table
        details = [
            ["Código:", data.get('codigo', 'N/A')],
            ["Proyecto:", data.get('nombre', 'N/A')],
            ["Cliente:", data.get('cliente', {}).get('nombre', 'N/A')],
            ["Estado:", data.get('estado', 'En Ejecución')],
            ["Duración:", data.get('duracion_total', 'N/A')]
        ]
        
        table = Table(details, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f3f4f6')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(table)
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    def generate_proyecto_complejo(self, data: Dict[str, Any], output_path: Optional[str] = None) -> BytesIO:
        """Generate Complex PMI Project PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
             buffer if not output_path else output_path,
             pagesize=self.page_size
        )
        story = []
        
        story.append(Paragraph("PROJECT CHARTER", self.styles['CustomTitle']))
        story.append(Paragraph("Estándar PMI - Gestión Profesional", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # KPIs
        story.append(Paragraph("KPIs Principales", self.styles['SectionHeader']))
        
        kpi_data = [
            ["KPI", "Valor", "Estado"],
            ["SPI (Cronograma)", str(data.get('spi', 1.0)), "🟢"],
            ["CPI (Costos)", str(data.get('cpi', 1.0)), "🟢"],
            ["EV (Valor Ganado)", f"${data.get('ev', 0):,.2f}", "-"],
        ]
        
        kpi_table = Table(kpi_data, colWidths=[2.5*inch, 2*inch, 1*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(kpi_table)
        
        # Scope
        story.append(Paragraph("Alcance del Proyecto", self.styles['SectionHeader']))
        story.append(Paragraph(data.get('alcance', 'Descripción del alcance...'), self.styles['CustomBody']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    def generate_informe_tecnico(self, data: Dict[str, Any], output_path: Optional[str] = None) -> BytesIO:
        """Alias for generic generate_informe but with specific title handling if needed"""
        if 'titulo' not in data:
            data['titulo'] = "INFORME TÉCNICO"
        return self.generate_informe(data, output_path)

    def generate_informe_ejecutivo(self, data: Dict[str, Any], output_path: Optional[str] = None) -> BytesIO:
        """Generate Executive Report PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
             buffer if not output_path else output_path,
             pagesize=self.page_size
        )
        story = []
        
        story.append(Paragraph(data.get('titulo', 'INFORME EJECUTIVO'), self.styles['CustomTitle']))
        
        # Financial Dashboard
        story.append(Paragraph("Tablero Financiero", self.styles['SectionHeader']))
        
        metrics = [
            ["ROI", f"{data.get('roi', 0)}%"],
            ["Payback", f"{data.get('payback', 0)} m"],
            ["TIR", f"{data.get('tir', 0)}%"],
            ["Ahorro", f"${data.get('ahorro_anual', 0):,.2f}"]
        ]
        
        # Checkered Layout for Metrics
        t = Table(metrics, colWidths=[2*inch, 2*inch])
        t.setStyle(TableStyle([
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('TEXTCOLOR', (1,0), (1,-1), colors.HexColor('#15803d')), # Green for money
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#3b82f6')),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor('#bfdbfe')),
            ('PADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(t)
        
        story.append(Paragraph("Resumen Ejecutivo", self.styles['SectionHeader']))
        story.append(Paragraph(data.get('resumen', ''), self.styles['CustomBody']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
