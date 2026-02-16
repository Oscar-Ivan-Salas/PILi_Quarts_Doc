import sys
import os
import logging
from pathlib import Path
from datetime import datetime
import time

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.modules.documents.service import unified_service, DocumentType, DocumentFormat

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def run_validation_matrix():
    print("\n[R.A.L.F.T.H.] INICIANDO MATRIZ DE VALIDACIÓN 6x3")
    print("==================================================")
    print("Motor Word:  python-docx (Nativo)")
    print("Motor Excel: openpyxl (Nativo)")
    print("Motor PDF:   ReportLab (Renderizado Directo)")
    print("--------------------------------------------------")

    # Datos "Gold Standard" - Usuario 001 / Cliente 001
    base_data = {
        "numero": "COT-CAMI-001",
        "codigo": "PRJ-CAMI-001",
        "fecha": datetime.now().strftime('%d/%m/%Y'),
        "valida_hasta": "15 días",
        "cliente": {
            "nombre": "Cami Salon",
            "empresa": "Cami Salon SPA",
            "email": "contacto@camisalon.com",
            "telefono": "999-123-456",
            # "RUC" is often part of empresa string or separate, key depends on implementation
            "direccion": "Av. Larco 101, Miraflores, Lima"
        },
        # Items para Cotización (Total math check: 1000 + 156.40 = 1156.40 ? No, let's make it exact)
        # User asked for Total S/ 1156.40
        # Let's say Subtotal = 980.00, IGV (18%) = 176.40 -> Total = 1156.40
        "items": [
            {"descripcion": "Servicio de Mantenimiento Eléctrico (Salón Principal)", "cantidad": 1, "precio_unitario": 500.00, "total": 500.00},
            {"descripcion": "Instalación de Luminarias LED (Zona Lavado)", "cantidad": 4, "precio_unitario": 120.00, "total": 480.00}
        ],
        "totales": {
            "subtotal": 980.00,
            "igv": 176.40,
            "total": 1156.40
        },
        "terminos": "Pago 50% al inicio, 50% al finalizar. Garantía de 12 meses.",
        # Data for Projects/Reports
        "proposito": "Mejorar la iluminación y seguridad eléctrica del local.",
        "objetivos": "1. Reducir consumo energético.\n2. Cumplir normativa INDECI.",
        "alcance": "Tableros eléctricos, cableado estructurado, iluminación LED.",
        "supuestos": "Acceso permitido en horario nocturno.",
        "spi": 1.0, "cpi": 1.0, "ev": 5000, "ac": 4800, "pv": 5000, "bac": 10000,
        "conclusiones": "El sistema eléctrico cumple con los estándares de seguridad.",
        "recomendaciones": "Realizar mantenimiento preventivo cada 6 meses."
    }

    # Matrix Definition
    doc_types = [
        ("Cotización Simple", DocumentType.COTIZACION_SIMPLE),
        ("Cotización Compleja", DocumentType.COTIZACION_COMPLEJA),
        ("Proyecto Simple", DocumentType.PROYECTO_SIMPLE),
        ("Proyecto Complejo", DocumentType.PROYECTO_COMPLEJO),
        ("Informe Técnico", DocumentType.INFORME_TECNICO),
        ("Informe Ejecutivo", DocumentType.INFORME_EJECUTIVO)
    ]

    formats = [
        ("WORD", DocumentFormat.WORD),
        ("EXCEL", DocumentFormat.EXCEL),
        ("PDF", DocumentFormat.PDF)
    ]

    results = []
    
    total_ops = len(doc_types) * len(formats)
    current_op = 0

    print(f"{'DOCUMENTO':<25} | {'FMT':<6} | {'ESTADO':<10} | {'ARCHIVO':<40} | {'COMENTARIO'}")
    print("-" * 110)

    success_count = 0

    for doc_name, doc_type in doc_types:
        for fmt_name, fmt in formats:
            current_op += 1
            # Simulate slight delay for "processing" feel and avoid file lock race conditions
            # time.sleep(0.1) 
            
            try:
                # Generate
                path = unified_service.generate(doc_type, fmt, base_data)
                
                # Check
                file_path = Path(path)
                if file_path.exists() and file_path.stat().st_size > 1000: # > 1KB
                    status = "✅ OK"
                    comment = "Generado Correctamente"
                    success_count += 1
                else:
                    status = "❌ FAIL"
                    comment = "Archivo vacío o no encontrado"
                
                print(f"{doc_name:<25} | {fmt_name:<6} | {status:<10} | {file_path.name:<40} | {comment}")
                
            except Exception as e:
                print(f"{doc_name:<25} | {fmt_name:<6} | {'❌ ERR':<10} | {'---':<40} | {str(e)[:30]}")

    print("-" * 110)
    print(f"\n[RESUMEN] Generados: {success_count}/{total_ops}")
    
    if success_count == total_ops:
        print("[CERTIFICADO] MATRIZ 6x3 COMPLETADA. ESPECIFICACIÓN R.A.L.F.T.H. CUMPLIDA.")
        return 0
    else:
        print("[ALERTA] LA MATRIZ PRESENTA FALLOS.")
        return 1

if __name__ == "__main__":
    sys.exit(run_validation_matrix())
