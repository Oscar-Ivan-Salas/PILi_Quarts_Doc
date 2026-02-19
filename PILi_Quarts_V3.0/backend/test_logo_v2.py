"""
Script de Prueba V2: Generar Excel con LOGS DETALLADOS del logo
"""

import sys
import logging
from pathlib import Path

# Configurar logging VERBOSE
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(name)s - %(message)s'
)

backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from modules.N04_Binary_Factory.index import BinaryFactory
import base64

request_data = {
    "header": {
        "user_id": "PRUEBA-002",
        "service_id": 1,
        "document_type": "ELECTRICIDAD_COTIZACION_SIMPLE"
    },
    "branding": {
        "color_hex": "#CC0000"
    },
    "payload": {
        "client_info": {
            "nombre": "PRUEBA LOGO REDIMENSIONADO",
            "ruc": "20601138787",
            "direccion": "Test Address",
            "telefono": "999999999",
            "email": "test@test.com",
            "fecha": "17/02/2026"
        },
        "items": [
            {
                "index": 1,
                "descripcion": "Item de prueba",
                "cantidad": "1",
                "unidad": "und",
                "precio_unitario": "100.00",
                "total": "100.00"
            }
        ],
        "totals": {
            "subtotal": "100.00",
            "igv": "18.00",
            "total": "118.00"
        },
        "technical_notes": "Prueba de logo"
    },
    "output_format": "XLSX"
}

print("=" * 80)
print("🔍 PRUEBA CON LOGS DETALLADOS - Logo Redimensionamiento")
print("=" * 80)
print()

try:
    factory = BinaryFactory()
    result = factory.process_request(request_data)
    
    if result.get('success'):
        file_b64 = result.get('file_b64')
        output_path = backend_path / "PRUEBA_LOGO_V2.xlsx"
        file_bytes = base64.b64decode(file_b64)
        
        with open(output_path, 'wb') as f:
            f.write(file_bytes)
        
        print(f"\n✅ Excel guardado: {output_path}")
        print(f"📊 Tamaño: {len(file_bytes):,} bytes")
        print()
        print("🔍 REVISA LOS LOGS ARRIBA para ver:")
        print("   - '✅ Logo insertado: XXXxYYYpx'")
        print("   - Si dice 150x60 o menos → CORRECTO")
        print("   - Si dice 512x472 → ERROR (no se redimensionó)")
    else:
        print(f"❌ Error: {result.get('error')}")
        
except Exception as e:
    print(f"❌ EXCEPCIÓN: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
