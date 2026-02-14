
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

from app.core.config import get_generated_directory

class ExcelGenerator:
    def generar_cotizacion(self, datos: Dict[str, Any], ruta_salida: str) -> str:
        """
        Genera un archivo Excel simple con los datos de la cotización/proyecto
        """
        try:
            logger.info(f"Generando Excel en: {ruta_salida}")
            
            # 1. Preparar datos generales
            info_general = {
                'Campo': ['Cliente', 'Proyecto', 'Descripción', 'Fecha', 'Total'],
                'Valor': [
                    datos.get('cliente', {}).get('nombre', 'Desconocido'),
                    datos.get('proyecto', 'Sin Nombre'),
                    datos.get('descripcion', ''),
                    datetime.now().strftime("%d/%m/%Y"),
                    datos.get('total', 0)
                ]
            }
            df_info = pd.DataFrame(info_general)
            
            # 2. Preparar items
            items = datos.get('items', [])
            if not items:
                items = [{'Descripcion': 'Sin items', 'Cantidad': 0, 'Precio': 0, 'Total': 0}]
                
            df_items = pd.DataFrame(items)
            
            # 3. Escribir a Excel con múltiples hojas
            with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
                df_info.to_excel(writer, sheet_name='Resumen', index=False)
                df_items.to_excel(writer, sheet_name='Detalles', index=False)
                
            return ruta_salida
            
        except Exception as e:
            logger.error(f"Error generando Excel: {e}")
            raise e

excel_generator = ExcelGenerator()
