import React, { useState, useEffect, useRef } from 'react';
import { Package, Plus, X, Zap, Check, ChevronRight, Box } from 'lucide-react';

const FormularioEntregablesPro = ({
    onSubmit,
    tipoProyecto = 'residencial',
    presupuesto = 0,
    area = 0
}) => {

    const TEMPLATES = {
        residencial: {
            nombre: 'Proyecto Residencial',
            entregables: ['diseno', 'suministro', 'instalacion', 'pruebas', 'documentacion'],
            descripcion: '5 entregables estándar'
        },
        industrial: {
            nombre: 'Proyecto Industrial',
            entregables: ['diseno', 'suministro', 'instalacion', 'scada', 'pruebas', 'documentacion', 'capacitacion'],
            descripcion: '7 entregables + SCADA'
        },
        comercial: {
            nombre: 'Proyecto Comercial',
            entregables: ['diseno', 'suministro', 'instalacion', 'pruebas', 'documentacion', 'capacitacion'],
            descripcion: '6 entregables + capacitación'
        }
    };

    const templateActual = TEMPLATES[tipoProyecto] || TEMPLATES.residencial;
    const defaultsActivos = templateActual.entregables;

    const [entregables, setEntregables] = useState({
        diseno: {
            checked: defaultsActivos.includes('diseno'),
            nombre: 'Diseño e ingeniería eléctrica completa',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        suministro: {
            checked: defaultsActivos.includes('suministro'),
            nombre: 'Suministro de materiales certificados',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        instalacion: {
            checked: defaultsActivos.includes('instalacion'),
            nombre: 'Instalación de sistema eléctrico',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        scada: {
            checked: defaultsActivos.includes('scada'),
            nombre: 'Sistema de automatización y control SCADA',
            cantidad: 1,
            unidad: 'glb',
            esencial: false
        },
        pruebas: {
            checked: defaultsActivos.includes('pruebas'),
            nombre: 'Pruebas FAT/SAT',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        documentacion: {
            checked: defaultsActivos.includes('documentacion'),
            nombre: 'Documentación técnica as-built',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        capacitacion: {
            checked: defaultsActivos.includes('capacitacion'),
            nombre: 'Capacitación al personal',
            cantidad: 1,
            unidad: 'sesión',
            esencial: false
        },
        garantia: {
            checked: defaultsActivos.includes('garantia'),
            nombre: 'Garantía',
            cantidad: 24,
            unidad: 'meses',
            esencial: false
        }
    });

    const [personalizados, setPersonalizados] = useState([]);
    const [nuevoEntregable, setNuevoEntregable] = useState('');
    const inputRef = useRef(null);

    const seleccionarComunes = () => {
        setEntregables(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                if (nuevo[key].esencial) {
                    nuevo[key].checked = true;
                }
            });
            return nuevo;
        });
    };

    const deseleccionarTodos = () => {
        setEntregables(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                nuevo[key].checked = false;
            });
            return nuevo;
        });
    };

    const aplicarTemplate = (tipo) => {
        const template = TEMPLATES[tipo];
        setEntregables(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                nuevo[key].checked = template.entregables.includes(key);
            });
            return nuevo;
        });
    };

    useEffect(() => {
        const handleKeyDown = (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
                e.preventDefault();
                handleSubmit();
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [entregables, personalizados]);

    const handleCheckChange = (key) => {
        setEntregables(prev => ({
            ...prev,
            [key]: { ...prev[key], checked: !prev[key].checked }
        }));
    };

    const handleCantidadChange = (key, valor) => {
        const num = parseInt(valor) || 0;
        if (num < 0 || num > 999) return;
        setEntregables(prev => ({
            ...prev,
            [key]: { ...prev[key], cantidad: num }
        }));
    };

    const agregarPersonalizado = () => {
        if (nuevoEntregable.trim()) {
            setPersonalizados(prev => [...prev, {
                id: Date.now(),
                nombre: nuevoEntregable.trim(),
                cantidad: 1,
                unidad: 'und',
                checked: true
            }]);
            setNuevoEntregable('');
            inputRef.current?.focus();
        }
    };

    const eliminarPersonalizado = (id) => {
        setPersonalizados(prev => prev.filter(e => e.id !== id));
    };

    const handleSubmit = () => {
        const seleccionados = Object.entries(entregables)
            .filter(([key, val]) => val.checked)
            .map(([key, val]) => ({
                nombre: val.nombre,
                cantidad: val.cantidad,
                unidad: val.unidad
            }));

        const todosEntregables = [
            ...seleccionados,
            ...personalizados.filter(e => e.checked)
        ];

        onSubmit(todosEntregables);
    };

    const totalSeleccionados = Object.values(entregables).filter(e => e.checked).length +
        personalizados.filter(e => e.checked).length;

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6 animate-fadeIn">
            <div className="max-w-6xl mx-auto space-y-8 pb-32">

                {/* HEADER */}
                <div className="bg-gradient-to-r from-red-950 via-red-900 to-black p-6 rounded-2xl border-2 border-yellow-600 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-4">
                    <div>
                        <h1 className="text-3xl font-bold text-yellow-500 flex items-center gap-3">
                            <Box className="w-8 h-8" />
                            Definición del Alcance (Entregables)
                        </h1>
                        <p className="text-gray-400 mt-1">
                            Plantilla Activa: <span className="text-blue-400 font-bold uppercase">{templateActual.nombre}</span>
                        </p>
                    </div>

                    <div className="flex gap-2">
                        {Object.entries(TEMPLATES).map(([key, template]) => (
                            <button
                                key={key}
                                onClick={() => aplicarTemplate(key)}
                                className={`px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all border ${tipoProyecto === key
                                    ? 'bg-blue-600 border-blue-400 text-white shadow-lg shadow-blue-500/20'
                                    : 'bg-black/40 border-gray-700 text-gray-500 hover:border-blue-500/50 hover:text-blue-400'
                                    }`}
                            >
                                {key}
                            </button>
                        ))}
                    </div>
                </div>

                {/* ACCIONES RÁPIDAS */}
                <div className="flex flex-wrap gap-3">
                    <button
                        onClick={seleccionarComunes}
                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-green-400 font-semibold rounded-lg transition-colors flex items-center gap-2 border border-gray-700 hover:border-green-500/50"
                    >
                        <Check className="w-4 h-4" />
                        Seleccionar Esenciales
                    </button>
                    <button
                        onClick={deseleccionarTodos}
                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white font-semibold rounded-lg transition-colors border border-gray-700"
                    >
                        Deseleccionar Todos
                    </button>
                </div>

                {/* LISTA DE ENTREGABLES */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.entries(entregables).map(([key, item]) => (
                        <div
                            key={key}
                            onClick={() => handleCheckChange(key)}
                            className={`flex items-start gap-4 p-5 rounded-xl border border-transparent transition-all cursor-pointer group relative overflow-hidden ${item.checked
                                    ? 'bg-gradient-to-br from-blue-900/20 to-black border-blue-500/50 shadow-lg shadow-blue-900/10'
                                    : 'bg-gray-900/40 border-gray-800 hover:border-gray-600'
                                }`}
                        >
                            <div className={`mt-1 w-5 h-5 rounded-md border flex items-center justify-center transition-colors ${item.checked ? 'bg-blue-600 border-blue-500' : 'border-gray-600 group-hover:border-gray-400'
                                }`}>
                                {item.checked && <Check className="w-3 h-3 text-white" />}
                            </div>

                            <div className="flex-1">
                                <h4 className={`font-bold text-lg ${item.checked ? 'text-white' : 'text-gray-500'}`}>{item.nombre}</h4>
                                {item.esencial && (
                                    <span className="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-green-900/30 text-green-400 border border-green-500/20">
                                        Esencial
                                    </span>
                                )}
                            </div>

                            {item.checked && (
                                <div className="flex items-center gap-2 bg-black/40 rounded-lg p-1 border border-blue-900/30" onClick={(e) => e.stopPropagation()}>
                                    <input
                                        type="number"
                                        min="1"
                                        max="999"
                                        value={item.cantidad}
                                        onChange={(e) => handleCantidadChange(key, e.target.value)}
                                        className="w-12 bg-transparent text-center font-bold text-blue-300 focus:outline-none"
                                    />
                                    <span className="text-xs text-gray-500 font-mono pr-2">{item.unidad}</span>
                                </div>
                            )}
                        </div>
                    ))}

                    {/* PERSONALIZADOS */}
                    {personalizados.map((item) => (
                        <div key={item.id} className="flex items-start gap-4 p-5 rounded-xl border border-yellow-500/30 bg-yellow-900/10 transition-all cursor-pointer relative overflow-hidden">
                            <div
                                onClick={() => setPersonalizados(prev => prev.map(e => e.id === item.id ? { ...e, checked: !e.checked } : e))}
                                className={`mt-1 w-5 h-5 rounded-md border flex items-center justify-center transition-colors ${item.checked ? 'bg-yellow-600 border-yellow-500' : 'border-yellow-700 bg-transparent'
                                    }`}
                            >
                                {item.checked && <Check className="w-3 h-3 text-black" />}
                            </div>

                            <div className="flex-1">
                                <h4 className="font-bold text-lg text-yellow-100">{item.nombre}</h4>
                                <span className="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-yellow-900/30 text-yellow-400 border border-yellow-500/20">
                                    Personalizado
                                </span>
                            </div>

                            <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                                <input
                                    type="number"
                                    min="1"
                                    value={item.cantidad}
                                    onChange={(e) => {
                                        const num = parseInt(e.target.value) || 0;
                                        setPersonalizados(prev => prev.map(ent => ent.id === item.id ? { ...ent, cantidad: num } : ent));
                                    }}
                                    className="w-12 bg-black/40 rounded border border-yellow-600/30 text-center font-bold text-yellow-300 focus:outline-none p-1"
                                />
                                <button
                                    onClick={() => eliminarPersonalizado(item.id)}
                                    className="p-1 hover:bg-red-500/20 rounded text-gray-500 hover:text-red-400 transition-colors"
                                >
                                    <X className="w-4 h-4" />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

                {/* INPUT AGREGAR */}
                <div className="relative group">
                    <input
                        ref={inputRef}
                        type="text"
                        value={nuevoEntregable}
                        onChange={(e) => setNuevoEntregable(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && agregarPersonalizado()}
                        placeholder="Escribe un entregable nuevo..."
                        className="w-full bg-black/40 border-2 border-gray-800 rounded-2xl py-4 pl-6 pr-32 text-white focus:border-yellow-500 outline-none transition-all placeholder-gray-600 text-lg"
                    />
                    <button
                        onClick={agregarPersonalizado}
                        disabled={!nuevoEntregable.trim()}
                        className="absolute right-2 top-2 bottom-2 px-6 bg-yellow-600 hover:bg-yellow-500 text-black font-bold rounded-xl disabled:opacity-0 disabled:scale-95 transition-all flex items-center gap-2"
                    >
                        <Plus className="w-5 h-5" /> Agregar
                    </button>
                </div>

                {/* FOOTER ACTIONS */}
                <div className="fixed bottom-0 left-0 right-0 p-4 bg-black/90 backdrop-blur-md border-t border-yellow-900/50 z-50 flex justify-end">
                    <button
                        onClick={handleSubmit}
                        disabled={totalSeleccionados === 0}
                        className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:to-cyan-500 text-white px-8 py-3 rounded-xl font-bold shadow-lg shadow-blue-900/50 flex items-center gap-2 transition-transform hover:scale-105 disabled:opacity-50 disabled:scale-100"
                    >
                        <Zap className="w-5 h-5" />
                        Confirmar Alcance
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FormularioEntregablesPro;
