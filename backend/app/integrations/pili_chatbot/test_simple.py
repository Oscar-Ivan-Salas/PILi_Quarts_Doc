"""
Test simple sin emojis para Windows
"""

import sys
sys.path.insert(0, 'e:\\TESLA_COTIZADOR-V3.0')

from Pili_ChatBot.pili_itse_chatbot import PILIITSEChatBot

# Crear instancia
chatbot = PILIITSEChatBot()

print("=== TEST PILI ITSE ChatBot ===\n")

# Paso 1: Inicio
print("PASO 1: Inicio")
resultado = chatbot.procesar("", None)
print(f"Success: {resultado['success']}")
print(f"Tiene botones: {len(resultado['botones'])} categorias")
print(f"Estado: {resultado['estado']}\n")

# Paso 2: Seleccionar SALUD
print("PASO 2: Seleccionar SALUD")
resultado = chatbot.procesar("SALUD", resultado['estado'])
print(f"Success: {resultado['success']}")
print(f"Tiene botones: {len(resultado['botones'])} tipos")
print(f"Estado: {resultado['estado']}\n")

# Paso 3: Seleccionar Hospital
print("PASO 3: Seleccionar Hospital")
resultado = chatbot.procesar("Hospital", resultado['estado'])
print(f"Success: {resultado['success']}")
print(f"Estado: {resultado['estado']}\n")

# Paso 4: Ingresar area 600
print("PASO 4: Ingresar area 600")
resultado = chatbot.procesar("600", resultado['estado'])
print(f"Success: {resultado['success']}")
print(f"Estado: {resultado['estado']}\n")

# Paso 5: Ingresar pisos 2
print("PASO 5: Ingresar pisos 2")
resultado = chatbot.procesar("2", resultado['estado'])
print(f"Success: {resultado['success']}")
print(f"Cotizacion generada: {resultado['cotizacion'] is not None}")

if resultado['cotizacion']:
    cot = resultado['cotizacion']
    print(f"\nCOTIZACION:")
    print(f"  Categoria: {cot['categoria']}")
    print(f"  Tipo: {cot['tipo']}")
    print(f"  Area: {cot['area']} m2")
    print(f"  Pisos: {cot['pisos']}")
    print(f"  Riesgo: {cot['riesgo']}")
    print(f"  Costo TUPA: S/ {cot['costo_tupa']:.2f}")
    print(f"  Costo Tesla: S/ {cot['costo_tesla_min']} - {cot['costo_tesla_max']}")
    print(f"  TOTAL: S/ {cot['total_min']:.2f} - {cot['total_max']:.2f}")
    print(f"  Dias: {cot['dias']}")

print("\n=== TEST COMPLETADO EXITOSAMENTE ===")
