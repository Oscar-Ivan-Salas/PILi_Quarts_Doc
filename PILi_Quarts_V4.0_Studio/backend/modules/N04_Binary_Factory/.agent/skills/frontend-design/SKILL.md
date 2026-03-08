---
name: frontend-design
description: Principios de diseño para el Studio UI del N04. React + Vite + TailwindCSS v4. Puerto 5173.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Frontend Design — N04 Studio

> **Stack**: React 19 + TypeScript + Vite 7 + TailwindCSS v4 + Framer Motion + Monaco Editor
> **Puerto**: 5173 (proxy hacia backend en 8005)

---

## Identidad Visual del Studio N04

El Studio sigue el **ADN Visual Tesla PILi**:
- **Color primario** → configurable por el usuario (default: `#0052A3` azul Tesla)
- **Color secundario** → configurable (default: `#1E40AF`)
- **Tipografía** → Calibri/Inter (configurable)
- **Sin púrpura**: Purple Ban activo — nunca usar violet/purple como colores de UI base

---

## Componentes existentes en `studio/src/`

| Componente | Archivo | Función |
|---|---|---|
| **App.tsx** | `src/App.tsx` (23K) | Estado global, layout principal |
| **PersonalizerPanel** | `components/studio/PersonalizerPanel.tsx` | Panel de personalización (colores, logo, moneda) |
| **Editor (Monaco)** | Integrado en App.tsx | Editor HTML del template |
| **Preview Panel** | Integrado en App.tsx | Vista previa del documento |

---

## Principios de UI para el Studio

### 1. Paleta (60-30-10)
```
60% → Fondo oscuro (#0a0a0f negro profundo)
30% → Paneles y superficies (grises oscuros)
10% → Acentos de marca (color configurado por usuario)
```

### 2. Layout del Studio
```
┌─────────────────────────────────────────┐
│  HEADER (título + controles globales)   │
├──────────┬──────────────┬───────────────┤
│ PANEL    │   EDITOR     │    PREVIEW    │
│ Config   │   Monaco     │    HTML Live  │
│ (190px)  │   (flex 1)   │    (flex 1)   │
└──────────┴──────────────┴───────────────┘
```

### 3. Animaciones (Framer Motion)
- Usar `AnimatePresence` SIN `mode="wait"` (causa crash conocido)
- Transiciones suaves: `duration: 0.2-0.3s`
- Easing: `ease-out` para entradas, `ease-in` para salidas

### 4. Monaco Editor
- No transformar imports de `monaco-editor`
- Usar `@monaco-editor/react` como wrapper
- Configurar con `theme: "vs-dark"` para coherencia visual

---

## Anti-Patrones a Evitar

- ❌ `AnimatePresence mode="wait"` → causa crash de React
- ❌ Colores hardcodeados en componentes (usar CSS variables `--pili-primary`)
- ❌ Estilos inline para ADN Visual → siempre via `adn-visual-preview` style tag inyectado por backend
- ❌ Importar monaco-editor directamente (usar `@monaco-editor/react`)
