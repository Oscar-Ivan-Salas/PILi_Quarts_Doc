import urllib.request
import json
import datetime

url = "http://127.0.0.1:8005/api/generate/excel"
data = {
    "type": "cotizacion_simple",
    "data": {
        "numero": "TEST-PYTHON-001",
        "cliente": {"nombre": "Cliente Python"},
        "items": [{"descripcion": "Item Python", "cantidad": 1, "precioUnitario": 100}]
    },
    "user_id": "test-user-python"
}

req = urllib.request.Request(url)
req.add_header('Content-Type', 'application/json')
jsondata = json.dumps(data).encode('utf-8')
req.add_header('Content-Length', len(jsondata))

print(f"Sending request to {url}...")
try:
    response = urllib.request.urlopen(req, jsondata)
    print(f"Response Code: {response.getcode()}")
    print("Response received.")
except Exception as e:
    print(f"Error: {e}")
