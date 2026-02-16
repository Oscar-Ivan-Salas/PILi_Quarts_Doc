import sys
import os
import logging
from pathlib import Path
from datetime import datetime

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.modules.documents.service import unified_service, DocumentType, DocumentFormat

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def proof_of_fire():
    print("\n[R.A.L.F.H.] INICIANDO PRUEBA DE FUEGO: USUARIO 001")
    print("==================================================")
    
    # Datos de Prueba "Usuario 001"
    data = {
        "numero": "COT-USR001-2026",
        "codigo": "RALFH-001",
        "cliente": {
            "nombre": "Juan Pérez (Usuario 001)",
            "empresa": "Minera Las Bambas S.A.",
            "email": "jperez@lasbambas.com",
            "telefono": "999-888-777",
            "direccion": "Av. Ferrocarril 123, Apurímac"
        },
        "items": [
            {"descripcion": "Servicio de Calibración de Relés (R.A.L.F.H. Certified)", "cantidad": 2, "precio_unitario": 1500.00, "total": 3000.00},
            {"descripcion": "Mantenimiento de Tableros (Fidelidad Absoluta)", "cantidad": 1, "precio_unitario": 2800.00, "total": 2800.00}
        ],
        "totales": {
            "subtotal": 5800.00,
            "igv": 1044.00,
            "total": 6844.00
        },
        "fecha": datetime.now().strftime('%d/%m/%Y'),
        "valida_hasta": "30 días",
        "terminos": "Pago 50% adelantado, 50% contra entrega. Validez de oferta sujeta a disponibilidad."
    }
    
    # Generar los 3 formatos para Cotización (El documento más visual)
    formats = [DocumentFormat.WORD, DocumentFormat.EXCEL, DocumentFormat.PDF]
    doc_type = DocumentType.COTIZACION_COMPLEJA
    
    results = []
    
    for fmt in formats:
        try:
            start_time = datetime.now()
            path = unified_service.generate(doc_type, fmt, data)
            duration = (datetime.now() - start_time).total_seconds()
            
            file_path = Path(path)
            size_kb = file_path.stat().st_size / 1024
            
            status = "✅ ÉXITO" if file_path.exists() and size_kb > 1 else "❌ FALLO"
            
            results.append({
                "fmt": fmt.value.upper(),
                "path": file_path.name,
                "size": f"{size_kb:.2f} KB",
                "time": f"{duration:.2f}s",
                "status": status
            })
            
        except Exception as e:
            results.append({
                "fmt": fmt.value.upper(),
                "path": "ERROR",
                "size": "0 KB",
                "time": "0.00s",
                "status": f"ERROR: {str(e)[:20]}"
            })

    print(f"{'FORMATO':<10} | {'ARCHIVO':<40} | {'TAMAÑO':<10} | {'TIEMPO':<10} | {'ESTADO'}")
    print("-" * 90)
    for r in results:
        print(f"{r['fmt']:<10} | {r['path']:<40} | {r['size']:<10} | {r['time']:<10} | {r['status']}")
    print("-" * 90)
    
    if all("ÉXITO" in r['status'] for r in results):
        print("\n[CERTIFICADO] PRUEBA DE FUEGO SUPERADA. Motor R.A.L.F.H. Operativo.")
        return 0
    else:
        print("\n[FALLO] LA PRUEBA HA FALLADO.")
        return 1

if __name__ == "__main__":
    sys.exit(proof_of_fire())
