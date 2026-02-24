
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional
from docxtpl import DocxTemplate
from html_parser import html_parser

logger = logging.getLogger(__name__)

class WordMasterGenerator:
    """
    Generador de Alta Fidelidad usando DocxTemplate y Masters de 38KB.
    Preserva el diseño original inyectando datos directamente.
    """
    
    BASE_DIR = Path(__file__).parent
    MASTERS_DIR = BASE_DIR / "templates" / "word_masters"
    
    # Mapeo de tipos de documento a archivos master
    MASTER_MAPPING = {
        "cotizacion_compleja": "master_cotizacion_compleja.docx",
        "cotizacion_simple": "master_cotizacion_simple.docx",
        "informe_ejecutivo_apa": "master_informe_ejecutivo_apa.docx",
        "informe_tecnico": "master_informe_tecnico.docx",
        "proyecto_complejo_pmi": "master_proyecto_complejo_pmi.docx",
        "proyecto_simple": "master_proyecto_simple.docx"
    }

    def generate(self, html_content: str, output_path: str, doc_type: str) -> Dict[str, Any]:
        """
        Genera un Word (.docx) basado en un master.
        """
        try:
            # 1. Identificar el master
            master_file = self.MASTER_MAPPING.get(doc_type.lower())
            if not master_file:
                # Intento de búsqueda por coincidencia parcial si falla el exacto
                for key, val in self.MASTER_MAPPING.items():
                    if key in doc_type.lower():
                        master_file = val
                        break
            
            if not master_file:
                 return {"success": False, "error": f"Tipo de documento '{doc_type}' no mapeado a un master."}

            master_path = self.MASTERS_DIR / master_file
            if not master_path.exists():
                return {"success": False, "error": f"Archivo master no encontrado en {master_path}"}

            # 2. Parsear el HTML para obtener el contexto (datos)
            context = html_parser.parsear_html_editado(html_content, doc_type)
            if context.get("error"):
                return {"success": False, "error": f"Error parseando HTML: {context.get('mensaje')}"}

            # Estandarizar tags a minúsculas (docxtpl suele usarlos así)
            # El context ya viene mayormente en minúsculas desde html_parser
            
            # 3. Renderizar con DocxTemplate
            logger.info(f"✨ Renderizando master {master_file} con docxtpl...")
            doc = DocxTemplate(str(master_path))
            doc.render(context)
            
            # 4. Guardar resultado
            doc.save(output_path)
            
            logger.info(f"✅ Documento generado exitosamente: {output_path}")
            return {
                "success": True, 
                "path": output_path,
                "type": doc_type,
                "master_used": master_file
            }

        except Exception as e:
            logger.error(f"❌ Error crítico en WordMasterGenerator: {e}")
            return {"success": False, "error": str(e)}

word_master_generator = WordMasterGenerator()
