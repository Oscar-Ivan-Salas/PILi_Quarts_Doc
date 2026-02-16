"""
Debug N02 Direct Call.
"""
import sys
import os
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

from modules.N02_Pili_Logic.index import logic_node

def debug_direct():
    print("🔬 Debugging N02 Direct Call...")
    
    # 1. Test Pozo Tierra with Wildcard
    response = logic_node.process_intention({
        "service": "pozo-tierra",
        "subtype": "*"
    })
    
    if response.get("success"):
        data = response.get("logic_result", {})
        items = data.get("items", [])
        print(f"✅ Success! Data Service: {data.get('service_info', {}).get('name')}")
        print(f"📦 Items returned: {len(items)}")
        for item in items[:5]:
             print(f"   - {item['key']} : {item['price']}")
    else:
        print(f"❌ Error: {response.get('error')}")

if __name__ == "__main__":
    debug_direct()
