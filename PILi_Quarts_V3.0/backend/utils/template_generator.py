"""
Template Generator - HTML Construction for PDF
Generates printable HTML strings mimicking the React components
"""
import json

def generate_html_template(doc_type, data, color_scheme='azul-tesla', font='Calibri'):
    """
    Generates a full HTML string with inline CSS for the given document type
    """
    
    # Define colors
    colors = {
        'azul-tesla': {'primary': '#0052A3', 'secondary': '#1E40AF', 'light': '#EFF6FF', 'border': '#DBEAFE'},
        'rojo-pili': {'primary': '#DC2626', 'secondary': '#991B1B', 'light': '#FEF2F2', 'border': '#FECACA'},
        'amarillo-pili': {'primary': '#D97706', 'secondary': '#B45309', 'light': '#FFFBEB', 'border': '#FDE68A'},
    }.get(color_scheme, {'primary': '#0052A3', 'secondary': '#1E40AF', 'light': '#EFF6FF', 'border': '#DBEAFE'})
    
    # Common CSS
    css = f"""
    <style>
        @page {{ size: A4; margin: 20mm; }}
        body {{ font-family: '{font}', sans-serif; color: #1f2937; line-height: 1.6; margin: 0; }}
        .header {{ display: flex; justify-content: space-between; border-bottom: 4px solid {colors['primary']}; padding-bottom: 20px; margin-bottom: 30px; }}
        .logo-box {{ width: 180px; height: 80px; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); color: white; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; border-radius: 8px; }}
        .company-info {{ text-align: right; font-size: 11px; color: #4b5563; }}
        .company-name {{ font-size: 20px; font-weight: bold; color: {colors['primary']}; margin-bottom: 8px; text-transform: uppercase; }}
        .title-box {{ text-align: center; margin: 30px 0; padding: 20px; background: {colors['light']}; border-left: 6px solid {colors['primary']}; border-radius: 4px; }}
        .doc-title {{ font-size: 28px; color: {colors['primary']}; font-weight: bold; margin-bottom: 8px; }}
        .section {{ margin: 25px 0; }}
        .section-title {{ font-size: 14px; color: {colors['primary']}; font-weight: bold; text-transform: uppercase; border-bottom: 2px solid {colors['primary']}; padding-bottom: 5px; margin-bottom: 10px; }}
        .label {{ font-size: 12px; font-weight: bold; color: {colors['secondary']}; }}
        .value {{ font-size: 12px; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .box {{ padding: 15px; border: 2px solid {colors['border']}; border-radius: 6px; background: #F9FAFB; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th {{ background: {colors['primary']}; color: white; padding: 10px; font-size: 12px; text-align: left; }}
        td {{ border-bottom: 1px solid #E5E7EB; padding: 10px; font-size: 11px; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 3px solid {colors['primary']}; text-align: center; font-size: 10px; color: #6B7280; }}
    </style>
    """

    # Header HTML
    header = f"""
    <div class="header">
        <div>
            <div class="logo-box">PILi</div>
            <p style="font-size: 10px; color: #6B7280; margin-top: 5px">Electricidad y Automatización</p>
        </div>
        <div class="company-info">
            <div class="company-name">PILi QUARTS - INGENIERÍA</div>
            <div>RUC: 20601138787</div>
            <div>Calle Las Ágatas, SJL</div>
            <div>contacto@piliquarts.com</div>
        </div>
    </div>
    """

    # Content based on Type
    content = ""
    
    if doc_type == 'proyecto-simple':
        content = f"""
        <div class="title-box">
            <div class="doc-title">PROPUESTA DE PROYECTO</div>
            <div>{data.get('proyecto', {}).get('nombre', 'Sin Nombre')}</div>
        </div>
        
        <div class="grid-2">
            <div class="box">
                <div class="section-title">Datos del Cliente</div>
                <p><span class="label">Cliente:</span> <span class="value">{data.get('cliente', {}).get('nombre', '')}</span></p>
                <p><span class="label">RUC:</span> <span class="value">{data.get('cliente', {}).get('ruc', '')}</span></p>
            </div>
            <div class="box">
                <div class="section-title">Datos del Proyecto</div>
                <p><span class="label">Ubicación:</span> <span class="value">{data.get('proyecto', {}).get('ubicacion', '')}</span></p>
                <p><span class="label">Duración:</span> <span class="value">{data.get('proyecto', {}).get('duracion', '')} días</span></p>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Descripción y Alcance</div>
            <div class="box">
                <p class="value">{data.get('proyecto', {}).get('descripcion', '')}</p>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Fases del Proyecto</div>
            <table>
                <thead>
                    <tr><th>Fase</th><th>Duración</th></tr>
                </thead>
                <tbody>
                    {''.join([f"<tr><td>{f.get('nombre')}</td><td>{f.get('duracion')} días</td></tr>" for f in data.get('fases', [])])}
                </tbody>
            </table>
        </div>
        """
        
    elif doc_type == 'cotizacion-simple':
        items_html = ''.join([
            f"<tr><td>{item.get('item')}</td><td>{item.get('descripcion')}</td><td>{item.get('cantidad')}</td><td>{item.get('unidad')}</td><td>{item.get('precioUnitario')}</td><td>{item.get('precioTotal')}</td></tr>" 
            for item in data.get('suministros', [])
        ])
        
        # Calculate totals safely
        total = sum(float(item.get('precioTotal', 0)) for item in data.get('suministros', []))
        igv = total * 0.18
        grand_total = total + igv

        content = f"""
        <div class="title-box">
            <div class="doc-title">COTIZACIÓN DE SERVICIOS</div>
            <div>Ref: {data.get('proyecto', {}).get('nombre', 'Sin Referencia')}</div>
        </div>
        
        <div class="grid-2">
            <div class="box">
                <div class="section-title">Cliente</div>
                <p><span class="label">Nombre:</span> <span class="value">{data.get('cliente', {}).get('nombre', '')}</span></p>
            </div>
            <div class="box">
                <div class="section-title">Detalles</div>
                <p><span class="label">Fecha:</span> <span class="value">{datetime.now().strftime('%d/%m/%Y')}</span></p>
            </div>
        </div>
        
        <div class="section">
            <table>
                <thead>
                    <tr><th>Item</th><th>Descripción</th><th>Cant.</th><th>Und.</th><th>P. Unit</th><th>Total</th></tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>
            <div style="text-align: right; font-size: 14px;">
                <p><strong>Subtotal:</strong> {total:.2f}</p>
                <p><strong>IGV (18%):</strong> {igv:.2f}</p>
                <p style="font-size: 18px; color: {colors['primary']}"><strong>TOTAL: {grand_total:.2f}</strong></p>
            </div>
        </div>
        """
        
    else:
        # Generic content for other types
        content = f"""
        <div class="title-box">
            <div class="doc-title">{doc_type.replace('-', ' ').upper()}</div>
            <div>{data.get('proyecto', {}).get('nombre', '')}</div>
        </div>
        <div class="box">
            <pre style="white-space: pre-wrap; font-family: inherit;">{json.dumps(data, indent=2, ensure_ascii=False)}</pre>
        </div>
        """

    # Footer
    footer = f"""
    <div class="footer">
        <div>PILi QUARTS - INGENIERÍA</div>
        <div>Generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
    </div>
    """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>{css}</head>
    <body>
        {header}
        {content}
        {footer}
    </body>
    </html>
    """
