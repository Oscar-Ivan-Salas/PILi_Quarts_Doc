"""
Template Renderer Service
Carga y renderiza las 6 plantillas HTML profesionales con datos dinámicos
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TemplateRenderer:
    """Renderiza plantillas HTML con datos dinámicos y personalización"""
    
    # Mapeo de tipo_documento → archivo de plantilla
    TEMPLATE_MAP = {
        'cotizacion': 'PLANTILLA_HTML_COTIZACION_SIMPLE.html',
        'cotizacion-simple': 'PLANTILLA_HTML_COTIZACION_SIMPLE.html',
        'cotizacion-compleja': 'PLANTILLA_HTML_COTIZACION_COMPLEJA.html',
        'proyecto': 'PLANTILLA_HTML_PROYECTO_SIMPLE.html',
        'proyecto-simple': 'PLANTILLA_HTML_PROYECTO_SIMPLE.html',
        'proyecto-pmi': 'PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html',
        'informe-tecnico': 'PLANTILLA_HTML_INFORME_TECNICO.html',
        'informe-ejecutivo': 'PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html',
    }
    
    # Esquemas de colores (4 opciones)
    COLOR_SCHEMES = {
        'azul': {
            'primario': '#0052A3',
            'secundario': '#1E40AF',
            'acento': '#3B82F6',
            'claro': '#EFF6FF',
        },
        'rojo': {
            'primario': '#8B0000',
            'secundario': '#991B1B',
            'acento': '#DC2626',
            'claro': '#FEE2E2',
        },
        'verde': {
            'primario': '#065F46',
            'secundario': '#047857',
            'acento': '#10B981',
            'claro': '#D1FAE5',
        },
        'dorado': {
            'primario': '#D4AF37',
            'secundario': '#B8860B',
            'acento': '#FFD700',
            'claro': '#FEF3C7',
        },
    }
    
    def __init__(self, templates_dir: str = None):
        """
        Inicializa el renderizador de plantillas
        
        Args:
            templates_dir: Directorio donde están las plantillas HTML
        """
        if templates_dir is None:
            # Buscar DOCUMENTOS TESIS en el proyecto
            base_dir = Path(__file__).parent.parent.parent.parent
            templates_dir = base_dir / "DOCUMENTOS TESIS"
        
        self.templates_dir = Path(templates_dir)
        logger.info(f"📁 Template directory: {self.templates_dir}")
    
    def cargar_plantilla(self, tipo_documento: str) -> str:
        """
        Carga una plantilla HTML desde el disco
        
        Args:
            tipo_documento: Tipo de documento (cotizacion, proyecto, informe-tecnico, etc.)
        
        Returns:
            str: Contenido HTML de la plantilla
        """
        # Normalizar tipo
        tipo_documento = tipo_documento.lower().replace('_', '-')
        
        # Obtener nombre de archivo
        template_file = self.TEMPLATE_MAP.get(tipo_documento)
        if not template_file:
            logger.warning(f"⚠️ Tipo desconocido: {tipo_documento}, usando cotizacion-simple")
            template_file = self.TEMPLATE_MAP['cotizacion-simple']
        
        # Cargar archivo
        template_path = self.templates_dir / template_file
        
        if not template_path.exists():
            raise FileNotFoundError(f"Plantilla no encontrada: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        logger.info(f"✅ Plantilla cargada: {template_file}")
        return html
    
    def mapear_datos(self, datos: Dict[str, Any]) -> Dict[str, str]:
        """
        Mapea datos de PILI a variables de plantilla
        
        Args:
            datos: Datos del documento (cliente, proyecto, items, etc.)
        
        Returns:
            dict: Variables mapeadas para reemplazo
        """
        variables = {}
        
        # Cliente
        cliente = datos.get('cliente', {})
        if isinstance(cliente, dict):
            variables['CLIENTE_NOMBRE'] = cliente.get('nombre', 'Cliente')
            variables['CLIENTE'] = cliente.get('nombre', 'Cliente')
        else:
            variables['CLIENTE_NOMBRE'] = str(cliente)
            variables['CLIENTE'] = str(cliente)
        
        # Proyecto
        variables['PROYECTO_NOMBRE'] = datos.get('proyecto', 'Proyecto')
        variables['NOMBRE_PROYECTO'] = datos.get('proyecto', 'Proyecto')
        
        # Fechas
        fecha = datos.get('fecha', datetime.now().strftime('%d/%m/%Y'))
        variables['FECHA_COTIZACION'] = fecha
        variables['FECHA'] = fecha
        variables['FECHA_INICIO'] = fecha
        
        # Números y códigos
        variables['NUMERO_COTIZACION'] = datos.get('numero', 'COT-001')
        variables['CODIGO_PROYECTO'] = datos.get('numero', 'PROY-001')
        variables['CODIGO_INFORME'] = datos.get('numero', 'INF-001')
        
        # Servicio y normativa
        variables['SERVICIO_NOMBRE'] = datos.get('servicio', 'Instalaciones Eléctricas')
        variables['NORMATIVA_APLICABLE'] = datos.get('normativa', 'CNE - Código Nacional de Electricidad')
        
        # Descripción
        variables['DESCRIPCION_PROYECTO'] = datos.get('descripcion', datos.get('contexto', ''))
        variables['ALCANCE_PROYECTO'] = datos.get('descripcion', datos.get('contexto', ''))
        variables['RESUMEN_EJECUTIVO'] = datos.get('descripcion', datos.get('contexto', ''))
        
        # Área
        variables['AREA_M2'] = str(datos.get('area_m2', '100'))
        
        # Vigencia
        variables['VIGENCIA'] = datos.get('vigencia', '30 días')
        
        # Totales
        variables['SUBTOTAL'] = f"{datos.get('subtotal', 0):.2f}"
        variables['IGV'] = f"{datos.get('igv', 0):.2f}"
        variables['TOTAL'] = f"{datos.get('total', 0):.2f}"
        variables['PRESUPUESTO'] = f"{datos.get('total', 0):.2f}"
        
        # Duraciones estimadas (para proyectos)
        variables['DURACION_TOTAL'] = str(datos.get('duracion_dias', 30))
        variables['DIAS_INGENIERIA'] = str(datos.get('dias_ingenieria', 10))
        variables['DIAS_ADQUISICIONES'] = str(datos.get('dias_adquisiciones', 7))
        variables['DIAS_INSTALACION'] = str(datos.get('dias_instalacion', 15))
        variables['DIAS_EJECUCION'] = str(datos.get('dias_ejecucion', 15))
        variables['DIAS_PRUEBAS'] = str(datos.get('dias_pruebas', 5))
        
        # Fecha fin estimada
        variables['FECHA_FIN'] = datos.get('fecha_fin', fecha)
        
        # Métricas PMI (valores por defecto)
        variables['SPI'] = '1.0'
        variables['CPI'] = '1.0'
        variables['EV_K'] = str(int(datos.get('total', 0) / 1000))
        variables['PV_K'] = str(int(datos.get('total', 0) / 1000))
        variables['AC_K'] = str(int(datos.get('total', 0) / 1000))
        
        # Métricas financieras (estimaciones)
        variables['ROI_ESTIMADO'] = '25'
        variables['TIR_PROYECTADA'] = '18'
        variables['PAYBACK_MESES'] = '12'
        variables['AHORRO_ANUAL_K'] = str(int(datos.get('total', 0) * 0.2 / 1000))
        variables['AHORRO_ENERGETICO'] = f"{datos.get('total', 0) * 0.15:.2f}"
        
        # Inversión desglosada
        total = datos.get('total', 0)
        variables['INVERSION_EQUIPOS'] = f"{total * 0.7:.2f}"
        variables['INVERSION_MANO_OBRA'] = f"{total * 0.2:.2f}"
        variables['CAPITAL_TRABAJO'] = f"{total * 0.1:.2f}"
        
        # Títulos específicos
        variables['TITULO_INFORME'] = datos.get('titulo', variables['PROYECTO_NOMBRE'])
        variables['TITULO_PROYECTO'] = datos.get('titulo', variables['PROYECTO_NOMBRE'])
        
        logger.info(f"📊 Variables mapeadas: {len(variables)}")
        return variables
    
    def aplicar_colores(self, html: str, esquema: str = 'azul') -> str:
        """
        Aplica esquema de colores a la plantilla HTML
        
        Args:
            html: HTML de la plantilla
            esquema: Nombre del esquema de colores (azul, rojo, verde, dorado)
        
        Returns:
            str: HTML con colores aplicados
        """
        esquema = esquema.lower()
        if esquema not in self.COLOR_SCHEMES:
            logger.warning(f"⚠️ Esquema desconocido: {esquema}, usando azul")
            esquema = 'azul'
        
        colores = self.COLOR_SCHEMES[esquema]
        
        # Reemplazar colores en CSS
        # Color primario
        html = html.replace('#0052A3', colores['primario'])
        # Color secundario
        html = html.replace('#1E40AF', colores['secundario'])
        # Color acento
        html = html.replace('#3B82F6', colores['acento'])
        # Color claro
        html = html.replace('#EFF6FF', colores['claro'])
        html = html.replace('#DBEAFE', colores['claro'])
        
        logger.info(f"🎨 Colores aplicados: {esquema}")
        return html
    
    def generar_tabla_items(self, items: List[Dict[str, Any]]) -> str:
        """
        Genera HTML de tabla de items
        
        Args:
            items: Lista de items con descripcion, cantidad, unidad, precio_unitario
        
        Returns:
            str: HTML de filas de tabla
        """
        if not items:
            return ""
        
        filas_html = []
        for i, item in enumerate(items, 1):
            cantidad = float(item.get('cantidad', 0))
            precio_unitario = float(item.get('precio_unitario', item.get('precioUnitario', 0)))
            total_item = cantidad * precio_unitario
            
            fila = f"""
                    <tr>
                        <td>{i:02d}</td>
                        <td>{item.get('descripcion', '')}</td>
                        <td class="text-right">{cantidad:.2f}</td>
                        <td class="text-right">{item.get('unidad', 'und')}</td>
                        <td class="text-right">$ {precio_unitario:.2f}</td>
                        <td class="text-right">$ {total_item:.2f}</td>
                    </tr>"""
            filas_html.append(fila)
        
        return '\n'.join(filas_html)
    
    def reemplazar_variables(self, html: str, variables: Dict[str, str]) -> str:
        """
        Reemplaza variables {{VARIABLE}} en el HTML
        
        Args:
            html: HTML con variables
            variables: Diccionario de variables y valores
        
        Returns:
            str: HTML con variables reemplazadas
        """
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            html = html.replace(placeholder, str(value))
        
        # Limpiar variables no reemplazadas (opcional)
        # html = re.sub(r'\{\{[A-Z_]+\}\}', '', html)
        
        return html
    
    def renderizar(
        self, 
        tipo_documento: str, 
        datos: Dict[str, Any],
        esquema_color: str = 'azul'
    ) -> str:
        """
        Renderiza una plantilla completa con datos
        
        Args:
            tipo_documento: Tipo de documento
            datos: Datos del documento
            esquema_color: Esquema de colores (azul, rojo, verde, dorado)
        
        Returns:
            str: HTML renderizado
        """
        logger.info(f"🎨 Renderizando {tipo_documento} con esquema {esquema_color}")
        
        # 1. Cargar plantilla
        html = self.cargar_plantilla(tipo_documento)
        
        # 2. Aplicar colores
        html = self.aplicar_colores(html, esquema_color)
        
        # 3. Mapear datos
        variables = self.mapear_datos(datos)
        
        # 4. Generar tabla de items si existe
        if 'items' in datos and datos['items']:
            tabla_items = self.generar_tabla_items(datos['items'])
            # Buscar y reemplazar sección de items
            # Por ahora, las plantillas ya tienen items de ejemplo
            # En producción, buscaríamos el <tbody> y lo reemplazaríamos
        
        # 5. Reemplazar variables
        html = self.reemplazar_variables(html, variables)
        
        logger.info(f"✅ Renderizado completado: {len(html)} caracteres")
        return html


# Función helper para uso rápido
def renderizar_documento(
    tipo_documento: str,
    datos: Dict[str, Any],
    esquema_color: str = 'azul'
) -> str:
    """
    Función helper para renderizar un documento
    
    Args:
        tipo_documento: Tipo de documento
        datos: Datos del documento
        esquema_color: Esquema de colores
    
    Returns:
        str: HTML renderizado
    """
    renderer = TemplateRenderer()
    return renderer.renderizar(tipo_documento, datos, esquema_color)
