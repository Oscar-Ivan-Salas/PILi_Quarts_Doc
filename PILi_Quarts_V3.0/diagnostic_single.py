
import sys
import os
import base64
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'backend')))

from modules.N04_Binary_Factory.index import binary_factory

payload = {
    'header': {'service_id': 42, 'user_id': 'DIAG_USER', 'document_type': 6}, 
    'branding': {'logo_b64': None, 'color_hex': '#0052A3'}, 
    'payload': {
        'client_info': {'nombre': 'DIAGNOSTIC TEST'}, 
        'items': [], 
        'totals': {}, 
        'technical_notes': 'Prueba de diagnóstico directo'
    }, 
    'output_format': 'DOCX'
}

print("Generating PROYECTO_COMPLEJO (Mode 4)...")
result = binary_factory.process_request(payload)
if result.get('success'):
    filename = result.get('filename')
    file_b64 = result.get('file_b64')
    output_path = Path("e:/PILi_Quarts/PILi_Quarts_V3.0/DOCUMENTOS PRUEBA WORD") / f"DIAG_{filename}"
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(file_b64))
    print(f"✅ Success! Saved to {output_path}")
    print(f"📏 Size: {output_path.stat().st_size} bytes")
    print(f"⚙️ Engine: {result.get('engine')}")
else:
    print(f"❌ Error: {result.get('error')}")
