# 📚 PLAN MAESTRO: DOCUMENTOS PROFESIONALES
## 20 Prompts Detallados para Carpeta `professional/`

---

## 🎯 OBJETIVO GENERAL

Implementar sistema completo de generación de documentos profesionales con:
- **FileProcessorPro**: Procesamiento de archivos (PDF, Word, Excel, OCR)
- **RAGEngine**: Búsqueda semántica con ChromaDB
- **MLEngine**: Machine Learning con spaCy + transformers
- **ChartEngine**: Gráficas profesionales con Plotly
- **DocumentGeneratorPro**: Orquestador maestro

---

## 📋 PROMPTS DETALLADOS

### PROMPT 1: Instalación de Dependencias Base

```
Instala las dependencias base para el sistema de documentos profesionales:

1. Crea el archivo `backend/requirements_professional.txt` con:
   - PyPDF2==3.0.1 (procesamiento PDF)
   - pdfplumber==0.10.3 (extracción avanzada PDF)
   - python-docx==1.1.0 (procesamiento Word)
   - openpyxl==3.1.2 (procesamiento Excel)
   - pytesseract==0.3.10 (OCR para imágenes)
   - Pillow==10.1.0 (procesamiento de imágenes)

2. Instala las dependencias:
   ```bash
   pip install -r backend/requirements_professional.txt
   ```

3. Verifica la instalación ejecutando:
   ```python
   import PyPDF2
   import pdfplumber
   from docx import Document
   import openpyxl
   print("✅ Dependencias base instaladas")
   ```

4. Documenta cualquier error de instalación y proporciona soluciones.
```

---

### PROMPT 2: Instalación de ChromaDB para RAG

```
Configura ChromaDB para el sistema RAG (Retrieval-Augmented Generation):

1. Instala ChromaDB y dependencias:
   ```bash
   pip install chromadb==0.4.18
   pip install sentence-transformers==2.2.2
   ```

2. Crea directorio para base de datos vectorial:
   ```bash
   mkdir -p backend/storage/chroma_db
   ```

3. Crea script de prueba `backend/test_chromadb.py`:
   ```python
   import chromadb
   from sentence_transformers import SentenceTransformer
   
   # Inicializar ChromaDB
   client = chromadb.PersistentClient(path="./storage/chroma_db")
   collection = client.get_or_create_collection("test")
   
   # Inicializar modelo de embeddings
   model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
   
   print("✅ ChromaDB configurado correctamente")
   ```

4. Ejecuta el script y verifica que no haya errores.

5. Documenta el tamaño de descarga (~500 MB) y tiempo de instalación.
```

---

### PROMPT 3: Instalación de spaCy para ML

```
Configura spaCy para procesamiento de lenguaje natural:

1. Instala spaCy:
   ```bash
   pip install spacy==3.7.2
   ```

2. Descarga modelo en español:
   ```bash
   python -m spacy download es_core_news_sm
   ```

3. Crea script de prueba `backend/test_spacy.py`:
   ```python
   import spacy
   
   # Cargar modelo
   nlp = spacy.load("es_core_news_sm")
   
   # Probar con texto
   text = "Necesito instalación eléctrica para casa de 150m² en Huancayo"
   doc = nlp(text)
   
   # Extraer entidades
   for ent in doc.ents:
       print(f"{ent.text} - {ent.label_}")
   
   print("✅ spaCy configurado correctamente")
   ```

4. Ejecuta el script y verifica extracción de entidades.

5. Documenta el tamaño del modelo (~100 MB) y tiempo de carga.
```

---

### PROMPT 4: Instalación de Plotly para Gráficas

```
Configura Plotly para generación de gráficas profesionales:

1. Instala Plotly y dependencias:
   ```bash
   pip install plotly==5.18.0
   pip install matplotlib==3.8.2
   pip install kaleido==0.2.1
   ```

2. Crea script de prueba `backend/test_plotly.py`:
   ```python
   import plotly.graph_objects as go
   import plotly.express as px
   
   # Crear gráfica de prueba
   fig = go.Figure(data=[go.Bar(x=['A', 'B', 'C'], y=[1, 3, 2])])
   fig.update_layout(title="Test Plotly")
   
   # Exportar a imagen
   fig.write_image("test_chart.png")
   
   print("✅ Plotly configurado correctamente")
   ```

3. Ejecuta el script y verifica que se genere `test_chart.png`.

4. Documenta cualquier problema con kaleido (común en Windows).
```

---

### PROMPT 5: Configurar FileProcessorPro

```
Implementa y configura FileProcessorPro para procesamiento de archivos:

1. Verifica que existe `backend/app/services/professional/processors/file_processor_pro.py`

2. Crea archivo de configuración `backend/app/services/professional/config/file_processor.yaml`:
   ```yaml
   file_processor:
     max_file_size_mb: 50
     allowed_extensions:
       - pdf
       - docx
       - xlsx
       - jpg
       - png
     
     ocr:
       enabled: true
       language: "spa"
       tesseract_path: "C:/Program Files/Tesseract-OCR/tesseract.exe"  # Windows
     
     chunking:
       default_chunk_size: 300
       overlap: 50
   ```

3. Crea script de prueba `backend/test_file_processor.py`:
   ```python
   from app.services.professional.processors.file_processor_pro import FileProcessorPro
   
   processor = FileProcessorPro()
   
   # Probar con archivo PDF de prueba
   result = processor.process_file("test.pdf")
   print(f"Texto extraído: {result['text'][:200]}")
   
   # Probar chunking
   chunks = processor.chunk_text(result['text'], chunk_size=300)
   print(f"Chunks generados: {len(chunks)}")
   ```

4. Documenta formatos soportados y limitaciones.
```

---

### PROMPT 6: Configurar RAGEngine

```
Implementa y configura RAGEngine para búsqueda semántica:

1. Verifica que existe `backend/app/services/professional/rag/rag_engine.py`

2. Crea archivo de configuración `backend/app/services/professional/config/rag.yaml`:
   ```yaml
   rag:
     database_path: "./storage/chroma_db"
     collection_name: "tesla_docs"
     
     embedding_model: "paraphrase-multilingual-MiniLM-L12-v2"
     
     search:
       default_n_results: 5
       similarity_threshold: 0.7
     
     indexing:
       batch_size: 100
       auto_index: true
   ```

3. Crea script de prueba `backend/test_rag.py`:
   ```python
   from app.services.professional.rag.rag_engine import RAGEngine
   
   rag = RAGEngine()
   
   # Indexar documentos de prueba
   chunks = [
       "Cotización para instalación eléctrica residencial de 150m²",
       "Proyecto de domótica para casa inteligente",
       "Certificado ITSE para establecimiento comercial"
   ]
   
   result = rag.add_chunks(chunks, metadata={"source": "test"})
   print(f"Chunks indexados: {result['indexed']}")
   
   # Buscar
   search_result = rag.search("instalación eléctrica casa", n_results=2)
   print(f"Resultados encontrados: {len(search_result['documents'])}")
   ```

4. Documenta tiempo de indexación y búsqueda.
```

---

### PROMPT 7: Configurar MLEngine

```
Implementa y configura MLEngine para análisis de texto:

1. Verifica que existe `backend/app/services/professional/ml/ml_engine.py`

2. Crea archivo de configuración `backend/app/services/professional/config/ml.yaml`:
   ```yaml
   ml:
     spacy_model: "es_core_news_sm"
     
     embedding_model: "paraphrase-multilingual-MiniLM-L12-v2"
     
     classification:
       services:
         - electrico-residencial
         - electrico-comercial
         - electrico-industrial
         - pozo-tierra
         - contraincendios
         - domotica
         - itse
       
       confidence_threshold: 0.6
     
     entity_extraction:
       entities:
         - area_m2
         - ubicacion
         - tipo_establecimiento
         - numero_pisos
   ```

3. Crea script de prueba `backend/test_ml.py`:
   ```python
   from app.services.professional.ml.ml_engine import MLEngine
   
   ml = MLEngine()
   
   # Analizar texto
   text = "Necesito instalación eléctrica para casa de 150m² en Huancayo"
   analysis = ml.analyze_text(text)
   
   print(f"Servicio detectado: {analysis['service']['service']}")
   print(f"Confianza: {analysis['service']['confidence']}")
   print(f"Entidades: {analysis['entities']}")
   ```

4. Documenta precisión de clasificación y entidades extraídas.
```

---

### PROMPT 8: Configurar ChartEngine

```
Implementa y configura ChartEngine para gráficas profesionales:

1. Verifica que existe `backend/app/services/professional/charts/chart_engine.py`

2. Crea archivo de configuración `backend/app/services/professional/config/charts.yaml`:
   ```yaml
   charts:
     output_dir: "./storage/charts"
     
     default_format: "png"
     default_width: 1200
     default_height: 800
     
     themes:
       default: "plotly"
       professional: "seaborn"
     
     chart_types:
       gantt:
         enabled: true
         color_scheme: "blues"
       
       cost_breakdown:
         enabled: true
         chart_type: "pie"
       
       kpi_dashboard:
         enabled: true
         metrics:
           - SPI
           - CPI
           - ROI
   ```

3. Crea script de prueba `backend/test_charts.py`:
   ```python
   from app.services.professional.charts.chart_engine import ChartEngine
   
   charts = ChartEngine()
   
   # Crear gráfica de Gantt
   tasks = [
       {"task": "Planificación", "start": "2024-01-01", "end": "2024-01-15"},
       {"task": "Ejecución", "start": "2024-01-16", "end": "2024-02-15"}
   ]
   
   gantt_path = charts.create_gantt_chart(tasks)
   print(f"Gantt creado: {gantt_path}")
   
   # Crear gráfica de costos
   items = [
       {"descripcion": "Materiales", "costo": 1500},
       {"descripcion": "Mano de obra", "costo": 2000}
   ]
   
   cost_path = charts.create_cost_breakdown(items)
   print(f"Costos creados: {cost_path}")
   ```

4. Documenta tipos de gráficas disponibles y formatos de exportación.
```

---

### PROMPT 9: Configurar DocumentGeneratorPro

```
Implementa y configura DocumentGeneratorPro (orquestador maestro):

1. Verifica que existe `backend/app/services/professional/generators/document_generator_pro.py`

2. Crea archivo de configuración `backend/app/services/professional/config/generator.yaml`:
   ```yaml
   generator:
     output_dir: "./storage/generated"
     
     components:
       file_processor: true
       rag_engine: true
       ml_engine: true
       chart_engine: true
     
     document_types:
       cotizacion-simple:
         use_ml: true
         use_rag: false
         use_charts: false
       
       cotizacion-compleja:
         use_ml: true
         use_rag: true
         use_charts: true
       
       proyecto-complejo-pmi:
         use_ml: true
         use_rag: true
         use_charts: true
         required_charts:
           - gantt
           - kpi_dashboard
       
       informe-ejecutivo-apa:
         use_ml: true
         use_rag: true
         use_charts: true
         required_charts:
           - cost_breakdown
           - kpi_dashboard
   ```

3. Crea script de prueba `backend/test_generator.py`:
   ```python
   from app.services.professional.generators.document_generator_pro import DocumentGeneratorPro
   
   gen = DocumentGeneratorPro()
   
   # Verificar componentes
   status = gen.get_component_status()
   print(f"Componentes disponibles: {status['components']}")
   
   # Generar documento de prueba
   result = await gen.generate_document(
       message="Instalación eléctrica para casa de 150m²",
       document_type="cotizacion",
       complexity="simple"
   )
   
   print(f"Documento generado: {result['file_name']}")
   ```

4. Documenta flujo completo de generación.
```

---

### PROMPT 10: Crear Tests Unitarios para FileProcessorPro

```
Crea suite completa de tests para FileProcessorPro:

1. Crea `backend/app/services/professional/tests/test_file_processor.py`:
   ```python
   import pytest
   from app.services.professional.processors.file_processor_pro import FileProcessorPro
   
   @pytest.fixture
   def processor():
       return FileProcessorPro()
   
   def test_process_pdf(processor):
       """Test procesamiento de PDF"""
       result = processor.process_file("test_files/sample.pdf")
       assert result['success'] == True
       assert len(result['text']) > 0
   
   def test_process_word(processor):
       """Test procesamiento de Word"""
       result = processor.process_file("test_files/sample.docx")
       assert result['success'] == True
       assert len(result['text']) > 0
   
   def test_process_excel(processor):
       """Test procesamiento de Excel"""
       result = processor.process_file("test_files/sample.xlsx")
       assert result['success'] == True
       assert len(result['tables']) > 0
   
   def test_chunk_text(processor):
       """Test división en chunks"""
       text = "Lorem ipsum " * 100
       chunks = processor.chunk_text(text, chunk_size=50)
       assert len(chunks) > 1
       assert all(len(chunk) <= 50 for chunk in chunks)
   
   def test_invalid_file(processor):
       """Test archivo inválido"""
       result = processor.process_file("invalid.xyz")
       assert result['success'] == False
   ```

2. Ejecuta los tests:
   ```bash
   pytest backend/app/services/professional/tests/test_file_processor.py -v
   ```

3. Documenta cobertura de tests y casos edge.
```

---

### PROMPT 11: Crear Tests Unitarios para RAGEngine

```
Crea suite completa de tests para RAGEngine:

1. Crea `backend/app/services/professional/tests/test_rag.py`:
   ```python
   import pytest
   from app.services.professional.rag.rag_engine import RAGEngine
   
   @pytest.fixture
   def rag():
       return RAGEngine()
   
   def test_add_chunks(rag):
       """Test indexación de chunks"""
       chunks = ["Test chunk 1", "Test chunk 2"]
       result = rag.add_chunks(chunks, metadata={"source": "test"})
       assert result['success'] == True
       assert result['indexed'] == 2
   
   def test_search(rag):
       """Test búsqueda semántica"""
       # Indexar primero
       chunks = [
           "Instalación eléctrica residencial",
           "Proyecto de domótica"
       ]
       rag.add_chunks(chunks)
       
       # Buscar
       result = rag.search("instalación casa", n_results=1)
       assert len(result['documents']) > 0
   
   def test_get_context_for_document(rag):
       """Test obtención de contexto"""
       context = rag.get_context_for_document(
           "Necesito cotización eléctrica",
           "cotizacion",
           n_results=3
       )
       assert 'context' in context
   
   def test_empty_search(rag):
       """Test búsqueda sin resultados"""
       result = rag.search("xyz123abc", n_results=5)
       assert len(result['documents']) == 0
   ```

2. Ejecuta los tests:
   ```bash
   pytest backend/app/services/professional/tests/test_rag.py -v
   ```

3. Documenta tiempo de búsqueda y precisión.
```

---

### PROMPT 12: Crear Tests Unitarios para MLEngine

```
Crea suite completa de tests para MLEngine:

1. Crea `backend/app/services/professional/tests/test_ml.py`:
   ```python
   import pytest
   from app.services.professional.ml.ml_engine import MLEngine
   
   @pytest.fixture
   def ml():
       return MLEngine()
   
   def test_analyze_text(ml):
       """Test análisis de texto"""
       text = "Instalación eléctrica para casa de 150m²"
       result = ml.analyze_text(text)
       assert 'service' in result
       assert 'entities' in result
   
   def test_classify_service(ml):
       """Test clasificación de servicio"""
       text = "Necesito pozo a tierra"
       result = ml.classify_service(text)
       assert result['service'] == 'pozo-tierra'
       assert result['confidence'] > 0.5
   
   def test_extract_entities(ml):
       """Test extracción de entidades"""
       text = "Casa de 150m² en Huancayo con 2 pisos"
       result = ml.extract_entities(text)
       assert 'area_m2' in result
       assert result['area_m2'] == 150
       assert 'ubicacion' in result
   
   def test_generate_structured_data(ml):
       """Test generación de datos estructurados"""
       message = "Cotización para casa de 200m²"
       data = ml.generate_structured_data(message, "cotizacion")
       assert 'servicio' in data
       assert 'area_m2' in data
   ```

2. Ejecuta los tests:
   ```bash
   pytest backend/app/services/professional/tests/test_ml.py -v
   ```

3. Documenta precisión de clasificación por servicio.
```

---

### PROMPT 13: Crear Tests Unitarios para ChartEngine

```
Crea suite completa de tests para ChartEngine:

1. Crea `backend/app/services/professional/tests/test_charts.py`:
   ```python
   import pytest
   from app.services.professional.charts.chart_engine import ChartEngine
   from pathlib import Path
   
   @pytest.fixture
   def charts():
       return ChartEngine()
   
   def test_create_gantt_chart(charts):
       """Test creación de Gantt"""
       tasks = [
           {"task": "Fase 1", "start": "2024-01-01", "end": "2024-01-15"},
           {"task": "Fase 2", "start": "2024-01-16", "end": "2024-02-01"}
       ]
       path = charts.create_gantt_chart(tasks)
       assert Path(path).exists()
   
   def test_create_cost_breakdown(charts):
       """Test gráfica de costos"""
       items = [
           {"descripcion": "Materiales", "costo": 1500},
           {"descripcion": "Mano de obra", "costo": 2000}
       ]
       path = charts.create_cost_breakdown(items)
       assert Path(path).exists()
   
   def test_create_kpi_dashboard(charts):
       """Test dashboard de KPIs"""
       kpis = {"SPI": 1.05, "CPI": 0.98, "ROI": 25}
       path = charts.create_kpi_dashboard(kpis)
       assert Path(path).exists()
   
   def test_create_charts_for_document(charts):
       """Test generación completa de gráficas"""
       data = {
           "fases": [...],
           "kpis": {"SPI": 1.0},
           "items": [...]
       }
       result = charts.create_charts_for_document("proyecto", data)
       assert len(result) > 0
   ```

2. Ejecuta los tests:
   ```bash
   pytest backend/app/services/professional/tests/test_charts.py -v
   ```

3. Documenta formatos de gráficas generadas.
```

---

### PROMPT 14: Crear Tests de Integración

```
Crea tests de integración para flujo completo:

1. Crea `backend/app/services/professional/tests/test_integration.py`:
   ```python
   import pytest
   from app.services.professional import DocumentGeneratorPro
   
   @pytest.fixture
   def generator():
       return DocumentGeneratorPro()
   
   @pytest.mark.asyncio
   async def test_full_document_generation(generator):
       """Test generación completa de documento"""
       result = await generator.generate_document(
           message="Instalación eléctrica para casa de 150m²",
           document_type="cotizacion",
           complexity="simple"
       )
       
       assert result['success'] == True
       assert result['document_generated'] == True
       assert 'file_path' in result
   
   @pytest.mark.asyncio
   async def test_document_with_files(generator):
       """Test generación con archivos subidos"""
       result = await generator.generate_document(
           message="Proyecto similar al anterior",
           document_type="proyecto",
           complexity="complejo",
           uploaded_files=["test_files/proyecto_anterior.pdf"]
       )
       
       assert result['success'] == True
       assert len(result['processing_steps']) > 0
   
   @pytest.mark.asyncio
   async def test_document_with_charts(generator):
       """Test generación con gráficas"""
       result = await generator.generate_document(
           message="Proyecto PMI completo",
           document_type="proyecto",
           complexity="complejo"
       )
       
       assert result['success'] == True
       assert 'charts_generated' in result
       assert len(result['charts_generated']) > 0
   ```

2. Ejecuta los tests:
   ```bash
   pytest backend/app/services/professional/tests/test_integration.py -v
   ```

3. Documenta tiempo total de generación por tipo de documento.
```

---

### PROMPT 15: Crear Endpoint API para Documentos Profesionales

```
Crea endpoint FastAPI para generación profesional:

1. Crea `backend/app/routers/professional.py`:
   ```python
   from fastapi import APIRouter, UploadFile, File, Body
   from typing import List, Optional
   from app.services.professional import DocumentGeneratorPro
   
   router = APIRouter()
   generator = DocumentGeneratorPro()
   
   @router.post("/generate-professional")
   async def generate_professional_document(
       message: str = Body(...),
       document_type: str = Body(...),
       complexity: str = Body("simple"),
       uploaded_files: Optional[List[UploadFile]] = File(None)
   ):
       """
       Genera documento profesional con ML + RAG + Gráficas
       """
       # Guardar archivos subidos
       file_paths = []
       if uploaded_files:
           for file in uploaded_files:
               path = f"./storage/uploads/{file.filename}"
               with open(path, "wb") as f:
                   f.write(await file.read())
               file_paths.append(path)
       
       # Generar documento
       result = await generator.generate_document(
           message=message,
           document_type=document_type,
           complexity=complexity,
           uploaded_files=file_paths
       )
       
       return result
   
   @router.get("/status")
   async def get_component_status():
       """Retorna estado de componentes profesionales"""
       return generator.get_component_status()
   ```

2. Registra el router en `main.py`:
   ```python
   from app.routers import professional
   app.include_router(professional.router, prefix="/api/professional", tags=["Professional"])
   ```

3. Prueba el endpoint:
   ```bash
   curl -X POST http://localhost:8000/api/professional/generate-professional \
     -H "Content-Type: application/json" \
     -d '{"message": "Casa 150m²", "document_type": "cotizacion", "complexity": "simple"}'
   ```

4. Documenta endpoints disponibles y parámetros.
```

---

### PROMPT 16: Crear Interfaz Frontend para Subida de Archivos

```
Crea componente React para subir archivos:

1. Crea `frontend/src/components/ProfessionalUploader.jsx`:
   ```javascript
   import React, { useState } from 'react';
   import { Upload, FileText } from 'lucide-react';
   
   const ProfessionalUploader = ({ onFilesUploaded }) => {
       const [files, setFiles] = useState([]);
       const [uploading, setUploading] = useState(false);
       
       const handleFileChange = (e) => {
           const selectedFiles = Array.from(e.target.files);
           setFiles(selectedFiles);
       };
       
       const handleUpload = async () => {
           setUploading(true);
           
           const formData = new FormData();
           files.forEach(file => formData.append('files', file));
           
           try {
               const response = await fetch('/api/professional/upload', {
                   method: 'POST',
                   body: formData
               });
               
               const data = await response.json();
               onFilesUploaded(data.file_paths);
           } catch (error) {
               console.error('Error:', error);
           } finally {
               setUploading(false);
           }
       };
       
       return (
           <div className="uploader">
               <input 
                   type="file" 
                   multiple 
                   onChange={handleFileChange}
                   accept=".pdf,.docx,.xlsx"
               />
               
               {files.length > 0 && (
                   <div className="file-list">
                       {files.map((file, i) => (
                           <div key={i} className="file-item">
                               <FileText size={16} />
                               <span>{file.name}</span>
                           </div>
                       ))}
                   </div>
               )}
               
               <button onClick={handleUpload} disabled={uploading}>
                   <Upload size={16} />
                   {uploading ? 'Subiendo...' : 'Subir Archivos'}
               </button>
           </div>
       );
   };
   
   export default ProfessionalUploader;
   ```

2. Integra en App.jsx para documentos complejos.

3. Documenta formatos soportados y límites de tamaño.
```

---

### PROMPT 17: Crear Sistema de Caché para RAG

```
Implementa sistema de caché para mejorar performance de RAG:

1. Crea `backend/app/services/professional/rag/cache_manager.py`:
   ```python
   import json
   from pathlib import Path
   from datetime import datetime, timedelta
   
   class RAGCacheManager:
       """Gestiona caché de búsquedas RAG"""
       
       def __init__(self, cache_dir="./storage/rag_cache"):
           self.cache_dir = Path(cache_dir)
           self.cache_dir.mkdir(parents=True, exist_ok=True)
           self.ttl = timedelta(hours=24)
       
       def get(self, query: str):
           """Obtiene resultado de caché"""
           cache_file = self.cache_dir / f"{hash(query)}.json"
           
           if not cache_file.exists():
               return None
           
           with open(cache_file) as f:
               data = json.load(f)
           
           # Verificar TTL
           cached_at = datetime.fromisoformat(data['cached_at'])
           if datetime.now() - cached_at > self.ttl:
               cache_file.unlink()
               return None
           
           return data['result']
       
       def set(self, query: str, result: dict):
           """Guarda resultado en caché"""
           cache_file = self.cache_dir / f"{hash(query)}.json"
           
           data = {
               'query': query,
               'result': result,
               'cached_at': datetime.now().isoformat()
           }
           
           with open(cache_file, 'w') as f:
               json.dump(data, f)
   ```

2. Integra en RAGEngine:
   ```python
   def search(self, query: str, n_results: int = 5):
       # Verificar caché
       cached = self.cache.get(query)
       if cached:
           return cached
       
       # Buscar
       result = self._search(query, n_results)
       
       # Guardar en caché
       self.cache.set(query, result)
       
       return result
   ```

3. Documenta mejora de performance (tiempo de respuesta).
```

---

### PROMPT 18: Crear Sistema de Logging Avanzado

```
Implementa sistema de logging detallado para debugging:

1. Crea `backend/app/services/professional/utils/logger.py`:
   ```python
   import logging
   from pathlib import Path
   from datetime import datetime
   
   class ProfessionalLogger:
       """Logger especializado para componentes profesionales"""
       
       def __init__(self, name: str):
           self.logger = logging.getLogger(name)
           self.logger.setLevel(logging.DEBUG)
           
           # Handler para archivo
           log_dir = Path("./logs/professional")
           log_dir.mkdir(parents=True, exist_ok=True)
           
           file_handler = logging.FileHandler(
               log_dir / f"{name}_{datetime.now():%Y%m%d}.log"
           )
           file_handler.setLevel(logging.DEBUG)
           
           # Formato
           formatter = logging.Formatter(
               '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
           )
           file_handler.setFormatter(formatter)
           
           self.logger.addHandler(file_handler)
       
       def log_component_status(self, component: str, status: bool):
           """Log estado de componente"""
           emoji = "✅" if status else "❌"
           self.logger.info(f"{emoji} {component}: {'ACTIVO' if status else 'INACTIVO'}")
       
       def log_processing_step(self, step: str, duration: float):
           """Log paso de procesamiento"""
           self.logger.info(f"⏱️ {step}: {duration:.2f}s")
       
       def log_error(self, component: str, error: Exception):
           """Log error detallado"""
           self.logger.error(f"❌ Error en {component}: {str(error)}", exc_info=True)
   ```

2. Integra en todos los componentes profesionales.

3. Documenta estructura de logs y rotación de archivos.
```

---

### PROMPT 19: Crear Dashboard de Monitoreo

```
Implementa dashboard para monitorear componentes profesionales:

1. Crea endpoint de métricas `backend/app/routers/professional.py`:
   ```python
   @router.get("/metrics")
   async def get_metrics():
       """Retorna métricas de uso de componentes profesionales"""
       return {
           "file_processor": {
               "files_processed": get_files_processed_count(),
               "avg_processing_time": get_avg_processing_time(),
               "formats": get_format_distribution()
           },
           "rag": {
               "total_chunks": get_total_chunks(),
               "searches_today": get_searches_count(),
               "avg_search_time": get_avg_search_time(),
               "cache_hit_rate": get_cache_hit_rate()
           },
           "ml": {
               "classifications_today": get_classifications_count(),
               "avg_confidence": get_avg_confidence(),
               "service_distribution": get_service_distribution()
           },
           "charts": {
               "charts_generated": get_charts_count(),
               "chart_types": get_chart_type_distribution()
           }
       }
   ```

2. Crea componente React `frontend/src/components/ProfessionalDashboard.jsx`:
   ```javascript
   import React, { useState, useEffect } from 'react';
   
   const ProfessionalDashboard = () => {
       const [metrics, setMetrics] = useState(null);
       
       useEffect(() => {
           fetch('/api/professional/metrics')
               .then(res => res.json())
               .then(data => setMetrics(data));
       }, []);
       
       if (!metrics) return <div>Cargando...</div>;
       
       return (
           <div className="dashboard">
               <h2>Dashboard Profesional</h2>
               
               <div className="metric-card">
                   <h3>FileProcessor</h3>
                   <p>Archivos procesados: {metrics.file_processor.files_processed}</p>
                   <p>Tiempo promedio: {metrics.file_processor.avg_processing_time}s</p>
               </div>
               
               <div className="metric-card">
                   <h3>RAG Engine</h3>
                   <p>Chunks indexados: {metrics.rag.total_chunks}</p>
                   <p>Cache hit rate: {metrics.rag.cache_hit_rate}%</p>
               </div>
               
               {/* Resto de métricas */}
           </div>
       );
   };
   ```

3. Documenta métricas disponibles y cómo interpretarlas.
```

---

### PROMPT 20: Crear Manual Completo de Usuario

```
Crea manual completo para usar sistema de documentos profesionales:

1. Crea `backend/app/services/professional/MANUAL_USUARIO.md`:
   ```markdown
   # 📖 MANUAL DE USUARIO - DOCUMENTOS PROFESIONALES
   
   ## 🎯 Introducción
   
   El sistema de documentos profesionales permite generar documentos de clase mundial con:
   - Procesamiento de archivos subidos (PDF, Word, Excel)
   - Búsqueda semántica de proyectos anteriores
   - Análisis inteligente con Machine Learning
   - Gráficas profesionales automáticas
   
   ## 📋 Tipos de Documentos
   
   ### 1. Cotización Simple
   - Tiempo: 5-15 minutos
   - Componentes: ML básico
   - Sin archivos necesarios
   
   ### 2. Cotización Compleja
   - Tiempo: 15-30 minutos
   - Componentes: ML + RAG + Gráficas
   - Archivos opcionales
   
   ### 3. Proyecto Simple
   - Tiempo: 20-40 minutos
   - Componentes: ML + RAG
   - Archivos recomendados
   
   ### 4. Proyecto Complejo PMI
   - Tiempo: 30-60 minutos
   - Componentes: ML + RAG + Gráficas (Gantt, KPIs)
   - Archivos requeridos
   
   ### 5. Informe Técnico
   - Tiempo: 20-40 minutos
   - Componentes: ML + RAG
   - Archivos opcionales
   
   ### 6. Informe Ejecutivo APA
   - Tiempo: 30-60 minutos
   - Componentes: ML + RAG + Gráficas (ROI, TIR)
   - Archivos recomendados
   
   ## 🚀 Cómo Usar
   
   ### Paso 1: Seleccionar Tipo de Documento
   
   En la interfaz, selecciona el tipo de documento que necesitas.
   
   ### Paso 2: Subir Archivos (Opcional)
   
   Si tienes proyectos anteriores o documentos de referencia:
   1. Click en "Subir Archivos"
   2. Selecciona PDF, Word o Excel
   3. Espera a que se procesen
   
   ### Paso 3: Describir Requerimientos
   
   Escribe una descripción clara de lo que necesitas:
   - Tipo de servicio
   - Área o tamaño
   - Ubicación
   - Características especiales
   
   ### Paso 4: Generar Documento
   
   Click en "Generar Documento Profesional"
   
   El sistema:
   1. Analiza tu mensaje con ML
   2. Busca proyectos similares en RAG
   3. Genera gráficas si es necesario
   4. Crea el documento Word
   
   ### Paso 5: Descargar
   
   Descarga el documento generado en formato Word o PDF.
   
   ## ⚙️ Configuración Avanzada
   
   ### Personalizar Gráficas
   
   En `config/charts.yaml` puedes configurar:
   - Colores
   - Tamaños
   - Tipos de gráficas
   
   ### Ajustar ML
   
   En `config/ml.yaml` puedes configurar:
   - Umbral de confianza
   - Servicios a clasificar
   - Entidades a extraer
   
   ## 🐛 Troubleshooting
   
   ### Componente no disponible
   
   Si ves "Componente X no disponible":
   1. Verifica instalación de dependencias
   2. Revisa logs en `logs/professional/`
   3. Ejecuta tests: `pytest tests/test_X.py`
   
   ### Procesamiento lento
   
   Si el procesamiento es lento:
   1. Verifica caché de RAG
   2. Reduce tamaño de archivos
   3. Ajusta `chunk_size` en config
   
   ## 📞 Soporte
   
   Para soporte técnico:
   - Email: soporte@teslaelectricidad.com
   - Logs: `logs/professional/`
   - Tests: `pytest tests/`
   ```

2. Crea video tutorial (opcional).

3. Documenta casos de uso comunes y mejores prácticas.
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Instalación (Prompts 1-4)
- [ ] Dependencias base instaladas
- [ ] ChromaDB configurado
- [ ] spaCy instalado
- [ ] Plotly funcionando

### Configuración (Prompts 5-9)
- [ ] FileProcessorPro configurado
- [ ] RAGEngine configurado
- [ ] MLEngine configurado
- [ ] ChartEngine configurado
- [ ] DocumentGeneratorPro configurado

### Testing (Prompts 10-14)
- [ ] Tests FileProcessorPro
- [ ] Tests RAGEngine
- [ ] Tests MLEngine
- [ ] Tests ChartEngine
- [ ] Tests de integración

### Integración (Prompts 15-16)
- [ ] Endpoint API creado
- [ ] Frontend para subida de archivos

### Optimización (Prompts 17-19)
- [ ] Sistema de caché
- [ ] Logging avanzado
- [ ] Dashboard de monitoreo

### Documentación (Prompt 20)
- [ ] Manual de usuario completo

---

## 📊 TIEMPO ESTIMADO

| Fase | Prompts | Tiempo |
|------|---------|--------|
| Instalación | 1-4 | 4 horas |
| Configuración | 5-9 | 6 horas |
| Testing | 10-14 | 8 horas |
| Integración | 15-16 | 4 horas |
| Optimización | 17-19 | 6 horas |
| Documentación | 20 | 2 horas |
| **TOTAL** | **20** | **30 horas** |

---

## 🎯 RESULTADO FINAL

Sistema completo de documentos profesionales con:
- ✅ Procesamiento de archivos (PDF, Word, Excel, OCR)
- ✅ Búsqueda semántica (RAG con ChromaDB)
- ✅ Machine Learning (spaCy + transformers)
- ✅ Gráficas profesionales (Plotly)
- ✅ Generación automática de 6 tipos de documentos
- ✅ Tests completos (>80% coverage)
- ✅ API REST documentada
- ✅ Dashboard de monitoreo
- ✅ Manual de usuario
