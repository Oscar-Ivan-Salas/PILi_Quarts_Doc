"""
RAG Service - Retrieval Augmented Generation
Compatible con ChromaDB 0.4.x+
"""

import logging
from typing import List, Dict, Any, Optional

# Importación opcional de chromadb (puede no estar instalado)
try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    chromadb = None
    ChromaSettings = None

from app.core.config import settings # <<< CORRECCIÓN: Importar settings

logger = logging.getLogger(__name__)


class RAGService:
    """
    Servicio de RAG usando ChromaDB para almacenamiento vectorial
    """
    
    def __init__(self):
        """Inicializar el servicio RAG con manejo de errores"""
        self.collection_name = "tesla_cotizador_docs"
        self.client = None
        self.collection = None

        # Verificar si chromadb está disponible
        if not CHROMADB_AVAILABLE:
            logger.warning("⚠️ ChromaDB no está instalado - RAG Service en modo degradado")
            return

        try:
            # <<< CORRECCIÓN: Usar la ruta de settings en lugar de hardcodearla
            # Esto soluciona el Problema #3
            persist_directory = str(settings.CHROMA_PERSIST_DIRECTORY)

            self.client = chromadb.PersistentClient(
                path=persist_directory
            )

            logger.info(f"✅ ChromaDB client inicializado en: {persist_directory}")

            # Obtener o crear colección
            self.collection = self._get_or_create_collection()

            logger.info(f"✅ RAGService inicializado con colección '{self.collection_name}'")

        except Exception as e:
            logger.error(f"❌ Error al inicializar RAGService: {str(e)}")
            logger.warning("⚠️ RAG Service funcionará en modo degradado")
            self.client = None
            self.collection = None
    
    def _get_or_create_collection(self):
        """
        Obtener o crear la colección en ChromaDB
        """
        try:
            collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
            return collection
        except Exception as e:
            logger.error(f"Error al crear/obtener colección: {str(e)}")
            # Si hay un error (ej. 'no such column'), intentamos resetear
            try:
                logger.warning(f"Intentando resetear la colección '{self.collection_name}'...")
                self.client.delete_collection(name=self.collection_name)
                collection = self.client.get_or_create_collection(name=self.collection_name)
                logger.info("Colección reseteada y recreada exitosamente.")
                return collection
            except Exception as e2:
                logger.critical(f"Fallo crítico al resetear la colección: {e2}")
                raise e2

    def is_available(self) -> bool:
        """Verificar si el servicio RAG está disponible"""
        return self.client is not None and self.collection is not None
    
    def agregar_documento(self, doc_id: str, texto: str, metadata: Dict[str, Any]) -> bool:
        """
        Agregar un documento a la colección
        
        Args:
            doc_id: ID único del documento
            texto: Contenido de texto
            metadata: Metadatos (ej. {'proyecto_id': 1, 'nombre_archivo': 'test.pdf'})
        
        Returns:
            True si se agregó exitosamente
        """
        if not self.is_available():
            logger.warning("RAG Service no disponible, no se puede agregar documento")
            return False
        
        try:
            self.collection.add(
                documents=[texto],
                metadatas=[metadata],
                ids=[doc_id]
            )
            logger.info(f"Documento agregado a RAG: {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error al agregar documento a RAG: {str(e)}")
            return False
            
    def buscar(self, query: str, n_results: int = 5, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Buscar documentos relevantes en la colección
        
        Args:
            query: Texto de búsqueda
            n_results: Número de resultados
            where: Filtro de metadatos (ej. {'proyecto_id': 1})
        
        Returns:
            Lista de resultados
        """
        if not self.is_available():
            logger.warning("RAG Service no disponible, búsqueda omitida")
            return []
            
        try:
            if where:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    where=where
                )
            else:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results
                )
            
            # Formatear resultados
            output = []
            if results and results.get('documents'):
                for i, doc in enumerate(results['documents'][0]):
                    output.append({
                        "id": results['ids'][0][i],
                        "documento": doc,
                        "metadata": results['metadatas'][0][i],
                        "distancia": results['distances'][0][i]
                    })
            
            return output
            
        except Exception as e:
            logger.error(f"Error al buscar en RAG: {str(e)}")
            return []
    
    def eliminar_documentos(self, where: Dict[str, Any]) -> bool:
        """
        Eliminar documentos de la colección basado en metadatos
        
        Args:
            where: Filtro de metadatos (ej. {'proyecto_id': 1})
        
        Returns:
            True si se eliminó exitosamente
        """
        if not self.is_available():
            logger.warning("RAG Service no disponible")
            return False
        
        try:
            self.collection.delete(where=where)
            logger.info(f"Documentos eliminados de RAG (filtro: {where})")
            return True
            
        except Exception as e:
            logger.error(f"Error al eliminar documentos: {str(e)}")
            return False
    
    def get_collection_count(self) -> int:
        """Obtener número de documentos en la colección"""
        if not self.is_available():
            return 0
        
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Error al contar documentos: {str(e)}")
            return 0
    
    def reset_collection(self) -> bool:
        """
        Resetear la colección (eliminar todos los documentos)
        
        Returns:
            True si se reseteó exitosamente
        """
        if not self.client:
            logger.warning("RAG Service no disponible")
            return False
        
        try:
            # Eliminar colección existente
            self.client.delete_collection(name=self.collection_name)
            
            # Recrear colección
            self.collection = self._get_or_create_collection()
            
            logger.info("✅ Colección reseteada")
            return True
            
        except Exception as e:
            logger.error(f"Error al resetear colección: {str(e)}")
            return False


# Crear instancia global
try:
    rag_service = RAGService()
except Exception as e:
    logger.error(f"❌ Fallo al crear la instancia global de RAGService: {e}")
    rag_service = None # Dejarlo como None para que is_available() falle