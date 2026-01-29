# ✅ PLAN DE PRUEBAS Y QA (Control de Calidad) - PILi V3.0

Protocolo de validación obligatorio antes de cualquier pase a producción.

**Objetivo:** Asegurar que las funciones críticas del negocio (cotizar, cobrar, informar) no fallen.

---

## 1. 🧪 PRUEBAS CRÍTICAS (HAPPY PATH)

Estos flujos deben funcionar PERFECTAMENTE en cada versión.

### CASO 1: Generación de Cotización Eléctrica (Flujo Completo)
1.  **Entrada:** Usuario ingresa "Cotiza instalación de 5 luminarias LED industriales".
2.  **Interacción:** El usuario responde a las preguntas de PILI (altura, tipo de techo).
3.  **Verificación 1:** PILI debe generar un resumen de costos en el chat.
4.  **Acción:** Hacer clic en "👁️ Ver Cotización Completa".
5.  **Verificación 2:** Se abre el modal editable. Los precios NO deben ser cero.
6.  **Acción Final:** Hacer clic en "Descargar PDF".
7.  **Resultado Esperado:** Un archivo `.pdf` se descarga con el logo de Tesla y los ítems correctos.

### CASO 2: Creación de Plan de Proyecto PMI
1.  **Entrada:** Usuario selecciona "Gestión de Proyectos" -> "Crear Nuevo Proyecto".
2.  **Acción:** Usuario sube un PDF (TDR o Plano).
3.  **Verificación 1:** PILI confirma "He leído el archivo..."
4.  **Acción:** Usuario pide "Generar Cronograma".
5.  **Resultado Esperado:** Se muestra una tabla Gantt con fases lógicas (Planificación -> Ejecución -> Cierre).

---

## 2. ⚠️ PRUEBAS DE ESTRÉS Y BORDES (EDGE CASES)

### CASO 3: Entrada Vacía o "Basura"
*   **Acción:** Enviar "alskdjalksdj" o mensaje vacío.
*   **Resultado Esperado:** PILI debe responder educadamente pidiendo clarificación, **NO** debe crashear ni mostrar error de código Python.

### CASO 4: Interrupción de Internet
*   **Acción:** Desconectar internet mientras PILI "está escribiendo...".
*   **Resultado Esperado:** La interfaz debe mostrar "Error de conexión, reintentando..." y permitir reenviar el mensaje, sin borrar el historial.

---

## 3. 📝 LISTA DE CHEQUEO PRE-DEPLOY

Antes de instalar en el servidor de Tesla, el Ing. de Sistemas debe marcar:

- [ ] Todas las pruebas "Happy Path" pasaron en local.
- [ ] No hay credenciales (API Keys) quemadas en el código (usar `.env`).
- [ ] La base de datos de precios está actualizada al mes corriente.
- [ ] El puerto 8000 (Backend) y 3000 (Frontend) están libres.

---
*QA Team - GatoMichuy*
