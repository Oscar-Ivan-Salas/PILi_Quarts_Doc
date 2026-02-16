
import sys
import os
import logging
from datetime import datetime
from pathlib import Path

# Add CWD to path
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LegacyVerifierAll")

try:
    from app.services.generators.cotizacion_compleja_generator import generar_cotizacion_compleja
    from app.services.generators.cotizacion_simple_generator import generar_cotizacion_simple
    from app.services.generators.proyecto_simple_generator import generar_proyecto_simple
    from app.services.generators.proyecto_complejo_pmi_generator import generar_proyecto_complejo_pmi
    from app.services.generators.informe_tecnico_generator import generar_informe_tecnico
    from app.services.generators.informe_ejecutivo_apa_generator import generar_informe_ejecutivo_apa
    from app.services.pdf_generator_v2 import pdf_generator_v2
except ImportError as e:
    logger.error(f"❌ Import Error: {e}")
    sys.exit(1)

def verify_all():
    output_dir = os.path.join(os.getcwd(), 'legacy_test_output')
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%H%M%S")
    
    # Common Data
    base_data = {
        "cliente": "Cliente de Prueba S.A.C.",
        "proyecto": "Proyecto de Verificación Legacy",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "codigo": f"TEST-{timestamp}",
        "items": [
             {"descripcion": "Item de Prueba 1", "cantidad": 10, "precio": 100, "precio_unitario": 100, "total": 1000},
             {"descripcion": "Item de Prueba 2", "cantidad": 5, "precio": 200, "precio_unitario": 200, "total": 1000}
        ]
    }

    tests = [
        ("Cotizacion_Compleja", generar_cotizacion_compleja, base_data),
        ("Cotizacion_Simple", generar_cotizacion_simple, base_data),
        ("Proyecto_Simple", generar_proyecto_simple, base_data),
        ("Proyecto_Complejo", generar_proyecto_complejo_pmi, base_data),
        ("Informe_Tecnico", generar_informe_tecnico, base_data),
        ("Informe_Ejecutivo", generar_informe_ejecutivo_apa, base_data),
    ]

    results = []

    for name, generator_func, data in tests:
        logger.info(f"🔄 Testing {name}...")
        word_path = os.path.join(output_dir, f"{name}_{timestamp}.docx")
        try:
            # Generate DOCX
            final_word = generator_func(data, word_path, {})
            logger.info(f"  ✅ DOCX: {os.path.basename(final_word)}")
            
            # Generate PDF
            final_pdf = pdf_generator_v2.convertir_word_a_pdf(Path(final_word))
            if final_pdf and final_pdf.exists():
                logger.info(f"  ✅ PDF: {final_pdf.name}")
                results.append((name, "SUCCESS", str(final_pdf)))
            else:
                logger.error(f"  ❌ PDF Failed for {name}")
                results.append((name, "PDF_FAIL", str(final_word)))
                
        except Exception as e:
            logger.error(f"  ❌ Failed {name}: {e}")
            results.append((name, "FAIL", str(e)))

    # Summary
    print("\n--- SUMMARY ---")
    for name, status, path in results:
        print(f"{name}: {status} -> {path}")

if __name__ == "__main__":
    verify_all()
