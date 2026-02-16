
import requests
import sys

def test_excel_generation():
    url = "http://localhost:8003/api/generate/excel"
    payload = {
        "title": "Test Project",
        "type": "cotizacion-simple",
        "data": {
            "cliente": { "nombre": "Test Client", "ruc": "12345678901" },
            "proyecto": "Test Project",
            "items": [
                { "descripcion": "Item 1", "cantidad": 10, "precio_unitario": 50 },
                { "descripcion": "Item 2", "cantidad": 5, "precio_unitario": 100 }
            ]
        }
    }

    try:
        print(f"Sending POST to {url}...")
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Success! Body size:", len(response.content))
            headers = response.headers
            print("Content-Type:", headers.get('content-type'))
            print("Content-Disposition:", headers.get('content-disposition'))
            
            if 'spreadsheetml' in headers.get('content-type', ''):
                print("✅ Verification PASSED: Excel file received.")
            else:
                print("❌ Verification FAILED: Incorrect Content-Type.")
                sys.exit(1)
        else:
            print("❌ Verification FAILED: Status not 200")
            print("Response:", response.text)
            sys.exit(1)

    except Exception as e:
        print(f"❌ Verification FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_excel_generation()
