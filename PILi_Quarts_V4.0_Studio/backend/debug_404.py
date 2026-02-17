import requests
import sys

URL = "http://localhost:3030/api/documents"
PARAMS = {"user_id": "demo-user-123", "type": "proyecto"}

try:
    print(f"Testing GET {URL} with params {PARAMS}...")
    response = requests.get(URL, params=PARAMS)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 404:
        print("Confirmed 404 Not Found.")
    else:
        print("Endpoint is accessible.")

except Exception as e:
    print(f"Error accessing endpoint: {e}")
