
import sys
import os

print(f"CWD: {os.getcwd()}")
print(f"sys.path before: {sys.path}")

# Add CWD to path if not present (Python usually does this for script dir, but let's be sure for CWD)
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

print(f"sys.path after: {sys.path}")

try:
    import app
    print("✅ SUCCESS: import app")
    print(f"   app location: {app.__file__}")
except ImportError as e:
    print(f"❌ FAIL: import app -> {e}")

try:
    import docx
    print("✅ SUCCESS: import docx")
    print(f"   docx location: {docx.__file__}")
except ImportError as e:
    print(f"❌ FAIL: import docx -> {e}")

try:
    from app.services.generators.cotizacion_compleja_generator import generar_cotizacion_compleja
    print("✅ SUCCESS: import generator")
except ImportError as e:
    print(f"❌ FAIL: import generator -> {e}")
except Exception as e:
    print(f"❌ FAIL: import generator (Exception) -> {e}")
