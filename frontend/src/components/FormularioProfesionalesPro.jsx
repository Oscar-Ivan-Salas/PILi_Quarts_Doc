import React, { useState, useEffect, useRef } from 'react';
import { Users, Plus, X, Zap, Check } from 'lucide-react';

/**
 * FormularioProfesionalesPro - Formulario PROFESIONAL para equipo humano
 * ✨ Features: Smart defaults + Keyboard shortcuts + Cantidades sugeridas
 */
const FormularioProfesionalesPro = ({
    onSubmit,
    tipoProyecto = 'residencial',
    presupuesto = 0,
    area = 0
}) => {

    // 🎯 TEMPLATES: Cantidades sugeridas por tipo de proyecto
    const TEMPLATES = {
        residencial: {
            nombre: 'Equipo Residencial',
            profesionales: {
                pm: 1, residente: 1, electrico: 1, tecnicos: 2, qa: 0,
                civil: 0, sst: 0, cadista: 0
            },
            descripcion: '5 profesionales básicos'
        },
        industrial: {
            nombre: 'Equipo Industrial',
            profesionales: {
                pm: 1, residente: 1, electrico: 2, tecnicos: 4, qa: 1,
                civil: 0, sst: 1, cadista: 1
            },
            descripcion: '11 profesionales + SST'
        },
        comercial: {
            nombre: 'Equipo Comercial',
            profesionales: {
                pm: 1, residente: 1, electrico: 2, tecnicos: 3, qa: 1,
                civil: 0, sst: 0, cadista: 1
            },
            descripcion: '9 profesionales'
        }
    };

    const templateActual = TEMPLATES[tipoProyecto] || TEMPLATES.residencial;
    const cantidadesDefault = templateActual.profesionales;

    const [profesionales, setProfesionales] = useState({
        pm: {
            checked: cantidadesDefault.pm > 0,
            nombre: 'Project Manager PMI',
            cantidad: cantidadesDefault.pm || 1,
            esencial: true
        },
        residente: {
            checked: cantidadesDefault.residente > 0,
            nombre: 'Ing. Residente',
            cantidad: cantidadesDefault.residente || 1,
            esencial: true
        },
        electrico: {
            checked: cantidadesDefault.electrico > 0,
            nombre: 'Ing. Eléctrico',
            cantidad: cantidadesDefault.electrico || 1,
            esencial: true
        },
        tecnicos: {
            checked: cantidadesDefault.tecnicos > 0,
            nombre: 'Técnicos Electricistas',
            cantidad: cantidadesDefault.tecnicos || 2,
            esencial: true
        },
        qa: {
            checked: cantidadesDefault.qa > 0,
            nombre: 'Inspector QA/QC',
            cantidad: cantidadesDefault.qa || 1,
            esencial: false
        },
        civil: {
            checked: cantidadesDefault.civil > 0,
            nombre: 'Ing. Civil',
            cantidad: cantidadesDefault.civil || 1,
            esencial: false
        },
        sst: {
            checked: cantidadesDefault.sst > 0,
            nombre: 'Supervisor SST',
            cantidad: cantidadesDefault.sst || 1,
            esencial: false
        },
        cadista: {
            checked: cantidadesDefault.cadista > 0,
            nombre: 'Dibujante CAD',
            cantidad: cantidadesDefault.cadista || 1,
            esencial: false
        }
    });

    const [personalizados, setPersonalizados] = useState([]);
    const [nuevoRol, setNuevoRol] = useState('');
    const inputRef = useRef(null);

    // 🎯 BOTÓN: Seleccionar esenciales
    const seleccionarEsenciales = () => {
        setProfesionales(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                if (nuevo[key].esencial) {
                    nuevo[key].checked = true;
                }
            });
            return nuevo;
        });
    };

    // 🎯 BOTÓN: Deseleccionar todos
    const deseleccionarTodos = () => {
        setProfesionales(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                nuevo[key].checked = false;
            });
            return nuevo;
        });
    };

    // 🎯 BOTÓN: Aplicar template
    const aplicarTemplate = (tipo) => {
        const template = TEMPLATES[tipo];
        setProfesionales(prev => {
            const nuevo = { ...prev };
            Object.keys(nuevo).forEach(key => {
                const cantidad = template.profesionales[key] || 0;
                nuevo[key].checked = cantidad > 0;
                nuevo[key].cantidad = cantidad || nuevo[key].cantidad;
            });
            return nuevo;
        });
    };

    // ⌨️ KEYBOARD SHORTCUTS
    useEffect(() => {
        const handleKeyDown = (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
                e.preventDefault();
                handleSubmit();
            }
            if ((e.metaKey || e.ctrlKey) && e.key === 'a') {
                e.preventDefault();
                seleccionarEsenciales();
            }
            if ((e.metaKey || e.ctrlKey) && e.key === 'd') {
                e.preventDefault();
                deseleccionarTodos();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [profesionales, personalizados]);

    const handleCheckChange = (key) => {
        setProfesionales(prev => ({
            ...prev,
            [key]: { ...prev[key], checked: !prev[key].checked }
        }));
    };

    const handleCantidadChange = (key, valor) => {
        const num = parseInt(valor) || 0;
        if (num < 0 || num > 99) return;

        setProfesionales(prev => ({
            ...prev,
            [key]: { ...prev[key], cantidad: num }
        }));
    };

    const agregarPersonalizado = () => {
        if (nuevoRol.trim()) {
            setPersonalizados(prev => [...prev, {
                id: Date.now(),
                nombre: nuevoRol.trim(),
                cantidad: 1,
                checked: true
            }]);
            setNuevoRol('');
            inputRef.current?.focus();
        }
    };

    const eliminarPersonalizado = (id) => {
        setPersonalizados(prev => prev.filter(p => p.id !== id));
    };

    const handleSubmit = () => {
        const seleccionados = Object.entries(profesionales)
            .filter(([key, val]) => val.checked)
            .map(([key, val]) => ({
                rol: val.nombre,
                cantidad: val.cantidad
            }));

        const todosProfesionales = [
            ...seleccionados,
            ...personalizados.filter(p => p.checked).map(p => ({
                rol: p.nombre,
                cantidad: p.cantidad
            }))
        ];

        onSubmit(todosProfesionales);
    };

    const totalPersonas = Object.values(profesionales)
        .filter(p => p.checked)
        .reduce((sum, p) => sum + p.cantidad, 0) +
        personalizados
            .filter(p => p.checked)
            .reduce((sum, p) => sum + p.cantidad, 0);

    const totalRoles = Object.values(profesionales).filter(p => p.checked).length +
        personalizados.filter(p => p.checked).length;

    return (
        <div className="bg-gradient-to-br from-purple-900/95 via-blue-900/95 to-slate-900/95 rounded-2xl p-6 border-2 border-purple-400/50 shadow-2xl backdrop-blur-sm">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className="bg-purple-600 p-3 rounded-xl">
                        <Users className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h3 className="text-xl font-bold text-white">👥 Equipo Profesional</h3>
                        <p className="text-sm text-purple-200">
                            Template: <span className="font-semibold text-cyan-300">{templateActual.nombre}</span>
                            {' '}• {templateActual.descripcion}
                        </p>
                    </div>
                </div>
            </div>

            {/* Botones Rápidos */}
            <div className="flex flex-wrap gap-2 mb-6">
                <button
                    onClick={seleccionarEsenciales}
                    className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors flex items-center gap-2 shadow-lg"
                >
                    <Check className="w-4 h-4" />
                    ✓ Seleccionar Esenciales
                    <span className="text-xs opacity-75">(Cmd+A)</span>
                </button>
                <button
                    onClick={deseleccionarTodos}
                    className="px-4 py-2 bg-slate-700 hover:bg-slate-800 text-white font-semibold rounded-lg transition-colors shadow-lg"
                >
                    Deseleccionar Todos
                    <span className="text-xs opacity-75 ml-2">(Cmd+D)</span>
                </button>

                {/* Templates */}
                <div className="flex gap-2 ml-auto">
                    {Object.entries(TEMPLATES).map(([key, template]) => (
                        <button
                            key={key}
                            onClick={() => aplicarTemplate(key)}
                            className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors shadow-md ${tipoProyecto === key
                                ? 'bg-purple-600 text-white'
                                : 'bg-white/10 text-white hover:bg-white/20 backdrop-blur-sm'
                                }`}
                        >
                            {template.nombre}
                        </button>
                    ))}
                </div>
            </div>

            {/* Lista de profesionales */}
            <div className="space-y-3 mb-6">
                {Object.entries(profesionales).map(([key, item]) => (
                    <div
                        key={key}
                        className={`flex items-center gap-3 p-4 rounded-xl border-2 transition-all cursor-pointer ${item.checked
                            ? 'bg-white border-purple-400 shadow-lg'
                            : 'bg-gray-50 border-gray-300 hover:border-gray-400'
                            }`}
                        onClick={() => handleCheckChange(key)}
                    >
                        <input
                            type="checkbox"
                            checked={item.checked}
                            onChange={() => { }}
                            className="w-5 h-5 text-purple-600 rounded focus:ring-2 focus:ring-purple-500 pointer-events-none"
                        />
                        <div className="flex-1">
                            <span className={`font-medium ${item.checked ? 'text-gray-900' : 'text-gray-600'}`}>
                                {item.nombre}
                            </span>
                            {item.esencial && (
                                <span className="ml-2 text-xs bg-green-600 text-white px-2 py-1 rounded shadow-md">
                                    Esencial
                                </span>
                            )}
                        </div>
                        {item.checked && (
                            <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                                <input
                                    type="number"
                                    min="1"
                                    max="99"
                                    value={item.cantidad}
                                    onChange={(e) => handleCantidadChange(key, e.target.value)}
                                    className="w-20 px-3 py-2 border-2 border-purple-400 bg-white rounded-lg text-center font-bold text-gray-900 focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                                />
                                <span className="text-sm text-gray-700 min-w-[70px]">personas</span>
                            </div>
                        )}
                    </div>
                ))}

                {/* Profesionales personalizados */}
                {personalizados.map((item) => (
                    <div
                        key={item.id}
                        className="flex items-center gap-3 p-4 rounded-xl border-2 bg-cyan-50 border-cyan-400 shadow-md"
                    >
                        <input
                            type="checkbox"
                            checked={item.checked}
                            onChange={() => {
                                setPersonalizados(prev => prev.map(p =>
                                    p.id === item.id ? { ...p, checked: !p.checked } : p
                                ));
                            }}
                            className="w-5 h-5 text-cyan-600 rounded focus:ring-2 focus:ring-cyan-500"
                        />
                        <span className="flex-1 font-medium text-gray-800">
                            {item.nombre}
                            <span className="ml-2 text-xs bg-cyan-200 text-cyan-700 px-2 py-1 rounded">
                                Personalizado
                            </span>
                        </span>
                        <div className="flex items-center gap-2">
                            <input
                                type="number"
                                min="1"
                                max="99"
                                value={item.cantidad}
                                onChange={(e) => {
                                    const num = parseInt(e.target.value) || 0;
                                    if (num >= 0 && num <= 99) {
                                        setPersonalizados(prev => prev.map(p =>
                                            p.id === item.id ? { ...p, cantidad: num } : p
                                        ));
                                    }
                                }}
                                className="w-20 px-3 py-2 border-2 border-cyan-300 rounded-lg text-center font-bold focus:ring-2 focus:ring-cyan-500"
                            />
                            <span className="text-sm text-gray-600 min-w-[70px]">personas</span>
                            <button
                                onClick={() => eliminarPersonalizado(item.id)}
                                className="p-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {/* Agregar personalizado */}
            <div className="mb-6">
                <div className="flex gap-2">
                    <input
                        ref={inputRef}
                        type="text"
                        value={nuevoRol}
                        onChange={(e) => setNuevoRol(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && agregarPersonalizado()}
                        placeholder="Agregar rol personalizado... (Enter para agregar)"
                        className="flex-1 px-4 py-3 border-2 border-purple-400/50 bg-white/10 text-white placeholder-purple-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 backdrop-blur-sm"
                    />
                    <button
                        onClick={agregarPersonalizado}
                        disabled={!nuevoRol.trim()}
                        className="px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white font-bold rounded-lg transition-colors flex items-center gap-2 shadow-lg"
                    >
                        <Plus className="w-5 h-5" />
                        Agregar
                    </button>
                </div>
            </div>

            {/* Botón continuar */}
            <button
                onClick={handleSubmit}
                disabled={totalRoles === 0}
                className="w-full py-4 bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold text-lg rounded-xl shadow-2xl transition-all transform hover:scale-105 disabled:scale-100 flex items-center justify-center gap-2"
            >
                <Zap className="w-5 h-5" />
                ✅ Continuar con este equipo
                <span className="text-sm opacity-75">(Cmd+Enter)</span>
            </button>

            {/* Resumen */}
            <div className="mt-4 space-y-2">
                <div className="p-4 bg-white/10 rounded-lg border-2 border-purple-400/50 backdrop-blur-sm">
                    <p className="text-sm text-purple-100">
                        <span className="font-bold text-cyan-300 text-lg">{totalPersonas}</span> profesionales en{' '}
                        <span className="font-bold text-cyan-300 text-lg">{totalRoles}</span> roles
                    </p>
                </div>

                <div className="p-3 bg-purple-800/50 rounded-lg border border-purple-400/30 backdrop-blur-sm">
                    <p className="text-xs text-purple-200 font-mono">
                        💡 <span className="font-semibold">Shortcuts:</span>
                        {' '}Cmd+A (Esenciales) • Cmd+D (Deseleccionar) • Cmd+Enter (Continuar)
                    </p>
                </div>
            </div>
        </div>
    );
};

export default FormularioProfesionalesPro;
