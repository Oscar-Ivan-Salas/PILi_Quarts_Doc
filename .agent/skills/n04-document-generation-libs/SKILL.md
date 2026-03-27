---
name: n04-document-generation-libs
description: Comparativa actualizada 2025 de las mejores librerías Python para generación de documentos Word, PDF y Excel desde HTML. Guía de selección y uso para el nodo N04-Studio.
---

# Librerías de Generación de Documentos 2025 — N04-Studio

> Esta es la guía de selección tecnológica para el nodo N04-Studio.
> Siempre usar la librería de mayor fidelidad disponible en el entorno.

## 📄 Generación Word (DOCX) — Ranking

| Librería | Fidelidad | Costo | Estado | Recomendación |
|---|---|---|---|---|
| **html4docx** | ⭐⭐⭐⭐ | 🆓 Gratis | Activo 2024 | ✅ **USAR — Reemplazo de htmldocx** |
| **python-docx** | ⭐⭐⭐ | 🆓 Gratis | Activo | ✅ Base obligatoria |
| **htmldocx** | ⭐⭐ | 🆓 Gratis | Abandonado | ⚠️ Tenemos pero sin updates |
| Spire.Doc | ⭐⭐⭐⭐⭐ | 💰 Pago | Activo | ❌ Comercial — no usar |
| Aspose.Words | ⭐⭐⭐⭐⭐ | 💰 Pago | Activo | ❌ Comercial — no usar |

**Acción:** Reemplazar `htmldocx` → `html4docx` en requirements.

---

## 📕 Generación PDF — Ranking

| Librería | Fidelidad CSS | JS Support | Velocidad | Recomendación |
|---|---|---|---|---|
| **Playwright** | ⭐⭐⭐⭐⭐ | ✅ Total | Media | ✅ **YA INSTALADO — ES EL MEJOR** |
| **WeasyPrint** | ⭐⭐⭐⭐ | ❌ No | Rápida | ✅ **AGREGAR — excelente fidelidad CSS** |
| pdfkit (wkhtmltopdf) | ⭐⭐⭐ | Parcial | Rápida | ⚠️ CSS moderno limitado |
| fpdf2 | ⭐⭐ | ❌ | Muy rápida | ⚠️ Solo texto/imágenes básicas |

**Acción:** Agregar `weasyprint` como fallback de alta calidad cuando no hay Playwright disponible.

---

## 📗 Generación Excel (XLSX) — Ranking

| Librería | Capacidad | Fidelidad HTML | Recomendación |
|---|---|---|---|
| **xlsxwriter** | Escritura avanzada | N/A | ✅ **AGREGAR — más robusto que openpyxl para escritura** |
| **pandas** | Lectura + Escritura | `pd.read_html()` | ✅ **AGREGAR — extrae tablas HTML directo** |
| **tablepyxl** | Bridge HTML→Excel | ⭐⭐⭐ | ✅ **AGREGAR — convierte `<table>` HTML a sheets** |
| openpyxl | Escritura avanzada | N/A | ✅ Ya instalado — mantener |

**Acción:** Agregar `pandas`, `xlsxwriter`, `tablepyxl`.

---

## 🔧 Stack Completo Recomendado 2025 para N04-Studio

```text
# PARSEO DE HTML
beautifulsoup4       ← Ya tenemos ✅
lxml                 ← Ya tenemos ✅
jinja2               ← Ya tenemos ✅

# WORD (DOCX)
python-docx          ← Ya tenemos ✅
html4docx            ← NUEVO (reemplaza htmldocx abandonado)

# PDF  
playwright           ← Ya tenemos ✅ (mejor opción HTML→PDF)
weasyprint           ← NUEVO (fallback CSS compliant sin browser)

# EXCEL
openpyxl             ← Ya tenemos ✅
xlsxwriter           ← NUEVO (escritura avanzada con estilos)
pandas               ← NUEVO (lectura de tablas HTML directa)
tablepyxl            ← NUEVO (bridge <table> HTML → Excel sheets)
```

---

## ⚙️ Protocolo de Instalación en el Nodo

```powershell
# Desde la carpeta raíz del nodo N04_Binary_Factory
pip install html4docx weasyprint xlsxwriter pandas tablepyxl
```

Luego actualizar `requirements_N04.txt` con las nuevas librerías.

---

## 🎯 Guía de Selección por Caso de Uso

| Necesito... | Usar |
|---|---|
| Word con tablas y estilos de color exacto | `html4docx` + `python-docx` |
| PDF pixel-perfect del HTML del usuario | `Playwright` |
| PDF rápido sin Chromium (servidor ligero) | `WeasyPrint` |
| Excel con tabla HTML intacta | `tablepyxl` + `openpyxl` |
| Excel con formato avanzado y gráficos | `xlsxwriter` |
| Extraer datos de tabla HTML para Excel | `pandas.read_html()` |
