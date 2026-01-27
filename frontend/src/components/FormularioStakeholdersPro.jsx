import React, { useState, useEffect } from 'react';
import { Users, Plus, Trash2, Save, UserCheck, Activity, Target, Shield } from 'lucide-react';

const FormularioStakeholdersPro = ({ onSubmit, valoresIniciales = [] }) => {
    const [stakeholders, setStakeholders] = useState([
        { id: 1, nombre: 'Cliente', rol: 'Patrocinador Principal', poder: 'Alto', interes: 'Alto' },
        { id: 2, nombre: 'Jefe de Proyecto', rol: 'Responsable de Ejecución', poder: 'Alto', interes: 'Alto' },
        { id: 3, nombre: 'Equipo Técnico', rol: 'Ejecutores', poder: 'Medio', interes: 'Alto' }
    ]);

    useEffect(() => {
        if (valoresIniciales && valoresIniciales.length > 0) {
            setStakeholders(valoresIniciales.map((s, i) => ({ ...s, id: i + 1 })));
        }
    }, [valoresIniciales]);

    const addStakeholder = () => {
        const newId = stakeholders.length > 0 ? Math.max(...stakeholders.map(s => s.id)) + 1 : 1;
        setStakeholders([...stakeholders, {
            id: newId,
            nombre: '',
            rol: '',
            poder: 'Medio',
            interes: 'Medio'
        }]);
    };

    const updateStakeholder = (id, field, value) => {
        setStakeholders(stakeholders.map(s =>
            s.id === id ? { ...s, [field]: value } : s
        ));
    };

    const removeStakeholder = (id) => {
        if (stakeholders.length > 1) {
            setStakeholders(stakeholders.filter(s => s.id !== id));
        }
    };

    const handleSubmit = () => {
        const validos = stakeholders.filter(s => s.nombre.trim() && s.rol.trim());
        if (validos.length === 0) return;
        onSubmit(validos);
    };

    const getNivelColor = (nivel) => {
        switch (nivel) {
            case 'Alto': return 'bg-red-900/60 text-red-200 border-red-500';
            case 'Medio': return 'bg-yellow-900/60 text-yellow-200 border-yellow-500';
            case 'Bajo': return 'bg-green-900/60 text-green-200 border-green-500';
            default: return 'bg-gray-800 text-gray-400';
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6 animate-fadeIn">
            <div className="max-w-5xl mx-auto space-y-8">

                {/* HEADER */}
                <div className="bg-gradient-to-r from-red-950 via-red-900 to-black p-6 rounded-2xl border-2 border-yellow-600 shadow-2xl flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-yellow-500 flex items-center gap-3">
                            <Users className="w-8 h-8" />
                            Gestión de Interesados (Stakeholders)
                        </h1>
                        <p className="text-gray-400 mt-1">Identificación y Análisis de Impacto - PMI</p>
                    </div>
                    <div className="bg-black/40 px-4 py-2 rounded-lg border border-yellow-800 text-yellow-200 text-sm font-semibold">
                        Total: {stakeholders.length} Interesados
                    </div>
                </div>

                <div className="space-y-4">
                    {stakeholders.map((stk, index) => (
                        <div key={stk.id} className="bg-black/40 backdrop-blur-md p-6 rounded-2xl border border-gray-800 hover:border-yellow-600 transition-all duration-300 shadow-xl group relative">
                            <div className="absolute top-4 right-4 text-gray-600 font-bold text-6xl opacity-10 select-none">
                                {index + 1}
                            </div>

                            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start relative z-10">

                                {/* Info Principal */}
                                <div className="lg:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <label className="text-yellow-500/80 text-xs font-bold uppercase tracking-wider flex items-center gap-1">
                                            <UserCheck className="w-3 h-3" /> Nombre / Entidad
                                        </label>
                                        <input
                                            type="text"
                                            value={stk.nombre}
                                            onChange={(e) => updateStakeholder(stk.id, 'nombre', e.target.value)}
                                            placeholder="Ej: Gerente de Planta"
                                            className="w-full bg-gray-900/80 border border-gray-700 rounded-xl px-4 py-3 text-white focus:border-yellow-500 outline-none transition-colors"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-blue-400/80 text-xs font-bold uppercase tracking-wider flex items-center gap-1">
                                            <Shield className="w-3 h-3" /> Rol en el Proyecto
                                        </label>
                                        <input
                                            type="text"
                                            value={stk.rol}
                                            onChange={(e) => updateStakeholder(stk.id, 'rol', e.target.value)}
                                            placeholder="Ej: Aprobador de Presupuesto"
                                            className="w-full bg-gray-900/80 border border-gray-700 rounded-xl px-4 py-3 text-white focus:border-blue-500 outline-none transition-colors"
                                        />
                                    </div>
                                </div>

                                {/* Matriz Poder/Interés */}
                                <div className="lg:col-span-4 flex flex-col gap-4 bg-gray-900/50 p-4 rounded-xl border border-gray-800">
                                    <div className="flex items-center justify-between">
                                        <span className="text-xs text-gray-400 font-bold flex items-center gap-2"><Activity className="w-3 h-3" /> PODER</span>
                                        <div className="flex bg-gray-950 rounded-lg p-1 gap-1">
                                            {['Alto', 'Medio', 'Bajo'].map(nivel => (
                                                <button
                                                    key={nivel}
                                                    onClick={() => updateStakeholder(stk.id, 'poder', nivel)}
                                                    className={`px-3 py-1 rounded-md text-[10px] font-bold transition-all ${stk.poder === nivel ? getNivelColor(nivel) : 'text-gray-600 hover:text-gray-300'}`}
                                                >
                                                    {nivel}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                    <div className="w-full h-px bg-gray-800"></div>
                                    <div className="flex items-center justify-between">
                                        <span className="text-xs text-gray-400 font-bold flex items-center gap-2"><Target className="w-3 h-3" /> INTERÉS</span>
                                        <div className="flex bg-gray-950 rounded-lg p-1 gap-1">
                                            {['Alto', 'Medio', 'Bajo'].map(nivel => (
                                                <button
                                                    key={nivel}
                                                    onClick={() => updateStakeholder(stk.id, 'interes', nivel)}
                                                    className={`px-3 py-1 rounded-md text-[10px] font-bold transition-all ${stk.interes === nivel ? getNivelColor(nivel) : 'text-gray-600 hover:text-gray-300'}`}
                                                >
                                                    {nivel}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                </div>

                                {/* Acciones */}
                                <div className="absolute top-0 right-0 -mt-2 -mr-2">
                                    <button
                                        onClick={() => removeStakeholder(stk.id)}
                                        disabled={stakeholders.length === 1}
                                        className="bg-gray-900 text-gray-600 hover:text-red-400 p-2 rounded-full border border-gray-700 hover:border-red-500 transition-all opacity-0 group-hover:opacity-100 disabled:opacity-0"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}

                    <button
                        onClick={addStakeholder}
                        className="w-full py-4 border-2 border-dashed border-gray-800 rounded-2xl text-gray-500 hover:border-yellow-600 hover:text-yellow-500 hover:bg-yellow-900/10 transition-all flex items-center justify-center gap-2 font-bold uppercase tracking-widest text-sm"
                    >
                        <Plus className="w-5 h-5" /> Agregar Nuevo Interesado
                    </button>
                </div>

                {/* Footer Flotante */}
                <div className="fixed bottom-0 left-0 right-0 p-4 bg-black/90 backdrop-blur-md border-t border-yellow-900/50 z-50 flex justify-end">
                    <button
                        onClick={handleSubmit}
                        disabled={stakeholders.length === 0}
                        className="bg-gradient-to-r from-yellow-600 to-yellow-500 hover:to-yellow-400 text-black px-8 py-3 rounded-xl font-bold shadow-lg shadow-yellow-900/50 flex items-center gap-2 transition-transform hover:scale-105 disabled:opacity-50 disabled:scale-100"
                    >
                        <Save className="w-5 h-5" />
                        Guardar y Continuar
                    </button>
                </div>
                <div className="h-20"></div> {/* Espaciador para footer */}
            </div>
        </div>
    );
};

export default FormularioStakeholdersPro;
