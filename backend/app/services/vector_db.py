"""
Servicio de Base de Datos Vectorial para RAG de PILI
Usa ChromaDB para almacenar embeddings de cotizaciones
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class VectorDBService:
    """Servicio para ChromaDB - Embeddings de cotizaciones para RAG"""
    
    def __init__(self):
        # Crear directorio para ChromaDB si no existe
        db_path = Path("./storage/chromadb")
        db_path.mkdir(parents=True, exist_ok=True)
        
        # Inicializar ChromaDB en modo persistente
        self.client = chromadb.PersistentClient(path=str(db_path))
        
        # Crear/obtener colección de cotizaciones
        self.collection = self.client.get_or_create_collection(
            name="cotizaciones",
            metadata={"description": "Embeddings de cotizaciones para RAG de PILI"}
        )
        
        logger.info(f"✅ ChromaDB inicializado en {db_path}")
        logger.info(f"📊 Colección 'cotizaciones' tiene {self.collection.count()} documentos")
    
    def agregar_cotizacion(self, cotizacion_id: str, datos: Dict[str, Any]):
        """
        Agregar cotización a BD vectorial para RAG
        
        Args:
            cotizacion_id: ID único de la cotización
            datos: Datos completos de la cotización
        """
        try:
            # Crear texto descriptivo para embedding
            texto = self._crear_texto_embedding(datos)
            
            # Preparar metadata
            cliente = datos.get("cliente", {})
            metadata = {
                "cliente": cliente.get("nombre", "") if isinstance(cliente, dict) else str(cliente),
                "proyecto": datos.get("proyecto", ""),
                "total": float(datos.get("total", 0)),
                "fecha": datos.get("fecha", ""),
                "numero": datos.get("numero", "")
            }
            
            # Agregar a ChromaDB
            self.collection.add(
                ids=[cotizacion_id],
                documents=[texto],
                metadatas=[metadata]
            )
            
            logger.info(f"✅ Cotización {cotizacion_id} agregada a ChromaDB")
            
        except Exception as e:
            logger.error(f"❌ Error al agregar cotización a ChromaDB: {e}")
            # No fallar si ChromaDB falla, solo loggear
    
    def buscar_similares(self, query: str, n_results: int = 5) -> Dict:
        """
        Buscar cotizaciones similares para RAG
        
        Args:
            query: Texto de búsqueda (ej: "instalación eléctrica residencial")
            n_results: Número de resultados
            
        Returns:
            Diccionario con resultados de ChromaDB
        """
        try:
            if self.collection.count() == 0:
                logger.warning("⚠️ ChromaDB vacío, no hay cotizaciones para buscar")
                return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
            
            results = self.collection.query(
                query_texts=[query],
                n_results=min(n_results, self.collection.count())
            )
            
            logger.info(f"🔍 Encontradas {len(results['documents'][0])} cotizaciones similares")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error al buscar en ChromaDB: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    def _crear_texto_embedding(self, datos: Dict) -> str:
        """Crear texto descriptivo para embedding"""
        cliente = datos.get("cliente", {})
        items = datos.get("items", [])
        
        # Extraer nombre de cliente (puede ser dict u objeto)
        if isinstance(cliente, dict):
            nombre_cliente = cliente.get("nombre", "")
        else:
            nombre_cliente = str(cliente)
        
        # Crear descripción de items
        texto_items = " ".join([
            f"{item.get('descripcion', '')} {item.get('cantidad', '')} {item.get('unidad', '')}"
            for item in items
        ])
        
        # Texto completo para embedding
        texto = f"""
        Cliente: {nombre_cliente}
        Proyecto: {datos.get('proyecto', '')}
        Descripción: {datos.get('descripcion', '')}
        Items: {texto_items}
        Total: S/ {datos.get('total', 0):,.2f}
        Observaciones: {datos.get('observaciones', '')}
        """
        
        return texto.strip()

# Instancia global (lazy initialization)
_vector_db_instance = None

def get_vector_db() -> VectorDBService:
    """Obtener instancia de VectorDB (lazy initialization)"""
    global _vector_db_instance
    if _vector_db_instance is None:
        try:
            _vector_db_instance = VectorDBService()
        except Exception as e:
            logger.error(f"❌ Error al inicializar ChromaDB: {e}")
            logger.warning("⚠️ ChromaDB no disponible, continuando sin RAG")
            # Retornar un mock que no haga nada
            class MockVectorDB:
                def agregar_cotizacion(self, *args, **kwargs):
                    pass
                def buscar_similares(self, *args, **kwargs):
                    return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
            _vector_db_instance = MockVectorDB()
    return _vector_db_instance

