
// @ts-nocheck
import React, { useState, useEffect } from 'react';

/**
 * Componente Editable: Cotización Compleja
 * Versión completa con Ingeniería de Detalle
 * Incluye: Alcance, Cronograma, Garantías, Condiciones de Pago
 */
const EditableCotizacionCompleja = ({
    datos = {},
    esquemaColores = 'azul', // 'azul' | 'rojo' | 'verde' | 'dorado' | 'magenta'
    logoBase64 = null,
    fuenteDocumento = 'Calibri',
    onDatosChange = () => { },
    ocultarIGV = false,
    ocultarPreciosUnitarios = false,
    ocultarTotalesPorItem = false
}) => {

    const [datosEditables, setDatosEditables] = useState({
        numero: datos.numero || 'COT-COMP-001',
        fecha: datos.fecha || new Date().toLocaleDateString('es-PE'),
        vigencia: datos.vigencia || '30 días',
        cliente: {
            nombre: datos.cliente?.nombre || '',
            ruc: datos.cliente?.ruc || '',
            direccion: datos.cliente?.direccion || ''
        },
        proyecto: datos.proyecto || '',
        area_m2: datos.area_m2 || 0,
        servicio: datos.servicio || 'Instalaciones Eléctricas',
        descripcion_proyecto: datos.descripcion_proyecto || 'Descripción detallada del proyecto...',
        normativa_aplicable: datos.normativa_aplicable || 'CNE - Código Nacional de Electricidad',
        items: datos.items || [
            { descripcion: 'Tablero eléctrico monofásico 12 circuitos', cantidad: 1, unidad: 'und', precio_unitario: 450 }
        ],
        // ✅ CRONOGRAMA AHORA COMO LISTA DINÁMICA
        cronograma_fases: datos.cronograma_fases || [
            { nombre: 'Ingeniería', dias: datos.cronograma?.dias_ingenieria || 5 },
            { nombre: 'Adquisiciones', dias: datos.cronograma?.dias_adquisiciones || 7 },
            { nombre: 'Instalación', dias: datos.cronograma?.dias_instalacion || 10 },
            { nombre: 'Pruebas', dias: datos.cronograma?.dias_pruebas || 3 }
        ],
        // ✅ LISTAS DINÁMICAS (Antes estáticas)
        garantias: datos.garantias || [
            { icon: '🛠️', texto: '12 meses en mano de obra' },
            { icon: '⚙️', texto: 'Garantía de fabricante en equipos' },
            { icon: '💬', texto: 'Soporte técnico por 6 meses' }
        ],
        condiciones_pago: datos.condiciones_pago || [
            '50% de adelanto a la firma del contrato',
            '30% al 50% de avance de obra',
            '20% contra entrega y conformidad'
        ],
        observaciones: datos.observaciones || [
            'Trabajos ejecutados según normativa vigente',
            'Materiales de primera calidad con certificación internacional',
            'Mano de obra especializada y certificada',
            'Incluye transporte de materiales',
            'Pruebas y puesta en marcha incluidas',
            'Capacitación al personal del cliente',
            'Documentación técnica completa (planos as-built, protocolos, certificados)',
            'Precios expresados en la moneda indicada',
            'Cotización válida por el periodo indicado'
        ]
    });

    // Estado para la moneda
    const [moneda, setMoneda] = useState(datos.moneda === 'USD' ? '$' : datos.moneda === 'EUR' ? '€' : 'S/'); // S/, $, €

    const COLORES = {
        'azul': { primario: '#0052A3', secundario: '#1E40AF', acento: '#3B82F6', claro: '#EFF6FF', claroBorde: '#DBEAFE' },
        'rojo': { primario: '#8B0000', secundario: '#991B1B', acento: '#DC2626', claro: '#FEF2F2', claroBorde: '#FECACA' },
        'verde': { primario: '#065F46', secundario: '#047857', acento: '#22C55E', claro: '#F0FDF4', claroBorde: '#BBF7D0' },
        'dorado': { primario: '#D4AF37', secundario: '#B8860B', acento: '#FFD700', claro: '#FEF3C7', claroBorde: '#FDE68A' },
        'magenta': { primario: '#D946EF', secundario: '#C026D3', acento: '#E879F9', claro: '#FAE8FF', claroBorde: '#F5D0FE' } // Magenta Theme
    };

    const colores = COLORES[esquemaColores] || COLORES['azul'];

    const calcularTotales = () => {
        const subtotal = datosEditables.items.reduce((sum, item) =>
            sum + (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || 0)), 0
        );
        const igv = subtotal * 0.18;
        const total = subtotal + igv;
        return { subtotal: subtotal.toFixed(2), igv: igv.toFixed(2), total: total.toFixed(2) };
    };

    const totales = calcularTotales();

    // Sincronizar hacia arriba cuando hay cambios
    useEffect(() => {
        onDatosChange({
            ...datosEditables,
            ...totales,
            moneda: moneda === 'S/' ? 'PEN' : moneda === '$' ? 'USD' : 'EUR'
        });
    }, [datosEditables, moneda]);

    const actualizarItem = (index, campo, valor) => {
        const nuevosItems = [...datosEditables.items];
        nuevosItems[index][campo] = campo === 'descripcion' || campo === 'unidad' ? valor : parseFloat(valor) || 0;
        setDatosEditables({ ...datosEditables, items: nuevosItems });
    };

    const agregarItem = () => {
        setDatosEditables({
            ...datosEditables,
            items: [...datosEditables.items, { descripcion: '', cantidad: 1, unidad: 'und', precio_unitario: 0 }]
        });
    };

    const eliminarItem = (index) => {
        const nuevosItems = datosEditables.items.filter((_, i) => i !== index);
        setDatosEditables({ ...datosEditables, items: nuevosItems });
    };

    return (
        <div className="mx-auto bg-white text-gray-800 shadow-xl" style={{ fontFamily: fuenteDocumento, width: '210mm', minHeight: '297mm', padding: '20mm', boxSizing: 'border-box' }}>

            {/* CABECERA */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '30px', paddingBottom: '20px', borderBottom: `4px solid ${colores.primario}` }}>
                <div style={{ width: '35%' }}>
                    {logoBase64 ? (
                        <img src={logoBase64} alt="Logo" style={{ width: '180px', height: '80px', objectFit: 'contain', borderRadius: '8px' }} />
                    ) : (
                        <div style={{ width: '180px', height: '80px', background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold', fontSize: '24px' }}>PILi</div>
                    )}
                </div>
                <div style={{ width: '65%', textAlign: 'right' }}>
                    <div style={{ fontSize: '20px', fontWeight: 'bold', color: colores.primario, marginBottom: '8px', textTransform: 'uppercase' }}>
                        PILi QUARTS S.A.C.
                    </div>
                    <div style={{ fontSize: '11px', color: '#4b5563', lineHeight: '1.5' }}>
                        <div>RUC: 20601138787</div>
                        <div>Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div>
                        <div>Teléfono: 906 315 961</div>
                        <div>Email: contacto@piliquarts.com</div>
                    </div>
                </div>

                {/* SELECTOR DE MONEDA */}
                <div style={{ position: 'absolute', top: '20mm', right: '20mm', display: 'flex', gap: '5px' }} className="print:hidden">
                    <button onClick={() => setMoneda('S/')} className={`px-2 py-1 text-xs rounded ${moneda === 'S/' ? 'bg-gray-800 text-white' : 'bg-gray-200'}`}>S/</button>
                    <button onClick={() => setMoneda('$')} className={`px-2 py-1 text-xs rounded ${moneda === '$' ? 'bg-gray-800 text-white' : 'bg-gray-200'}`}>$</button>
                    <button onClick={() => setMoneda('€')} className={`px-2 py-1 text-xs rounded ${moneda === '€' ? 'bg-gray-800 text-white' : 'bg-gray-200'}`}>€</button>
                </div>
            </div>

            {/* TÍTULO */}
            <div style={{ textAlign: 'center', margin: '30px 0', padding: '25px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderLeft: `6px solid ${colores.primario}`, borderRadius: '4px' }}>
                <h1 style={{ fontSize: '30px', color: colores.primario, fontWeight: 'bold', marginBottom: '8px' }}>COTIZACIÓN PROFESIONAL</h1>
                <div style={{ fontSize: '14px', color: colores.secundario, marginBottom: '10px', fontStyle: 'italic' }}>Versión Completa con Ingeniería de Detalle</div>
                <div style={{ fontSize: '16px', color: colores.secundario, fontWeight: '600' }}>
                    N° <input type="text" value={datosEditables.numero} onChange={(e) => setDatosEditables({ ...datosEditables, numero: e.target.value })} style={{ border: 'none', borderBottom: `2px solid ${colores.acento}`, background: 'transparent', color: colores.secundario, fontWeight: '600', fontSize: '16px', width: '150px', textAlign: 'center' }} />
                </div>
            </div>

            {/* INFORMACIÓN GENERAL */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', margin: '25px 0' }}>
                <div style={{ padding: '15px', border: `2px solid ${colores.claroBorde}`, borderRadius: '6px', background: '#F9FAFB' }}>
                    <h3 style={{ fontSize: '14px', color: colores.primario, fontWeight: 'bold', marginBottom: '10px', textTransform: 'uppercase', borderBottom: `2px solid ${colores.primario}`, paddingBottom: '5px' }}>Datos del Cliente</h3>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colores.secundario }}>Cliente:</strong>{' '}
                        <input type="text" value={datosEditables.cliente.nombre} onChange={(e) => setDatosEditables({ ...datosEditables, cliente: { ...datosEditables.cliente, nombre: e.target.value } })} style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '70%' }} />
                    </p>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colores.secundario }}>Proyecto:</strong>{' '}
                        <input type="text" value={datosEditables.proyecto} onChange={(e) => setDatosEditables({ ...datosEditables, proyecto: e.target.value })} style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '70%' }} />
                    </p>
                </div>
                <div style={{ padding: '15px', border: `2px solid ${colores.claroBorde}`, borderRadius: '6px', background: '#F9FAFB' }}>
                    <h3 style={{ fontSize: '14px', color: colores.primario, fontWeight: 'bold', marginBottom: '10px', textTransform: 'uppercase', borderBottom: `2px solid ${colores.primario}`, paddingBottom: '5px' }}>Detalles</h3>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colores.secundario }}>Fecha:</strong> {datosEditables.fecha}</p>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colores.secundario }}>Vigencia:</strong>{' '}
                        <input type="text" value={datosEditables.vigencia} onChange={(e) => setDatosEditables({ ...datosEditables, vigencia: e.target.value })} style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '100px' }} />
                    </p>
                </div>
            </div>

            {/* TABLA DE ITEMS */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}` }}>Ítems</h2>
                <table style={{ width: '100%', borderCollapse: 'collapse', margin: '15px 0' }}>
                    <thead style={{ background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, color: 'white' }}>
                        <tr>
                            <th style={{ padding: '10px' }}>Descripción</th>
                            <th style={{ padding: '10px' }}>Cant.</th>
                            <th style={{ padding: '10px' }}>P.Unit</th>
                            <th style={{ padding: '10px' }}>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {datosEditables.items.map((item, index) => {
                            const total = (item.cantidad * item.precio_unitario).toFixed(2);
                            return (
                                <tr key={index} style={{ borderBottom: '1px solid #ddd' }}>
                                    <td style={{ padding: '10px' }}><input value={item.descripcion} onChange={e => actualizarItem(index, 'descripcion', e.target.value)} style={{ width: '100%' }} /></td>
                                    <td style={{ padding: '10px' }}><input type="number" value={item.cantidad} onChange={e => actualizarItem(index, 'cantidad', e.target.value)} style={{ width: '50px' }} /></td>
                                    <td style={{ padding: '10px' }}>{moneda} <input type="number" value={item.precio_unitario} onChange={e => actualizarItem(index, 'precio_unitario', e.target.value)} style={{ width: '70px' }} /></td>
                                    <td style={{ padding: '10px' }}>{moneda} {total}</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
                <div className="print:hidden">
                    <button onClick={agregarItem} className="text-xs bg-gray-200 px-2 py-1 rounded hover:bg-gray-300">Adding Item</button>
                    {datosEditables.items.length > 1 && <button onClick={() => eliminarItem(datosEditables.items.length - 1)} className="text-xs bg-red-200 text-red-800 px-2 py-1 rounded hover:bg-red-300 ml-2">Remove Line</button>}
                </div>
            </div>

            {/* TOTALES */}
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '20px' }}>
                <div style={{ width: '300px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                        <span>Subtotal:</span>
                        <span style={{ fontWeight: 'bold' }}>{moneda} {totales.subtotal}</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                        <span>IGV (18%):</span>
                        <span style={{ fontWeight: 'bold' }}>{moneda} {totales.igv}</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '18px', color: colores.primario, borderTop: `2px solid ${colores.primario}`, paddingTop: '5px' }}>
                        <strong>TOTAL:</strong>
                        <strong>{moneda} {totales.total}</strong>
                    </div>
                </div>
            </div>

        </div>
    );
};

export default EditableCotizacionCompleja;
