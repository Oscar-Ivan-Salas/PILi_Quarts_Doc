# 🚀 INTEGRACIÓN RÁPIDA PILI - 20% FALTANTE

## ✅ LO QUE YA EXISTE (80%)

### 1. Arquitectura Modular Completa
- ✅ `pili/specialist.py` - UniversalSpecialist (428 líneas)
- ✅ `pili/config/` - 10 servicios YAML (87 KB)
- ✅ `pili/knowledge/` - 11 knowledge bases modulares
- ✅ `pili/core/` - Lógica central
- ✅ `pili/templates/` - Plantillas de mensajes

### 2. Código Legacy Funcionando
- ✅ `chat.py` - Endpoint funcionando
- ✅ `pili_local_specialists.py` - ITSESpecialist operativo
- ✅ `pili_integrator.py` - Orquestador legacy
- ✅ `pili_brain.py` - Fallback offline

---

## ⚠️ LO QUE FALTA (20%)

### 1. Conectar UniversalSpecialist con chat.py
**Archivo:** `backend/app/routers/chat.py`
**Línea:** 2891

**Cambio necesario:**
```python
# ANTES (legacy)
if tipo_flujo == 'itse':
    from app.services.pili_local_specialists import LocalSpecialistFactory
    specialist = LocalSpecialistFactory.create('itse')

# DESPUÉS (modular)
if tipo_flujo == 'itse':
    from app.services.pili.specialist import UniversalSpecialist
    specialist = UniversalSpecialist('itse', 'cotizacion-simple')
```

**Tiempo:** 30 minutos

---

### 2. Crear Wrapper para Compatibilidad
**Archivo:** `backend/app/services/pili/adapters/legacy_adapter.py`

**Propósito:** Mantener compatibilidad con código existente

```python
"""
Adapter para compatibilidad con código legacy
"""

from ..specialist import UniversalSpecialist

class LegacySpecialistAdapter:
    """Adapta UniversalSpecialist a interfaz legacy"""
    
    def __init__(self, service_name: str):
        self.specialist = UniversalSpecialist(service_name, 'cotizacion-simple')
    
    def process_message(self, message: str, state: dict = None) -> dict:
        """Interfaz compatible con código legacy"""
        response = self.specialist.process_message(message, state)
        
        # Adaptar formato de respuesta
        return {
            'texto': response.get('texto', ''),
            'botones': response.get('botones', []),
            'stage': response.get('stage'),
            'conversation_state': response.get('state'),
            'datos_generados': response.get('state', {}).get('data', {})
        }

class LocalSpecialistFactory:
    """Factory compatible con código legacy"""
    
    @staticmethod
    def create(service_name: str):
        return LegacySpecialistAdapter(service_name)
```

**Tiempo:** 1 hora

---

### 3. Actualizar Imports en chat.py
**Archivo:** `backend/app/routers/chat.py`

**Cambio:**
```python
# Línea 2894 - ANTES
from app.services.pili_local_specialists import LocalSpecialistFactory

# Línea 2894 - DESPUÉS
from app.services.pili.adapters.legacy_adapter import LocalSpecialistFactory
```

**Tiempo:** 15 minutos

---

### 4. Crear Tests de Integración
**Archivo:** `backend/app/services/pili/tests/test_integration.py`

```python
import pytest
from app.services.pili.specialist import UniversalSpecialist
from app.services.pili.adapters.legacy_adapter import LocalSpecialistFactory

def test_universal_specialist_itse():
    """Test UniversalSpecialist con ITSE"""
    specialist = UniversalSpecialist('itse', 'cotizacion-simple')
    
    # Test mensaje inicial
    response = specialist.process_message('', None)
    assert 'SALUD' in str(response.get('botones', []))
    assert response.get('stage') == 'categoria'

def test_legacy_adapter():
    """Test adapter de compatibilidad"""
    specialist = LocalSpecialistFactory.create('itse')
    
    # Test interfaz legacy
    response = specialist.process_message('', None)
    assert 'texto' in response
    assert 'botones' in response
    assert 'conversation_state' in response

def test_full_conversation_flow():
    """Test flujo completo de conversación"""
    specialist = UniversalSpecialist('itse', 'cotizacion-simple')
    
    # Paso 1: Mensaje inicial
    r1 = specialist.process_message('', None)
    assert r1['stage'] == 'categoria'
    
    # Paso 2: Seleccionar categoría
    r2 = specialist.process_message('SALUD', r1['state'])
    assert r2['stage'] == 'tipo'
    
    # Paso 3: Seleccionar tipo
    r3 = specialist.process_message('Hospital', r2['state'])
    assert r3['stage'] == 'area'
    
    # Paso 4: Ingresar área
    r4 = specialist.process_message('500', r3['state'])
    assert r4['stage'] == 'pisos'
    
    # Paso 5: Ingresar pisos
    r5 = specialist.process_message('2', r4['state'])
    assert r5['stage'] == 'quotation'
```

**Tiempo:** 1 hora

---

### 5. Actualizar pili_integrator.py
**Archivo:** `backend/app/services/pili_integrator.py`
**Línea:** 58-64

**Ya está hecho:** ✅
```python
# Líneas 58-64 - Ya comentado
# try:
#     from app.services.pili.specialist import UniversalSpecialist
#     NUEVA_ARQUITECTURA_DISPONIBLE = True
# except ImportError:
NUEVA_ARQUITECTURA_DISPONIBLE = False
```

**Cambio necesario:** Descomentar y activar
```python
try:
    from app.services.pili.specialist import UniversalSpecialist
    from app.services.pili.adapters.legacy_adapter import LocalSpecialistFactory as NewFactory
    NUEVA_ARQUITECTURA_DISPONIBLE = True
except ImportError:
    NUEVA_ARQUITECTURA_DISPONIBLE = False
```

**Tiempo:** 15 minutos

---

### 6. Crear Configuración de Multi-IA
**Archivo:** `backend/app/services/pili/config/multi_ia.yaml`

```yaml
multi_ia:
  enabled: true
  fallback_mode: "pili_brain"
  
  providers:
    gemini:
      enabled: true
      priority: 1
      api_key_env: "GEMINI_API_KEY"
      model: "gemini-1.5-pro"
      use_for:
        - "cotizacion-simple"
        - "cotizacion-compleja"
        - "proyecto-simple"
        - "proyecto-complejo-pmi"
        - "informe-tecnico"
        - "informe-ejecutivo-apa"
```

**Tiempo:** 30 minutos

---

### 7. Documentación Rápida
**Archivo:** `backend/app/services/pili/README.md`

```markdown
# PILI - Arquitectura Modular

## Uso Rápido

```python
from app.services.pili.specialist import UniversalSpecialist

# Crear especialista
specialist = UniversalSpecialist('itse', 'cotizacion-simple')

# Procesar mensaje
response = specialist.process_message('', None)
```

## Servicios Disponibles

- itse
- electricidad
- pozo-tierra
- contraincendios
- domotica
- cctv
- redes
- saneamiento
- automatizacion-industrial
- expedientes

## Configuración

Editar archivos YAML en `config/`:
- `services/*.yaml` - Configuración de servicios
- `multi_ia.yaml` - Configuración multi-IA
```

**Tiempo:** 30 minutos

---

## 📋 PLAN DE EJECUCIÓN RÁPIDA

### Fase 1: Adapter (1.5 horas)
1. Crear `pili/adapters/legacy_adapter.py`
2. Implementar LegacySpecialistAdapter
3. Implementar LocalSpecialistFactory

### Fase 2: Integración (1 hora)
1. Actualizar import en `chat.py`
2. Descomentar código en `pili_integrator.py`
3. Verificar que no rompe nada

### Fase 3: Tests (1 hora)
1. Crear `pili/tests/test_integration.py`
2. Ejecutar tests
3. Verificar cobertura

### Fase 4: Configuración (1 hora)
1. Crear `multi_ia.yaml`
2. Crear `README.md`
3. Documentar uso

### Fase 5: Verificación (0.5 horas)
1. Reiniciar backend
2. Probar chat ITSE
3. Verificar que funciona

**TOTAL:** 5 horas (en vez de 17)

---

## 🎯 COMANDOS RÁPIDOS

### Crear estructura
```bash
mkdir -p backend/app/services/pili/adapters
mkdir -p backend/app/services/pili/tests
touch backend/app/services/pili/adapters/__init__.py
touch backend/app/services/pili/adapters/legacy_adapter.py
touch backend/app/services/pili/tests/__init__.py
touch backend/app/services/pili/tests/test_integration.py
touch backend/app/services/pili/config/multi_ia.yaml
touch backend/app/services/pili/README.md
```

### Ejecutar tests
```bash
cd backend
pytest app/services/pili/tests/test_integration.py -v
```

### Reiniciar backend
```bash
# El uvicorn se reiniciará automáticamente con --reload
```

---

## ✅ CHECKLIST

### Fase 1: Adapter
- [ ] Crear `adapters/legacy_adapter.py`
- [ ] Implementar LegacySpecialistAdapter
- [ ] Implementar LocalSpecialistFactory
- [ ] Crear `adapters/__init__.py`

### Fase 2: Integración
- [ ] Actualizar import en `chat.py` línea 2894
- [ ] Descomentar código en `pili_integrator.py` línea 58-64
- [ ] Verificar imports

### Fase 3: Tests
- [ ] Crear `tests/test_integration.py`
- [ ] Test UniversalSpecialist
- [ ] Test LegacyAdapter
- [ ] Test flujo completo
- [ ] Ejecutar tests

### Fase 4: Configuración
- [ ] Crear `config/multi_ia.yaml`
- [ ] Crear `README.md`
- [ ] Documentar uso

### Fase 5: Verificación
- [ ] Reiniciar backend
- [ ] Probar chat ITSE en frontend
- [ ] Verificar logs
- [ ] Confirmar funcionamiento

---

## 🚀 INICIO INMEDIATO

Voy a empezar con Fase 1: Crear el adapter de compatibilidad.

¿Procedo?
