import React, { useState, useEffect } from 'react';

const EDITABLE_INFORME_EJECUTIVO = ({ datos = {}, esquemaColores = 'azul-tesla', logoBase64 = null, fuenteDocumento = 'Times New Roman', onDatosChange = () => { } }) => {
    const [datosEditables, setDatosEditables] = useState({
        titulo_proyecto: datos.titulo_proyecto || 'SISTEMA DE INSTALACIÓN ELÉCTRICA INDUSTRIAL',
        cliente: datos.cliente || '',
        fecha: datos.fecha || new Date().toLocaleDateString('es-PE'),
        codigo_informe: datos.codigo_informe || 'INF-EJ-001',
        resumen_ejecutivo: datos.resumen_ejecutivo || '',
        presupuesto: datos.presupuesto || '50,000',
        roi_estimado: datos.roi_estimado || '45',
        payback_meses: datos.payback_meses || '18',
        tir_proyectada: datos.tir_proyectada || '35',
        ahorro_anual_k: datos.ahorro_anual_k || '15',
        contexto_organizacional: datos.contexto_organizacional || '',
        inversion_equipos: datos.inversion_equipos || '35,000',
        inversion_mano_obra: datos.inversion_mano_obra || '10,000',
        capital_trabajo: datos.capital_trabajo || '5,000',
        ahorro_energetico: datos.ahorro_energetico || '8,000',
        servicio_nombre: datos.servicio_nombre || 'Instalaciones Eléctricas',
        normativa_aplicable: datos.normativa_aplicable || 'CNE - Código Nacional de Electricidad',
        referencias: datos.referencias || [
            'Ministerio de Energía y Minas. (2011). CNE - Código Nacional de Electricidad. Lima, Perú.',
            'Project Management Institute. (2021). A guide to the project management body of knowledge (PMBOK® guide) (7th ed.).',
            'Reglamento Nacional de Edificaciones. (2023). Norma técnica de edificación. Lima: Ministerio de Vivienda.',
            'Tesla Electricidad y Automatización S.A.C. (2024). Especificaciones técnicas y estándares de calidad. Lima, Perú.'
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

    return (
        <div style={{ fontFamily: fuenteDocumento, color: '#000000', lineHeight: '2.0', background: '#ffffff', fontSize: '12pt' }}>
            {/* PORTADA APA */}
            <div style={{ textAlign: 'center', padding: '100px 40px', minHeight: '280mm', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', maxWidth: '210mm', margin: '0 auto' }}>
                <div style={{ marginTop: '80px' }}>
                    <h1 style={{ fontSize: '14pt', color: '#000000', fontWeight: 'bold', margin: '40px 0', lineHeight: '2.0' }}>
                        INFORME EJECUTIVO:<br />
                        ANÁLISIS DE VIABILIDAD DEL PROYECTO<br />
                        <input type="text" value={datosEditables.titulo_proyecto} onChange={(e) => setDatosEditables({ ...datosEditables, titulo_proyecto: e.target.value })} style={{ width: '90%', border: 'none', borderBottom: '2px solid #ccc', background: 'transparent', fontSize: '14pt', textAlign: 'center', marginTop: '10px' }} />
                    </h1>
                </div>
                <div>
                    <div style={{ fontWeight: 'bold', marginBottom: '10px' }}>Elaborado para:</div>
                    <div><input type="text" value={datosEditables.cliente} onChange={(e) => setDatosEditables({ ...datosEditables, cliente: e.target.value })} style={{ width: '60%', border: 'none', borderBottom: '1px solid #ccc', background: 'transparent', textAlign: 'center' }} /></div>
                    <div style={{ marginTop: '40px', fontWeight: 'bold' }}>Preparado por:</div>
                    <div>Tesla Electricidad y Automatización S.A.C.</div>
                    <div>Departamento de Gestión de Proyectos</div>
                    <div style={{ marginTop: '40px' }}>{datosEditables.fecha}</div>
                    <div style={{ marginTop: '20px', fontSize: '10pt', color: '#6B7280' }}>Código del Informe: {datosEditables.codigo_informe}</div>
                </div>
            </div>
            <div style={{ pageBreakAfter: 'always' }}></div>

            {/* CONTENIDO PRINCIPAL */}
            <div style={{ maxWidth: '210mm', margin: '0 auto', padding: '25mm', background: 'white' }}>
                {/* HEADER */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px', paddingBottom: '15px', borderBottom: `3px solid ${colores.primario}` }}>
                    <div>
                        {logoBase64 ? <img src={logoBase64} alt="Logo" style={{ width: '160px', height: '70px', objectFit: 'contain', borderRadius: '6px' }} /> :
                            <div style={{ width: '160px', height: '70px', background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, borderRadius: '6px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold', fontSize: '22px' }}>TESLA</div>}
                        <p style={{ fontSize: '9pt', color: '#6B7280', fontFamily: 'Calibri, sans-serif' }}>Electricidad y Automatización</p>
                    </div>
                    <div style={{ textAlign: 'right', fontSize: '10pt', color: '#4b5563' }}>
                        <div style={{ fontSize: '14pt', fontWeight: 'bold', color: colores.primario, marginBottom: '8px' }}>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
                        <div>RUC: 20601138787</div><div>Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div><div>Email: ingenieria.teslaelectricidad@gmail.com</div>
                    </div>
                </div>

                {/* EXECUTIVE SUMMARY */}
                <div style={{ padding: '30px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderLeft: `8px solid ${colores.primario}`, borderRadius: '6px', margin: '30px 0' }}>
                    <h2 style={{ fontSize: '16pt', color: colores.primario, marginBottom: '20px', fontWeight: 'bold', textAlign: 'center', textTransform: 'uppercase' }}>Executive Summary</h2>
                    <textarea value={datosEditables.resumen_ejecutivo} onChange={(e) => setDatosEditables({ ...datosEditables, resumen_ejecutivo: e.target.value })} style={{ width: '100%', minHeight: '120px', fontSize: '11pt', color: '#1f2937', lineHeight: '1.8', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '15px', fontFamily: 'Calibri, Arial, sans-serif' }} placeholder="Resumen ejecutivo del proyecto..." />
                    <div style={{ marginTop: '25px' }}>
                        <p style={{ fontFamily: 'Calibri, sans-serif' }}><strong style={{ color: colores.primario }}>Hallazgos Principales:</strong></p>
                        <ul style={{ fontFamily: 'Calibri, sans-serif', marginTop: '10px' }}>
                            <li>Inversión requerida: $ {datosEditables.presupuesto}</li>
                            <li>ROI estimado: {datosEditables.roi_estimado}%</li>
                            <li>Período de retorno: {datosEditables.payback_meses} meses</li>
                            <li>TIR proyectada: {datosEditables.tir_proyectada}%</li>
                        </ul>
                        <p style={{ marginTop: '15px', fontFamily: 'Calibri, sans-serif' }}><strong style={{ color: colores.primario }}>Recomendación:</strong></p>
                        <p style={{ fontFamily: 'Calibri, sans-serif' }}>Se recomienda aprobar el proyecto dada su alta viabilidad técnica y financiera.</p>
                    </div>
                </div>

                {/* PRESUPUESTO DESTACADO */}
                <div style={{ textAlign: 'center', padding: '30px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderRadius: '8px', margin: '25px 0' }}>
                    <div style={{ fontSize: '11pt', color: '#6B7280', marginBottom: '10px', fontFamily: 'Calibri, sans-serif' }}>INVERSIÓN TOTAL REQUERIDA</div>
                    <div style={{ fontSize: '40pt', color: colores.primario, fontWeight: 'bold', fontFamily: 'Calibri, sans-serif' }}>
                        $ <input type="text" value={datosEditables.presupuesto} onChange={(e) => setDatosEditables({ ...datosEditables, presupuesto: e.target.value })} style={{ width: '250px', border: 'none', background: 'transparent', color: colores.primario, fontWeight: 'bold', fontSize: '40pt', textAlign: 'center' }} />
                    </div>
                </div>

                {/* SECCIÓN 1: ANÁLISIS DE SITUACIÓN */}
                <div style={{ margin: '40px 0' }}>
                    <h2 style={{ fontSize: '14pt', color: colores.primario, fontWeight: 'bold', margin: '25px 0 15px 0', paddingBottom: '8px', borderBottom: `2px solid ${colores.primario}` }}>1. Análisis de Situación</h2>
                    <h3 style={{ fontSize: '12pt', color: colores.secundario, fontWeight: 'bold', margin: '20px 0 10px 0' }}>1.1. Contexto Organizacional</h3>
                    <textarea value={datosEditables.contexto_organizacional} onChange={(e) => setDatosEditables({ ...datosEditables, contexto_organizacional: e.target.value })} style={{ width: '100%', minHeight: '80px', fontSize: '11pt', border: `1px solid ${colores.claroBorde}`, borderRadius: '4px', padding: '10px', fontFamily: 'Calibri, sans-serif' }} placeholder="Contexto organizacional del proyecto..." />

                    <h3 style={{ fontSize: '12pt', color: colores.secundario, fontWeight: 'bold', margin: '20px 0 10px 0' }}>1.2. Problemática Identificada</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px', margin: '25px 0' }}>
                        {[
                            { titulo: 'Equipos Obsoletos', texto: 'Sistemas actuales con tecnología desactualizada que requieren reemplazo' },
                            { titulo: 'Incumplimiento Normativo', texto: 'Necesidad de actualización para cumplir con regulaciones actuales' },
                            { titulo: 'Ineficiencia Operativa', texto: 'Costos operativos elevados por falta de optimización' }
                        ].map((hallazgo, i) => (
                            <div key={i} style={{ padding: '20px', background: '#F9FAFB', borderLeft: `5px solid ${colores.acento}`, borderRadius: '6px' }}>
                                <div style={{ fontSize: '11pt', color: colores.primario, fontWeight: 'bold', marginBottom: '10px', fontFamily: 'Calibri, sans-serif' }}>{hallazgo.titulo}</div>
                                <div style={{ fontSize: '10pt', color: '#374151', lineHeight: '1.6', fontFamily: 'Calibri, sans-serif' }}>{hallazgo.texto}</div>
                            </div>
                        ))}
                    </div>

                    <h3 style={{ fontSize: '12pt', color: colores.secundario, fontWeight: 'bold', margin: '20px 0 10px 0' }}>1.3. Oportunidades de Mejora</h3>
                    <ul style={{ margin: '15px 0', paddingLeft: '40px', fontFamily: 'Calibri, sans-serif' }}>
                        <li style={{ fontSize: '11pt', margin: '10px 0', lineHeight: '1.8' }}>Reducción significativa de costos operativos mediante modernización</li>
                        <li style={{ fontSize: '11pt', margin: '10px 0', lineHeight: '1.8' }}>Mejora en los índices de seguridad y confiabilidad del sistema</li>
                        <li style={{ fontSize: '11pt', margin: '10px 0', lineHeight: '1.8' }}>Cumplimiento total de la normativa {datosEditables.normativa_aplicable}</li>
                        <li style={{ fontSize: '11pt', margin: '10px 0', lineHeight: '1.8' }}>Incremento de la eficiencia energética y operativa</li>
                    </ul>
                </div>

                {/* SECCIÓN 2: MÉTRICAS Y KPIs */}
                <div style={{ margin: '40px 0' }}>
                    <h2 style={{ fontSize: '14pt', color: colores.primario, fontWeight: 'bold', margin: '25px 0 15px 0', paddingBottom: '8px', borderBottom: `2px solid ${colores.primario}` }}>2. Métricas y Indicadores Clave de Desempeño</h2>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', margin: '25px 0' }}>
                        {[
                            { label: 'ROI Estimado', value: `${datosEditables.roi_estimado}%`, desc: 'Retorno de Inversión', field: 'roi_estimado' },
                            { label: 'Payback', value: datosEditables.payback_meses, desc: 'Meses de recuperación', field: 'payback_meses' },
                            { label: 'TIR', value: `${datosEditables.tir_proyectada}%`, desc: 'Tasa Interna de Retorno', field: 'tir_proyectada' },
                            { label: 'Ahorro Anual', value: `$ ${datosEditables.ahorro_anual_k}K`, desc: 'Proyección de ahorro', field: 'ahorro_anual_k' }
                        ].map((metrica, i) => (
                            <div key={i} style={{ padding: '25px', background: 'white', border: `2px solid ${colores.claroBorde}`, borderRadius: '8px', textAlign: 'center', boxShadow: '0 2px 8px rgba(0, 82, 163, 0.1)' }}>
                                <div style={{ fontSize: '10pt', color: '#6B7280', fontWeight: '600', marginBottom: '10px', fontFamily: 'Calibri, sans-serif' }}>{metrica.label}</div>
                                <div style={{ fontSize: '28pt', color: colores.primario, fontWeight: 'bold', fontFamily: 'Calibri, sans-serif' }}>
                                    <input type="text" value={metrica.value} onChange={(e) => setDatosEditables({ ...datosEditables, [metrica.field]: e.target.value.replace(/[^0-9]/g, '') })} style={{ width: '100%', border: 'none', background: 'transparent', color: colores.primario, fontWeight: 'bold', fontSize: '28pt', textAlign: 'center' }} />
                                </div>
                                <div style={{ fontSize: '9pt', color: '#9CA3AF', marginTop: '8px', fontFamily: 'Calibri, sans-serif' }}>{metrica.desc}</div>
                            </div>
                        ))}
                    </div>

                    <h3 style={{ fontSize: '12pt', color: colores.secundario, fontWeight: 'bold', margin: '20px 0 10px 0' }}>2.1. Métricas de Eficiencia</h3>
                    <ul style={{ fontFamily: 'Calibri, sans-serif' }}>
                        <li style={{ fontSize: '11pt', margin: '10px 0', lineHeight: '1.8' }}>Reducción de costos operativos: 20%</li>
                        <li style={{ fontSize: '11pt', margin: '10px 0', lineHeight: '1.8' }}>Incremento de eficiencia: 35%</li>
                        <li style={{ fontSize: '11pt', margin: '10px 0', lineHeight: '1.8' }}>Ahorro energético anual proyectado: $ {datosEditables.ahorro_energetico}</li>
                        <li style={{ fontSize: '11pt', margin: '10px 0', lineHeight: '1.8' }}>Reducción de tiempos de mantenimiento: 40%</li>
                    </ul>
                </div>

                {/* SECCIÓN 3: ANÁLISIS FINANCIERO */}
                <div style={{ margin: '40px 0' }}>
                    <h2 style={{ fontSize: '14pt', color: colores.primario, fontWeight: 'bold', margin: '25px 0 15px 0', paddingBottom: '8px', borderBottom: `2px solid ${colores.primario}` }}>3. Análisis Financiero Detallado</h2>
                    <h3 style={{ fontSize: '12pt', color: colores.secundario, fontWeight: 'bold', margin: '20px 0 10px 0' }}>3.1. Inversión Requerida</h3>
                    <table style={{ width: '100%', borderCollapse: 'collapse', margin: '20px 0', fontFamily: 'Calibri, Arial, sans-serif' }}>
                        <thead style={{ background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, color: 'white' }}>
                            <tr>
                                <th style={{ padding: '12px', textAlign: 'left', fontSize: '11pt', fontWeight: '700' }}>Concepto</th>
                                <th style={{ padding: '12px', textAlign: 'right', fontSize: '11pt', fontWeight: '700' }}>Monto (USD)</th>
                                <th style={{ padding: '12px', textAlign: 'right', fontSize: '11pt', fontWeight: '700' }}>Porcentaje</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td style={{ padding: '10px 12px', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>Inversión en equipos y materiales</td><td style={{ padding: '10px 12px', textAlign: 'right', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>$ {datosEditables.inversion_equipos}</td><td style={{ padding: '10px 12px', textAlign: 'right', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>70%</td></tr>
                            <tr style={{ background: '#F9FAFB' }}><td style={{ padding: '10px 12px', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>Mano de obra e instalación</td><td style={{ padding: '10px 12px', textAlign: 'right', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>$ {datosEditables.inversion_mano_obra}</td><td style={{ padding: '10px 12px', textAlign: 'right', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>20%</td></tr>
                            <tr><td style={{ padding: '10px 12px', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>Capital de trabajo y contingencias</td><td style={{ padding: '10px 12px', textAlign: 'right', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>$ {datosEditables.capital_trabajo}</td><td style={{ padding: '10px 12px', textAlign: 'right', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>10%</td></tr>
                            <tr style={{ background: colores.claro, fontWeight: 'bold' }}><td style={{ padding: '10px 12px', fontSize: '10pt' }}>TOTAL INVERSIÓN</td><td style={{ padding: '10px 12px', textAlign: 'right', color: colores.primario, fontSize: '10pt' }}>$ {datosEditables.presupuesto}</td><td style={{ padding: '10px 12px', textAlign: 'right', fontSize: '10pt' }}>100%</td></tr>
                        </tbody>
                    </table>
                </div>

                {/* SECCIÓN 4: EVALUACIÓN DE RIESGOS */}
                <div style={{ margin: '40px 0' }}>
                    <h2 style={{ fontSize: '14pt', color: colores.primario, fontWeight: 'bold', margin: '25px 0 15px 0', paddingBottom: '8px', borderBottom: `2px solid ${colores.primario}` }}>4. Evaluación de Riesgos</h2>
                    <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'Calibri, sans-serif' }}>
                        <thead style={{ background: `linear-gradient(135deg, ${colores.primario} 0%, ${colores.secundario} 100%)`, color: 'white' }}>
                            <tr>
                                <th style={{ padding: '12px', textAlign: 'left', fontSize: '11pt' }}>Riesgo</th>
                                <th style={{ padding: '12px', textAlign: 'center', fontSize: '11pt' }}>Probabilidad</th>
                                <th style={{ padding: '12px', textAlign: 'center', fontSize: '11pt' }}>Impacto</th>
                                <th style={{ padding: '12px', textAlign: 'left', fontSize: '11pt' }}>Plan de Mitigación</th>
                            </tr>
                        </thead>
                        <tbody>
                            {[
                                { riesgo: 'Retrasos en entrega de equipos', prob: 'Media', imp: 'Alto', plan: 'Compra anticipada de equipos críticos' },
                                { riesgo: 'Variación de precios de materiales', prob: 'Media', imp: 'Medio', plan: 'Cláusulas de precio fijo en contratos' },
                                { riesgo: 'Cambios en el alcance del proyecto', prob: 'Alta', imp: 'Alto', plan: 'Control de cambios riguroso con aprobaciones' }
                            ].map((r, i) => (
                                <tr key={i} style={{ background: i % 2 === 0 ? 'white' : '#F9FAFB' }}>
                                    <td style={{ padding: '10px 12px', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>{r.riesgo}</td>
                                    <td style={{ padding: '10px 12px', textAlign: 'center', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>{r.prob}</td>
                                    <td style={{ padding: '10px 12px', textAlign: 'center', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>{r.imp}</td>
                                    <td style={{ padding: '10px 12px', fontSize: '10pt', borderBottom: '1px solid #E5E7EB' }}>{r.plan}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* GRÁFICOS SUGERIDOS */}
                <div style={{ padding: '25px', background: '#F9FAFB', border: `2px dashed ${colores.acento}`, borderRadius: '8px', margin: '25px 0' }}>
                    <h4 style={{ fontSize: '11pt', color: colores.primario, fontWeight: 'bold', marginBottom: '15px', fontFamily: 'Calibri, sans-serif' }}>📊 Gráficos Recomendados para Presentación Ejecutiva</h4>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px' }}>
                        {[
                            { icon: '📊', texto: 'Dashboard ejecutivo de KPIs' },
                            { icon: '💰', texto: 'Análisis de ROI y payback' },
                            { icon: '📅', texto: 'Diagrama de Gantt' },
                            { icon: '⚠️', texto: 'Matriz de riesgos' },
                            { icon: '📈', texto: 'Flujo de caja proyectado' },
                            { icon: '🔄', texto: 'Comparativa de escenarios' }
                        ].map((grafico, i) => (
                            <div key={i} style={{ padding: '15px', background: 'white', border: `1px solid ${colores.claroBorde}`, borderRadius: '6px', textAlign: 'center', fontSize: '9pt', fontFamily: 'Calibri, sans-serif' }}>
                                <div style={{ fontSize: '28px', marginBottom: '8px' }}>{grafico.icon}</div>
                                <div>{grafico.texto}</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* CONCLUSIONES */}
                <div style={{ padding: '30px', background: `linear-gradient(135deg, ${colores.claro} 0%, ${colores.claroBorde} 100%)`, borderLeft: `8px solid ${colores.primario}`, borderRadius: '6px', margin: '30px 0' }}>
                    <h3 style={{ fontSize: '14pt', color: colores.primario, fontWeight: 'bold', marginBottom: '20px', textAlign: 'center' }}>CONCLUSIONES Y RECOMENDACIONES</h3>
                    <ul style={{ listStyle: 'none', padding: 0, fontFamily: 'Calibri, sans-serif' }}>
                        {[
                            `El proyecto es técnicamente viable según ${datosEditables.normativa_aplicable}`,
                            `El análisis financiero demuestra un ROI atractivo de ${datosEditables.roi_estimado}%`,
                            'Los riesgos identificados son manejables con los planes de mitigación propuestos',
                            'Se recomienda aprobación e implementación inmediata del proyecto',
                            'El proyecto generará valor significativo con beneficios cuantificables a corto y largo plazo'
                        ].map((conclusion, i) => (
                            <li key={i} style={{ fontSize: '11pt', color: '#1f2937', margin: '15px 0', paddingLeft: '30px', position: 'relative', lineHeight: '1.8' }}>
                                <span style={{ position: 'absolute', left: 0, color: colores.primario, fontWeight: 'bold', fontSize: '18pt' }}>✓</span>{conclusion}
                            </li>
                        ))}
                    </ul>
                </div>

                {/* BIBLIOGRAFÍA APA */}
                <div style={{ margin: '40px 0' }}>
                    <h2 style={{ fontSize: '14pt', color: '#000000', fontWeight: 'bold', marginBottom: '20px', textAlign: 'center' }}>Referencias</h2>
                    {datosEditables.referencias.map((ref, i) => (
                        <div key={i} style={{ fontSize: '11pt', color: '#1f2937', lineHeight: '2.0', marginLeft: '40px', textIndent: '-40px', marginBottom: '15px', fontFamily: 'Times New Roman, serif' }}>{ref}</div>
                    ))}
                </div>

                {/* FOOTER */}
                <div style={{ marginTop: '50px', paddingTop: '20px', borderTop: `3px solid ${colores.primario}`, textAlign: 'center', fontSize: '9pt', color: '#6B7280', fontFamily: 'Calibri, sans-serif' }}>
                    <div style={{ fontWeight: 'bold', color: colores.primario, fontSize: '11pt', marginBottom: '8px' }}>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
                    <div>RUC: 20601138787 | Teléfono: 906 315 961 | Email: ingenieria.teslaelectricidad@gmail.com</div>
                    <div>Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div>
                    <div style={{ marginTop: '15px', fontStyle: 'italic', color: '#9CA3AF' }}>Este informe fue preparado de acuerdo con los estándares de la 7ma edición del Manual de Publicaciones de la APA.</div>
                </div>
            </div>
        </div>
    );
};

export default EDITABLE_INFORME_EJECUTIVO;
