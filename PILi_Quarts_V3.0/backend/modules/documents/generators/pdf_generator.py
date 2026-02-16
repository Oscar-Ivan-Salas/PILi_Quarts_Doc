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
        Initialize PDF generator with Tesla Visual Identity.
        
        Args:
            page_size: Page size (letter, A4, etc.)
        """
        self.page_size = page_size
        
        # Tesla Visual Identity Colors
        self.COLOR_PRIMARY = colors.HexColor('#0052A3')
        self.COLOR_SECONDARY = colors.HexColor('#1E40AF')
        self.COLOR_ACCENT = colors.HexColor('#3B82F6')
        self.COLOR_BG_LIGHT = colors.HexColor('#EFF6FF')
        self.COLOR_TEXT_GRAY = colors.HexColor('#374151')
        self.COLOR_BORDER = colors.HexColor('#DBEAFE')
        
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        logger.info(f"PDF Generator initialized with page size: {page_size}")
    
    def _setup_custom_styles(self):
        """Define custom paragraph styles matching HTML templates"""
        
        # Custom Title (Centered, Blue)
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.COLOR_PRIMARY,
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        # Custom Subtitle (Centered, Secondary Blue)
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=self.COLOR_SECONDARY,
            spaceAfter=10,
            alignment=TA_CENTER
        ))
        
        # Section Header (Block with Background)
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.white,
            backColor=self.COLOR_PRIMARY,
            borderPadding=(10, 5),
            spaceAfter=10,
            spaceBefore=15
        ))
        
        # Card Label (Small, Gray, Bold)
        self.styles.add(ParagraphStyle(
            name='CardLabel',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=self.COLOR_TEXT_GRAY,
            fontName='Helvetica-Bold'
        ))
        
        # Card Value (Primary Color, Bold)
        self.styles.add(ParagraphStyle(
            name='CardValue',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.COLOR_PRIMARY,
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
        Build PDF header (Tesla Visual Identity).
        structure: Left (Logo Box), Right (Info).
        """
        elements = []
        
        # Left Content: Logo + Slogan
        logo_text = Paragraph("TESLA", ParagraphStyle(
            'LogoTitle', parent=self.styles['Normal'],
            fontSize=24, textColor=colors.white, alignment=TA_CENTER, fontName='Helvetica-Bold'
        ))
        slogan_text = Paragraph("Electricidad y Automatización", ParagraphStyle(
            'LogoSlogan', parent=self.styles['Normal'],
            fontSize=9, textColor=colors.HexColor('#E5E7EB'), alignment=TA_CENTER, fontName='Helvetica-Oblique'
        ))
        
        # Determine if we have a logo image, if so use it, otherwise use text
        left_content = [logo_text, slogan_text]
        if 'logo_path' in data and data['logo_path']:
             try:
                logo = Image(data['logo_path'], width=1.5*inch, height=0.5*inch)
                left_content = [logo, slogan_text]
             except:
                pass

        # Right Content: Company Info
        info_text = """
        <b>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</b><br/>
        RUC: 20601138787<br/>
        Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL<br/>
        Teléfono: 906 315 961<br/>
        Email: ingenieria.teslaelectricidad@gmail.com
        """
        right_content = Paragraph(info_text, ParagraphStyle(
            'CompanyInfo', parent=self.styles['Normal'],
            fontSize=8, textColor=self.COLOR_PRIMARY, alignment=TA_RIGHT, leading=10
        ))
        
        # Main Header Table
        table_data = [[left_content, right_content]]
        table = Table(table_data, colWidths=[2.5*inch, 4.5*inch])
        
        table.setStyle(TableStyle([
            # Left Cell Styling (Blue Box)
            ('BACKGROUND', (0, 0), (0, 0), self.COLOR_PRIMARY),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (0, 0), 10),
            ('BOTTOMPADDING', (0, 0), (0, 0), 10),
            
            # Right Cell Styling
            ('VALIGN', (1, 0), (1, 0), 'MIDDLE'),
            ('LEFTPADDING', (1, 0), (1, 0), 20),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Document info (Below Header)
        # Title Matches Excel
        elements.append(Paragraph("COTIZACIÓN DE SERVICIOS", self.styles['CustomTitle']))
        
        # Subtitle
        sub_text = f"N° {data.get('numero', 'COT-001')}"
        elements.append(Paragraph(sub_text, self.styles['CustomSubtitle']))
        
        elements.append(Spacer(1, 0.2*inch))
        
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
        """Build document footer (Brand Footer)"""
        elements = []
        elements.append(Spacer(1, 0.3*inch))
        
        footer_style = ParagraphStyle(
            'FooterStyle', parent=self.styles['Normal'],
            fontSize=8, textColor=colors.HexColor('#6B7280'), alignment=TA_CENTER, leading=10
        )
        
        # Line 1: Company Name
        elements.append(Paragraph("<b>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</b>", 
                                ParagraphStyle('FooterBold', parent=footer_style, fontSize=10, textColor=self.COLOR_PRIMARY)))
        
        # Line 2-4
        info = """
        RUC: 20601138787 | Teléfono: 906 315 961<br/>
        Email: ingenieria.teslaelectricidad@gmail.com<br/>
        Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL
        """
        elements.append(Paragraph(info, footer_style))
        
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
        """Generate Simple Project PDF - High Fidelity"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
             buffer if not output_path else output_path,
             pagesize=self.page_size,
             rightMargin=1*inch, leftMargin=1*inch,
             topMargin=1*inch, bottomMargin=1*inch
        )
        story = []
        
        # 1. Header
        story.append(Paragraph("FICHA DE PROYECTO", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # 2. Details Table (Grid Layout)
        details = [
            ["Código:", data.get('codigo', 'PROY-000'), "Cliente:", data.get('cliente', {}).get('nombre', 'N/A')],
            ["Proyecto:", data.get('nombre', 'Proyecto Sin Nombre'), "Líder:", data.get('lider', 'Ing. Responsable')],
            ["Estado:", data.get('estado', 'En Ejecución'), "Duración:", data.get('duracion_total', '30 días')],
            ["Inicio:", data.get('fecha_inicio', '01/01/2026'), "Presupuesto:", f"${data.get('presupuesto', 0):,.2f}"]
        ]
        
        table = Table(details, colWidths=[1*inch, 2.5*inch, 1*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'), # Labels Col 1
            ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'), # Labels Col 3
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f3f4f6')),
            ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#f3f4f6')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # 3. Phases Table
        story.append(Paragraph("Cronograma de Fases", self.styles['SectionHeader']))
        
        headers = ["Fase", "Fechas", "Estado", "Responsable"]
        phases_data = [headers]
        fases = data.get('fases', [
            {"nombre": "Ingeniería", "rango": "Día 1-10", "estado": "Completado", "resp": "Ing. Diseño"},
            {"nombre": "Adquisiciones", "rango": "Día 11-20", "estado": "En Proceso", "resp": "Logística"},
            {"nombre": "Ejecución", "rango": "Día 21-50", "estado": "Pendiente", "resp": "Ing. Campo"},
            {"nombre": "Cierre", "rango": "Día 51-60", "estado": "Pendiente", "resp": "PM"}
        ])
        
        for f in fases:
            phases_data.append([
                f.get('nombre'),
                f.get('rango'),
                f.get('estado'),
                f.get('resp')
            ])
            
        t_phases = Table(phases_data, colWidths=[2*inch, 2*inch, 1.5*inch, 1.5*inch])
        t_phases.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9fafb')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        story.append(t_phases)
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    def generate_proyecto_complejo(self, data: Dict[str, Any], output_path: Optional[str] = None) -> BytesIO:
        """Generate Complex PMI Project PDF - High Fidelity"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
             buffer if not output_path else output_path,
             pagesize=self.page_size
        )
        story = []
        
        story.append(Paragraph("PROJECT CHARTER", self.styles['CustomTitle']))
        story.append(Paragraph(f"Estándar PMI - Código: {data.get('codigo', 'PMI-001')}", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # 1. Executive Summary Box
        story.append(Paragraph("Propósito y Alcance", self.styles['SectionHeader']))
        purpose_text = f"<b>Propósito:</b> {data.get('proposito', 'Definir objetivos...')}<br/><br/><b>Alcance:</b> {data.get('alcance', 'Alcance detallado...')}"
        story.append(Paragraph(purpose_text, self.styles['CustomBody']))
        story.append(Spacer(1, 0.2*inch))

        # 2. KPI Dashboard Table
        story.append(Paragraph("Tablero de Control (EVM)", self.styles['SectionHeader']))
        
        kpi_data = [
            ["KPI", "Valor Actual", "Meta", "Estado"],
            ["SPI (Cronograma)", str(data.get('spi', 1.0)), ">= 1.0", "🟢"],
            ["CPI (Costos)", str(data.get('cpi', 1.0)), ">= 1.0", "🟢"],
            ["EV (Valor Ganado)", f"${data.get('ev', 0):,.2f}", "-", "🔵"],
            ["AC (Costo Real)", f"${data.get('ac', 0):,.2f}", "< EV", "🔵"],
        ]
        
        kpi_table = Table(kpi_data, colWidths=[2*inch, 2*inch, 1*inch, 1*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (1,1), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 6),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 0.2*inch))
        
        # 3. Risk Matrix Table
        story.append(Paragraph("Matriz de Riesgos Principales", self.styles['SectionHeader']))
        
        risk_data = [["Riesgo", "Prob.", "Impacto", "Estrategia"]]
        riesgos = data.get('riesgos', [
            {"desc": "Retraso Suministros", "prob": "Alta", "imp": "Alto", "estr": "Mitigar"},
            {"desc": "Cambios Alcance", "prob": "Media", "imp": "Medio", "estr": "Aceptar"}
        ])
        
        for r in riesgos:
            risk_data.append([r.get('desc'), r.get('prob'), r.get('imp'), r.get('estr')])
            
        t_risk = Table(risk_data, colWidths=[3*inch, 1*inch, 1*inch, 1*inch])
        t_risk.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dc2626')), # Red header for risks
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('fontName', (0,0), (-1,0), 'Helvetica-Bold'),
        ]))
        story.append(t_risk)
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    def generate_informe_tecnico(self, data: Dict[str, Any], output_path: Optional[str] = None) -> BytesIO:
        """Generate Technical Report PDF - High Fidelity"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
             buffer if not output_path else output_path,
             pagesize=self.page_size,
             topMargin=1*inch, bottomMargin=1*inch
        )
        story = []
        
        # Title
        story.append(Paragraph(data.get('titulo', 'INFORME TÉCNICO').upper(), self.styles['CustomTitle']))
        story.append(Paragraph(f"Ref: {data.get('codigo', 'INF-TECNICO-001')}", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # 1. Technical Specs Table
        story.append(Paragraph("Especificaciones Técnicas", self.styles['SectionHeader']))
        
        specs = data.get('specs', [
            ["Normativa Aplicable", "CNE Suministro 2011"],
            ["Nivel de Tensión", "220V / 380V"],
            ["Frecuencia", "60 Hz"],
            ["Potencia Instalada", "100 kW"]
        ])
        
        t_specs = Table(specs, colWidths=[3*inch, 3*inch])
        t_specs.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#eff6ff')), # Light blue col 1
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_specs)
        story.append(Spacer(1, 0.2*inch))
        
        # 2. Results Table
        story.append(Paragraph("Resultados de Mediciones", self.styles['SectionHeader']))
        
        headers = ["Punto de Medida", "L1 (A)", "L2 (A)", "L3 (A)", "Estado"]
        results_data = [headers]
        mediciones = data.get('mediciones', [
            {"pto": "Tablero General", "l1": 105, "l2": 104, "l3": 106, "res": "OK"},
            {"pto": "Subestación", "l1": 200, "l2": 198, "l3": 201, "res": "OK"},
        ])
        
        for m in mediciones:
            results_data.append([m['pto'], str(m['l1']), str(m['l2']), str(m['l3']), m['res']])
            
        t_results = Table(results_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        t_results.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1f2937')), # Dark header
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (1,1), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        story.append(t_results)
        
        # 3. Dynamic Sections
        for section in data.get('secciones', []):
            story.append(Paragraph(section.get('titulo', ''), self.styles['SectionHeader']))
            story.append(Paragraph(section.get('contenido', ''), self.styles['CustomBody']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    def generate_informe_ejecutivo(self, data: Dict[str, Any], output_path: Optional[str] = None) -> BytesIO:
        """Generate Executive Report PDF - High Fidelity"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
             buffer if not output_path else output_path,
             pagesize=self.page_size
        )
        story = []
        
        story.append(Paragraph(data.get('titulo', 'INFORME EJECUTIVO').upper(), self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # 1. Financial Dashboard (Grid Layout)
        story.append(Paragraph("Tablero Financiero Estratégico", self.styles['SectionHeader']))
        
        # Row 1: ROI & TIR
        row1 = [
            f"ROI: {data.get('roi', 25)}%\nRetorno de Inversión", 
            f"TIR: {data.get('tir', 30)}%\nTasa Interna de Retorno"
        ]
        # Row 2: Payback & Savings
        row2 = [
            f"Payback: {data.get('payback', 18)} meses\nRecuperación", 
            f"Ahorro: ${data.get('ahorro_anual', 75000):,.2f}\nAnual Estimado"
        ]
        
        data_kpi = [row1, row2]
        
        t_kpi = Table(data_kpi, colWidths=[3*inch, 3*inch], rowHeights=[1*inch, 1*inch])
        t_kpi.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#3b82f6')),
            ('BACKGROUND', (0,0), (0,0), colors.HexColor('#eff6ff')),
            ('BACKGROUND', (1,1), (1,1), colors.HexColor('#f0fdf4')), # Green ish
            ('FONTSIZE', (0,0), (-1,-1), 14),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ]))
        story.append(t_kpi)
        story.append(Spacer(1, 0.3*inch))
        
        # 2. Investment Breakdown
        story.append(Paragraph("Desglose de Inversión", self.styles['SectionHeader']))
        
        headers = ["Categoría", "Monto", "Prioridad"]
        inv_data = [headers]
        breakdown = data.get('inversion_detalle', [
            {"cat": "Equipos Principales", "monto": 35000, "pri": "Alta"},
            {"cat": "Mano de Obra Calificada", "monto": 10000, "pri": "Alta"},
            {"cat": "Capital de Trabajo", "monto": 5000, "pri": "Media"}
        ])
        
        for item in breakdown:
            inv_data.append([item['cat'], f"${item['monto']:,.2f}", item['pri']])
            
        t_inv = Table(inv_data, colWidths=[4*inch, 1.5*inch, 1.5*inch])
        t_inv.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ]))
        story.append(t_inv)
        
        # 3. Executive Summary Text
        story.append(Paragraph("Resumen Estratégico", self.styles['SectionHeader']))
        story.append(Paragraph(data.get('resumen', 'El proyecto presenta viabilidad financiera sólida...'), self.styles['CustomBody']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
