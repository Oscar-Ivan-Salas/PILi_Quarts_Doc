"""
GENERADOR DE DOCUMENTOS PROFESIONAL v4.0
Integracion de todos los componentes para documentos de clase mundial

Genera los 6 tipos de documentos:
1. Cotizacion Simple
2. Cotizacion Compleja
3. Proyecto Simple
4. Proyecto Complejo (PMI)
5. Informe Tecnico
6. Informe Ejecutivo (APA)
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

# Imports de componentes profesionales
try:
    from ..processors.file_processor_pro import FileProcessorPro, get_file_processor
    from ..rag.rag_engine import RAGEngine, get_rag_engine
    from ..ml.ml_engine import MLEngine, get_ml_engine
    from ..charts.chart_engine import ChartEngine, get_chart_engine
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Error importando componentes: {e}")
    COMPONENTS_AVAILABLE = False

# Import de los generadores modulares profesionales
try:
    from . import generar_documento, tipos_disponibles, GENERADORES
    GENERADORES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Generadores modulares no disponibles: {e}")
    GENERADORES_AVAILABLE = False

# Fallback al generador Word existente (para compatibilidad)
try:
    from app.services.word_generator import WordGenerator, get_word_generator
    WORD_GENERATOR_AVAILABLE = True
except ImportError:
    WORD_GENERATOR_AVAILABLE = False
    logger.warning("WordGenerator no disponible")


class DocumentGeneratorPro:
    """
    Generador de documentos profesional de clase mundial.

    Integra:
    - FileProcessorPro: Procesamiento de archivos subidos
    - RAGEngine: Busqueda semantica de contexto
    - MLEngine: Clasificacion y extraccion de entidades
    - ChartEngine: Graficas profesionales
    - WordGenerator: Generacion final de documentos
    """

    def __init__(self):
        """Inicializa el generador con todos los componentes"""

        # Obtener instancias de componentes
        self.file_processor = get_file_processor() if COMPONENTS_AVAILABLE else None
        self.rag_engine = get_rag_engine() if COMPONENTS_AVAILABLE else None
        self.ml_engine = get_ml_engine() if COMPONENTS_AVAILABLE else None
        self.chart_engine = get_chart_engine() if COMPONENTS_AVAILABLE else None

        # Generadores modulares (prioridad) o fallback al WordGenerator antiguo
        self.generadores_modulares = GENERADORES_AVAILABLE
        self.word_generator = get_word_generator() if WORD_GENERATOR_AVAILABLE else None

        # Directorio de salida
        self.output_dir = Path("backend/storage/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Estado de componentes
        self.component_status = {
            "file_processor": self.file_processor is not None,
            "rag_engine": self.rag_engine is not None and self.rag_engine.is_available(),
            "ml_engine": self.ml_engine is not None and self.ml_engine.is_available(),
            "chart_engine": self.chart_engine is not None and self.chart_engine.is_available(),
            "generadores_modulares": self.generadores_modulares,
            "word_generator_fallback": self.word_generator is not None
        }

        logger.info("=" * 60)
        logger.info("DOCUMENT GENERATOR PRO v4.0 INICIALIZADO")
        logger.info("=" * 60)
        for component, status in self.component_status.items():
            emoji = "✅" if status else "❌"
            logger.info(f"  {emoji} {component}: {'ACTIVO' if status else 'NO DISPONIBLE'}")
        logger.info("=" * 60)

    async def generate_document(
        self,
        message: str,
        document_type: str = "cotizacion",
        complexity: str = "simple",
        uploaded_files: List[str] = None,
        logo_base64: str = None,
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Genera un documento profesional completo.

        Este es el metodo principal que orquesta todo el proceso:
        1. Procesa archivos subidos (si hay)
        2. Indexa contenido en RAG
        3. Analiza mensaje con ML
        4. Recupera contexto relevante
        5. Genera graficas si es necesario
        6. Crea documento final

        Args:
            message: Mensaje/descripcion del usuario
            document_type: "cotizacion", "proyecto", "informe"
            complexity: "simple" o "complejo"
            uploaded_files: Rutas a archivos subidos
            logo_base64: Logo en base64
            options: Opciones adicionales

        Returns:
            Dict con documento generado y metadata
        """
        try:
            logger.info(f"Generando documento: {document_type} - {complexity}")

            result = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "document_type": document_type,
                "complexity": complexity,
                "processing_steps": []
            }

            # Paso 1: Procesar archivos subidos
            context_from_files = ""
            if uploaded_files and self.file_processor:
                file_result = self.file_processor.process_multiple(uploaded_files)
                context_from_files = file_result.get("combined_text", "")
                result["processing_steps"].append({
                    "step": "file_processing",
                    "files_processed": file_result.get("processed", 0),
                    "success": file_result.get("success", False)
                })

                # Indexar en RAG
                if context_from_files and self.rag_engine and self.rag_engine.is_available():
                    chunks = self.file_processor.chunk_text(context_from_files, chunk_size=300)
                    rag_result = self.rag_engine.add_chunks(
                        chunks,
                        metadata={"source": "user_upload", "document_type": document_type}
                    )
                    result["processing_steps"].append({
                        "step": "rag_indexing",
                        "chunks_indexed": len(chunks),
                        "success": rag_result.get("success", False)
                    })

            # Paso 2: Analizar mensaje con ML
            analysis = {}
            if self.ml_engine:
                analysis = self.ml_engine.analyze_text(message)
                result["processing_steps"].append({
                    "step": "ml_analysis",
                    "service_detected": analysis.get("service", {}).get("service"),
                    "confidence": analysis.get("service", {}).get("confidence", 0)
                })

            # Paso 3: Recuperar contexto de RAG
            rag_context = {}
            if self.rag_engine and self.rag_engine.is_available():
                rag_context = self.rag_engine.get_context_for_document(
                    message,
                    document_type,
                    n_results=3
                )
                result["processing_steps"].append({
                    "step": "rag_retrieval",
                    "fragments_found": rag_context.get("total_fragments", 0)
                })

            # Paso 4: Generar datos estructurados
            structured_data = self._build_structured_data(
                message=message,
                document_type=document_type,
                complexity=complexity,
                analysis=analysis,
                rag_context=rag_context,
                file_context=context_from_files,
                options=options
            )
            result["structured_data"] = structured_data

            # Paso 5: Generar graficas (para documentos complejos)
            charts = {}
            if complexity == "complejo" and self.chart_engine:
                charts = self.chart_engine.create_charts_for_document(
                    document_type,
                    structured_data
                )
                result["charts_generated"] = list(charts.keys())
                result["processing_steps"].append({
                    "step": "chart_generation",
                    "charts_created": len(charts)
                })

            # Paso 6: Generar documento Word
            # PRIORIDAD: Usar generadores modulares profesionales
            if self.generadores_modulares:
                # Mapear tipo + complejidad a generador específico
                tipo_generador = self._map_to_generator_type(document_type, complexity)

                # Preparar ruta de salida
                numero = structured_data.get("numero", self._generate_document_number(document_type))
                file_path = self.output_dir / f"{numero}.docx"

                # Preparar datos para generador modular
                datos_documento = self._prepare_data_for_generator(
                    structured_data,
                    document_type,
                    complexity,
                    charts
                )

                # Generar documento usando sistema modular
                try:
                    doc_path = generar_documento(
                        tipo_documento=tipo_generador,
                        datos=datos_documento,
                        ruta_salida=str(file_path),
                        opciones=options
                    )

                    result["document_generated"] = True
                    result["file_path"] = str(doc_path)
                    result["file_name"] = Path(doc_path).name
                    result["generator_type"] = tipo_generador
                    result["generator_system"] = "modular_professional"

                    result["processing_steps"].append({
                        "step": "document_generation",
                        "success": True,
                        "generator": tipo_generador,
                        "system": "modular",
                        "file": Path(doc_path).name
                    })

                except Exception as e:
                    logger.error(f"Error con generador modular: {e}")
                    result["document_generated"] = False
                    result["error"] = str(e)

            # FALLBACK: Usar WordGenerator antiguo si generadores modulares no disponibles
            elif self.word_generator:
                # Preparar datos para WordGenerator
                datos_json = {
                    "datos_extraidos": structured_data,
                    "agente_responsable": self._get_agent_name(document_type, complexity),
                    "graficas": charts
                }

                word_result = self.word_generator.generar_desde_json_pili(
                    datos_json=datos_json,
                    tipo_documento=document_type,
                    opciones=options,
                    logo_base64=logo_base64
                )

                result["document_generated"] = word_result.get("exito", False)
                result["file_path"] = word_result.get("ruta_archivo")
                result["file_name"] = word_result.get("nombre_archivo")
                result["generator_system"] = "word_generator_legacy"

                result["processing_steps"].append({
                    "step": "document_generation",
                    "success": word_result.get("exito", False),
                    "generator": "word_generator",
                    "system": "legacy",
                    "file": word_result.get("nombre_archivo")
                })
            else:
                result["document_generated"] = False
                result["error"] = "No hay generadores disponibles"

            logger.info(f"Documento generado exitosamente: {result.get('file_name')}")
            return result

        except Exception as e:
            logger.error(f"Error generando documento: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _map_to_generator_type(self, document_type: str, complexity: str) -> str:
        """
        Mapea document_type + complexity al tipo específico del generador modular.

        Args:
            document_type: "cotizacion", "proyecto", "informe"
            complexity: "simple" o "complejo"

        Returns:
            Tipo para el generador modular (ej: "cotizacion-simple", "proyecto-pmi")
        """
        mapping = {
            ("cotizacion", "simple"): "cotizacion-simple",
            ("cotizacion", "complejo"): "cotizacion-compleja",
            ("proyecto", "simple"): "proyecto-simple",
            ("proyecto", "complejo"): "proyecto-pmi",
            ("informe", "simple"): "informe-tecnico",
            ("informe", "complejo"): "informe-apa"
        }

        tipo = mapping.get((document_type, complexity))
        if not tipo:
            logger.warning(f"Mapeo no encontrado para {document_type}/{complexity}, usando default")
            return f"{document_type}-simple"

        return tipo

    def _prepare_data_for_generator(
        self,
        structured_data: Dict[str, Any],
        document_type: str,
        complexity: str,
        charts: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepara los datos estructurados en el formato que esperan los generadores modulares.

        Los generadores modulares esperan estructura específica según tipo:
        - Cotizaciones: numero, fecha, cliente, proyecto, items[], subtotal, igv, total
        - Proyectos: nombre, cliente, descripcion, objetivos[], entregables[], cronograma[]
        - Informes: titulo, autor, fecha, resumen, contenido[], conclusiones[]

        Args:
            structured_data: Datos estructurados del ML/RAG
            document_type: Tipo de documento
            complexity: Complejidad
            charts: Gráficas generadas

        Returns:
            Datos en formato esperado por generadores modulares
        """
        datos = {}

        # Datos comunes a todos
        datos["numero"] = structured_data.get("numero", self._generate_document_number(document_type))
        datos["fecha"] = structured_data.get("fecha", datetime.now().strftime("%d/%m/%Y"))
        datos["cliente"] = structured_data.get("cliente", "Cliente")

        if document_type == "cotizacion":
            # Estructura para cotizaciones
            datos["proyecto"] = structured_data.get("proyecto", f"Proyecto {structured_data.get('servicio', 'Eléctrico')}")
            datos["descripcion"] = structured_data.get("descripcion", "")

            # Items de cotización
            items = structured_data.get("items", [])
            if not items:
                # Generar items básicos desde structured_data
                items = [{
                    "descripcion": structured_data.get("servicio", "Servicio eléctrico"),
                    "cantidad": structured_data.get("cantidad", 1),
                    "unidad": "glb",
                    "precio_unitario": structured_data.get("precio_estimado", 5000.0)
                }]
            datos["items"] = items

            # Calcular totales
            subtotal = sum(item.get("cantidad", 1) * item.get("precio_unitario", 0) for item in items)
            datos["subtotal"] = subtotal
            datos["igv"] = subtotal * 0.18
            datos["total"] = subtotal + datos["igv"]

            # Datos adicionales
            datos["vigencia"] = structured_data.get("vigencia", "30 días")
            datos["observaciones"] = structured_data.get("observaciones", "Precios incluyen IGV")

            # Si es compleja, agregar análisis
            if complexity == "complejo":
                datos["analisis_riesgos"] = structured_data.get("riesgos", [])
                datos["cronograma_estimado"] = structured_data.get("cronograma", [])
                if charts:
                    datos["graficas"] = charts

        elif document_type == "proyecto":
            # Estructura para proyectos
            datos["nombre"] = structured_data.get("nombre", f"Proyecto {structured_data.get('servicio', 'Eléctrico')}")
            datos["descripcion"] = structured_data.get("descripcion", "")
            datos["objetivos"] = structured_data.get("objetivos", [
                "Objetivo principal del proyecto"
            ])
            datos["entregables"] = structured_data.get("entregables", [
                "Entregable 1"
            ])
            datos["presupuesto"] = structured_data.get("presupuesto", 0.0)

            # Si es complejo (PMI), agregar datos PMI
            if complexity == "complejo":
                datos["stakeholders"] = structured_data.get("stakeholders", [])
                datos["kpis"] = structured_data.get("kpis", {})
                datos["matriz_raci"] = structured_data.get("matriz_raci", self._generate_raci_matrix())
                datos["plan_comunicaciones"] = structured_data.get("plan_comunicaciones", {})
                if charts:
                    datos["graficas"] = charts

        elif document_type == "informe":
            # Estructura para informes
            datos["titulo"] = structured_data.get("titulo", f"Informe {structured_data.get('servicio', 'Técnico')}")
            datos["autor"] = structured_data.get("autor", "Tesla Electricidad y Automatización S.A.C.")
            datos["resumen"] = structured_data.get("resumen", "")
            datos["introduccion"] = structured_data.get("introduccion", "")
            datos["metodologia"] = structured_data.get("metodologia", "")
            datos["resultados"] = structured_data.get("resultados", [])
            datos["conclusiones"] = structured_data.get("conclusiones", [])
            datos["recomendaciones"] = structured_data.get("recomendaciones", [])

            # Si es complejo (APA), agregar datos ejecutivos
            if complexity == "complejo":
                datos["formato"] = "APA 7ma edición"
                datos["abstract"] = structured_data.get("abstract", "")
                datos["referencias"] = structured_data.get("referencias", [])
                datos["metricas_clave"] = structured_data.get("metricas_clave", {})
                if charts:
                    datos["graficas"] = charts

        # Agregar contexto RAG si existe
        if "contexto_rag" in structured_data:
            datos["contexto_adicional"] = structured_data["contexto_rag"]

        # Agregar contenido de archivos si existe
        if "contenido_archivos_subidos" in structured_data:
            datos["archivos_referencia"] = structured_data["contenido_archivos_subidos"]

        return datos

    def _build_structured_data(
        self,
        message: str,
        document_type: str,
        complexity: str,
        analysis: Dict[str, Any],
        rag_context: Dict[str, Any],
        file_context: str,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Construye los datos estructurados para el documento.

        Combina:
        - Analisis ML del mensaje
        - Contexto de RAG
        - Contexto de archivos
        - Opciones del usuario
        """
        # Datos base del ML
        if self.ml_engine:
            data = self.ml_engine.generate_structured_data(message, document_type)
        else:
            data = {
                "servicio": "electrico-residencial",
                "area_m2": 100,
                "cliente": "Cliente"
            }

        # Agregar datos comunes
        data["numero"] = self._generate_document_number(document_type)
        data["fecha"] = datetime.now().strftime("%d/%m/%Y")
        data["complejidad"] = complexity

        # Enriquecer con contexto RAG
        context = rag_context.get("context", {})

        if document_type == "cotizacion":
            # Datos especificos de cotizacion
            data.setdefault("vigencia", "30 dias")
            data.setdefault("observaciones", "Precios incluyen IGV")

            if context.get("precios"):
                data["referencia_precios"] = context["precios"][0][:200]

        elif document_type == "proyecto":
            # Datos especificos de proyecto
            data.setdefault("nombre", f"Proyecto {data.get('servicio')}")
            data.setdefault("estado", "En Planificacion")

            if complexity == "complejo":
                # Agregar datos PMI
                data["kpis"] = {
                    "SPI": 1.0,
                    "CPI": 1.0
                }
                data["matriz_raci"] = self._generate_raci_matrix()

            if context.get("alcance"):
                data["alcance_referencia"] = context["alcance"][0][:300]

        elif document_type == "informe":
            # Datos especificos de informe
            data.setdefault("titulo", f"Informe de {data.get('servicio')}")
            data.setdefault("autor", "Tesla Electricidad")

            if complexity == "complejo":
                # Agregar datos ejecutivos
                data["metricas_clave"] = {
                    "roi_estimado": 25,
                    "payback_meses": 18,
                    "tir_proyectada": 30,
                    "reduccion_costos_operativos": 20
                }
                data["formato"] = "APA 7ma edicion"

            if context.get("antecedentes"):
                data["antecedentes_referencia"] = context["antecedentes"][0][:300]

        # Agregar contenido de archivos si hay
        if file_context:
            data["contenido_archivos_subidos"] = file_context[:1000]

        # Aplicar opciones del usuario
        if options:
            for key, value in options.items():
                if value is not None:
                    data[key] = value

        return data

    def _generate_document_number(self, document_type: str) -> str:
        """Genera numero unico de documento"""
        prefix = {
            "cotizacion": "COT",
            "proyecto": "PROY",
            "informe": "INF"
        }.get(document_type, "DOC")

        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        return f"{prefix}-{timestamp}"

    def _get_agent_name(self, document_type: str, complexity: str) -> str:
        """Obtiene nombre del agente PILI segun tipo"""
        agents = {
            ("cotizacion", "simple"): "PILI Cotizadora",
            ("cotizacion", "complejo"): "PILI Analista Senior",
            ("proyecto", "simple"): "PILI Coordinadora",
            ("proyecto", "complejo"): "PILI Directora PMI",
            ("informe", "simple"): "PILI Reportera",
            ("informe", "complejo"): "PILI Directora Ejecutiva"
        }
        return agents.get((document_type, complexity), "PILI Asistente")

    def _generate_raci_matrix(self) -> List[Dict[str, str]]:
        """Genera matriz RACI para proyectos PMI"""
        return [
            {"actividad": "Planificacion", "pm": "R", "ing": "C", "tec": "I", "cliente": "A"},
            {"actividad": "Ingenieria", "pm": "A", "ing": "R", "tec": "C", "cliente": "I"},
            {"actividad": "Ejecucion", "pm": "A", "ing": "C", "tec": "R", "cliente": "I"},
            {"actividad": "Control", "pm": "R", "ing": "C", "tec": "I", "cliente": "A"},
            {"actividad": "Cierre", "pm": "R", "ing": "C", "tec": "I", "cliente": "A"}
        ]

    async def process_uploaded_files(
        self,
        files: List[str]
    ) -> Dict[str, Any]:
        """
        Procesa archivos subidos e indexa en RAG.

        Util para preparar contexto antes de generar documento.

        Args:
            files: Lista de rutas a archivos

        Returns:
            Resultado del procesamiento
        """
        if not self.file_processor:
            return {"success": False, "error": "FileProcessor no disponible"}

        # Procesar archivos
        result = self.file_processor.process_multiple(files)

        # Indexar en RAG
        if result.get("success") and self.rag_engine:
            text = result.get("combined_text", "")
            if text:
                chunks = self.file_processor.chunk_text(text)
                rag_result = self.rag_engine.add_chunks(
                    chunks,
                    metadata={"source": "batch_upload"}
                )
                result["rag_indexing"] = rag_result

        return result

    def get_component_status(self) -> Dict[str, Any]:
        """Retorna estado de todos los componentes"""
        return {
            "version": "4.0",
            "components": self.component_status,
            "all_available": all(self.component_status.values()),
            "timestamp": datetime.now().isoformat()
        }

    def get_available_document_types(self) -> List[Dict[str, str]]:
        """Lista los tipos de documentos disponibles"""
        return [
            {"type": "cotizacion", "complexity": "simple", "name": "Cotizacion Simple"},
            {"type": "cotizacion", "complexity": "complejo", "name": "Cotizacion Compleja"},
            {"type": "proyecto", "complexity": "simple", "name": "Proyecto Simple"},
            {"type": "proyecto", "complexity": "complejo", "name": "Proyecto PMI"},
            {"type": "informe", "complexity": "simple", "name": "Informe Tecnico"},
            {"type": "informe", "complexity": "complejo", "name": "Informe Ejecutivo APA"}
        ]


# Instancia global
document_generator_pro = DocumentGeneratorPro()

def get_document_generator_pro() -> DocumentGeneratorPro:
    """Obtiene la instancia del generador profesional"""
    return document_generator_pro
