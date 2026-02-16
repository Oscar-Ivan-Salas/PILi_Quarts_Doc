import sys
import os
import logging
from pathlib import Path
import time

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.modules.documents.service import unified_service, DocumentType, DocumentFormat

# Configure logging
logging.basicConfig(level=logging.INFO)
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

def test_6x3_matrix():
    print("🚀 INICIANDO VERIFICACIÓN MATRIZ 6x3 (18 DOCUMENTOS)...")
    
    success_count = 0
    total_tests = 0
    errors = []

    # Datos Dummy Genéricos
    base_data = {
        "numero": "TEST-6x3-001",
        "codigo": "PROJ-6x3-001",
        "nombre": "Proyecto Matriz 6x3",
        "titulo": "Informe Matriz 6x3",
        "cliente": {
            "nombre": "Cliente Matrix",
            "empresa": "Matrix Corp",
            "email": "neo@matrix.com"
        },
        "items": [
            {"descripcion": "Item Prueba 1", "cantidad": 10, "precio_unitario": 100, "subtotal": 1000},
            {"descripcion": "Item Prueba 2", "cantidad": 5, "precio_unitario": 200, "subtotal": 1000}
        ],
        "totales": {"subtotal": 2000, "iva": 360, "total": 2360},
        "secciones": [{"titulo": "Intro", "contenido": "Contenido de prueba."}],
        "presupuesto": 100000,
        "roi": 15,
        "duracion_total": "90 días"
    }

    for doc_type in DOC_TYPES:
        print(f"\n📂 Tipo: {doc_type.value}")
        for fmt in FORMATS:
            total_tests += 1
            try:
                print(f"   👉 Generando {fmt.value}...", end="")
                path = unified_service.generate(doc_type, fmt, base_data)
                
                if Path(path).exists() and Path(path).stat().st_size > 0:
                    print(f" ✅ OK ({Path(path).name})")
                    success_count += 1
                else:
                    print(f" ❌ FALLÓ (Archivo vacío o no existe)")
                    errors.append(f"{doc_type.value} - {fmt.value}: Archivo inválido")
                    
            except Exception as e:
                print(f" ❌ ERROR: {str(e)}")
                errors.append(f"{doc_type.value} - {fmt.value}: {str(e)}")

    print("\n📊 RESULTADOS FINAL MATRIZ 6x3:")
    print(f"   ✅ Éxitos: {success_count} / {total_tests}")
    
    if errors:
        print("\n❌ ERRORES ENCONTRADOS:")
        for err in errors:
            print(f"   - {err}")
    else:
        print("\n✨ ¡MATRIZ 100% OPERATIVA! ✨")

if __name__ == "__main__":
    test_6x3_matrix()
