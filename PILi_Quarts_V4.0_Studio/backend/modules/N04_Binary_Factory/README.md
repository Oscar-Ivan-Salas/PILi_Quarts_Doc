# 🏭 N04_Binary_Factory (La Caja Negra)

Este módulo es la implementación operativa del Skill **`@binary-factory`**.

## 🚀 Propósito
Es el corazón de generación de documentos de PILi. Utiliza tecnología de micro-agentes para transformar datos en documentos DOCX, XLSX y PDF de alta fidelidad.

## 🛡️ Protocolo
Este módulo debe mantenerse como una "Caja Negra" operativa. Cualquier modificación en el comportamiento de los generadores debe estar guiada por las reglas definidas en el Skill local:
`/.agent/skills/binary-factory/SKILL.md`

## 📂 Componentes
- `index.py`: Orquestador de micro-agentes.
- `generators/`: Motores binarios (Word, Excel, PDF) optimizados.
- `templates/html/`: La interfaz editable del sistema.

**NO MODIFICAR LA LÓGICA DE GENERADORES PROBADOS.** Priorizar siempre la edición de los templates HTML para cambios visuales.
