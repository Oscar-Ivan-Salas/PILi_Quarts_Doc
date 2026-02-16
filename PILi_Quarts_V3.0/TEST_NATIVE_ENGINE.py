import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from backend.modules.N04_Binary_Factory.generators.cotizacion_compleja_generator import generar_cotizacion_compleja

def test_native_engine():
    print("🚀 INICIANDO PRUEBA MOTOR NATIVO (WORD_GENERATOR)...")
    
    # Datos de prueba (Mismos que el anterior para comparar)
    datos = {
        "numero": "COT-NATIVE-001",
        "cliente": {
            "nombre": "Usuario VIP 001",
            "direccion": "Av. La Paz 123, Miraflores",
            "ruc": "20555555551"
        },
        "proyecto": "Implementación Sistema Eléctrico (MOTOR NATIVO)",
        "fecha": "13/02/2025",
        "vigencia": "15 días",
        "servicio": "Electricidad Industrial", # Ajustado key
        "descripcion_proyecto": "Suministro e instalación con Motor Nativo B.",
        "items": [
            {
                "descripcion": "Tablero General (Renderizado Nativo)",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 2500.00
            },
            {
                "descripcion": "Cableado Estructurado (Lineas perfectas)",
                "cantidad": 100,
                "unidad": "m",
                "precio_unitario": 15.00
            },
            {
                "descripcion": "Pruebas de Calidad (Sin errores visuales)",
                "cantidad": 20,
                "unidad": "pto",
                "precio_unitario": 50.00
            }
        ]
    }
    
    ruta_salida = Path("storage/generados/COT_NATIVE_V3_LAYOUT.docx")
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"📄 Generando documento: {ruta_salida}...")
    try:
        resultado = generar_cotizacion_compleja(datos, ruta_salida)
        print(f"✅ ¡ÉXITO! Documento NATIVO generado en: {resultado}")
        print("🔍 Este documento debería tener formato perfecto (Encabezados, Tablas, Colores).")
    except Exception as e:
        print(f"❌ FALLO MOTOR NATIVO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_native_engine()
