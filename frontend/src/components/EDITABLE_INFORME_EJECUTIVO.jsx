import React, { useState, useEffect } from 'react';

/**
 * Componente Editable: Informe Ejecutivo (Formato APA)
 * Incluye: Abstract, Metodología, Resultados, Discusión, Referencias
 */
const EDITABLE_INFORME_EJECUTIVO = ({
    datos = {},
    esquemaColores = 'azul-tesla',
    logoBase64 = null,
    fuenteDocumento = 'Calibri',
    onDatosChange = () => { }
}) => {

    const [datosEditables, setDatosEditables] = useState({
        codigo: datos.codigo || 'INF-EJEC-001',
        fecha: datos.fecha || new Date().toLocaleDateString('es-PE'),
        cliente: { nombre: datos.cliente?.nombre || '' },
        titulo: datos.titulo || 'Informe Ejecutivo',
        autor: datos.autor || 'Tesla Electricidad',
        abstract: datos.abstract || 'Abstract del informe ejecutivo...',
        metodologia: datos.metodologia || 'Metodología utilizada en el estudio...',
        resultados: datos.resultados || 'Resultados obtenidos del análisis...',
        discusion: datos.discusion || 'Discusión de los resultados...',
        referencias: datos.referencias || [
            { autor: 'Autor, A.', año: '2024', titulo: 'Título del artículo', fuente: 'Revista Científica' }
        ]
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

    const actualizarReferencia = (index, campo, valor) => {
        const nuevasRefs = [...datosEditables.referencias];
        nuevasRefs[index][campo] = valor;
        setDatosEditables({ ...datosEditables, referencias: nuevasRefs });
    };

    const agregarReferencia = () => {
        setDatosEditables({
            ...datosEditables,
            referencias: [...datosEditables.referencias, { autor: '', año: '', titulo: '', fuente: '' }]
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
                <h1 style={{ fontSize: '30px', color: colores.primario, fontWeight: 'bold', marginBottom: '8px' }}>INFORME EJECUTIVO</h1>
                <div style={{ fontSize: '14px', color: colores.secundario, fontStyle: 'italic', marginBottom: '10px' }}>Formato APA</div>
                <div style={{ fontSize: '16px', color: colores.secundario, fontWeight: '600', marginTop: '10px' }}>
                    <input
                        type="text"
                        value={datosEditables.titulo}
                        onChange={(e) => setDatosEditables({ ...datosEditables, titulo: e.target.value })}
                        style={{ border: 'none', borderBottom: `2px solid ${colores.acento}`, background: 'transparent', color: colores.secundario, fontWeight: '600', fontSize: '16px', width: '80%', textAlign: 'center' }}
                    />
                </div>
                <div style={{ fontSize: '13px', color: '#374151', marginTop: '10px' }}>
                    Autor: <input type="text" value={datosEditables.autor} onChange={(e) => setDatosEditables({ ...datosEditables, autor: e.target.value })} style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '13px', width: '200px', textAlign: 'center' }} />
                </div>
                <div style={{ fontSize: '12px', color: '#6B7280', marginTop: '5px' }}>
                    {datosEditables.fecha} | Código: {datosEditables.codigo}
                </div>
            </div>

            {/* INFORMACIÓN GENERAL */}
            <div style={{ padding: '15px', border: `2px solid ${colores.claroBorde}`, borderRadius: '6px', background: '#F9FAFB', margin: '25px 0' }}>
                <p style={{ fontSize: '12px', margin: '5px 0' }}>
                    <strong style={{ color: colores.secundario }}>Cliente:</strong>{' '}
                    <input type="text" value={datosEditables.cliente.nombre} onChange={(e) => setDatosEditables({ ...datosEditables, cliente: { ...datosEditables.cliente, nombre: e.target.value } })} style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '12px', width: '70%' }} />
                </p>
                <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colores.secundario }}>Fecha:</strong> {datosEditables.fecha}</p>
                <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colores.secundario }}>Código:</strong> {datosEditables.codigo}</p>
            </div>

            {/* ABSTRACT */}
            <div style={{ margin: '30px 0', padding: '25px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderLeft: `6px solid ${colores.primario}`, borderRadius: '4px' }}>
                <h3 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', textTransform: 'uppercase' }}>Abstract</h3>
                <textarea
                    value={datosEditables.abstract}
                    onChange={(e) => setDatosEditables({ ...datosEditables, abstract: e.target.value })}
                    style={{ width: '100%', minHeight: '120px', fontSize: '12px', color: '#374151', lineHeight: '1.8', textAlign: 'justify', fontStyle: 'italic', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px', background: 'white' }}
                />
                <p style={{ fontSize: '10px', color: '#6B7280', marginTop: '10px', fontStyle: 'italic' }}>
                    Palabras clave: Instalaciones eléctricas, Ingeniería, Automatización
                </p>
            </div>

            {/* 1. INTRODUCCIÓN */}
            <div style={{ margin: '35px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>1. INTRODUCCIÓN</h2>
                <p style={{ fontSize: '12px', color: '#374151', lineHeight: '1.8', textAlign: 'justify' }}>
                    El presente informe ejecutivo presenta los hallazgos y recomendaciones derivados del análisis realizado para {datosEditables.cliente.nombre}.
                    El estudio se enfoca en proporcionar información técnica relevante para la toma de decisiones estratégicas.
                </p>
            </div>

            {/* 2. METODOLOGÍA */}
            <div style={{ margin: '35px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>2. METODOLOGÍA</h2>
                <textarea
                    value={datosEditables.metodologia}
                    onChange={(e) => setDatosEditables({ ...datosEditables, metodologia: e.target.value })}
                    style={{ width: '100%', minHeight: '150px', fontSize: '12px', color: '#374151', lineHeight: '1.8', textAlign: 'justify', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px' }}
                />
            </div>

            {/* 3. RESULTADOS */}
            <div style={{ margin: '35px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>3. RESULTADOS</h2>
                <textarea
                    value={datosEditables.resultados}
                    onChange={(e) => setDatosEditables({ ...datosEditables, resultados: e.target.value })}
                    style={{ width: '100%', minHeight: '200px', fontSize: '12px', color: '#374151', lineHeight: '1.8', textAlign: 'justify', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px' }}
                />
            </div>

            {/* 4. DISCUSIÓN */}
            <div style={{ margin: '35px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>4. DISCUSIÓN</h2>
                <textarea
                    value={datosEditables.discusion}
                    onChange={(e) => setDatosEditables({ ...datosEditables, discusion: e.target.value })}
                    style={{ width: '100%', minHeight: '150px', fontSize: '12px', color: '#374151', lineHeight: '1.8', textAlign: 'justify', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px' }}
                />
            </div>

            {/* CONCLUSIONES */}
            <div style={{ margin: '30px 0' }}>
                <div style={{ padding: '25px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderLeft: `6px solid ${colores.primario}`, borderRadius: '4px' }}>
                    <h3 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px' }}>CONCLUSIONES</h3>
                    <p style={{ fontSize: '12px', color: '#374151', lineHeight: '1.6' }}>
                        Basándose en los resultados obtenidos y la discusión presentada, se concluye que el análisis realizado proporciona
                        información valiosa para la toma de decisiones estratégicas en el ámbito de las instalaciones eléctricas y automatización.
                    </p>
                </div>
            </div>

            {/* REFERENCIAS (Formato APA) */}
            <div style={{ margin: '35px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>REFERENCIAS</h2>
                <div style={{ fontSize: '11px', color: '#374151', lineHeight: '1.6' }}>
                    {datosEditables.referencias.map((ref, index) => (
                        <div key={index} style={{ marginBottom: '15px', paddingLeft: '30px', textIndent: '-30px', padding: '10px', background: '#F9FAFB', borderRadius: '4px' }}>
                            <div style={{ marginBottom: '5px' }}>
                                <strong>Autor:</strong>{' '}
                                <input
                                    type="text"
                                    value={ref.autor}
                                    onChange={(e) => actualizarReferencia(index, 'autor', e.target.value)}
                                    style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '11px', width: '200px' }}
                                />
                            </div>
                            <div style={{ marginBottom: '5px' }}>
                                <strong>Año:</strong>{' '}
                                <input
                                    type="text"
                                    value={ref.año}
                                    onChange={(e) => actualizarReferencia(index, 'año', e.target.value)}
                                    style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '11px', width: '80px' }}
                                />
                            </div>
                            <div style={{ marginBottom: '5px' }}>
                                <strong>Título:</strong>{' '}
                                <input
                                    type="text"
                                    value={ref.titulo}
                                    onChange={(e) => actualizarReferencia(index, 'titulo', e.target.value)}
                                    style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '11px', width: '70%' }}
                                />
                            </div>
                            <div>
                                <strong>Fuente:</strong>{' '}
                                <input
                                    type="text"
                                    value={ref.fuente}
                                    onChange={(e) => actualizarReferencia(index, 'fuente', e.target.value)}
                                    style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', fontSize: '11px', width: '70%' }}
                                />
                            </div>
                        </div>
                    ))}
                </div>
                <button onClick={agregarReferencia} style={{ marginTop: '10px', padding: '8px 16px', background: colores.primario, color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '12px' }}>+ Agregar Referencia</button>
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

export default EDITABLE_INFORME_EJECUTIVO;
