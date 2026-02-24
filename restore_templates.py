import os
import re

source_dir = r"e:\PILi_Quarts\DOCUMENTOS TESIS"
target_dir = r"e:\PILi_Quarts\PILi_Quarts_V3.0\backend\modules\N04_Binary_Factory\templates\html"

templates = [
    "PLANTILLA_HTML_COTIZACION_COMPLEJA.html",
    "PLANTILLA_HTML_COTIZACION_SIMPLE.html",
    "PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html",
    "PLANTILLA_HTML_INFORME_TECNICO.html",
    "PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html",
    "PLANTILLA_HTML_PROYECTO_SIMPLE.html"
]

def standardize_placeholders(content):
    # Regex to find {{ PLACEHOLDER }} or {{PLACEHOLDER}}
    # We want to capture the name and standardize to {{ name }}
    pattern = r"{{\s*([A-Za-z0-9_]+)\s*}}"
    def replacer(match):
        placeholder = match.group(1).lower()
        return f"{{{{ {placeholder} }}}}"
    
    return re.sub(pattern, replacer, content)

results = []

for template in templates:
    source_path = os.path.join(source_dir, template)
    target_path = os.path.join(target_dir, template)
    
    if os.path.exists(source_path):
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            standardized_content = standardize_placeholders(content)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(standardized_content)
            results.append(f"SUCCESS: {template}")
        except Exception as e:
            results.append(f"ERROR: {template} - {str(e)}")
    else:
        results.append(f"NOT_FOUND: {template}")

for res in results:
    print(res)
