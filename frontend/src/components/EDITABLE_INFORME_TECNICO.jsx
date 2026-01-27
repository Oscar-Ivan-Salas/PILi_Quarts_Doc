import React, { useState, useEffect } from 'react';

/**
 * Componente Editable: Informe Técnico
 * Incluye: Resumen Ejecutivo, Introducción, Análisis Técnico, Conclusiones
 */
const EDITABLE_INFORME_TECNICO = ({
    datos = {},
    esquemaColores = 'azul-tesla',
    logoBase64 = null,
    fuenteDocumento = 'Calibri',
    onDatosChange = () => { }
}) => {

    const [datosEditables, setDatosEditables] = useState({
        codigo: datos.codigo || 'INF-TEC-001',
        fecha: datos.fecha || new Date().toLocaleDateString('es-PE'),
        cliente: { nombre: datos.cliente?.nombre || '' },
        titulo: datos.titulo || 'Informe Técnico',
        resumen_ejecutivo: datos.resumen_ejecutivo || 'Resumen ejecutivo del informe...',
        introduccion: datos.introduccion || 'Introducción y contexto del informe...',
        analisis_tecnico: datos.analisis_tecnico || 'Análisis técnico detallado...',
        resultados: datos.resultados || 'Resultados obtenidos...',
        conclusiones: datos.conclusiones || 'Conclusiones del análisis...',
        recomendaciones: datos.recomendaciones || ['Recomendación 1', 'Recomendación 2']
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
                <h1 style={{ fontSize: '30px', color: colores.primario, fontWeight: 'bold', marginBottom: '8px' }}>INFORME TÉCNICO</h1>
                <div style={{ fontSize: '16px', color: colores.secundario, fontWeight: '600', marginTop: '10px' }}>
                    <input
                        type="text"
                        value={datosEditables.titulo}
                        onChange={(e) => setDatosEditables({ ...datosEditables, titulo: e.target.value })}
                        style={{ border: 'none', borderBottom: `2px solid ${colores.acento}`, background: 'transparent', color: colores.secundario, fontWeight: '600', fontSize: '16px', width: '80%', textAlign: 'center' }}
                    />
                </div>
                <div style={{ fontSize: '14px', color: colores.secundario, marginTop: '10px' }}>
                    Código: <input type="text" value={datosEditables.codigo} onChange={(e) => setDatosEditables({ ...datosEditables, codigo: e.target.value })} style={{ border: 'none', borderBottom: `1px solid ${colores.acento}`, background: 'transparent', color: colores.secundario, fontSize: '14px', width: '150px', textAlign: 'center' }} />
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
                </div>
                <div style={{ padding: '15px', border: `2px solid ${colores.claroBorde}`, borderRadius: '6px', background: '#F9FAFB' }}>
                    <h3 style={{ fontSize: '14px', color: colores.primario, fontWeight: 'bold', marginBottom: '10px', textTransform: 'uppercase', borderBottom: `2px solid ${colores.primario}`, paddingBottom: '5px' }}>Datos del Informe</h3>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colores.secundario }}>Fecha:</strong> {datosEditables.fecha}</p>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colores.secundario }}>Código:</strong> {datosEditables.codigo}</p>
                </div>
            </div>

            {/* RESUMEN EJECUTIVO */}
            <div style={{ margin: '30px 0', padding: '25px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderLeft: `6px solid ${colores.primario}`, borderRadius: '4px' }}>
                <h3 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', textTransform: 'uppercase' }}>Resumen Ejecutivo</h3>
                <textarea
                    value={datosEditables.resumen_ejecutivo}
                    onChange={(e) => setDatosEditables({ ...datosEditables, resumen_ejecutivo: e.target.value })}
                    style={{ width: '100%', minHeight: '100px', fontSize: '13px', color: '#374151', lineHeight: '1.8', textAlign: 'justify', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px', background: 'white' }}
                />
            </div>

            {/* 1. INTRODUCCIÓN */}
            <div style={{ margin: '35px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>1. INTRODUCCIÓN</h2>
                <textarea
                    value={datosEditables.introduccion}
                    onChange={(e) => setDatosEditables({ ...datosEditables, introduccion: e.target.value })}
                    style={{ width: '100%', minHeight: '150px', fontSize: '12px', color: '#374151', lineHeight: '1.8', textAlign: 'justify', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px' }}
                />
            </div>

            {/* 2. ANÁLISIS TÉCNICO */}
            <div style={{ margin: '35px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>2. ANÁLISIS TÉCNICO</h2>
                <textarea
                    value={datosEditables.analisis_tecnico}
                    onChange={(e) => setDatosEditables({ ...datosEditables, analisis_tecnico: e.target.value })}
                    style={{ width: '100%', minHeight: '200px', fontSize: '12px', color: '#374151', lineHeight: '1.8', textAlign: 'justify', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px' }}
                />
            </div>

            {/* 3. RESULTADOS */}
            <div style={{ margin: '35px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>3. RESULTADOS</h2>
                <textarea
                    value={datosEditables.resultados}
                    onChange={(e) => setDatosEditables({ ...datosEditables, resultados: e.target.value })}
                    style={{ width: '100%', minHeight: '150px', fontSize: '12px', color: '#374151', lineHeight: '1.8', textAlign: 'justify', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px' }}
                />
            </div>

            {/* CONCLUSIONES */}
            <div style={{ margin: '30px 0' }}>
                <div style={{ padding: '25px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderLeft: `6px solid ${colores.primario}`, borderRadius: '4px' }}>
                    <h3 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px' }}>CONCLUSIONES</h3>
                    <textarea
                        value={datosEditables.conclusiones}
                        onChange={(e) => setDatosEditables({ ...datosEditables, conclusiones: e.target.value })}
                        style={{ width: '100%', minHeight: '150px', fontSize: '12px', color: '#374151', lineHeight: '1.6', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px', background: 'white' }}
                    />
                </div>
            </div>

            {/* RECOMENDACIONES */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '20px', color: colores.primario, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colores.primario}` }}>RECOMENDACIONES</h2>
                <ul style={{ listStyle: 'none', padding: 0 }}>
                    {datosEditables.recomendaciones.map((rec, i) => (
                        <li key={i} style={{ fontSize: '12px', color: '#374151', margin: '12px 0', paddingLeft: '30px', position: 'relative', lineHeight: '1.6' }}>
                            <span style={{ position: 'absolute', left: '10px', color: colores.primario, fontSize: '16px' }}>●</span>
                            {rec}
                        </li>
                    ))}
                </ul>
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

export default EDITABLE_INFORME_TECNICO;
