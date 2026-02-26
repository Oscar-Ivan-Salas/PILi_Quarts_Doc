
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

        # 2. Motor de Reemplazo Universal (Flatten Data)
        def flatten_dict(d, prefix=''):
            res = {}
            for k, v in d.items():
                key = f"{prefix}{k.upper()}"
                if isinstance(v, dict):
                    res.update(flatten_dict(v, f"{key}_"))
                else:
                    res[key] = v
            return res

        flat_data = flatten_dict(data)
        flat_data["NUMERO_COTIZACION"] = data.get("numero") or data.get("codigo", "DOC-000")
        flat_data["CLIENTE"] = data.get("client_info", {}).get("nombre", "CLIENTE")
        
        # Totals and Currency
        settings = data.get("settings", {})
        currency_code = settings.get("currency", "PEN")
        simbolos = {'PEN': 'S/', 'USD': '$', 'EUR': '€'}
        simbolo = simbolos.get(currency_code, 'S/')
        
        # Reemplazar placeholders dinámicamente
        for k, v in flat_data.items():
            placeholder = "{{" + k + "}}"
            if placeholder in html_content:
                if isinstance(v, (int, float)) and any(x in k for x in ['TOTAL', 'SUBTOTAL', 'IGV', 'PRESUPUESTO']):
                    val_str = f"{simbolo} {float(v):,.2f}"
                else:
                    val_str = str(v)
                html_content = html_content.replace(placeholder, val_str)

        # Inyectar ADN Visual (Colores)
        branding = data.get("branding", {})
        primary_color = branding.get("color") or "#0052A3"
        adn_style = f"""
        <style>
            :root {{
                --color-primario: {primary_color};
            }}
            .color-primario, .empresa-nombre, .titulo-documento h1, .info-box h3, 
            .tabla-section h2, .totales-label, .totales-valor, .footer-empresa {{
                color: {primary_color} !important;
            }}
            .bg-primario, thead, .totales-row:last-child {{
                background: {primary_color} !important;
            }}
            .header, .titulo-documento, .info-box h3, .tabla-section h2, .totales-box, .footer {{
                border-color: {primary_color} !important;
            }}
        </style>
        """
        if "</head>" in html_content:
            html_content = html_content.replace("</head>", adn_style + "</head>")

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
                        <td class="text-right">{simbolo} {float(item.get('precio', item.get('precio_unitario', 0))):,.2f}</td>
                        <td class="text-right">{simbolo} {float(item.get('total', 0)):,.2f}</td>
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
        
        # 3. Render PDF with Playwright (Isolated Subprocess to avoid Event Loop issues)
        import subprocess
        import sys
        import tempfile
        
        # Create temp HTML file for the CLI
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as tmp:
            tmp.write(html_content)
            tmp_path = tmp.name
            
        try:
            cli_path = Path(__file__).parent / "playwright_pdf_cli.py"
            # Use current python executable
            result = subprocess.run(
                [sys.executable, str(cli_path), tmp_path, output_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0 or "ERROR:" in result.stdout:
                raise RuntimeError(f"CLI PDF Failed: {result.stdout} {result.stderr}")
                
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            
        logger.info(f"✅ PDF Generated via Isolated Playwright: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Isolated Playwright Generation Failed: {e}", exc_info=True)
        raise e
