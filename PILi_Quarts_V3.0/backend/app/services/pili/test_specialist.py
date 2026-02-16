"""
🧪 TEST UNIVERSAL SPECIALIST - Script de Prueba
📁 RUTA: backend/app/services/pili/test_specialist.py

Script para probar que UniversalSpecialist funciona correctamente con los 10 servicios.
"""

import sys
from pathlib import Path

# Agregar el path del backend al PYTHONPATH
backend_path = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.services.pili.specialist import UniversalSpecialist


def test_service(service_name: str):
    """Prueba un servicio específico."""
    print(f"\n{'='*80}")
    print(f"🧪 PROBANDO SERVICIO: {service_name.upper()}")
    print(f"{'='*80}\n")
    
    try:
        # Crear el especialista
        specialist = UniversalSpecialist(service_name)
        
        # Verificar que se cargó la configuración
        print(f"✅ Configuración cargada")
        print(f"   - Nombre: {specialist.config.get('name', 'N/A')}")
        print(f"   - Descripción: {specialist.config.get('description', 'N/A')}")
        print(f"   - Normativa: {specialist.config.get('normativa', 'N/A')}")
        
        # Verificar etapas
        num_etapas = len(specialist.stages)
        print(f"\n✅ Etapas de conversación: {num_etapas}")
        for i, stage in enumerate(specialist.stages, 1):
            print(f"   {i}. {stage['id']} ({stage['type']}) - {stage.get('progress', 'N/A')}")
        
        # Probar el primer mensaje
        print(f"\n🤖 Iniciando conversación...")
        response = specialist.process_message('')
        
        print(f"\n📝 Respuesta inicial:")
        print(f"   - Stage: {response.get('stage')}")
        print(f"   - Progreso: {response.get('progreso', 'N/A')}")
        print(f"   - Texto: {response.get('texto', '')[:200]}...")
        
        if 'botones' in response:
            print(f"   - Botones: {len(response['botones'])} opciones")
            for btn in response['botones'][:3]:  # Mostrar solo los primeros 3
                print(f"      • {btn.get('text', 'N/A')}")
        
        print(f"\n✅ SERVICIO {service_name.upper()} FUNCIONA CORRECTAMENTE\n")
        return True
    
    except Exception as e:
        print(f"\n❌ ERROR EN SERVICIO {service_name.upper()}")
        print(f"   Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal de prueba."""
    print("\n" + "="*80)
    print("🚀 INICIANDO PRUEBAS DE UNIVERSAL SPECIALIST")
    print("="*80)
    
    # Lista de servicios a probar
    servicios = [
        'itse',
        'electricidad',
        'pozo-tierra',
        'contraincendios',
        'domotica',
        'cctv',
        'redes',
        'automatizacion-industrial',
        'expedientes',
        'saneamiento'
    ]
    
    resultados = {}
    
    # Probar cada servicio
    for servicio in servicios:
        resultado = test_service(servicio)
        resultados[servicio] = resultado
    
    # Resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*80 + "\n")
    
    exitosos = sum(1 for r in resultados.values() if r)
    fallidos = len(resultados) - exitosos
    
    print(f"✅ Servicios exitosos: {exitosos}/{len(resultados)}")
    print(f"❌ Servicios fallidos: {fallidos}/{len(resultados)}\n")
    
    for servicio, resultado in resultados.items():
        estado = "✅ OK" if resultado else "❌ FALLO"
        print(f"   {estado} - {servicio}")
    
    print("\n" + "="*80)
    
    if fallidos == 0:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    else:
        print(f"⚠️  {fallidos} servicio(s) necesitan corrección")
    
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
