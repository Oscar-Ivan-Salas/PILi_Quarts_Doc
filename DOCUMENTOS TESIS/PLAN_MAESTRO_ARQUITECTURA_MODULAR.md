# 🏗️ PLAN MAESTRO: Arquitectura Modular Escalable con Mantenimiento Predictivo

**Fecha:** 2025-12-31  
**Objetivo:** Migrar ITSE a arquitectura modular y preparar para 10 servicios  
**Inspiración:** Netflix OSS, Google SRE, AWS Well-Architected Framework

---

## 📋 TABLA DE CONTENIDOS

1. [Plan de Migración ITSE](#plan-migracion)
2. [Arquitectura Escalable 10 Servicios](#arquitectura-escalable)
3. [Sistema de Mantenimiento Predictivo](#mantenimiento-predictivo)
4. [Scripts de Diagnóstico Automático](#diagnostico-automatico)
5. [Flujo de Trabajo DevOps](#flujo-devops)

---

## 🎯 PLAN DE MIGRACIÓN ITSE

### Fase 1: Preparación (1 hora)

#### 1.1 Backup Completo
```bash
# Crear backup antes de cualquier cambio
git add -A
git commit -m "backup: Estado antes de migración modular ITSE"
git tag backup-pre-migracion-itse
git push origin backup-pre-migracion-itse
```

#### 1.2 Crear Rama de Desarrollo
```bash
git checkout -b feature/arquitectura-modular-itse
```

#### 1.3 Documentar Estado Actual
- ✅ Capturar estructura actual de archivos
- ✅ Documentar dependencias
- ✅ Crear checklist de verificación

---

### Fase 2: Reestructuración de Archivos (2 horas)

#### 2.1 Crear Estructura Modular

**Nueva estructura:**
```
Pili_ChatBot/
├── __init__.py
├── itse/
│   ├── __init__.py
│   ├── backend/
│   │   ├── __init__.py
│   │   └── pili_itse_chatbot.py (lógica Python)
│   ├── frontend/
│   │   ├── PiliITSEChat.jsx (componente React)
│   │   └── styles.css (estilos dedicados)
│   ├── tests/
│   │   ├── test_backend.py
│   │   ├── test_frontend.js
│   │   └── test_integration.py
│   ├── diagnostics/
│   │   ├── health_check.py
│   │   └── performance_monitor.py
│   └── README.md (documentación del módulo)
```

#### 2.2 Cambios por Archivo

##### Archivo 1: `Pili_ChatBot/itse/backend/pili_itse_chatbot.py`
**Acción:** Mover desde raíz  
**Cambios:**
- ✅ Mover `Pili_ChatBot/pili_itse_chatbot.py` → `Pili_ChatBot/itse/backend/`
- ✅ Sin cambios en el código (funciona como está)
- ✅ Actualizar imports en archivos que lo usan

**Riesgo:** Bajo  
**Tiempo:** 10 minutos

##### Archivo 2: `Pili_ChatBot/itse/frontend/PiliITSEChat.jsx`
**Acción:** Mover desde frontend/src/components/  
**Cambios:**
- ✅ Mover `frontend/src/components/PiliITSEChat.jsx` → `Pili_ChatBot/itse/frontend/`
- ✅ Sin cambios en el código
- ✅ Actualizar import en App.jsx

**Antes:**
```javascript
// App.jsx
import PiliITSEChat from './components/PiliITSEChat';
```

**Después:**
```javascript
// App.jsx
import PiliITSEChat from '../../../Pili_ChatBot/itse/frontend/PiliITSEChat';
```

**Riesgo:** Medio (puede romper build de React)  
**Tiempo:** 15 minutos  
**Verificación:** `npm start` debe compilar sin errores

##### Archivo 3: `backend/app/routers/chat.py`
**Acción:** Actualizar imports  
**Cambios:**

**Antes (líneas 67-87):**
```python
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from Pili_ChatBot.pili_itse_chatbot import PILIITSEChatBot
    pili_itse_bot = PILIITSEChatBot()
except Exception as e:
    logger.error(f"Error: {e}")
    pili_itse_bot = None
```

**Después:**
```python
try:
    from Pili_ChatBot.itse.backend.pili_itse_chatbot import PILIITSEChatBot
    pili_itse_bot = PILIITSEChatBot()
    logger.info("✅ Módulo ITSE cargado correctamente")
except Exception as e:
    logger.error(f"❌ Error cargando módulo ITSE: {e}")
    pili_itse_bot = None
```

**Riesgo:** Bajo  
**Tiempo:** 5 minutos

##### Archivo 4: `frontend/src/App.jsx`
**Acción:** Actualizar import  
**Cambios:**

**Antes (línea 6):**
```javascript
import PiliITSEChat from './components/PiliITSEChat';
```

**Después:**
```javascript
import PiliITSEChat from '../../../Pili_ChatBot/itse/frontend/PiliITSEChat';
```

**Riesgo:** Medio  
**Tiempo:** 5 minutos

---

### Fase 3: Verificación (30 minutos)

#### 3.1 Tests Automáticos
```bash
# Backend
cd backend
python -m pytest Pili_ChatBot/itse/tests/test_backend.py

# Frontend
cd frontend
npm test

# Integración
python Pili_ChatBot/itse/tests/test_integration.py
```

#### 3.2 Verificación Manual
1. ✅ Iniciar backend: `uvicorn app.main:app --reload`
2. ✅ Iniciar frontend: `npm start`
3. ✅ Probar flujo completo ITSE
4. ✅ Verificar auto-rellenado
5. ✅ Verificar vista previa

#### 3.3 Checklist de Verificación
- [ ] Backend inicia sin errores
- [ ] Frontend compila sin errores
- [ ] Chat ITSE se abre correctamente
- [ ] Mensaje inicial aparece (1 sola vez)
- [ ] Botones funcionan
- [ ] Estado avanza correctamente
- [ ] Auto-rellenado funciona
- [ ] Vista previa se actualiza
- [ ] No hay errores en consola

---

## 🏢 ARQUITECTURA ESCALABLE PARA 10 SERVICIOS

### Inspiración: Netflix Microservices Architecture

```
Pili_ChatBot/
├── __init__.py
├── core/                           # Código compartido
│   ├── base_chatbot.py            # Clase base para todos los servicios
│   ├── validators.py              # Validaciones comunes
│   └── formatters.py              # Formateo de respuestas
│
├── itse/                          # Servicio 1: ITSE
│   ├── backend/
│   │   └── pili_itse_chatbot.py
│   ├── frontend/
│   │   └── PiliITSEChat.jsx
│   ├── tests/
│   ├── diagnostics/
│   └── README.md
│
├── puesta_tierra/                 # Servicio 2: Puesta a Tierra
│   ├── backend/
│   │   └── pili_tierra_chatbot.py
│   ├── frontend/
│   │   └── PiliTierraChat.jsx
│   ├── tests/
│   ├── diagnostics/
│   └── README.md
│
├── instalaciones/                 # Servicio 3: Instalaciones Eléctricas
│   ├── backend/
│   ├── frontend/
│   ├── tests/
│   ├── diagnostics/
│   └── README.md
│
├── mantenimiento/                 # Servicio 4: Mantenimiento
│   └── ...
│
├── proyectos/                     # Servicio 5: Proyectos
│   └── ...
│
├── consultoria/                   # Servicio 6: Consultoría
│   └── ...
│
├── capacitacion/                  # Servicio 7: Capacitación
│   └── ...
│
├── auditoria/                     # Servicio 8: Auditoría
│   └── ...
│
├── emergencias/                   # Servicio 9: Emergencias
│   └── ...
│
└── soporte/                       # Servicio 10: Soporte Técnico
    └── ...
```

### Patrón de Diseño: Plugin Architecture

**Clase Base (core/base_chatbot.py):**
```python
from abc import ABC, abstractmethod

class BaseChatBot(ABC):
    """Clase base para todos los servicios de chat"""
    
    @abstractmethod
    def procesar(self, mensaje: str, estado: dict) -> dict:
        """Método que todos los servicios deben implementar"""
        pass
    
    @abstractmethod
    def health_check(self) -> dict:
        """Verificación de salud del servicio"""
        pass
    
    @abstractmethod
    def get_metrics(self) -> dict:
        """Métricas de rendimiento"""
        pass
```

**Implementación por Servicio:**
```python
from Pili_ChatBot.core.base_chatbot import BaseChatBot

class PILIITSEChatBot(BaseChatBot):
    def procesar(self, mensaje, estado):
        # Lógica específica de ITSE
        pass
    
    def health_check(self):
        return {
            'service': 'ITSE',
            'status': 'healthy',
            'version': '1.0.0'
        }
    
    def get_metrics(self):
        return {
            'requests_total': self.request_count,
            'avg_response_time': self.avg_time,
            'error_rate': self.error_rate
        }
```

---

## 🔧 SISTEMA DE MANTENIMIENTO PREDICTIVO

### Inspiración: Google SRE (Site Reliability Engineering)

#### 1. Health Checks Automáticos

**Archivo: `Pili_ChatBot/itse/diagnostics/health_check.py`**
```python
"""
Health Check para servicio ITSE
Basado en Google SRE best practices
"""

class ITSEHealthCheck:
    def __init__(self, chatbot_instance):
        self.bot = chatbot_instance
    
    def check_all(self) -> dict:
        """Ejecuta todos los checks"""
        return {
            'timestamp': datetime.now().isoformat(),
            'service': 'ITSE',
            'checks': {
                'liveness': self.check_liveness(),
                'readiness': self.check_readiness(),
                'dependencies': self.check_dependencies(),
                'performance': self.check_performance()
            },
            'overall_status': self.get_overall_status()
        }
    
    def check_liveness(self) -> dict:
        """¿El servicio está vivo?"""
        try:
            # Test básico
            result = self.bot.procesar("", None)
            return {'status': 'pass', 'message': 'Service is alive'}
        except Exception as e:
            return {'status': 'fail', 'error': str(e)}
    
    def check_readiness(self) -> dict:
        """¿El servicio está listo para recibir tráfico?"""
        checks = {
            'knowledge_base_loaded': self._check_kb(),
            'pricing_data_loaded': self._check_pricing(),
            'memory_usage': self._check_memory()
        }
        
        all_pass = all(c['status'] == 'pass' for c in checks.values())
        return {
            'status': 'pass' if all_pass else 'fail',
            'checks': checks
        }
    
    def check_dependencies(self) -> dict:
        """¿Las dependencias están disponibles?"""
        return {
            'python_version': sys.version,
            'required_modules': self._check_modules()
        }
    
    def check_performance(self) -> dict:
        """Métricas de rendimiento"""
        # Medir tiempo de respuesta
        start = time.time()
        self.bot.procesar("SALUD", {'etapa': 'categoria'})
        response_time = time.time() - start
        
        return {
            'avg_response_time_ms': response_time * 1000,
            'status': 'pass' if response_time < 1.0 else 'warn'
        }
```

#### 2. Monitoreo de Métricas

**Archivo: `Pili_ChatBot/itse/diagnostics/performance_monitor.py`**
```python
"""
Performance Monitor para servicio ITSE
Basado en Prometheus metrics
"""

class ITSEPerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_error': 0,
            'response_times': [],
            'errors': []
        }
    
    def record_request(self, success: bool, response_time: float, error=None):
        """Registra una petición"""
        self.metrics['requests_total'] += 1
        
        if success:
            self.metrics['requests_success'] += 1
        else:
            self.metrics['requests_error'] += 1
            if error:
                self.metrics['errors'].append({
                    'timestamp': datetime.now(),
                    'error': str(error)
                })
        
        self.metrics['response_times'].append(response_time)
    
    def get_metrics(self) -> dict:
        """Obtiene métricas actuales"""
        response_times = self.metrics['response_times']
        
        return {
            'requests': {
                'total': self.metrics['requests_total'],
                'success': self.metrics['requests_success'],
                'error': self.metrics['requests_error'],
                'success_rate': self._calculate_success_rate()
            },
            'performance': {
                'avg_response_time_ms': np.mean(response_times) * 1000 if response_times else 0,
                'p50_response_time_ms': np.percentile(response_times, 50) * 1000 if response_times else 0,
                'p95_response_time_ms': np.percentile(response_times, 95) * 1000 if response_times else 0,
                'p99_response_time_ms': np.percentile(response_times, 99) * 1000 if response_times else 0
            },
            'errors': {
                'recent_errors': self.metrics['errors'][-10:],  # Últimos 10 errores
                'error_rate': self._calculate_error_rate()
            }
        }
    
    def _calculate_success_rate(self) -> float:
        total = self.metrics['requests_total']
        if total == 0:
            return 100.0
        return (self.metrics['requests_success'] / total) * 100
    
    def _calculate_error_rate(self) -> float:
        return 100.0 - self._calculate_success_rate()
```

---

## 🔍 SCRIPTS DE DIAGNÓSTICO AUTOMÁTICO

### Script 1: Diagnóstico Completo de Servicio

**Archivo: `diagnostico_servicio.py`**
```python
#!/usr/bin/env python3
"""
Script de diagnóstico automático para servicios PILI
Uso: python diagnostico_servicio.py itse
"""

import sys
import json
from datetime import datetime

def diagnosticar_servicio(servicio_nombre: str):
    """Ejecuta diagnóstico completo de un servicio"""
    
    print(f"{'='*60}")
    print(f"🔍 DIAGNÓSTICO AUTOMÁTICO: {servicio_nombre.upper()}")
    print(f"{'='*60}\n")
    
    # 1. Importar servicio
    try:
        modulo = importar_servicio(servicio_nombre)
        print("✅ Módulo importado correctamente")
    except Exception as e:
        print(f"❌ Error importando módulo: {e}")
        return generar_reporte_fallo('import_error', str(e))
    
    # 2. Health Check
    try:
        health = modulo.health_check()
        print(f"✅ Health Check: {health['overall_status']}")
    except Exception as e:
        print(f"❌ Health Check falló: {e}")
        return generar_reporte_fallo('health_check_error', str(e))
    
    # 3. Test de Funcionalidad
    try:
        resultado = test_funcionalidad(modulo)
        print(f"✅ Test de funcionalidad: PASS")
    except Exception as e:
        print(f"❌ Test de funcionalidad: FAIL - {e}")
        return generar_reporte_fallo('functionality_error', str(e))
    
    # 4. Métricas de Rendimiento
    try:
        metricas = modulo.get_metrics()
        print(f"✅ Métricas obtenidas")
        print(f"   - Tiempo promedio: {metricas['performance']['avg_response_time_ms']:.2f}ms")
        print(f"   - Tasa de éxito: {metricas['requests']['success_rate']:.2f}%")
    except Exception as e:
        print(f"⚠️ No se pudieron obtener métricas: {e}")
    
    # 5. Generar reporte
    reporte = generar_reporte_exitoso(servicio_nombre, health, metricas)
    guardar_reporte(reporte, servicio_nombre)
    
    print(f"\n{'='*60}")
    print(f"✅ DIAGNÓSTICO COMPLETADO")
    print(f"📄 Reporte guardado en: DIAGNOSTICO_{servicio_nombre.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    print(f"{'='*60}\n")
    
    return reporte

def test_funcionalidad(modulo):
    """Test básico de funcionalidad"""
    # Test 1: Estado inicial
    r1 = modulo.procesar("", None)
    assert r1['success'] == True
    
    # Test 2: Procesar mensaje
    r2 = modulo.procesar("SALUD", {'etapa': 'categoria'})
    assert r2['success'] == True
    assert r2['estado']['etapa'] == 'tipo'
    
    return True

def generar_reporte_exitoso(servicio, health, metricas):
    return {
        'timestamp': datetime.now().isoformat(),
        'servicio': servicio,
        'status': 'SUCCESS',
        'health_check': health,
        'metricas': metricas,
        'recomendaciones': generar_recomendaciones(metricas)
    }

def generar_recomendaciones(metricas):
    """Genera recomendaciones basadas en métricas"""
    recomendaciones = []
    
    # Check tiempo de respuesta
    avg_time = metricas['performance']['avg_response_time_ms']
    if avg_time > 1000:
        recomendaciones.append({
            'tipo': 'PERFORMANCE',
            'severidad': 'HIGH',
            'mensaje': f'Tiempo de respuesta alto ({avg_time:.2f}ms). Optimizar lógica de procesamiento.'
        })
    
    # Check tasa de error
    error_rate = metricas['errors']['error_rate']
    if error_rate > 5:
        recomendaciones.append({
            'tipo': 'RELIABILITY',
            'severidad': 'CRITICAL',
            'mensaje': f'Tasa de error alta ({error_rate:.2f}%). Revisar logs de errores.'
        })
    
    return recomendaciones

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python diagnostico_servicio.py <nombre_servicio>")
        print("Ejemplo: python diagnostico_servicio.py itse")
        sys.exit(1)
    
    servicio = sys.argv[1]
    diagnosticar_servicio(servicio)
```

### Script 2: Diagnóstico de Todos los Servicios

**Archivo: `diagnostico_todos_servicios.py`**
```python
#!/usr/bin/env python3
"""
Diagnóstico de TODOS los servicios
Genera dashboard con estado de cada uno
"""

SERVICIOS = [
    'itse',
    'puesta_tierra',
    'instalaciones',
    'mantenimiento',
    'proyectos',
    'consultoria',
    'capacitacion',
    'auditoria',
    'emergencias',
    'soporte'
]

def diagnosticar_todos():
    resultados = {}
    
    print("🔍 DIAGNÓSTICO DE TODOS LOS SERVICIOS")
    print("="*60)
    
    for servicio in SERVICIOS:
        print(f"\n📦 Diagnosticando {servicio}...")
        try:
            resultado = diagnosticar_servicio(servicio)
            resultados[servicio] = resultado
        except Exception as e:
            resultados[servicio] = {
                'status': 'ERROR',
                'error': str(e)
            }
    
    # Generar dashboard
    generar_dashboard(resultados)
    
    return resultados

def generar_dashboard(resultados):
    """Genera dashboard visual de estado"""
    print("\n" + "="*60)
    print("📊 DASHBOARD DE SERVICIOS")
    print("="*60 + "\n")
    
    print(f"{'Servicio':<20} {'Estado':<15} {'Tiempo Resp.':<15} {'Tasa Éxito':<15}")
    print("-"*65)
    
    for servicio, resultado in resultados.items():
        if resultado['status'] == 'SUCCESS':
            estado = "✅ OK"
            tiempo = f"{resultado['metricas']['performance']['avg_response_time_ms']:.2f}ms"
            tasa = f"{resultado['metricas']['requests']['success_rate']:.2f}%"
        else:
            estado = "❌ ERROR"
            tiempo = "N/A"
            tasa = "N/A"
        
        print(f"{servicio:<20} {estado:<15} {tiempo:<15} {tasa:<15}")
    
    print("\n" + "="*60)
```

---

## 🚀 FLUJO DE TRABAJO DEVOPS

### Inspiración: AWS Well-Architected Framework

#### 1. Desarrollo Local
```bash
# 1. Crear rama feature
git checkout -b feature/nuevo-servicio

# 2. Desarrollar servicio
# ... código ...

# 3. Tests locales
python -m pytest Pili_ChatBot/<servicio>/tests/

# 4. Diagnóstico local
python diagnostico_servicio.py <servicio>

# 5. Commit
git add -A
git commit -m "feat: Nuevo servicio <nombre>"
```

#### 2. Integración Continua (CI)
```yaml
# .github/workflows/ci.yml
name: CI - Tests y Diagnóstico

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest Pili_ChatBot/*/tests/
      
      - name: Run diagnostics
        run: python diagnostico_todos_servicios.py
      
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: diagnostic-report
          path: DIAGNOSTICO_*.json
```

#### 3. Deployment
```bash
# 1. Merge a main
git checkout main
git merge feature/nuevo-servicio

# 2. Tag de versión
git tag v1.1.0
git push origin v1.1.0

# 3. Deploy automático (GitHub Actions)
```

---

## 📊 MÉTRICAS DE ÉXITO

### SLIs (Service Level Indicators)

1. **Disponibilidad:** > 99.9%
2. **Latencia P95:** < 500ms
3. **Tasa de Error:** < 1%
4. **Tiempo de Recuperación:** < 5 minutos

### SLOs (Service Level Objectives)

- **Uptime mensual:** 99.9% (43 minutos de downtime permitido)
- **Tiempo de respuesta:** 95% de requests < 500ms
- **Tasa de éxito:** 99% de requests exitosos

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Fase 1: Migración ITSE (4 horas)
- [ ] Crear backup y rama
- [ ] Crear estructura modular
- [ ] Mover archivos
- [ ] Actualizar imports
- [ ] Tests automáticos
- [ ] Verificación manual
- [ ] Commit y push

### Fase 2: Sistema de Diagnóstico (2 horas)
- [ ] Crear health checks
- [ ] Crear performance monitor
- [ ] Crear scripts de diagnóstico
- [ ] Probar scripts
- [ ] Documentar uso

### Fase 3: Preparar para Escalabilidad (2 horas)
- [ ] Crear clase base
- [ ] Documentar patrón de diseño
- [ ] Crear template para nuevos servicios
- [ ] Actualizar README principal

---

## 📚 DOCUMENTACIÓN

Cada servicio debe tener:

1. **README.md** - Descripción, uso, ejemplos
2. **CHANGELOG.md** - Historial de cambios
3. **API.md** - Documentación de API
4. **TROUBLESHOOTING.md** - Solución de problemas comunes

---

**Archivo:** `PLAN_MAESTRO_ARQUITECTURA_MODULAR.md`  
**Fecha:** 2025-12-31  
**Estado:** Listo para implementación
