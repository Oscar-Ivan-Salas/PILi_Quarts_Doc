# 🔧 MANUAL DE MANTENIMIENTO Y SOPORTE IT - PILi V3.0

Guía técnica para Administradores de Sistemas y DevOps encargados de mantener la salud operativa de PILi_Quarts.

---

## 1. 🔍 DIAGNÓSTICO RÁPIDO (Troubleshooting)

### Problema A: "Error de Conexión con el Asistente" 🔴
*   **Síntoma:** El chat muestra un mensaje rojo o se queda cargando infinitamente.
*   **Causa Probable:** El backend (FastAPI) se detuvo o no hay conexión a internet para Gemini.
*   **Solución:**
    1.  Verificar terminal del backend. Si está cerrada, ejecutar:
        `uvicorn app.main:app --reload`
    2.  Verificar logs del backend por errores `HttpxConnectionError` (falla de internet).

### Problema B: "No se generan los PDFs" 📄
*   **Síntoma:** El botón de descarga no hace nada o devuelve error 500.
*   **Causa Probable:**
    1.  Falta la carpeta `out/` o `temp/` en el servidor.
    2.  Permisos de escritura denegados.
*   **Solución:**
    ```bash
    # En la carpeta backend/
    mkdir temp
    chmod 777 temp  # En Linux
    ```

### Problema C: "Alucinaciones Matemáticas" 🧮
*   **Síntoma:** PILI da un precio incorrecto en el chat.
*   **Causa:** La IA está "adivinando" en lugar de usar la calculadora.
*   **Solución:** Recordar al usuario que **el precio final válido es el de la Vista Previa Editable**, no el del chat. El chat es estimativo; el documento editable usa el motor de cálculo Python.

---

## 2. 📊 UBICACIÓN DE LOGS

Para rastrear errores profundos:

*   **Backend Logs (Consola):**
    Uvicorn muestra los logs en tiempo real en la terminal. Buscar líneas con `ERROR:`.
*   **Frontend Logs (Navegador):**
    Presionar `F12` -> Pestaña `Console`. Aquí aparecen errores de React o de red (CORS).

---

## 3. 💾 COPIAS DE SEGURIDAD (BACKUPS)

### Base de Datos
Actualmente PILI usa **SQLite** (`tesla_cotizador.db`).

*   **Frecuencia:** Semanal.
*   **Procedimiento:** Copiar el archivo `backend/tesla_cotizador.db` a una ubicación segura (OneDrive/Google Drive corporativo).

### Código Fuente
El código vive en el repositorio Git. Asegurarse de hacer `git push` regularmente de cualquier cambio local.

---

## 4. 🔄 ACTUALIZACIÓN DEL SISTEMA

Cuando GatoMichuy libere una nueva versión:

1.  **Bajar cambios:**
    ```bash
    git pull origin main
    ```
2.  **Actualizar librerías (Backend):**
    ```bash
    cd backend
    pip install -r requirements.txt --upgrade
    ```
3.  **Actualizar librerías (Frontend):**
    ```bash
    cd frontend
    npm install
    npm run build
    ```
4.  **Reiniciar servicios.**

---
*Soporte Nivel 2 - GatoMichuy*
