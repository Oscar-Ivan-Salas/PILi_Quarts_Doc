/**
 * QuoteForm - Form for Quote Documents
 * Handles editing of client info and itemized supplies
 */
import { useState } from 'react';
import { Plus, Trash2, Calendar, User, ShoppingCart, DollarSign } from 'lucide-react';
import { useDocumentStore } from '../../store/useDocumentStore';
import { motion, AnimatePresence } from 'framer-motion';

export function QuoteForm() {
    const { documentData, updateData } = useDocumentStore();

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

    const addSupply = () => {
        const currentSupplies = documentData.suministros || [];
        const newSupply = {
            item: String(currentSupplies.length + 1).padStart(2, '0'),
            descripcion: '',
            cantidad: 1,
            unidad: 'und',
            precioUnitario: 0,
            precioTotal: 0
        };

        updateData({
            suministros: [...currentSupplies, newSupply]
        });
    };

    const removeSupply = (index: number) => {
        const newSupplies = [...(documentData.suministros || [])];
        newSupplies.splice(index, 1);
        // Renumber items
        const renumbered = newSupplies.map((item, idx) => ({
            ...item,
            item: String(idx + 1).padStart(2, '0')
        }));
        updateData({ suministros: renumbered });
    };

    const updateSupply = (index: number, field: string, value: any) => {
        const newSupplies = [...(documentData.suministros || [])];
        const currentItem = newSupplies[index];

        // Update field
        const updatedItem = {
            ...currentItem,
            [field]: field === 'cantidad' || field === 'precioUnitario' ? parseFloat(value) || 0 : value
        };

        // Recalculate total if needed
        if (field === 'cantidad' || field === 'precioUnitario') {
            updatedItem.precioTotal = updatedItem.cantidad * updatedItem.precioUnitario;
        }

        newSupplies[index] = updatedItem;
        updateData({ suministros: newSupplies });
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
                        <label className="text-xs font-medium text-gray-600">Cliente</label>
                        <input
                            type="text"
                            value={documentData.cliente.nombre}
                            onChange={(e) => updateClient('nombre', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                            placeholder="Nombre del cliente"
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Proyecto</label>
                        <input
                            type="text"
                            value={documentData.proyecto.nombre}
                            onChange={(e) => updateProject('nombre', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                            placeholder="Referencia del proyecto"
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
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-xs font-medium text-gray-600">Fecha</label>
                            <div className="relative">
                                <Calendar size={14} className="absolute left-3 top-3 text-gray-400" />
                                <input
                                    type="date"
                                    value={documentData.proyecto.fechaInicio}
                                    onChange={(e) => updateProject('fechaInicio', e.target.value)}
                                    className="w-full text-sm p-2 pl-9 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Suministros */}
            <div className="border-t pt-6 space-y-4">
                <div className="flex justify-between items-center">
                    <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-2">
                        <ShoppingCart size={16} /> Items ({documentData.suministros?.length || 0})
                    </h3>
                    <button
                        onClick={addSupply}
                        className="p-1 rounded-full bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors"
                        title="Agregar Item"
                    >
                        <Plus size={16} />
                    </button>
                </div>

                <div className="space-y-3">
                    <AnimatePresence>
                        {(documentData.suministros || []).map((item, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                                className="bg-gray-50 p-3 rounded-md border border-gray-100 group relative"
                            >
                                <div className="flex justify-between items-start mb-2">
                                    <span className="text-xs font-bold text-gray-400">#{item.item}</span>
                                    <button
                                        onClick={() => removeSupply(index)}
                                        className="text-gray-400 hover:text-red-500 transition-colors"
                                    >
                                        <Trash2 size={14} />
                                    </button>
                                </div>

                                <div className="grid gap-2">
                                    <input
                                        type="text"
                                        value={item.descripcion}
                                        onChange={(e) => updateSupply(index, 'descripcion', e.target.value)}
                                        className="text-sm font-medium bg-transparent border-none focus:ring-0 p-0 text-gray-800 placeholder-gray-400 w-full mb-1"
                                        placeholder="Descripción del item"
                                    />

                                    <div className="grid grid-cols-3 gap-2">
                                        <div className="space-y-1">
                                            <label className="text-[10px] text-gray-500">Cant.</label>
                                            <input
                                                type="number"
                                                value={item.cantidad}
                                                onChange={(e) => updateSupply(index, 'cantidad', e.target.value)}
                                                className="w-full text-xs bg-white border rounded p-1 text-center"
                                            />
                                        </div>
                                        <div className="space-y-1">
                                            <label className="text-[10px] text-gray-500">Unidad</label>
                                            <input
                                                type="text"
                                                value={item.unidad}
                                                onChange={(e) => updateSupply(index, 'unidad', e.target.value)}
                                                className="w-full text-xs bg-white border rounded p-1 text-center"
                                            />
                                        </div>
                                        <div className="space-y-1">
                                            <label className="text-[10px] text-gray-500">Precio</label>
                                            <input
                                                type="number"
                                                value={item.precioUnitario}
                                                onChange={(e) => updateSupply(index, 'precioUnitario', e.target.value)}
                                                className="w-full text-xs bg-white border rounded p-1 text-right"
                                            />
                                        </div>
                                    </div>

                                    <div className="mt-1 pt-2 border-t border-gray-100 flex justify-between items-center">
                                        <span className="text-xs text-gray-500">Total:</span>
                                        <span className="text-sm font-bold text-gray-800">
                                            {(item.cantidad * item.precioUnitario).toFixed(2)}
                                        </span>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {(documentData.suministros?.length === 0 || !documentData.suministros) && (
                        <div className="text-center p-4 border-2 border-dashed border-gray-200 rounded-md text-gray-400 text-xs">
                            No hay items en la cotización
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
