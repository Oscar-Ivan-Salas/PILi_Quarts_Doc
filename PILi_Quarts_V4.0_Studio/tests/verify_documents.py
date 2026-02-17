
import requests
import sys

def test_document_generation():
    base_url = "http://localhost:8003/api/generate"
    payload = {
        "title": "Test Document",
        "type": "cotizacion-simple",
        "data": {
            "cliente": { "nombre": "Test Client", "ruc": "12345678901" },
            "proyecto": "Test Project",
            "items": [
                { "descripcion": "Item 1", "cantidad": 10, "precio_unitario": 50 }
            ]
        }
    }

    # Test PDF
    print(f"\n--- Testing PDF Generation ---")
    try:
        response = requests.post(f"{base_url}/pdf", json=payload)
        if response.status_code == 200:
            ctype = response.headers.get('content-type', '')
            if 'pdf' in ctype:
                print("✅ PDF Verification PASSED")
            else:
                print(f"❌ PDF Failed: Wrong Content-Type {ctype}")
        else:
            print(f"❌ PDF Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ PDF Error: {e}")

    # Test Word
    print(f"\n--- Testing Word Generation ---")
    try:
        response = requests.post(f"{base_url}/word", json=payload)
        if response.status_code == 200:
            ctype = response.headers.get('content-type', '')
            if 'wordprocessingml' in ctype or 'officedocument' in ctype:
                print("✅ Word Verification PASSED")
            else:
                print(f"❌ Word Failed: Wrong Content-Type {ctype}")
        else:
            print(f"❌ Word Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Word Error: {e}")

if __name__ == "__main__":
    test_document_generation()
