import React, { useState, useEffect } from 'react';

/**
 * Componente Editable: Cotización Compleja
 * Versión completa con Ingeniería de Detalle
 * Incluye: Alcance, Cronograma, Garantías, Condiciones de Pago
 */
const EDITABLE_COTIZACION_COMPLEJA = ({
    datos = {},
    esquemaColores = 'azul-tesla',
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
    const [moneda, setMoneda] = useState('S/'); // S/, $, €

    const COLORES = {
        'azul-tesla': { primario: '#0052A3', secundario: '#1E40AF', acento: '#3B82F6', claro: '#EFF6FF', claroBorde: '#DBEAFE' },
        'rojo-energia': { primario: '#8B0000', secundario: '#991B1B', acento: '#DC2626', claro: '#FEF2F2', claroBorde: '#FECACA' },
        'verde-ecologico': { primario: '#27AE60', secundario: '#16A34A', acento: '#22C55E', claro: '#F0FDF4', claroBorde: '#BBF7D0' },
        'personalizado': { primario: '#8B5CF6', secundario: '#7C3AED', acento: '#A78BFA', claro: '#F5F3FF', claroBorde: '#DDD6FE' }  // Morado personalizado
    };

    const colores = COLORES[esquemaColores] || COLORES['azul-tesla'];

    const calcularTotales = () => {
        const subtotal = datosEditables.items.reduce((sum, item) =>
            sum + (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || 0)), 0
        );
        const igv = subtotal * 0.18;
        const total = subtotal + igv;
        return { subtotal: subtotal.toFixed(2), igv: igv.toFixed(2), total: total.toFixed(2) };
    };

    const totales = calcularTotales();

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
        <div style={{ fontFamily: fuenteDocumento, maxWidth: '210mm', margin: '0 auto', padding: '20mm', background: 'white', color: '#1f2937', lineHeight: '1.6' }}>

            {/* CABECERA */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '30px', paddingBottom: '20px', borderBottom: `4px solid ${colores.primario}` }}>
                <div style={{ width: '35%' }}>
                    {logoBase64 ? (
                        <img src={logoBase64} alt="Logo" style={{ width: '180px', height: '80px', objectFit: 'contain', borderRadius: '8px' }} />
                    ) : (
                        <div style={{ width: '180px', height: '80px', background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold', fontSize: '24px' }}>TESLA</div>
                    )}
                    {/* Solo mostrar texto si NO hay logo personalizado */}
                    {!logoBase64 && <p style={{ fontSize: '10px', color: '#6B7280', marginTop: '10px' }}>Electricidad y Automatización</p>}
                </div>
                <div style={{ width: '65%', textAlign: 'right' }}>
                    <div style={{ fontSize: '20px', fontWeight: 'bold', color: colores.primario, marginBottom: '8px', textTransform: 'uppercase' }}>
                        TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.
                    </div>
                    <div style={{ fontSize: '11px', color: '#4b5563', lineHeight: '1.5' }}>
                        <div>RUC: 20601138787</div>
                        <div>Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div>
                        <div>Teléfono: 906 315 961</div>
                        <div>Email: ingenieria.teslaelectricidad@gmail.com</div>
                    </div>
                </div>

                {/* SELECTOR DE MONEDA */}
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '20px', gap: '10px', alignItems: 'center' }}>
                    <span style={{ fontSize: '12px', fontWeight: '600', color: colores.secundario }}>Moneda:</span>
                    <button
                        onClick={() => setMoneda('S/')}
                        style={{
                            padding: '6px 12px',
                            background: moneda === 'S/' ? colores.primario : '#E5E7EB',
                            color: moneda === 'S/' ? 'white' : '#6B7280',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontSize: '11px',
                            fontWeight: '600'
                        }}
                    >
                        S/ Soles
                    </button>
                    <button
                        onClick={() => setMoneda('$')}
                        style={{
                            padding: '6px 12px',
                            background: moneda === '$' ? colores.primario : '#E5E7EB',
                            color: moneda === '$' ? 'white' : '#6B7280',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontSize: '11px',
                            fontWeight: '600'
                        }}
                    >
                        $ Dólares
                    </button>
                    <button
                        onClick={() => setMoneda('€')}
                        style={{
                            padding: '6px 12px',
                            background: moneda === '€' ? colores.primario : '#E5E7EB',
                            color: moneda === '€' ? 'white' : '#6B7280',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontSize: '11px',
                            fontWeight: '600'
                        }}
                    >
                        € Euros
                    </button>
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
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colores.secundario }}>Área:</strong>{' '}
                        <input type="number" value={datosEditables.area_m2} onChange={(e) => setDatosEditables({ ...datosEditables, area_m2: e.target.value })} style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '60px' }} /> m²
                    </p>
                </div>
                <div style={{ padding: '15px', border: `2px solid ${colores.claroBorde}`, borderRadius: '6px', background: '#F9FAFB' }}>
                    <h3 style={{ fontSize: '14px', color: colores.primario, fontWeight: 'bold', marginBottom: '10px', textTransform: 'uppercase', borderBottom: `2px solid ${colores.primario}`, paddingBottom: '5px' }}>Datos de la Cotización</h3>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colores.secundario }}>Fecha:</strong> {datosEditables.fecha}</p>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colores.secundario }}>Vigencia:</strong>{' '}
                        <input type="text" value={datosEditables.vigencia} onChange={(e) => setDatosEditables({ ...datosEditables, vigencia: e.target.value })} style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '100px' }} />
                    </p>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colores.secundario }}>Servicio:</strong>{' '}
                        <input type="text" value={datosEditables.servicio} onChange={(e) => setDatosEditables({ ...datosEditables, servicio: e.target.value })} style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '70%' }} />
                    </p>
                </div>
            </div>

            {/* ALCANCE DEL PROYECTO */}
            <div style={{ margin: '25px 0', padding: '20px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, borderRadius: '4px' }}>
                <h2 style={{ fontSize: '16px', color: colores.primario, fontWeight: 'bold', marginBottom: '15px', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '4px', height: '20px', background: colores.acento, display: 'inline-block' }}></span>
                    Alcance del Proyecto
                </h2>
                <textarea
                    value={datosEditables.descripcion_proyecto}
                    onChange={(e) => setDatosEditables({ ...datosEditables, descripcion_proyecto: e.target.value })}
                    style={{ width: '100%', minHeight: '100px', fontSize: '12px', color: '#374151', lineHeight: '1.8', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px' }}
                />
                <p style={{ marginTop: '15px', fontSize: '12px' }}><strong style={{ color: colores.primario }}>INCLUYE:</strong></p>
                <div style={{ fontSize: '11px', color: '#6B7280', fontStyle: 'italic' }}>(Edita las observaciones abajo para modificar los detalles de inclusión)</div>
            </div>

            {/* TABLA DE ITEMS */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}` }}>Detalle de la Cotización</h2>
                <table style={{ width: '100%', borderCollapse: 'collapse', margin: '15px 0', boxShadow: `0 2px 8px rgba(0, 82, 163, 0.1)` }}>
                    <thead style={{ background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, color: 'white' }}>
                        <tr>
                            <th style={{ padding: '14px 10px', textAlign: 'left', fontSize: '12px', fontWeight: '700', width: '8%' }}>ITEM</th>
                            <th style={{ padding: '14px 10px', textAlign: 'left', fontSize: '12px', fontWeight: '700', width: '42%' }}>DESCRIPCIÓN</th>
                            <th style={{ padding: '14px 10px', textAlign: 'center', fontSize: '12px', fontWeight: '700', width: '10%' }}>CANT.</th>
                            <th style={{ padding: '14px 10px', textAlign: 'center', fontSize: '12px', fontWeight: '700', width: '10%' }}>UND.</th>
                            <th style={{ padding: '14px 10px', textAlign: 'right', fontSize: '12px', fontWeight: '700', width: '15%' }}>P. UNIT.</th>
                            <th style={{ padding: '14px 10px', textAlign: 'right', fontSize: '12px', fontWeight: '700', width: '15%' }}>TOTAL</th>
                        </tr>
                    </thead>
                    <tbody>
                        {datosEditables.items.map((item, index) => {
                            const subtotalItem = (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || 0)).toFixed(2);
                            return (
                                <tr key={index} style={{ borderBottom: '1px solid #E5E7EB', background: index % 2 === 0 ? '#F9FAFB' : 'white' }}>
                                    <td style={{ padding: '12px 10px', textAlign: 'center', fontSize: '11px' }}>{String(index + 1).padStart(2, '0')}</td>
                                    <td style={{ padding: '12px 10px', fontSize: '11px' }}>
                                        <input type="text" value={item.descripcion} onChange={(e) => actualizarItem(index, 'descripcion', e.target.value)} style={{ width: '100%', border: 'none', background: 'transparent', fontSize: '11px' }} />
                                    </td>
                                    <td style={{ padding: '12px 10px', textAlign: 'right', fontSize: '11px' }}>
                                        <input type="number" value={item.cantidad} onChange={(e) => actualizarItem(index, 'cantidad', e.target.value)} style={{ width: '60px', border: 'none', background: 'transparent', fontSize: '11px', textAlign: 'right' }} />
                                    </td>
                                    <td style={{ padding: '12px 10px', textAlign: 'right', fontSize: '11px' }}>
                                        <input type="text" value={item.unidad} onChange={(e) => actualizarItem(index, 'unidad', e.target.value)} style={{ width: '50px', border: 'none', background: 'transparent', fontSize: '11px', textAlign: 'right' }} />
                                    </td>
                                    <td style={{ padding: '12px 10px', textAlign: 'right', fontSize: '11px', color: ocultarPreciosUnitarios ? 'transparent' : '#1f2937' }}>
                                        {moneda} <input type="number" value={item.precio_unitario} onChange={(e) => actualizarItem(index, 'precio_unitario', e.target.value)} style={{ width: '80px', border: 'none', background: 'transparent', fontSize: '11px', textAlign: 'right', color: ocultarPreciosUnitarios ? 'transparent' : '#1f2937' }} />
                                    </td>
                                    <td style={{ padding: '12px 10px', textAlign: 'right', fontSize: '11px', fontWeight: '600', color: ocultarTotalesPorItem ? 'transparent' : '#1f2937' }}>{moneda} {subtotalItem}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
                <div style={{ marginTop: '10px', display: 'flex', gap: '10px' }}>
                    <button onClick={agregarItem} style={{ padding: '8px 16px', background: colores.primario, color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '12px' }}>+ Agregar Item</button>
                    {datosEditables.items.length > 1 && (
                        <button onClick={() => eliminarItem(datosEditables.items.length - 1)} style={{ padding: '8px 16px', background: '#DC2626', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '12px' }}>- Eliminar Último</button>
                    )}
                </div>
            </div>

            {/* TOTALES */}
            <div style={{ marginTop: '25px', display: 'flex', justifyContent: 'flex-end' }}>
                <div style={{ width: '350px', border: `2px solid ${colores.primario}`, borderRadius: '6px', overflow: 'hidden' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 20px', borderBottom: `1px solid ${colores.claroBorde}` }}>
                        <span style={{ fontWeight: '600', color: colores.secundario }}>SUBTOTAL:</span>
                        <span style={{ fontWeight: '700', color: colores.primario }}>{moneda} {totales.subtotal}</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 20px', borderBottom: `1px solid ${colores.claroBorde}` }}>
                        <span style={{ fontWeight: '600', color: ocultarIGV ? 'transparent' : colores.secundario }}>IGV (18%):</span>
                        <span style={{ fontWeight: '700', color: ocultarIGV ? 'transparent' : colores.primario }}>{moneda} {totales.igv}</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 20px', background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, color: 'white', fontWeight: 'bold', fontSize: '16px' }}>
                        <span>TOTAL:</span>
                        <span>{moneda} {ocultarIGV ? totales.subtotal : totales.total}</span>
                    </div>
                </div>
            </div>

            {/* CRONOGRAMA ESTIMADO (Editable) */}
            <div style={{ margin: '30px 0', padding: '20px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, borderRadius: '4px' }}>
                <h2 style={{ fontSize: '16px', color: colores.primario, fontWeight: 'bold', marginBottom: '15px', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '4px', height: '20px', background: colores.acento, display: 'inline-block' }}></span>
                    Cronograma Estimado
                </h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '15px', margin: '20px 0' }}>
                    {datosEditables.cronograma_fases.map((fase, i) => (
                        <div key={i} style={{ padding: '15px', background: 'white', border: `2px solid ${colores.claroBorde}`, borderRadius: '6px', textAlign: 'center' }}>
                            <div style={{ width: '40px', height: '40px', background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '18px', margin: '0 auto 10px' }}>{i + 1}</div>
                            <div style={{ fontSize: '12px', color: colores.primario, fontWeight: 'bold', marginBottom: '5px' }}>
                                <input
                                    type="text"
                                    value={fase.nombre}
                                    onChange={(e) => {
                                        const newFases = [...datosEditables.cronograma_fases];
                                        newFases[i].nombre = e.target.value;
                                        setDatosEditables({ ...datosEditables, cronograma_fases: newFases });
                                    }}
                                    style={{ width: '100%', border: 'none', background: 'transparent', color: colores.primario, fontWeight: 'bold', textAlign: 'center' }}
                                />
                            </div>
                            <div style={{ fontSize: '11px', color: '#6B7280' }}>
                                <input
                                    type="number"
                                    value={fase.dias}
                                    onChange={(e) => {
                                        const newFases = [...datosEditables.cronograma_fases];
                                        newFases[i].dias = parseInt(e.target.value) || 0;
                                        setDatosEditables({ ...datosEditables, cronograma_fases: newFases });
                                    }}
                                    style={{ width: '40px', border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '11px', textAlign: 'center' }}
                                /> días
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* GARANTÍAS (Editable) */}
            <div style={{ margin: '25px 0', padding: '20px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, borderRadius: '4px' }}>
                <h2 style={{ fontSize: '16px', color: colores.primario, fontWeight: 'bold', marginBottom: '15px', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '4px', height: '20px', background: colores.acento, display: 'inline-block' }}></span>
                    Garantías Incluidas
                </h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', margin: '20px 0' }}>
                    {datosEditables.garantias.map((garantia, i) => (
                        <div key={i} style={{ padding: '15px', background: 'white', border: `2px solid ${colores.claroBorde}`, borderRadius: '6px', textAlign: 'center' }}>
                            <div style={{ width: '50px', height: '50px', background: colores.claro, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 10px', fontSize: '24px' }}>
                                <input
                                    type="text"
                                    value={garantia.icon}
                                    onChange={(e) => {
                                        const nuevasGarantias = [...datosEditables.garantias];
                                        nuevasGarantias[i].icon = e.target.value;
                                        setDatosEditables({ ...datosEditables, garantias: nuevasGarantias });
                                    }}
                                    style={{ width: '40px', border: 'none', background: 'transparent', textAlign: 'center' }}
                                />
                            </div>
                            <div style={{ fontSize: '11px', color: '#374151', fontWeight: '600' }}>
                                <input
                                    type="text"
                                    value={garantia.texto}
                                    onChange={(e) => {
                                        const nuevasGarantias = [...datosEditables.garantias];
                                        nuevasGarantias[i].texto = e.target.value;
                                        setDatosEditables({ ...datosEditables, garantias: nuevasGarantias });
                                    }}
                                    style={{ width: '100%', border: 'none', background: 'transparent', textAlign: 'center', fontWeight: '600' }}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* CONDICIONES DE PAGO (Editable) */}
            <div style={{ margin: '25px 0', padding: '20px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, borderRadius: '4px' }}>
                <h2 style={{ fontSize: '16px', color: colores.primario, fontWeight: 'bold', marginBottom: '15px', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '4px', height: '20px', background: colores.acento, display: 'inline-block' }}></span>
                    Condiciones de Pago
                </h2>
                <ul style={{ listStyle: 'none', padding: 0 }}>
                    {datosEditables.condiciones_pago.map((condicion, i) => (
                        <li key={i} style={{ fontSize: '11px', margin: '10px 0', paddingLeft: '25px', position: 'relative' }}>
                            <span style={{ position: 'absolute', left: 0, color: colores.primario, fontWeight: 'bold', fontSize: '14px' }}>✓</span>
                            <input
                                type="text"
                                value={condicion}
                                onChange={(e) => {
                                    const nuevasCondiciones = [...datosEditables.condiciones_pago];
                                    nuevasCondiciones[i] = e.target.value;
                                    setDatosEditables({ ...datosEditables, condiciones_pago: nuevasCondiciones });
                                }}
                                style={{ width: '95%', border: 'none', background: 'transparent' }}
                            />
                        </li>
                    ))}
                </ul>
            </div>

            {/* OBSERVACIONES (Editable) */}
            <div style={{ margin: '25px 0', padding: '20px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, borderRadius: '4px' }}>
                <h2 style={{ fontSize: '16px', color: colores.primario, fontWeight: 'bold', marginBottom: '15px', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '4px', height: '20px', background: colores.acento, display: 'inline-block' }}></span>
                    Observaciones Técnicas
                </h2>
                <ul style={{ listStyle: 'none', padding: 0 }}>
                    {datosEditables.observaciones.map((obs, i) => (
                        <li key={i} style={{ fontSize: '11px', margin: '10px 0', paddingLeft: '25px', position: 'relative' }}>
                            <span style={{ position: 'absolute', left: 0, color: colores.primario, fontWeight: 'bold', fontSize: '14px' }}>✓</span>
                            <input
                                type="text"
                                value={obs}
                                onChange={(e) => {
                                    const nuevasObs = [...datosEditables.observaciones];
                                    nuevasObs[i] = e.target.value;
                                    setDatosEditables({ ...datosEditables, observaciones: nuevasObs });
                                }}
                                style={{ width: '95%', border: 'none', background: 'transparent' }}
                            />
                        </li>
                    ))}
                </ul>
            </div>

            {/* PIE DE PÁGINA */}
            <div style={{ marginTop: '40px', paddingTop: '20px', borderTop: `3px solid ${colores.primario}`, textAlign: 'center', fontSize: '10px', color: '#6B7280' }}>
                <div style={{ fontWeight: 'bold', color: colores.primario, fontSize: '12px', marginBottom: '8px' }}>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
                <div>RUC: 20601138787 | Teléfono: 906 315 961</div>
                <div>Email: ingenieria.teslaelectricidad@gmail.com</div>
                <div>Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div>
            </div>
        </div>
    );
};

export default EDITABLE_COTIZACION_COMPLEJA;
