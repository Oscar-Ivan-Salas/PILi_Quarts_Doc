/**
 * ReportExecutive - Editable Executive Report Document
 * 
 * ALINEACIÓN FIDELIDAD TOTAL: PLANTILLA_HTML_INFORME_EJECUTIVO_APA.html
 */
import { useState, useEffect } from 'react';
import type { DocumentData, ColorScheme } from '../../store/useDocumentStore';

interface ReportExecutiveProps {
    data?: Partial<DocumentData>;
    colorScheme?: ColorScheme;
    font?: string;
    onDataChange?: (data: DocumentData) => void;
    editable?: boolean;
}

const COLOR_SCHEMES = {
    'azul-tesla': { primary: '#0052A3', secondary: '#1E40AF', accent: '#3B82F6', text: '#1f2937', contrast: '#DBEAFE' },
    'rojo-pili': { primary: '#DC2626', secondary: '#991B1B', accent: '#EF4444', text: '#1f2937', contrast: '#FEE2E2' },
    'amarillo-pili': { primary: '#D97706', secondary: '#92400E', accent: '#F59E0B', text: '#1f2937', contrast: '#FEF3C7' },
};

export function ReportExecutive({
    data,
    colorScheme = 'azul-tesla',
    font = 'Calibri',
    onDataChange,
    editable = false,
}: ReportExecutiveProps) {
    const colors = COLOR_SCHEMES[colorScheme] || COLOR_SCHEMES['azul-tesla'];

    const [editableData] = useState<DocumentData>({
        cliente: {
            nombre: data?.cliente?.nombre || 'EMPRESA CLIENTE S.A.C.',
            ruc: data?.cliente?.ruc || '20000000000',
            direccion: data?.cliente?.direccion || 'Dirección del Cliente',
            telefono: data?.cliente?.telefono || '999 000 000',
            email: data?.cliente?.email || 'contacto@cliente.com',
        },
        proyecto: {
            nombre: data?.proyecto?.nombre || 'PROYECTO DE MODERNIZACIÓN ELÉCTRICA',
            descripcion: data?.proyecto?.descripcion || 'Resultados estratégicos del periodo...',
            ubicacion: data?.proyecto?.ubicacion || 'Planta Industrial SJL',
            presupuesto: data?.proyecto?.presupuesto || 45000,
            duracion: data?.proyecto?.duracion || 90,
            fechaInicio: data?.proyecto?.fechaInicio || '2026-03-01',
            fechaFin: data?.proyecto?.fechaFin || '2026-06-01',
        },
        resumen_ejecutivo: data?.resumen_ejecutivo || 'Se recomienda aprobar el proyecto dada su alta viabilidad técnica y financiera.',
        titulo: data?.titulo || 'ANÁLISIS DE VIABILIDAD DEL PROYECTO',
        codigo: data?.codigo || 'INF-2026-001X',
        kpis_financieros: data?.kpis_financieros || {
            roi: '85',
            payback: '14',
            tir: '32',
            ahorro_anual: '12',
            ahorro_energetico: '4,500'
        },
        conclusiones: data?.conclusiones || [
            'El proyecto es técnicamente viable según normativa vigente.',
            'El análisis financiero demuestra un ROI atractivo del 85%.',
            'Los riesgos identificados son manejables con planes de mitigación.'
        ],
        emisor: {
            nombre: data?.emisor?.nombre || 'ELABORADO POR',
            empresa: data?.emisor?.empresa || data?.emisor?.nombre || 'TU EMPRESA S.A.C.',
            ruc: data?.emisor?.ruc || '00000000000',
            direccion: data?.emisor?.direccion || 'Tu Dirección, Lima',
            logo: data?.emisor?.logo || null
        }
    } as any);

    const handleTextChange = (path: string, value: string) => {
        const newData = { ...editableData };
        const keys = path.split('.');
        let current: any = newData;
        for (let i = 0; i < keys.length - 1; i++) {
            current = current[keys[i]];
        }
        current[keys[keys.length - 1]] = value;
        onDataChange?.(newData);
    };

    useEffect(() => {
        onDataChange?.(editableData);
    }, [editableData, onDataChange]);

    return (
        <div style={{ backgroundColor: '#f3f4f6', padding: '40px 0', minHeight: '100vh' }}>
            <div style={{
                fontFamily: font,
                maxWidth: '210mm',
                margin: '0 auto',
                background: 'white',
                boxShadow: '0 0 20px rgba(0,0,0,0.1)',
                color: '#000'
            }}>

                {/* PORTADA APA */}
                <div style={{
                    height: '280mm',
                    padding: '25mm',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    textAlign: 'center',
                    borderBottom: '1px solid #e5e7eb'
                }}>
                    <div style={{ marginTop: '80px' }}>
                        <h1
                            style={{ fontSize: '24px', fontWeight: 'bold', lineHeight: '2', textTransform: 'uppercase', outline: 'none' }}
                            contentEditable={editable}
                            suppressContentEditableWarning
                            onBlur={e => handleTextChange('titulo', e.currentTarget.textContent || '')}
                        >
                            INFORME EJECUTIVO:<br />
                            {editableData.titulo}<br />
                            {editableData.proyecto.nombre}
                        </h1>
                    </div>

                    <div style={{ marginBottom: '60px', lineHeight: '2' }}>
                        <div style={{ fontWeight: 'bold' }}>Elaborado para:</div>
                        <div>{editableData.cliente.nombre}</div>
                        <div style={{ marginTop: '40px', fontWeight: 'bold' }}>Preparado por:</div>
                        <div>{editableData.emisor?.empresa}</div>
                        <div>{editableData.emisor?.nombre}</div>
                        <div style={{ marginTop: '40px' }}>{new Date().toLocaleDateString()}</div>
                        <div style={{ marginTop: '20px', fontSize: '14px', color: '#6B7280' }}>
                            Código del Informe: {editableData.codigo}
                        </div>
                    </div>
                </div>

                {/* CONTENIDO PRINCIPAL - CONTAINER */}
                <div style={{ padding: '25mm' }}>
                    {/* HEADER */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '15px', borderBottom: `3px solid ${colors.primary}`, marginBottom: '30px' }}>
                        <div>
                            {editableData.emisor?.logo ? (
                                <img src={editableData.emisor.logo} alt="Logo" style={{ maxWidth: '160px', maxHeight: '70px', objectFit: 'contain' }} />
                            ) : (
                                <div style={{
                                    width: '160px',
                                    height: '70px',
                                    background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 100%)`,
                                    borderRadius: '6px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: 'white',
                                    fontWeight: 'bold',
                                    fontSize: '22px'
                                }}>
                                    {editableData.emisor?.nombre?.substring(0, 10).toUpperCase() || 'PILI'}
                                </div>
                            )}
                            <p style={{ fontSize: '12px', color: '#6b7280', marginTop: '5px' }}>{editableData.emisor?.nombre}</p>
                        </div>
                        <div style={{ textAlign: 'right', fontSize: '13px', color: '#4b5563' }}>
                            <div style={{ fontSize: '18px', fontWeight: 'bold', color: colors.primary, marginBottom: '8px' }}>{editableData.emisor?.empresa}</div>
                            <div>RUC: {editableData.emisor?.ruc}</div>
                            <div>{editableData.emisor?.direccion}</div>
                        </div>
                    </div>

                    {/* EXECUTIVE SUMMARY BOX */}
                    <div style={{
                        padding: '30px',
                        background: `linear-gradient(135deg, ${colors.contrast} 0%, #DBEAFE 100%)`,
                        borderLeft: `8px solid ${colors.primary}`,
                        borderRadius: '6px',
                        margin: '30px 0'
                    }}>
                        <h2 style={{ fontSize: '20px', color: colors.primary, marginBottom: '20px', fontWeight: 'bold', textAlign: 'center', textTransform: 'uppercase' }}>Executive Summary</h2>
                        <p
                            style={{ fontSize: '15px', textAlign: 'justify', lineHeight: '1.8', outline: 'none' }}
                            contentEditable={editable}
                            suppressContentEditableWarning
                            onBlur={e => handleTextChange('resumen_ejecutivo', e.currentTarget.textContent || '')}
                        >
                            {editableData.resumen_ejecutivo}
                        </p>

                        <div style={{ marginTop: '25px' }}>
                            <p><strong style={{ color: colors.primary }}>Hallazgos Principales:</strong></p>
                            <ul style={{ marginTop: '10px' }}>
                                <li>Inversión requerida: $ {editableData.proyecto.presupuesto.toLocaleString()}</li>
                                <li>ROI estimado: {editableData.kpis_financieros?.roi || '0'}%</li>
                                <li>Período de retorno: {editableData.kpis_financieros?.payback || '0'} meses</li>
                                <li>TIR proyectada: {editableData.kpis_financieros?.tir || '0'}%</li>
                            </ul>
                        </div>
                    </div>

                    {/* GRANDE PRESUPUESTO */}
                    <div style={{ textAlign: 'center', padding: '30px', background: colors.contrast, borderRadius: '8px', margin: '25px 0' }}>
                        <div style={{ fontSize: '15px', color: '#6B7280', marginBottom: '10px' }}>INVERSIÓN TOTAL REQUERIDA</div>
                        <div style={{ fontSize: '54px', color: colors.primary, fontWeight: 'bold' }}>$ {editableData.proyecto.presupuesto.toLocaleString()}</div>
                    </div>

                    {/* MÉTRICAS GRID */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', margin: '35px 0' }}>
                        {[
                            { label: 'ROI Estimado', value: `${editableData.kpis_financieros?.roi || '0'}%`, desc: 'Retorno Inversión' },
                            { label: 'Payback', value: `${editableData.kpis_financieros?.payback || '0'}m`, desc: 'Recuperación' },
                            { label: 'TIR', value: `${editableData.kpis_financieros?.tir || '0'}%`, desc: 'Tasa Retorno' },
                            { label: 'Ahorro Anual', value: `$${editableData.kpis_financieros?.ahorro_anual || '0'}K`, desc: 'Proyección' }
                        ].map((m, i) => (
                            <div key={i} style={{ padding: '20px', background: 'white', border: `2px solid ${colors.contrast}`, borderRadius: '8px', textAlign: 'center', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
                                <div style={{ fontSize: '12px', color: '#6B7280', fontWeight: 'bold', marginBottom: '10px' }}>{m.label}</div>
                                <div style={{ fontSize: '24px', color: colors.primary, fontWeight: 'bold' }}>{m.value}</div>
                                <div style={{ fontSize: '11px', color: '#9CA3AF', marginTop: '5px' }}>{m.desc}</div>
                            </div>
                        ))}
                    </div>

                    {/* SECCIÓN CONCLUSIONES FIDELIDAD TOTAL */}
                    <div style={{ padding: '30px', background: `linear-gradient(135deg, ${colors.contrast} 0%, #DBEAFE 100%)`, borderLeft: `8px solid ${colors.primary}`, borderRadius: '6px', margin: '40px 0' }}>
                        <h3 style={{ fontSize: '18px', color: colors.primary, fontWeight: 'bold', marginBottom: '20px', textAlign: 'center' }}>CONCLUSIONES Y RECOMENDACIONES</h3>
                        <ul style={{ listStyle: 'none', padding: 0 }}>
                            {(Array.isArray(editableData.conclusiones) ? editableData.conclusiones : (editableData.conclusiones ? [editableData.conclusiones] : [])).map((concl: any, i: number) => (
                                <li key={i} style={{ fontSize: '15px', color: '#1f2937', margin: '15px 0', paddingLeft: '35px', position: 'relative', lineHeight: '1.8' }}>
                                    <span style={{ position: 'absolute', left: 0, color: colors.primary, fontWeight: 'bold', fontSize: '24px' }}>✓</span>
                                    {concl}
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* FOOTER */}
                    <div style={{ marginTop: '50px', paddingTop: '20px', borderTop: `3px solid ${colors.primary}`, textAlign: 'center', fontSize: '12px', color: '#6B7280' }}>
                        <div style={{ fontWeight: 'bold', color: colors.primary, fontSize: '14px', marginBottom: '8px' }}>{editableData.emisor?.empresa}</div>
                        <div>RUC: {editableData.emisor?.ruc} | {editableData.emisor?.direccion}</div>
                        <div style={{ marginTop: '15px', fontStyle: 'italic', color: '#9CA3AF' }}>
                            Informe preparado bajo estándares APA 7ma Edición.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
