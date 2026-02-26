
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TEST_GENERATION")

def test_all_generations():
    url = "http://localhost:8004/api/studio/generate"
    test_cases = [
        {"format": "word", "name": "PROYECTO COMPLEJO PMI"},
        {"format": "word", "name": "COTIZACION COMPLEJA"},
        {"format": "excel", "name": "COTIZACION COMPLEJA"},
        {"format": "pdf", "name": "INFORME TECNICO"}
    ]
    
    for case in test_cases:
        payload = {
            "html": "<html><body><h1>PRUEBA ORO</h1><p id='total'>S/ 1,234.56</p><p id='kpi-spi'>1.10</p><table><tr><td>Item</td><td>Desc</td><td>Cant</td><td>Und</td><td>P.U</td><td>Total</td></tr><tr class='item-row'><td>1</td><td>Servicio Prueba</td><td>1</td><td>und</td><td>1000</td><td>1000</td></tr></table></body></html>",
            "format": case["format"],
            "name": case["name"]
        }
        
        logger.info(f"📡 Probando {case['format']} para {case['name']}...")
        try:
            response = requests.post(url, json=payload, stream=True)
            if response.status_code == 200:
                ext = "docx" if case["format"] == "word" else case["format"]
                filename = f"TEST_FINAL_{case['format']}.{ext}"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                logger.info(f"✅ ÉXITO: {filename} guardado ({len(response.content)} bytes)")
            else:
                logger.error(f"❌ FALLO para {case['name']} ({case['format']}): {response.status_code}")
                # Si falló, intentar ver si hay un error JSON
                try:
                    print(response.json())
                except:
                    print(response.text[:200])
        except Exception as e:
            logger.error(f"❌ ERROR de conexión: {e}")

if __name__ == "__main__":
    test_all_generations()
