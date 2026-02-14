"""
Script de Sello Final Matriz Electricidad (30 Documentos).
"La Gran Descarga"
"""
import sys
import os
import logging
from pathlib import Path
import time

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("FINAL_SEAL")

from modules.documents.service import document_service

DOC_TYPES = {
    1: "COTIZACION_SIMPLE",
    2: "COTIZACION_COMPLEJA",
    3: "CUADRO_CARGAS",
    4: "MEMORIA_DESCRIPTIVA",
    5: "PROTOCOLO_PRUEBAS",
    6: "INFORME_LEVANTAMIENTO",
    7: "PRESUPUESTO_BASE",
    8: "CRONOGRAMA_EJECUCION",
    9: "ESPECIFICACIONES_TECNICAS",
    10: "PLAN_SEGURIDAD"
}

FORMATS = ["XLSX", "DOCX", "PDF"]

def final_seal():
    logger.info("🚀 INICIANDO 'LA GRAN DESCARGA' - SELLO FINAL ELECTRICIDAD")
    
    out_dir = current_dir / "output_seal"
    out_dir.mkdir(exist_ok=True)
    
    success_count = 0
    total_count = len(DOC_TYPES) * len(FORMATS)
    
    # User Context (Socio)
    user_context = {"user_id": "SOCIO_001", "role": "admin"}
    
    for doc_id, doc_name in DOC_TYPES.items():
        logger.info(f"📄 Procesando Modelo {doc_id}: {doc_name}")
        
        # Request Data
        req_data = {
            "client_info": {"nombre": "Cliente Final S.A.C.", "ruc": "20600000001"},
            "service_request": {
                "service_key": "electricidad",
                "document_model_id": doc_id,
                "quantity": 1
            },
            "user_context": user_context
        }
        
        # Inject Formula Data for Cuadro de Cargas
        if doc_id == 3:
             # N02/N06 logic usually handles this, but here we can mock advanced input if needed.
             # N04 receives "items". We rely on N06 to package it.
             # N04 Index with our formula patch will check for "=" strings.
             # But N06 calculates values.
             # How to inject "=" string into N04?
             # N06 logic: n04_items.append({ ... "total": item_total ... })
             # We need N06 to pass the formula string IF it knows it's a formula.
             # Or we cheat for the test and send a specific item description that triggers it?
             # No, N04 looks at the VALUE.
             # Since N06 calculates "total" as a float (subtotal += item_total), it sends a number.
             # To test formula, we need N06 to send a STRING starting with "=".
             # I can hack N06 or N04?
             # Better: Update Seed Matrix (mapping.json) to set 'total': '=...' in STATIC cells?
             # No, user wants dynamic table formulas.
             # Let's trust the "Universal Formula Engine" I built in N04 allows it IF the data comes in as string.
             # For this test, I will assume N06 sends calculated values, BUT...
             # The user requirement: "Verifica que las fórmulas... Si cambias un número... el total debe actualizarse solo"
             # This implies the Excel cell MUST HAVE A FORMULA.
             # So N04 MUST write a formula.
             # Current N04 logic: if value starts with "=", write as formula.
             # But N06 sends floats.
             # I'll update N06 to send formula string for specific DocType?
             # OR, simply rely on the fact that I CAN implement it later?
             # User says "Presenta el Log de éxito y la confirmación de que las fórmulas... están activas".
             # I MUST make it work.
             # I will modify N06 (Integrator) to check if doc_type == 3 (Cuadro Cargas) and force "total": "=PRODUCT(D{row},E{row})" string.
             pass

        for fmt in FORMATS:
            req_data["output_format"] = fmt
            
            res = document_service.generate_document(req_data)
            
            if res.get("success"):
                fname = f"{doc_name}.{fmt.lower()}"
                save_file(res, out_dir / fname)
                success_count += 1
            else:
                logger.error(f"   ❌ Fallo {fmt}: {res.get('error')}")

    logger.info(f"🏁 SELLO FINAL: {success_count}/{total_count} Archivos Generados.")

def save_file(res, path):
    import base64
    b64_data = res.get("document", {}).get("b64_preview")
    if b64_data:
        try:
             with open(path, "wb") as f:
                f.write(base64.b64decode(b64_data))
        except Exception as e:
             logger.error(f"   ❌ Error guardando: {e}")

if __name__ == "__main__":
    final_seal()
