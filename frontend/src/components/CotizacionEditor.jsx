import React, { useState } from 'react';
import { Edit2, Save, X, Plus, Trash2, Calculator } from 'lucide-react';

const CotizacionEditor = ({ cotizacionInicial, onGuardar }) => {
  const [cotizacion, setCotizacion] = useState(cotizacionInicial || {
    cliente: '',
    proyecto: '',
    items: [],
    subtotal: 0,
    igv: 0,
    total: 0
  });

  const [editandoItem, setEditandoItem] = useState(null);

  const agregarItem = () => {
    const nuevoItem = {
      id: Date.now(),
      descripcion: 'Nuevo servicio',
      cantidad: 1,
      precioUnitario: 0,
      total: 0
    };

    setCotizacion(prev => ({
      ...prev,
      items: [...prev.items, nuevoItem]
    }));

    setEditandoItem(nuevoItem.id);
  };

  const actualizarItem = (id, campo, valor) => {
    setCotizacion(prev => {
      const nuevosItems = prev.items.map(item => {
        if (item.id === id) {
          const itemActualizado = { ...item, [campo]: valor };
          
          // Recalcular total del item
          if (campo === 'cantidad' || campo === 'precioUnitario') {
            itemActualizado.total = itemActualizado.cantidad * itemActualizado.precioUnitario;
          }
          
          return itemActualizado;
        }
        return item;
      });

      // Recalcular totales
      const subtotal = nuevosItems.reduce((sum, item) => sum + item.total, 0);
      const igv = subtotal * 0.18;
      const total = subtotal + igv;

      return {
        ...prev,
        items: nuevosItems,
        subtotal: subtotal.toFixed(2),
        igv: igv.toFixed(2),
        total: total.toFixed(2)
      };
    });
  };

  const eliminarItem = (id) => {
    setCotizacion(prev => {
      const nuevosItems = prev.items.filter(item => item.id !== id);
      
      const subtotal = nuevosItems.reduce((sum, item) => sum + item.total, 0);
      const igv = subtotal * 0.18;
      const total = subtotal + igv;

      return {
        ...prev,
        items: nuevosItems,
        subtotal: subtotal.toFixed(2),
        igv: igv.toFixed(2),
        total: total.toFixed(2)
      };
    });
  };

  return (
    <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-8 border-2 border-yellow-600">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <Edit2 className="text-yellow-400" size={32} />
          <h2 className="text-3xl font-black text-yellow-400">
            Editor de Cotización
          </h2>
        </div>
        
        <button
          onClick={() => onGuardar(cotizacion)}
          className="bg-gradient-to-r from-green-600 to-green-500 text-white px-6 py-3 rounded-xl font-bold hover:scale-105 transition-all flex items-center gap-2"
        >
          <Save size={20} />
          Guardar Cambios
        </button>
      </div>

      {/* Datos del cliente */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div>
          <label className="text-yellow-400 font-bold mb-2 block">Cliente</label>
          <input
            type="text"
            value={cotizacion.cliente}
            onChange={(e) => setCotizacion(prev => ({ ...prev, cliente: e.target.value }))}
            className="w-full bg-gray-800 text-white rounded-xl p-3 border-2 border-gray-700 focus:border-yellow-600 focus:outline-none"
            placeholder="Nombre del cliente"
          />
        </div>

        <div>
          <label className="text-yellow-400 font-bold mb-2 block">Proyecto</label>
          <input
            type="text"
            value={cotizacion.proyecto}
            onChange={(e) => setCotizacion(prev => ({ ...prev, proyecto: e.target.value }))}
            className="w-full bg-gray-800 text-white rounded-xl p-3 border-2 border-gray-700 focus:border-yellow-600 focus:outline-none"
            placeholder="Nombre del proyecto"
          />
        </div>
      </div>

      {/* Items */}
      <div className="bg-gray-800 rounded-xl p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-yellow-400 font-bold text-xl">Servicios / Productos</h3>
          <button
            onClick={agregarItem}
            className="bg-gradient-to-r from-yellow-600 to-yellow-500 text-black px-4 py-2 rounded-lg font-bold hover:scale-105 transition-all flex items-center gap-2"
          >
            <Plus size={20} />
            Agregar Item
          </button>
        </div>

        <div className="space-y-4">
          {cotizacion.items.map((item) => (
            <div key={item.id} className="bg-gray-900 rounded-lg p-4 border-2 border-gray-700">
              <div className="grid grid-cols-12 gap-4 items-center">
                <div className="col-span-5">
                  <input
                    type="text"
                    value={item.descripcion}
                    onChange={(e) => actualizarItem(item.id, 'descripcion', e.target.value)}
                    className="w-full bg-gray-800 text-white rounded-lg p-2 border border-gray-600 focus:border-yellow-600 focus:outline-none"
                    placeholder="Descripción"
                  />
                </div>

                <div className="col-span-2">
                  <input
                    type="number"
                    value={item.cantidad}
                    onChange={(e) => actualizarItem(item.id, 'cantidad', parseFloat(e.target.value) || 0)}
                    className="w-full bg-gray-800 text-white rounded-lg p-2 border border-gray-600 focus:border-yellow-600 focus:outline-none text-center"
                    placeholder="Cant."
                    min="0"
                  />
                </div>

                <div className="col-span-2">
                  <input
                    type="number"
                    value={item.precioUnitario}
                    onChange={(e) => actualizarItem(item.id, 'precioUnitario', parseFloat(e.target.value) || 0)}
                    className="w-full bg-gray-800 text-white rounded-lg p-2 border border-gray-600 focus:border-yellow-600 focus:outline-none text-center"
                    placeholder="Precio"
                    min="0"
                    step="0.01"
                  />
                </div>

                <div className="col-span-2">
                  <div className="bg-yellow-900/30 text-yellow-400 rounded-lg p-2 text-center font-bold">
                    S/ {item.total.toFixed(2)}
                  </div>
                </div>

                <div className="col-span-1 flex justify-center">
                  <button
                    onClick={() => eliminarItem(item.id)}
                    className="text-red-500 hover:text-red-400 transition-colors"
                  >
                    <Trash2 size={20} />
                  </button>
                </div>
              </div>
            </div>
          ))}

          {cotizacion.items.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              <Calculator size={48} className="mx-auto mb-4 opacity-50" />
              <p>No hay items. Haz clic en "Agregar Item" para comenzar.</p>
            </div>
          )}
        </div>
      </div>

      {/* Totales */}
      <div className="bg-gradient-to-r from-red-900 to-black rounded-2xl p-6 border-2 border-yellow-600">
        <div className="space-y-4">
          <div className="flex justify-between text-lg">
            <span className="text-gray-300">Subtotal:</span>
            <span className="text-white font-bold">S/ {cotizacion.subtotal}</span>
          </div>
          
          <div className="flex justify-between text-lg">
            <span className="text-gray-300">IGV (18%):</span>
            <span className="text-white font-bold">S/ {cotizacion.igv}</span>
          </div>
          
          <div className="h-px bg-yellow-600"></div>
          
          <div className="flex justify-between text-3xl">
            <span className="text-yellow-400 font-black">TOTAL:</span>
            <span className="text-yellow-400 font-black">S/ {cotizacion.total}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CotizacionEditor;