import requests
import json
import os

BASE_URL = "http://localhost:8001/api"
TEST_DOC_ID = None

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_root():
    try:
        r = requests.get(f"http://localhost:8001/")
        if r.status_code == 200:
            log("Backend Root: OK", "PASS")
            return True
        else:
            log(f"Backend Root: Failed ({r.status_code})", "FAIL")
            return False
    except Exception as e:
        log(f"Backend Connection Error: {e}", "FAIL")
        return False

def test_create_document():
    global TEST_DOC_ID
    payload = {
        "title": "Test Document Automated",
        "type": "proyecto-simple",
        "data": {
            "cliente": {"nombre": "Cliente Test"},
            "proyecto": {"nombre": "Proyecto Test"}
        },
        "color_scheme": "azul-tesla",
        "font": "Calibri",
        "user_id": "test-user"
    }
    
    try:
        r = requests.post(f"{BASE_URL}/documents/", json=payload)
        if r.status_code == 200:
            data = r.json()
            TEST_DOC_ID = data['id']
            log(f"Create Document: OK (ID: {TEST_DOC_ID})", "PASS")
            return True
        else:
            log(f"Create Document: Failed ({r.text})", "FAIL")
            return False
    except Exception as e:
        log(f"Create Error: {e}", "FAIL")
        return False

def test_generate_pdf():
    payload = {
        "title": "Test PDF",
        "type": "proyecto-simple",
        "data": {
            "cliente": {"nombre": "Cliente PDF"},
            "proyecto": {"nombre": "Proyecto PDF Test"}
        },
        "color_scheme": "rojo-pili"
    }
    
    try:
        r = requests.post(f"{BASE_URL}/generate/pdf", json=payload)
        if r.status_code == 200 and r.headers['content-type'] == 'application/pdf':
            log("Generate PDF: OK", "PASS")
            return True
        else:
            log(f"Generate PDF: Failed ({r.status_code})", "FAIL")
            return False
    except Exception as e:
        log(f"PDF Error: {e}", "FAIL")
        return False

def run_tests():
    print("=== STARTING FINAL SYSTEM VERIFICATION ===")
    if not test_root(): return
    if not test_create_document(): return
    test_generate_pdf()
    print("=== VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    run_tests()
