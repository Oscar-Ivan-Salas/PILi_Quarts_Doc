# 🧪 PLAN DE PRUEBAS - ARQUITECTURA PILI

## 🎯 OBJETIVO

Probar EXHAUSTIVAMENTE la nueva arquitectura PILI antes de integrarla al sistema principal.

**Regla de oro:** El código antiguo NO se toca hasta que el nuevo esté 100% probado y funcionando.

---

## 📋 FASES DE PRUEBAS

### FASE 1: Tests Unitarios (2 horas)

#### 1.1 Tests de ConfigLoader
```python
# test_config_loader.py
def test_load_service_itse():
    """Test carga de servicio ITSE"""
    loader = ConfigLoader()
    config = loader.load_service('itse')
    assert config is not None
    assert 'service' in config
    assert config['service'] == 'itse'

def test_load_document_cotizacion_simple():
    """Test carga de documento cotizacion-simple"""
    loader = ConfigLoader()
    config = loader.load_document('cotizacion-simple')
    assert config is not None
    assert config['document']['type'] == 'cotizacion-simple'

def test_load_agents():
    """Test carga de agentes"""
    loader = ConfigLoader()
    agents = loader.load_agents()
    assert 'agents' in agents
    assert len(agents['agents']) == 6

def test_list_services():
    """Test listar servicios"""
    loader = ConfigLoader()
    services = loader.list_services()
    assert 'itse' in services
    assert 'electricidad' in services
    assert len(services) == 10
```

**Ejecutar:**
```bash
cd backend
pytest app/services/pili/tests/test_config_loader.py -v
```

---

#### 1.2 Tests de FallbackManager
```python
# test_fallback_manager.py
def test_extract_data():
    """Test extracción de datos sin IA"""
    fallback = FallbackManager()
    data = fallback.extract_data("Casa de 150m²", "cotizacion-simple")
    assert 'numero' in data
    assert 'fecha' in data
    assert data.get('area_m2') == 150

def test_calculate_simple_quote():
    """Test cálculo de cotización simple"""
    fallback = FallbackManager()
    data = {"area_m2": 100}
    result = fallback.calculate_simple_quote(data)
    assert 'subtotal' in result
    assert 'igv' in result
    assert 'total' in result
    assert result['total'] > result['subtotal']
```

**Ejecutar:**
```bash
pytest app/services/pili/tests/test_fallback_manager.py -v
```

---

#### 1.3 Tests de Validators
```python
# test_validators.py
from app.services.pili.utils import validate_area, validate_pisos, validate_nombre

def test_validate_area_valid():
    """Test validación de área válida"""
    is_valid, msg = validate_area(150)
    assert is_valid == True
    assert msg == ""

def test_validate_area_invalid_too_small():
    """Test área muy pequeña"""
    is_valid, msg = validate_area(5)
    assert is_valid == False
    assert "mayor a 10" in msg

def test_validate_pisos_valid():
    """Test validación de pisos válida"""
    is_valid, msg = validate_pisos(3)
    assert is_valid == True

def test_validate_nombre_valid():
    """Test validación de nombre válido"""
    is_valid, msg = validate_nombre("Juan Pérez")
    assert is_valid == True
```

**Ejecutar:**
```bash
pytest app/services/pili/tests/test_validators.py -v
```

---

#### 1.4 Tests de Calculators
```python
# test_calculators.py
from app.services.pili.utils import calculate_simple_quote, calculate_itse_quote

def test_calculate_simple_quote():
    """Test cálculo de cotización simple"""
    data = {
        "area_m2": 100,
        "servicio": "electrico-residencial"
    }
    result = calculate_simple_quote(data)
    assert 'items' in result
    assert 'subtotal' in result
    assert 'igv' in result
    assert 'total' in result
    assert result['subtotal'] == 5000  # 100m² * 50

def test_calculate_itse_quote():
    """Test cálculo de cotización ITSE"""
    data = {
        "categoria": "SALUD",
        "tipo": "Hospital",
        "area_m2": 500,
        "pisos": 2
    }
    result = calculate_itse_quote(data)
    assert 'items' in result
    assert 'detalles' in result
    assert result['total'] > 0
```

**Ejecutar:**
```bash
pytest app/services/pili/tests/test_calculators.py -v
```

---

### FASE 2: Tests de Integración (3 horas)

#### 2.1 Tests de UniversalSpecialist
```python
# test_universal_specialist.py
from app.services.pili.specialists import UniversalSpecialist

def test_init_itse():
    """Test inicialización con ITSE"""
    specialist = UniversalSpecialist('itse', 'cotizacion-simple')
    assert specialist.service_name == 'itse'
    assert specialist.document_type == 'cotizacion-simple'

def test_initial_message():
    """Test mensaje inicial"""
    specialist = UniversalSpecialist('itse', 'cotizacion-simple')
    response = specialist.process_message('', None)
    assert 'texto' in response
    assert 'botones' in response
    assert len(response['botones']) > 0

def test_full_conversation_flow():
    """Test flujo completo de conversación"""
    specialist = UniversalSpecialist('itse', 'cotizacion-simple')
    
    # Paso 1: Mensaje inicial
    r1 = specialist.process_message('', None)
    assert r1.get('stage') in ['categoria', 'initial']
    
    # Paso 2: Seleccionar categoría
    r2 = specialist.process_message('SALUD', r1.get('state'))
    assert r2.get('stage') != r1.get('stage')
    
    # Paso 3: Seleccionar tipo
    r3 = specialist.process_message('Hospital', r2.get('state'))
    assert r3.get('stage') != r2.get('stage')
```

**Ejecutar:**
```bash
pytest app/services/pili/tests/test_universal_specialist.py -v
```

---

#### 2.2 Tests de LegacyAdapter
```python
# test_legacy_adapter.py
from app.services.pili.adapters import LocalSpecialistFactory

def test_factory_create():
    """Test factory crea adapter correctamente"""
    specialist = LocalSpecialistFactory.create('itse')
    assert specialist is not None
    assert specialist.service_name == 'itse'

def test_adapter_interface():
    """Test interfaz legacy del adapter"""
    specialist = LocalSpecialistFactory.create('itse')
    response = specialist.process_message('', None)
    
    # Verificar formato legacy
    assert 'texto' in response
    assert 'botones' in response
    assert 'stage' in response
    assert 'conversation_state' in response
    assert 'datos_generados' in response

def test_adapter_full_flow():
    """Test flujo completo con adapter"""
    specialist = LocalSpecialistFactory.create('itse')
    
    r1 = specialist.process_message('', None)
    assert 'conversation_state' in r1
    
    r2 = specialist.process_message('SALUD', r1['conversation_state'])
    assert r2['stage'] != r1['stage']
```

**Ejecutar:**
```bash
pytest app/services/pili/tests/test_legacy_adapter.py -v
```

---

### FASE 3: Tests E2E (End-to-End) (2 horas)

#### 3.1 Test Completo ITSE
```python
# test_e2e_itse.py
def test_itse_complete_flow():
    """Test flujo completo ITSE desde inicio hasta cotización"""
    specialist = LocalSpecialistFactory.create('itse')
    
    # Inicio
    r1 = specialist.process_message('', None)
    assert len(r1['botones']) > 0
    
    # Categoría
    r2 = specialist.process_message('SALUD', r1['conversation_state'])
    assert 'Hospital' in str(r2['botones'])
    
    # Tipo
    r3 = specialist.process_message('Hospital', r2['conversation_state'])
    assert 'área' in r3['texto'].lower()
    
    # Área
    r4 = specialist.process_message('500', r3['conversation_state'])
    assert 'pisos' in r4['texto'].lower()
    
    # Pisos
    r5 = specialist.process_message('2', r4['conversation_state'])
    assert 'nombre' in r5['texto'].lower()
    
    # Nombre
    r6 = specialist.process_message('Hospital Central', r5['conversation_state'])
    
    # Verificar datos generados
    assert 'datos_generados' in r6
    datos = r6['datos_generados']
    assert datos.get('categoria') == 'SALUD'
    assert datos.get('tipo') == 'Hospital'
    assert datos.get('area_m2') == 500
    assert datos.get('pisos') == 2
```

**Ejecutar:**
```bash
pytest app/services/pili/tests/test_e2e_itse.py -v
```

---

### FASE 4: Tests de Compatibilidad (1 hora)

#### 4.1 Verificar que NO rompe código existente
```python
# test_compatibility.py
def test_legacy_code_still_works():
    """Verificar que código legacy sigue funcionando"""
    # Importar código antiguo
    from app.services.pili_local_specialists import LocalSpecialistFactory as OldFactory
    
    # Crear specialist antiguo
    old_specialist = OldFactory.create('itse')
    old_response = old_specialist.process_message('', None)
    
    # Verificar que funciona
    assert 'texto' in old_response
    assert 'botones' in old_response

def test_new_code_compatible_with_old():
    """Verificar que código nuevo es compatible"""
    # Importar código nuevo
    from app.services.pili.adapters import LocalSpecialistFactory as NewFactory
    
    # Crear specialist nuevo
    new_specialist = NewFactory.create('itse')
    new_response = new_specialist.process_message('', None)
    
    # Verificar mismo formato que código antiguo
    assert 'texto' in new_response
    assert 'botones' in new_response
    assert 'conversation_state' in new_response
```

**Ejecutar:**
```bash
pytest app/services/pili/tests/test_compatibility.py -v
```

---

## ✅ CHECKLIST DE PRUEBAS

### Tests Unitarios
- [ ] ConfigLoader - Carga de servicios
- [ ] ConfigLoader - Carga de documentos
- [ ] ConfigLoader - Carga de agentes
- [ ] ConfigLoader - Listar servicios
- [ ] FallbackManager - Extracción de datos
- [ ] FallbackManager - Cálculos
- [ ] Validators - Área
- [ ] Validators - Pisos
- [ ] Validators - Nombre
- [ ] Calculators - Cotización simple
- [ ] Calculators - ITSE

### Tests de Integración
- [ ] UniversalSpecialist - Inicialización
- [ ] UniversalSpecialist - Mensaje inicial
- [ ] UniversalSpecialist - Flujo completo
- [ ] LegacyAdapter - Factory
- [ ] LegacyAdapter - Interfaz
- [ ] LegacyAdapter - Flujo completo

### Tests E2E
- [ ] ITSE - Flujo completo
- [ ] Electricidad - Flujo completo
- [ ] Pozo a tierra - Flujo completo

### Tests de Compatibilidad
- [ ] Código legacy sigue funcionando
- [ ] Código nuevo compatible con legacy
- [ ] Chat.py funciona con ambos

---

## 🚀 PLAN DE MIGRACIÓN GRADUAL

### Paso 1: Pruebas Locales (ACTUAL)
- ✅ Implementar toda la arquitectura
- ⏳ Ejecutar todos los tests
- ⏳ Verificar 100% de tests pasando

### Paso 2: Integración Paralela
- [ ] Mantener código antiguo funcionando
- [ ] Agregar flag de feature para usar código nuevo
- [ ] Probar en desarrollo con código nuevo
- [ ] Comparar resultados antiguo vs nuevo

### Paso 3: Testing en Producción
- [ ] Desplegar con flag desactivado
- [ ] Activar flag para 10% de usuarios
- [ ] Monitorear errores
- [ ] Incrementar a 50% si todo bien
- [ ] Incrementar a 100% si todo bien

### Paso 4: Deprecación
- [ ] Mover código antiguo a _deprecated
- [ ] Actualizar imports
- [ ] Eliminar flags de feature
- [ ] Documentar cambios

---

## 📊 CRITERIOS DE ÉXITO

Para considerar la migración exitosa:

1. ✅ **100% de tests pasando**
2. ✅ **Código nuevo genera mismos resultados que antiguo**
3. ✅ **Performance igual o mejor**
4. ✅ **Sin errores en logs**
5. ✅ **Usuarios no notan diferencia**

---

## ⚠️ PLAN DE ROLLBACK

Si algo falla:

1. Desactivar flag de feature
2. Volver a código antiguo
3. Analizar logs de error
4. Corregir problema
5. Repetir pruebas

---

## 🎯 PRÓXIMO PASO INMEDIATO

**Crear todos los archivos de tests y ejecutarlos.**

¿Quieres que empiece creando los archivos de tests?
