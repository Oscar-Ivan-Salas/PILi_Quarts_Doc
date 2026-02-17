/**
 * ProjectComplex - Editable Complex Project Document
 * 
 * ALINEACIÓN FIDELIDAD TOTAL: PLANTILLA_HTML_PROYECTO_COMPLEJO_PMI.html
 */
import { useState, useEffect } from 'react';
import type { DocumentData, ColorScheme } from '../../store/useDocumentStore';

interface ProjectComplexProps {
    data?: Partial<DocumentData>;
    colorScheme?: ColorScheme;
    logo?: string | null;
    font?: string;
    onDataChange?: (data: DocumentData) => void;
    editable?: boolean;
}

const COLOR_SCHEMES = {
    'azul-tesla': { primary: '#0052A3', secondary: '#1E40AF', accent: '#3B82F6', text: '#1f2937', contrast: '#DBEAFE' },
    'rojo-pili': { primary: '#DC2626', secondary: '#991B1B', accent: '#EF4444', text: '#1f2937', contrast: '#FEE2E2' },
    'amarillo-pili': { primary: '#D97706', secondary: '#92400E', accent: '#F59E0B', text: '#1f2937', contrast: '#FEF3C7' },
};

export function ProjectComplex({
    data,
    colorScheme = 'azul-tesla',
    font = 'Calibri',
    onDataChange,
    editable = false,
}: ProjectComplexProps) {
    const colors = COLOR_SCHEMES[colorScheme] || COLOR_SCHEMES['azul-tesla'];

    const [editableData] = useState<DocumentData>({
        cliente: {
            nombre: data?.cliente?.nombre || 'CLIENTE CORPORATIVO S.A.',
            ruc: data?.cliente?.ruc || '20555666777',
            direccion: data?.cliente?.direccion || 'Av. Industrial 456, Callao',
            telefono: data?.cliente?.telefono || '01 333 4444',
            email: data?.cliente?.email || 'contacto@cliente.com',
        },
        proyecto: {
            nombre: data?.proyecto?.nombre || 'PLAN MAESTRO DE INFRAESTRUCTURA',
            descripcion: data?.proyecto?.descripcion || 'Desarrollo integral bajo estándares PMI...',
            ubicacion: data?.proyecto?.ubicacion || 'Centro de Datos Sede Sur',
            presupuesto: data?.proyecto?.presupuesto || 120000,
            duracion: data?.proyecto?.duracion || 180,
            fechaInicio: data?.proyecto?.fechaInicio || new Date().toISOString().split('T')[0],
            fechaFin: data?.proyecto?.fechaFin || '',
        },
        fases: data?.fases || [
            { nombre: 'Fase I: Iniciación y Charter', descripcion: 'Definición de objetivos y stakeholders', duracion: 2, presupuesto: 5000 },
            { nombre: 'Fase II: Planificación Detallada', descripcion: 'WBS, Cronograma y Matriz de Riesgos', duracion: 4, presupuesto: 15000 },
            { nombre: 'Fase III: Ejecución y Control', descripcion: 'Suministro e instalación de equipos', duracion: 12, presupuesto: 85000 },
            { nombre: 'Fase IV: Cierre y Handover', descripcion: 'Pruebas finales y documentación as-built', duracion: 2, presupuesto: 15000 }
        ],
        riesgos: data?.riesgos || [
            { descripcion: 'Fluctuación de costos de importación', probabilidad: 'alta', impacto: 'medio', mitigacion: 'Reserva de contingencia financiera' },
            { descripcion: 'Retraso en permisos municipales', probabilidad: 'media', impacto: 'alto', mitigacion: 'Gestión anticipada de trámites' }
        ],
        emisor: {
            nombre: data?.emisor?.nombre || 'TU EMPRESA S.A.C.',
            empresa: data?.emisor?.empresa || data?.emisor?.nombre || 'TU EMPRESA S.A.C.',
            ruc: data?.emisor?.ruc || '00000000000',
            direccion: data?.emisor?.direccion || 'Tu Dirección, Lima',
            logo: data?.emisor?.logo || null
        },
        profesionales: data?.profesionales || [
            { nombre: 'Ing. Marco Polo', cargo: 'Project Manager PMP', especialidad: 'Gestión', registro: 'CIP 88888' },
            { nombre: 'Ing. Ana Luz', cargo: 'Ingeniero Residente', especialidad: 'Electricidad', registro: 'CIP 99999' }
        ],
        kpis_pmi: data?.kpis_pmi || {
            spi: 1.05,
            cpi: 0.98,
            progreso_fisico: 45,
            progreso_financiero: 42
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
                color: '#1f2937'
            }}>
                <div style={{ padding: '20mm' }}>
                    {/* HEADER */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', paddingBottom: '20px', borderBottom: `4px solid ${colors.primary}`, marginBottom: '30px' }}>
                        <div style={{ width: '35%' }}>
                            {editableData.emisor?.logo ? (
                                <img src={editableData.emisor.logo} alt="Logo" style={{ maxWidth: '180px', maxHeight: '80px', objectFit: 'contain' }} />
                            ) : (
                                <div style={{
                                    width: '180px',
                                    height: '80px',
                                    background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 100%)`,
                                    borderRadius: '8px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: 'white',
                                    fontWeight: 'bold',
                                    fontSize: '24px'
                                }}>
                                    {editableData.emisor?.nombre?.substring(0, 10).toUpperCase() || 'PILI'}
                                </div>
                            )}
                            <p style={{ fontSize: '10px', color: '#6B7280', marginTop: '5px' }}>{editableData.emisor?.empresa}</p>
                        </div>
                        <div style={{ width: '65%', textAlign: 'right' }}>
                            <div style={{ fontSize: '20px', fontWeight: 'bold', color: colors.primary, marginBottom: '8px', textTransform: 'uppercase' }}>CHART DE PROYECTO PMI</div>
                            <div style={{ fontSize: '11px', color: '#4b5563', lineHeight: '1.5' }}>
                                <div>N° PROY-PMI-{new Date().getFullYear()}-102</div>
                                <div>Estado: En Planificación / Ejecución</div>
                                <div>Prioridad: Alta</div>
                            </div>
                        </div>
                    </div>

                    {/* PROJECT TITLE BLOCK */}
                    <div style={{ textAlign: 'center', margin: '30px 0', padding: '30px', border: `3px double ${colors.primary}`, background: colors.contrast, borderRadius: '8px' }}>
                        <h1
                            style={{ fontSize: '32px', color: colors.primary, fontWeight: '900', margin: '0 0 10px 0', outline: 'none' }}
                            contentEditable={editable}
                            suppressContentEditableWarning
                            onBlur={e => handleTextChange('proyecto.nombre', e.currentTarget.textContent || '')}
                        >
                            {editableData.proyecto.nombre}
                        </h1>
                        <div style={{ fontSize: '16px', color: colors.secondary, fontWeight: 'bold' }}>PLAN INTEGRAL DE GESTIÓN Y CONTROL</div>
                    </div>

                    {/* KPI DASHBOARD PMI */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '15px', marginBottom: '30px' }}>
                        {[
                            { label: 'SPI (Tiempo)', value: editableData.kpis_pmi?.spi || 0, desc: (editableData.kpis_pmi?.spi || 0) >= 1 ? 'Adelantado' : 'Atrasado', color: (editableData.kpis_pmi?.spi || 0) >= 1 ? '#059669' : '#dc2626' },
                            { label: 'CPI (Costo)', value: editableData.kpis_pmi?.cpi || 0, desc: (editableData.kpis_pmi?.cpi || 0) >= 1 ? 'Bajo Presup.' : 'Sobre Presup.', color: (editableData.kpis_pmi?.cpi || 0) >= 1 ? '#059669' : '#dc2626' },
                            { label: 'Avance Físico', value: `${editableData.kpis_pmi?.progreso_fisico || 0}%`, desc: 'Curva S', color: colors.primary },
                            { label: 'Avance Finan.', value: `${editableData.kpis_pmi?.progreso_financiero || 0}%`, desc: 'Facturado', color: colors.secondary }
                        ].map((k, i) => (
                            <div key={i} style={{ padding: '15px', background: 'white', border: `1px solid ${colors.contrast}`, borderRadius: '10px', textAlign: 'center', boxShadow: '0 2px 6px rgba(0,0,0,0.05)' }}>
                                <div style={{ fontSize: '11px', color: '#6B7280', fontWeight: 'bold', marginBottom: '8px' }}>{k.label}</div>
                                <div style={{ fontSize: '22px', color: k.color, fontWeight: 'bold' }}>{k.value}</div>
                                <div style={{ fontSize: '10px', color: '#9CA3AF', marginTop: '4px' }}>{k.desc}</div>
                            </div>
                        ))}
                    </div>

                    {/* FASES / WBS LEVEL 1 */}
                    <section style={{ marginBottom: '40px' }}>
                        <h2 style={{ fontSize: '18px', color: colors.primary, borderBottom: `2px solid ${colors.primary}`, paddingBottom: '8px', fontWeight: 'bold', textTransform: 'uppercase' }}>I. Desglose de Fases (WBS Lvl 1)</h2>
                        <div style={{ marginTop: '15px' }}>
                            {(editableData.fases || []).map((f: any, i: number) => (
                                <div key={i} style={{ display: 'flex', marginBottom: '15px', background: colors.contrast, borderRadius: '8px', overflow: 'hidden' }}>
                                    <div style={{ width: '60px', background: colors.primary, color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '20px' }}>
                                        0{i + 1}
                                    </div>
                                    <div style={{ padding: '15px', flex: 1 }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                                            <span style={{ fontWeight: 'bold', color: colors.primary }}>{f.nombre}</span>
                                            <span style={{ fontWeight: 'bold' }}>$ {f.presupuesto.toLocaleString()}</span>
                                        </div>
                                        <div style={{ fontSize: '11px', color: '#4b5563' }}>{f.descripcion} | Duración: {f.duracion} semanas</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* RACI MATRIX SIMPLIFIED */}
                    <section style={{ marginBottom: '40px' }}>
                        <h2 style={{ fontSize: '18px', color: colors.primary, borderBottom: `2px solid ${colors.primary}`, paddingBottom: '8px', fontWeight: 'bold', textTransform: 'uppercase' }}>II. Matriz de Responsabilidades (RACI)</h2>
                        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '15px', fontSize: '11px' }}>
                            <thead>
                                <tr style={{ background: colors.primary, color: 'white' }}>
                                    <th style={{ padding: '10px', textAlign: 'left' }}>Entregable / Actividad</th>
                                    {editableData.profesionales.map((p: any, i: number) => (
                                        <th key={i} style={{ padding: '10px' }}>{p.cargo}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {[
                                    { act: 'Diseño de Ingeniería', roles: ['A', 'R'] },
                                    { act: 'Gestión de Suministros', roles: ['R', 'C'] },
                                    { act: 'Montaje en Campo', roles: ['C', 'R'] },
                                    { act: 'Pruebas y QA', roles: ['I', 'A'] }
                                ].map((row, i) => (
                                    <tr key={i} style={{ borderBottom: `1px solid ${colors.contrast}`, background: i % 2 === 0 ? 'white' : colors.contrast }}>
                                        <td style={{ padding: '10px', fontWeight: 'bold' }}>{row.act}</td>
                                        {row.roles.map((r, ri) => (
                                            <td key={ri} style={{ padding: '10px', textAlign: 'center', color: colors.primary, fontWeight: 'bold' }}>{r}</td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        <p style={{ fontSize: '9px', color: '#6B7280', marginTop: '8px' }}>R: Responsable, A: Accountable, C: Consulted, I: Informed</p>
                    </section>

                    {/* RISK REGISTER */}
                    <section style={{ marginBottom: '40px' }}>
                        <h2 style={{ fontSize: '18px', color: colors.primary, borderBottom: `2px solid ${colors.primary}`, paddingBottom: '8px', fontWeight: 'bold', textTransform: 'uppercase' }}>III. Registro de Riesgos Críticos</h2>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '15px' }}>
                            {(editableData.riesgos || []).map((r: any, i: number) => (
                                <div key={i} style={{ padding: '15px', border: `1px solid ${colors.contrast}`, borderRadius: '8px', position: 'relative' }}>
                                    <div style={{ position: 'absolute', top: '10px', right: '10px', fontSize: '10px', padding: '3px 8px', borderRadius: '12px', background: r.probabilidad === 'alta' ? '#fee2e2' : '#fef3c7', color: r.probabilidad === 'alta' ? '#dc2626' : '#d97706', fontWeight: 'bold' }}>
                                        {r.probabilidad.toUpperCase()}
                                    </div>
                                    <div style={{ fontWeight: 'bold', color: colors.primary, fontSize: '13px', marginBottom: '8px' }}>{r.descripcion}</div>
                                    <div style={{ fontSize: '11px', color: '#4b5563' }}>
                                        <strong>Mitigación:</strong> {r.mitigacion}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* FOOTER */}
                    <div style={{ marginTop: '50px', paddingTop: '20px', borderTop: `3px solid ${colors.primary}`, textAlign: 'center', fontSize: '11px', color: '#6B7280' }}>
                        <div style={{ fontWeight: 'bold', color: colors.primary, marginBottom: '5px' }}>{editableData.emisor?.empresa || 'EMRESA EMISORA'}</div>
                        <div>{editableData.emisor?.direccion || 'Dirección de contacto'} | RUC: {editableData.emisor?.ruc}</div>
                        <div style={{ marginTop: '10px', fontStyle: 'italic' }}>Documento controlado N° PROY-PM-{new Date().getFullYear()}</div>
                    </div>
                </div>
            </div>
        </div>
    );
}
