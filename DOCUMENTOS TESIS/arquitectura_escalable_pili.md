# 🏗️ ARQUITECTURA ESCALABLE PROFESIONAL PARA PILI

## 🎯 PROBLEMA IDENTIFICADO

**Escala actual:**
- 10 servicios × 6 documentos = 60 especializaciones
- 1,000 líneas por especialista = 60,000 líneas
- **INMANEJABLE** en un solo archivo

## ✅ SOLUCIÓN: ARQUITECTURA MODULAR CON PATRONES PROFESIONALES

---

## 📐 NUEVA ARQUITECTURA PROPUESTA

### **Estructura de Carpetas:**

```
backend/app/services/pili/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── base_specialist.py          # Clase base abstracta
│   ├── conversation_engine.py      # Motor de conversación
│   ├── validation_engine.py        # Motor de validación
│   └── calculation_engine.py       # Motor de cálculos
│
├── specialists/                     # 10 servicios
│   ├── __init__.py
│   ├── electricidad/
│   │   ├── __init__.py
│   │   ├── base.py                 # Base electricidad
│   │   ├── cotizacion_simple.py    # 200 líneas
│   │   ├── cotizacion_compleja.py  # 200 líneas
│   │   ├── proyecto_simple.py      # 200 líneas
│   │   ├── proyecto_complejo.py    # 200 líneas
│   │   ├── informe_simple.py       # 200 líneas
│   │   └── informe_ejecutivo.py    # 200 líneas
│   │
│   ├── itse/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── cotizacion_simple.py
│   │   ├── cotizacion_compleja.py
│   │   ├── proyecto_simple.py
│   │   ├── proyecto_complejo.py
│   │   ├── informe_simple.py
│   │   └── informe_ejecutivo.py
│   │
│   ├── pozo_tierra/
│   ├── contraincendios/
│   ├── domotica/
│   ├── cctv/
│   ├── redes/
│   ├── automatizacion/
│   ├── expedientes/
│   └── saneamiento/
│
├── knowledge/                       # Bases de conocimiento
│   ├── __init__.py
│   ├── electricidad_kb.py
│   ├── itse_kb.py
│   ├── pozo_tierra_kb.py
│   └── ...
│
├── templates/                       # Plantillas de conversación
│   ├── __init__.py
│   ├── presentacion.py             # Templates de presentación
│   ├── confirmacion.py             # Templates de confirmación
│   ├── cotizacion.py               # Templates de cotización
│   └── cierre.py                   # Templates de cierre
│
├── utils/
│   ├── __init__.py
│   ├── formatters.py               # Formateo de moneda, fechas
│   ├── validators.py               # Validadores reutilizables
│   └── calculators.py              # Calculadoras reutilizables
│
└── factory.py                       # Factory pattern para crear especialistas
```

**Total:** ~60 archivos de 200-300 líneas cada uno = **MANEJABLE**

---

## 🎨 PATRÓN 1: COMPOSICIÓN EN LUGAR DE HERENCIA

### **Antes (Herencia):**
```python
class ITSESpecialist(LocalSpecialist):
    def _process_itse(self):
        # 1000 líneas de código
        pass
```

### **Después (Composición):**
```python
# core/base_specialist.py
class BaseSpecialist:
    def __init__(self, service_name, document_type):
        self.service = service_name
        self.doc_type = document_type
        self.conversation = ConversationEngine()
        self.validator = ValidationEngine()
        self.calculator = CalculationEngine()
        self.kb = KnowledgeBase.load(service_name)
    
    def process(self, message, state):
        # Lógica genérica usando motores
        pass

# specialists/itse/cotizacion_simple.py
class ITSECotizacionSimple(BaseSpecialist):
    def __init__(self):
        super().__init__("itse", "cotizacion-simple")
        self.stages = self._define_stages()
    
    def _define_stages(self):
        return [
            Stage("categoria", self._ask_categoria),
            Stage("tipo", self._ask_tipo),
            Stage("area", self._ask_area),
            Stage("pisos", self._ask_pisos),
            Stage("cotizacion", self._generate_quote)
        ]
    
    def _ask_categoria(self, state):
        return self.conversation.ask_with_buttons(
            template="itse.presentacion",
            buttons=self.kb.categorias
        )
    
    # Solo 200 líneas - muy manejable
```

---

## 🎨 PATRÓN 2: MOTOR DE CONVERSACIÓN REUTILIZABLE

```python
# core/conversation_engine.py
class ConversationEngine:
    """Motor de conversación reutilizable para todos los especialistas"""
    
    def __init__(self):
        self.templates = ConversationTemplates()
    
    def ask_with_buttons(self, template, buttons, **kwargs):
        """Pregunta con botones dinámicos"""
        text = self.templates.render(template, **kwargs)
        return {
            "texto": text,
            "botones": self._format_buttons(buttons),
            "progreso": kwargs.get("progreso")
        }
    
    def ask_with_input(self, template, example, **kwargs):
        """Pregunta con input de texto"""
        text = self.templates.render(template, example=example, **kwargs)
        return {
            "texto": text,
            "progreso": kwargs.get("progreso")
        }
    
    def confirm_selection(self, template, value, **kwargs):
        """Confirma selección del usuario"""
        text = self.templates.render(template, value=value, **kwargs)
        return {"texto": text}
    
    def generate_quote(self, template, data, **kwargs):
        """Genera cotización visual"""
        text = self.templates.render(template, **data, **kwargs)
        return {
            "texto": text,
            "datos_generados": data,
            "botones": self._get_action_buttons()
        }
```

---

## 🎨 PATRÓN 3: PLANTILLAS DE CONVERSACIÓN (Jinja2-style)

```python
# templates/presentacion.py
TEMPLATES = {
    "itse.presentacion": """¡Hola! 👋 Soy **Pili**, tu especialista en certificados ITSE de **Tesla Electricidad - Huancayo**.

🎯 Te ayudo a obtener tu certificado ITSE con:
✅ Visita técnica GRATUITA
✅ Precios oficiales TUPA Huancayo
✅ Trámite 100% gestionado
✅ Entrega en 7 días hábiles

**Selecciona tu tipo de establecimiento:**""",
    
    "itse.confirm_categoria": "Perfecto, sector **{categoria}**. ¿Qué tipo específico es?",
    
    "itse.confirm_tipo": """Entendido, es un **{tipo}**.

¿Cuál es el área total en m²?

_Escribe el número (ejemplo: 150)_""",
    
    "itse.cotizacion": """💰 **COSTOS DESGLOSADOS:**

🏛️ **Derecho Municipal (TUPA):**
└ S/ {costo_tupa:.2f}

⚡ **Servicio Técnico TESLA:**
└ S/ {costo_servicio:.2f}
└ Incluye: Evaluación + Planos + Gestión + Seguimiento

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **TOTAL ESTIMADO:**
**S/ {total:.2f}**

⏱️ **Tiempo:** 7 días hábiles
🎁 **Visita técnica:** GRATUITA
✅ **Garantía:** 100% aprobación

¿Qué deseas hacer?"""
}

class ConversationTemplates:
    def render(self, template_name, **kwargs):
        template = TEMPLATES.get(template_name, "")
        return template.format(**kwargs)
```

---

## 🎨 PATRÓN 4: FACTORY PATTERN INTELIGENTE

```python
# factory.py
class SpecialistFactory:
    """Factory para crear especialistas dinámicamente"""
    
    _registry = {}
    
    @classmethod
    def register(cls, service, doc_type, specialist_class):
        """Registra un especialista"""
        key = f"{service}:{doc_type}"
        cls._registry[key] = specialist_class
    
    @classmethod
    def create(cls, service, doc_type):
        """Crea un especialista"""
        key = f"{service}:{doc_type}"
        specialist_class = cls._registry.get(key)
        
        if not specialist_class:
            # Fallback a especialista genérico
            return GenericSpecialist(service, doc_type)
        
        return specialist_class()
    
    @classmethod
    def auto_discover(cls):
        """Auto-descubre y registra todos los especialistas"""
        import pkgutil
        import importlib
        
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=['app/services/pili/specialists'],
            prefix='app.services.pili.specialists.'
        ):
            if not ispkg:
                module = importlib.import_module(modname)
                # Auto-registra clases que heredan de BaseSpecialist
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseSpecialist) and obj != BaseSpecialist:
                        service = obj.service_name
                        doc_type = obj.document_type
                        cls.register(service, doc_type, obj)

# Uso:
SpecialistFactory.auto_discover()
specialist = SpecialistFactory.create("itse", "cotizacion-simple")
```

---

## 🎨 PATRÓN 5: CONFIGURATION OVER CODE

```python
# specialists/itse/config.yaml
service: itse
name: "Certificado ITSE"

stages:
  - id: categoria
    type: buttons
    template: itse.presentacion
    buttons_source: kb.categorias
    next: tipo
  
  - id: tipo
    type: buttons
    template: itse.confirm_categoria
    buttons_source: kb.tipos[{categoria}]
    next: area
  
  - id: area
    type: input_number
    template: itse.confirm_tipo
    validation:
      min: 10
      max: 10000
      type: float
    next: pisos
  
  - id: pisos
    type: input_number
    template: itse.ask_pisos
    validation:
      min: 1
      max: 50
      type: int
    next: cotizacion
  
  - id: cotizacion
    type: generate
    template: itse.cotizacion
    calculator: itse_calculator
    actions:
      - agendar_visita
      - mas_informacion
      - enviar_cotizacion
      - nueva_consulta

# specialists/itse/cotizacion_simple.py
class ITSECotizacionSimple(ConfigurableSpecialist):
    config_file = "specialists/itse/config.yaml"
```

---

## 🚀 OPCIÓN AVANZADA: USAR LANGCHAIN + TRANSFORMERS

### **Arquitectura con LangChain:**

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer

# Usar modelo local pequeño (distilgpt2, gpt2-medium)
class TransformerSpecialist:
    def __init__(self, service, doc_type):
        self.service = service
        self.doc_type = doc_type
        
        # Cargar modelo local
        model_name = "distilgpt2"  # 82MB - muy ligero
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Crear pipeline
        self.llm = HuggingFacePipeline.from_model_id(
            model_id=model_name,
            task="text-generation",
            model_kwargs={"temperature": 0.7, "max_length": 200}
        )
        
        # Crear chain con memoria
        self.memory = ConversationBufferMemory()
        self.chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self._create_prompt()
        )
    
    def _create_prompt(self):
        template = """Eres Pili, especialista en {service} de Tesla Electricidad.
Tu trabajo es ayudar al usuario a cotizar {doc_type}.

Contexto del servicio: {knowledge_base}

Conversación:
{history}
Usuario: {input}
Pili:"""
        
        return PromptTemplate(
            input_variables=["service", "doc_type", "knowledge_base", "history", "input"],
            template=template
        )
    
    def process(self, message, state):
        response = self.chain.predict(
            service=self.service,
            doc_type=self.doc_type,
            knowledge_base=self.kb.summary,
            input=message
        )
        return self._parse_response(response)
```

**Ventajas:**
- ✅ Conversación más natural
- ✅ Menos código hardcodeado
- ✅ Modelo local (offline)
- ✅ Escalable

**Desventajas:**
- ❌ Requiere GPU (opcional pero recomendado)
- ❌ Más complejo de debuggear
- ❌ Necesita fine-tuning para mejor calidad

---

## 📊 COMPARACIÓN DE OPCIONES

| Aspecto | Actual (Monolito) | Modular + Patrones | LangChain + Transformers |
|---------|-------------------|-------------------|-------------------------|
| **Líneas por archivo** | 3,500 | 200-300 | 100-200 |
| **Mantenibilidad** | ❌ Difícil | ✅ Fácil | ✅ Muy fácil |
| **Escalabilidad** | ❌ Baja | ✅ Alta | ✅ Muy alta |
| **Complejidad** | Media | Media | Alta |
| **Dependencias** | Ninguna | Ninguna | transformers, langchain |
| **Tamaño descarga** | 0 MB | 0 MB | ~500 MB (modelos) |
| **Calidad conversación** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Tiempo implementación** | - | 2-3 días | 5-7 días |
| **Requiere GPU** | No | No | Recomendado |

---

## ✅ RECOMENDACIÓN FINAL

### **FASE 1: Arquitectura Modular (AHORA)**
- Reorganizar en carpetas por servicio
- Usar patrones de composición
- Implementar motores reutilizables
- Usar templates de conversación

**Beneficios:**
- ✅ Código manejable (200-300 líneas por archivo)
- ✅ Fácil de mantener
- ✅ No requiere dependencias nuevas
- ✅ Se puede hacer en 2-3 días

### **FASE 2: LangChain + Transformers (FUTURO)**
- Cuando el sistema esté estable
- Si necesitas conversación más natural
- Si tienes GPU disponible

---

## 🎯 PLAN DE MIGRACIÓN

### **Paso 1: Crear estructura de carpetas**
```bash
mkdir -p backend/app/services/pili/{core,specialists,knowledge,templates,utils}
```

### **Paso 2: Extraer motores comunes**
- `ConversationEngine`
- `ValidationEngine`
- `CalculationEngine`

### **Paso 3: Migrar ITSE como piloto**
- Crear `specialists/itse/cotizacion_simple.py`
- Usar motores reutilizables
- Probar que funciona

### **Paso 4: Replicar a otros servicios**
- Copiar patrón de ITSE
- Adaptar knowledge base
- Adaptar templates

**Tiempo estimado:** 2-3 días
**Resultado:** Código 100% manejable y escalable

---

## 🚀 ¿PROCEDEMOS?

**Opción A:** Arquitectura modular (recomendado para ahora)
**Opción B:** LangChain + Transformers (para el futuro)
**Opción C:** Ambas (modular ahora, transformers después)

¿Cuál prefieres?
