
import zipfile
import re
from pathlib import Path

master_path = Path("e:/PILi_Quarts/PILi_Quarts_V3.0/backend/modules/N04_Binary_Factory/templates/word_masters/master_cotizacion_compleja.docx")

if master_path.exists():
    with zipfile.ZipFile(master_path, 'r') as z:
        content = z.read('word/document.xml').decode('utf-8')
        tags = re.findall(r'\{\{.*?\}\}', content)
        print("TAGS DETECTADOS:")
        for t in sorted(list(set(tags))):
            print(t)
else:
    print("Master no encontrado.")
