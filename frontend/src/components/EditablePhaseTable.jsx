import React, { useState, useEffect } from 'react';
import { Calendar, Clock, ChevronRight, Activity } from 'lucide-react';

const EditablePhaseTable = ({ fasesIniciales, duracionTotal, fechaInicio, onFasesChange }) => {
    const [fases, setFases] = useState(fasesIniciales || []);

    useEffect(() => {
        if (fasesIniciales && fasesIniciales.length > 0) {
            setFases(fasesIniciales);
        }
    }, [fasesIniciales]);

    const handleDuracionChange = (index, nuevosDias) => {
        const nuevasFases = [...fases];
        nuevasFases[index].duracion_dias = parseInt(nuevosDias) || 1;

        // Recalcular fechas simple
        let fechaCursor = new Date(fechaInicio);
        let total = 0;

        nuevasFases.forEach(f => {
            f.fecha_inicio = fechaCursor.toLocaleDateString();
            fechaCursor.setDate(fechaCursor.getDate() + f.duracion_dias);
            f.fecha_fin = fechaCursor.toLocaleDateString();
            total += f.duracion_dias;
        });

        setFases(nuevasFases);
        if (onFasesChange) {
            onFasesChange(nuevasFases, total, fechaCursor);
        }
    };

    if (fases.length === 0) {
        return (
            <div className="text-center p-12 border-2 border-dashed border-gray-800 rounded-2xl bg-black/40 backdrop-blur-sm flex flex-col items-center justify-center group hover:border-yellow-500/50 transition-all">
                <div className="p-4 bg-gray-900 rounded-full mb-4 group-hover:scale-110 transition-transform shadow-lg shadow-yellow-900/20">
                    <Calendar className="w-8 h-8 text-gray-500 group-hover:text-yellow-400 transition-colors" />
                </div>
                <p className="text-gray-400 font-medium">No se han generado fases para el cronograma.</p>
                <p className="text-xs text-gray-600 mt-2">Configura la complejidad del proyecto para visualizar las fases.</p>
            </div>
        )
    }

    return (
        <div className="space-y-6 animate-fadeIn">
            {/* Header de Resumen */}
            <div className="flex items-center justify-between bg-gradient-to-r from-yellow-950/40 to-black/40 p-4 rounded-xl border border-yellow-900/30 backdrop-blur-md">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-yellow-500/10 rounded-lg">
                        <Activity className="w-5 h-5 text-yellow-500" />
                    </div>
                    <div>
                        <h3 className="text-sm font-bold text-gray-200">Distribución de Fases</h3>
                        <p className="text-xs text-yellow-500/80">Ajuste dinámico de tiempos</p>
                    </div>
                </div>
                <div className="flex flex-col items-end">
                    <span className="text-xs text-gray-500 font-bold uppercase tracking-wider">Duración Total</span>
                    <span className="text-xl font-bold text-white bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 to-orange-300">
                        {duracionTotal} días
                    </span>
                </div>
            </div>

            <div className="space-y-3">
                {fases.map((fase, idx) => (
                    <div key={idx} className="relative bg-black/40 backdrop-blur-sm rounded-xl p-5 border border-gray-800 hover:border-yellow-500/50 transition-all group overflow-hidden">
                        {/* Barra de progreso de fondo sutil */}
                        <div
                            className="absolute bottom-0 left-0 h-1 bg-gradient-to-r from-yellow-600 to-orange-500 opacity-20 group-hover:opacity-100 transition-opacity"
                            style={{ width: `${(fase.duracion_dias / duracionTotal) * 100}%` }}
                        />

                        <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-4 relative z-10">
                            <div className="flex items-center gap-4 w-full md:w-auto">
                                <div className="w-10 h-10 rounded-xl bg-gray-900 flex items-center justify-center text-yellow-500 font-bold border border-gray-700 shadow-inner group-hover:border-yellow-500/30 transition-colors">
                                    {idx + 1}
                                </div>
                                <div>
                                    <h4 className="font-bold text-white text-lg group-hover:text-yellow-300 transition-colors">{fase.nombre}</h4>
                                    <div className="flex items-center gap-2 text-xs text-gray-500">
                                        <Calendar className="w-3 h-3" />
                                        <span>{fase.fecha_inicio}</span>
                                        <ChevronRight className="w-3 h-3 text-gray-700" />
                                        <span>{fase.fecha_fin}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Control de Días */}
                            <div className="flex items-center gap-2 bg-gray-950/80 rounded-lg p-1.5 border border-gray-800 group-hover:border-yellow-500/30 transition-colors shadow-inner">
                                <Clock className="w-4 h-4 text-gray-500 ml-2" />
                                <input
                                    type="number"
                                    min="1"
                                    max={Math.max(60, duracionTotal)}
                                    value={fase.duracion_dias}
                                    onChange={(e) => handleDuracionChange(idx, e.target.value)}
                                    className="w-16 bg-transparent text-right font-mono font-bold text-xl text-white focus:outline-none focus:text-yellow-400 selection:bg-yellow-500/30"
                                />
                                <span className="text-gray-500 text-xs font-bold px-2 border-l border-gray-700">DÍAS</span>
                            </div>
                        </div>

                        {/* Slider Estilizado */}
                        <div className="relative h-6 flex items-center w-full px-1">
                            <input
                                type="range"
                                min="1"
                                max={Math.max(60, duracionTotal)}
                                value={fase.duracion_dias}
                                onChange={(e) => handleDuracionChange(idx, e.target.value)}
                                className="w-full h-1.5 bg-gray-800 rounded-full appearance-none cursor-pointer accent-yellow-500 hover:accent-orange-400 transition-all focus:outline-none focus:ring-2 focus:ring-yellow-500/20"
                            />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default EditablePhaseTable;
