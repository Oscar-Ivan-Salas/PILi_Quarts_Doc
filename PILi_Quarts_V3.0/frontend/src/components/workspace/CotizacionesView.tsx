// @ts-nocheck
import React from 'react';
import { Plus, FileText } from 'lucide-react';

/**
 * CotizacionesView - Vista de cotizaciones (Refactorizado para Workspace Agentic)
 * 
 * Se ha eliminado la dependencia de chats individuales.
 * Ahora emite el evento onServiceSelect para que el WorkArea maneje el cambio de vista.
 */
const CotizacionesView = ({ onServiceSelect }) => {

    // Lista de servicios disponibles con sus iconos
    const servicios = [
        { id: 'electricidad', nombre: 'Electricidad', icon: '⚡' },
        { id: 'itse', nombre: 'ITSE', icon: '📋' },
        { id: 'puesta-tierra', nombre: 'Puesta a Tierra', icon: '🔌' },
        { id: 'contra-incendios', nombre: 'Contra Incendios', icon: '🔥' },
        { id: 'domotica', nombre: 'Domótica', icon: '🏠' },
        { id: 'cctv', nombre: 'CCTV', icon: '📹' },
        { id: 'redes', nombre: 'Redes', icon: '🌐' },
        { id: 'automatizacion', nombre: 'Automatización', icon: '🤖' },
        { id: 'expedientes', nombre: 'Expedientes', icon: '📄' },
        { id: 'saneamiento', nombre: 'Saneamiento', icon: '🚰' }
    ];

    return (
        <div className="p-6 h-full overflow-y-auto bg-gray-50 dark:bg-gray-950">
            {/* Header */}
            <div className="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 dark:text-white">Cotizaciones</h2>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        Selecciona un servicio para crear una nueva cotización
                    </p>
                </div>
            </div>

            {/* Grid de Servicios */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
                {servicios.map(servicio => (
                    <button
                        key={servicio.id}
                        onClick={() => onServiceSelect(servicio.id)}
                        className="bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-xl p-6 hover:border-red-600 hover:shadow-xl transition-all text-left group">
                        <div className="flex items-start justify-between mb-4">
                            <div className="text-4xl">{servicio.icon}</div>
                            <Plus className="w-5 h-5 text-gray-400 group-hover:text-red-600 transition-colors" />
                        </div>
                        <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-2 group-hover:text-red-600 transition-colors">
                            {servicio.nombre}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                            Click para crear cotización
                        </p>
                    </button>
                ))}
            </div>

            {/* Nota Informativa */}
            <div className="bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500 p-4 rounded-r">
                <div className="flex">
                    <div className="flex-shrink-0">
                        <FileText className="h-5 w-5 text-blue-400" />
                    </div>
                    <div className="ml-3">
                        <p className="text-sm text-blue-700 dark:text-blue-300">
                            Al seleccionar un servicio, se abrirá el editor manual.
                            También puedes usar el Chat a la derecha para asistencia con IA.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CotizacionesView;
