
import requests
import json
import uuid

BASE_URL = "http://localhost:8003"
CHAT_ENDPOINT = f"{BASE_URL}/api/pili/chat"
HEALTH_ENDPOINT = f"{BASE_URL}/api/pili/health"

def test_health():
    try:
        response = requests.get(HEALTH_ENDPOINT)
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            print("PILI Service is healthy.")
        else:
            print(f"FAILED: {response.text}")
    except Exception as e:
        print(f"Health Check Connection Failed: {e}")

def test_chat():
    payload = {
        "user_id": str(uuid.uuid4()),
        "message": "Hola, genera una cotizacion de prueba",
        "context": {}
    }
    
    try:
        response = requests.post(CHAT_ENDPOINT, json=payload)
        print(f"Chat Response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Chat Success!")
            print(f"Response: {data.get('response', '')[:50]}...")
        else:
            print(f"Chat FAILED: {response.text}")
    except Exception as e:
        print(f"Chat Connection Failed: {e}")

if __name__ == "__main__":
    print(f"Verifying PILI API at {BASE_URL}...")
    test_health()
    test_chat()
