import requests
import json

url = "http://localhost:8003/api/generate/excel"
payload = {
    "title": "Test Project",
    "type": "cotizacion-simple",
    "data": {
        "cliente": {"nombre": "Test Client"},
        "items": []
    },
    "user_id": "test_script"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    if response.status_code == 200:
        print("Success: Excel generated")
        with open("test_output.xlsx", "wb") as f:
            f.write(response.content)
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Connection Failed: {e}")
