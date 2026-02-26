# 🏭 N04_Binary_Factory (La Caja Negra - SOBERANO V10)
# =======================================================

Este módulo es una implementación **Soberana e Independiente** del corazón de generación de documentos de PILi.

## 🚀 Propósito
Transformar datos técnicos en documentos **DOCX, XLSX y PDF** de alta fidelidad. Este nodo funciona como un micro-servicio autónomo, sin dependencias externas del Core, facilitando su integración como módulo en cualquier aplicación web.

## 🛡️ Estatus Soberano (V10)
- **Independencia Total**: No importa archivos fuera de su directorio.
- **Motores Locales**: Incluye `excel_generator.py` y `html_parser.py` dentro de su carpeta.
- **Protocolo RALFTH**: Blindaje contra errores de índice y validación estricta de contrato via Pydantic.

## 📂 Estructura Modular
- `index.py`: Orquestador y Puente de Compatibilidad (Bridge Mode).
- `studio_api.py`: API FastAPI independiente (Puerto 8005).
- `generators/`: Motores binarios locales.
- `studio/`: Frontend React para pruebas y diseño vivo (Puerto 5173).
- `templates/html/`: Capa de presentación editable.

## 🛠️ Ejecución Independiente
1. Instalar requisitos: `pip install -r requirements_N04.txt`
2. Levantar API: `python studio_api.py` (Puerto 8005)
3. Levantar Studio: `cd studio && npm run dev` (Puerto 5173)

**MANTENER LA SOBERANÍA: NO IMPORTAR DESDE EL CORE EXTERNO.**
