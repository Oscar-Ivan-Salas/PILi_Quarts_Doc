"""
Script de prueba de aislamiento para N04 Binary Factory.
Debe ejecutarse SIN importar nada de 'app' o 'pili.legacy'.
"""
import sys
import os
import json
import base64
from pathlib import Path

# Agregar el directorio backend al path para poder importar modules
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

try:
    from modules.N04_Binary_Factory.index import factory
    print("✅ N04 Binary Factory importado correctamente.")
except ImportError as e:
    print(f"❌ Error importando N04: {e}")
    sys.exit(1)

# Datos de prueba (Payload estricto según contrato)
test_payload = {
    "user_context": {
        "empresa_nombre": "Tesla S.A.C. (Prueba Aislamiento)",
        "empresa_ruc": "20601234567",
        "empresa_direccion": "Av. Prueba 123",
        "empresa_telefono": "999888777",
        "empresa_email": "test@tesla.com"
    },
    "document_metadata": {
        "tipo": "COTIZACION",
        "subtipo": "SIMPLE",
        "formato": "XLSX"
    },
    "payload": {
        "numero": "COT-ISOLATION-001",
        "cliente": "Cliente Aislado",
        "proyecto": "Prueba de Aislamiento N04",
        "fecha": "13/02/2026",
        "items": [
            {"descripcion": "Item 1 Aislado", "cantidad": 10, "precio_unitario": 100},
            {"descripcion": "Item 2 Aislado", "cantidad": 5, "precio_unitario": 200}
        ]
    }
}

print("\n🚀 Ejecutando factory.process_request()...")
result = factory.process_request(test_payload)

if result["success"]:
    print("✅ Generación exitosa.")
    print(f"📄 Nombre: {result['file_name']}")
    print(f"📊 Tamaño: {result['size_bytes']} bytes")
    
    # Decodificar y guardar para verificar
    output_path = f"test_isolation_{result['file_name']}"
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(result["file_base64"]))
    print(f"💾 Archivo guardado en: {output_path}")
    
else:
    print("❌ Error en generación:")
    print(result["error"])
    sys.exit(1)
