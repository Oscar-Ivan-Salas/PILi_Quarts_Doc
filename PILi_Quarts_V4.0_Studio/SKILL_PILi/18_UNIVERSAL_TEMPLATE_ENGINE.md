# SKILL 18: UNIVERSAL TEMPLATE ENGINE (WYSIWYG)

> **Standard**: BLACK BOX ATOMIC
> **Version**: 1.0
> **Status**: ACTIVE

## 1. The Concept: "Dynamic Mirror"

The N04 Binary Factory is not just a hardcoded script generator; it is a **Universal Template Engine**.
It follows the "Dynamic Mirror" architecture:
- **Input**: A folder containing `layout.html`, `mapping.json`, `style.css`.
- **Process**: The Python Engine reads the `mapping.json` to understand where to place data in the target format (XLSX, DOCX, PDF).
- **Output**: A document that visually mirrors the `layout.html` but allows for native format features (formulas in Excel, vectors in PDF).

## 2. Directory Structure

Every template MUST reside in its own folder within `backend/modules/N04_Binary_Factory/templates/`:

```
/templates/
  ├── MODELO_COTIZACION_SIMPLE/
  │     ├── layout.html        # WYSIWYG View for Dashboard
  │     ├── mapping.json       # Coordinates for Excel/Word
  │     └── style.css          # Shared Styles (Fonts, Colors)
  ├── MODELO_USUARIO_TEST/
  │     ├── ...
  └── ...
```

## 3. Mapping Contract (`mapping.json`)

The `mapping.json` file defines the relationship between Data Keys and Document Coordinates.

```json
{
  "meta": {
    "name": "User Test Model",
    "version": "1.0"
  },
  "excel_layout": {
    "sheet_name": "Proforma",
    "static_cells": {
      "B2": "CORPORACIÓN TEST",
      "B4": "{date}"
    },
    "dynamic_cells": {
      "user_name": "B6",
      "service_name": "B7",
      "total_label": "E20",
      "total_value": "F20"
    },
    "tables": [
      {
        "data_key": "items",
        "start_row": 10,
        "columns": {
          "index": "B",
          "description": "C",
          "unit": "D",
          "quantity": "E",
          "price": "F",
          "total": "G"
        },
        "style": "table_blue"
      }
    ]
  },
  "styles": {
    "colors": {
      "primary": "#0052A3",
      "text": "#333333"
    }
  }
}
```

## 4. Implementation Rules

1. **Auto-Discovery**: The system must check `templates/` for available models at runtime or configuration.
2. **Fallback**: If a `mapping.json` is missing/invalid, fallback to Hardcoded Logic (Legacy Mode) or return error.
3. **Hot-Swap**: Editing `mapping.json` must instantly change the output generation without restarting the server.
