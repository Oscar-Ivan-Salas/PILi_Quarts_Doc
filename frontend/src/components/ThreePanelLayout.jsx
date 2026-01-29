import React, { useState, useMemo } from 'react';
import { X, Maximize2, Minimize2 } from 'lucide-react';

/**
 * ThreePanelLayout - Layout de 3 paneles estilo IDE
 * 
 * Inspirado en VS Code, Cursor, Windsurf
 * - Izquierda (30%): Formulario
 * - Centro (40%): Vista previa del documento
 * - Derecha (30%): Chat con PILI
 */
const ThreePanelLayout = ({ children }) => {
    const [leftPanelVisible, setLeftPanelVisible] = useState(true);
    const [rightPanelVisible, setRightPanelVisible] = useState(true);
    const [centerMaximized, setCenterMaximized] = useState(false);

    // Calcular anchos dinámicos
    const panelWidths = useMemo(() => {
        if (centerMaximized) {
            return { left: '0%', center: '100%', right: '0%' };
        }
        if (!leftPanelVisible && !rightPanelVisible) {
            return { left: '0%', center: '100%', right: '0%' };
        }
        if (!leftPanelVisible) {
            return { left: '0%', center: '70%', right: '30%' };
        }
        if (!rightPanelVisible) {
            return { left: '30%', center: '70%', right: '0%' };
        }
        return { left: '30%', center: '40%', right: '30%' };
    }, [leftPanelVisible, rightPanelVisible, centerMaximized]);

    return (
        <div className="flex h-screen bg-gray-950 overflow-hidden">
            {/* Panel Izquierdo - Formulario */}
            {leftPanelVisible && !centerMaximized && (
                <div
                    className="bg-gray-900 border-r-2 border-red-600 overflow-y-auto flex-shrink-0 transition-all duration-300"
                    style={{ width: panelWidths.left }}
                >
                    <div className="sticky top-0 z-10 bg-gray-900 border-b border-gray-800 px-4 py-3 flex items-center justify-between">
                        <h2 className="text-yellow-400 font-bold text-lg">
                            📋 Configuración del Proyecto
                        </h2>
                        <button
                            onClick={() => setLeftPanelVisible(false)}
                            className="text-gray-400 hover:text-white transition-colors"
                            title="Ocultar panel"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                    <div className="p-4">
                        {children[0]}
                    </div>
                </div>
            )}

            {/* Panel Central - Vista Previa */}
            <div
                className="bg-gray-800 overflow-y-auto flex-shrink-0 transition-all duration-300"
                style={{ width: panelWidths.center }}
            >
                <div className="sticky top-0 z-10 bg-gray-800 border-b border-gray-700 px-4 py-3 flex items-center justify-between">
                    <h2 className="text-white font-bold text-lg">
                        📄 Vista Previa del Documento
                    </h2>
                    <div className="flex items-center gap-2">
                        {!leftPanelVisible && (
                            <button
                                onClick={() => setLeftPanelVisible(true)}
                                className="text-gray-400 hover:text-yellow-400 transition-colors text-sm px-3 py-1 rounded bg-gray-700"
                            >
                                ← Formulario
                            </button>
                        )}
                        <button
                            onClick={() => setCenterMaximized(!centerMaximized)}
                            className="text-gray-400 hover:text-white transition-colors"
                            title={centerMaximized ? "Restaurar" : "Maximizar"}
                        >
                            {centerMaximized ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
                        </button>
                        {!rightPanelVisible && (
                            <button
                                onClick={() => setRightPanelVisible(true)}
                                className="text-gray-400 hover:text-yellow-400 transition-colors text-sm px-3 py-1 rounded bg-gray-700"
                            >
                                Chat PILI →
                            </button>
                        )}
                    </div>
                </div>
                <div className="p-6">
                    {children[1]}
                </div>
            </div>

            {/* Panel Derecho - Chat PILI */}
            {rightPanelVisible && !centerMaximized && (
                <div
                    className="bg-gray-900 border-l-2 border-red-600 flex flex-col flex-shrink-0 transition-all duration-300"
                    style={{ width: panelWidths.right }}
                >
                    <div className="bg-gray-900 border-b border-gray-800 px-4 py-3 flex items-center justify-between flex-shrink-0">
                        <h2 className="text-yellow-400 font-bold text-lg flex items-center gap-2">
                            🤖 PILI - Asistente IA
                        </h2>
                        <button
                            onClick={() => setRightPanelVisible(false)}
                            className="text-gray-400 hover:text-white transition-colors"
                            title="Ocultar panel"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                    <div className="flex-1 overflow-y-auto">
                        {children[2]}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ThreePanelLayout;
