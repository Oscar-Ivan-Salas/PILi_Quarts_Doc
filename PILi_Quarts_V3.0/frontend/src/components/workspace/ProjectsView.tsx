// @ts-nocheck
import React from 'react';
import { Plus, FolderOpen } from 'lucide-react';

/**
 * ProjectsView - Vista de selección para Proyectos
 */
const ProjectsView = ({ onServiceSelect }) => {

    const servicios = [
        { id: 'proyecto-simple', nombre: 'Instalaciones Eléctricas', icon: '⚡', desc: 'Planificación técnica básica' },
        { id: 'proyecto-complejo', nombre: 'Ingeniería Integral', icon: '🏗️', desc: 'Proyecto completo llave en mano' },
        { id: 'proyecto-simple', nombre: 'Mantenimiento Preventivo', icon: '🛠️', desc: 'Cronograma de servicios' },
        { id: 'proyecto-complejo', nombre: 'Sistemas de Seguridad', icon: '📹', desc: 'Diseño e implementación' }
    ];

    return (
        <div className="p-6 h-full overflow-y-auto bg-gray-50 dark:bg-gray-950">
            <div className="mb-6">
                <h2 className="text-3xl font-bold text-gray-800 dark:text-white">Proyectos</h2>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    Selecciona una modalidad para iniciar la gestión del proyecto
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4 mb-8">
                {servicios.map((servicio, idx) => (
                    <button
                        key={`${servicio.id}-${idx}`}
                        onClick={() => onServiceSelect(servicio.id)}
                        className="bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-2xl p-6 hover:border-blue-600 hover:shadow-xl transition-all text-left group flex items-start gap-4">
                        <div className="text-5xl bg-gray-50 dark:bg-gray-700 p-4 rounded-xl group-hover:bg-blue-50 dark:group-hover:bg-blue-900/30 transition-colors">
                            {servicio.icon}
                        </div>
                        <div className="flex-1">
                            <div className="flex items-center justify-between mb-1">
                                <h3 className="text-xl font-bold text-gray-800 dark:text-white group-hover:text-blue-600 transition-colors">
                                    {servicio.nombre}
                                </h3>
                                <Plus className="w-5 h-5 text-gray-400 group-hover:text-blue-600 transition-colors" />
                            </div>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                                {servicio.desc}
                            </p>
                            <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider ${servicio.id.includes('complejo')
                                    ? 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400'
                                    : 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
                                }`}>
                                {servicio.id.includes('complejo') ? 'Premium' : 'Estándar'}
                            </span>
                        </div>
                    </button>
                ))}
            </div>

            <div className="bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500 p-4 rounded-r">
                <div className="flex">
                    <div className="flex-shrink-0">
                        <FolderOpen className="h-5 w-5 text-blue-400" />
                    </div>
                    <div className="ml-3">
                        <p className="text-sm text-blue-700 dark:text-blue-300">
                            Los proyectos permiten una gestión temporal y presupuestaria más detallada que una cotización simple.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProjectsView;
