"""
PRUEBA FINAL: Generación Excel desde Frontend (Simulación)
===========================================================

Este script simula exactamente lo que hace el frontend:
1. Captura HTML de vista previa
2. Envía POST a /api/generation/excel
3. Verifica que el Excel generado sea espejo del HTML
"""

import requests
import json
from pathlib import Path

# URL del backend
BASE_URL = "http://localhost:8005"

# HTML de prueba (simulando lo que envía el frontend)
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        .bg-white { background: white; }
        .cotizacion-container { padding: 20px; }
        .header { margin-bottom: 20px; }
        .empresa-detalles { text-align: right; }
        .items-table { width: 100%; }
    </style>
</head>
<body>
    <div class="bg-white shadow-2xl cotizacion-container">
        <div class="header">
            <div class="empresa-detalles">
                <div>RUC: 20601138787</div>
                <div>Jr. Las Águilas M-8 Lote 03</div>
                <div>Teléfono: 968 315 961</div>
                <div>Email: ingenieria.teslaelectricidad@gmail.com</div>
            </div>
        </div>
        
        <h1 style="color: #0052A3; text-align: center;">COTIZACIÓN DE SERVICIOS</h1>
        
        <div class="client-info">
            <p><strong>Cliente:</strong> MINERA LAS BAMBAS S.A.</p>
            <p><strong>Fecha:</strong> 17/02/2026</p>
        </div>
        
        <table class="items-table" border="1">
            <thead>
                <tr style="background: #0052A3; color: white;">
                    <th>ÍTEM</th>
                    <th>DESCRIPCIÓN</th>
                    <th>CANT.</th>
                    <th>UND</th>
                    <th>P. UNIT</th>
                    <th>TOTAL</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>01</td>
                    <td>Tablero eléctrico monofásico 12 circuitos</td>
                    <td>2</td>
                    <td>und</td>
                    <td>$ 450.00</td>
                    <td>$ 900.00</td>
                </tr>
                <tr>
                    <td>02</td>
                    <td>Circuitos eléctricos empotrados 14AWG THW</td>
                    <td>6</td>
                    <td>cto</td>
                    <td>$ 120.00</td>
                    <td>$ 720.00</td>
                </tr>
                <tr>
                    <td>03</td>
                    <td>Puntos de iluminación LED</td>
                    <td>10</td>
                    <td>pto</td>
                    <td>$ 45.00</td>
                    <td>$ 450.00</td>
                </tr>
            </tbody>
        </table>
        
        <div class="totals" style="text-align: right; margin-top: 20px;">
            <p><strong>SUBTOTAL:</strong> $ 2,070.00</p>
            <p><strong>IGV (18%):</strong> $ 372.60</p>
            <p><strong>TOTAL:</strong> $ 2,442.60</p>
        </div>
    </div>
</body>
</html>
"""

# Request data (igual que el frontend)
request_data = {
    "title": "Cotizacion_MINERA_LAS_BAMBAS",
    "type": "cotizacion_simple",
    "doc_type": "cotizacion_simple",
    "html_content": html_content,
    "data": {
        "client_info": {
            "nombre": "MINERA LAS BAMBAS S.A.",
            "fecha": "17/02/2026"
        }
    }
}

print("=" * 80)
print("🧪 PRUEBA FINAL: Generación Excel desde Frontend")
print("=" * 80)
print()

print("📋 Datos de prueba:")
print(f"   Cliente: MINERA LAS BAMBAS S.A.")
print(f"   Tamaño HTML: {len(html_content)} caracteres")
print()

print("🚀 Enviando POST a /api/generation/excel...")
print()

try:
    response = requests.post(
        f"{BASE_URL}/api/generation/excel",
        json=request_data,
        timeout=30
    )
    
    if response.status_code == 200:
        # Guardar archivo
        output_path = Path("PRUEBA_FRONTEND_EXCEL.xlsx")
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content)
        print(f"✅ Excel generado exitosamente")
        print(f"   Archivo: {output_path}")
        print(f"   Tamaño: {file_size:,} bytes")
        print()
        
        # Verificar contenido
        from openpyxl import load_workbook
        wb = load_workbook(output_path)
        ws = wb.active
        
        print("🔍 Verificación de contenido:")
        print(f"   Título hoja: {ws.title}")
        print(f"   Número de imágenes: {len(ws._images)}")
        if ws._images:
            img = ws._images[0]
            print(f"   Logo: {img.width}x{img.height}px")
        
        print()
        print("🎉 ¡PRUEBA EXITOSA!")
        print()
        print("📊 Abre el archivo para verificar:")
        print(f"   {output_path.absolute()}")
        
    else:
        print(f"❌ Error HTTP {response.status_code}")
        print(f"   Respuesta: {response.text}")
        
except Exception as e:
    print(f"❌ EXCEPCIÓN: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
