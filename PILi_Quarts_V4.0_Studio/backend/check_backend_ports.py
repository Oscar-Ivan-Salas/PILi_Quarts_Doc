import urllib.request
import json
import ssl

def check_url(url):
    print(f"Testing {url} ...", end=" ")
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2, context=ctx) as response:
            print(f"✅ OK ({response.getcode()})")
            return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

print("🔍 Scanning Backend Ports...")
ports = [8000, 8001, 8002, 8005, 3030]

for port in ports:
    base = f"http://localhost:{port}"
    if check_url(base + "/"):
        print(f"🚀 FOUND BACKEND AT PORT {port}")
        # Check docs
        check_url(base + "/api/documents/")
        check_url(base + "/api/pili/v2/generate") # Expect 405 Method Not Allowed (GET)
