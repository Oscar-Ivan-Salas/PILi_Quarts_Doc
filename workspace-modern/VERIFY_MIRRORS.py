import sys
import os
import logging
from pathlib import Path
import time
from datetime import datetime

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.modules.documents.service import unified_service, DocumentType, DocumentFormat

# Configure logging
logger = logging.getLogger(__name__)

DOC_TYPES = [
    DocumentType.COTIZACION_SIMPLE,
    DocumentType.COTIZACION_COMPLEJA,
    DocumentType.PROYECTO_SIMPLE,
    DocumentType.PROYECTO_COMPLEJO,
    DocumentType.INFORME_TECNICO,
    DocumentType.INFORME_EJECUTIVO
]

FORMATS = [
    DocumentFormat.WORD,
    DocumentFormat.PDF,
    DocumentFormat.EXCEL
]

def verify_mirrors():
    output_lines = []
    
    def log(msg):
        print(msg)
        output_lines.append(msg)

    log(f"\n[VERIFICATION] INICIANDO PROTOCOLO DE CONFIANZA (6x3 MATRIZ)")
    log(f"FECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=========================================================================================")
    log(f"{'DOCUMENTO':<30} | {'FORMATO':<10} | {'ESTADO':<10} | {'ARCHIVO GENERADO'}")
    log("-----------------------------------------------------------------------------------------")
    
    success_count = 0
    total_tests = 0
    
    # Datos de Prueba para "Espejo" - V2 High Fidelity
    base_data = {
        "numero": "PROOF-V2-001",
        "codigo": "MIRROR-V2-001",
        "nombre": "Proyecto Espejo V2 High Fidelity",
        "titulo": "Informe de Verificacion V2",
        "lider": "System Auditor",
        "estado": "Auditando",
        "cliente": {
            "nombre": "Cliente Auditoria V2",
            "empresa": "Matrix Corp Reloaded",
            "email": "neo_v2@matrix.com"
        },
        "items": [
            {"descripcion": "Verificacion Word V2", "cantidad": 1, "precio_unitario": 200, "total": 200},
            {"descripcion": "Verificacion PDF V2", "cantidad": 1, "precio_unitario": 200, "total": 200},
            {"descripcion": "Verificacion Excel V2", "cantidad": 1, "precio_unitario": 200, "total": 200}
        ],
        "fases": [
             {"nombre": "Upgrade Excel", "rango": "Fase 1", "estado": "Completado", "resp": "Dev AI"},
             {"nombre": "Upgrade PDF", "rango": "Fase 2", "estado": "Completado", "resp": "Dev AI"},
             {"nombre": "Verification", "rango": "Fase 3", "estado": "En Proceso", "resp": "QA Bot"}
        ],
        "presupuesto": 25000,
        "roi": 35,
        "duracion_total": "45 dias",
        "subtotal": 600,
        "igv": 108,
        "total": 708
    }

    for doc_type in DOC_TYPES:
        for fmt in FORMATS:
            total_tests += 1
            status = "[WAIT]"
            filename = "N/A"
            
            try:
                path = unified_service.generate(doc_type, fmt, base_data)
                file_path = Path(path)
                
                if file_path.exists() and file_path.stat().st_size > 500: # Threshold increased for richer docs
                    status = "[OK-V2]"
                    filename = file_path.name
                    success_count += 1
                else:
                    status = "[SMALL/FAIL]"
            except Exception as e:
                import traceback
                status = "[ERROR]" 
                filename = str(e)[:30]
                log(f"\n[ERROR DETAIL] {doc_type} / {fmt}: {str(e)}")
                traceback.print_exc()
            
            # Limpiar nombre del tipo para la tabla
            type_name = doc_type.value.replace('cotizacion_', 'Cot. ').replace('proyecto_', 'Proy. ').replace('informe_', 'Inf. ').title()
            
            log(f"{type_name:<30} | {fmt.value:<10} | {status:<10} | {filename}")

    log("=========================================================================================")
    log(f"\n[RESUMEN FINAL]")
    log(f"   Total Solicitados: {total_tests}")
    log(f"   Generados Correctamente: {success_count}")
    log(f"   Tasa de Exito: {(success_count/total_tests)*100:.1f}%")
    
    result_code = 0
    if success_count == total_tests:
        log("\n[CERTIFICADO] El sistema genera los 18 documentos espejo correctamente.")
    else:
        log("\n[ALERTA] Se encontraron fallos en la generacion.")
        result_code = 1
        
    # Write to file explicitly with UTF-8 encoding
    with open('verification_results.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
        
    return result_code

if __name__ == "__main__":
    sys.exit(verify_mirrors())
