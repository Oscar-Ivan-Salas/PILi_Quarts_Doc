# -*- coding: utf-8 -*-
"""
Clase Base para Generadores de Documentos
Contiene funcionalidad compartida por todos los generadores
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime
from pathlib import Path
from PIL import Image as PILImage
import logging


class BaseDocumentGenerator:
    """Clase base con funcionalidad compartida para todos los generadores"""
    
    # Colores Tesla Azul (por defecto)
    COLOR_PRIMARIO = RGBColor(0, 82, 163)      # #0052A3
    COLOR_SECUNDARIO = RGBColor(30, 64, 175)   # #1E40AF
    COLOR_ACENTO = RGBColor(59, 130, 246)      # #3B82F6
    COLOR_CLARO = RGBColor(239, 246, 255)      # #EFF6FF
    
    def __init__(self, datos, opciones=None):
        """
        Inicializa el generador
        
        Args:
            datos: Diccionario con datos del documento
            opciones: Opciones de personalización (colores, fuente, etc.)
        """
        self.datos = datos
        self.opciones = opciones or {}
        
        # 📂 SMART MASTER LOADING: Cargar plantilla si existe
        template_dir = Path(__file__).parent.parent / "templates" / "word_masters"
        mode = self.opciones.get('mode', 'cotizacion_simple')
        template_path = template_dir / f"master_{mode}.docx"
        
        import logging
        logger = logging.getLogger(__name__)

        if template_path.exists():
            logger.info(f"📑 Cargando Plantilla Maestra: {template_path}")
            self.doc = Document(str(template_path))
            self.using_master = True
        else:
            logger.warning(f"⚠️ Plantilla Maestra no encontrada en {template_path}. Usando documento en blanco.")
            self.doc = Document()
            self.using_master = False
            
        # Aplicar esquema de colores personalizado
        self._aplicar_colores()
        
        # Configurar márgenes (solo si no hay master, para no romper el diseño del maestro)
        if not self.using_master:
            self._configurar_margenes()
    
    def _hex_to_rgb(self, hex_color):
        """Convierte string hexadecimal (#RRGGBB) a tupla (R, G, B)"""
        if not hex_color:
            return None
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return None

    def _rgb_to_hex(self, rgb_color):
        """Convierte RGBColor a string hexadecimal"""
        if hasattr(rgb_color, '_color'):
            color_int = rgb_color._color
            r = (color_int >> 16) & 0xFF
            g = (color_int >> 8) & 0xFF
            b = color_int & 0xFF
        else:
            r, g, b = getattr(self, 'color_primario_rgb', (0, 0, 0))
        return '{:02X}{:02X}{:02X}'.format(r, g, b)
    
    def _aplicar_colores(self):
        """Aplica esquema de colores y fuentes según opciones"""
        import logging
        logger = logging.getLogger(__name__)
        
        # Prioridad 1: ADN Visual dinámico (del Studio)
        color_primario_hex = self.opciones.get('primaryColor') or self.opciones.get('color_primario_hex')
        color_secundario_hex = self.opciones.get('secondaryColor')
        font_family = self.opciones.get('fontFamily', 'Calibri')
        font_size = self.opciones.get('fontSize', 11)
        
        # Guardar fuente para uso en todo el documento
        self.font_family = font_family
        self.font_size = font_size
        
        if color_primario_hex:
            logger.info(f"🎨 Aplicando ADN Visual Dinámico: {color_primario_hex} | Fuente: {font_family} {font_size}pt")
            rgb_primario = self._hex_to_rgb(color_primario_hex)
            if rgb_primario:
                self.color_primario_rgb = rgb_primario
                # Derivar secundario si no viene
                self.color_secundario_rgb = self._hex_to_rgb(color_secundario_hex) if color_secundario_hex else (
                    max(0, rgb_primario[0] - 30),
                    max(0, rgb_primario[1] - 30),
                    max(0, rgb_primario[2] - 30)
                )
                self.color_acento_rgb = (
                    min(255, rgb_primario[0] + 50),
                    min(255, rgb_primario[1] + 50),
                    min(255, rgb_primario[2] + 50)
                )
                
                self.COLOR_PRIMARIO = RGBColor(*self.color_primario_rgb)
                self.COLOR_SECUNDARIO = RGBColor(*self.color_secundario_rgb)
                self.COLOR_ACENTO = RGBColor(*self.color_acento_rgb)
                return

        # Prioridad 2: Esquemas estáticos
        esquema = self.opciones.get('esquema_colores', 'azul-tesla')
        logger.info(f"🎨 Aplicando Esquema Estático: {esquema} | Fuente: {font_family} {font_size}pt")
        
        esquemas = {
            'azul-tesla': {
                'primario': (0, 82, 163),
                'secundario': (30, 64, 175),
                'acento': (59, 130, 246),
            },
            'rojo-energia': {
                'primario': (139, 0, 0),
                'secundario': (153, 27, 27),
                'acento': (220, 38, 38),
            },
            'verde-ecologico': {
                'primario': (6, 95, 70),
                'secundario': (4, 120, 87),
                'acento': (16, 185, 129),
            },
            'dorado': {
                'primario': (212, 175, 55),
                'secundario': (184, 134, 11),
                'acento': (255, 215, 0),
            },
            'personalizado': {
                'primario': (139, 92, 246),  # Morado #8B5CF6
                'secundario': (124, 58, 237),  # Morado oscuro #7C3AED
                'acento': (167, 139, 250),  # Morado claro #A78BFA
            },
        }
        
        colores = esquemas.get(esquema, esquemas['azul-tesla'])
        
        # Guardar como tuplas RGB
        self.color_primario_rgb = colores['primario']
        self.color_secundario_rgb = colores['secundario']
        self.color_acento_rgb = colores['acento']
        
        # Crear objetos RGBColor
        self.COLOR_PRIMARIO = RGBColor(*colores['primario'])
        self.COLOR_SECUNDARIO = RGBColor(*colores['secundario'])
        self.COLOR_ACENTO = RGBColor(*colores['acento'])
    
    def _configurar_margenes(self):
        """Configura márgenes del documento"""
        sections = self.doc.sections
        for section in sections:
            section.top_margin = Inches(0.8)
            section.bottom_margin = Inches(0.8)
            section.left_margin = Inches(0.8)
            section.right_margin = Inches(0.8)

    def _obtener_simbolo_moneda(self):
        """Retorna el símbolo de moneda basado en config o datos"""
        moneda = self.datos.get('settings', {}).get('currency', 'PEN')
        simbolos = {
            'PEN': 'S/',
            'USD': '$',
            'EUR': '€'
        }
        return simbolos.get(moneda, 'S/')
    
    def _agregar_header_basico(self):
        """Agrega header profesional con Smart Scale (PIL) y Ghost Headers"""
        if getattr(self, 'using_master', False):
            return

        section = self.doc.sections[0]
        header = section.header
        
        if len(header.paragraphs) > 0:
            p_first = header.paragraphs[0]
            p_first.text = ""
            p_first.paragraph_format.space_after = Pt(0)

        # Agregar tabla al header (GHOST TABLE - Sin bordes)
        table = header.add_table(rows=1, cols=2, width=Inches(7.2))
        table.autofit = False
        
        # Eliminar bordes de la tabla (Inspirado en Prototipo Raíz)
        # Esto evita que aparezcan líneas negras en Word/PDF
        tbl = table._element
        tblPr = tbl.xpath('w:tblPr')[0]
        tblBorders = OxmlElement('w:tblBorders')
        for tag in ['w:top', 'w:left', 'w:bottom', 'w:right', 'w:insideH', 'w:insideV']:
            edge = OxmlElement(tag)
            edge.set(qn('w:val'), 'none')
            tblBorders.append(edge)
        tblPr.append(tblBorders)

        # Columna izquierda: Logo con Smart Scale
        cell_logo = table.rows[0].cells[0]
        cell_logo.width = Inches(3.2)
        p_logo = cell_logo.paragraphs[0]
        p_logo.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        logo_path = self.opciones.get('logo_path') or self.datos.get('branding', {}).get('logo_path')
        
        if logo_path and Path(logo_path).exists():
            try:
                # [SMART SCALE] Detectar dimensiones reales para evitar deformación
                with PILImage.open(logo_path) as img:
                    w, h = img.size
                    aspect = w / h
                    
                    # Máximo deseado: ancho 2.0" o alto 0.6"
                    target_h = 0.6
                    target_w = target_h * aspect
                    
                    if target_w > 2.5: # Si es muy ancho, limitar por ancho
                        target_w = 2.5
                        target_h = target_w / aspect
                
                run_logo = p_logo.add_run()
                run_logo.add_picture(str(logo_path), height=Inches(target_h), width=Inches(target_w))
            except Exception as e:
                logger.error(f"Error Smart Scale: {e}")
                run_logo = p_logo.add_run('TESLA')
                run_logo.font.size = Pt(24)
                run_logo.font.bold = True
                run_logo.font.color.rgb = self.COLOR_PRIMARIO
        else:
            run_logo = p_logo.add_run('TESLA')
            run_logo.font.size = Pt(24)
            run_logo.font.bold = True
            run_logo.font.color.rgb = self.COLOR_PRIMARIO
        
        # Columna derecha: ADN Winner Info
        cell_info = table.rows[0].cells[1]
        cell_info.width = Inches(4.0)
        
        p_empresa = cell_info.paragraphs[0]
        p_empresa.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run_empresa = p_empresa.add_run('TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.')
        run_empresa.font.size = Pt(11)
        run_empresa.font.bold = True
        run_empresa.font.color.rgb = self.COLOR_PRIMARIO
        
        info_lines = [
            f"RUC: {self.empresa_info.get('ruc', '20601138787')}",
            self.empresa_info.get('email', 'ingenieria.teslaelectricidad@gmail.com')
        ]
        
        for linea in info_lines:
            p = cell_info.add_paragraph(linea)
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p.runs[0].font.size = Pt(8)
            p.runs[0].font.color.rgb = self.COLOR_PRIMARIO # Inyectar ADN en líneas info
            p.paragraph_format.space_after = Pt(0)

        # Tratar de eliminar el espacio extra que deja Word bajo la tabla
        # (A veces queda un párrafo vacío después de la tabla)


    
    def _agregar_footer_basico(self):
        """Agrega pie de página básico"""
        # 📂 SI USAMOS MASTER, NO SOBREESCRIBIR EL FOOTER DEL MAESTRO
        if getattr(self, 'using_master', False):
            return

        self.doc.add_paragraph()
        
        p_footer = self.doc.add_paragraph()
        p_footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p_footer.add_run('TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.')
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = self.COLOR_PRIMARIO
        
        contacto = [
            'RUC: 20601138787 | Teléfono: 906 315 961',
            'Email: ingenieria.teslaelectricidad@gmail.com',
            'Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL'
        ]
        
        for linea in contacto:
            p = self.doc.add_paragraph(linea)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.size = Pt(8)
            p.runs[0].font.color.rgb = RGBColor(107, 114, 128)
    
    def _set_cell_border(self, cell, **kwargs):
        """
        Set cell border
        Usage: _set_cell_border(cell, top={"sz": 12, "val": "single", "color": "#FF0000"})
        """
        tc = cell._element
        tcPr = tc.get_or_add_tcPr()

        # check for tag existence, if none create it
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            edge_data = kwargs.get(edge)
            if edge_data:
                tag = 'w:{}'.format(edge)
                element = tcPr.find(qn(tag))
                if element is None:
                    element = OxmlElement(tag)
                    tcPr.append(element)

                # assign attributes
                for key in ["sz", "val", "color", "space", "shadow"]:
                    if key in edge_data:
                        element.set(qn('w:{}'.format(key)), str(edge_data[key]))

    def generar(self, ruta_salida):
        """
        Método abstracto - debe ser implementado por clases hijas
        """
        raise NotImplementedError("Subclases deben implementar generar()")
