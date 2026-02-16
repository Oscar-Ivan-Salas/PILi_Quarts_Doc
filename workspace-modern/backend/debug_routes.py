import sys
import os

# Add current directory to path so we can import main
sys.path.append(os.getcwd())

try:
    from main import app
    print("\n✅ FastAPI App Loaded Successfully!")
    print(f"Title: {app.title}")
    
    print("\n🔍 Registered Routes:")
    for route in app.routes:
        methods = ", ".join(route.methods) if hasattr(route, "methods") else "None"
        path = route.path
        name = route.name
        print(f" - {methods} {path} ({name})")
        
except Exception as e:
    print(f"❌ Error loading app: {e}")
    import traceback
    traceback.print_exc()
