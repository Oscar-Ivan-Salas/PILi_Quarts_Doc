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

def regenerate_projects_reports():
    # Datos "Gold Standard" - Usuario 001 / Cliente 001
    base_data = {
        "numero": "PRJ-INF-REGEN-001",
        "codigo": "RALFH-REGEN",
        "fecha": datetime.now().strftime('%d/%m/%Y'),
        "valida_hasta": "15 días",
        "cliente": {
            "nombre": "Cami Salon (Regeneración)",
            "empresa": "Cami Salon SPA",
            "email": "contacto@camisalon.com",
            "telefono": "999-123-456",
            "direccion": "Av. Larco 101, Miraflores, Lima"
        },
        "proposito": "Mejorar la iluminación y seguridad eléctrica del local.",
        "evaluacion": "El sistema actual presenta riesgos de corto circuito.", # For Reports
        "objetivos": "1. Reducir consumo energético.\n2. Cumplir normativa INDECI.",
        "alcance": "Tableros eléctricos, cableado estructurado, iluminación LED.",
        "supuestos": "Acceso permitido en horario nocturno.",
        # FIX: Riesgos must be list of dicts (supersect of keys for Word/PDF)
        "riesgos": [
            {
                "descripcion": "Retrasos en materiales", "desc": "Retrasos Materiales",
                "probabilidad": "Media", "prob": "Media",
                "impacto": "Alto", "imp": "Alto",
                "mitigacion": "Compra local", "estr": "Mitigar"
            }
        ],
        # FIX: Cronograma must be dict
        "cronograma": {
            "duracion_total": "3 Semanas",
            "fecha_inicio": "01/03/2026",
            "fecha_fin": "21/03/2026"
        },
        "duracion_total": "3 Semanas", # Fallback
        "spi": 1.0, "cpi": 1.0, "ev": 5000, "ac": 4800, "pv": 5000, "bac": 10000,
        "conclusiones": "El sistema eléctrico cumple con los estándares de seguridad.",
        "recomendaciones": "Realizar mantenimiento preventivo cada 6 meses."
    }

    # Only Projects and Reports
    doc_types = [
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

    with open("regen_report.txt", "w", encoding="utf-8") as f:
        f.write("[R.A.L.F.H.] REGENERANDO PROYECTOS E INFORMES (TARGET: 12 ARCHIVOS)\n")
        f.write("===================================================================\n")

        generated_files = []

        f.write(f"{'DOCUMENTO':<25} | {'FMT':<6} | {'ESTADO':<10} | {'ARCHIVO':<40}\n")
        f.write("-" * 90 + "\n")

        for doc_name, doc_type in doc_types:
            for fmt_name, fmt in formats:
                try:
                    # Generate
                    path = unified_service.generate(doc_type, fmt, base_data)
                    file_path = Path(path)
                    
                    if file_path.exists() and file_path.stat().st_size > 1000:
                        status = "[OK]"
                        generated_files.append(file_path.absolute())
                    else:
                        status = "[FAIL]"
                    
                    f.write(f"{doc_name:<25} | {fmt_name:<6} | {status:<10} | {file_path.name:<40}\n")
                    print(f"{doc_name} {fmt_name}: {status}") # Console echo
                    
                except Exception as e:
                    f.write(f"{doc_name:<25} | {fmt_name:<6} | {'[ERR]':<10} | {str(e)[:30]}\n")
                    print(f"{doc_name} {fmt_name}: [ERR] {e}")

        f.write("-" * 90 + "\n")
        f.write(f"Total Generados: {len(generated_files)}/12\n")

        if len(generated_files) == 12:
            return 0
        else:
            return 1

if __name__ == "__main__":
    sys.exit(regenerate_projects_reports())
