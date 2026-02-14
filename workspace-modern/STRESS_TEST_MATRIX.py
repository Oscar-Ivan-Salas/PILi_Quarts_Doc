import sys
import os
import logging
from pathlib import Path
from datetime import datetime
import time

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.modules.N08_User_Management.identity_db import SessionLocal, ProyectoActivo, UsuarioEjecutor, ClienteFinal
from backend.modules.documents.service import unified_service, DocumentType, DocumentFormat

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_stress_test():
    print("🚀 INICIANDO EJECUCIÓN MATRIZ DE ESTRÉS (DOC GENERATION)...")
    
    session = SessionLocal()
    projects = session.query(ProyectoActivo).all()
    
    total_projects = len(projects)
    print(f"📊 Total Proyectos a Procesar: {total_projects}")
    
    success_count = 0
    error_count = 0
    start_time = time.time()
    
    for idx, project in enumerate(projects, 1):
        try:
            # 1. Prepare Data from DB (simulate N06 Integrator logic)
            ejecutor = project.ejecutor
            cliente = project.cliente
            
            # Map DB Type to DocumentType
            # Simply use generic types for stress test
            doc_type_map = {
                1: DocumentType.COTIZACION_SIMPLE,
                2: DocumentType.COTIZACION_COMPLEJA,
                3: DocumentType.PROYECTO_SIMPLE,
                4: DocumentType.PROYECTO_COMPLEJO,
                5: DocumentType.INFORME_TECNICO,
                6: DocumentType.INFORME_EJECUTIVO
            }
            # Fallback modulo 6 to ensure valid type
            doc_type = doc_type_map.get((project.document_type_id % 6) + 1, DocumentType.COTIZACION_COMPLEJA)
            
            # Construct Payload
            data = {
                "numero": project.project_code,
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "valida_hasta": "30 días",
                "cliente": {
                    "nombre": cliente.persona_contacto,
                    "empresa": cliente.razon_social,
                    "email": "cliente@test.com",
                    "telefono": "555-0000",
                    "direccion": cliente.direccion
                },
                "items": [
                     {"descripcion": f"Servicio Matriz {project.service_id}", "cantidad": 1, "precio_unitario": 2500.00, "subtotal": 2500.00},
                     {"descripcion": "Insumos Varios", "cantidad": 2, "precio_unitario": 500.00, "subtotal": 1000.00}
                ],
                "totales": {
                    "subtotal": 3500.00,
                    "iva": 560.00,
                    "total": 4060.00
                },
                "terminos": "Condiciones estándar de prueba de estrés.",
                "empresa_nombre": ejecutor.nombre_completo, # Using User Name as Company Name for Exec
                "empresa_contacto": "contacto@stress-test.com"
            }
            
            # 2. Generate WORD
            print(f"[{idx}/{total_projects}] Generando {doc_type.value} para {project.project_code}...")
            unified_service.generate(doc_type, DocumentFormat.WORD, data)
            
            # 3. Generate PDF (Simulated)
            # unified_service.generate(doc_type, DocumentFormat.PDF, data)
            
            success_count += 1
            
        except Exception as e:
            logger.error(f"❌ Error en Proyecto {project.project_code}: {e}")
            error_count += 1
            
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n✅ EJECUCIÓN FINALIZADA")
    print(f"   ⏱️ Duración: {duration:.2f} segundos")
    print(f"   ✅ Éxitos: {success_count}")
    print(f"   ❌ Errores: {error_count}")
    print(f"   ⚡ Velocidad: {total_projects/duration:.2f} docs/seg")

if __name__ == "__main__":
    run_stress_test()
