
import sys
import os
import logging
from pathlib import Path

# Setup path relative to script location
# Assuming script is in backend/reproduce_error_500.py
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR)) # Add backend/ to path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock Data
mock_html = """
<!DOCTYPE html>
<html>
<head><style>.text-blue-600 { color: #2563EB; }</style></head>
<body>
    <div class="text-blue-600">Test Content</div>
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=" />
</body>
</html>
"""

mock_customization = {
    "esquemaColores": "rojo-energia",
    "logoBase64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
    "fuenteDocumento": "Roboto",
    "tamanoFuente": 12
}

def test_word_generation():
    print("\n--- Testing Word Generation ---")
    try:
        from app.routers.generation import _generate_word_from_html
        output = Path("test_output.docx")
        
        # Call function
        result = _generate_word_from_html(mock_html, str(output), "test_doc", customization=mock_customization)
        print(f"✅ Word Generated: {result}")
        
    except Exception as e:
        print(f"❌ Word Error: {e}")
        import traceback
        traceback.print_exc()

def test_pdf_generation():
    print("\n--- Testing PDF Generation ---")
    try:
        from modules.N04_Binary_Factory.generators.html_to_pdf_generator import generate_pdf_playwright
        output = Path("test_output.pdf")
        
        # Check defaults first
        # Need to simulate what generation.py does: it calls _generate_pdf_from_html which calls generate_pdf_playwright
        # Let's import the wrapper from generation.py if possible, or just the generator
        
        # Actually generation.py has the logic I added (or did I add it to the module? let's check file view history)
        # I added substitution logic to html_to_pdf_generator.py in "Step Id: 16928"
        # So testing the module directly is good.
        
        data = {"codigo": "COT-TEST", "client_info": {}, "totals": {}, "items": []}
        generate_pdf_playwright(data, str(output), template_path=None, customization=mock_customization) 
        # Wait, generate_pdf_playwright expects template_path. generation.py passes str(tmp_html).
        # But if I pass template_path=None it uses default.
        # I want to test the customization logic.
        
        # Let's create a temp html file to pass as template
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as f:
            f.write(mock_html)
            tmp_path = f.name
            
        generate_pdf_playwright(data, str(output), template_path=tmp_path, customization=mock_customization)
        print(f"✅ PDF Generated: {output}")
        
    except Exception as e:
        print(f"❌ PDF Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_word_generation()
    test_pdf_generation()
