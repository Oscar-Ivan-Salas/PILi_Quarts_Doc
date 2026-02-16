"""
Script de prueba para generar documento Excel
"""
import requests
import json

# Datos de prueba para cotización simple
data = {
    "document_type": "cotizacion_simple",
    "format": "xlsx",
    "data": {
        "numero": "COT-2026-001",
        "cliente": "Empresa Demo SAC",
        "proyecto": "Instalación Eléctrica Industrial",
        "fecha": "13/02/2026",
        "vigencia": "30 días",
        "servicio": "Instalaciones Eléctricas",
        "area_m2": "500",
        "items": [
            {
                "descripcion": "Cableado eléctrico",
                "cantidad": 100,
                "unidad": "m",
                "precio_unitario": 15.50
            },
            {
                "descripcion": "Tomacorrientes dobles",
                "cantidad": 20,
                "unidad": "und",
                "precio_unitario": 25.00
            },
            {
                "descripcion": "Interruptores",
                "cantidad": 15,
                "unidad": "und",
                "precio_unitario": 18.50
            }
        ]
    },
    "options": {
        "esquema_colores": "azul-tesla"
    }
}

print("🚀 Generando documento Excel...")
print(f"Endpoint: http://localhost:8005/api/documents/generate")
print(f"Tipo: {data['document_type']}")
print(f"Formato: {data['format']}")

try:
    response = requests.post(
        "http://localhost:8005/api/documents/generate",
        json=data,
        timeout=30
    )
    
    if response.status_code == 200:
        # Guardar archivo
        filename = "test_cotizacion_simple.xlsx"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Documento generado exitosamente: {filename}")
        print(f"📊 Tamaño: {len(response.content)} bytes")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Respuesta: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
