import requests

URL = "http://localhost:8005/openapi.json"

try:
    print(f"Fetching {URL}...")
    r = requests.get(URL, timeout=5)
    
    if r.status_code == 200:
        data = r.json()
        paths = list(data.get("paths", {}).keys())
        print(f"\n✅ Backend on 8005 - {len(paths)} routes available:")
        for p in sorted(paths):
            print(f" - {p}")
            
        # Check critical endpoints
        critical = ["/api/documents", "/api/generate/word", "/api/pili/v2/generate"]
        missing = [c for c in critical if c not in "".join(paths)]
        
        if not missing:
            print("\n✅ All critical endpoints found!")
        else:
            print(f"\n⚠️ Missing endpoints: {missing}")
            
    else:
        print(f"❌ Failed: Status {r.status_code}")

except Exception as e:
    print(f"❌ Error: {e}")
