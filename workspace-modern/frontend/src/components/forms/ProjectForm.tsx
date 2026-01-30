/**
 * ProjectForm - Form for Simple Project Document
 * Handles editing of client info, project details, and phases
 */
import { useState, useEffect } from 'react';
import { Plus, Trash2, Calendar, MapPin, Building, User, DollarSign } from 'lucide-react';
import { useDocumentStore, type DocumentData } from '../../store/useDocumentStore';
import { motion, AnimatePresence } from 'framer-motion';

export function ProjectForm() {
    const { documentData, updateData } = useDocumentStore();
    const [activeSection, setActiveSection] = useState<string>('cliente');

    const updateClient = (field: string, value: string) => {
        updateData({
            cliente: {
                ...documentData.cliente,
                [field]: value
            }
        });
    };

    const updateProject = (field: string, value: any) => {
        updateData({
            proyecto: {
                ...documentData.proyecto,
                [field]: value
            }
        });
    };

    const addPhase = () => {
        const currentPhases = documentData.fases || [];
        const newPhase = {
            nombre: `Fase ${currentPhases.length + 1}`,
            descripcion: '',
            duracion: 7,
            presupuesto: 0,
            actividades: []
        };

        updateData({
            fases: [...currentPhases, newPhase]
        });
    };

    const removePhase = (index: number) => {
        const newPhases = [...(documentData.fases || [])];
        newPhases.splice(index, 1);
        updateData({ fases: newPhases });
    };

    const updatePhase = (index: number, field: string, value: any) => {
        const newPhases = [...(documentData.fases || [])];
        newPhases[index] = {
            ...newPhases[index],
            [field]: field === 'duracion' || field === 'presupuesto' ? parseFloat(value) || 0 : value
        };
        updateData({ fases: newPhases });
    };

    return (
        <div className="space-y-6 pb-20">
            {/* Sección Cliente */}
            <div className="space-y-4">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-2">
                    <User size={16} /> Datos del Cliente
                </h3>
                <div className="grid gap-4">
                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Nombre / Razón Social</label>
                        <input
                            type="text"
                            value={documentData.cliente.nombre}
                            onChange={(e) => updateClient('nombre', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                            placeholder="Ej. Minera Las Bambas S.A."
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                        <div className="space-y-2">
                            <label className="text-xs font-medium text-gray-600">RUC</label>
                            <input
                                type="text"
                                value={documentData.cliente.ruc}
                                onChange={(e) => updateClient('ruc', e.target.value)}
                                className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                                placeholder="20123456789"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-xs font-medium text-gray-600">Teléfono</label>
                            <input
                                type="text"
                                value={documentData.cliente.telefono}
                                onChange={(e) => updateClient('telefono', e.target.value)}
                                className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                                placeholder="999 888 777"
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Email</label>
                        <input
                            type="email"
                            value={documentData.cliente.email}
                            onChange={(e) => updateClient('email', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                            placeholder="contacto@empresa.com"
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Dirección</label>
                        <input
                            type="text"
                            value={documentData.cliente.direccion}
                            onChange={(e) => updateClient('direccion', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                            placeholder="Av. Javier Prado 123"
                        />
                    </div>
                </div>
            </div>

            <div className="border-t pt-6 space-y-4">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-2">
                    <Building size={16} /> Datos del Proyecto
                </h3>

                <div className="grid gap-4">
                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Nombre del Proyecto</label>
                        <input
                            type="text"
                            value={documentData.proyecto.nombre}
                            onChange={(e) => updateProject('nombre', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                            placeholder="Implementación de Sistema..."
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Ubicación</label>
                        <div className="relative">
                            <MapPin size={14} className="absolute left-3 top-3 text-gray-400" />
                            <input
                                type="text"
                                value={documentData.proyecto.ubicacion}
                                onChange={(e) => updateProject('ubicacion', e.target.value)}
                                className="w-full text-sm p-2 pl-9 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                                placeholder="Planta Concentradora"
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Descripción</label>
                        <textarea
                            value={documentData.proyecto.descripcion}
                            onChange={(e) => updateProject('descripcion', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none min-h-[80px]"
                            placeholder="Descripción breve del alcance..."
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                        <div className="space-y-2">
                            <label className="text-xs font-medium text-gray-600">Presupuesto</label>
                            <div className="relative">
                                <DollarSign size={14} className="absolute left-3 top-3 text-gray-400" />
                                <input
                                    type="number"
                                    value={documentData.proyecto.presupuesto}
                                    onChange={(e) => updateProject('presupuesto', e.target.value)}
                                    className="w-full text-sm p-2 pl-8 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                                />
                            </div>
                        </div>
                        <div className="space-y-2">
                            <label className="text-xs font-medium text-gray-600">Duración (días)</label>
                            <div className="relative">
                                <Calendar size={14} className="absolute left-3 top-3 text-gray-400" />
                                <input
                                    type="number"
                                    value={documentData.proyecto.duracion}
                                    onChange={(e) => updateProject('duracion', e.target.value)}
                                    className="w-full text-sm p-2 pl-9 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Fases */}
            <div className="border-t pt-6 space-y-4">
                <div className="flex justify-between items-center">
                    <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-2">
                        <Calendar size={16} /> Fases del Proyecto
                    </h3>
                    <button
                        onClick={addPhase}
                        className="p-1 rounded-full bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors"
                        title="Agregar Fase"
                    >
                        <Plus size={16} />
                    </button>
                </div>

                <div className="space-y-3">
                    <AnimatePresence>
                        {(documentData.fases || []).map((fase, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                                className="bg-gray-50 p-3 rounded-md border border-gray-100 group relative"
                            >
                                <button
                                    onClick={() => removePhase(index)}
                                    className="absolute top-2 right-2 text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                                >
                                    <Trash2 size={14} />
                                </button>

                                <div className="grid gap-2 mb-2">
                                    <input
                                        type="text"
                                        value={fase.nombre}
                                        onChange={(e) => updatePhase(index, 'nombre', e.target.value)}
                                        className="text-sm font-medium bg-transparent border-none focus:ring-0 p-0 text-gray-800 placeholder-gray-400 w-full"
                                        placeholder="Nombre de la fase"
                                    />
                                    <div className="flex gap-2">
                                        <input
                                            type="number"
                                            value={fase.duracion}
                                            onChange={(e) => updatePhase(index, 'duracion', e.target.value)}
                                            className="text-xs bg-white border rounded px-1 w-16"
                                            placeholder="Días"
                                        />
                                        <span className="text-xs text-gray-500 self-center">días</span>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {(documentData.fases?.length === 0 || !documentData.fases) && (
                        <div className="text-center p-4 border-2 border-dashed border-gray-200 rounded-md text-gray-400 text-xs">
                            No hay fases definidas
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
