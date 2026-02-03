import React from 'react';
import { Briefcase, Calendar, DollarSign, TrendingUp } from 'lucide-react';

/**
 * ProyectoCard - Tarjeta de proyecto
 * 
 * Muestra información resumida de un proyecto
 */
const ProyectoCard = ({ proyecto, onClick }) => {
    const estadoColors = {
        'activo': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        'pendiente': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
        'completado': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
        'cancelado': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
    };

    return (
        <div
            onClick={onClick}
            className="bg-white dark:bg-gray-800 light:bg-white border-2 border-gray-200 dark:border-gray-700 light:border-gray-200 rounded-xl p-6 hover:border-red-600 hover:shadow-xl transition-all cursor-pointer group">

            {/* Header */}
            <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-red-100 dark:bg-red-900 light:bg-red-100 rounded-lg group-hover:bg-red-600 transition-all">
                    <Briefcase className="w-6 h-6 text-red-600 dark:text-red-400 light:text-red-600 group-hover:text-white" />
                </div>
                <span className={`px-3 py-1 text-xs font-bold rounded-full ${estadoColors[proyecto.estado] || estadoColors.pendiente}`}>
                    {proyecto.estado}
                </span>
            </div>

            {/* Contenido */}
            <h3 className="text-lg font-bold text-gray-800 dark:text-white light:text-gray-800 mb-2 group-hover:text-red-600 transition-colors">
                {proyecto.nombre}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 light:text-gray-600 mb-4 line-clamp-2">
                {proyecto.descripcion}
            </p>

            {/* Footer */}
            <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 light:text-gray-500">
                <div className="flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    <span>{proyecto.fecha}</span>
                </div>
                <div className="flex items-center gap-1 font-bold text-yellow-600 dark:text-yellow-400">
                    <DollarSign className="w-3 h-3" />
                    <span>{proyecto.presupuesto}</span>
                </div>
            </div>
        </div>
    );
};

export default ProyectoCard;
