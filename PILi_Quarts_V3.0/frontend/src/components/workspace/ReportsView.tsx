// @ts-nocheck
import React from 'react';
import { Plus, BarChart3 } from 'lucide-react';

/**
 * ReportsView - Vista de selección para Informes
 */
const ReportsView = ({ onServiceSelect }) => {

    const servicios = [
        { id: 'informe-simple', nombre: 'Informe Técnico Standard', icon: '📝', desc: 'Resumen de actividades y hallazgos' },
        { id: 'informe-complejo', nombre: 'Análisis de Ingeniería', icon: '🔬', desc: 'Estudio profundo con cálculos y diagramas' },
        { id: 'informe-simple', nombre: 'Reporte de Conformidad', icon: '✅', desc: 'Validación de cumplimiento normativo' },
        { id: 'informe-complejo', nombre: 'Auditoría Energética', icon: '💡', desc: 'Evaluación de eficiencia y consumo' }
    ];

    return (
        <div className="p-6 h-full overflow-y-auto bg-gray-50 dark:bg-gray-950">
            <div className="mb-6">
                <h2 className="text-3xl font-bold text-gray-800 dark:text-white">Informes</h2>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    Genera reportes técnicos y profesionales basados en tus proyectos
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4 mb-8">
                {servicios.map((servicio, idx) => (
                    <button
                        key={`${servicio.id}-${idx}`}
                        onClick={() => onServiceSelect(servicio.id)}
                        className="bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-2xl p-6 hover:border-emerald-600 hover:shadow-xl transition-all text-left group flex items-start gap-4">
                        <div className="text-5xl bg-gray-50 dark:bg-gray-700 p-4 rounded-xl group-hover:bg-emerald-50 dark:group-hover:bg-emerald-900/30 transition-colors">
                            {servicio.icon}
                        </div>
                        <div className="flex-1">
                            <div className="flex items-center justify-between mb-1">
                                <h3 className="text-xl font-bold text-gray-800 dark:text-white group-hover:text-emerald-600 transition-colors">
                                    {servicio.nombre}
                                </h3>
                                <Plus className="w-5 h-5 text-gray-400 group-hover:text-emerald-600 transition-colors" />
                            </div>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                                {servicio.desc}
                            </p>
                            <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider ${servicio.id.includes('complejo')
                                    ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'
                                    : 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                                }`}>
                                {servicio.id.includes('complejo') ? 'Analítico' : 'Descriptivo'}
                            </span>
                        </div>
                    </button>
                ))}
            </div>

            <div className="bg-emerald-50 dark:bg-emerald-900/20 border-l-4 border-emerald-500 p-4 rounded-r">
                <div className="flex">
                    <div className="flex-shrink-0">
                        <BarChart3 className="h-5 w-5 text-emerald-400" />
                    </div>
                    <div className="ml-3">
                        <p className="text-sm text-emerald-700 dark:text-emerald-300">
                            Los informes técnicos permiten documentar hallazgos, resultados y recomendaciones de manera profesional.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ReportsView;
