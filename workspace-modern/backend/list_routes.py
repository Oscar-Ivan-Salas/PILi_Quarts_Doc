import requests
import json

URL = "http://localhost:3030/openapi.json"

try:
    print(f"Fetching {URL}...")
    r = requests.get(URL)
    
    if r.status_code == 200:
        data = r.json()
        paths = list(data.get("paths", {}).keys())
        print(f"\n✅ Successfully fetched {len(paths)} routes:")
        for p in sorted(paths):
            print(f" - {p}")
            
        # Check specifically for /api/documents
        if "/api/documents" in paths or "/api/documents/" in paths:
             print("\n✅ /api/documents FOUND in routes!")
        else:
             print("\n❌ /api/documents NOT FOUND in routes.")
             
    else:
        print(f"❌ Failed to fetch openapi.json: Status {r.status_code}")
        print(r.text[:500])

except Exception as e:
    print(f"❌ Error: {e}")
