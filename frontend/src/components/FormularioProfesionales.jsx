import React, { useState } from 'react';
import { Users, Plus, X } from 'lucide-react';

/**
 * FormularioProfesionales - Formulario interactivo con checkboxes
 * para seleccionar equipo profesional del proyecto
 */
const FormularioProfesionales = ({ onSubmit, datosIniciales = {} }) => {
    const [profesionales, setProfesionales] = useState({
        pm: {
            checked: true,
            nombre: 'Project Manager PMI',
            cantidad: 1
        },
        residente: {
            checked: true,
            nombre: 'Ing. Residente',
            cantidad: 1
        },
        electrico: {
            checked: true,
            nombre: 'Ing. Eléctrico',
            cantidad: 2
        },
        tecnicos: {
            checked: true,
            nombre: 'Técnicos Electricistas',
            cantidad: 3
        },
        qa: {
            checked: true,
            nombre: 'Inspector QA/QC',
            cantidad: 1
        },
        civil: {
            checked: false,
            nombre: 'Ing. Civil',
            cantidad: 1
        },
        sst: {
            checked: false,
            nombre: 'Supervisor SST',
            cantidad: 1
        },
        cadista: {
            checked: false,
            nombre: 'Dibujante CAD',
            cantidad: 1
        }
    });

    const [personalizados, setPersonalizados] = useState([]);
    const [nuevoRol, setNuevoRol] = useState('');

    const handleCheckChange = (key) => {
        setProfesionales(prev => ({
            ...prev,
            [key]: { ...prev[key], checked: !prev[key].checked }
        }));
    };

    const handleCantidadChange = (key, valor) => {
        setProfesionales(prev => ({
            ...prev,
            [key]: { ...prev[key], cantidad: parseInt(valor) || 0 }
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

    return (
        <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-2xl p-6 border-2 border-blue-200 shadow-lg">
            {/* Header */}
            <div className="flex items-center gap-3 mb-6">
                <div className="bg-blue-600 p-3 rounded-xl">
                    <Users className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h3 className="text-xl font-bold text-gray-800">👥 Equipo Profesional</h3>
                    <p className="text-sm text-gray-600">Selecciona los roles necesarios y sus cantidades</p>
                </div>
            </div>

            {/* Lista de profesionales */}
            <div className="space-y-3 mb-6">
                {Object.entries(profesionales).map(([key, item]) => (
                    <div
                        key={key}
                        className={`flex items-center gap-3 p-4 rounded-xl border-2 transition-all ${item.checked
                                ? 'bg-white border-blue-400 shadow-md'
                                : 'bg-gray-50 border-gray-200'
                            }`}
                    >
                        <input
                            type="checkbox"
                            checked={item.checked}
                            onChange={() => handleCheckChange(key)}
                            className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                        />
                        <span className={`flex-1 font-medium ${item.checked ? 'text-gray-800' : 'text-gray-400'}`}>
                            {item.nombre}
                        </span>
                        {item.checked && (
                            <div className="flex items-center gap-2">
                                <input
                                    type="number"
                                    min="1"
                                    max="99"
                                    value={item.cantidad}
                                    onChange={(e) => handleCantidadChange(key, e.target.value)}
                                    className="w-20 px-3 py-2 border-2 border-blue-300 rounded-lg text-center font-bold focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                />
                                <span className="text-sm text-gray-600 min-w-[60px]">personas</span>
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
                        </span>
                        <div className="flex items-center gap-2">
                            <input
                                type="number"
                                min="1"
                                max="99"
                                value={item.cantidad}
                                onChange={(e) => {
                                    setPersonalizados(prev => prev.map(p =>
                                        p.id === item.id ? { ...p, cantidad: parseInt(e.target.value) || 0 } : p
                                    ));
                                }}
                                className="w-20 px-3 py-2 border-2 border-cyan-300 rounded-lg text-center font-bold focus:ring-2 focus:ring-cyan-500"
                            />
                            <span className="text-sm text-gray-600 min-w-[60px]">personas</span>
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
                        value={nuevoRol}
                        onChange={(e) => setNuevoRol(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && agregarPersonalizado()}
                        placeholder="Agregar rol personalizado..."
                        className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                    <button
                        onClick={agregarPersonalizado}
                        disabled={!nuevoRol.trim()}
                        className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition-colors flex items-center gap-2"
                    >
                        <Plus className="w-5 h-5" />
                        Agregar
                    </button>
                </div>
            </div>

            {/* Botón continuar */}
            <button
                onClick={handleSubmit}
                className="w-full py-4 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-bold text-lg rounded-xl shadow-lg transition-all transform hover:scale-105"
            >
                ✅ Continuar con este equipo
            </button>

            {/* Resumen */}
            <div className="mt-4 p-4 bg-white rounded-lg border-2 border-blue-200">
                <p className="text-sm text-gray-600">
                    <span className="font-bold text-blue-600">{totalPersonas}</span> profesionales en{' '}
                    <span className="font-bold text-blue-600">
                        {Object.values(profesionales).filter(p => p.checked).length + personalizados.filter(p => p.checked).length}
                    </span> roles
                </p>
            </div>
        </div>
    );
};

export default FormularioProfesionales;
