"""
SISTEMA RAG LOCAL v4.0
Retrieval Augmented Generation sin necesidad de IA en red

Usa:
- sentence-transformers para embeddings locales
- ChromaDB como vector store local
- Busqueda semantica para recuperar contexto relevante
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import hashlib

logger = logging.getLogger(__name__)

# Imports condicionales
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    logger.warning("sentence-transformers no disponible - pip install sentence-transformers")

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logger.warning("chromadb no disponible - pip install chromadb")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class RAGEngine:
    """
    Motor RAG local para busqueda semantica de documentos.

    Funciona 100% offline sin necesidad de APIs externas.
    Ideal para entornos con restricciones de red.
    """

    def __init__(
        self,
        collection_name: str = "tesla_documents",
        persist_directory: str = None,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        """
        Inicializa el motor RAG.

        Args:
            collection_name: Nombre de la coleccion en ChromaDB
            persist_directory: Directorio para persistir la base de datos
            model_name: Modelo de sentence-transformers a usar
        """
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory) if persist_directory else Path("backend/storage/embeddings")
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        self.model_name = model_name
        self.model = None
        self.client = None
        self.collection = None

        # Inicializar componentes
        self._initialize_components()

        logger.info(f"RAGEngine inicializado - Collection: {collection_name}")

    def _initialize_components(self):
        """Inicializa modelo de embeddings y ChromaDB"""

        # Inicializar modelo de embeddings
        if EMBEDDINGS_AVAILABLE:
            try:
                self.model = SentenceTransformer(self.model_name)
                logger.info(f"Modelo de embeddings cargado: {self.model_name}")
            except Exception as e:
                logger.error(f"Error cargando modelo de embeddings: {e}")
                self.model = None
        else:
            logger.warning("sentence-transformers no disponible")

        # Inicializar ChromaDB
        if CHROMADB_AVAILABLE:
            try:
                self.client = chromadb.Client(Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=str(self.persist_directory),
                    anonymized_telemetry=False
                ))

                # Obtener o crear coleccion
                self.collection = self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )

                logger.info(f"ChromaDB coleccion lista: {self.collection_name}")

            except Exception as e:
                logger.error(f"Error inicializando ChromaDB: {e}")
                # Fallback a cliente en memoria
                try:
                    self.client = chromadb.Client()
                    self.collection = self.client.get_or_create_collection(
                        name=self.collection_name
                    )
                    logger.info("ChromaDB en modo memoria")
                except Exception as e2:
                    logger.error(f"Error en fallback ChromaDB: {e2}")
        else:
            logger.warning("ChromaDB no disponible")

    def add_document(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        doc_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Agrega un documento al vector store.

        Args:
            text: Texto del documento
            metadata: Metadatos adicionales
            doc_id: ID unico del documento

        Returns:
            Resultado de la operacion
        """
        if not self.model or not self.collection:
            return {
                "success": False,
                "error": "RAG no inicializado correctamente"
            }

        try:
            # Generar ID si no se proporciona
            if not doc_id:
                doc_id = hashlib.md5(text.encode()).hexdigest()[:16]

            # Generar embedding
            embedding = self.model.encode(text).tolist()

            # Preparar metadatos
            meta = metadata or {}
            meta["timestamp"] = datetime.now().isoformat()
            meta["text_length"] = len(text)

            # Agregar a coleccion
            self.collection.add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[meta],
                ids=[doc_id]
            )

            return {
                "success": True,
                "doc_id": doc_id,
                "message": "Documento agregado exitosamente"
            }

        except Exception as e:
            logger.error(f"Error agregando documento: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def add_chunks(
        self,
        chunks: List[str],
        metadata: Optional[Dict[str, Any]] = None,
        source_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Agrega multiples chunks de un documento.

        Args:
            chunks: Lista de fragmentos de texto
            metadata: Metadatos comunes
            source_id: ID del documento fuente

        Returns:
            Resultado de la operacion
        """
        if not self.model or not self.collection:
            return {
                "success": False,
                "error": "RAG no inicializado correctamente"
            }

        try:
            # Generar IDs
            source_id = source_id or hashlib.md5(str(chunks).encode()).hexdigest()[:8]
            ids = [f"{source_id}_chunk_{i}" for i in range(len(chunks))]

            # Generar embeddings para todos los chunks
            embeddings = self.model.encode(chunks).tolist()

            # Preparar metadatos para cada chunk
            metadatas = []
            for i in range(len(chunks)):
                meta = dict(metadata) if metadata else {}
                meta["chunk_index"] = i
                meta["total_chunks"] = len(chunks)
                meta["source_id"] = source_id
                meta["timestamp"] = datetime.now().isoformat()
                metadatas.append(meta)

            # Agregar todos los chunks
            self.collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )

            return {
                "success": True,
                "source_id": source_id,
                "chunks_added": len(chunks),
                "message": f"{len(chunks)} chunks agregados exitosamente"
            }

        except Exception as e:
            logger.error(f"Error agregando chunks: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Busca documentos relevantes para una consulta.

        Args:
            query: Consulta de busqueda
            n_results: Numero de resultados a retornar
            filter_metadata: Filtros de metadatos

        Returns:
            Resultados de busqueda con scores
        """
        if not self.model or not self.collection:
            return {
                "success": False,
                "error": "RAG no inicializado correctamente",
                "results": []
            }

        try:
            # Generar embedding de la consulta
            query_embedding = self.model.encode(query).tolist()

            # Buscar en coleccion
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata
            )

            # Formatear resultados
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        "text": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "id": results['ids'][0][i] if results['ids'] else None,
                        "distance": results['distances'][0][i] if results.get('distances') else None
                    })

            return {
                "success": True,
                "query": query,
                "results": formatted_results,
                "total_results": len(formatted_results)
            }

        except Exception as e:
            logger.error(f"Error en busqueda: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": []
            }

    def search_and_combine(
        self,
        query: str,
        n_results: int = 5,
        separator: str = "\n\n---\n\n"
    ) -> str:
        """
        Busca y combina resultados en un solo texto.

        Util para inyectar contexto en templates.

        Args:
            query: Consulta de busqueda
            n_results: Numero de resultados
            separator: Separador entre resultados

        Returns:
            Texto combinado de todos los resultados
        """
        search_result = self.search(query, n_results)

        if not search_result.get("success") or not search_result.get("results"):
            return ""

        texts = [r["text"] for r in search_result["results"]]
        return separator.join(texts)

    def get_context_for_document(
        self,
        query: str,
        document_type: str = "cotizacion",
        n_results: int = 3
    ) -> Dict[str, Any]:
        """
        Obtiene contexto relevante para generar un documento.

        Busca informacion relacionada y la organiza por categorias.

        Args:
            query: Descripcion del documento a generar
            document_type: Tipo de documento
            n_results: Resultados por categoria

        Returns:
            Contexto organizado por secciones
        """
        # Busquedas especificas segun tipo de documento
        searches = {
            "cotizacion": [
                ("especificaciones", f"especificaciones tecnicas {query}"),
                ("precios", f"precios costos {query}"),
                ("normativa", f"normativa {query}")
            ],
            "proyecto": [
                ("alcance", f"alcance proyecto {query}"),
                ("cronograma", f"cronograma fases {query}"),
                ("recursos", f"recursos personal {query}")
            ],
            "informe": [
                ("antecedentes", f"antecedentes contexto {query}"),
                ("metodologia", f"metodologia procedimiento {query}"),
                ("resultados", f"resultados conclusiones {query}")
            ]
        }

        context = {}

        for category, search_query in searches.get(document_type, []):
            result = self.search(search_query, n_results=n_results)
            if result.get("success") and result.get("results"):
                context[category] = [r["text"] for r in result["results"]]

        return {
            "success": True,
            "document_type": document_type,
            "context": context,
            "total_fragments": sum(len(v) for v in context.values())
        }

    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """Elimina un documento por ID"""
        if not self.collection:
            return {"success": False, "error": "Coleccion no disponible"}

        try:
            self.collection.delete(ids=[doc_id])
            return {
                "success": True,
                "message": f"Documento {doc_id} eliminado"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def clear_collection(self) -> Dict[str, Any]:
        """Elimina todos los documentos de la coleccion"""
        if not self.client:
            return {"success": False, "error": "Cliente no disponible"}

        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            return {
                "success": True,
                "message": "Coleccion limpiada"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadisticas de la coleccion"""
        if not self.collection:
            return {"success": False, "error": "Coleccion no disponible"}

        try:
            count = self.collection.count()
            return {
                "success": True,
                "collection_name": self.collection_name,
                "document_count": count,
                "model": self.model_name,
                "embeddings_available": EMBEDDINGS_AVAILABLE,
                "chromadb_available": CHROMADB_AVAILABLE
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def is_available(self) -> bool:
        """Verifica si el sistema RAG esta disponible"""
        return self.model is not None and self.collection is not None


# Instancia global
rag_engine = RAGEngine()

def get_rag_engine() -> RAGEngine:
    """Obtiene la instancia del motor RAG"""
    return rag_engine
