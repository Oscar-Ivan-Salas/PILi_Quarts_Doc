
import requests
import json

BASE_URL = "http://localhost:8005/api/admin"

def test_dashboard():
    print("Testing GET /dashboard...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Settings found: {'settings' in data}")
            print(f"Metrics found: {'metrics' in data}")
            return data
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")
    return None

def test_toggle(type_, id_, state):
    print(f"Testing POST /toggle-{type_} for {id_} to {state}...")
    try:
        response = requests.post(
            f"{BASE_URL}/toggle-{type_}",
            json={"id": id_, "estado": state}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Success: {response.json().get('success')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    data = test_dashboard()
    if data:
        # Test toggling a service
        test_toggle("service", "pili_brain", False)
        # Verify
        test_dashboard()
        # Toggle back
        test_toggle("service", "pili_brain", True)
