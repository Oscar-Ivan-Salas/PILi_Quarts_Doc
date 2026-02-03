import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import PILIQuartsApp from './App';
import WorkspacePage from './pages/WorkspacePage';

/**
 * AppRouter - Router principal de la aplicación
 * 
 * IMPORTANTE: Este archivo NO modifica App.jsx existente
 * Solo agrega routing para la nueva ruta /workspace
 * 
 * Rutas:
 * - / → App.jsx original (sin cambios)
 * - /workspace → Nueva interfaz moderna
 */
const AppRouter = () => {
    return (
        <BrowserRouter>
            <Routes>
                {/* Ruta principal - App.jsx original sin cambios */}
                <Route path="/" element={<PILIQuartsApp />} />

                {/* Nueva ruta - Workspace moderno */}
                <Route path="/workspace" element={<WorkspacePage />} />

                {/* Redirect para rutas no encontradas */}
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </BrowserRouter>
    );
};

export default AppRouter;
