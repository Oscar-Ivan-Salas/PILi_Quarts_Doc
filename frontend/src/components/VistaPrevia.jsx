import React, { useState, useRef, forwardRef, useImperativeHandle } from 'react';
import { Eye, EyeOff, Download, FileText, Edit, Save } from 'lucide-react';

/**
 * VistaPrevia - Componente para mostrar y editar documentos
 * Basado en ARTEFACTO MODELO con tabla editable inline
 */
const VistaPrevia = forwardRef(({
  cotizacion,
  proyecto,
  informe,
  onGenerarDocumento,
  tipoDocumento = 'cotizacion',
  htmlPreview = ''
}, ref) => {

  // Estados principales
  const [modoEdicion, setModoEdicion] = useState(true); // ✅ TRUE por defecto como ARTEFACTO
  const [ocultarPreciosUnitarios, setOcultarPreciosUnitarios] = useState(false);
  const [ocultarTotalesPorItem, setOcultarTotalesPorItem] = useState(false);
  const [modoVisualizacionIGV, setModoVisualizacionIGV] = useState('sin-igv');

  // Estado editable de la cotización
  const [cotizacionEditable, setCotizacionEditable] = useState(cotizacion || proyecto || informe || {});

  const documentoRef = useRef(null);

  // Exponer métodos al componente padre
  useImperativeHandle(ref, () => ({
    getEditedHTML: () => {
      return documentoRef.current ? documentoRef.current.innerHTML : '';
    },
    isEditMode: () => modoEdicion,
    getEditedData: () => cotizacionEditable
  }));

  // Función para actualizar items (inline editing)
  const actualizarItem = (index, campo, valor) => {
    const nuevosItems = [...cotizacionEditable.items];
    nuevosItems[index][campo] = campo === 'descripcion' || campo === 'unidad'
      ? valor
      : parseFloat(valor) || 0;

    setCotizacionEditable({
      ...cotizacionEditable,
      items: nuevosItems
    });
  };

  // Calcular totales
  const calcularTotales = () => {
    const subtotal = cotizacionEditable.items?.reduce((sum, item) =>
      sum + (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || item.precioUnitario || 0)), 0
    ) || 0;
    const igv = subtotal * 0.18;
    const total = subtotal + igv;

    return {
      subtotal: subtotal.toFixed(2),
      igv: igv.toFixed(2),
      total: total.toFixed(2)
    };
  };

  const totales = calcularTotales();

  // Agrupar items por capítulo
  const itemsPorCapitulo = cotizacionEditable.items?.reduce((acc, item) => {
    const cap = item.capitulo || item.categoria || 'Sin clasificar';
    if (!acc[cap]) acc[cap] = [];
    acc[cap].push(item);
    return acc;
  }, {}) || {};

  const obtenerTituloDocumento = () => {
    if (tipoDocumento.includes('proyecto')) return 'PROYECTO';
    if (tipoDocumento.includes('informe')) return 'INFORME TÉCNICO';
    return 'COTIZACIÓN';
  };

  return (
    <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-8 border-2 border-yellow-600">

      {/* PANEL DE CONTROL - NO SE IMPRIME */}
      <div className="no-print mb-6">
        <div className="bg-gradient-to-r from-yellow-900 to-yellow-800 border-2 border-yellow-500 rounded-2xl p-4 backdrop-blur-md bg-opacity-90 shadow-2xl">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <h3 className="text-black font-bold text-lg">
                {modoEdicion ? '✏️ MODO EDICIÓN' : '✅ VISTA FINAL'}
              </h3>
              <div className="flex gap-2">
                {ocultarPreciosUnitarios && (
                  <span className="bg-purple-600 text-white text-xs px-3 py-1 rounded-full font-bold">
                    🚫 P.U. OCULTOS
                  </span>
                )}
                {ocultarTotalesPorItem && (
                  <span className="bg-indigo-600 text-white text-xs px-3 py-1 rounded-full font-bold">
                    💎 SOLO TOTAL FINAL
                  </span>
                )}
                {modoVisualizacionIGV === 'con-igv' && (
                  <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full font-bold">
                    💵 CON IGV
                  </span>
                )}
                {modoVisualizacionIGV === 'ocultar-igv' && (
                  <span className="bg-blue-800 text-white text-xs px-3 py-1 rounded-full font-bold">
                    🔒 IGV OCULTO
                  </span>
                )}
              </div>
            </div>

            <div className="flex gap-2 flex-wrap">
              {/* Botón Modo Edición */}
              <button
                onClick={() => setModoEdicion(!modoEdicion)}
                className={`px-4 py-2 rounded-xl font-semibold flex items-center gap-2 transition-all border-2 shadow-xl ${modoEdicion
                  ? 'bg-green-800 hover:bg-green-700 border-green-600'
                  : 'bg-blue-800 hover:bg-blue-700 border-blue-600'
                  } text-white`}
              >
                {modoEdicion ? <><Save className="w-5 h-5" /> Finalizar</> : <><Edit className="w-5 h-5" /> Editar</>}
              </button>

              {/* Botones específicos para cotizaciones */}
              {tipoDocumento.includes('cotizacion') && (
                <>
                  <button
                    onClick={() => setOcultarPreciosUnitarios(!ocultarPreciosUnitarios)}
                    className={`px-4 py-2 rounded-xl font-semibold flex items-center gap-2 transition-all border-2 shadow-xl ${ocultarPreciosUnitarios
                      ? 'bg-purple-800 hover:bg-purple-700 border-purple-600'
                      : 'bg-gray-700 hover:bg-gray-600 border-gray-500'
                      } text-white`}
                  >
                    {ocultarPreciosUnitarios ? <><Eye className="w-5 h-5" /> P.U.</> : <><EyeOff className="w-5 h-5" /> P.U.</>}
                  </button>

                  <button
                    onClick={() => setOcultarTotalesPorItem(!ocultarTotalesPorItem)}
                    className={`px-4 py-2 rounded-xl font-semibold flex items-center gap-2 transition-all border-2 shadow-xl ${ocultarTotalesPorItem
                      ? 'bg-indigo-800 hover:bg-indigo-700 border-indigo-600'
                      : 'bg-gray-700 hover:bg-gray-600 border-gray-500'
                      } text-white`}
                  >
                    {ocultarTotalesPorItem ? <><Eye className="w-5 h-5" /> Totales</> : <><EyeOff className="w-5 h-5" /> Totales</>}
                  </button>

                  {/* Dropdown Vista IGV */}
                  <div className="relative group">
                    <button className="px-4 py-2 bg-blue-800 hover:bg-blue-700 text-white rounded-xl font-semibold flex items-center gap-2 transition-all border-2 border-blue-600 shadow-xl">
                      💰 Vista IGV
                    </button>
                    <div className="absolute top-full mt-2 right-0 bg-gray-900 border-2 border-blue-600 rounded-xl shadow-2xl hidden group-hover:block z-50 min-w-64">
                      <div className="p-2">
                        <button
                          onClick={() => setModoVisualizacionIGV('sin-igv')}
                          className={`w-full text-left px-4 py-2 rounded-lg mb-1 ${modoVisualizacionIGV === 'sin-igv' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-800'
                            }`}
                        >
                          📊 Precios SIN IGV (por defecto)
                        </button>
                        <button
                          onClick={() => setModoVisualizacionIGV('con-igv')}
                          className={`w-full text-left px-4 py-2 rounded-lg mb-1 ${modoVisualizacionIGV === 'con-igv' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-800'
                            }`}
                        >
                          💵 Precios CON IGV incluido
                        </button>
                        <button
                          onClick={() => setModoVisualizacionIGV('ocultar-igv')}
                          className={`w-full text-left px-4 py-2 rounded-lg ${modoVisualizacionIGV === 'ocultar-igv' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-800'
                            }`}
                        >
                          🔒 Ocultar desglose IGV
                        </button>
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Botones de Exportación */}
          <div className="mt-4 p-4 bg-gradient-to-r from-blue-900 to-blue-800 rounded-xl border-2 border-blue-500">
            <h4 className="font-bold mb-2 flex items-center gap-2 text-white">
              <Download className="w-5 h-5" />
              📦 Formatos de Exportación
            </h4>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => onGenerarDocumento('word')}
                className="bg-blue-800 hover:bg-blue-700 text-white px-4 py-2 rounded-xl flex items-center justify-center gap-2 transition-all border-2 border-blue-600 shadow-xl"
              >
                <Download className="w-5 h-5" /> DOCX
              </button>
              <button
                onClick={() => onGenerarDocumento('pdf')}
                className="bg-red-800 hover:bg-red-700 text-white px-4 py-2 rounded-xl flex items-center justify-center gap-2 transition-all border-2 border-red-600 shadow-xl"
              >
                <Download className="w-5 h-5" /> PDF
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* DOCUMENTO HTML EDITABLE - FONDO BLANCO */}
      <div
        ref={documentoRef}
        className="bg-white text-gray-900 rounded-2xl p-8 shadow-2xl"
        id="documento-preview"
      >
        {/* Encabezado */}
        <div className="border-b-4 border-red-900 pb-6 mb-6">
          <div className="flex justify-between">
            <div>
              <h1 className="text-4xl font-bold text-red-900">TESLA COTIZADOR PRO</h1>
              <p className="text-gray-600 mt-2">RUC: 20601138787</p>
              <p className="text-sm text-gray-500">Lima, Perú</p>
            </div>
            <div className="text-right">
              <div className="bg-gradient-to-r from-red-900 to-red-800 text-yellow-400 px-4 py-2 rounded-lg inline-block border-2 border-yellow-600">
                <p className="text-sm font-bold">{obtenerTituloDocumento()}</p>
                <p className="text-2xl font-bold">v1.0</p>
              </div>
              <p className="text-sm text-gray-500 mt-2">{new Date().toLocaleDateString('es-PE')}</p>
            </div>
          </div>
        </div>

        {/* Información del Cliente */}
        <div className="mb-6">
          <h3 className="font-bold text-red-900 mb-2">INFORMACIÓN DEL CLIENTE</h3>
          <p><strong>Cliente:</strong> {cotizacionEditable.cliente?.nombre || 'N/A'}</p>
          <p><strong>Proyecto:</strong> {cotizacionEditable.cliente?.proyecto || 'N/A'}</p>
          <p><strong>Dirección:</strong> {cotizacionEditable.cliente?.direccion || 'N/A'}</p>
        </div>

        {/* TABLA DE ITEMS EDITABLE INLINE */}
        {Object.keys(itemsPorCapitulo).map((capitulo, capIndex) => (
          <div key={capIndex} className="mb-6">
            <h3 className="font-bold text-red-900 mb-3 text-lg">{capitulo.toUpperCase()}</h3>

            <div className="overflow-x-auto">
              <table className="w-full border-collapse border-2 border-gray-300">
                <thead>
                  <tr className="bg-red-900 text-white">
                    <th className="py-3 px-3 text-left border-r-2 border-red-800">DESCRIPCIÓN</th>
                    <th className="py-3 px-3 text-center border-r-2 border-red-800 w-24">CANT.</th>
                    <th className="py-3 px-3 text-center border-r-2 border-red-800 w-20">UND.</th>
                    {!ocultarPreciosUnitarios && (
                      <th className="py-3 px-3 text-right border-r-2 border-red-800 w-32">P.U.</th>
                    )}
                    {!ocultarTotalesPorItem && (
                      <th className="py-3 px-3 text-right w-32">TOTAL</th>
                    )}
                  </tr>
                </thead>
                <tbody>
                  {itemsPorCapitulo[capitulo].map((item, itemIndex) => {
                    const globalIndex = cotizacionEditable.items.findIndex(i => i === item);
                    const subtotalItem = parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || item.precioUnitario || 0);

                    return (
                      <tr key={itemIndex} className="border-b border-gray-200">
                        {/* Descripción - EDITABLE */}
                        <td className="py-2 px-3 border-r border-gray-200">
                          {modoEdicion ? (
                            <input
                              type="text"
                              value={item.descripcion}
                              onChange={(e) => actualizarItem(globalIndex, 'descripcion', e.target.value)}
                              className="w-full px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-red-500 focus:outline-none text-sm"
                            />
                          ) : (
                            item.descripcion
                          )}
                        </td>

                        {/* Cantidad - EDITABLE */}
                        <td className="text-center py-2 px-3 border-r border-gray-200">
                          {modoEdicion ? (
                            <input
                              type="number"
                              step="0.01"
                              value={item.cantidad}
                              onChange={(e) => actualizarItem(globalIndex, 'cantidad', e.target.value)}
                              className="w-20 px-2 py-1 border border-gray-300 rounded text-center focus:ring-2 focus:ring-red-500 focus:outline-none"
                            />
                          ) : (
                            item.cantidad
                          )}
                        </td>

                        {/* Unidad */}
                        <td className="text-center py-2 px-3 text-sm border-r border-gray-200">
                          {item.unidad}
                        </td>

                        {/* Precio Unitario - EDITABLE */}
                        {!ocultarPreciosUnitarios && (
                          <td className="text-right py-2 px-3 border-r border-gray-200">
                            {modoEdicion ? (
                              <input
                                type="number"
                                step="0.01"
                                value={item.precio_unitario || item.precioUnitario || 0}
                                onChange={(e) => actualizarItem(globalIndex, 'precioUnitario', e.target.value)}
                                className="w-24 px-2 py-1 border border-gray-300 rounded text-right focus:ring-2 focus:ring-red-500 focus:outline-none"
                              />
                            ) : (
                              `S/ ${parseFloat(item.precio_unitario || item.precioUnitario || 0).toFixed(2)}`
                            )}
                          </td>
                        )}

                        {/* Total - CALCULADO AUTOMÁTICAMENTE */}
                        {!ocultarTotalesPorItem && (
                          <td className="text-right py-2 px-3 font-bold text-base">
                            S/ {subtotalItem.toFixed(2)}
                          </td>
                        )}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        ))}

        {/* TOTALES */}
        <div className="flex justify-end mb-8">
          <div className="w-full md:w-96">
            {modoVisualizacionIGV !== 'ocultar-igv' && (
              <>
                <div className="flex justify-between py-3 border-b-2 border-gray-300 text-lg">
                  <span className="font-semibold">Subtotal:</span>
                  <span className="font-bold">S/ {totales.subtotal}</span>
                </div>
                {modoVisualizacionIGV === 'sin-igv' && (
                  <div className="flex justify-between py-3 border-b-2 border-gray-300 text-lg">
                    <span className="font-semibold">IGV (18%):</span>
                    <span className="font-bold">S/ {totales.igv}</span>
                  </div>
                )}
              </>
            )}
            <div className="flex justify-between py-6 bg-gradient-to-r from-red-900 via-red-800 to-red-900 text-yellow-400 px-6 rounded-2xl mt-4 shadow-2xl border-4 border-yellow-600">
              <span className="font-black text-3xl">TOTAL:</span>
              <span className="font-black text-5xl">
                S/ {modoVisualizacionIGV === 'con-igv'
                  ? (parseFloat(totales.total) * 1.18).toFixed(2)
                  : totales.total}
              </span>
            </div>
            {modoVisualizacionIGV === 'con-igv' && (
              <p className="text-center text-sm text-gray-600 mt-2 italic">* Precio incluye IGV (18%)</p>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="border-t-2 pt-6 text-center text-gray-600">
          <p className="font-bold text-red-900 text-xl mb-2">TESLA COTIZADOR PRO</p>
          <p>📱 WhatsApp: +51 999 888 777</p>
          <p>📧 ventas@teslacotizador.com</p>
          <p>📍 Lima, Perú</p>
        </div>
      </div>

      {/* Información adicional */}
      <div className="mt-6 bg-yellow-900/20 border-2 border-yellow-600 rounded-xl p-6">
        <div className="flex items-start gap-3">
          <div className="bg-yellow-600 rounded-full p-2 mt-1">
            <FileText className="text-black" size={20} />
          </div>
          <div>
            <h4 className="text-yellow-400 font-bold text-lg mb-2">
              Formatos disponibles
            </h4>
            <ul className="text-gray-300 space-y-1">
              <li>• <strong>PDF:</strong> Para envío profesional al cliente</li>
              <li>• <strong>Word:</strong> Para edición y personalización posterior</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
});

export default VistaPrevia;