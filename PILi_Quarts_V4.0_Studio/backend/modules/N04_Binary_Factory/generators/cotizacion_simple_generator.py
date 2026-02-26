# -*- coding: utf-8 -*-
"""
Generador Profesional de Cotizaciones Simples
Basado en PLANTILLA_HTML_COTIZACION_SIMPLE.html

Genera documentos Word con diseño profesional que coincide EXACTAMENTE
con la vista previa HTML.
"""

try:
    from .base_generator import BaseDocumentGenerator
except (ImportError, ValueError):
    from base_generator import BaseDocumentGenerator

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime


class CotizacionSimpleGenerator(BaseDocumentGenerator):
    """Generador de cotizaciones simples con diseño profesional"""
    
    def _agregar_header(self):
        """Agrega header profesional usando el método de la base"""
        return self._agregar_header_basico()
    
    def _agregar_titulo(self):
        """Agrega título del documento"""
        # Título principal
        p_titulo = self.doc.add_paragraph()
        p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_titulo = p_titulo.add_run('COTIZACIÓN DE SERVICIOS')
        run_titulo.font.size = Pt(28)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        # Número de cotización
        numero = self.datos.get('numero', f"COT-{datetime.now().strftime('%Y%m%d%H%M')}")
        p_numero = self.doc.add_paragraph()
        p_numero.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_numero = p_numero.add_run(f'N° {numero}')
        run_numero.font.size = Pt(16)
        run_numero.font.bold = True
        run_numero.font.color.rgb = self.COLOR_SECUNDARIO
        
        self.doc.add_paragraph()
    
    def _agregar_info_general(self):
        """Agrega sección de información general"""
        # Tabla 2x2 para información
        table = self.doc.add_table(rows=1, cols=2)
        table.style = 'Table Grid' # Usar un estilo neutral
        
        # Celda 1: Datos del Cliente
        cell1 = table.rows[0].cells[0]
        p1 = cell1.paragraphs[0]
        run1 = p1.add_run('DATOS DEL CLIENTE')
        run1.font.size = Pt(11)
        run1.font.bold = True
        run1.font.color.rgb = self.COLOR_PRIMARIO
        
        # Celda 2: Datos de Emisión
        cell2 = table.rows[0].cells[1]
        
        # Aplicar borde a la celda
        color_hex = self._rgb_to_hex(self.COLOR_PRIMARIO)
        border_spec = {"sz": 12, "val": "single", "color": color_hex}
        self._set_cell_border(cell1, top=border_spec, bottom=border_spec, left=border_spec, right=border_spec)
        self._set_cell_border(cell2, top=border_spec, bottom=border_spec, left=border_spec, right=border_spec)
        
        # Extraer datos del cliente (puede ser dict o string)
        cliente_data = self.datos.get('cliente', 'Cliente')
        if isinstance(cliente_data, dict):
            cliente = cliente_data.get('nombre', 'Cliente')
        else:
            cliente = str(cliente_data)
        
        proyecto = self.datos.get('proyecto', 'Proyecto')
        area = self.datos.get('area_m2', '0')
        
        cell1.add_paragraph(f'Cliente: {cliente}').runs[0].font.size = Pt(10)
        cell1.add_paragraph(f'Proyecto: {proyecto}').runs[0].font.size = Pt(10)
        cell1.add_paragraph(f'Área: {area} m²').runs[0].font.size = Pt(10)
        
        # Celda 2: Datos de la Cotización
        cell2 = table.rows[0].cells[1]
        p2 = cell2.paragraphs[0]
        run2 = p2.add_run('DATOS DE LA COTIZACIÓN')
        run2.font.size = Pt(11)
        run2.font.bold = True
        run2.font.color.rgb = self.COLOR_PRIMARIO
        
        fecha = self.datos.get('fecha', datetime.now().strftime('%d/%m/%Y'))
        vigencia = self.datos.get('vigencia', '30 días')
        servicio = self.datos.get('servicio', 'Instalaciones Eléctricas')
        
        cell2.add_paragraph(f'Fecha: {fecha}').runs[0].font.size = Pt(10)
        cell2.add_paragraph(f'Vigencia: {vigencia}').runs[0].font.size = Pt(10)
        cell2.add_paragraph(f'Servicio: {servicio}').runs[0].font.size = Pt(10)
        
        self.doc.add_paragraph()
    
    def _agregar_tabla_items(self):
        """Agrega tabla de items con diseño profesional"""
        # Título de sección
        p_titulo = self.doc.add_paragraph('Detalle de la Cotización')
        p_titulo.runs[0].font.size = Pt(14)
        p_titulo.runs[0].font.bold = True
        p_titulo.runs[0].font.color.rgb = self.COLOR_PRIMARIO
        
        # Tabla de items
        items = self.datos.get('items', [])
        if not items:
            self.doc.add_paragraph('No hay items en esta cotización')
            return
        
        # Crear tabla
        table = self.doc.add_table(rows=1 + len(items), cols=6)
        table.style = 'Table Grid' # Usar un estilo neutral
        
        # Header
        headers = ['ITEM', 'DESCRIPCIÓN', 'CANT.', 'UNIDAD', 'P. UNIT.', 'TOTAL']
        for i, header in enumerate(headers):
            cell = table.rows[0].cells[i]
            cell.text = header
            # Estilo del header
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(255, 255, 255)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Fondo con color personalizado
            shading_elm = OxmlElement('w:shd')
            color_hex = self._rgb_to_hex(self.COLOR_PRIMARIO)
            shading_elm.set(qn('w:fill'), color_hex)
            cell._element.get_or_add_tcPr().append(shading_elm)
            
            # Bordes del color primario
            border_spec = {"sz": 4, "val": "single", "color": color_hex}
            self._set_cell_border(cell, top=border_spec, bottom=border_spec, left=border_spec, right=border_spec)
        
        # Datos
        for idx, item in enumerate(items, 1):
            row = table.rows[idx]
            
            # Item number
            row.cells[0].text = str(idx).zfill(2)
            row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Descripción
            row.cells[1].text = item.get('descripcion', '')
            
            # Cantidad
            cantidad = item.get('cantidad', 0)
            row.cells[2].text = f"{cantidad:.2f}"
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            
            # Unidad
            row.cells[3].text = item.get('unidad', 'und')
            row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Precio unitario
            precio = item.get('precio_unitario', 0) or item.get('precioUnitario', 0)
            simbolo = self._obtener_simbolo_moneda()
            row.cells[4].text = f"{simbolo} {precio:.2f}"
            row.cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            
            # Total
            total_item = cantidad * precio
            row.cells[5].text = f"{simbolo} {total_item:.2f}"
            row.cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[5].paragraphs[0].runs[0].font.bold = True
        
        self.doc.add_paragraph()
    
    def _agregar_totales(self):
        """Agrega sección de totales"""
        # Calcular totales
        items = self.datos.get('items', [])
        subtotal = sum((item.get('cantidad', 0) * (item.get('precio_unitario', 0) or item.get('precioUnitario', 0))) for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        # Tabla de totales (alineada a la derecha)
        table = self.doc.add_table(rows=3, cols=2)
        table.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        # Subtotal
        simbolo = self._obtener_simbolo_moneda()
        table.rows[0].cells[0].text = 'SUBTOTAL:'
        table.rows[0].cells[1].text = f'{simbolo} {subtotal:.2f}'
        
        # IGV
        table.rows[1].cells[0].text = 'IGV (18%):'
        table.rows[1].cells[1].text = f'{simbolo} {igv:.2f}'
        
        # Total
        table.rows[2].cells[0].text = 'TOTAL:'
        table.rows[2].cells[1].text = f'{simbolo} {total:.2f}'
        
        # Estilo de la última fila (total)
        for cell in table.rows[2].cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.size = Pt(14)
                    run.font.color.rgb = RGBColor(255, 255, 255)
            
            # Fondo con color personalizado
            shading_elm = OxmlElement('w:shd')
            color_hex = self._rgb_to_hex(self.COLOR_PRIMARIO)
            shading_elm.set(qn('w:fill'), color_hex)
            cell._element.get_or_add_tcPr().append(shading_elm)
            
            # Bordes
            border_spec = {"sz": 8, "val": "single", "color": color_hex}
            self._set_cell_border(cell, top=border_spec, bottom=border_spec, left=border_spec, right=border_spec)
        
        self.doc.add_paragraph()
    
    def _agregar_observaciones(self):
        """Agrega sección de observaciones"""
        p_titulo = self.doc.add_paragraph('Observaciones Técnicas')
        p_titulo.runs[0].font.size = Pt(12)
        p_titulo.runs[0].font.bold = True
        p_titulo.runs[0].font.color.rgb = self.COLOR_PRIMARIO
        
        observaciones = [
            'Trabajos ejecutados según CNE - Código Nacional de Electricidad',
            'Materiales de primera calidad con certificación',
            'Mano de obra especializada',
            'Garantía de 12 meses en mano de obra',
            f'Precios en {self.datos.get("settings", {}).get("currency", "soles peruanos (PEN)")}',
            'Forma de pago: 50% adelanto, 50% contra entrega',
            f"Cotización válida por {self.datos.get('vigencia', '30 días')}"
        ]
        
        for obs in observaciones:
            p = self.doc.add_paragraph(obs, style='List Bullet')
            p.runs[0].font.size = Pt(10)
    
    def _agregar_footer(self):
        """Agrega pie de página"""
        return self._agregar_footer_basico()
    
    def generar(self, ruta_salida):
        """
        Genera el documento Word completo
        
        Args:
            ruta_salida: Ruta donde guardar el documento
        
        Returns:
            Ruta del documento generado
        """
        # Construir documento
        self._agregar_header()
        self._agregar_titulo()
        self._agregar_info_general()
        self._agregar_tabla_items()
        self._agregar_totales()
        self._agregar_observaciones()
        self._agregar_footer()
        
        # Guardar
        self.doc.save(ruta_salida)
        return ruta_salida


def generar_cotizacion_simple(datos, ruta_salida, opciones=None):
    """
    Función helper para generar cotización simple
    """
    generator = CotizacionSimpleGenerator(datos, opciones)
    return generator.generar(ruta_salida)
