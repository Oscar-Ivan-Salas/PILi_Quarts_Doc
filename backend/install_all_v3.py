import os

req_path = r'd:\PILi_Quarts\PILi_Quarts_V3.0\backend\requirements.txt'
with open(req_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = [l for l in lines if 'google-generativeai' not in l and 'google-api-core' not in l]

new_req_path = r'd:\PILi_Quarts\backend\venv_new\filtered_reqs.txt'
with open(new_req_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Iniciando instalacion masiva de dependencias...")
os.system(r'd:\PILi_Quarts\backend\venv_new\Scripts\python.exe -m pip install -r d:\PILi_Quarts\backend\venv_new\filtered_reqs.txt')
print("FINALIZADO")
