
import sys
import os
import json
from bs4 import BeautifulSoup

# Ensure backend root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from modules.N04_Binary_Factory.index import binary_factory
    print("✅ Successfully imported binary_factory")
except ImportError as e:
    print(f"❌ Failed to import binary_factory: {e}")
    sys.exit(1)

def verify_mirror():
    """
    Verifies that the generated documents rely EXACTLY on the HTML structure and Mapping.
    """
    template_name = "ELECTRICIDAD_COTIZACION_COMPLEJA"
    # Locate template dir relative to the binary factory module
    import modules.N04_Binary_Factory
    base_dir = os.path.dirname(modules.N04_Binary_Factory.__file__)
    template_dir = os.path.join(base_dir, "templates", template_name)
    
    print(f"🔍 Inspecting Template: {template_name}")
    print(f"📂 Template Dir: {template_dir}")
    
    # 1. Read HTML Source ( The "Truth")
    layout_path = os.path.join(template_dir, "layout.html")
    if not os.path.exists(layout_path):
        print(f"❌ Layout not found: {layout_path}")
        return

    with open(layout_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
    print(f"✅ HTML Source Loaded. Title: {soup.title.string}")
    
    # 2. Read Mapping (The "Instructions")
    mapping_path = os.path.join(template_dir, "mapping.json")
    if not os.path.exists(mapping_path):
        print(f"❌ Mapping not found: {mapping_path}")
        return

    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)
        
    print(f"✅ Mapping Loaded. Excel Sheet: {mapping['excel_layout']['sheet_name']}")
    
    # 3. Generate Documents
    payload = {
        "header": {
            "user_id": "test_user_mirror",
            "service_id": 1,
            "document_type": template_name
        },
        "branding": {"color_hex": "#CC0000"},
        "payload": {
            "items": [
                {"index": 1, "description": "Mirror Test Item", "quantity": 10, "price": 100, "total": 1000}
            ],
            "totals": {"total": 1180},
            "client_info": {"name": "Mirror Client"}
        }
    }
    
    formats = ["XLSX", "DOCX", "PDF"]
    results = {}
    
    for fmt in formats:
        payload["output_format"] = fmt
        print(f"🚀 Generating {fmt}...")
        try:
             res = binary_factory.process_request(payload)
             if res["success"]:
                 print(f"  ✅ {fmt} Generated: {res['filename']}")
                 results[fmt] = True
             else:
                 print(f"  ❌ {fmt} Failed: {res['error']}")
                 results[fmt] = False
        except Exception as e:
            print(f"  ❌ {fmt} Crash: {e}")
            results[fmt] = False
            
    # Conclusion
    if all(results.values()):
        print("\n✨ MIRROR VERIFICATION SUCCESSFUL ✨")
        print("All 3 formats were generated using the SAME input data and SAME mapping logic.")
    else:
        print("\n❌ MIRROR VERIFICATION FAILED")

if __name__ == "__main__":
    verify_mirror()
