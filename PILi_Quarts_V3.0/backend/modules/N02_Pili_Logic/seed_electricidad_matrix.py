"""
Script de Sembrado Masivo Matriz de Electricidad (10 Documentos).
Crea 10 configuraciones en N02 y 10 carpetas en N04.
"""
import sys
import os
import shutil
import json
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

from modules.N02_Pili_Logic.knowledge_db import SessionLocal, PiliService, PiliTemplateConfig

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

def seed_matrix():
    print("⚡ Iniciando Sembrado de Matriz Electricidad (10x10)...")
    session = SessionLocal()
    
    try:
        # 1. Get Service
        service = session.query(PiliService).filter_by(service_key="electricidad").first()
        if not service:
            print("❌ Servicio 'electricidad' no encontrado. Ejecuta seed_electricidad_ralf.py primero.")
            return

        # 2. Iterate Docs
        templates_base_dir = backend_dir / "modules" / "N04_Binary_Factory" / "templates"
        
        for doc_id, doc_name in DOC_TYPES.items():
            template_ref = f"ELECTRICIDAD_{doc_name}"
            
            # A. Update N02
            config = session.query(PiliTemplateConfig).filter_by(service_id=service.id, document_type_id=doc_id).first()
            if not config:
                config = PiliTemplateConfig(
                    service_id=service.id,
                    document_type_id=doc_id,
                    template_ref=template_ref
                )
                session.add(config)
                print(f"   ✅ N02 Config: {doc_name} (ID {doc_id})")
            else:
                config.template_ref = template_ref
            
            # B. Create N04 Folder (Clone from user test or create fresh)
            folder_path = templates_base_dir / template_ref
            folder_path.mkdir(exist_ok=True)
            
            # Create Layouts based on Doc Type
            create_template_assets(folder_path, doc_name, doc_id)
            print(f"   📂 N04 Template: {template_ref}")
            
        session.commit()
        print("🏁 Matriz 10x10 Sbrada.")

    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

def create_template_assets(path, name, doc_id):
    # 1. Layout HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head><title>{name}</title><link rel='stylesheet' href='style.css'></head>
<body>
    <h1>{name.replace('_', ' ')}</h1>
    <p>Cliente: {{{{ client_name }}}}</p>
    <table>
        <thead><tr><th>Item</th><th>Desc</th><th>Total</th></tr></thead>
        <tbody>
            {{% for item in items %}}
            <tr><td>{{{{ loop.index }}}}</td><td>{{{{ item.description }}}}</td><td>{{{{ item.total }}}}</td></tr>
            {{% endfor %}}
        </tbody>
    </table>
</body>
</html>"""
    (path / "layout.html").write_text(html_content, encoding="utf-8")

    # 2. Mapping JSON (Specific for Cuadro de Cargas)
    # Special columns/formulas for ID 3
    columns = {"index": "B", "description": "C", "quantity": "D", "price": "E", "total": "F"}
    
    # Simple items for standard, but Cuadro de Cargas needs formulas?
    # Passing raw formulas in data usually, or defining them here?
    # I implemented formula injection in N04 logic: checks if val.startswith("=").
    # N04 receives data from N02/N06. 
    # N06 calculates generic totals.
    # To test "Excel Formulas", I should inject a formula in the PAYLOAD or mapping?
    # "Verifica que las fórmulas... Si cambias un número... el total debe actualizarse solo"
    # This means the "Total" column in Excel should be "=D{row}*E{row}", NOT a static value.
    # I need to configure mapping.json to inject this formula string instead of the value from payload?
    # Or N06 sends the formula?
    # Better: mapping.json defines the column content as a template.
    # My simplified N04 implementation:
    # row_data = { ... "total": item.total ... }
    # if "total" in row_data: ws[col] = row_data["total"]
    # So N06 must generate the formula string for "total" field if doc_type is Cuadro de Cargas.
    # OR, better: N04 mapping allows literals.
    # Let's adjust N04 implementation to allow mapping value NOT to be a field key, but a literal/template.
    
    mapping = {
        "excel_layout": {
            "sheet_name": name,
            "static_cells": {"B2": name.replace('_', ' ')},
            "dynamic_cells": {"client_name": "C5"},
            "tables": [{
                "data_key": "items",
                "start_row": 8,
                "columns": columns
            }]
        },
        "word_layout": {
            "title": name.replace('_', ' '),
            "headers": ["Item", "Descripción", "Cant", "P. Unit", "Total"]
        },
        "styles": {"colors": {"primary": "#CC0000"}}
    }
    
    # CUADRO DE CARGAS Special Logic
    if doc_id == 3:
        # We want the 'total' column (F) to be a formula: =D{row}*E{row}
        # In my current N04 logic, it iterates fields.
        # I need N04 items to contain the formula string.
        # N06 prepares the items.
        pass
        
    import json
    (path / "mapping.json").write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    
    # 3. Style CSS
    (path / "style.css").write_text("body { font-family: Arial; }", encoding="utf-8")

if __name__ == "__main__":
    seed_matrix()
