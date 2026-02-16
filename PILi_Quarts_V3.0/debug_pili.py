
import sys
import os
import asyncio
import logging

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_brain():
    print("--- TESTING IMPORTS ---")
    try:
        from backend.modules.pili.core.brain import PILIBrain
        print("✅ PILIBrain imported")
    except ImportError as e:
        print(f"❌ PILIBrain import failed: {e}")
        return

    print("\n--- TESTING INSTANTIATION ---")
    try:
        brain = PILIBrain()
        print("✅ PILIBrain instantiated")
    except Exception as e:
        print(f"❌ PILIBrain instantiation failed: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n--- TESTING PROCESSING ---")
    try:
        context = {
            "service_id": "electricidad",
            "tipo_flujo": "cotizacion-simple",
            "data": {},
            "history": []
        }
        print("Sending message...")
        result = await brain.process_message(
            message="Hola, necesito ayuda",
            user_id="test-user",
            context=context
        )
        print(f"✅ Result: {result.keys()}")
        print(f"Response: {result.get('response')[:50]}...")
        if 'thought_trace' in result.get('extracted_data', {}):
             print(f"✅ Thought trace found: {len(result['extracted_data']['thought_trace'])} steps")
        else:
             print("⚠️ Thought trace MISSING")

    except Exception as e:
        print(f"❌ Processing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_brain())
