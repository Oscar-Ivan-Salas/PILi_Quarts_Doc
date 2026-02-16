
import requests
import sys

def check_dashboard():
    url = "http://localhost:8005/api/admin/dashboard"
    print(f"📡 Querying {url}...")
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()["metrics"]
            users = data["users"]["total"]
            clients = data["clients"]["total"]
            projects = data["projects"]["total"]
            print(f"✅ Dashboard Data Received:")
            print(f"   Users: {users}")
            print(f"   Clients: {clients}")
            print(f"   Projects: {projects}")
            
            if users >= 50 and clients >= 50:
                print("🎯 SUCCESS: Dashboard reflects Mass Production Data.")
            else:
                print(f"⚠️ WAIT: Data counts ({users}/{clients}) less than expected (50/50). Check DB.")
        else:
            print(f"❌ Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    check_dashboard()
