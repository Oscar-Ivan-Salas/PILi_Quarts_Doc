import requests
import json

URL = "http://localhost:8004/api/studio/generate"
payload = {
    "html": "<html><body><h1>PRUEBA WORD</h1><p>Contenido de prueba</p></body></html>",
    "format": "word",
    "name": "COTIZACION SIMPLE"
}

try:
    print("🚀 Triggering Word Generation...")
    res = requests.post(URL, json=payload, timeout=30)
    print(f"Status Code: {res.status_code}")
    print("Response Content:")
    try:
        print(json.dumps(res.json(), indent=2))
    except:
        print(res.text[:500])
except Exception as e:
    print(f"Error: {e}")
