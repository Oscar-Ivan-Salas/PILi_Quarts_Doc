
from docxtpl import DocxTemplate
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger("N04_Binary_Factory")

class WordMasterGenerator:
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
        self.master_template = self.templates_dir / "master_tesla.docx"

    def generate_document(self, data: dict, output_path: Path) -> Path:
        """
        Generates a Word document by injecting data into the Master Tesla Template (docxtpl)
        Protocol: Mirror Perfect
        """
        try:
            if not self.master_template.exists():
                raise FileNotFoundError(f"CRITICAL: Master Template not found at {self.master_template}")
            
            doc = DocxTemplate(self.master_template)
            
            # Prepare Context (Flattened for Jinja2 in Docx)
            # data comes from N04 which is already reasonably structured, but let's ensure mapping.
            
            # Header / Metadata
            context = {
                "TITULO_DOCUMENTO": data.get("titulo", "DOCUMENTO TÉCNICO"),
                "CLIENTE_NOMBRE": data.get("cliente", "CLIENTE GENERAL"),
                "PROYECTO_NOMBRE": data.get("proyecto", "PROYECTO GENERAL"),
                "FECHA": data.get("fecha", datetime.now().strftime("%d/%m/%Y")),
                "SUBTOTAL": f"{data.get('subtotal', 0):,.2f}",
                "IGV": f"{data.get('igv', 0):,.2f}",
                "TOTAL": f"{data.get('total', 0):,.2f}",
                "items": []
            }
            
            # Additional keys if present in data
            for k, v in data.items():
                if k not in context and isinstance(v, (str, int, float)):
                    context[k] = v
            
            # Items Loop
            input_items = data.get("items", [])
            for idx, item in enumerate(input_items, 1):
                params_item = {
                    "index": idx,
                    "descripcion": item.get("descripcion", ""),
                    "unidad": item.get("unidad", "UND"),
                    "cantidad": item.get("cantidad", 0),
                    "precio": f"{item.get('precio_unitario', 0):,.2f}",
                    "total": f"{item.get('total', 0):,.2f}"
                }
                context["items"].append(params_item)
            
            # Render
            logger.info(f"Injecting {len(context['items'])} items into Master Template...")
            doc.render(context)
            
            # Save
            output_path.parent.mkdir(parents=True, exist_ok=True)
            doc.save(output_path)
            
            logger.info(f"✅ Word Document Generated: {output_path.name}")
            return output_path

        except Exception as e:
            logger.error(f"WordMasterGenerator Failed: {e}", exc_info=True)
            raise

# Singleton
word_master_generator = WordMasterGenerator()
