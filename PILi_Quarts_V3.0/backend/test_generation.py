import requests
import json

ports = [3030]

payload = {
    "user_id": "b2289941-d90c-4d48-b8c2-6e3fafe88944",
    "project_id": "default-project-1",
    "format": "docx",
    "data": {
        "cliente": {
            "nombre": "Cliente Test Python",
            "empresa": "Empresa Test S.A."
        },
        "items": [
            {"descripcion": "Item Test Python", "cantidad": 2, "precio_unitario": 150}
        ]
    }
}

for port in ports:
    try:
        url = f"http://localhost:{port}/api/pili/v2/generate"
        print(f"Testing port {port}...")
        response = requests.post(url, json=payload, timeout=2)
        print(f"Success on port {port}!")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        break
    except Exception as e:
        print(f"Failed on port {port}: {e}")

