# Plan de Implementación: Corrección de Lógica ITSE y Fallback

## 🥅 Objetivo
Solucionar el problema crítico donde el chat genera cotizaciones eléctricas por defecto cuando se consulta por ITSE. Esto se debe a que la clase `ITSESpecialist` no está implementada en el sistema de fallback (`Nivel 3`) y el sistema principal (`Nivel 2`) está fallando silenciosamente.

## 🚨 User Review Required
> [!IMPORTANT]
> Se modificará `pili_local_specialists.py` para agregar la clase faltante `ITSESpecialist`. Esta es una intervención mayor en el backend que habilitará el funcionamiento correcto del servicio ITSE incluso si la nueva arquitectura falla.

## 📝 Proposed Changes

### Backend

#### [MODIFY] [pili_local_specialists.py](file:///e:/TESLA_COTIZADOR-V3.0/backend/app/services/pili_local_specialists.py)
*   **Implementar `class ITSESpecialist(LocalSpecialist)`**:
    *   Agregar lógica específica para manejar las etapas de ITSE: `categoria`, `tipo`, `area`, `pisos`.
    *   Implementar método `_process_itse(self, message)`.
    *   Conectar el cálculo de precios usando las reglas definidas en `KNOWLEDGE_BASE['itse']`.

#### [MODIFY] [pili_integrator.py](file:///e:/TESLA_COTIZADOR-V3.0/backend/app/services/pili_integrator.py)
*   **Mejorar logging de errores**: Hacer visibles las excepciones de `UniversalSpecialist` (Nivel 2) para facilitar la depuración futura.
*   **Validar importación**: Asegurar que si falla Nivel 2, el fallback a Nivel 3 use explícitamente el servicio ITSE y no "electricidad".

## 🚨 Emergency Changes (User Requested)
#### [MODIFY] [pili_integrator.py](file:///e:/TESLA_COTIZADOR-V3.0/backend/app/services/pili_integrator.py)
*   **GLOBAL KILL SWITCH en Gemini**: Se ha comentado la inicialización del servicio `gemini_service` en `PILIIntegrator`.
    *   **Motivo**: La IA ("Nivel 1") interceptaba solicitudes de ITSE y alucinaba respuestas de "Instalaciones Eléctricas", impidiendo que la lógica determinista ("Nivel 3") tomara el control.
    *   **Estado**: Gemini APAGADO. El sistema ahora es 100% determinista usando `LocalSpecialist`.

## ✅ Verification Plan

### Manual Verification
1.  **Reiniciar Backend**: Asegurar que los cambios se carguen (`uvicorn` reload).
2.  **Prueba Flujo ITSE**:
    *   Ir a Frontend -> Chat ITSE.
    *   Mensaje: "Iniciar". -> Debe mostrar categorías de ITSE (Salud, Educación, etc.), NO residencial/comercial.
    *   Seleccionar "Salud". -> Debe preguntar tipo de establecimiento.
    *   Seleccionar "Clínica". -> Debe preguntar Área.
    *   Ingresar "200". -> Debe preguntar Pisos.
    *   Ingresar "2". -> Debe generar cotización ITSE.
3.  **Confirmar ausencia de "Electricidad"**: Verificar que en ningún momento mencione "Instalaciones Eléctricas" o "CNE Suministro" (salvo que sea normativa ITSE).

### Automated Tests
*   No se crearán tests automatizados nuevos, se usará verificación manual exhaustiva ya que es un flujo conversacional complejo.
