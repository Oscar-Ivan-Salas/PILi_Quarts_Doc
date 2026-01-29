import React, { useState, useEffect } from 'react';
import {
    ChevronDown, ChevronUp, Calendar, Users, Package, AlertTriangle,
    FileText, CheckSquare, Building2, Mail, Phone, MapPin, Upload
} from 'lucide-react';

/**
 * FormularioProyectoUnificado - Formulario único con todas las secciones
 * 
 * Consolida las 8 pestañas en un solo formulario scrollable con acordeones
 */
const FormularioProyectoUnificado = ({
    datosProyecto,
    onUpdateDatos,
    complejidad = 7,
    onComplejidadChange
}) => {
    // Estados para acordeones (colapsables)
    const [seccionesAbiertas, setSeccionesAbiertas] = useState({
        basico: true,
        cliente: true,
        alcance: true,
        cronograma: false,
        stakeholders: false,
        entregables: false,
        recursos: false,
        suministros: false,
        riesgos: false
    });

    // Estado local para fases del Gantt
    const [fases, setFases] = useState([]);

    // Inicializar fases según complejidad
    useEffect(() => {
        const fases5 = [
            { id: 1, nombre: 'Iniciación', duracion: 5 },
            { id: 2, nombre: 'Planificación', duracion: 15 },
            { id: 3, nombre: 'Ejecución', duracion: 50 },
            { id: 4, nombre: 'Control', duracion: 15 },
            { id: 5, nombre: 'Cierre', duracion: 5 }
        ];

        const fases7 = [
            { id: 1, nombre: 'Inicio', duracion: 5 },
            { id: 2, nombre: 'Planificación Detallada', duracion: 10 },
            { id: 3, nombre: 'Gestión de Riesgos', duracion: 5 },
            { id: 4, nombre: 'Ingeniería y Diseño', duracion: 25 },
            { id: 5, nombre: 'Ejecución y Monitoreo', duracion: 45 },
            { id: 6, nombre: 'Pruebas Integrales', duracion: 10 },
            { id: 7, nombre: 'Cierre', duracion: 5 }
        ];

        setFases(complejidad === 5 ? fases5 : fases7);
    }, [complejidad]);

    const toggleSeccion = (seccion) => {
        setSeccionesAbiertas(prev => ({
            ...prev,
            [seccion]: !prev[seccion]
        }));
    };

    const handleChange = (field, value) => {
        onUpdateDatos({
            ...datosProyecto,
            [field]: value
        });
    };

    const handleClienteChange = (field, value) => {
        onUpdateDatos({
            ...datosProyecto,
            cliente: {
                ...datosProyecto.cliente,
                [field]: value
            }
        });
    };

    const handleFaseDuracionChange = (faseId, nuevaDuracion) => {
        const nuevasFases = fases.map(f =>
            f.id === faseId ? { ...f, duracion: parseInt(nuevaDuracion) || 1 } : f
        );
        setFases(nuevasFases);

        // Actualizar en datosProyecto
        const totalDias = nuevasFases.reduce((acc, f) => acc + f.duracion, 0);
        onUpdateDatos({
            ...datosProyecto,
            fases: nuevasFases,
            duracion_total: totalDias
        });
    };

    const SeccionHeader = ({ icono: Icono, titulo, seccion }) => (
        <button
            onClick={() => toggleSeccion(seccion)}
            className="w-full flex items-center justify-between p-4 bg-gray-800 hover:bg-gray-750 transition-colors rounded-lg mb-2"
        >
            <div className="flex items-center gap-3">
                <Icono className="w-5 h-5 text-yellow-400" />
                <h3 className="text-white font-semibold text-lg">{titulo}</h3>
            </div>
            {seccionesAbiertas[seccion] ? (
                <ChevronUp className="w-5 h-5 text-gray-400" />
            ) : (
                <ChevronDown className="w-5 h-5 text-gray-400" />
            )}
        </button>
    );

    const InputField = ({ label, value, onChange, type = "text", placeholder = "", required = false }) => (
        <div className="mb-4">
            <label className="block text-yellow-400 text-sm font-semibold mb-2">
                {label} {required && <span className="text-red-500">*</span>}
            </label>
            <input
                type={type}
                value={value || ''}
                onChange={(e) => onChange(e.target.value)}
                placeholder={placeholder}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-red-600 transition-colors"
            />
        </div>
    );

    const totalDias = fases.reduce((acc, f) => acc + f.duracion, 0);

    return (
        <div className="space-y-4">
            {/* 1. DATOS BÁSICOS */}
            <div>
                <SeccionHeader icono={FileText} titulo="Datos Básicos del Proyecto" seccion="basico" />
                {seccionesAbiertas.basico && (
                    <div className="p-4 bg-gray-850 rounded-lg space-y-4">
                        <InputField
                            label="Nombre del Proyecto"
                            value={datosProyecto.nombre_proyecto}
                            onChange={(v) => handleChange('nombre_proyecto', v)}
                            placeholder="Ej: Instalación Eléctrica Industrial"
                            required
                        />
                        <div className="grid grid-cols-2 gap-4">
                            <InputField
                                label="Presupuesto"
                                value={datosProyecto.presupuesto}
                                onChange={(v) => handleChange('presupuesto', v)}
                                type="number"
                                placeholder="50000"
                                required
                            />
                            <div className="mb-4">
                                <label className="block text-yellow-400 text-sm font-semibold mb-2">
                                    Moneda
                                </label>
                                <select
                                    value={datosProyecto.moneda || 'USD'}
                                    onChange={(e) => handleChange('moneda', e.target.value)}
                                    className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-red-600"
                                >
                                    <option value="USD">USD ($)</option>
                                    <option value="PEN">PEN (S/)</option>
                                    <option value="EUR">EUR (€)</option>
                                </select>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* 2. DATOS DEL CLIENTE */}
            <div>
                <SeccionHeader icono={Building2} titulo="Datos del Cliente" seccion="cliente" />
                {seccionesAbiertas.cliente && (
                    <div className="p-4 bg-gray-850 rounded-lg space-y-4">
                        <InputField
                            label="Nombre / Razón Social"
                            value={datosProyecto.cliente?.nombre}
                            onChange={(v) => handleClienteChange('nombre', v)}
                            placeholder="Empresa S.A.C."
                            required
                        />
                        <div className="grid grid-cols-2 gap-4">
                            <InputField
                                label="RUC / NIT"
                                value={datosProyecto.cliente?.ruc}
                                onChange={(v) => handleClienteChange('ruc', v)}
                                placeholder="20123456789"
                            />
                            <InputField
                                label="Teléfono"
                                value={datosProyecto.cliente?.telefono}
                                onChange={(v) => handleClienteChange('telefono', v)}
                                placeholder="+51 999 999 999"
                            />
                        </div>
                        <InputField
                            label="Email"
                            value={datosProyecto.cliente?.email}
                            onChange={(v) => handleClienteChange('email', v)}
                            type="email"
                            placeholder="contacto@empresa.com"
                        />
                        <InputField
                            label="Dirección"
                            value={datosProyecto.cliente?.direccion}
                            onChange={(v) => handleClienteChange('direccion', v)}
                            placeholder="Av. Principal 123, Lima"
                        />
                    </div>
                )}
            </div>

            {/* 3. DEFINIR ALCANCE */}
            <div>
                <SeccionHeader icono={CheckSquare} titulo="Definir Alcance del Proyecto" seccion="alcance" />
                {seccionesAbiertas.alcance && (
                    <div className="p-4 bg-gray-850 rounded-lg space-y-4">
                        <div>
                            <label className="block text-yellow-400 text-sm font-semibold mb-3">
                                Complejidad del Proyecto
                            </label>
                            <div className="grid grid-cols-2 gap-4">
                                <button
                                    onClick={() => onComplejidadChange(5)}
                                    className={`p-4 rounded-lg border-2 transition-all ${complejidad === 5
                                            ? 'bg-blue-600 border-blue-400 text-white'
                                            : 'bg-gray-800 border-gray-700 text-gray-400 hover:border-gray-600'
                                        }`}
                                >
                                    <div className="font-bold text-lg">5 Fases - Básico</div>
                                    <div className="text-sm mt-1">Proyectos estándar</div>
                                </button>
                                <button
                                    onClick={() => onComplejidadChange(7)}
                                    className={`p-4 rounded-lg border-2 transition-all ${complejidad === 7
                                            ? 'bg-indigo-600 border-indigo-400 text-white'
                                            : 'bg-gray-800 border-gray-700 text-gray-400 hover:border-gray-600'
                                        }`}
                                >
                                    <div className="font-bold text-lg">7 Fases - Avanzado</div>
                                    <div className="text-sm mt-1">Gestión integral PMI</div>
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* 4. CRONOGRAMA MAESTRO (GANTT) */}
            <div>
                <SeccionHeader icono={Calendar} titulo="Cronograma Maestro (Gantt)" seccion="cronograma" />
                {seccionesAbiertas.cronograma && (
                    <div className="p-4 bg-gray-850 rounded-lg space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <InputField
                                label="Fecha de Inicio"
                                value={datosProyecto.fecha_inicio}
                                onChange={(v) => handleChange('fecha_inicio', v)}
                                type="date"
                                required
                            />
                            <div className="mb-4">
                                <label className="block text-yellow-400 text-sm font-semibold mb-2">
                                    Duración Total
                                </label>
                                <div className="px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white font-bold">
                                    {totalDias} días
                                </div>
                            </div>
                        </div>

                        {/* Sliders de Fases */}
                        <div className="space-y-3 mt-6">
                            <h4 className="text-white font-semibold mb-3">Ajustar Duración de Fases</h4>
                            {fases.map((fase) => (
                                <div key={fase.id} className="space-y-2">
                                    <div className="flex items-center justify-between">
                                        <label className="text-gray-300 text-sm font-medium">
                                            Fase {fase.id}: {fase.nombre}
                                        </label>
                                        <span className="text-yellow-400 font-bold">{fase.duracion} días</span>
                                    </div>
                                    <input
                                        type="range"
                                        min="1"
                                        max="60"
                                        value={fase.duracion}
                                        onChange={(e) => handleFaseDuracionChange(fase.id, e.target.value)}
                                        className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider-red"
                                    />
                                    <div className="h-3 bg-gray-700 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-red-600 to-red-400 transition-all duration-300"
                                            style={{ width: `${(fase.duracion / 60) * 100}%` }}
                                        />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>

            {/* 5. STAKEHOLDERS */}
            <div>
                <SeccionHeader icono={Users} titulo="Stakeholders" seccion="stakeholders" />
                {seccionesAbiertas.stakeholders && (
                    <div className="p-4 bg-gray-850 rounded-lg">
                        <p className="text-gray-400 text-sm">
                            Lista de stakeholders (próximamente)
                        </p>
                    </div>
                )}
            </div>

            {/* 6. ENTREGABLES */}
            <div>
                <SeccionHeader icono={Package} titulo="Entregables" seccion="entregables" />
                {seccionesAbiertas.entregables && (
                    <div className="p-4 bg-gray-850 rounded-lg">
                        <p className="text-gray-400 text-sm">
                            Lista de entregables (próximamente)
                        </p>
                    </div>
                )}
            </div>

            {/* 7. RECURSOS Y RACI */}
            <div>
                <SeccionHeader icono={Users} titulo="Recursos y Matriz RACI" seccion="recursos" />
                {seccionesAbiertas.recursos && (
                    <div className="p-4 bg-gray-850 rounded-lg">
                        <p className="text-gray-400 text-sm">
                            Matriz RACI (próximamente)
                        </p>
                    </div>
                )}
            </div>

            {/* 8. SUMINISTROS */}
            <div>
                <SeccionHeader icono={Package} titulo="Suministros" seccion="suministros" />
                {seccionesAbiertas.suministros && (
                    <div className="p-4 bg-gray-850 rounded-lg">
                        <p className="text-gray-400 text-sm">
                            Lista de suministros (próximamente)
                        </p>
                    </div>
                )}
            </div>

            {/* 9. RIESGOS */}
            <div>
                <SeccionHeader icono={AlertTriangle} titulo="Gestión de Riesgos" seccion="riesgos" />
                {seccionesAbiertas.riesgos && (
                    <div className="p-4 bg-gray-850 rounded-lg">
                        <p className="text-gray-400 text-sm">
                            Matriz de riesgos (próximamente)
                        </p>
                    </div>
                )}
            </div>

            {/* Botón de Guardar */}
            <div className="sticky bottom-0 bg-gray-900 p-4 border-t border-gray-800">
                <button
                    className="w-full py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg transition-colors"
                >
                    Guardar y Continuar con PILI →
                </button>
            </div>

            <style jsx>{`
        .slider-red::-webkit-slider-thumb {
          appearance: none;
          width: 20px;
          height: 20px;
          background: #dc2626;
          cursor: pointer;
          border-radius: 50%;
          border: 2px solid #fbbf24;
        }
        .slider-red::-moz-range-thumb {
          width: 20px;
          height: 20px;
          background: #dc2626;
          cursor: pointer;
          border-radius: 50%;
          border: 2px solid #fbbf24;
        }
      `}</style>
        </div>
    );
};

export default FormularioProyectoUnificado;
