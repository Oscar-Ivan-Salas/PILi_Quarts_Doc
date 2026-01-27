import React, { useState, useEffect } from 'react';

/**
 * Componente Editable: Proyecto Simple
 * Incluye: Resumen, Fases, Cronograma, Recursos
 */
const EDITABLE_PROYECTO_SIMPLE = ({
    datos = {},
    esquemaColores = 'azul-tesla',
    logoBase64 = null,
    fuenteDocumento = 'Calibri',
    onDatosChange = () => { }
}) => {

    const [datosEditables, setDatosEditables] = useState({
        numero: datos.numero || 'PROY-001',
        fecha: datos.fecha || new Date().toLocaleDateString('es-PE'),
        cliente: { nombre: datos.cliente?.nombre || '' },
        nombre_proyecto: datos.nombre_proyecto || '',
        resumen: datos.resumen || 'Resumen ejecutivo del proyecto...',
        fases: datos.fases || [
            { nombre: 'Fase 1: Planificación', descripcion: 'Descripción...', duracion: '2 semanas', responsable: 'Por asignar' }
        ],
        cronograma: {
            fecha_inicio: datos.cronograma?.fecha_inicio || '01/01/2025',
            fecha_fin: datos.cronograma?.fecha_fin || '31/03/2025',
            duracion_total: datos.cronograma?.duracion_total || '12 semanas'
        },
        recursos: {
            humanos: datos.recursos?.humanos || ['Ingeniero de proyecto', 'Técnico electricista'],
            materiales: datos.recursos?.materiales || ['Cables', 'Tableros', 'Equipos']
        }
    });

    const COLORES = {
        'azul-tesla': { primario: '#0052A3', secundario: '#1E40AF', acento: '#3B82F6', claro: '#EFF6FF', claroBorde: '#DBEAFE' },
        'rojo-energia': { primario: '#8B0000', secundario: '#991B1B', acento: '#DC2626', claro: '#FEF2F2', claroBorde: '#FECACA' },
        'verde-ecologico': { primario: '#27AE60', secundario: '#16A34A', acento: '#22C55E', claro: '#F0FDF4', claroBorde: '#BBF7D0' },
        'personalizado': { primario: '#8B5CF6', secundario: '#7C3AED', acento: '#A78BFA', claro: '#F5F3FF', claroBorde: '#DDD6FE' }  // Morado personalizado
    };

    const colores = COLORES[esquemaColores] || COLORES['azul-tesla'];

    useEffect(() => {
        onDatosChange(datosEditables);
    }, [datosEditables]);

    const actualizarFase = (index, campo, valor) => {
        const nuevasFases = [...datosEditables.fases];
        nuevasFases[index][campo] = valor;
        setDatosEditables({ ...datosEditables, fases: nuevasFases });
    };

    const agregarFase = () => {
        setDatosEditables({
            ...datosEditables,
            fases: [...datosEditables.fases, { nombre: 'Nueva Fase', descripcion: '', duracion: '1 semana', responsable: '' }]
        });
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
            </div>

            {/* TÍTULO */}
            <div style={{ textAlign: 'center', margin: '30px 0', padding: '25px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderLeft: `6px solid ${colores.primario}`, borderRadius: '4px' }}>
                <h1 style={{ fontSize: '30px', color: colores.primario, fontWeight: 'bold', marginBottom: '8px' }}>PROYECTO DE SERVICIOS</h1>
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
                        <input type="text" value={datosEditables.nombre_proyecto} onChange={(e) => setDatosEditables({ ...datosEditables, nombre_proyecto: e.target.value })} style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '70%' }} />
                    </p>
                </div>
                <div style={{ padding: '15px', border: `2px solid ${colores.claroBorde}`, borderRadius: '6px', background: '#F9FAFB' }}>
                    <h3 style={{ fontSize: '14px', color: colores.primario, fontWeight: 'bold', marginBottom: '10px', textTransform: 'uppercase', borderBottom: `2px solid ${colores.primario}`, paddingBottom: '5px' }}>Datos del Proyecto</h3>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colores.secundario }}>Fecha:</strong> {datosEditables.fecha}</p>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colores.secundario }}>Duración:</strong>{' '}
                        <input type="text" value={datosEditables.cronograma.duracion_total} onChange={(e) => setDatosEditables({ ...datosEditables, cronograma: { ...datosEditables.cronograma, duracion_total: e.target.value } })} style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '100px' }} />
                    </p>
                </div>
            </div>

            {/* RESUMEN EJECUTIVO */}
            <div style={{ margin: '30px 0', padding: '25px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderLeft: `6px solid ${colores.primario}`, borderRadius: '4px' }}>
                <h3 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', textTransform: 'uppercase' }}>Resumen del Proyecto</h3>
                <textarea
                    value={datosEditables.resumen}
                    onChange={(e) => setDatosEditables({ ...datosEditables, resumen: e.target.value })}
                    style={{ width: '100%', minHeight: '100px', fontSize: '13px', lineHeight: '1.8', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px', background: 'white' }}
                />
            </div>

            {/* FASES DEL PROYECTO */}
            <div style={{ margin: '35px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>FASES DEL PROYECTO</h2>
                <p style={{ fontSize: '12px', color: '#374151', lineHeight: '1.8', marginBottom: '20px' }}>El proyecto se desarrollará en las siguientes fases principales:</p>
                {datosEditables.fases.map((fase, index) => (
                    <div key={index} style={{ margin: '15px 0', padding: '15px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, borderRadius: '4px' }}>
                        <div style={{ marginBottom: '10px' }}>
                            <strong style={{ color: colores.primario }}>Fase {index + 1}:</strong>{' '}
                            <input
                                type="text"
                                value={fase.nombre}
                                onChange={(e) => actualizarFase(index, 'nombre', e.target.value)}
                                style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '60%', fontWeight: 'bold' }}
                            />
                        </div>
                        <div style={{ marginBottom: '8px' }}>
                            <strong style={{ fontSize: '11px', color: colores.secundario }}>Descripción:</strong>
                            <textarea
                                value={fase.descripcion}
                                onChange={(e) => actualizarFase(index, 'descripcion', e.target.value)}
                                style={{ width: '100%', minHeight: '60px', fontSize: '11px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '8px', marginTop: '5px' }}
                            />
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '11px' }}>
                            <div>
                                <strong style={{ color: colores.secundario }}>Duración:</strong>{' '}
                                <input
                                    type="text"
                                    value={fase.duracion}
                                    onChange={(e) => actualizarFase(index, 'duracion', e.target.value)}
                                    style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '11px', width: '100px' }}
                                />
                            </div>
                            <div>
                                <strong style={{ color: colores.secundario }}>Responsable:</strong>{' '}
                                <input
                                    type="text"
                                    value={fase.responsable}
                                    onChange={(e) => actualizarFase(index, 'responsable', e.target.value)}
                                    style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '11px', width: '150px' }}
                                />
                            </div>
                        </div>
                    </div>
                ))}
                <button onClick={agregarFase} style={{ marginTop: '10px', padding: '8px 16px', background: colores.primario, color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '12px' }}>+ Agregar Fase</button>
            </div>

            {/* CRONOGRAMA */}
            <div style={{ margin: '35px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>CRONOGRAMA</h2>
                <div style={{ padding: '20px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, borderRadius: '4px' }}>
                    <p style={{ fontSize: '12px', marginBottom: '10px' }}>
                        <strong>Fecha de Inicio:</strong>{' '}
                        <input
                            type="text"
                            value={datosEditables.cronograma.fecha_inicio}
                            onChange={(e) => setDatosEditables({ ...datosEditables, cronograma: { ...datosEditables.cronograma, fecha_inicio: e.target.value } })}
                            style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '120px' }}
                        />
                    </p>
                    <p style={{ fontSize: '12px', marginBottom: '10px' }}>
                        <strong>Fecha de Fin:</strong>{' '}
                        <input
                            type="text"
                            value={datosEditables.cronograma.fecha_fin}
                            onChange={(e) => setDatosEditables({ ...datosEditables, cronograma: { ...datosEditables.cronograma, fecha_fin: e.target.value } })}
                            style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '120px' }}
                        />
                    </p>
                    <p style={{ fontSize: '12px' }}>
                        <strong>Duración Total:</strong>{' '}
                        <input
                            type="text"
                            value={datosEditables.cronograma.duracion_total}
                            onChange={(e) => setDatosEditables({ ...datosEditables, cronograma: { ...datosEditables.cronograma, duracion_total: e.target.value } })}
                            style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '120px' }}
                        />
                    </p>
                </div>
            </div>

            {/* RECURSOS */}
            <div style={{ margin: '35px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>RECURSOS</h2>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                    <div style={{ padding: '15px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, borderRadius: '4px' }}>
                        <h3 style={{ fontSize: '14px', color: colores.primario, marginBottom: '10px' }}>Recursos Humanos</h3>
                        <ul style={{ listStyle: 'none', padding: 0 }}>
                            {datosEditables.recursos.humanos.map((recurso, i) => (
                                <li key={i} style={{ fontSize: '11px', margin: '8px 0', paddingLeft: '20px', position: 'relative' }}>
                                    <span style={{ position: 'absolute', left: 0, color: colores.primario, fontSize: '14px' }}>●</span>
                                    {recurso}
                                </li>
                            ))}
                        </ul>
                    </div>
                    <div style={{ padding: '15px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, borderRadius: '4px' }}>
                        <h3 style={{ fontSize: '14px', color: colores.primario, marginBottom: '10px' }}>Recursos Materiales</h3>
                        <ul style={{ listStyle: 'none', padding: 0 }}>
                            {datosEditables.recursos.materiales.map((material, i) => (
                                <li key={i} style={{ fontSize: '11px', margin: '8px 0', paddingLeft: '20px', position: 'relative' }}>
                                    <span style={{ position: 'absolute', left: 0, color: colores.primario, fontSize: '14px' }}>●</span>
                                    {material}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>

            {/* PIE DE PÁGINA */}
            <div style={{ marginTop: '40px', paddingTop: '20px', borderTop: `3px solid ${colores.primario}`, textAlign: 'center', fontSize: '10px', color: '#6B7280' }}>
                <div style={{ fontWeight: 'bold', color: colores.primario, fontSize: '12px', marginBottom: '8px' }}>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
                <div style={{ margin: '5px 0' }}>RUC: 20601138787 | Teléfono: 906 315 961</div>
                <div style={{ margin: '5px 0' }}>Email: ingenieria.teslaelectricidad@gmail.com</div>
                <div style={{ margin: '5px 0' }}>Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div>
            </div>
        </div>
    );
};

export default EDITABLE_PROYECTO_SIMPLE;
