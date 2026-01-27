import React, { useState } from 'react';
import { Wrench, Plus, X } from 'lucide-react';

/**
 * FormularioSuministros - Formulario interactivo con checkboxes
 * para seleccionar suministros eléctricos del proyecto
 */
const FormularioSuministros = ({ onSubmit, datosIniciales = {} }) => {
    const [suministros, setSuministros] = useState({
        tableros: {
            checked: true,
            nombre: 'Tableros eléctricos certificados',
            cantidad: 5,
            unidad: 'und'
        },
        cables: {
            checked: true,
            nombre: 'Cables THW/THHN',
            cantidad: 500,
            unidad: 'm'
        },
        protecciones: {
            checked: true,
            nombre: 'Protecciones termomagnéticas',
            cantidad: 20,
            unidad: 'und'
        },
        puesta_tierra: {
            checked: true,
            nombre: 'Sistema de puesta a tierra',
            cantidad: 1,
            unidad: 'glb'
        },
        luminarias: {
            checked: true,
            nombre: 'Luminarias LED',
            cantidad: 50,
            unidad: 'und'
        },
        transformador: {
            checked: false,
            nombre: 'Transformador',
            cantidad: 1,
            unidad: 'und'
        },
        ups: {
            checked: false,
            nombre: 'UPS',
            cantidad: 2,
            unidad: 'und'
        },
        generador: {
            checked: false,
            nombre: 'Generador eléctrico',
            cantidad: 1,
            unidad: 'und'
        },
        conduit: {
            checked: false,
            nombre: 'Tubería conduit',
            cantidad: 200,
            unidad: 'm'
        },
        bandejas: {
            checked: false,
            nombre: 'Bandejas portacables',
            cantidad: 100,
            unidad: 'm'
        }
    });

    const [personalizados, setPersonalizados] = useState([]);
    const [nuevoSuministro, setNuevoSuministro] = useState('');

    const handleCheckChange = (key) => {
        setSuministros(prev => ({
            ...prev,
            [key]: { ...prev[key], checked: !prev[key].checked }
        }));
    };

    const handleCantidadChange = (key, valor) => {
        setSuministros(prev => ({
            ...prev,
            [key]: { ...prev[key], cantidad: parseInt(valor) || 0 }
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

    return (
        <div className="bg-gradient-to-br from-orange-50 to-yellow-50 rounded-2xl p-6 border-2 border-orange-200 shadow-lg">
            {/* Header */}
            <div className="flex items-center gap-3 mb-6">
                <div className="bg-orange-600 p-3 rounded-xl">
                    <Wrench className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h3 className="text-xl font-bold text-gray-800">🔧 Suministros Eléctricos</h3>
                    <p className="text-sm text-gray-600">Selecciona los materiales necesarios y cantidades</p>
                </div>
            </div>

            {/* Lista de suministros */}
            <div className="space-y-3 mb-6 max-h-[500px] overflow-y-auto pr-2">
                {Object.entries(suministros).map(([key, item]) => (
                    <div
                        key={key}
                        className={`flex items-center gap-3 p-4 rounded-xl border-2 transition-all ${item.checked
                                ? 'bg-white border-orange-400 shadow-md'
                                : 'bg-gray-50 border-gray-200'
                            }`}
                    >
                        <input
                            type="checkbox"
                            checked={item.checked}
                            onChange={() => handleCheckChange(key)}
                            className="w-5 h-5 text-orange-600 rounded focus:ring-2 focus:ring-orange-500"
                        />
                        <span className={`flex-1 font-medium ${item.checked ? 'text-gray-800' : 'text-gray-400'}`}>
                            {item.nombre}
                        </span>
                        {item.checked && (
                            <div className="flex items-center gap-2">
                                <input
                                    type="number"
                                    min="1"
                                    value={item.cantidad}
                                    onChange={(e) => handleCantidadChange(key, e.target.value)}
                                    className="w-24 px-3 py-2 border-2 border-orange-300 rounded-lg text-center font-bold focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                                />
                                <span className="text-sm text-gray-600 min-w-[50px]">{item.unidad}</span>
                            </div>
                        )}
                    </div>
                ))}

                {/* Suministros personalizados */}
                {personalizados.map((item) => (
                    <div
                        key={item.id}
                        className="flex items-center gap-3 p-4 rounded-xl border-2 bg-yellow-50 border-yellow-400 shadow-md"
                    >
                        <input
                            type="checkbox"
                            checked={item.checked}
                            onChange={() => {
                                setPersonalizados(prev => prev.map(s =>
                                    s.id === item.id ? { ...s, checked: !s.checked } : s
                                ));
                            }}
                            className="w-5 h-5 text-yellow-600 rounded focus:ring-2 focus:ring-yellow-500"
                        />
                        <span className="flex-1 font-medium text-gray-800">
                            {item.nombre}
                        </span>
                        <div className="flex items-center gap-2">
                            <input
                                type="number"
                                min="1"
                                value={item.cantidad}
                                onChange={(e) => {
                                    setPersonalizados(prev => prev.map(s =>
                                        s.id === item.id ? { ...s, cantidad: parseInt(e.target.value) || 0 } : s
                                    ));
                                }}
                                className="w-24 px-3 py-2 border-2 border-yellow-300 rounded-lg text-center font-bold focus:ring-2 focus:ring-yellow-500"
                            />
                            <span className="text-sm text-gray-600 min-w-[50px]">{item.unidad}</span>
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
                        type="text"
                        value={nuevoSuministro}
                        onChange={(e) => setNuevoSuministro(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && agregarPersonalizado()}
                        placeholder="Agregar suministro personalizado..."
                        className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    />
                    <button
                        onClick={agregarPersonalizado}
                        disabled={!nuevoSuministro.trim()}
                        className="px-6 py-3 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition-colors flex items-center gap-2"
                    >
                        <Plus className="w-5 h-5" />
                        Agregar
                    </button>
                </div>
            </div>

            {/* Botón continuar */}
            <button
                onClick={handleSubmit}
                className="w-full py-4 bg-gradient-to-r from-orange-600 to-yellow-600 hover:from-orange-700 hover:to-yellow-700 text-white font-bold text-lg rounded-xl shadow-lg transition-all transform hover:scale-105"
            >
                ✅ Continuar con estos suministros
            </button>

            {/* Resumen */}
            <div className="mt-4 p-4 bg-white rounded-lg border-2 border-orange-200">
                <p className="text-sm text-gray-600">
                    <span className="font-bold text-orange-600">
                        {Object.values(suministros).filter(s => s.checked).length + personalizados.filter(s => s.checked).length}
                    </span> tipos de suministros seleccionados
                </p>
            </div>
        </div>
    );
};

export default FormularioSuministros;
