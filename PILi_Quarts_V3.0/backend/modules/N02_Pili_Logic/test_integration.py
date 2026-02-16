"""
Script de Integración N02.
Verifica que el código legacy (pili_local_specialists) puede consultar el conocimiento desde N02.
"""
import sys
import os
from pathlib import Path
import logging

# Setup paths
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
sys.path.append(str(backend_dir))

# Config Logging
logging.basicConfig(level=logging.INFO)

# Import del módulo refactorizado (Legacy Proxy)
try:
    from modules.pili.legacy.pili_local_specialists import KNOWLEDGE_BASE
    
    print("✅ Importación exitosa de pili_local_specialists (Proxy).")
    
    # Test: Puesta a Tierra (Key legacy: pozo-tierra)
    service_key = "pozo-tierra"
    print(f"🔄 Consultando Legacy KNOWLEDGE_BASE['{service_key}']...")
    
    data = KNOWLEDGE_BASE[service_key]
    
    if data:
        print("🎉 DATOS RECIBIDOS DEL PROXY N02!")
        print(f"Normativa: {data.get('normativa')}")
        
        # Verificar precio específico
        # Nota: La estructura del proxy devuelve un 'STANDARD' genérico en 'tipos'
        tipos = data.get('tipos', {})
        first_type = list(tipos.values())[0]
        precios = first_type.get('precios', {})
        
        print(f"Precios encontrados: {len(precios)}")
        if precios:
             print("Ejemplos de precios:")
             for k, v in list(precios.items())[:3]:
                 print(f"  - {k}: {v}")
        else:
             print("⚠️ No se encontraron precios en la respuesta.")
             
    else:
        print("❌ Error: KNOWLEDGE_BASE devolvió datos vacíos o nulos.")

except ImportError as e:
    print(f"❌ Error de Importación: {e}")
except Exception as e:
    print(f"❌ Error General: {e}")
