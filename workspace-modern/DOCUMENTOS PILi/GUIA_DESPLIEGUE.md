# 🚀 GUÍA DE DESPLIEGUE E INSTALACIÓN - PILi V3.0

Esta guía detalla los pasos técnicos para instalar **PILi_Quarts** (Backend + Frontend) en un entorno limpio (Servidor o PC de Desarrollo).

**Nivel Técnico Requerido:** Intermedio (Manejo de Terminal).

---

## 1. 📦 REQUISITOS PREVIOS DEL SISTEMA

Antes de comenzar, asegúrate de tener instalado:

### Software Base
*   **Git:** Para clonar el repositorio.
*   **Python:** Versión **3.12** o superior.
    *   Verificar con: `python --version`
*   **Node.js:** Versión **18 LTS** o superior.
    *   Verificar con: `node -v`
*   **Google Chrome:** Para visualizar la aplicación.

### Claves de API (Necesarias)
*   **Google Gemini API Key:** Obtener en [Google AI Studio](https://aistudio.google.com/).

---

## 2. 📥 INSTALACIÓN PASO A PASO

### PASO 1: Clonar el Repositorio
Abre tu terminal (PowerShell o CMD) y ejecuta:

```bash
git clone <URL_DEL_REPOSITORIO>
cd PILi_Quarts
```

---

### PASO 2: Configurar el Backend (Cerebro) 🧠

1.  **Navegar a la carpeta:**
    ```bash
    cd backend
    ```

2.  **Crear entorno virtual (Recomendado):**
    Aísla las librerías del sistema.
    ```bash
    python -m venv venv
    .\venv\Scripts\activate   # En Windows
    # source venv/bin/activate  # En Linux/Mac
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno:**
    *   Crea un archivo llamado `.env` dentro de la carpeta `backend/`.
    *   Pega el siguiente contenido (reemplazando `TU_CLAVE_AQUI`):

    ```env
    gemini_api_key=TU_CLAVE_DE_GOOGLE_AI_STUDIO_AQUI
    GEMINI_MODEL=gemini-pro
    DATABASE_URL=sqlite:///./tesla_cotizador.db
    ```

5.  **Iniciar el Servidor:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    *Si ves "Application startup complete", el backend está vivo en `http://localhost:8000`.*

---

### PASO 3: Configurar el Frontend (Interfaz) 💻

1.  **Abrir una NUEVA terminal** (no cierres la del backend).

2.  **Navegar a la carpeta:**
    ```bash
    cd PILi_Quarts/frontend
    ```

3.  **Instalar librerías de Node:**
    ```bash
    npm install
    # Si da error, intenta: npm install --legacy-peer-deps
    ```

4.  **Iniciar la Interfaz:**
    ```bash
    npm start
    ```

---

## 3. ✅ VERIFICACIÓN DE INSTALACIÓN

1.  Abre tu navegador en `http://localhost:3000`.
2.  Deberías ver la pantalla de bienvenida con el logo de **PILI**.
3.  Prueba el chat: Escribe "Hola" en el módulo de Electricidad.
4.  Si responde, ¡Todo está conectado! 🎉

---
*Dpto. de TI - GatoMichuy / TESLA*
