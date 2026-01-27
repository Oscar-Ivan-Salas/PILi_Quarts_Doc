import React, { useState, useEffect } from 'react';

const EDITABLE_PROYECTO_SIMPLE = ({ datos = {}, esquemaColores = 'azul-tesla', logoBase64 = null, fuenteDocumento = 'Calibri', onDatosChange = () => { } }) => {
    const [datosEditables, setDatosEditables] = useState({
        nombre_proyecto: datos.nombre_proyecto || 'Proyecto de Instalación Eléctrica',
        codigo_proyecto: datos.codigo_proyecto || 'PROY-001',
        cliente: datos.cliente || '',
        duracion_total: datos.duracion_total || 45,
        fecha_inicio: datos.fecha_inicio || new Date().toLocaleDateString('es-PE'),
        fecha_fin: datos.fecha_fin || '',
        presupuesto: datos.presupuesto || '25,000',
        alcance_proyecto: datos.alcance_proyecto || '',
        normativa_aplicable: datos.normativa_aplicable || 'CNE - Código Nacional de Electricidad',
        fases: datos.fases || [
            { numero: 1, nombre: 'Inicio y Planificación', duracion: 5, actividades: ['Levantamiento de información', 'Elaboración de propuesta técnica', 'Aprobación de alcance y presupuesto'], entregable: 'Plan de proyecto aprobado' },
            { numero: 2, nombre: 'Ingeniería y Diseño', duracion: 10, actividades: ['Cálculos técnicos según normativa', 'Elaboración de planos', 'Metrados y especificaciones'], entregable: 'Expediente técnico' },
            { numero: 3, nombre: 'Ejecución', duracion: 20, actividades: ['Adquisición de materiales', 'Instalación y montaje', 'Supervisión técnica'], entregable: 'Obra ejecutada' },
            { numero: 4, nombre: 'Pruebas y Puesta en Marcha', duracion: 5, actividades: ['Pruebas de funcionamiento', 'Ajustes y calibraciones', 'Capacitación'], entregable: 'Sistema operativo' },
            { numero: 5, nombre: 'Cierre', duracion: 3, actividades: ['Documentación as-built', 'Entrega de garantías', 'Acta de conformidad'], entregable: 'Proyecto cerrado' }
        ],
        recursos: datos.recursos || [
            { rol: 'Jefe de Proyecto', cantidad: 1, dedicacion: '25%', responsabilidad: 'Coordinación general' },
            { rol: 'Ingeniero Residente', cantidad: 1, dedicacion: '100%', responsabilidad: 'Ejecución técnica' },
            { rol: 'Técnicos Instaladores', cantidad: 3, dedicacion: '100%', responsabilidad: 'Instalación' },
            { rol: 'Inspector de Calidad', cantidad: 1, dedicacion: '50%', responsabilidad: 'Control de calidad' }
        ],
        riesgos: datos.riesgos || [
            { descripcion: 'Retrasos en entrega de materiales', probabilidad: 'Media', impacto: 'Alto', mitigacion: 'Compra anticipada' },
            { descripcion: 'Condiciones climáticas adversas', probabilidad: 'Baja', impacto: 'Medio', mitigacion: 'Programación flexible' },
            { descripcion: 'Cambios en alcance', probabilidad: 'Media', impacto: 'Alto', mitigacion: 'Control de cambios' }
        ]
    });

    const COLORES = {
        'azul-tesla': { primario: '#0052A3', secundario: '#1E40AF', acento: '#3B82F6', claro: '#EFF6FF', claroBorde: '#DBEAFE' },
        'rojo-energia': { primario: '#8B0000', secundario: '#991B1B', acento: '#DC2626', claro: '#FEF2F2', claroBorde: '#FECACA' },
        'verde-ecologico': { primario: '#27AE60', secundario: '#16A34A', acento: '#22C55E', claro: '#F0FDF4', claroBorde: '#BBF7D0' },
        'dorado-premium': { primario: '#D4AF37', secundario: '#B8860B', acento: '#FFD700', claro: '#FFFBEB', claroBorde: '#FDE68A' }
    };
    const colores = COLORES[esquemaColores] || COLORES['azul-tesla'];

    useEffect(() => { onDatosChange(datosEditables); }, [datosEditables]);

    const getBadgeStyle = (nivel) => {
        const styles = {
            'Alta': { background: '#FEE2E2', color: '#991B1B' },
            'Media': { background: '#FEF3C7', color: '#92400E' },
            'Baja': { background: '#D1FAE5', color: '#065F46' },
            'Alto': { background: '#FEE2E2', color: '#991B1B' },
            'Medio': { background: '#FEF3C7', color: '#92400E' },
            'Bajo': { background: '#D1FAE5', color: '#065F46' }
        };
        return styles[nivel] || styles['Media'];
    };

    return (
        <div style={{ fontFamily: fuenteDocumento, maxWidth: '210mm', margin: '0 auto', padding: '20mm', background: 'white', color: '#1f2937', lineHeight: '1.6' }}>
            {/* HEADER */}
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '30px', paddingBottom: '20px', borderBottom: `4px solid ${colores.primario}` }}>
                <div>
                    {logoBase64 ? <img src={logoBase64} alt="Logo" style={{ width: '180px', height: '80px', objectFit: 'contain', borderRadius: '8px' }} /> :
                        <div style={{ width: '180px', height: '80px', background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold', fontSize: '24px' }}>TESLA</div>}
                    <p style={{ fontSize: '10px', color: '#6B7280', marginTop: '10px' }}>Electricidad y Automatización</p>
                </div>
                <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '20px', fontWeight: 'bold', color: colores.primario, marginBottom: '8px' }}>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
                    <div style={{ fontSize: '11px', color: '#4b5563' }}>
                        <div>RUC: 20601138787</div><div>Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div><div>Teléfono: 906 315 961 | Email: ingenieria.teslaelectricidad@gmail.com</div>
                    </div>
                </div>
            </div>

            {/* TÍTULO */}
            <div style={{ textAlign: 'center', margin: '30px 0', padding: '25px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderLeft: `6px solid ${colores.primario}` }}>
                <h1 style={{ fontSize: '28px', color: colores.primario, marginBottom: '10px' }}>PLAN DE PROYECTO</h1>
                <div style={{ fontSize: '18px', color: colores.secundario, margin: '10px 0' }}>
                    <input type="text" value={datosEditables.nombre_proyecto} onChange={(e) => setDatosEditables({ ...datosEditables, nombre_proyecto: e.target.value })} style={{ border: 'none', borderBottom: `2px solid ${colores.acento}`, background: 'transparent', color: colores.secundario, fontSize: '18px', textAlign: 'center', width: '80%' }} />
                </div>
                <div style={{ fontSize: '16px', color: colores.secundario, fontWeight: '600' }}>
                    CÓDIGO: <input type="text" value={datosEditables.codigo_proyecto} onChange={(e) => setDatosEditables({ ...datosEditables, codigo_proyecto: e.target.value })} style={{ border: 'none', borderBottom: `2px solid ${colores.acento}`, background: 'transparent', color: colores.secundario, fontSize: '16px', width: '150px' }} />
                </div>
            </div>

            {/* INFO GRID (4 CARDS) */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '15px', margin: '25px 0' }}>
                {[
                    { label: 'Cliente', value: datosEditables.cliente, field: 'cliente' },
                    { label: 'Duración', value: `${datosEditables.duracion_total} días`, field: 'duracion_total' },
                    { label: 'Inicio', value: datosEditables.fecha_inicio, field: 'fecha_inicio' },
                    { label: 'Fin Estimado', value: datosEditables.fecha_fin, field: 'fecha_fin' }
                ].map((card, i) => (
                    <div key={i} style={{ padding: '15px', background: '#F9FAFB', borderLeft: '4px solid #3B82F6', borderRadius: '4px' }}>
                        <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: '600', textTransform: 'uppercase', marginBottom: '5px' }}>{card.label}</div>
                        <div style={{ fontSize: '16px', color: colores.primario, fontWeight: 'bold' }}>
                            <input type="text" value={card.value} onChange={(e) => setDatosEditables({ ...datosEditables, [card.field]: e.target.value })} style={{ width: '100%', border: 'none', background: 'transparent', color: colores.primario, fontWeight: 'bold', fontSize: '14px' }} />
                        </div>
                    </div>
                ))}
            </div>

            {/* PRESUPUESTO DESTACADO */}
            <div style={{ textAlign: 'center', padding: '20px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderRadius: '6px', margin: '20px 0' }}>
                <div style={{ fontSize: '12px', color: '#6B7280', marginBottom: '5px' }}>PRESUPUESTO ESTIMADO</div>
                <div style={{ fontSize: '32px', color: colores.primario, fontWeight: 'bold' }}>
                    $ <input type="text" value={datosEditables.presupuesto} onChange={(e) => setDatosEditables({ ...datosEditables, presupuesto: e.target.value })} style={{ width: '200px', border: 'none', background: 'transparent', color: colores.primario, fontWeight: 'bold', fontSize: '32px', textAlign: 'center' }} />
                </div>
            </div>

            {/* ALCANCE DEL PROYECTO */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Alcance del Proyecto
                </h2>
                <div style={{ padding: '15px', background: '#F9FAFB', borderLeft: `4px solid ${colores.acento}`, fontSize: '12px', lineHeight: '1.8' }}>
                    <textarea value={datosEditables.alcance_proyecto} onChange={(e) => setDatosEditables({ ...datosEditables, alcance_proyecto: e.target.value })} style={{ width: '100%', minHeight: '100px', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px', fontSize: '12px' }} placeholder="Descripción del alcance del proyecto..." />
                </div>
            </div>

            {/* FASES DEL PROYECTO (5 FASES DETALLADAS) */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Fases del Proyecto
                </h2>
                <div style={{ margin: '20px 0' }}>
                    {datosEditables.fases.map((fase, index) => (
                        <div key={index} style={{ marginBottom: '25px', padding: '20px', background: '#F9FAFB', borderLeft: `6px solid ${colores.primario}`, borderRadius: '4px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                                <div style={{ fontSize: '16px', color: colores.primario, fontWeight: 'bold' }}>
                                    {fase.numero}. <input type="text" value={fase.nombre} onChange={(e) => {
                                        const nuevasFases = [...datosEditables.fases];
                                        nuevasFases[index].nombre = e.target.value;
                                        setDatosEditables({ ...datosEditables, fases: nuevasFases });
                                    }} style={{ border: 'none', background: 'transparent', color: colores.primario, fontWeight: 'bold', fontSize: '16px', width: '70%' }} />
                                </div>
                                <div style={{ padding: '5px 15px', background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, color: 'white', borderRadius: '20px', fontSize: '12px', fontWeight: '600' }}>
                                    <input type="number" value={fase.duracion} onChange={(e) => {
                                        const nuevasFases = [...datosEditables.fases];
                                        nuevasFases[index].duracion = e.target.value;
                                        setDatosEditables({ ...datosEditables, fases: nuevasFases });
                                    }} style={{ width: '40px', border: 'none', background: 'transparent', color: 'white', fontWeight: '600', fontSize: '12px', textAlign: 'center' }} /> días
                                </div>
                            </div>
                            <div style={{ margin: '15px 0' }}>
                                <h4 style={{ fontSize: '13px', color: colores.secundario, marginBottom: '10px', fontWeight: '600' }}>Actividades:</h4>
                                <ul style={{ listStyle: 'none', padding: 0 }}>
                                    {fase.actividades.map((act, i) => (
                                        <li key={i} style={{ fontSize: '12px', color: '#374151', margin: '8px 0', paddingLeft: '25px', position: 'relative' }}>
                                            <span style={{ position: 'absolute', left: 0, color: colores.acento, fontSize: '10px' }}>▶</span>{act}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            <div style={{ marginTop: '15px', padding: '12px', background: 'white', border: `2px dashed ${colores.acento}`, borderRadius: '4px', fontSize: '12px' }}>
                                <strong style={{ color: colores.primario }}>Entregable:</strong> {fase.entregable}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* RECURSOS ASIGNADOS (GRID 4 CARDS) */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Recursos Asignados
                </h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px', margin: '20px 0' }}>
                    {datosEditables.recursos.map((recurso, i) => (
                        <div key={i} style={{ padding: '15px', background: 'white', border: `2px solid ${colores.claroBorde}`, borderRadius: '6px' }}>
                            <div style={{ fontSize: '14px', color: colores.primario, fontWeight: 'bold', marginBottom: '8px' }}>{recurso.rol}</div>
                            <div style={{ fontSize: '11px', color: '#374151', margin: '5px 0' }}><strong style={{ color: colores.secundario }}>Cantidad:</strong> {recurso.cantidad}</div>
                            <div style={{ fontSize: '11px', color: '#374151', margin: '5px 0' }}><strong style={{ color: colores.secundario }}>Dedicación:</strong> {recurso.dedicacion}</div>
                            <div style={{ fontSize: '11px', color: '#374151', margin: '5px 0' }}><strong style={{ color: colores.secundario }}>Responsabilidad:</strong> {recurso.responsabilidad}</div>
                        </div>
                    ))}
                </div>
            </div>

            {/* ANÁLISIS DE RIESGOS (TABLA CON BADGES) */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Análisis de Riesgos
                </h2>
                <table style={{ width: '100%', borderCollapse: 'collapse', margin: '15px 0' }}>
                    <thead style={{ background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, color: 'white' }}>
                        <tr>
                            <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', fontWeight: '700', width: '40%' }}>Riesgo</th>
                            <th style={{ padding: '12px', textAlign: 'center', fontSize: '12px', fontWeight: '700', width: '15%' }}>Probabilidad</th>
                            <th style={{ padding: '12px', textAlign: 'center', fontSize: '12px', fontWeight: '700', width: '15%' }}>Impacto</th>
                            <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', fontWeight: '700', width: '30%' }}>Mitigación</th>
                        </tr>
                    </thead>
                    <tbody>
                        {datosEditables.riesgos.map((riesgo, i) => (
                            <tr key={i} style={{ background: i % 2 === 0 ? '#F9FAFB' : 'white', borderBottom: '1px solid #E5E7EB' }}>
                                <td style={{ padding: '10px 12px', fontSize: '11px' }}>{riesgo.descripcion}</td>
                                <td style={{ padding: '10px 12px', textAlign: 'center' }}>
                                    <span style={{ padding: '4px 10px', borderRadius: '12px', fontSize: '10px', fontWeight: '600', display: 'inline-block', ...getBadgeStyle(riesgo.probabilidad) }}>
                                        {riesgo.probabilidad}
                                    </span>
                                </td>
                                <td style={{ padding: '10px 12px', textAlign: 'center' }}>
                                    <span style={{ padding: '4px 10px', borderRadius: '12px', fontSize: '10px', fontWeight: '600', display: 'inline-block', ...getBadgeStyle(riesgo.impacto) }}>
                                        {riesgo.impacto}
                                    </span>
                                </td>
                                <td style={{ padding: '10px 12px', fontSize: '11px' }}>{riesgo.mitigacion}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* ENTREGABLES PRINCIPALES (GRID 3x2) */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '18px', color: colores.primario, marginBottom: '15px', paddingBottom: '8px', borderBottom: `3px solid ${colores.primario}`, display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ width: '6px', height: '24px', background: colores.acento }}></span>Entregables Principales
                </h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', margin: '20px 0' }}>
                    {[
                        { icon: '📋', nombre: 'Plan de proyecto' },
                        { icon: '📐', nombre: 'Planos de instalación' },
                        { icon: '📄', nombre: 'Especificaciones técnicas' },
                        { icon: '🧮', nombre: 'Memoria de cálculo' },
                        { icon: '✅', nombre: 'Protocolos de pruebas' },
                        { icon: '🏗️', nombre: 'Planos as-built' },
                        { icon: '🛡️', nombre: 'Certificados de garantía' }
                    ].map((entregable, i) => (
                        <div key={i} style={{ padding: '15px', background: 'white', border: `2px solid ${colores.claroBorde}`, borderRadius: '6px', textAlign: 'center' }}>
                            <div style={{ fontSize: '32px', marginBottom: '10px' }}>{entregable.icon}</div>
                            <div style={{ fontSize: '11px', color: '#374151', fontWeight: '600' }}>{entregable.nombre}</div>
                        </div>
                    ))}
                </div>
            </div>

            {/* NORMATIVA APLICABLE */}
            <div style={{ padding: '15px', background: '#F9FAFB', borderLeft: `4px solid ${colores.primario}`, margin: '25px 0' }}>
                <div style={{ fontSize: '12px', color: '#6B7280', marginBottom: '5px' }}>NORMATIVA APLICABLE</div>
                <div style={{ fontSize: '14px', color: colores.primario, fontWeight: 'bold' }}>
                    <input type="text" value={datosEditables.normativa_aplicable} onChange={(e) => setDatosEditables({ ...datosEditables, normativa_aplicable: e.target.value })} style={{ width: '100%', border: 'none', background: 'transparent', color: colores.primario, fontWeight: 'bold', fontSize: '14px' }} />
                </div>
            </div>

            {/* FOOTER */}
            <div style={{ marginTop: '40px', paddingTop: '20px', borderTop: `3px solid ${colores.primario}`, textAlign: 'center', fontSize: '10px', color: '#6B7280' }}>
                <div style={{ fontWeight: 'bold', color: colores.primario, fontSize: '12px', marginBottom: '8px' }}>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
                <div>RUC: 20601138787 | Teléfono: 906 315 961 | Email: ingenieria.teslaelectricidad@gmail.com</div>
            </div>
        </div>
    );
};

export default EDITABLE_PROYECTO_SIMPLE;
