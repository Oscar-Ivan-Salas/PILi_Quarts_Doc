# 🎯 PLAN MAESTRO: CENTRALIZAR TODO EN PILI

## 📋 OBJETIVO

**Centralizar TODA la lógica del sistema en la carpeta `pili/`:**

1. ✅ Agentes inteligentes (6 agentes PILI)
2. ✅ Orquestador maestro
3. ✅ Multi-IA (Gemini, Claude, GPT-4, etc.)
4. ✅ Fallbacks cuando no hay conexión
5. ✅ Configuración YAML para 6 tipos de documentos
6. ✅ Knowledge base modular
7. ✅ Tests locales antes de integración

---

## 🌳 ESTRATEGIA DE RAMAS

### Rama 1: `feature/pili-centralized` (TÚ trabajas aquí)
**Responsable:** Antigravity AI  
**Objetivo:** Centralizar toda la lógica en `pili/`

**Trabajo:**
- Crear estructura completa de `pili/`
- Configurar YAML para 6 tipos de documentos
- Implementar agentes inteligentes
- Implementar orquestador
- Implementar multi-IA + fallbacks
- Tests locales
- Manual de configuración

---

### Rama 2: `feature/professional-docs` (USUARIO trabaja aquí)
**Responsable:** Usuario  
**Objetivo:** Trabajar en documentos profesionales

**Trabajo:**
- Configurar `professional/`
- Instalar dependencias (ChromaDB, spaCy, etc.)
- Integrar componentes profesionales
- Tests de generación de documentos

---

### Rama 3: `main` (Producción)
**Estado:** Estable, funcionando  
**Acción:** NO tocar hasta que ambas ramas estén probadas

---

## 🏗️ ARQUITECTURA FINAL DE PILI/

```
pili/
├── config/
│   ├── services/
│   │   ├── itse.yaml
│   │   ├── electricidad.yaml
│   │   ├── pozo-tierra.yaml
│   │   ├── contraincendios.yaml
│   │   ├── domotica.yaml
│   │   ├── cctv.yaml
│   │   ├── redes.yaml
│   │   ├── saneamiento.yaml
│   │   ├── automatizacion-industrial.yaml
│   │   └── expedientes.yaml
│   │
│   ├── documents/
│   │   ├── cotizacion-simple.yaml
│   │   ├── cotizacion-compleja.yaml
│   │   ├── proyecto-simple.yaml
│   │   ├── proyecto-complejo-pmi.yaml
│   │   ├── informe-tecnico.yaml
│   │   └── informe-ejecutivo-apa.yaml
│   │
│   ├── agents/
│   │   └── pili-agents.yaml (6 agentes)
│   │
│   └── multi-ia.yaml (configuración multi-IA)
│
├── core/
│   ├── orchestrator.py (orquestador maestro)
│   ├── multi_ia_manager.py (gestión multi-IA)
│   ├── fallback_manager.py (fallbacks offline)
│   └── config_loader.py (carga YAML)
│
├── agents/
│   ├── base_agent.py (clase base)
│   ├── cotizadora.py (PILI Cotizadora)
│   ├── analista.py (PILI Analista)
│   ├── coordinadora.py (PILI Coordinadora)
│   ├── project_manager.py (PILI Project Manager)
│   ├── reportera.py (PILI Reportera)
│   └── analista_senior.py (PILI Analista Senior)
│
├── specialists/
│   ├── base_specialist.py
│   ├── universal_specialist.py (UniversalSpecialist)
│   └── specialist_factory.py
│
├── knowledge/
│   ├── itse_kb.py
│   ├── electricidad_kb.py
│   └── ... (resto de KB)
│
├── utils/
│   ├── validators.py
│   ├── formatters.py
│   └── calculators.py
│
├── tests/
│   ├── test_orchestrator.py
│   ├── test_agents.py
│   ├── test_specialists.py
│   └── test_multi_ia.py
│
└── __init__.py (exporta todo)
```

---

## 📝 CONFIGURACIONES YAML

### 1. Agentes PILI (`config/agents/pili-agents.yaml`)

```yaml
# ═══════════════════════════════════════════════════════════════
# 🤖 CONFIGURACIÓN DE AGENTES PILI
# ═══════════════════════════════════════════════════════════════

agents:
  cotizadora:
    nombre: "PILI Cotizadora"
    personalidad: "Amigable, rápida, eficiente"
    especialidad: "Cotizaciones simples (5-15 min)"
    emoji: "💰"
    documentos:
      - cotizacion-simple
    capacidades:
      - "Extracción rápida de datos"
      - "Cálculos automáticos"
      - "Generación de cotizaciones estándar"
    prompt_sistema: |
      Eres PILI Cotizadora, especialista en cotizaciones rápidas.
      Tu objetivo es generar cotizaciones en 5-15 minutos.
      Eres amigable, eficiente y directa.
  
  analista:
    nombre: "PILI Analista"
    personalidad: "Técnica, detallista, precisa"
    especialidad: "Proyectos complejos con OCR"
    emoji: "🔍"
    documentos:
      - cotizacion-compleja
    capacidades:
      - "OCR avanzado (fotos, PDFs)"
      - "Análisis técnico detallado"
      - "Cálculos complejos"
      - "Procesamiento multimodal"
    prompt_sistema: |
      Eres PILI Analista, especialista en proyectos complejos.
      Analizas documentos técnicos, fotos, planos.
      Eres precisa, detallista y técnica.
  
  coordinadora:
    nombre: "PILI Coordinadora"
    personalidad: "Organizada, estructurada, clara"
    especialidad: "Gestión de proyectos simples"
    emoji: "📋"
    documentos:
      - proyecto-simple
    capacidades:
      - "Planificación de proyectos"
      - "Cronogramas básicos"
      - "Asignación de recursos"
    prompt_sistema: |
      Eres PILI Coordinadora, especialista en proyectos simples.
      Organizas, planificas y estructuras proyectos.
      Eres clara, organizada y eficiente.
  
  project_manager:
    nombre: "PILI Project Manager"
    personalidad: "Profesional, metodológica, estratégica"
    especialidad: "Proyectos PMI avanzados"
    emoji: "🎯"
    documentos:
      - proyecto-complejo-pmi
    capacidades:
      - "Metodología PMI"
      - "Gestión de stakeholders"
      - "Análisis de riesgos"
      - "WBS detallado"
      - "KPIs (SPI, CPI)"
    prompt_sistema: |
      Eres PILI Project Manager, certificada PMI.
      Gestionas proyectos complejos con metodología PMI.
      Eres profesional, estratégica y metodológica.
  
  reportera:
    nombre: "PILI Reportera"
    personalidad: "Comunicativa, clara, concisa"
    especialidad: "Informes técnicos"
    emoji: "📄"
    documentos:
      - informe-tecnico
    capacidades:
      - "Redacción técnica"
      - "Análisis de datos"
      - "Conclusiones fundamentadas"
    prompt_sistema: |
      Eres PILI Reportera, especialista en informes técnicos.
      Redactas informes claros, concisos y técnicos.
      Eres comunicativa y profesional.
  
  analista_senior:
    nombre: "PILI Analista Senior"
    personalidad: "Ejecutiva, estratégica, formal"
    especialidad: "Informes ejecutivos APA"
    emoji: "📊"
    documentos:
      - informe-ejecutivo-apa
    capacidades:
      - "Formato APA 7ma edición"
      - "Análisis estratégico"
      - "Métricas ejecutivas (ROI, TIR)"
      - "Gráficos profesionales"
    prompt_sistema: |
      Eres PILI Analista Senior, especialista en informes ejecutivos.
      Redactas informes formato APA con análisis estratégico.
      Eres ejecutiva, formal y estratégica.
```

---

### 2. Multi-IA (`config/multi-ia.yaml`)

```yaml
# ═══════════════════════════════════════════════════════════════
# 🌐 CONFIGURACIÓN MULTI-IA
# ═══════════════════════════════════════════════════════════════

multi_ia:
  enabled: true
  fallback_mode: "pili_brain"  # Cuando no hay conexión
  
  providers:
    gemini:
      enabled: true
      priority: 1
      api_key_env: "GEMINI_API_KEY"
      model: "gemini-1.5-pro"
      max_tokens: 8000
      temperature: 0.7
      use_for:
        - "cotizacion-simple"
        - "cotizacion-compleja"
        - "proyecto-simple"
        - "proyecto-complejo-pmi"
        - "informe-tecnico"
        - "informe-ejecutivo-apa"
    
    claude:
      enabled: false
      priority: 2
      api_key_env: "ANTHROPIC_API_KEY"
      model: "claude-3-opus-20240229"
      max_tokens: 4000
      temperature: 0.7
      use_for:
        - "informe-ejecutivo-apa"
        - "proyecto-complejo-pmi"
    
    gpt4:
      enabled: false
      priority: 3
      api_key_env: "OPENAI_API_KEY"
      model: "gpt-4-turbo-preview"
      max_tokens: 4000
      temperature: 0.7
      use_for:
        - "cotizacion-compleja"
        - "informe-ejecutivo-apa"
    
    groq:
      enabled: false
      priority: 4
      api_key_env: "GROQ_API_KEY"
      model: "llama3-70b-8192"
      max_tokens: 8000
      temperature: 0.7
      use_for:
        - "cotizacion-simple"
    
    together:
      enabled: false
      priority: 5
      api_key_env: "TOGETHER_API_KEY"
      model: "meta-llama/Llama-3-70b-chat-hf"
      max_tokens: 4000
      temperature: 0.7
      use_for:
        - "proyecto-simple"
  
  fallback:
    pili_brain:
      enabled: true
      description: "Fallback offline cuando no hay conexión a IA"
      capabilities:
        - "Cálculos básicos"
        - "Generación de estructura"
        - "Datos demo"
    
    retry_strategy:
      max_retries: 3
      retry_delay: 2  # segundos
      backoff_multiplier: 2
```

---

### 3. Documentos (`config/documents/cotizacion-simple.yaml`)

```yaml
# ═══════════════════════════════════════════════════════════════
# 📄 CONFIGURACIÓN: COTIZACIÓN SIMPLE
# ═══════════════════════════════════════════════════════════════

document:
  type: "cotizacion-simple"
  name: "Cotización Simple"
  description: "Cotización rápida para servicios eléctricos estándar"
  agent: "cotizadora"
  tiempo_estimado: "5-15 minutos"
  
  flujo_conversacional:
    etapas:
      - id: "servicio"
        type: "buttons"
        message: "¿Qué servicio necesitas?"
        opciones:
          - { text: "⚡ Instalación Eléctrica", value: "electrico-residencial" }
          - { text: "🔌 Pozo a Tierra", value: "pozo-tierra" }
          - { text: "🔥 Contraincendios", value: "contraincendios" }
          - { text: "🏠 Domótica", value: "domotica" }
        next: "area"
      
      - id: "area"
        type: "input_number"
        message: "¿Cuál es el área en m²?"
        validacion:
          min: 10
          max: 10000
          type: "float"
        next: "datos_cliente"
      
      - id: "datos_cliente"
        type: "input_text"
        message: "¿Nombre del cliente?"
        validacion:
          min_length: 2
          max_length: 100
        next: "generar"
      
      - id: "generar"
        type: "generate"
        calculator: "calculate_simple_quote"
        template: "cotizacion_simple"
  
  estructura_documento:
    secciones:
      - "encabezado"
      - "datos_cliente"
      - "items"
      - "totales"
      - "observaciones"
    
    campos_requeridos:
      - "numero"
      - "fecha"
      - "cliente"
      - "servicio"
      - "area_m2"
      - "items"
      - "subtotal"
      - "igv"
      - "total"
    
    campos_opcionales:
      - "vigencia"
      - "observaciones"
      - "condiciones_pago"
  
  calculos:
    precios_base:
      electrico-residencial:
        hasta_100m2: 1500
        hasta_500m2: 3500
        mas_500m2: 5000
      
      pozo-tierra:
        basico: 450
        intermedio: 850
        avanzado: 1200
    
    igv: 0.18
    
    formulas:
      subtotal: "sum(items.subtotal)"
      igv: "subtotal * 0.18"
      total: "subtotal + igv"
```

---

## 🔧 CÓDIGO CORE

### 1. Orquestador Maestro (`core/orchestrator.py`)

```python
"""
🎯 ORQUESTADOR MAESTRO PILI
Centraliza TODA la lógica del sistema
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from .multi_ia_manager import MultiIAManager
from .fallback_manager import FallbackManager
from .config_loader import ConfigLoader
from ..agents import AgentFactory
from ..specialists import SpecialistFactory

logger = logging.getLogger(__name__)


class PILIOrchestrator:
    """
    Orquestador maestro que coordina:
    - Agentes inteligentes
    - Multi-IA
    - Especialistas
    - Fallbacks
    """
    
    def __init__(self):
        """Inicializa el orquestador"""
        
        # Cargar configuraciones
        self.config_loader = ConfigLoader()
        self.agents_config = self.config_loader.load_agents()
        self.multi_ia_config = self.config_loader.load_multi_ia()
        
        # Inicializar componentes
        self.multi_ia = MultiIAManager(self.multi_ia_config)
        self.fallback = FallbackManager()
        self.agent_factory = AgentFactory(self.agents_config)
        self.specialist_factory = SpecialistFactory()
        
        logger.info("🎯 PILI Orchestrator inicializado")
    
    async def process_request(
        self,
        message: str,
        document_type: str,
        service_type: str = None,
        conversation_state: Dict = None,
        use_ia: bool = True
    ) -> Dict[str, Any]:
        """
        Procesa una solicitud completa.
        
        Args:
            message: Mensaje del usuario
            document_type: Tipo de documento a generar
            service_type: Tipo de servicio (itse, electricidad, etc.)
            conversation_state: Estado de conversación
            use_ia: Si usar IA o solo fallback
        
        Returns:
            Respuesta completa con documento generado
        """
        try:
            logger.info(f"📨 Procesando: {document_type}")
            
            # 1. Seleccionar agente apropiado
            agent = self.agent_factory.create_agent(document_type)
            logger.info(f"🤖 Agente seleccionado: {agent.name}")
            
            # 2. Si hay service_type, usar especialista
            if service_type:
                specialist = self.specialist_factory.create(service_type)
                response = specialist.process_message(message, conversation_state)
                
                # Si la conversación no está completa, retornar
                if response.get('state', {}).get('stage') != 'completed':
                    return response
                
                # Extraer datos generados
                data = response.get('datos_generados', {})
            else:
                # Extraer datos del mensaje con IA o fallback
                if use_ia and self.multi_ia.is_available():
                    data = await self.multi_ia.extract_data(
                        message, 
                        document_type,
                        agent.prompt_sistema
                    )
                else:
                    data = self.fallback.extract_data(message, document_type)
            
            # 3. Generar documento con agente
            document = await agent.generate_document(data, document_type)
            
            return {
                "success": True,
                "agent": agent.name,
                "document": document,
                "data": data
            }
            
        except Exception as e:
            logger.error(f"❌ Error en orquestador: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_available_agents(self) -> list:
        """Retorna lista de agentes disponibles"""
        return self.agent_factory.list_agents()
    
    def get_available_services(self) -> list:
        """Retorna lista de servicios disponibles"""
        return self.specialist_factory.list_services()
```

---

### 2. Multi-IA Manager (`core/multi_ia_manager.py`)

```python
"""
🌐 GESTOR MULTI-IA
Maneja múltiples proveedores de IA con fallbacks
"""

import logging
from typing import Dict, Any, Optional
import os

logger = logging.getLogger(__name__)


class MultiIAManager:
    """
    Gestiona múltiples proveedores de IA:
    - Gemini (Google)
    - Claude (Anthropic)
    - GPT-4 (OpenAI)
    - Groq
    - Together AI
    """
    
    def __init__(self, config: Dict):
        """Inicializa el gestor multi-IA"""
        self.config = config
        self.providers = {}
        
        # Inicializar proveedores disponibles
        self._init_providers()
    
    def _init_providers(self):
        """Inicializa los proveedores de IA"""
        for provider_name, provider_config in self.config['providers'].items():
            if not provider_config.get('enabled', False):
                continue
            
            # Verificar API key
            api_key_env = provider_config.get('api_key_env')
            api_key = os.getenv(api_key_env)
            
            if not api_key:
                logger.warning(f"⚠️ {provider_name}: API key no encontrada")
                continue
            
            # Inicializar proveedor
            try:
                if provider_name == 'gemini':
                    from .providers.gemini_provider import GeminiProvider
                    self.providers[provider_name] = GeminiProvider(api_key, provider_config)
                
                elif provider_name == 'claude':
                    from .providers.claude_provider import ClaudeProvider
                    self.providers[provider_name] = ClaudeProvider(api_key, provider_config)
                
                elif provider_name == 'gpt4':
                    from .providers.openai_provider import OpenAIProvider
                    self.providers[provider_name] = OpenAIProvider(api_key, provider_config)
                
                # ... resto de proveedores
                
                logger.info(f"✅ {provider_name} inicializado")
                
            except Exception as e:
                logger.error(f"❌ Error inicializando {provider_name}: {e}")
    
    def is_available(self) -> bool:
        """Verifica si hay al menos un proveedor disponible"""
        return len(self.providers) > 0
    
    async def extract_data(
        self,
        message: str,
        document_type: str,
        system_prompt: str
    ) -> Dict[str, Any]:
        """
        Extrae datos del mensaje usando el mejor proveedor disponible.
        
        Intenta con proveedores en orden de prioridad.
        """
        # Ordenar proveedores por prioridad
        sorted_providers = sorted(
            self.providers.items(),
            key=lambda x: self.config['providers'][x[0]]['priority']
        )
        
        for provider_name, provider in sorted_providers:
            try:
                logger.info(f"🔄 Intentando con {provider_name}")
                
                data = await provider.extract_data(
                    message,
                    document_type,
                    system_prompt
                )
                
                logger.info(f"✅ Datos extraídos con {provider_name}")
                return data
                
            except Exception as e:
                logger.warning(f"⚠️ {provider_name} falló: {e}")
                continue
        
        # Si todos fallaron, lanzar error
        raise Exception("Todos los proveedores de IA fallaron")
```

---

## 📋 PLAN DE IMPLEMENTACIÓN

### FASE 1: Crear Rama y Estructura (1 hora)

```bash
# Crear rama
git checkout -b feature/pili-centralized

# Crear estructura
mkdir -p backend/app/services/pili/config/{services,documents,agents}
mkdir -p backend/app/services/pili/core
mkdir -p backend/app/services/pili/agents
mkdir -p backend/app/services/pili/specialists
mkdir -p backend/app/services/pili/utils
mkdir -p backend/app/services/pili/tests
```

---

### FASE 2: Configuraciones YAML (3 horas)

- [ ] Crear `pili-agents.yaml` (6 agentes)
- [ ] Crear `multi-ia.yaml` (configuración multi-IA)
- [ ] Crear 6 archivos `documents/*.yaml` (uno por tipo de documento)
- [ ] Migrar 10 archivos `services/*.yaml` (ya existen)

---

### FASE 3: Core (4 horas)

- [ ] Implementar `orchestrator.py`
- [ ] Implementar `multi_ia_manager.py`
- [ ] Implementar `fallback_manager.py`
- [ ] Implementar `config_loader.py`

---

### FASE 4: Agentes (4 horas)

- [ ] Implementar `base_agent.py`
- [ ] Implementar 6 agentes (cotizadora, analista, etc.)
- [ ] Implementar `agent_factory.py`

---

### FASE 5: Tests Locales (3 horas)

- [ ] Tests de orquestador
- [ ] Tests de agentes
- [ ] Tests de multi-IA
- [ ] Tests de fallbacks

---

### FASE 6: Manual de Configuración (2 horas)

- [ ] Crear `MANUAL_CONFIGURACION.md`
- [ ] Documentar cada YAML
- [ ] Ejemplos de uso
- [ ] Troubleshooting

---

## 📖 MANUAL DE CONFIGURACIÓN

### Archivo: `MANUAL_CONFIGURACION.md`

```markdown
# 📖 MANUAL DE CONFIGURACIÓN PILI

## 🎯 Configurar Agentes

Editar: `pili/config/agents/pili-agents.yaml`

Para agregar un nuevo agente:
1. Copiar estructura de agente existente
2. Cambiar nombre, personalidad, especialidad
3. Definir documentos que maneja
4. Escribir prompt_sistema

## 🌐 Configurar Multi-IA

Editar: `pili/config/multi-ia.yaml`

Para activar un proveedor:
1. Cambiar `enabled: true`
2. Configurar API key en `.env`
3. Ajustar prioridad (1 = más alta)

## 📄 Configurar Documentos

Editar: `pili/config/documents/{tipo}.yaml`

Para modificar flujo conversacional:
1. Editar `flujo_conversacional.etapas`
2. Agregar/quitar etapas
3. Cambiar validaciones

## 🧪 Probar Localmente

```bash
# Test de orquestador
python -m pytest pili/tests/test_orchestrator.py

# Test de agente específico
python -m pytest pili/tests/test_agents.py::test_cotizadora

# Test de multi-IA
python -m pytest pili/tests/test_multi_ia.py
```
```

---

## ✅ CHECKLIST DE TRABAJO

### Tu Trabajo (Rama `feature/pili-centralized`)

- [ ] Crear rama
- [ ] Crear estructura de carpetas
- [ ] Implementar configuraciones YAML
- [ ] Implementar core (orchestrator, multi-IA, fallbacks)
- [ ] Implementar agentes
- [ ] Tests locales
- [ ] Manual de configuración
- [ ] Commit y push

### Trabajo del Usuario (Rama `feature/professional-docs`)

- [ ] Crear rama
- [ ] Configurar `professional/`
- [ ] Instalar dependencias
- [ ] Integrar componentes
- [ ] Tests de generación
- [ ] Commit y push

### Integración Final (Ambos)

- [ ] Merge `feature/pili-centralized` a `main`
- [ ] Merge `feature/professional-docs` a `main`
- [ ] Tests de integración
- [ ] Deploy

---

## 🎯 PRÓXIMO PASO INMEDIATO

¿Quieres que empiece creando la rama `feature/pili-centralized` y la estructura de carpetas?
