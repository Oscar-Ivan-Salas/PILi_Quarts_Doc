"""
Script de Prueba: Generar Excel usando N04_Binary_Factory (Caja Negra)
Objetivo: Verificar que la generación de Excel funciona correctamente
"""

import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from modules.N04_Binary_Factory.index import BinaryFactory
import base64
import json

# ============================================================================
# DATOS DE PRUEBA - Cotización Simple
# ============================================================================

request_data = {
    "header": {
        "user_id": "PRUEBA-001",
        "service_id": 1,
        "document_type": "ELECTRICIDAD_COTIZACION_SIMPLE"
    },
    "branding": {
        "color_hex": "#CC0000"  # Rojo
    },
    "payload": {
        "client_info": {
            "nombre": "ACEROS DEL PERÚ S.A.C.",
            "ruc": "20601138787",
            "direccion": "Jr. Las Águilas M-8 Lote 03, Urb. San Carlos, S.J.L.",
            "telefono": "968 315 961",
            "email": "ingenieria.teslaelectricidad@gmail.com",
            "fecha": "17/02/2026"
        },
        "items": [
            {
                "index": 1,
                "descripcion": "Tablero eléctrico monofásico 12 circuitos",
                "cantidad": "2",
                "unidad": "und",
                "precio_unitario": "450.00",
                "total": "900.00"
            },
            {
                "index": 2,
                "descripcion": "Circuitos eléctricos empotrados 14AWG THW (inc. tubería PVC)",
                "cantidad": "6",
                "unidad": "cto",
                "precio_unitario": "120.00",
                "total": "720.00"
            },
            {
                "index": 3,
                "descripcion": "Puntos de iluminación LED",
                "cantidad": "10",
                "unidad": "pto",
                "precio_unitario": "45.00",
                "total": "450.00"
            },
            {
                "index": 4,
                "descripcion": "Tomacorrientes dobles con toma tierra",
                "cantidad": "8",
                "unidad": "pto",
                "precio_unitario": "35.00",
                "total": "280.00"
            },
            {
                "index": 5,
                "descripcion": "Sistema de puesta a tierra (inc. pozo + cable)",
                "cantidad": "1",
                "unidad": "glb",
                "precio_unitario": "850.00",
                "total": "850.00"
            }
        ],
        "totals": {
            "subtotal": "3,200.00",
            "igv": "576.00",
            "total": "3,776.00"
        },
        "technical_notes": "Instalación según CNE Suministro 2011"
    },
    "output_format": "XLSX"
}

# ============================================================================
# EJECUTAR GENERACIÓN
# ============================================================================

print("=" * 80)
print("🏭 PRUEBA: Generación Excel con N04_Binary_Factory")
print("=" * 80)
print()

print("📋 Request Data:")
print(json.dumps(request_data, indent=2, ensure_ascii=False))
print()

print("🚀 Invocando BinaryFactory.process_request()...")
print()

try:
    factory = BinaryFactory()
    result = factory.process_request(request_data)
    
    print("✅ Resultado:")
    print(f"   Success: {result.get('success')}")
    print(f"   Filename: {result.get('filename')}")
    print(f"   Engine: {result.get('engine')}")
    print(f"   MIME Type: {result.get('mime_type')}")
    
    if result.get('success'):
        # Decodificar y guardar
        file_b64 = result.get('file_b64')
        if file_b64:
            output_path = backend_path / "PRUEBA_EXCEL_N04.xlsx"
            file_bytes = base64.b64decode(file_b64)
            
            with open(output_path, 'wb') as f:
                f.write(file_bytes)
            
            file_size = len(file_bytes)
            print(f"   Tamaño: {file_size:,} bytes")
            print()
            print(f"📊 Excel guardado en: {output_path}")
            print()
            print("🎉 ¡PRUEBA EXITOSA!")
        else:
            print("❌ No se recibió file_b64 en la respuesta")
    else:
        print(f"❌ Error: {result.get('error')}")
        
except Exception as e:
    print(f"❌ EXCEPCIÓN: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
