import React, { useState, useEffect, useRef } from 'react';
import { Wrench, Plus, X, Zap, Check, Calculator, Box, TrendingUp } from 'lucide-react';

const FormularioSuministrosPro = ({
    onSubmit,
    tipoProyecto = 'residencial',
    presupuesto = 0,
    area = 0
}) => {

    const calcularCantidad = (item, areaM2) => {
        if (!areaM2 || areaM2 <= 0) return 0;

        const calculos = {
            tableros: Math.ceil(areaM2 / 200),
            cables: Math.ceil(areaM2 * 2.5),
            protecciones: Math.ceil(areaM2 / 50),
            puesta_tierra: 1,
            luminarias: Math.ceil(areaM2 / 10),
            transformador: Math.ceil(areaM2 / 1000),
            ups: Math.ceil(areaM2 / 500),
            generador: Math.ceil(areaM2 / 2000),
            conduit: Math.ceil(areaM2 * 1.5),
            bandejas: Math.ceil(areaM2 * 0.8)
        };

        return calculos[item] || 1;
    };

    const TEMPLATES = {
        residencial: {
            nombre: 'Suministros Residencial',
            suministros: ['tableros', 'cables', 'protecciones', 'puesta_tierra', 'luminarias'],
            descripcion: '5 suministros básicos'
        },
        industrial: {
            nombre: 'Suministros Industrial',
            suministros: ['tableros', 'cables', 'protecciones', 'puesta_tierra', 'luminarias', 'transformador', 'ups', 'generador', 'conduit', 'bandejas'],
            descripcion: '10 suministros completos'
        },
        comercial: {
            nombre: 'Suministros Comercial',
            suministros: ['tableros', 'cables', 'protecciones', 'puesta_tierra', 'luminarias', 'ups', 'conduit', 'bandejas'],
            descripcion: '8 suministros + UPS'
        }
    };

    const templateActual = TEMPLATES[tipoProyecto] || TEMPLATES.residencial;
    const suministrosDefault = templateActual.suministros;

    const [suministros, setSuministros] = useState({
        tableros: {
            checked: suministrosDefault.includes('tableros'),
            nombre: 'Tableros eléctricos certificados',
            cantidad: area > 0 ? calcularCantidad('tableros', area) : 5,
            unidad: 'und',
            esencial: true
        },
        cables: {
            checked: suministrosDefault.includes('cables'),
            nombre: 'Cables THW/THHN',
            cantidad: area > 0 ? calcularCantidad('cables', area) : 500,
            unidad: 'm',
            esencial: true
        },
        protecciones: {
            checked: suministrosDefault.includes('protecciones'),
            nombre: 'Protecciones termomagnéticas',
            cantidad: area > 0 ? calcularCantidad('protecciones', area) : 20,
            unidad: 'und',
            esencial: true
        },
        puesta_tierra: {
            checked: suministrosDefault.includes('puesta_tierra'),
            nombre: 'Sistema de puesta a tierra',
            cantidad: 1,
            unidad: 'glb',
            esencial: true
        },
        luminarias: {
            checked: suministrosDefault.includes('luminarias'),
            nombre: 'Luminarias LED',
            cantidad: area > 0 ? calcularCantidad('luminarias', area) : 50,
            unidad: 'und',
            esencial: true
        },
        transformador: {
            checked: suministrosDefault.includes('transformador'),
            nombre: 'Transformador',
            cantidad: area > 0 ? calcularCantidad('transformador', area) : 1,
            unidad: 'und',
            esencial: false
        },
        ups: {
            checked: suministrosDefault.includes('ups'),
            nombre: 'UPS',
            cantidad: area > 0 ? calcularCantidad('ups', area) : 2,
            unidad: 'und',
            esencial: false
        },
        generador: {
            checked: suministrosDefault.includes('generador'),
            nombre: 'Generador eléctrico',
            cantidad: area > 0 ? calcularCantidad('generador', area) : 1,
            unidad: 'und',
            esencial: false
        },
        conduit: {
            checked: suministrosDefault.includes('conduit'),
            nombre: 'Tubería conduit',
            cantidad: area > 0 ? calcularCantidad('conduit', area) : 200,
            unidad: 'm',
            esencial: false
        },
        bandejas: {
            checked: suministrosDefault.includes('bandejas'),
            nombre: 'Bandejas portacables',
            cantidad: area > 0 ? calcularCantidad('bandejas', area) : 100,
            unidad: 'm',
            esencial: false
        }
    });

    const [personalizados, setPersonalizados] = useState([]);
    const [nuevoSuministro, setNuevoSuministro] = useState('');
    const inputRef = useRef(null);

    const seleccionarEsenciales = () => {
        setSuministros(prev => {
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
        setSuministros(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                nuevo[key].checked = false;
            });
            return nuevo;
        });
    };

    const recalcularCantidades = () => {
        if (area <= 0) return;
        setSuministros(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                const cantidadCalculada = calcularCantidad(key, area);
                if (cantidadCalculada > 0) {
                    nuevo[key].cantidad = cantidadCalculada;
                }
            });
            return nuevo;
        });
    };

    const aplicarTemplate = (tipo) => {
        const template = TEMPLATES[tipo];
        setSuministros(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                nuevo[key].checked = template.suministros.includes(key);
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
    }, [suministros, personalizados, area]);

    const handleCheckChange = (key) => {
        setSuministros(prev => ({
            ...prev,
            [key]: { ...prev[key], checked: !prev[key].checked }
        }));
    };

    const handleCantidadChange = (key, valor) => {
        const num = parseInt(valor) || 0;
        if (num < 0 || num > 9999) return;
        setSuministros(prev => ({
            ...prev,
            [key]: { ...prev[key], cantidad: num }
        }));
    };

    const agregarPersonalizado = () => {
        if (nuevoSuministro.trim()) {
            setPersonalizados(prev => [...prev, {
                id: Date.now(),
                nombre: nuevoSuministro.trim(),
                cantidad: 1,
                unidad: 'und',
                checked: true
            }]);
            setNuevoSuministro('');
            inputRef.current?.focus();
        }
    };

    const eliminarPersonalizado = (id) => {
        setPersonalizados(prev => prev.filter(s => s.id !== id));
    };

    const handleSubmit = () => {
        const seleccionados = Object.entries(suministros)
            .filter(([key, val]) => val.checked)
            .map(([key, val]) => ({
                nombre: val.nombre,
                cantidad: val.cantidad,
                unidad: val.unidad
            }));

        const todosSuministros = [
            ...seleccionados,
            ...personalizados.filter(s => s.checked)
        ];

        onSubmit(todosSuministros);
    };

    const totalSeleccionados = Object.values(suministros).filter(s => s.checked).length +
        personalizados.filter(s => s.checked).length;

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-950 via-orange-950 to-black text-white p-6 animate-fadeIn">
            <div className="max-w-6xl mx-auto space-y-8 pb-32">

                {/* HEADER */}
                <div className="bg-gradient-to-r from-orange-950 via-red-900 to-black p-6 rounded-2xl border-2 border-orange-600 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-4">
                    <div>
                        <h1 className="text-3xl font-bold text-orange-500 flex items-center gap-3">
                            <Wrench className="w-8 h-8" />
                            Costos y Suministros
                        </h1>
                        <p className="text-gray-400 mt-1">
                            Plantilla Activa: <span className="text-orange-400 font-bold uppercase">{templateActual.nombre}</span>
                            {area > 0 && <span className="ml-2 text-blue-400 bg-blue-900/40 px-2 py-0.5 rounded text-xs border border-blue-500/30">ÁREA: {area}m² (Auto-cálculo)</span>}
                        </p>
                    </div>

                    <div className="flex gap-2">
                        {Object.entries(TEMPLATES).map(([key, template]) => (
                            <button
                                key={key}
                                onClick={() => aplicarTemplate(key)}
                                className={`px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all border ${tipoProyecto === key
                                    ? 'bg-orange-600 border-orange-400 text-white shadow-lg shadow-orange-500/20'
                                    : 'bg-black/40 border-gray-700 text-gray-500 hover:border-orange-500/50 hover:text-orange-400'
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
                        onClick={seleccionarEsenciales}
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
                    {area > 0 && (
                        <button
                            onClick={recalcularCantidades}
                            className="px-4 py-2 bg-blue-900/50 hover:bg-blue-800 text-blue-300 font-semibold rounded-lg transition-colors flex items-center gap-2 border border-blue-700 hover:border-blue-500"
                        >
                            <Calculator className="w-4 h-4" />
                            Recalcular por Área
                        </button>
                    )}
                </div>

                {/* LISTA DE SUMINISTROS */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.entries(suministros).map(([key, item]) => (
                        <div
                            key={key}
                            onClick={() => handleCheckChange(key)}
                            className={`flex items-start gap-4 p-5 rounded-xl border border-transparent transition-all cursor-pointer group relative overflow-hidden ${item.checked
                                    ? 'bg-gradient-to-br from-orange-900/20 to-black border-orange-500/50 shadow-lg shadow-orange-900/10'
                                    : 'bg-gray-900/40 border-gray-800 hover:border-gray-600'
                                }`}
                        >
                            <div className={`mt-1 w-5 h-5 rounded-md border flex items-center justify-center transition-colors ${item.checked ? 'bg-orange-600 border-orange-500' : 'border-gray-600 group-hover:border-gray-400'
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
                                <div className="flex items-center gap-2 bg-black/40 rounded-lg p-1 border border-orange-900/30" onClick={(e) => e.stopPropagation()}>
                                    <input
                                        type="number"
                                        min="1"
                                        max="9999"
                                        value={item.cantidad}
                                        onChange={(e) => handleCantidadChange(key, e.target.value)}
                                        className="w-16 bg-transparent text-center font-bold text-orange-300 focus:outline-none"
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
                                        setPersonalizados(prev => prev.map(s => s.id === item.id ? { ...s, cantidad: num } : s));
                                    }}
                                    className="w-16 bg-black/40 rounded border border-yellow-600/30 text-center font-bold text-yellow-300 focus:outline-none p-1"
                                />
                                <span className="text-xs text-gray-500 font-mono pr-1">{item.unidad}</span>
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
                        value={nuevoSuministro}
                        onChange={(e) => setNuevoSuministro(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && agregarPersonalizado()}
                        placeholder="Escribe un suministro nuevo..."
                        className="w-full bg-black/40 border-2 border-gray-800 rounded-2xl py-4 pl-6 pr-32 text-white focus:border-orange-500 outline-none transition-all placeholder-gray-600 text-lg"
                    />
                    <button
                        onClick={agregarPersonalizado}
                        disabled={!nuevoSuministro.trim()}
                        className="absolute right-2 top-2 bottom-2 px-6 bg-orange-600 hover:bg-orange-500 text-black font-bold rounded-xl disabled:opacity-0 disabled:scale-95 transition-all flex items-center gap-2"
                    >
                        <Plus className="w-5 h-5" /> Agregar
                    </button>
                </div>

                {/* FOOTER ACTIONS */}
                <div className="fixed bottom-0 left-0 right-0 p-4 bg-black/90 backdrop-blur-md border-t border-orange-900/50 z-50 flex justify-end">
                    <button
                        onClick={handleSubmit}
                        disabled={totalSeleccionados === 0}
                        className="bg-gradient-to-r from-orange-600 to-red-600 hover:to-red-500 text-white px-8 py-3 rounded-xl font-bold shadow-lg shadow-orange-900/50 flex items-center gap-2 transition-transform hover:scale-105 disabled:opacity-50 disabled:scale-100"
                    >
                        <Zap className="w-5 h-5" />
                        Confirmar Costos
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FormularioSuministrosPro;
