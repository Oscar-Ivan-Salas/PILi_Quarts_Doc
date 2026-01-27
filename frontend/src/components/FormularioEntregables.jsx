import React, { useState } from 'react';
import { Package, Plus, X } from 'lucide-react';

/**
 * FormularioEntregables - Formulario interactivo con checkboxes
 * para seleccionar entregables del proyecto
 */
const FormularioEntregables = ({ onSubmit, datosIniciales = {} }) => {
    const [entregables, setEntregables] = useState({
        diseno: {
            checked: true,
            nombre: 'Diseño e ingeniería eléctrica completa',
            cantidad: 1,
            unidad: 'glb'
        },
        suministro: {
            checked: true,
            nombre: 'Suministro de materiales certificados',
            cantidad: 1,
            unidad: 'glb'
        },
        instalacion: {
            checked: true,
            nombre: 'Instalación de sistema eléctrico',
            cantidad: 1,
            unidad: 'glb'
        },
        scada: {
            checked: false,
            nombre: 'Sistema de automatización y control SCADA',
            cantidad: 1,
            unidad: 'glb'
        },
        pruebas: {
            checked: true,
            nombre: 'Pruebas FAT/SAT',
            cantidad: 1,
            unidad: 'glb'
        },
        documentacion: {
            checked: true,
            nombre: 'Documentación técnica as-built',
            cantidad: 1,
            unidad: 'glb'
        },
        capacitacion: {
            checked: true,
            nombre: 'Capacitación al personal',
            cantidad: 1,
            unidad: 'sesión'
        },
        garantia: {
            checked: false,
            nombre: 'Garantía',
            cantidad: 24,
            unidad: 'meses'
        }
    });

    const [personalizados, setPersonalizados] = useState([]);
    const [nuevoEntregable, setNuevoEntregable] = useState('');

    const handleCheckChange = (key) => {
        setEntregables(prev => ({
            ...prev,
            [key]: { ...prev[key], checked: !prev[key].checked }
        }));
    };

    const handleCantidadChange = (key, valor) => {
        setEntregables(prev => ({
            ...prev,
            [key]: { ...prev[key], cantidad: parseInt(valor) || 0 }
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

    return (
        <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-2xl p-6 border-2 border-purple-200 shadow-lg">
            {/* Header */}
            <div className="flex items-center gap-3 mb-6">
                <div className="bg-purple-600 p-3 rounded-xl">
                    <Package className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h3 className="text-xl font-bold text-gray-800">📦 Entregables del Proyecto</h3>
                    <p className="text-sm text-gray-600">Selecciona los entregables necesarios</p>
                </div>
            </div>

            {/* Lista de entregables */}
            <div className="space-y-3 mb-6">
                {Object.entries(entregables).map(([key, item]) => (
                    <div
                        key={key}
                        className={`flex items-center gap-3 p-4 rounded-xl border-2 transition-all ${item.checked
                                ? 'bg-white border-purple-400 shadow-md'
                                : 'bg-gray-50 border-gray-200'
                            }`}
                    >
                        <input
                            type="checkbox"
                            checked={item.checked}
                            onChange={() => handleCheckChange(key)}
                            className="w-5 h-5 text-purple-600 rounded focus:ring-2 focus:ring-purple-500"
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
                                    className="w-20 px-3 py-2 border-2 border-purple-300 rounded-lg text-center font-bold focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                                />
                                <span className="text-sm text-gray-600 min-w-[60px]">{item.unidad}</span>
                            </div>
                        )}
                    </div>
                ))}

                {/* Entregables personalizados */}
                {personalizados.map((item) => (
                    <div
                        key={item.id}
                        className="flex items-center gap-3 p-4 rounded-xl border-2 bg-blue-50 border-blue-400 shadow-md"
                    >
                        <input
                            type="checkbox"
                            checked={item.checked}
                            onChange={() => {
                                setPersonalizados(prev => prev.map(e =>
                                    e.id === item.id ? { ...e, checked: !e.checked } : e
                                ));
                            }}
                            className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
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
                                    setPersonalizados(prev => prev.map(ent =>
                                        ent.id === item.id ? { ...ent, cantidad: parseInt(e.target.value) || 0 } : ent
                                    ));
                                }}
                                className="w-20 px-3 py-2 border-2 border-blue-300 rounded-lg text-center font-bold focus:ring-2 focus:ring-blue-500"
                            />
                            <span className="text-sm text-gray-600 min-w-[60px]">{item.unidad}</span>
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
                        value={nuevoEntregable}
                        onChange={(e) => setNuevoEntregable(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && agregarPersonalizado()}
                        placeholder="Agregar entregable personalizado..."
                        className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                    />
                    <button
                        onClick={agregarPersonalizado}
                        disabled={!nuevoEntregable.trim()}
                        className="px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition-colors flex items-center gap-2"
                    >
                        <Plus className="w-5 h-5" />
                        Agregar
                    </button>
                </div>
            </div>

            {/* Botón continuar */}
            <button
                onClick={handleSubmit}
                className="w-full py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold text-lg rounded-xl shadow-lg transition-all transform hover:scale-105"
            >
                ✅ Continuar con estos entregables
            </button>

            {/* Resumen */}
            <div className="mt-4 p-4 bg-white rounded-lg border-2 border-purple-200">
                <p className="text-sm text-gray-600">
                    <span className="font-bold text-purple-600">
                        {Object.values(entregables).filter(e => e.checked).length + personalizados.filter(e => e.checked).length}
                    </span> entregables seleccionados
                </p>
            </div>
        </div>
    );
};

export default FormularioEntregables;
