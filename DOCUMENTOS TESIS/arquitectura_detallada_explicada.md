# 🏗️ ARQUITECTURA BASADA EN CONFIGURACIÓN - EXPLICACIÓN DETALLADA

## 📚 ÍNDICE
1. Visión General con Analogía
2. Estructura de Carpetas Explicada
3. Flujo Completo Paso a Paso
4. Código de Cada Componente
5. Ejemplo Práctico Completo
6. Comparación Antes/Después

---

## 🎯 1. VISIÓN GENERAL CON ANALOGÍA

### **Analogía: Restaurante de Comida Rápida**

**ANTES (Tu código actual):**
```
Tienes 10 cocineros diferentes:
- Cocinero de hamburguesas
- Cocinero de pizzas
- Cocinero de tacos
...

Cada cocinero sabe hacer TODO:
- Tomar orden
- Cocinar
- Servir
- Cobrar

Problema: Si cambias cómo se toma la orden,
         tienes que enseñar a los 10 cocineros.
```

**DESPUÉS (Arquitectura basada en configuración):**
```
Tienes UN SOLO sistema con roles especializados:

1. RECEPCIONISTA (ConversationEngine)
   - Toma órdenes
   - Hace preguntas
   - Confirma datos

2. COCINERO (CalculationEngine)
   - Cocina según receta
   - Calcula precios
   - Prepara orden

3. CAJERO (ValidationEngine)
   - Valida datos
   - Verifica información

4. RECETAS (Archivos YAML)
   - Hamburguesa: pan + carne + lechuga
   - Pizza: masa + salsa + queso
   - Taco: tortilla + carne + salsa

Ventaja: Si cambias cómo se toma la orden,
         solo cambias al RECEPCIONISTA (1 lugar).
         Si agregas un nuevo plato,
         solo agregas una RECETA nueva.
```

---

## 📁 2. ESTRUCTURA DE CARPETAS EXPLICADA

```
backend/app/services/pili/
│
├── 📂 core/                          # MOTORES REUTILIZABLES
│   ├── conversation_engine.py        # Motor de conversación
│   ├── validation_engine.py          # Motor de validación
│   └── calculation_engine.py         # Motor de cálculos
│
├── 📂 config/                        # CONFIGURACIONES (RECETAS)
│   ├── itse.yaml                     # Receta para ITSE
│   ├── electricidad.yaml             # Receta para Electricidad
│   ├── pozo_tierra.yaml              # Receta para Pozo a Tierra
│   └── ... (7 más)
│
├── 📂 templates/                     # PLANTILLAS DE MENSAJES
│   └── messages.yaml                 # Todos los mensajes
│
├── 📂 knowledge/                     # BASES DE CONOCIMIENTO
│   ├── itse_kb.py                    # Datos de ITSE
│   ├── electricidad_kb.py            # Datos de Electricidad
│   └── ... (8 más)
│
└── 📄 specialist.py                  # CLASE UNIVERSAL (CEREBRO)
```

### **¿Qué hace cada carpeta?**

#### **A) core/ - Los Motores (Los Trabajadores)**

**ConversationEngine** = El que habla con el usuario
```python
# Sabe:
- Hacer preguntas
- Mostrar botones
- Confirmar respuestas
- Generar cotizaciones visuales

# NO sabe:
- Qué preguntar (eso está en YAML)
- Cómo calcular (eso está en CalculationEngine)
```

**ValidationEngine** = El que valida datos
```python
# Sabe:
- Validar números
- Validar rangos
- Validar formatos

# NO sabe:
- Qué validar (eso está en YAML)
```

**CalculationEngine** = El que calcula
```python
# Sabe:
- Calcular precios
- Calcular totales
- Aplicar descuentos

# NO sabe:
- Qué calcular (eso está en YAML)
```

#### **B) config/ - Las Recetas (Qué hacer)**

**itse.yaml** = Receta para ITSE
```yaml
# Define:
- Qué preguntas hacer
- En qué orden
- Qué validar
- Cómo calcular
```

**electricidad.yaml** = Receta para Electricidad
```yaml
# Define:
- Qué preguntas hacer (diferentes a ITSE)
- En qué orden (diferente a ITSE)
- Qué validar (diferente a ITSE)
- Cómo calcular (diferente a ITSE)
```

#### **C) templates/ - Los Mensajes (Qué decir)**

**messages.yaml** = Todos los mensajes
```yaml
itse:
  presentacion: "¡Hola! Soy Pili, especialista en ITSE..."
  confirm_categoria: "Perfecto, sector {categoria}..."
  
electricidad:
  presentacion: "¡Hola! Soy Pili, especialista en Electricidad..."
  confirm_tipo: "Entendido, instalación {tipo}..."
```

#### **D) specialist.py - El Cerebro (Coordina todo)**

```python
# Lee la receta (YAML)
# Usa los motores (core/)
# Genera mensajes (templates/)
# Retorna respuesta
```

---

## 🔄 3. FLUJO COMPLETO PASO A PASO

### **Ejemplo: Usuario pide certificado ITSE**

```
┌─────────────────────────────────────────────────────────────┐
│ PASO 1: Usuario envía mensaje                              │
│ "Necesito certificado ITSE"                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 2: Frontend llama al backend                          │
│ POST /api/pili/process                                      │
│ {                                                           │
│   "service": "itse",                                        │
│   "document_type": "cotizacion-simple",                     │
│   "message": "Necesito certificado ITSE",                   │
│   "state": {}                                               │
│ }                                                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 3: specialist.py crea instancia                       │
│ specialist = UniversalSpecialist("itse", "cotizacion-simple")│
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 4: specialist.py carga configuración                  │
│ Abre: config/itse.yaml                                      │
│ Lee: stages para "cotizacion-simple"                        │
│ Encuentra: 5 stages (categoria, tipo, area, pisos, quote)  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 5: specialist.py identifica stage actual              │
│ state = {} (vacío) → stage = "initial"                      │
│ Busca en YAML: stage con id="categoria" (el primero)       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 6: specialist.py procesa stage                        │
│ Stage config:                                               │
│   type: buttons                                             │
│   message_template: "itse.presentacion"                     │
│   data_source: "kb.categorias"                              │
│   next: "tipo"                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 7: ConversationEngine genera mensaje                  │
│ Lee template: "itse.presentacion" de messages.yaml         │
│ Texto: "¡Hola! Soy Pili, especialista en ITSE..."          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 8: specialist.py obtiene botones                      │
│ Lee: kb.categorias de itse_kb.py                            │
│ Botones: [Salud, Educación, Hospedaje, Comercio, ...]      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 9: Retorna respuesta al frontend                      │
│ {                                                           │
│   "texto": "¡Hola! Soy Pili...",                            │
│   "botones": [                                              │
│     {"text": "🏥 Salud", "value": "SALUD"},                │
│     {"text": "🎓 Educación", "value": "EDUCACION"}         │
│   ],                                                        │
│   "stage": "tipo",                                          │
│   "progreso": "1/5"                                         │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 4. CÓDIGO DE CADA COMPONENTE

### **A) config/itse.yaml (50 líneas)**

```yaml
# Configuración completa para ITSE
service: itse
name: "Certificado ITSE"

# Configuración por tipo de documento
documents:
  # COTIZACIÓN SIMPLE
  cotizacion-simple:
    stages:
      # Stage 1: Seleccionar categoría
      - id: categoria
        type: buttons
        message_template: itse.presentacion
        data_source: kb.categorias
        next: tipo
        progress: 1/5
      
      # Stage 2: Seleccionar tipo específico
      - id: tipo
        type: buttons
        message_template: itse.confirm_categoria
        data_source: kb.tipos[{categoria}]
        next: area
        progress: 2/5
      
      # Stage 3: Ingresar área
      - id: area
        type: input_number
        message_template: itse.ask_area
        validation:
          min: 10
          max: 10000
          type: float
        next: pisos
        progress: 3/5
      
      # Stage 4: Ingresar pisos
      - id: pisos
        type: input_number
        message_template: itse.ask_pisos
        validation:
          min: 1
          max: 50
          type: int
        next: quote
        progress: 4/5
      
      # Stage 5: Generar cotización
      - id: quote
        type: generate_quote
        message_template: itse.cotizacion
        calculator: calculate_itse_quote
        progress: 5/5
        actions:
          - text: "📅 Agendar visita"
            value: AGENDAR
          - text: "💬 Más información"
            value: MAS_INFO
          - text: "🔄 Nueva consulta"
            value: RESTART
  
  # COTIZACIÓN COMPLEJA (más stages)
  cotizacion-compleja:
    stages:
      - id: categoria
        # ... misma estructura pero con más campos
      
      - id: tipo
        # ...
      
      - id: area
        # ...
      
      - id: pisos
        # ...
      
      - id: personal
        type: input_number
        message_template: itse.ask_personal
        validation: {min: 1, max: 500}
        next: equipos
      
      - id: equipos
        type: input_number
        message_template: itse.ask_equipos
        validation: {min: 0, max: 100}
        next: quote
      
      - id: quote
        type: generate_quote
        # ...
```

### **B) templates/messages.yaml (100 líneas)**

```yaml
# Plantillas de mensajes para ITSE
itse:
  presentacion: |
    ¡Hola! 👋 Soy **Pili**, tu especialista en certificados ITSE de **Tesla Electricidad - Huancayo**.
    
    🎯 Te ayudo a obtener tu certificado ITSE con:
    ✅ Visita técnica GRATUITA
    ✅ Precios oficiales TUPA Huancayo
    ✅ Trámite 100% gestionado
    ✅ Entrega en 7 días hábiles
    
    **Selecciona tu tipo de establecimiento:**
  
  confirm_categoria: |
    Perfecto, sector **{categoria}**. ¿Qué tipo específico es?
  
  ask_area: |
    Entendido, es un **{tipo}**.
    
    ¿Cuál es el área total en m²?
    
    _Escribe el número (ejemplo: 150)_
  
  ask_pisos: |
    📐 Área: **{area} m²**
    
    ¿Cuántos pisos tiene el establecimiento?
    
    _Escribe el número (ejemplo: 2)_
  
  cotizacion: |
    💰 **COSTOS DESGLOSADOS:**
    
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
    
    ¿Qué deseas hacer?

# Plantillas para Electricidad
electricidad:
  presentacion: |
    ¡Hola! 👋 Soy **Pili**, tu especialista en instalaciones eléctricas...
  
  # ... más mensajes
```

### **C) core/conversation_engine.py (200 líneas)**

```python
import yaml
from pathlib import Path
from typing import Dict, List, Any

class ConversationEngine:
    """Motor de conversación reutilizable"""
    
    def __init__(self):
        # Cargar todas las plantillas de mensajes
        templates_path = Path("app/services/pili/templates/messages.yaml")
        with open(templates_path, 'r', encoding='utf-8') as f:
            self.templates = yaml.safe_load(f)
    
    def render_message(self, service: str, template_name: str, **kwargs) -> str:
        """
        Renderiza un mensaje desde template
        
        Args:
            service: Nombre del servicio (itse, electricidad, etc.)
            template_name: Nombre del template (presentacion, confirm_categoria, etc.)
            **kwargs: Variables para reemplazar en el template
        
        Returns:
            Mensaje formateado
        """
        # Obtener template
        template = self.templates.get(service, {}).get(template_name, "")
        
        # Reemplazar variables
        try:
            return template.format(**kwargs)
        except KeyError as e:
            # Si falta una variable, retornar template sin formatear
            return template
    
    def create_buttons_response(
        self,
        service: str,
        template_name: str,
        buttons: List[Dict],
        next_stage: str,
        progress: str,
        **template_vars
    ) -> Dict:
        """
        Crea respuesta con botones
        
        Args:
            service: Nombre del servicio
            template_name: Nombre del template de mensaje
            buttons: Lista de botones
            next_stage: Siguiente stage
            progress: Progreso (ej: "2/5")
            **template_vars: Variables para el template
        
        Returns:
            Diccionario con respuesta completa
        """
        # Renderizar mensaje
        text = self.render_message(service, template_name, **template_vars)
        
        # Crear respuesta
        return {
            "texto": text,
            "botones": buttons,
            "stage": next_stage,
            "progreso": progress
        }
    
    def create_input_response(
        self,
        service: str,
        template_name: str,
        next_stage: str,
        progress: str,
        **template_vars
    ) -> Dict:
        """Crea respuesta que espera input del usuario"""
        text = self.render_message(service, template_name, **template_vars)
        
        return {
            "texto": text,
            "stage": next_stage,
            "progreso": progress
        }
    
    def create_quote_response(
        self,
        service: str,
        template_name: str,
        quote_data: Dict,
        actions: List[Dict]
    ) -> Dict:
        """Crea respuesta con cotización"""
        text = self.render_message(service, template_name, **quote_data)
        
        return {
            "texto": text,
            "botones": actions,
            "datos_generados": quote_data,
            "stage": "completed",
            "progreso": quote_data.get("progress", "5/5")
        }
```

### **D) core/validation_engine.py (100 líneas)**

```python
import re
from typing import Tuple

class ValidationEngine:
    """Motor de validación reutilizable"""
    
    def validate_number(
        self,
        value: str,
        min_val: float = None,
        max_val: float = None,
        value_type: str = "float"
    ) -> Tuple[bool, float, str]:
        """
        Valida un número
        
        Args:
            value: Valor a validar
            min_val: Valor mínimo permitido
            max_val: Valor máximo permitido
            value_type: Tipo de número ("int" o "float")
        
        Returns:
            (es_valido, numero, mensaje_error)
        """
        # Limpiar valor
        value = value.strip().replace(",", ".")
        
        # Intentar convertir
        try:
            if value_type == "int":
                numero = int(float(value))
            else:
                numero = float(value)
        except ValueError:
            return (False, None, "❌ Por favor ingresa un número válido")
        
        # Validar rango mínimo
        if min_val is not None and numero < min_val:
            return (False, None, f"❌ El valor debe ser mayor o igual a {min_val}")
        
        # Validar rango máximo
        if max_val is not None and numero > max_val:
            return (False, None, f"❌ El valor debe ser menor o igual a {max_val}")
        
        return (True, numero, "")
    
    def validate_email(self, email: str) -> Tuple[bool, str]:
        """Valida un email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return (True, "")
        return (False, "❌ Email inválido")
    
    def validate_phone(self, phone: str) -> Tuple[bool, str]:
        """Valida un teléfono"""
        # Limpiar
        phone = re.sub(r'[^\d]', '', phone)
        
        # Validar longitud
        if len(phone) >= 9:
            return (True, "")
        return (False, "❌ Teléfono debe tener al menos 9 dígitos")
```

### **E) core/calculation_engine.py (100 líneas)**

```python
from typing import Dict, Any

class CalculationEngine:
    """Motor de cálculos reutilizable"""
    
    def calculate_itse_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula cotización para ITSE
        
        Args:
            data: Datos recopilados (categoria, tipo, area, pisos)
        
        Returns:
            Diccionario con costos calculados
        """
        # Obtener datos
        categoria = data.get('categoria', '')
        area = data.get('area', 0)
        pisos = data.get('pisos', 1)
        
        # Calcular riesgo
        riesgo = self._calculate_risk(categoria, area, pisos)
        
        # Costo TUPA (fijo según categoría)
        costos_tupa = {
            'SALUD': 703.00,
            'EDUCACION': 450.00,
            'HOSPEDAJE': 550.00,
            'COMERCIO': 400.00,
            'RESTAURANTE': 500.00,
            'OFICINA': 350.00,
            'INDUSTRIAL': 800.00,
            'ENCUENTRO': 600.00
        }
        costo_tupa = costos_tupa.get(categoria, 500.00)
        
        # Costo servicio (según riesgo y área)
        if riesgo == 'ALTO':
            costo_servicio = 800 + (area * 0.5)
        elif riesgo == 'MEDIO':
            costo_servicio = 600 + (area * 0.3)
        else:
            costo_servicio = 400 + (area * 0.2)
        
        # Totales
        subtotal = costo_tupa + costo_servicio
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            'categoria': categoria,
            'tipo': data.get('tipo', ''),
            'area': area,
            'pisos': pisos,
            'riesgo': riesgo,
            'costo_tupa': costo_tupa,
            'costo_servicio': costo_servicio,
            'subtotal': subtotal,
            'igv': igv,
            'total': total,
            'tiempo_entrega': '7 días hábiles',
            'condiciones': 'Visita técnica GRATUITA'
        }
    
    def _calculate_risk(self, categoria: str, area: float, pisos: int) -> str:
        """Calcula nivel de riesgo"""
        if categoria in ['SALUD', 'INDUSTRIAL', 'ENCUENTRO']:
            return 'ALTO'
        elif area > 500 or pisos > 3:
            return 'MEDIO'
        else:
            return 'BAJO'
    
    def calculate_electricidad_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula cotización para Electricidad"""
        # Lógica específica para electricidad
        pass
```

### **F) specialist.py - EL CEREBRO (300 líneas)**

```python
import yaml
from pathlib import Path
from typing import Dict, Any, List
from .core.conversation_engine import ConversationEngine
from .core.validation_engine import ValidationEngine
from .core.calculation_engine import CalculationEngine

class UniversalSpecialist:
    """
    Especialista universal que maneja TODOS los servicios
    basándose en configuración YAML
    """
    
    def __init__(self, service: str, document_type: str):
        self.service = service
        self.document_type = document_type
        
        # Cargar configuración del servicio
        config_path = Path(f"app/services/pili/config/{service}.yaml")
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # Obtener stages para este tipo de documento
        doc_config = self.config['documents'].get(document_type)
        if not doc_config:
            raise ValueError(f"Documento {document_type} no encontrado para {service}")
        
        self.stages = doc_config['stages']
        
        # Cargar knowledge base
        kb_module = __import__(f"app.services.pili.knowledge.{service}_kb", fromlist=['KB'])
        self.kb = kb_module.KB
        
        # Inicializar motores
        self.conversation = ConversationEngine()
        self.validator = ValidationEngine()
        self.calculator = CalculationEngine()
    
    def process(self, message: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario
        
        Args:
            message: Mensaje del usuario
            state: Estado actual de la conversación
        
        Returns:
            Respuesta con texto, botones, etc.
        """
        # Obtener stage actual
        current_stage_id = state.get('stage', 'initial')
        
        # Si es initial, empezar con el primer stage
        if current_stage_id == 'initial':
            current_stage_id = self.stages[0]['id']
        
        # Buscar configuración del stage
        stage_config = self._find_stage(current_stage_id)
        
        if not stage_config:
            return {"error": f"Stage {current_stage_id} no encontrado"}
        
        # Procesar según tipo de stage
        stage_type = stage_config['type']
        
        if stage_type == 'buttons':
            return self._process_buttons_stage(stage_config, message, state)
        
        elif stage_type == 'input_number':
            return self._process_input_number_stage(stage_config, message, state)
        
        elif stage_type == 'generate_quote':
            return self._process_quote_stage(stage_config, message, state)
        
        else:
            return {"error": f"Tipo de stage desconocido: {stage_type}"}
    
    def _find_stage(self, stage_id: str) -> Dict:
        """Busca un stage por ID"""
        for stage in self.stages:
            if stage['id'] == stage_id:
                return stage
        return None
    
    def _process_buttons_stage(self, config: Dict, message: str, state: Dict) -> Dict:
        """Procesa un stage con botones"""
        # Obtener botones desde data_source
        buttons = self._get_data_from_source(config['data_source'], state)
        
        # Formatear botones
        formatted_buttons = [
            {"text": f"{btn['icon']} {btn['name']}", "value": btn['value']}
            for btn in buttons
        ]
        
        # Generar respuesta
        return self.conversation.create_buttons_response(
            service=self.service,
            template_name=config['message_template'],
            buttons=formatted_buttons,
            next_stage=config['next'],
            progress=config.get('progress', ''),
            **state.get('data', {})
        )
    
    def _process_input_number_stage(self, config: Dict, message: str, state: Dict) -> Dict:
        """Procesa un stage con input numérico"""
        # Validar input
        validation = config.get('validation', {})
        is_valid, value, error = self.validator.validate_number(
            message,
            min_val=validation.get('min'),
            max_val=validation.get('max'),
            value_type=validation.get('type', 'float')
        )
        
        if not is_valid:
            # Retornar error
            return {
                "texto": error,
                "stage": config['id'],  # Mantener en el mismo stage
                "progreso": config.get('progress', '')
            }
        
        # Guardar dato
        if 'data' not in state:
            state['data'] = {}
        state['data'][config['id']] = value
        
        # Siguiente stage
        next_stage_config = self._find_stage(config['next'])
        
        # Si el siguiente es buttons, procesarlo
        if next_stage_config['type'] == 'buttons':
            return self._process_buttons_stage(next_stage_config, message, state)
        
        # Si el siguiente es input, mostrar pregunta
        elif next_stage_config['type'] == 'input_number':
            return self.conversation.create_input_response(
                service=self.service,
                template_name=next_stage_config['message_template'],
                next_stage=next_stage_config['id'],
                progress=next_stage_config.get('progress', ''),
                **state.get('data', {})
            )
        
        # Si el siguiente es quote, generar
        elif next_stage_config['type'] == 'generate_quote':
            return self._process_quote_stage(next_stage_config, message, state)
    
    def _process_quote_stage(self, config: Dict, message: str, state: Dict) -> Dict:
        """Procesa stage de generación de cotización"""
        # Obtener función de cálculo
        calculator_name = config['calculator']
        calculator_func = getattr(self.calculator, calculator_name)
        
        # Calcular
        quote_data = calculator_func(state.get('data', {}))
        
        # Obtener acciones
        actions = config.get('actions', [])
        
        # Generar respuesta
        return self.conversation.create_quote_response(
            service=self.service,
            template_name=config['message_template'],
            quote_data=quote_data,
            actions=actions
        )
    
    def _get_data_from_source(self, source: str, state: Dict) -> List[Dict]:
        """
        Obtiene datos desde una fuente
        
        Ejemplos de source:
        - "kb.categorias" → self.kb['categorias']
        - "kb.tipos[{categoria}]" → self.kb['tipos'][state['data']['categoria']]
        """
        # Parsear source
        if source.startswith('kb.'):
            # Remover 'kb.'
            path = source[3:]
            
            # Si tiene variables entre {}
            if '{' in path:
                # Reemplazar variables
                for key, value in state.get('data', {}).items():
                    path = path.replace(f'{{{key}}}', str(value))
            
            # Evaluar path
            parts = path.split('[')
            data = self.kb
            
            for part in parts:
                part = part.rstrip(']').strip('"').strip("'")
                if part:
                    data = data[part]
            
            return data
        
        return []
```

---

## 🎯 5. EJEMPLO PRÁCTICO COMPLETO

### **Conversación completa de ITSE:**

```python
# Crear especialista
specialist = UniversalSpecialist("itse", "cotizacion-simple")

# Estado inicial
state = {}

# Mensaje 1: Usuario inicia
response1 = specialist.process("Hola", state)
print(response1)
# Output:
# {
#   "texto": "¡Hola! 👋 Soy Pili, especialista en ITSE...\n\nSelecciona tu tipo de establecimiento:",
#   "botones": [
#     {"text": "🏥 Salud", "value": "SALUD"},
#     {"text": "🎓 Educación", "value": "EDUCACION"},
#     ...
#   ],
#   "stage": "tipo",
#   "progreso": "1/5"
# }

# Mensaje 2: Usuario selecciona SALUD
state['stage'] = 'tipo'
state['data'] = {'categoria': 'SALUD'}
response2 = specialist.process("SALUD", state)
print(response2)
# Output:
# {
#   "texto": "Perfecto, sector SALUD. ¿Qué tipo específico es?",
#   "botones": [
#     {"text": "Hospital", "value": "HOSPITAL"},
#     {"text": "Clínica", "value": "CLINICA"},
#     ...
#   ],
#   "stage": "area",
#   "progreso": "2/5"
# }

# Mensaje 3: Usuario selecciona Hospital
state['stage'] = 'area'
state['data']['tipo'] = 'HOSPITAL'
response3 = specialist.process("Hospital", state)
# Output:
# {
#   "texto": "Entendido, es un Hospital.\n\n¿Cuál es el área total en m²?...",
#   "stage": "area",
#   "progreso": "3/5"
# }

# Mensaje 4: Usuario ingresa área
response4 = specialist.process("300", state)
# Output:
# {
#   "texto": "📐 Área: 300 m²\n\n¿Cuántos pisos tiene...?",
#   "stage": "pisos",
#   "progreso": "4/5"
# }

# Mensaje 5: Usuario ingresa pisos
state['stage'] = 'pisos'
state['data']['area'] = 300
response5 = specialist.process("2", state)
# Output:
# {
#   "texto": "💰 COSTOS DESGLOSADOS:\n\n🏛️ Derecho Municipal: S/ 703.00...",
#   "botones": [
#     {"text": "📅 Agendar visita", "value": "AGENDAR"},
#     ...
#   ],
#   "datos_generados": {
#     "categoria": "SALUD",
#     "tipo": "HOSPITAL",
#     "area": 300,
#     "pisos": 2,
#     "total": 2009.54,
#     ...
#   },
#   "stage": "completed",
#   "progreso": "5/5"
# }
```

---

## 📊 6. COMPARACIÓN ANTES/DESPUÉS

### **ANTES (Tu código actual):**

```python
# pili_local_specialists.py (3,500 líneas)

class ITSESpecialist(LocalSpecialist):
    def _process_itse(self, message, state):
        if stage == "initial":
            return {
                "texto": "¡Hola! Soy Pili...",  # Hardcodeado
                "botones": [...]  # Hardcodeado
            }
        elif stage == "categoria":
            # 50 líneas de código
            pass
        elif stage == "tipo":
            # 50 líneas de código
            pass
        # ... 200 líneas más

class ElectricidadSpecialist(LocalSpecialist):
    def _process_electricidad(self, message, state):
        if stage == "initial":
            return {
                "texto": "¡Hola! Soy Pili...",  # DUPLICADO
                "botones": [...]  # DUPLICADO
            }
        # ... 200 líneas DUPLICADAS
```

**Problemas:**
- ❌ 3,500 líneas en un archivo
- ❌ Código duplicado masivo
- ❌ Mensajes hardcodeados
- ❌ Difícil de mantener

### **DESPUÉS (Arquitectura basada en configuración):**

```python
# specialist.py (300 líneas)
class UniversalSpecialist:
    def process(self, message, state):
        # Lee configuración YAML
        # Usa motores reutilizables
        # Retorna respuesta
        pass

# config/itse.yaml (50 líneas)
# Define qué hacer

# config/electricidad.yaml (50 líneas)
# Define qué hacer (diferente)

# templates/messages.yaml (100 líneas)
# Define qué decir
```

**Ventajas:**
- ✅ 900 líneas totales
- ✅ 0% código duplicado
- ✅ Mensajes en YAML
- ✅ Fácil de mantener

---

## ✅ CONCLUSIÓN

**¿Entiendes ahora la arquitectura?**

**Resumen:**
1. **Motores** (core/) = Trabajadores especializados
2. **Configuraciones** (config/) = Recetas de qué hacer
3. **Templates** (templates/) = Qué decir
4. **Specialist** = Cerebro que coordina todo

**Ventaja principal:**
- Agregar servicio nuevo = crear YAML de 50 líneas
- Cambiar algo = modificar 1 lugar
- 0% código duplicado

**¿Quieres que implemente esta arquitectura?**
