
"""
Parser HTML → JSON (Versión SOBERANA V10 - Protocolo RALFTH)
Propósito: Extrae datos del HTML editado en el Studio con blindaje ante errores de índice.
"""
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)

class HTMLParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parsear_html_editado(self, html: str, doc_type: str = "") -> Dict[str, Any]:
        """
        Extrae datos del HTML de forma defensiva para evitar el error 'list index out of range'.
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 1. Extracción de Metadatos y Encabezados
            datos = {
                "numero": self._extraer_valor(soup, ["#meta-doc", ".numero-cotizacion", ".numero", "#document-id"]),
                "cliente": self._extraer_valor(soup, ["#cliente-nombre", ".cliente-nombre", "#cliente", ".info-cliente b"]),
                "cliente_ruc": self._extraer_valor(soup, ["#cliente-ruc", ".cliente-ruc"]),
                "cliente_direccion": self._extraer_valor(soup, ["#cliente-direccion", ".cliente-direccion"]),
                "cliente_email": self._extraer_valor(soup, ["#cliente-email", ".cliente-email"]),
                
                "emisor_nombre": self._extraer_valor(soup, ["#emisor-nombre", ".emisor-nombre"]),
                "emisor_ruc": self._extraer_valor(soup, ["#emisor-ruc"]),
                "emisor_direccion": self._extraer_valor(soup, ["#emisor-direccion"]),
                
                "proyecto": self._extraer_valor(soup, ["#proyecto-nombre", ".proyecto-nombre", "#proyecto"]),
                "fecha": self._extraer_valor(soup, [".meta-doc", ".fecha", "#fecha", ".info-fecha"]),
                "vigencia": self._extraer_valor(soup, [".vigencia", ".info-card.resumen .info-value"]),
                "servicio_nombre": self._extraer_valor(soup, ["#servicio-nombre", "header h1", "h1"]),
                
                # KPIs y Métricas (PMI/APA)
                "spi": self._extraer_valor(soup, ["#kpi-spi", ".kpi-value"]),
                "cpi": self._extraer_valor(soup, ["#kpi-cpi"]),
                "roi": self._extraer_valor(soup, [".metrica-value", "#roi-value"]),
                "payback": self._extraer_valor(soup, ["#payback-value"]),
                
                "items": [],
                "subtotal": 0.0,
                "igv": 0.0,
                "total": 0.0
            }

            # 2. Procesamiento Inteligente de Tabla de Items
            # Buscamos la primera tabla que contenga encabezados de items
            tabla = soup.find('table')
            if tabla:
                filas = tabla.find_all('tr')
                if len(filas) > 1:
                    # Detectar mapeo de columnas dinámicamente
                    header_fila = filas[0]
                    columnas = [td.get_text().strip().upper() for td in header_fila.find_all(['th', 'td'])]
                    
                    # Intentar encontrar índices por nombre de columna (Robustez Semántica)
                    idx_desc = self._buscar_indice(columnas, ["DETALLE", "DESCRIPCIÓN", "ITEM", "DESCRIPCION"])
                    idx_cant = self._buscar_indice(columnas, ["CANT", "CANTIDAD"])
                    idx_pu = self._buscar_indice(columnas, ["P.U", "P/U", "UNITARIO", "PRECIO"])
                    idx_total = self._buscar_indice(columnas, ["TOTAL", "SUBTOTAL"])
                    idx_und = self._buscar_indice(columnas, ["UND", "UNIDAD"])

                    # Procesar filas de datos
                    for fila in filas[1:]:
                        celdas = fila.find_all('td')
                        if not celdas: continue
                        
                        num_celdas = len(celdas)
                        
                        # Extraer valores con protección de índices
                        item = {
                            "n": len(datos["items"]) + 1,
                            "descripcion": self._safe_cell_text(celdas, idx_desc if idx_desc < num_celdas else 1 if num_celdas > 1 else 0),
                            "cantidad": self._safe_cell_num(celdas, idx_cant if idx_cant < num_celdas else 2 if num_celdas > 2 else 1),
                            "unidad": self._safe_cell_text(celdas, idx_und if idx_und < num_celdas else 3 if num_celdas > 3 else -1) or "und",
                            "precio_unitario": self._safe_cell_num(celdas, idx_pu if idx_pu < num_celdas else 4 if num_celdas > 4 else 2),
                            "total": self._safe_cell_num(celdas, idx_total if idx_total < num_celdas else 5 if num_celdas > 5 else num_celdas-1)
                        }

                        if item["descripcion"] and item["descripcion"].strip():
                            datos["items"].append(item)

            # 3. Extracción de Totales con múltiples fallbacks
            # Intentamos por ID primero, luego por selectores de clase, luego por texto
            datos["subtotal"] = self._extraer_numero_smart(soup, ["#total-subtotal", ".subtotal-valor", "#subtotal"])
            datos["igv"] = self._extraer_numero_smart(soup, ["#total-igv", ".igv-valor", "#igv"])
            datos["total"] = self._extraer_numero_smart(soup, ["#total-general", ".total-valor", "#total", ".grand-total"])

            # 4. Lógica de Autocorrección (Integridad de Datos RALFTH)
            # Si el total es 0 pero hay items, recalculamos para evitar documentos vacíos
            if datos["total"] <= 0 and datos["items"]:
                calc_subtotal = sum(i["total"] for i in datos["items"])
                # Si los totales en línea también son 0, usamos Cantidad * PU
                if calc_subtotal <= 0:
                    calc_subtotal = sum(i["cantidad"] * i["precio_unitario"] for i in datos["items"])
                    # Actualizar totales de items si estaban en 0
                    for i in datos["items"]:
                        if i["total"] <= 0: i["total"] = i["cantidad"] * i["precio_unitario"]
                
                datos["subtotal"] = calc_subtotal
                datos["igv"] = calc_subtotal * 0.18
                datos["total"] = calc_subtotal + datos["igv"]
                logger.info(f"⚡ Totales recalculados por seguridad: {datos['total']}")

            return datos

        except Exception as e:
            logger.error(f"❌ Error crítico en HTMLParser: {e}", exc_info=True)
            return {"error": True, "mensaje": str(e), "items": []}

    def _buscar_indice(self, columnas, terminos):
        for i, col in enumerate(columnas):
            if any(t in col for t in terminos):
                return i
        return 99 # Fuera de rango para forzar fallback

    def _safe_cell_text(self, celdas, idx):
        if idx < 0 or idx >= len(celdas): return ""
        inp = celdas[idx].find(['input', 'textarea'])
        if inp: return inp.get('value', '').strip()
        return celdas[idx].get_text().strip()

    def _safe_cell_num(self, celdas, idx):
        txt = self._safe_cell_text(celdas, idx)
        return self._limpiar_numero(txt)

    def _extraer_valor(self, soup, selectores):
        for s in selectores:
            try:
                el = soup.select_one(s)
                if el:
                    # Prioridad a inputs editables en el Studio
                    if el.name in ['input', 'textarea']:
                        return el.get('value', '').strip()
                    # Limpiar placeholders {{ }} si quedaron
                    return el.get_text().strip().replace('{{','').replace('}}','')
            except: continue
        return ""

    def _extraer_numero_smart(self, soup, selectores):
        val = self._extraer_valor(soup, selectores)
        if not val:
            # Búsqueda desesperada por texto descriptivo cerca de la etiqueta
            for text in ["TOTAL", "Total", "Grand Total", "Subtotal"]:
                el = soup.find(string=re.compile(text))
                if el and el.parent:
                    # Buscar el número más cercano en el hermano o el padre
                    nums = re.findall(r'[\d,.]+', el.parent.get_text())
                    if nums: return self._limpiar_numero(nums[-1])
        return self._limpiar_numero(val)

    def _limpiar_numero(self, txt):
        if not txt: return 0.0
        # Eliminar moneda, comas y espacios, preservar punto decimal y signo menos
        txt = str(txt).replace(',', '').replace('S/', '').replace('$', '').strip()
        txt = re.sub(r'[^\d.-]', '', txt)
        try:
            return float(txt)
        except:
            return 0.0

html_parser = HTMLParser()
