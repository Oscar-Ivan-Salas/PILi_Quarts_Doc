
import requests
import json

try:
    response = requests.get("http://localhost:8005/openapi.json")
    if response.status_code == 200:
        data = response.json()
        paths = data.get("paths", {}).keys()
        print("Available paths on port 8005:")
        for path in sorted(paths):
            print(f" - {path}")
    else:
        print(f"Error fetching openapi.json: {response.status_code}")
except Exception as e:
    print(f"Connection failed: {e}")
