import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from backend.modules.N04_Binary_Factory.html_to_word_generator import html_to_word_generator

def test_senior_protocol():
    print("🚀 INICIANDO PROTOCOLO SENIOR DE VERIFICACIÓN...")
    
    # Datos de prueba (REALES, no estáticos)
    datos = {
        "numero": "COT-SENIOR-001",
        "cliente": {
            "nombre": "Usuario VIP 001",
            "direccion": "Av. La Paz 123, Miraflores",
            "ruc": "20555555551"
        },
        "proyecto": "Implementación Sistema Eléctrico Industrial (SENIOR)",
        "fecha": "13/02/2025",
        "vigencia": "15 días",
        "servicio_nombre": "Electricidad Industrial",
        "descripcion": "Suministro e instalación de tableros con el nuevo motor de inyección biológica.",
        "subtotal": 5000.00,
        "igv": 900.00,
        "total": 5900.00,
        "normativa": "CNE 2011 / NTP IEC 60364",
        "dias_ingenieria": "3",
        "dias_adquisiciones": "5",
        "dias_instalacion": "10",
        "dias_pruebas": "2",
        "items": [
            {
                "descripcion": "Tablero General de Baja Tensión (TGBT) - Inyección Dinámica",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 2500.00
            },
            {
                "descripcion": "Cableado Estructurado Cat 6A (Item Dinámico 2)",
                "cantidad": 100,
                "unidad": "m",
                "precio_unitario": 15.00
            },
            {
                "descripcion": "Certificación de Puntos de Red (Item Dinámico 3)",
                "cantidad": 20,
                "unidad": "pto",
                "precio_unitario": 50.00
            }
        ]
    }
    
    print(f"📄 Generando documento para: {datos['cliente']['nombre']}...")
    try:
        ruta = html_to_word_generator.generar_cotizacion_compleja(datos)
        print(f"✅ ¡ÉXITO! Documento generado en: {ruta}")
        print("🔍 Verifica que la tabla tenga 3 items y el diseño sea 'Espejo Exacto'.")
    except Exception as e:
        print(f"❌ FALLO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_senior_protocol()
