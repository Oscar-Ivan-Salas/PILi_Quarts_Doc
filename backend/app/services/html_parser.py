"""
Parser HTML → JSON
Extrae datos de HTML editado por el usuario y los convierte a JSON limpio
Diseñado para trabajar con las vistas previas editables de PILI
"""
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)


class HTMLParser:
    """
    Parser inteligente que extrae datos del HTML editado por el usuario
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parsear_html_editado(
        self,
        html: str,
        tipo_documento: str = "cotizacion"
    ) -> Dict[str, Any]:
        """
        Parsea HTML editado y retorna JSON estructurado

        Args:
            html: HTML editado por el usuario (con inputs, checkboxes, etc.)
            tipo_documento: Tipo de documento (cotizacion, proyecto, informe)

        Returns:
            Dict con datos extraídos y limpios
        """
        try:
            self.logger.info(f"🔍 Parseando HTML editado de tipo: {tipo_documento}")

            soup = BeautifulSoup(html, 'html.parser')

            # Seleccionar método según tipo de documento
            if "cotizacion" in tipo_documento.lower():
                datos = self._parsear_cotizacion(soup, tipo_documento)
            elif "proyecto" in tipo_documento.lower():
                datos = self._parsear_proyecto(soup, tipo_documento)
            elif "informe" in tipo_documento.lower():
                datos = self._parsear_informe(soup, tipo_documento)
            else:
                # Fallback genérico
                datos = self._parsear_generico(soup)

            self.logger.info(f"✅ HTML parseado exitosamente: {len(datos)} campos extraídos")
            return datos

        except Exception as e:
            self.logger.error(f"❌ Error parseando HTML: {str(e)}")
            return {
                "error": True,
                "mensaje": f"Error parseando HTML: {str(e)}"
            }

    def _parsear_cotizacion(self, soup: BeautifulSoup, tipo: str) -> Dict[str, Any]:
        """Parsea HTML de cotización"""

        datos = {
            "tipo_documento": tipo,
            "cliente": "",
            "proyecto": "",
            "numero": "",
            "fecha": "",
            "vigencia": "",
            "items": [],
            "observaciones": "",
            "mostrar_precios_unitarios": True,
            "mostrar_igv": True,
            "mostrar_total": True,
            "subtotal": 0.0,
            "igv": 0.0,
            "total": 0.0
        }

        # Extraer datos de encabezado (inputs o texto)
        datos["cliente"] = self._extraer_valor(soup, ["input[name='cliente']", ".cliente", "#cliente"])
        datos["proyecto"] = self._extraer_valor(soup, ["input[name='proyecto']", ".proyecto", "#proyecto"])
        datos["numero"] = self._extraer_valor(soup, ["input[name='numero']", ".numero", "#numero"])
        datos["fecha"] = self._extraer_valor(soup, ["input[name='fecha']", ".fecha", "#fecha"])
        datos["vigencia"] = self._extraer_valor(soup, ["input[name='vigencia']", ".vigencia"])

        # Extraer opciones de visualización (checkboxes)
        datos["mostrar_precios_unitarios"] = self._extraer_checkbox(soup, "mostrar_precios_unitarios")
        datos["mostrar_igv"] = self._extraer_checkbox(soup, "mostrar_igv")
        datos["mostrar_total"] = self._extraer_checkbox(soup, "mostrar_total")

        # Extraer items de la tabla
        tabla_items = soup.find('table', class_='items-table')
        if tabla_items:
            filas = tabla_items.find_all('tr')[1:]  # Saltar header

            for fila in filas:
                celdas = fila.find_all('td')
                if len(celdas) >= 4:
                    item = {
                        "descripcion": self._extraer_valor_celda(celdas[0]),
                        "cantidad": self._extraer_numero(celdas[1]),
                        "unidad": self._extraer_valor_celda(celdas[2]) or "und",
                        "precio_unitario": self._extraer_numero(celdas[3])
                    }

                    # Calcular subtotal del item
                    item["subtotal"] = item["cantidad"] * item["precio_unitario"]
                    datos["items"].append(item)

        # Calcular totales
        datos["subtotal"] = sum(item["subtotal"] for item in datos["items"])
        datos["igv"] = datos["subtotal"] * 0.18
        datos["total"] = datos["subtotal"] + datos["igv"]

        # Extraer observaciones
        datos["observaciones"] = self._extraer_valor(soup, ["textarea[name='observaciones']", ".observaciones"])

        return datos

    def _parsear_proyecto(self, soup: BeautifulSoup, tipo: str) -> Dict[str, Any]:
        """Parsea HTML de proyecto"""

        datos = {
            "tipo_documento": tipo,
            "nombre": "",
            "cliente": "",
            "codigo": "",
            "descripcion": "",
            "fecha_inicio": "",
            "fecha_fin": "",
            "duracion_total": "",
            "presupuesto": 0.0,
            "fases": [],
            "recursos": [],
            "riesgos": []
        }

        # Extraer datos básicos
        datos["nombre"] = self._extraer_valor(soup, ["input[name='nombre']", ".nombre", "#nombre"])
        datos["cliente"] = self._extraer_valor(soup, ["input[name='cliente']", ".cliente"])
        datos["codigo"] = self._extraer_valor(soup, ["input[name='codigo']", ".codigo"])
        datos["descripcion"] = self._extraer_valor(soup, ["textarea[name='descripcion']", ".descripcion"])
        datos["fecha_inicio"] = self._extraer_valor(soup, ["input[name='fecha_inicio']", ".fecha-inicio"])
        datos["fecha_fin"] = self._extraer_valor(soup, ["input[name='fecha_fin']", ".fecha-fin"])
        datos["duracion_total"] = self._extraer_valor(soup, ["input[name='duracion']", ".duracion"])
        datos["presupuesto"] = self._extraer_numero(soup.find('input', {'name': 'presupuesto'}))

        # Extraer fases (si hay tabla o lista)
        fases_container = soup.find('div', class_='fases') or soup.find('table', class_='fases-table')
        if fases_container:
            fases_elementos = fases_container.find_all(['tr', 'div'], class_=['fase-row', 'fase-item'])
            for elemento in fases_elementos:
                fase = {
                    "nombre": self._extraer_valor_elemento(elemento, [".fase-nombre", "input[name*='fase_nombre']"]),
                    "duracion": self._extraer_valor_elemento(elemento, [".fase-duracion", "input[name*='duracion']"]),
                    "estado": self._extraer_valor_elemento(elemento, [".fase-estado", "select"])
                }
                if fase["nombre"]:
                    datos["fases"].append(fase)

        return datos

    def _parsear_informe(self, soup: BeautifulSoup, tipo: str) -> Dict[str, Any]:
        """Parsea HTML de informe"""

        datos = {
            "tipo_documento": tipo,
            "titulo": "",
            "codigo": "",
            "cliente": "",
            "fecha": "",
            "autor": "",
            "resumen": "",
            "conclusiones": "",
            "recomendaciones": "",
            "secciones": []
        }

        # Extraer datos básicos
        datos["titulo"] = self._extraer_valor(soup, ["input[name='titulo']", ".titulo", "h1"])
        datos["codigo"] = self._extraer_valor(soup, ["input[name='codigo']", ".codigo"])
        datos["cliente"] = self._extraer_valor(soup, ["input[name='cliente']", ".cliente"])
        datos["fecha"] = self._extraer_valor(soup, ["input[name='fecha']", ".fecha"])
        datos["autor"] = self._extraer_valor(soup, ["input[name='autor']", ".autor"])

        # Extraer contenido
        datos["resumen"] = self._extraer_valor(soup, ["textarea[name='resumen']", ".resumen"])
        datos["conclusiones"] = self._extraer_valor(soup, ["textarea[name='conclusiones']", ".conclusiones"])
        datos["recomendaciones"] = self._extraer_valor(soup, ["textarea[name='recomendaciones']", ".recomendaciones"])

        return datos

    def _parsear_generico(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Parsea HTML genérico extrayendo todos los inputs"""

        datos = {"inputs": {}}

        # Extraer todos los inputs
        for input_elem in soup.find_all(['input', 'textarea', 'select']):
            name = input_elem.get('name') or input_elem.get('id')
            if name:
                if input_elem.name == 'input' and input_elem.get('type') == 'checkbox':
                    datos["inputs"][name] = input_elem.has_attr('checked')
                else:
                    datos["inputs"][name] = input_elem.get('value', '')

        return datos

    # ═══════════════════════════════════════════════════════════
    # UTILIDADES DE EXTRACCIÓN
    # ═══════════════════════════════════════════════════════════

    def _extraer_valor(self, soup: BeautifulSoup, selectores: List[str]) -> str:
        """Intenta extraer valor con múltiples selectores CSS"""
        for selector in selectores:
            elemento = soup.select_one(selector)
            if elemento:
                # Si es input/textarea/select, obtener value
                if elemento.name in ['input', 'textarea', 'select']:
                    return elemento.get('value', '').strip()
                # Si es otro elemento, obtener texto
                return elemento.get_text().strip()
        return ""

    def _extraer_valor_elemento(self, elemento, selectores: List[str]) -> str:
        """Extrae valor de un sub-elemento"""
        for selector in selectores:
            sub_elem = elemento.select_one(selector)
            if sub_elem:
                if sub_elem.name in ['input', 'textarea', 'select']:
                    return sub_elem.get('value', '').strip()
                return sub_elem.get_text().strip()
        return ""

    def _extraer_valor_celda(self, celda) -> str:
        """Extrae valor de una celda (td) que puede tener input o texto"""
        input_elem = celda.find(['input', 'textarea', 'select'])
        if input_elem:
            return input_elem.get('value', '').strip()
        return celda.get_text().strip()

    def _extraer_numero(self, elemento) -> float:
        """Extrae número de elemento, limpiando formato"""
        if elemento is None:
            return 0.0

        # Si es elemento BeautifulSoup
        if hasattr(elemento, 'name'):
            if elemento.name in ['input', 'textarea']:
                texto = elemento.get('value', '0')
            else:
                texto = elemento.get_text()
        else:
            texto = str(elemento)

        # Limpiar: quitar S/, comas, espacios
        texto = re.sub(r'[^\d.-]', '', texto.replace(',', ''))

        try:
            return float(texto)
        except ValueError:
            return 0.0

    def _extraer_checkbox(self, soup: BeautifulSoup, name: str) -> bool:
        """Extrae estado de checkbox"""
        checkbox = soup.find('input', {'name': name, 'type': 'checkbox'})
        if checkbox:
            return checkbox.has_attr('checked')
        return True  # Default: mostrar todo


# Instancia global
html_parser = HTMLParser()


# ═══════════════════════════════════════════════════════════
# FUNCIÓN DE AYUDA PARA TESTING
# ═══════════════════════════════════════════════════════════

def test_parser():
    """Función de prueba del parser"""

    html_prueba = """
    <html>
    <body>
        <input name="cliente" value="CLIENTE PRUEBA S.A.C.">
        <input name="proyecto" value="Instalación Eléctrica">
        <input name="numero" value="COT-202512-0001">

        <input type="checkbox" name="mostrar_igv" checked>

        <table class="items-table">
            <tr><th>Desc</th><th>Cant</th><th>Unidad</th><th>Precio</th></tr>
            <tr>
                <td><input value="Tablero eléctrico"></td>
                <td><input type="number" value="1"></td>
                <td>und</td>
                <td><input type="number" value="500.00"></td>
            </tr>
            <tr>
                <td><input value="Cable THW 10mm"></td>
                <td><input type="number" value="50"></td>
                <td>m</td>
                <td><input type="number" value="3.50"></td>
            </tr>
        </table>
    </body>
    </html>
    """

    parser = HTMLParser()
    resultado = parser.parsear_html_editado(html_prueba, "cotizacion-simple")

    print("=" * 60)
    print("TEST PARSER HTML→JSON")
    print("=" * 60)
    print(f"Cliente: {resultado['cliente']}")
    print(f"Proyecto: {resultado['proyecto']}")
    print(f"Número: {resultado['numero']}")
    print(f"Mostrar IGV: {resultado['mostrar_igv']}")
    print(f"Items: {len(resultado['items'])}")
    for i, item in enumerate(resultado['items'], 1):
        print(f"  Item {i}: {item['descripcion']} - {item['cantidad']} {item['unidad']} x S/ {item['precio_unitario']}")
    print(f"Subtotal: S/ {resultado['subtotal']:.2f}")
    print(f"IGV: S/ {resultado['igv']:.2f}")
    print(f"Total: S/ {resultado['total']:.2f}")
    print("=" * 60)


if __name__ == "__main__":
    test_parser()
