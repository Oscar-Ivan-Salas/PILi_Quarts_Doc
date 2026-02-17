
import logging
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64

logger = logging.getLogger("N04_PlaywrightGenerator")

def generate_pdf_playwright(data: dict, output_path: str, template_path: str = None) -> str:
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
        # Header/Footer
        html_content = html_content.replace("{{NUMERO_COTIZACION}}", data.get("codigo", "COT-0000"))
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
