"""
N04 BINARY FACTORY - PURE MIRROR PDF GENERATOR (PLAYWRIGHT)
==========================================================
Protocolo R.A.L.F.T.H. (Fidelidad Visual Absoluta)
"""

import logging
from playwright.sync_api import sync_playwright

logger = logging.getLogger("N04_PDF_Generator")

def generate_pdf_playwright(html_content: str, output_path: str) -> str:
    """
    Renderiza HTML ya procesado a un archivo PDF de alta fidelidad.
    """
    logger.info(f"🔄 Renderizando PDF (Playwright): {output_path}")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Inyectar el HTML directo
            page.set_content(html_content, wait_until="networkidle")
            
            # Generar PDF con márgenes estándar y fondo habilitado
            page.pdf(
                path=output_path,
                format="A4",
                margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
                print_background=True
            )
            
            browser.close()
            
        logger.info(f"✅ PDF Generado con éxito: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"💥 Fallo en renderizado PDF Playwright: {e}")
        raise e
