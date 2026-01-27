import React, { useState, useEffect } from 'react';
import { AlertTriangle, Plus, Trash2, CheckCircle, Save, ShieldAlert, Activity, ArrowRight } from 'lucide-react';

const FormularioRiesgosPro = ({ onSubmit, valoresIniciales = [] }) => {
    const [riesgos, setRiesgos] = useState(valoresIniciales.length > 0 ? valoresIniciales : [
        { descripcion: '', probabilidad: 'Media', impacto: 'Medio', mitigacion: '', severidad: 'Media' }
    ]);

    const opcionesProbabilidad = ['Alta', 'Media', 'Baja'];
    const opcionesImpacto = ['Alto', 'Medio', 'Bajo'];

    const calcularSeveridad = (prob, imp) => {
        const matriz = {
            'Alta-Alto': 'Crítica', 'Alta-Medio': 'Alta', 'Alta-Bajo': 'Media',
            'Media-Alto': 'Alta', 'Media-Medio': 'Media', 'Media-Bajo': 'Baja',
            'Baja-Alto': 'Media', 'Baja-Medio': 'Baja', 'Baja-Bajo': 'Baja'
        };
        return matriz[`${prob}-${imp}`] || 'Media';
    };

    const handleChange = (index, campo, valor) => {
        const nuevos = [...riesgos];
        nuevos[index][campo] = valor;

        // Recalcular severidad si cambia prob o impacto
        if (campo === 'probabilidad' || campo === 'impacto') {
            nuevos[index].severidad = calcularSeveridad(
                nuevos[index].probabilidad,
                nuevos[index].impacto
            );
        }

        setRiesgos(nuevos);
    };

    const agregarRiesgo = () => {
        setRiesgos([...riesgos, {
            descripcion: '',
            probabilidad: 'Media',
            impacto: 'Medio',
            mitigacion: '',
            severidad: 'Media'
        }]);
    };

    const eliminarRiesgo = (index) => {
        if (riesgos.length > 1) {
            const nuevos = riesgos.filter((_, i) => i !== index);
            setRiesgos(nuevos);
        }
    };

    const handleGuardar = () => {
        const validos = riesgos.filter(r => r.descripcion.trim().length > 3);
        if (validos.length === 0) return;
        onSubmit(validos);
    };

    const getSeveridadColor = (sev) => {
        switch (sev) {
            case 'Crítica': return 'bg-red-600 text-white shadow-red-500/50';
            case 'Alta': return 'bg-orange-600 text-white shadow-orange-500/50';
            case 'Media': return 'bg-yellow-600 text-black shadow-yellow-500/50';
            case 'Baja': return 'bg-green-600 text-white shadow-green-500/50';
            default: return 'bg-gray-600';
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6 animate-fadeIn">
            <div className="max-w-6xl mx-auto space-y-8 pb-32">

                {/* HEADER */}
                <div className="bg-gradient-to-r from-red-950 via-red-900 to-black p-6 rounded-2xl border-2 border-yellow-600 shadow-2xl flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-yellow-500 flex items-center gap-3">
                            <ShieldAlert className="w-8 h-8" />
                            Matriz de Riesgos Interactiva
                        </h1>
                        <p className="text-gray-400 mt-1">PMBOK 7th - Gestión de Incertidumbre</p>
                    </div>
                </div>

                {/* TABLA DE RIESGOS */}
                <div className="bg-black/40 backdrop-blur-md rounded-2xl border border-gray-800 shadow-xl overflow-hidden">
                    <div className="grid grid-cols-12 bg-gray-900/80 p-4 border-b border-gray-700 text-xs font-bold uppercase tracking-wider text-gray-400">
                        <div className="col-span-4">Descripción del Riesgo</div>
                        <div className="col-span-2 text-center">Probabilidad</div>
                        <div className="col-span-2 text-center">Impacto</div>
                        <div className="col-span-3">Plan de Mitigación</div>
                        <div className="col-span-1 text-center">Severidad</div>
                    </div>

                    <div className="space-y-1 p-2">
                        {riesgos.map((riesgo, idx) => (
                            <div key={idx} className="grid grid-cols-12 gap-4 items-center bg-gray-900/40 p-3 rounded-xl border border-transparent hover:border-yellow-600/30 transition-all group relative">

                                {/* 1. Descripción */}
                                <div className="col-span-4 relative">
                                    <textarea
                                        value={riesgo.descripcion}
                                        onChange={(e) => handleChange(idx, 'descripcion', e.target.value)}
                                        placeholder="Ej: Retraso en importación de equipos..."
                                        className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-sm text-white focus:border-yellow-500 outline-none resize-none h-20"
                                    />
                                </div>

                                {/* 2. Probabilidad */}
                                <div className="col-span-2 px-2">
                                    <select
                                        value={riesgo.probabilidad}
                                        onChange={(e) => handleChange(idx, 'probabilidad', e.target.value)}
                                        className="w-full bg-gray-950 border border-gray-700 rounded-lg p-2 text-xs text-center text-white focus:border-yellow-500 outline-none cursor-pointer"
                                    >
                                        {opcionesProbabilidad.map(op => <option key={op} value={op}>{op}</option>)}
                                    </select>
                                </div>

                                {/* 3. Impacto */}
                                <div className="col-span-2 px-2">
                                    <select
                                        value={riesgo.impacto}
                                        onChange={(e) => handleChange(idx, 'impacto', e.target.value)}
                                        className="w-full bg-gray-950 border border-gray-700 rounded-lg p-2 text-xs text-center text-white focus:border-yellow-500 outline-none cursor-pointer"
                                    >
                                        {opcionesImpacto.map(op => <option key={op} value={op}>{op}</option>)}
                                    </select>
                                </div>

                                {/* 4. Mitigación */}
                                <div className="col-span-3 relative">
                                    <textarea
                                        value={riesgo.mitigacion}
                                        onChange={(e) => handleChange(idx, 'mitigacion', e.target.value)}
                                        placeholder="Acción preventiva..."
                                        className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-sm text-gray-300 focus:border-green-500 outline-none resize-none h-20"
                                    />
                                    {/* Botón Eliminar flotante */}
                                    <button
                                        onClick={() => eliminarRiesgo(idx)}
                                        className="absolute -right-8 top-1/2 -translate-y-1/2 p-2 text-gray-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </div>

                                {/* 5. Severidad (Calculada) */}
                                <div className="col-span-1 flex justify-center">
                                    <div className={`px-2 py-1 rounded text-[10px] font-bold uppercase shadow-lg ${getSeveridadColor(riesgo.severidad || calcularSeveridad(riesgo.probabilidad, riesgo.impacto))}`}>
                                        {riesgo.severidad || calcularSeveridad(riesgo.probabilidad, riesgo.impacto)}
                                    </div>
                                </div>

                            </div>
                        ))}
                    </div>

                    <div className="p-4 border-t border-gray-800">
                        <button
                            onClick={agregarRiesgo}
                            className="w-full py-3 border-2 border-dashed border-gray-700 rounded-xl text-gray-400 hover:border-yellow-600 hover:text-yellow-500 hover:bg-yellow-900/10 transition-all flex items-center justify-center gap-2 text-sm font-bold uppercase tracking-wider"
                        >
                            <Plus className="w-5 h-5" /> Agregar Nuevo Riesgo
                        </button>
                    </div>
                </div>

                {/* FOOTER ACTIONS */}
                <div className="fixed bottom-0 left-0 right-0 p-4 bg-black/90 backdrop-blur-md border-t border-yellow-900/50 z-50 flex justify-end">
                    <button
                        onClick={handleGuardar}
                        className="bg-gradient-to-r from-blue-600 to-blue-500 hover:to-blue-400 text-white px-8 py-3 rounded-xl font-bold shadow-lg shadow-blue-900/50 flex items-center gap-2 transition-transform hover:scale-105"
                    >
                        <Save className="w-5 h-5" />
                        Guardar Matriz de Riesgos
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FormularioRiesgosPro;
