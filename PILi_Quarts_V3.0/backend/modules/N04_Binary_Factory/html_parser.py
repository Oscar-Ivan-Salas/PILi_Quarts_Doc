
"""
Parser HTML → JSON (Versión Sincronizada con Masters - Protocolo Mirror)
Propósito: Extrae datos del HTML usando selectores dinámicos y los mapea a tags de Word.
"""
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)

class HTMLParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parsear_html_editado(self, html: str, tipo_documento: str = "cotizacion") -> Dict[str, Any]:
        """
        Extrae datos del HTML y los devuelve en un diccionario compatible con docxtpl.
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Datos comunes a todos los documentos (Case-Insensitive Mapping)
            datos = {
                # Mapeo a tags de Word (Mayúsculas por estándar de masters)
                "NUMERO_COTIZACION": self._extraer_valor(soup, ["#meta-doc", ".numero-cotizacion", ".numero"]),
                "CLIENTE_NOMBRE": self._extraer_valor(soup, ["#cliente-nombre", ".cliente-nombre"]),
                "CLIENTE_RUC": self._extraer_valor(soup, ["#cliente-ruc", ".cliente-ruc"]),
                "CLIENTE_DIRECCION": self._extraer_valor(soup, ["#cliente-direccion", ".cliente-direccion"]),
                "CLIENTE_EMAIL": self._extraer_valor(soup, ["#cliente-email", ".cliente-email"]),
                
                # Datos del Emisor (Soberanía)
                "NOMBRE_EMISOR": self._extraer_valor(soup, ["#emisor-nombre"]),
                "RUC_EMISOR": self._extraer_valor(soup, ["#emisor-ruc"]),
                "DIRECCION_EMISOR": self._extraer_valor(soup, ["#emisor-direccion"]),
                "EMAIL_EMISOR": self._extraer_valor(soup, ["#emisor-email"]),
                "TELEFONO_EMISOR": self._extraer_valor(soup, ["#emisor-tel"]),
                
                "PROYECTO_NOMBRE": self._extraer_valor(soup, ["#proyecto-nombre", ".proyecto-nombre"]),
                "FECHA_COTIZACION": self._extraer_valor(soup, [".meta-doc", ".fecha"]),
                "VIGENCIA": self._extraer_valor(soup, [".vigencia", ".info-card.resumen .info-value"]),
                
                # Items y Totales
                "items": [],
                "SUBTOTAL": 0.0,
                "IGV": 0.0,
                "TOTAL": 0.0
            }

            # Procesar tabla de items
            tabla = soup.find('table')
            if tabla:
                filas = tabla.find_all('tr')[1:] # Saltar header
                for fila in filas:
                    celdas = fila.find_all('td')
                    if len(celdas) >= 6:
                        item = {
                            "item": self._extraer_valor_celda(celdas[0]),
                            "descripcion": self._extraer_valor_celda(celdas[1]),
                            "cantidad": self._extraer_numero(celdas[2]),
                            "unidad": self._extraer_valor_celda(celdas[3]),
                            "precio_unitario": self._extraer_numero(celdas[4]),
                            "total": self._extraer_numero(celdas[5])
                        }
                        if item["descripcion"]:
                            datos["items"].append(item)

            # Extraer totales directos o calcular
            datos["SUBTOTAL"] = self._extraer_numero(soup.select_one(".totales-valor:contains('SUBTOTAL')") or datos.get("SUBTOTAL"))
            datos["IGV"] = self._extraer_numero(soup.select_one(".totales-valor:contains('IGV')") or datos.get("IGV"))
            datos["TOTAL"] = self._extraer_numero(soup.select_one(".totales-row:last-child .totales-valor") or datos.get("TOTAL"))
            
            # Recalcular si vienen en 0
            if datos["TOTAL"] == 0 and datos["items"]:
                datos["SUBTOTAL"] = sum(i["total"] for i in datos["items"])
                datos["IGV"] = datos["SUBTOTAL"] * 0.18
                datos["TOTAL"] = datos["SUBTOTAL"] + datos["IGV"]

            return datos

        except Exception as e:
            logger.error(f"Error parseando HTML: {e}")
            return {"error": True, "mensaje": str(e)}

    def _extraer_valor(self, soup, selectores):
        for s in selectores:
            el = soup.select_one(s)
            if el:
                # Si es un input o textarea
                if el.name in ['input', 'textarea']:
                    return el.get('value', el.get_text()).strip()
                return el.get_text().strip().replace('{{','').replace('}}','')
        return ""

    def _extraer_valor_celda(self, celda):
        inp = celda.find('input')
        if inp: return inp.get('value').strip()
        return celda.get_text().strip()

    def _extraer_numero(self, el):
        if not el: return 0.0
        txt = el.get_text() if hasattr(el, 'get_text') else str(el)
        # Limpiar moneda y comas
        txt = re.sub(r'[^\d.-]', '', txt.replace(',', ''))
        try: return float(txt)
        except: return 0.0

html_parser = HTMLParser()
