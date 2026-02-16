"""
Script de Prueba de Hipótesis R.A.L.F. (N04).
Verifica consistencia entre Excel y Word (Espejo Dinámico).
"""
import sys
import os
import logging
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("RALF_TEST")

from modules.N06_Integrator.index import integrator_node

def test_hypothesis():
    logger.info("🧪 PROYECTO R.A.L.F: Verificación de Hipótesis N04 (Espejo Dinámico)")
    
    # Input Común
    input_data = {
        "client_info": {
            "nombre": "Industrias Tester S.A.",
            "ruc": "20555555551"
        },
        "service_request": {
            "service_key": "electricidad",
            "document_model_id": 2, # Cotización Compleja -> Maps to ELECTRICIDAD_COT_COMPLEJA
            "quantity": 1
        },
        "user_context": {"user_id": "RALF_AUDITOR"}
    }
    
    # 1. Generar Excel
    logger.info("1️⃣ Generando EXCEL...")
    input_data["output_format"] = "XLSX"
    res_xlsx = integrator_node.dispatch(input_data)
    
    if not res_xlsx.get("success"):
        logger.error(f"❌ Fallo Excel: {res_xlsx.get('error')}")
        return

    # 2. Generar Word
    # Note: N06 dispatch logic I wrote in Step 6157 checks request["output_format"] override!
    # "Override format from input request if present" - Yes, I added that logic.
    logger.info("2️⃣ Generando WORD...")
    input_data["output_format"] = "DOCX"
    res_docx = integrator_node.dispatch(input_data)
     
    if not res_docx.get("success"):
        logger.error(f"❌ Fallo Word: {res_docx.get('error')}")
        return

    # 3. Comparación (Rigor Científico)
    total_xlsx = res_xlsx.get("summary", {}).get("total_cost", 0)
    total_docx = res_docx.get("summary", {}).get("total_cost", 0)
    
    logger.info(f"📊 COMPARATIVA:")
    logger.info(f"   Total Calculado (Excel Loop): {total_xlsx}")
    logger.info(f"   Total Calculado (Word Loop):  {total_docx}")
    
    diff = abs(total_xlsx - total_docx)
    if diff == 0:
        logger.info("✅ HIPÓTESIS VALIDADA: Tolerancia 0.00% cumplida.")
        logger.info("   El motor N06 garantiza consistencia matemática entre formatos.")
        
        # Guardar Archivos
        save_file(res_xlsx, "RALF_Electricidad.xlsx")
        save_file(res_docx, "RALF_Electricidad.docx")
    else:
        logger.error(f"❌ HIPÓTESIS RECHAZADA: Diferencia de {diff}")

def save_file(res, name):
    import base64
    out_dir = current_dir / "output_test"
    out_dir.mkdir(exist_ok=True)
    path = out_dir / name
    
    b64_data = res.get("document", {}).get("b64_preview")
    if b64_data:
        try:
             with open(path, "wb") as f:
                f.write(base64.b64decode(b64_data))
             logger.info(f"   💾 Archivo Guardado: {path}")
        except Exception as e:
             logger.error(f"   ❌ Error guardando archivo: {e}")
    else:
        logger.error("   ❌ No B64 data found in response")

if __name__ == "__main__":
    test_hypothesis()
