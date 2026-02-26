
import requests
import json
from datetime import datetime
from pathlib import Path

# Configuración Soberana
API_BASE = "http://localhost:8004/api/studio/generate"
OUTPUT_DIR = Path("e:/PILi_Quarts/PILi_Quarts_V3.0/backend/modules/N04_Binary_Factory/output_test")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Datos de Prueba (Mock para RALFTH)
datos_base = {
    "numero": "AUD-2026-X01",
    "cliente": "CLIENTE AUDITORIA S.A.C.",
    "proyecto": "PROYECTO DE CERTIFICACION RALFTH",
    "fecha": datetime.now().strftime("%d/%m/%Y"),
    "items": [
        {"descripcion": "AUDITORIA DE SISTEMAS", "cantidad": 1, "unidad": "und", "precio_unitario": 5000.0, "total": 5000.0},
        {"descripcion": "CERTIFICACION DE CALIDAD", "cantidad": 1, "unidad": "srv", "precio_unitario": 2500.0, "total": 2500.0}
    ],
    "subtotal": 7500.0,
    "igv": 1350.0,
    "total": 8850.0
}

config_personalizacion = {
    "esquemaColores": "#0052A3",
    "logoBase64": None
}

tipos_doc = [
    "COTIZACION SIMPLE",
    "COTIZACION COMPLEJA",
    "PROYECTO SIMPLE",
    "PROYECTO COMPLEJO",
    "INFORME TECNICO",
    "INFORME EJECUTIVO"
]

formatos = ["word", "excel", "pdf"]

def test_generation():
    print("="*60)
    print("🔱 INICIANDO AUDITORIA SOBERANA N04 - RALFTH V10")
    print("="*60)
    
    total = 0
    passed = 0
    
    for doc in tipos_doc:
        for fmt in formatos:
            total += 1
            payload = {
                "html": f"<html><body><h1>{doc}</h1><table><tr><td>Item</td><td>Cant</td><td>PU</td><td>Total</td></tr><tr><td>TEST</td><td>1</td><td>100</td><td>100</td></tr></table></body></html>",
                "format": fmt,
                "name": doc,
                "settings": config_personalizacion
            }
            
            try:
                print(f"Testing {doc} [{fmt}]...", end=" ", flush=True)
                res = requests.post(API_BASE, json=payload, timeout=30)
                if res.status_code == 200:
                    ext = "docx" if fmt == "word" else fmt
                    out_path = OUTPUT_DIR / f"{doc.replace(' ', '_')}.{ext}"
                    with open(out_path, "wb") as f:
                        f.write(res.content)
                    print("✅ OK")
                    passed += 1
                else:
                    print(f"❌ FAIL ({res.status_code})")
                    print(f"   Error: {res.text[:100]}")
            except Exception as e:
                print(f"💥 ERROR: {str(e)}")
                
    print("="*60)
    print(f"📊 RESUMEN: {passed}/{total} PASARON LA PRUEBA")
    print("="*60)

if __name__ == "__main__":
    test_generation()
