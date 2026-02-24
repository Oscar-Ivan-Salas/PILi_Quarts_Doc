
from docxtpl import DocxTemplate
from pathlib import Path

master_path = Path("e:/PILi_Quarts/PILi_Quarts_V3.0/backend/modules/N04_Binary_Factory/templates/word_masters/master_cotizacion_compleja.docx")

if master_path.exists():
    doc = DocxTemplate(str(master_path))
    tags = doc.get_undeclared_template_variables()
    print("TAGS ENCONTRADOS EN EL MASTER:")
    print(sorted(list(tags)))
else:
    print(f"No se encontró el master en {master_path}")
