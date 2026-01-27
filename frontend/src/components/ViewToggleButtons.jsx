import React from 'react';
import { MessageSquare, Layout, Eye } from 'lucide-react';

/**
 * Componente reutilizable para botones de toggle de vista
 * Diseño profesional con iconos elegantes
 */
const ViewToggleButtons = ({ viewMode, setViewMode }) => {
    // Si no se pasan las props, no renderizar nada
    if (!viewMode || !setViewMode) return null;

    return (
        <div className="flex items-center gap-1.5 bg-white/5 backdrop-blur-md rounded-lg p-1 border border-white/10">
            <button
                onClick={() => setViewMode('chat')}
                title="Chat Pantalla Completa"
                className={`p-2 rounded-md transition-all duration-200 ${viewMode === 'chat'
                        ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg shadow-purple-500/30'
                        : 'text-gray-300 hover:bg-white/10 hover:text-white'
                    }`}
            >
                <MessageSquare className="w-4 h-4" />
            </button>
            <button
                onClick={() => setViewMode('split')}
                title="Vista Dividida"
                className={`p-2 rounded-md transition-all duration-200 ${viewMode === 'split'
                        ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg shadow-purple-500/30'
                        : 'text-gray-300 hover:bg-white/10 hover:text-white'
                    }`}
            >
                <Layout className="w-4 h-4" />
            </button>
            <button
                onClick={() => setViewMode('preview')}
                title="Preview Pantalla Completa"
                className={`p-2 rounded-md transition-all duration-200 ${viewMode === 'preview'
                        ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg shadow-purple-500/30'
                        : 'text-gray-300 hover:bg-white/10 hover:text-white'
                    }`}
            >
                <Eye className="w-4 h-4" />
            </button>
        </div>
    );
};

export default ViewToggleButtons;
