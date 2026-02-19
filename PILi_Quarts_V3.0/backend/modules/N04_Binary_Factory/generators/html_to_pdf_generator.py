
import logging
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64

logger = logging.getLogger("N04_PlaywrightGenerator")

def generate_pdf_playwright(data: dict, output_path: str, template_path: str = None, customization: dict = None) -> str:
    """
    Generates a PDF by rendering an HTML template with Playwright.
    Attributes:
        data: Dict containing 'items', 'totals', 'client_info', etc.
        output_path: Destination for the PDF.
        template_path: Path to the HTML template. If None, uses a default.
    """
    try:
        # 1. Resolve Template Path
        if not template_path:
            # Fallback to default template (Relative Path)
            # generators/ -> N04_Binary_Factory/ -> templates/
            base_factory_path = Path(__file__).parent.parent
            template_path = base_factory_path / "templates" / "ELECTRICIDAD_COTIZACION_SIMPLE" / "html" / "layout.html"
            logger.warning(f"⚠️ No template path provided. Using default fallback: {template_path}")
            
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"HTML Template not found: {template_path}")

        # 2. Read and Populate HTML (Simple Jinja-like replacement for speed/compatibility)
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Replace Placeholders (Data Injection)
        # Customization Injection (CSS Variables)
        css_custom = ""
        if customization:
            primary = customization.get('esquemaColores', {}).get('color', None) # Asumiendo que recibe objeto o ID
            # Si recibe solo ID, necesitariamos mapa. Mejor que reciba el HEX directo.
            # Ajustaremos para que reciba lo que envia el frontend (docConfig)
            
            # Mapeo rapido si viene nombre
            color_map = {
                'azul-tesla': '#3B82F6', 'rojo-energia': '#EF4444', 
                'verde-ecologico': '#22C55E', 'personalizado': '#8B5CF6'
            }
            color_id = customization.get('esquemaColores', 'azul-tesla')
            primary_color = color_map.get(color_id, '#3B82F6')
            
            # FontSize & Family
            font_size = customization.get('tamanoFuente', 11)
            font_name = customization.get('fuenteDocumento', 'Calibri')
            
            # Google Fonts Map
            font_urls = {
                'Roboto': 'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap',
                'Arial': '', # System font
                'Calibri': '' # System font
            }
            font_import = ""
            if font_name in font_urls and font_urls[font_name]:
                font_import = f"@import url('{font_urls[font_name]}');"
                
            css_custom = f"""
            <style>
                {font_import}
                :root {{
                    --primary-color: {primary_color} !important;
                    --secondary-color: {primary_color} !important; 
                    --font-size-base: {font_size}pt !important;
                    --font-family-base: '{font_name}', sans-serif !important;
                }}
                body {{ 
                    font-size: var(--font-size-base) !important; 
                    font-family: var(--font-family-base) !important;
                }}
                .header, .borde-color {{ border-color: var(--primary-color) !important; color: var(--primary-color) !important; }}
                th {{ background-color: var(--primary-color) !important; }}
                h1, h2, h3, .text-primary {{ color: var(--primary-color) !important; }}
                
                /* Force overrides */
                *[style*="border-bottom"] {{ border-bottom-color: var(--primary-color) !important; }}
                *[style*="color: #0052A3"] {{ color: var(--primary-color) !important; }}
                
                /* Reemplazo de Logo si es necesario (manejado por HTML directo usualmente) */
            </style>
            """

        # Replace Placeholders (Data Injection)
        # Header/Footer
        html_content = html_content.replace("{{NUMERO_COTIZACION}}", data.get("codigo", "COT-0000"))
        
        
        # 🟢 SEARCH & REPLACE BRUTE FORCE (Safety Net for Styles)
        if customization:
            try:
                # Recalculate or use existing primary_color safely
                # If primary_color is not in local scope (because it was defined in a previous if block that might share scope but let's be safe), recalculate.
                if 'primary_color' not in locals():
                     color_id = customization.get('esquemaColores', 'azul-tesla')
                     # Simple map fallback
                     color_map_pdf = {
                        'azul-tesla': '#3B82F6',
                        'rojo-energia': '#EF4444',
                        'verde-ecologico': '#10B981',
                        'dorado-premium': '#F59E0B'
                     }
                     target_col = color_map_pdf.get(color_id, '#3B82F6')
                else:
                     target_col = primary_color

                common_blues = [
                    '#3B82F6', '#2563EB', '#1D4ED8', '#0052cc', # Hex
                    'rgb(59, 130, 246)', 'rgb(37, 99, 235)', 'rgb(29, 78, 216)', 'rgb(0, 82, 204)' # RGB
                ]
                
                for blue in common_blues:
                    html_content = html_content.replace(blue, target_col)
                    if blue.startswith('#'):
                        html_content = html_content.replace(blue.lower(), target_col)
                        
                logger.info("🎨 Colores reemplazados en HTML (PDF) por " + target_col)
            except Exception as e:
                logger.error(f"⚠️ Error reemplazando colores en PDF (ignorando): {e}")

        # INJECT CSS
        if "</head>" in html_content:
            html_content = html_content.replace("</head>", f"{css_custom}</head>")
        else:
            html_content = css_custom + html_content
        html_content = html_content.replace("{{CLIENTE}}", data.get("client_info", {}).get("nombre", "CLIENTE GENERAL"))
        html_content = html_content.replace("{{RUC_CLIENTE}}", data.get("client_info", {}).get("ruc", "00000000000"))
        html_content = html_content.replace("{{DIRECCION_CLIENTE}}", data.get("client_info", {}).get("direccion", "Lima, Peru"))
        
        # Totals
        totals = data.get("totals", {})
        html_content = html_content.replace("{{SUBTOTAL}}", f"{float(totals.get('subtotal', 0)):,.2f}")
        html_content = html_content.replace("{{IGV}}", f"{float(totals.get('igv', 0)):,.2f}")
        html_content = html_content.replace("{{TOTAL}}", f"{float(totals.get('total', 0)):,.2f}")

        # Items - Dynamic Construction
        # We need to find the `<tbody>` and inject rows.
        # This is a bit hacky with string replacement but valid for this specific template structure.
        items_html = ""
        items = data.get("items", [])
        for idx, item in enumerate(items, 1):
             row = f"""
                    <tr>
                        <td>{idx:02d}</td>
                        <td>{item.get('descripcion', '')}</td>
                        <td class="text-right">{float(item.get('cantidad', 0)):.2f}</td>
                        <td class="text-right">{item.get('unidad', 'und')}</td>
                        <td class="text-right">$ {float(item.get('precio', 0)):,.2f}</td>
                        <td class="text-right">$ {float(item.get('total', 0)):,.2f}</td>
                    </tr>
             """
             items_html += row
             
        # Inject Items (Replacing a marker or appending to tbody if we parse it, 
        # but simpler to replace the example row if we know the structure, 
        # OR better: The template has `<!-- ITEMS DINÁMICOS -->`. Perfect.)
        
        # Remove existing example rows (approximate slash and burn for MVP)
        # We will split at <!-- ITEMS DINÁMICOS --> and </tbody>
        if "<!-- ITEMS DINÁMICOS -->" in html_content and "</tbody>" in html_content:
            pre_items, rest = html_content.split("<!-- ITEMS DINÁMICOS -->", 1)
            _, post_items = rest.split("</tbody>", 1)
            html_content = pre_items + items_html + "</tbody>" + post_items
        
        # 3. Render PDF with Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set Content
            page.set_content(html_content)
            
            # Print to PDF
            page.pdf(path=output_path, format="A4", margin={"top": "2cm", "bottom": "2cm", "left": "2cm", "right": "2cm"}, print_background=True)
            
            browser.close()
            
        logger.info(f"✅ PDF Generated via Playwright: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Playwright Generation Failed: {e}", exc_info=True)
        raise e
