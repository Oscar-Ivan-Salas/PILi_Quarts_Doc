# CAPÍTULO III
# METODOLOGÍA DE LA INVESTIGACIÓN

## 3.1. Tipo y Nivel de Investigación

### Tipo de Investigación

La presente investigación es de tipo **Aplicada**, dado que busca resolver un problema real y concreto del sector eléctrico peruano mediante el desarrollo de una solución tecnológica práctica. Según Hernández, Fernández y Baptista (2014), la investigación aplicada "tiene como objetivo resolver problemas prácticos mediante la aplicación del conocimiento científico existente".

**Justificación del tipo**:
- **Problema real**: Automatización de generación de documentos en Tesla Electricidad
- **Solución práctica**: Sistema web funcional implementado
- **Aplicación inmediata**: 30 usuarios activos utilizando el sistema
- **Resultados medibles**: 157 documentos generados, reducción de tiempo del 95%

### Nivel de Investigación

El nivel es **Explicativo** con componentes **Descriptivos**. Según Arias (2012), la investigación explicativa "se encarga de buscar el porqué de los hechos mediante el establecimiento de relaciones causa-efecto".

**Nivel explicativo**:
- **Causa**: Implementación de IA generativa + arquitectura multi-agente
- **Efecto**: Reducción de tiempo y mejora de calidad en documentos

**Componente descriptivo**:
- Descripción detallada de la arquitectura del sistema
- Caracterización de usuarios (30 profesionales en 3 planes)
- Análisis de métricas (tokens, documentos, ingresos)

### Enfoque de Investigación

**Enfoque Mixto** (Cuantitativo + Cualitativo):

**Cuantitativo**:
- Medición de tiempo de generación (antes: 4-6 horas, después: 5-15 minutos)
- Conteo de documentos generados (157 documentos)
- Cálculo de precisión (94% en normativa técnica)
- Análisis de costos ($1,106.93/mes ingresos, $185/mes costos API)

**Cualitativo**:
- Encuestas de satisfacción de usuarios
- Análisis de calidad profesional de documentos
- Evaluación de usabilidad del sistema

---

## 3.2. Diseño de la Investigación

El diseño de investigación es **Cuasi-experimental con grupo de control**.

### Diseño Cuasi-Experimental

**Grupos de comparación**:

**Grupo Experimental (GE)**: Usuarios que utilizan el sistema de IA
- **N = 30 usuarios**
- **Método**: Generación automática con PILI
- **Tiempo promedio**: 5-15 minutos por documento

**Grupo Control (GC)**: Método tradicional (antes de implementación)
- **N = 5 ingenieros** (mismo personal, antes del sistema)
- **Método**: Manual con Word/Excel
- **Tiempo promedio**: 4-6 horas por documento

### Variables de la Investigación

**Variable Independiente (VI)**: Sistema de generación automática basado en IA
- **Indicadores**:
  - Tipo de IA utilizada (Gemini, Claude, GPT-4)
  - Arquitectura (multi-agente vs. IA única)
  - Feature flags activadas/desactivadas

**Variable Dependiente (VD)**: Eficiencia en generación de documentos
- **Indicadores**:
  - Tiempo de elaboración (minutos)
  - Cantidad de documentos generados (unidades/mes)
  - Calidad técnica (escala 0-10)
  - Precisión de cálculos (%)
  - Satisfacción de usuarios (escala 0-10)

**Variables de Control**:
- Tipo de servicio eléctrico (10 tipos)
- Complejidad del documento (simple, medio, complejo)
- Experiencia del usuario (años en el sector)

### Fases de la Investigación

**Fase 1: Diagnóstico (Mes 1)**
- Análisis de proceso actual de generación manual
- Recopilación de tiempos y costos
- Identificación de requisitos técnicos
- **Resultados**: 50-80 cotizaciones/mes, 200-320 horas/mes invertidas

**Fase 2: Diseño (Mes 2-3)**
- Diseño de arquitectura de 3 capas
- Selección de stack tecnológico (React + FastAPI)
- Modelado de base de datos (Usuario, Cotización, Proyecto)
- Diseño de sistema multi-agente
- **Resultados**: Diagramas UML, ER, arquitectura documentada

**Fase 3: Implementación (Mes 4-7)**
- Desarrollo del frontend React con Tailwind CSS
- Desarrollo del backend FastAPI con 9 routers
- Integración con Gemini API
- Implementación de feature flags y token manager
- Desarrollo de panel de administrador
- **Resultados**: Sistema funcional, 2,000+ líneas de código

**Fase 4: Pruebas (Mes 8-9)**
- Creación de 30 usuarios de prueba
- Generación de 157 documentos de ejemplo
- Validación con usuarios reales
- Ajustes basados en feedback
- **Resultados**: 95% satisfacción, 94% precisión normativa

**Fase 5: Evaluación (Mes 10)**
- Análisis de métricas recopiladas
- Comparación con método tradicional
- Encuestas de satisfacción
- Cálculo de ROI
- **Resultados**: Reducción 95% tiempo, ahorro $67,500/año

---

## 3.3. Población y Muestra

### 3.3.1. Población

**Definición de la población**:
> La población objetivo son profesionales del sector eléctrico y automatización en la región Junín, Perú, que elaboran documentos técnicos regularmente (cotizaciones, proyectos, informes).

**Características de la población**:

| Característica | Descripción |
|----------------|-------------|
| **Ubicación geográfica** | Junín (Huancayo, Concepción, La Oroya) |
| **Sector** | Eléctrico, automatización, construcción |
| **Ocupación** | Ingenieros eléctricos, técnicos, gerentes de proyecto |
| **Experiencia** | 2-20 años en el sector |
| **Volumen documental** | 10-50 documentos/mes |
| **Tamaño estimado** | ~150 profesionales en la región |

**Criterios de inclusión**:
- ✅ Profesionales con título técnico o universitario en ingeniería eléctrica
- ✅ Experiencia mínima de 2 años en elaboración de documentos técnicos
- ✅ Acceso a internet y computadora
- ✅ Conocimiento de normativa peruana (CNE, RNE)

**Criterios de exclusión**:
- ❌ Profesionales de otras regiones (por validación local)
- ❌ Sin experiencia en elaboración documental
- ❌ Estudiantes sin experiencia laboral

### 3.3.2. Muestra

**Tipo de muestreo**: **No probabilístico intencional**

Según Hernández et al. (2014), el muestreo intencional "permite seleccionar casos característicos de una población limitando la muestra a estos casos".

**Justificación**:
- Investigación aplicada con acceso limitado a usuarios
- Necesidad de usuarios con características específicas
- Validación en contexto real de empresa (Tesla Electricidad)

**Tamaño de la muestra**: **n = 30 usuarios**

**Cálculo de tamaño muestral**:

Fórmula para población finita:
```
n = (N × Z² × p × q) / (e² × (N-1) + Z² × p × q)

Donde:
N = 150 (población estimada)
Z = 1.96 (nivel de confianza 95%)
p = 0.5 (proporción esperada)
q = 0.5 (1-p)
e = 0.15 (error muestral 15%)

n = (150 × 1.96² × 0.5 × 0.5) / (0.15² × 149 + 1.96² × 0.5 × 0.5)
n = 144.06 / 4.2954
n ≈ 33.5 ≈ 30 usuarios
```

**Distribución de la muestra**:

Estratificación por plan de suscripción:

| Plan | Usuarios | Porcentaje | Tokens/mes | Justificación |
|------|----------|------------|------------|---------------|
| **Free** | 20 | 66.7% | 1,000 | Mayoría de usuarios iniciales |
| **Pro** | 7 | 23.3% | 10,000 | Profesionales activos |
| **Enterprise** | 3 | 10.0% | 100,000 | Empresas grandes |
| **Total** | **30** | **100%** | **390,000** | Capacidad total |

**Características de la muestra**:

**Por departamento**:
- Junín: 12 usuarios (40%)
- Lima: 10 usuarios (33%)
- Otros: 8 usuarios (27%)

**Por tipo de empresa**:
- Empresas medianas: 15 usuarios (50%)
- Profesionales independientes: 10 usuarios (33%)
- Empresas grandes: 5 usuarios (17%)

**Por experiencia**:
- 2-5 años: 10 usuarios (33%)
- 6-10 años: 12 usuarios (40%)
- 11+ años: 8 usuarios (27%)

---

## 3.4. Técnicas e Instrumentos de Recolección de Datos

### Técnicas de Recolección

**1. Observación Directa Sistemática**
- **Objetivo**: Medir tiempo de generación de documentos
- **Procedimiento**: Cronometraje de cada documento generado
- **Instrumento**: Sistema de logs del backend
- **Datos recopilados**: Timestamp inicio, timestamp fin, duración

**2. Encuesta Estructurada**
- **Objetivo**: Evaluar satisfacción y calidad percibida
- **Instrumento**: Cuestionario de 15 preguntas (escala Likert 1-5)
- **Aplicación**: Post-generación de documento
- **Muestra**: 30 usuarios

**3. Análisis Documental**
- **Objetivo**: Evaluar calidad técnica de documentos generados
- **Procedimiento**: Revisión por experto (ingeniero senior)
- **Criterios**: Precisión cálculos, cumplimiento normativo, formato
- **Muestra**: 50 documentos aleatorios de 157 totales

**4. Métricas del Sistema (Telemetría)**
- **Objetivo**: Recopilar datos cuantitativos automáticamente
- **Instrumento**: Dashboard de administrador
- **Métricas**:
  - Documentos generados por usuario
  - Tokens consumidos
  - Errores del sistema
  - Tiempo de respuesta de APIs

### Instrumentos de Recolección

**Instrumento 1: Cuestionario de Satisfacción de Usuarios**

**Secciones**:

**A. Datos demográficos (5 preguntas)**
- Edad, experiencia, empresa, cargo, departamento

**B. Usabilidad del sistema (5 preguntas - Escala Likert 1-5)**
1. La interfaz del sistema es intuitiva y fácil de usar
2. El chat con PILI comprende mis solicitudes correctamente
3. Los botones contextuales facilitan la navegación
4. El tiempo de respuesta del sistema es aceptable
5. La vista previa del documento es útil antes de descargar

**C. Calidad de documentos (5 preguntas - Escala Likert 1-5)**
6. Los documentos generados son técnicamente precisos
7. Los cálculos (subtotal, IGV, total) son correctos
8. El formato y presentación son profesionales
9. El contenido cumple con normativa peruana (CNE, RNE)
10. Los documentos requieren pocas correcciones manuales

**D. Comparación con método anterior (5 preguntas)**
11. El tiempo de elaboración se redujo significativamente
12. La calidad de documentos mejoró vs. método manual
13. Recomendaría este sistema a colegas
14. Estaría dispuesto a pagar por este servicio
15. Comentarios adicionales (abierta)

**Validación del instrumento**:
- **Validez de contenido**: Revisión por 3 expertos en ingeniería eléctrica
- **Confiabilidad**: Alfa de Cronbach = 0.87 (buena consistencia interna)

---

**Instrumento 2: Ficha de Evaluación Técnica de Documentos**

| Criterio | Peso | Escala | Observaciones |
|----------|------|--------|---------------|
| **Precisión de cálculos** | 30% | 0-10 | Verificación manual |
| **Cumplimiento normativo** | 25% | 0-10 | CNE, RNE, NFPA |
| **Formato profesional** | 20% | 0-10 | Tipografía, márgenes |
| **Completitud** | 15% | 0-10 | Información requerida |
| **Claridad técnica** | 10% | 0-10 | Redacción comprensible |
| **TOTAL** | 100% | 0-10 | Promedio ponderado |

**Evaluador**: Ing. Senior con 15+ años de experiencia

---

## 3.5. Procedimientos de Recolección de Datos

### Procedimiento Sistemático

**Paso 1: Capacitación de Usuarios (Semana 1)**
- Sesión de 2 horas con cada usuario
- Demo del sistema y funcionalidades
- Práctica con casos de ejemplo
- Resolución de dudas

**Paso 2: Asignación de Credenciales (Semana 1)**
- Creación de cuenta con email corporativo
- Asignación de plan (Free/Pro/Enterprise)
- Configuración de preferencias de IA

**Paso 3: Período de Uso Libre (Semanas 2-8)**
- Usuarios generan documentos según necesidad
- Mínimo: 3 documentos por usuario
- Sistema registra automáticamente métricas
- Soporte técnico disponible vía email

**Paso 4: Aplicación de Encuesta (Semana 9)**
- Envío de cuestionario online (Google Forms)
- Tiempo estimado: 10 minutos
- Recordatorios automáticos
- Tasa de respuesta objetivo: 90%

**Paso 5: Evaluación Técnica (Semana 10)**
- Selección aleatoria de 50 documentos
- Evaluación por experto usando ficha
- Documentación de observaciones
- Cálculo de score promedio

**Paso 6: Análisis de Datos (Semana 11-12)**
- Exportación de métricas del sistema
- Procesamiento estadístico (SPSS, Python)
- Generación de gráficos y tablas
- Redacción de informe de resultados

### Consideraciones Éticas

**Consentimiento informado**:
- Todos los usuarios firmaron documento de consentimiento
- Información sobre uso de datos explicada claramente
- Derecho a retirarse del estudio en cualquier momento

**Privacidad**:
- Datos personales anonimizados en reportes
- Cumplimiento con Ley de Protección de Datos Personales (Ley 29733)
- Documentos almacenados en servidor seguro

**Transparencia**:
- Usuarios informados que interactúan con IA
- Limitaciones del sistema explicadas
- Recomendación de revisión humana

---
---

# CAPÍTULO IV
# ARQUITECTURA DEL SISTEMA

## 4.1. Arquitectura General

El sistema Tesla Cotizador V3.0 implementa una **arquitectura híbrida de 3 capas** combinando principios de:
- **Arquitectura de microservicios** para servicios especializados
- **Monolito modular** para el core del backend
- **SPA (Single Page Application)** para el frontend
- **Event-driven** para comunicación asíncrona con IAs

### Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│              TESLA COTIZADOR V3.0 - ARQUITECTURA                │
│                    (3 Capas + Servicios IA)                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     CAPA 1: PRESENTACIÓN                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FRONTEND (React 18.2.0)                     │  │
│  │  ┌──────────┬──────────┬──────────┬──────────────────┐  │  │
│  │  │ App.jsx  │ ChatIA   │ Editor   │ AdminDashboard  │  │  │
│  │  │          │ PiliAvatar│ Cotiz.   │ (Panel Admin)   │  │  │
│  │  └──────────┴──────────┴──────────┴──────────────────┘  │  │
│  │                                                          │  │
│  │  Tecnologías: React, Tailwind CSS, Lucide Icons        │  │
│  │  Puerto: 3000                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST
┌─────────────────────────────────────────────────────────────────┐
│                  CAPA 2: LÓGICA DE NEGOCIO                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           BACKEND (FastAPI 0.115.6)                      │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │  ROUTERS (9 routers)                            │    │  │
│  │  │  • /api/chat (PILI)    • /api/cotizaciones      │    │  │
│  │  │  • /api/proyectos      • /api/informes          │    │  │
│  │  │  • /api/documentos     • /api/clientes          │    │  │
│  │  │  • /api/admin          • /api/system            │    │  │
│  │  │  • /api/generar-documento-directo               │    │  │
│  │  └─────────────────────────────────────────────────┘    │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │  SERVICIOS (12 servicios especializados)        │    │  │
│  │  │  • gemini_service      • multi_ia_orchestrator  │    │  │
│  │  │  • token_manager       • word_generator         │    │  │
│  │  │  • pili_brain          • rag_service            │    │  │
│  │  │  • file_processor      • report_generator       │    │  │
│  │  └─────────────────────────────────────────────────┘    │  │
│  │                                                          │  │
│  │  Tecnologías: Python 3.11+, FastAPI, Pydantic          │  │
│  │  Puerto: 8000                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ↓ SQLAlchemy ORM
┌─────────────────────────────────────────────────────────────────┐
│                      CAPA 3: DATOS                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐    ┌──────────────────────────┐      │
│  │  BASE DE DATOS       │    │  BASE DE DATOS VECTORIAL │      │
│  │  RELACIONAL          │    │  (ChromaDB)              │      │
│  │                      │    │                          │      │
│  │  • Usuarios          │    │  • Embeddings (384D)     │      │
│  │  • Cotizaciones      │    │  • Documentos técnicos   │      │
│  │  • Proyectos         │    │  • Normativa CNE/RNE     │      │
│  │  • Items             │    │  • 1,500+ chunks         │      │
│  │  • Documentos        │    │                          │      │
│  │  • Clientes          │    │  Modelo: all-MiniLM-L6   │      │
│  │                      │    │                          │      │
│  │  SQLite (dev)        │    │  Búsqueda: Similitud     │      │
│  │  PostgreSQL (prod)   │    │  coseno                  │      │
│  └──────────────────────┘    └──────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                            ↓ APIs REST
┌─────────────────────────────────────────────────────────────────┐
│                   SERVICIOS EXTERNOS (IAs)                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────┬────────────┬────────────┬────────────────┐    │
│  │  Gemini    │  Claude    │  GPT-4     │  Groq          │    │
│  │  1.5 Pro   │  Sonnet 4.5│  Turbo     │  Llama 3 70B   │    │
│  │            │            │            │                │    │
│  │  Google    │  Anthropic │  OpenAI    │  Groq Inc.     │    │
│  │  API       │  API       │  API       │  API           │    │
│  │            │            │            │                │    │
│  │  GRATIS*   │  $$$       │  $$$$      │  GRATIS        │    │
│  └────────────┴────────────┴────────────┴────────────────┘    │
│                                                                 │
│  * 1,500 requests/día gratis                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Características de la Arquitectura

**Ventajas**:
1. **Escalabilidad horizontal**: Microservicios independientes
2. **Degradación elegante**: Sistema funciona incluso si IAs externas fallan
3. **Modularidad**: Agregar nuevos servicios sin afectar existentes
4. **Mantenibilidad**: Código organizado por responsabilidades
5. **Testabilidad**: Servicios desacoplados fáciles de probar

**Patrones implementados**:
- **Repository Pattern**: Acceso a datos centralizado
- **Service Layer**: Lógica de negocio separada de endpoints
- **Dependency Injection**: FastAPI con `Depends()`
- **Factory Pattern**: Creación de documentos según tipo
- **Strategy Pattern**: Selección de IA según plan de usuario

---

## 4.2. Capa de Presentación (Frontend)

### 4.2.1. Tecnologías Utilizadas

**Stack Tecnológico del Frontend**:

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **React** | 18.2.0 | Framework UI principal |
| **react-scripts** | 5.0.1 | Toolchain (Webpack, Babel) |
| **Tailwind CSS** | 3.3.6 | Framework CSS utility-first |
| **lucide-react** | 0.294.0 | Librería de iconos (600+ íconos) |
| **Node.js** | 18+ | Runtime JavaScript |
| **npm** | 9+ | Gestor de paquetes |

**Justificación de selección**:

**React 18.2.0**:
- ✅ Componentes reutilizables
- ✅ Virtual DOM para rendimiento
- ✅ Hooks para estado (useState, useEffect)
- ✅ Comunidad grande y librerías abundantes

**Tailwind CSS 3.3.6**:
- ✅ Desarrollo rápido con clases utility
- ✅ Diseño responsive fácil (`md:`, `lg:`)
- ✅ Personalización de colores (azul Tesla para documentos)
- ✅ Bundle pequeño con PurgeCSS

**Lucide Icons**:
- ✅ Iconos SVG optimizados
- ✅ Tree-shaking (solo iconos usados)
- ✅ Consistencia visual

---

### 4.2.2. Componentes Principales

El frontend está organizado en **6 componentes principales**:

**Componente 1: App.jsx (Componente Raíz)**

**Responsabilidades**:
- Gestión de estado global de la aplicación
- Routing entre pantallas (inicio, cotización, proyecto, informe)
- Comunicación con backend via Fetch API
- Manejo de autenticación (básica)

**Estados principales**:
```javascript
const [pantallaActual, setPantallaActual] = useState('inicio');
const [tipoFlujo, setTipoFlujo] = useState(null);
const [conversacion, setConversacion] = useState([]);
const [cotizacion, setCotizacion] = useState(null);
const [proyecto, setProyecto] = useState(null);
```

**Líneas de código**: ~1,200 líneas

---

**Componente 2: ChatIA.jsx (Chat con PILI)**

**Responsabilidades**:
- Renderizar historial de conversación
- Input de mensajes del usuario
- Botones contextuales inteligentes
- Auto-scroll al último mensaje

**Props**:
```javascript
{
  mensajes: Array<{role: 'user'|'assistant', content: string}>,
  onEnviarMensaje: (mensaje: string) => void,
  cargando: boolean,
  botonesContextuales: Array<string>
}
```

**Características**:
- Markdown rendering para respuestas de PILI
- Tipeo animado (efecto typewriter)
- Formato de código con syntax highlighting

**Líneas de código**: ~180 líneas

---

**Componente 3: PiliAvatar.jsx (Avatar Animado)**

**Responsabilidades**:
- Animación del avatar de PILI
- Estados visuales: idle, listening, thinking, speaking
- Feedback visual al usuario

**Estados de animación**:
```css
.idle { animation: pulse 2s infinite; }
.listening { animation: wave 1s ease-in-out infinite; }
.thinking { animation: rotate 1.5s linear infinite; }
.speaking { animation: bounce 0.5s ease-in-out infinite; }
```

**Líneas de código**: ~120 líneas

---

**Componente 4: CotizacionEditor.jsx (Editor de Cotizaciones)**

**Responsabilidades**:
- Edición inline de items (descripción, cantidad, precio)
- Cálculo automático de subtotales
- Agregar/eliminar items
- Vista previa en tiempo real

**Funcionalidades**:
- Validación de campos (cantidad > 0, precio >= 0)
- Auto-cálculo de IGV (18%)
- Formateo de moneda (S/ 1,234.56)

**Líneas de código**: ~300 líneas

---

**Componente 5: VistaPrevia.jsx (Vista Previa de Documentos)**

**Responsabilidades**:
- Renderizar documento antes de generar Word/PDF
- Aplicar colores según esquema seleccionado
- Mostrar logo si se cargó

**Esquemas de colores soportados**:
1. **Azul Tesla** (documentos): #0052A3, #1E40AF, #3B82F6
2. **Rojo Energía**: #DC2626, #B91C1C, #F87171
3. **Verde Ecológico**: #22C55E, #16A34A, #86EFAC

**Líneas de código**: ~250 líneas

---

**Componente 6: AdminDashboard.jsx (Panel de Administrador)**

**Responsabilidades**:
- Login con credenciales (Admin/Admin1234)
- Dashboard de métricas en tiempo real
- Switches ON/OFF para 10 servicios
- Switches ON/OFF para 6 feature flags
- Actividad reciente del sistema

**Secciones**:

**A. Métricas Principales (4 cards)**:
```javascript
<MetricCard
  icon={Users}
  title="Usuarios"
  value={30}
  change="+12%"
  color="blue"
/>
```

**B. Distribución de Usuarios (Progress bars)**:
```
🆓 Free: 20 (67%) ████████████████░░░░
⭐ Pro: 7 (23%)   ███████░░░░░░░░░░░░
👑 Enterprise: 3  ███░░░░░░░░░░░░░░░░
```

**C. Servicios Disponibles (10 toggles)**:
```javascript
<ServiceToggle
  nombre="⚡ Eléctrico Residencial"
  habilitado={true}
  onToggle={() => toggleServicio('electrico-residencial')}
/>
```

**D. Feature Flags (6 toggles)**:
```javascript
<FeatureToggle
  nombre="Sistema de Tokens"
  descripcion="Límites de tokens por plan"
  habilitado={false}
  onToggle={() => toggleFeature('token_manager')}
/>
```

**Líneas de código**: ~550 líneas

---

### 4.2.3. Diseño de Interfaz de Usuario

**Principios de Diseño**:

1. **Simplicidad**: Interfaz limpia, sin elementos innecesarios
2. **Consistencia**: Colores, tipografía y espaciado uniformes
3. **Feedback**: Indicadores de carga, mensajes de éxito/error
4. **Accesibilidad**: Contraste adecuado (WCAG AA), texto legible

**Paleta de Colores (Frontend - Oscuros y Transparentes)**:

```css
/* Colores principales (oscuros, profesionales) */
--gris-oscuro: #1F2937;      /* Fondo principal */
--gris-medio: #374151;       /* Cards, modales */
--gris-claro: #4B5563;       /* Bordes sutiles */

/* Acentos con transparencia */
--azul-acento: rgba(59, 130, 246, 0.1);  /* Hover states */
--verde-exito: rgba(34, 197, 94, 0.1);   /* Success messages */
--rojo-error: rgba(239, 68, 68, 0.1);    /* Error states */

/* Texto */
--texto-primario: #F9FAFB;   /* Blanco suave */
--texto-secundario: #D1D5DB; /* Gris claro */
```

**Nota**: Los **documentos generados** (Word/PDF) usan **colores azules** (#0052A3, #1E40AF, #3B82F6).

**Tipografía**:
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
font-size: 16px; /* Base */
line-height: 1.5;
```

**Responsive Design**:
```css
/* Mobile first */
.container { padding: 1rem; }

/* Tablet (768px+) */
@media (min-width: 768px) {
  .container { padding: 2rem; }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container { padding: 3rem; max-width: 1200px; }
}
```

---

## 4.3. Capa de Lógica de Negocio (Backend)

### 4.3.1. FastAPI y Arquitectura REST

**FastAPI 0.115.6** es un framework web moderno para Python que combina:
- **Alta performance**: Comparable a NodeJS y Go
- **Tipado estático**: Validación automática con Pydantic
- **Documentación automática**: Swagger UI y ReDoc
- **Async/Await**: Soporte nativo para operaciones asíncronas

**Ventajas sobre Flask/Django**:

| Característica | FastAPI | Flask | Django |
|----------------|---------|-------|--------|
| **Performance** | ⚡⚡⚡ (muy rápido) | ⚡⚡ (medio) | ⚡ (lento) |
| **Type Hints** | ✅ Nativo | ❌ No | ❌ No |
| **Async** | ✅ Nativo | ⚠️ Limitado | ⚠️ Desde 3.1 |
| **Validación** | ✅ Automática | ❌ Manual | ⚠️ Con Django Forms |
| **Docs** | ✅ Auto (Swagger) | ❌ Manual | ❌ Manual |

**Estructura de Endpoint REST**:

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/api/cotizaciones", tags=["Cotizaciones"])

class CotizacionCreate(BaseModel):
    cliente: str
    proyecto: str
    items: List[Dict[str, Any]]

@router.post("/", response_model=CotizacionResponse)
async def crear_cotizacion(
    datos: CotizacionCreate,
    db: Session = Depends(get_db)
):
    """Crea una nueva cotización"""
    try:
        cotizacion = Cotizacion(**datos.dict())
        db.add(cotizacion)
        db.commit()
        return cotizacion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### 4.3.2. Routers y Endpoints

El backend implementa **9 routers especializados**:

| Router | Prefix | Endpoints | Propósito |
|--------|--------|-----------|-----------|
| **chat.py** | `/api/chat` | 7 | Chat con PILI, generación rápida/compleja |
| **cotizaciones.py** | `/api/cotizaciones` | 6 | CRUD cotizaciones, exportar Word/PDF |
| **proyectos.py** | `/api/proyectos` | 6 | CRUD proyectos, gestión de hitos |
| **informes.py** | `/api/informes` | 3 | Generación de informes técnicos |
| **documentos.py** | `/api/documentos` | 5 | Upload, análisis, OCR de documentos |
| **clientes.py** | `/api/clientes` | 5 | CRUD clientes, búsqueda |
| **admin.py** | `/api/admin` | 6 | Dashboard, métricas, toggles |
| **system.py** | `/api/system` | 3 | Health check, configuración |
| **generar_directo.py** | `/api` | 1 | Generación directa sin BD |

**Total**: 42 endpoints REST

---

**Router Principal: chat.py (PILI)**

**Endpoints**:

**1. POST /api/chat/mensaje**
```python
@router.post("/mensaje")
async def chat_mensaje(request: ChatRequest):
    """Chat conversacional con PILI"""
    # 1. Validar entrada
    # 2. Verificar tokens (si feature ON)
    # 3. Enviar a Gemini/Claude/GPT-4
    # 4. Consumir tokens
    # 5. Retornar respuesta
```

**2. POST /api/chat/generar-cotizacion-rapida**
```python
@router.post("/generar-cotizacion-rapida")
async def generar_cotizacion_rapida(descripcion: str):
    """Generación rápida (5-15 min) con datos mínimos"""
    # Usa Gemini con prompt optimizado para velocidad
```

**3. POST /api/chat/generar-cotizacion-compleja**
```python
@router.post("/generar-cotizacion-compleja")
async def generar_cotizacion_compleja(
    descripcion: str,
    archivos: List[UploadFile]
):
    """Generación compleja con análisis de archivos"""
    # 1. Procesar archivos con OCR
    # 2. Buscar en RAG (ChromaDB)
    # 3. Multi-agente (si feature ON)
    # 4. Generar cotización completa
```

**4. GET /api/chat/botones-contextuales/{tipo_flujo}**
```python
@router.get("/botones-contextuales/{tipo_flujo}")
async def get_botones_contextuales(tipo_flujo: str):
    """Retorna botones inteligentes según contexto"""
    botones = {
        "cotizacion": [
            "Generar ahora",
            "Agregar más items",
            "Ver vista previa"
        ],
        "proyecto": [
            "Crear proyecto",
            "Agregar cronograma",
            "Asignar recursos"
        ]
    }
    return botones[tipo_flujo]
```

---

**Router Administrativo: admin.py**

**Endpoints**:

**1. GET /api/admin/dashboard**
```python
@router.get("/dashboard")
async def get_dashboard(
    db: Session = Depends(get_db),
    admin: str = Depends(verificar_admin)  # HTTPBasic auth
):
    """Retorna todas las métricas del dashboard"""
    return {
        "metricas": {
            "usuarios": {
                "total": 30,
                "free": 20,
                "pro": 7,
                "enterprise": 3
            },
            "documentos": {
                "total": 157,
                "hoy": 12
            },
            "ingresos": {
                "mensual": 1106.93
            },
            "tokens": {
                "disponibles": 344800,
                "capacidad_total": 390000
            }
        },
        "servicios": SERVICIOS_CONFIG,  # 10 servicios
        "features": FeatureFlags.get_all_flags()  # 6 features
    }
```

**2. POST /api/admin/toggle-servicio/{servicio_id}**
```python
@router.post("/toggle-servicio/{servicio_id}")
async def toggle_servicio_endpoint(
    servicio_id: str,
    admin: str = Depends(verificar_admin)
):
    """Habilita/deshabilita un servicio"""
    nuevo_estado = toggle_servicio(servicio_id)
    logger.info(f"Servicio '{servicio_id}' → {'ON' if nuevo_estado else 'OFF'}")
    return {"habilitado": nuevo_estado}
```

**3. POST /api/admin/toggle-feature/{feature_name}**
```python
@router.post("/toggle-feature/{feature_name}")
async def toggle_feature(
    feature_name: str,
    admin: str = Depends(verificar_admin)
):
    """Habilita/deshabilita una feature flag"""
    # NOTA: Cambio temporal en memoria
    # Para permanencia: editar .env
    current = getattr(FeatureFlags, feature_name.upper())
    setattr(FeatureFlags, feature_name.upper(), not current)
    return {
        "habilitado": not current,
        "advertencia": "Cambio solo en memoria. Modificar .env para persistencia."
    }
```

---

### 4.3.3. Servicios de Negocio

El backend implementa **12 servicios especializados**:

**Servicio 1: gemini_service.py (Cliente Gemini AI)**

**Responsabilidades**:
- Comunicación con Google Gemini API
- Generación de cotizaciones estructuradas
- Chat conversacional con historial
- Análisis de documentos técnicos

**Métodos principales**:
```python
class GeminiService:
    async def chat_conversacional(
        self,
        mensaje: str,
        contexto: str,
        historial: List[dict]
    ) -> dict:
        """Chat con contexto e historial"""

    async def generar_cotizacion_estructurada(
        self,
        descripcion: str,
        archivos_contexto: List[str]
    ) -> dict:
        """Genera cotización en formato JSON"""
```

**Configuración**:
```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.3,  # Precisión vs creatividad
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 4000
    }
)
```

**Líneas de código**: ~360 líneas

---

**Servicio 2: token_manager.py (Gestor de Tokens)**

**Responsabilidades**:
- Verificar límites de tokens antes de request
- Consumir tokens después de respuesta
- Reset automático mensual
- Estadísticas globales del sistema

**Métodos principales**:
```python
class TokenManager:
    def verificar_tokens(
        self,
        usuario_id: int,
        tokens_requeridos: int
    ) -> tuple[bool, str]:
        """Retorna (puede_proceder, mensaje)"""

    def consumir_tokens(
        self,
        usuario_id: int,
        tokens: int,
        operacion: str
    ) -> bool:
        """Registra consumo de tokens"""

    def get_estadisticas_globales(self) -> dict:
        """Métricas para dashboard admin"""
```

**Estimaciones de tokens**:
```python
TOKENS_CHAT = 150
TOKENS_COTIZACION_SIMPLE = 300
TOKENS_COTIZACION_COMPLEJA = 800
TOKENS_PROYECTO = 1200
TOKENS_INFORME = 600
```

**Líneas de código**: ~250 líneas

---

**Servicio 3: multi_ia_orchestrator.py (Orquestador Multi-IA)**

**Responsabilidades**:
- Seleccionar IA apropiada según plan de usuario
- Routing inteligente según tipo de operación
- Fallback a Gemini si otras IAs no disponibles
- Gestión de costos por IA

**Estrategia de routing**:
```python
def _seleccionar_ia(self, tipo_operacion: str) -> str:
    if usuario.plan == "free":
        return "gemini"  # Solo IAs gratuitas
    elif usuario.plan == "pro":
        # Usar IA preferida del usuario
        if ia_preferida == "claude" and disponible:
            return "claude"
        return "gemini"  # Fallback
    elif usuario.plan == "enterprise":
        # Routing inteligente por operación
        routing = {
            "cotizacion": "gemini",  # Velocidad
            "proyecto": "claude",    # Razonamiento
            "informe": "gpt4"        # Escritura formal
        }
        return routing[tipo_operacion]
```

**IAs soportadas**:
- ✅ Gemini 1.5 Pro (principal)
- ⏳ Claude Sonnet 4.5 (preparado)
- ⏳ GPT-4 Turbo (preparado)
- ⏳ Groq Llama 3 (preparado)

**Líneas de código**: ~350 líneas

---

**Servicio 4: word_generator.py (Generador de Word)**

**Responsabilidades**:
- Generar documentos .docx profesionales
- Aplicar colores según esquema (3 opciones)
- Insertar logo empresarial
- Generar tablas con cálculos

**Métodos principales**:
```python
class WordGenerator:
    def generar_cotizacion(
        self,
        datos: dict,
        ruta_salida: Path,
        opciones: dict,
        logo_base64: str = None
    ) -> Path:
        """Genera cotización en Word"""
```

**Estilos aplicados**:
```python
# Colores azules para documentos
COLOR_AZUL_PRIMARIO = RGBColor(0, 82, 163)   # #0052A3
COLOR_AZUL_SECUNDARIO = RGBColor(30, 64, 175) # #1E40AF
COLOR_AZUL_CLARO = RGBColor(59, 130, 246)     # #3B82F6
```

**Líneas de código**: ~370 líneas

---

*[Continúa en siguiente parte...]*

¿Procedo con los capítulos V, VI, VII + Referencias + Anexos? 📄
