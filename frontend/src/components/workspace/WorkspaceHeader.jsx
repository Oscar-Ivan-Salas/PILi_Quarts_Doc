import React from 'react';
import { Home, Save } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import PiliAvatar from '../PiliAvatar';
import ThemeToggle from './ThemeToggle';

/**
 * WorkspaceHeader - Barra superior del workspace
 * 
 * Características:
 * - Logo y breadcrumbs
 * - Selector de tema
 * - Botones de acción
 * - Avatar del usuario
 */
const WorkspaceHeader = () => {
    const navigate = useNavigate();

    return (
        <header className="h-16 bg-gray-900 dark:bg-gray-900 light:bg-white border-b-2 border-red-600 flex items-center justify-between px-6 shadow-lg">
            {/* Logo y Navegación */}
            <div className="flex items-center gap-4">
                <h1 className="text-2xl font-bold text-yellow-400">PILi_Quarts</h1>
                <span className="text-gray-400 dark:text-gray-400 light:text-gray-600">/ Workspace</span>
            </div>

            {/* Acciones */}
            <div className="flex items-center gap-4">
                {/* Theme Toggle */}
                <ThemeToggle />

                {/* Botón Volver al Inicio */}
                <button
                    onClick={() => navigate('/')}
                    className="px-4 py-2 bg-gray-700 hover:bg-gray-600 dark:bg-gray-700 dark:hover:bg-gray-600 light:bg-gray-200 light:hover:bg-gray-300 text-white dark:text-white light:text-gray-800 rounded-lg transition-all flex items-center gap-2"
                    title="Volver al inicio">
                    <Home className="w-4 h-4" />
                    <span className="hidden md:inline">Inicio</span>
                </button>

                {/* Botón Guardar */}
                <button
                    className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg font-medium transition-all shadow-md hover:shadow-lg">
                    Guardar
                </button>

                {/* Avatar */}
                <div className="flex items-center gap-2">
                    <PiliAvatar size={32} showCrown={true} />
                </div>
            </div>
        </header>
    );
};

export default WorkspaceHeader;
