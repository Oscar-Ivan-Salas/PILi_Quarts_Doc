/**
 * ReportTechnical - Technical Report Document
 * 
 * Sections:
 * - Executive Summary
 * - Introduction
 * - Technical Analysis
 * - Results
 * - Conclusions
 * - Recommendations
 */
import { useState, useEffect } from 'react';
import { useDocumentStore, type DocumentData, type ColorScheme } from '../../store/useDocumentStore';

interface ReportTechnicalProps {
    data?: Partial<DocumentData>;
    colorScheme?: ColorScheme;
    logo?: string | null;
    font?: string;
    onDataChange?: (data: DocumentData) => void;
}

const COLOR_SCHEMES = {
    'azul-tesla': { primary: '#0052A3', secondary: '#1E40AF', accent: '#3B82F6', light: '#EFF6FF', lightBorder: '#DBEAFE' },
    'rojo-pili': { primary: '#DC2626', secondary: '#991B1B', accent: '#EF4444', light: '#FEF2F2', lightBorder: '#FECACA' },
    'amarillo-pili': { primary: '#D97706', secondary: '#B45309', accent: '#F59E0B', light: '#FFFBEB', lightBorder: '#FDE68A' },
};

export function ReportTechnical({ data, colorScheme = 'azul-tesla', logo = null, font = 'Calibri', onDataChange }: ReportTechnicalProps) {
    const colors = COLOR_SCHEMES[colorScheme];

    const [editableData, setEditableData] = useState<DocumentData>({
        cliente: { nombre: data?.cliente?.nombre || '', ruc: '', direccion: '', telefono: '', email: '' },
        proyecto: {
            nombre: data?.proyecto?.nombre || 'Informe Técnico',
            descripcion: data?.proyecto?.descripcion || 'Resumen ejecutivo del informe...',
            ubicacion: '',
            presupuesto: 0,
            duracion: 0,
            fechaInicio: new Date().toISOString().split('T')[0],
            fechaFin: '',
        },
        profesionales: [],
        suministros: [],
        entregables: [],
    });

    useEffect(() => {
        onDataChange?.(editableData);
    }, [editableData, onDataChange]);

    return (
        <div style={{ fontFamily: font, maxWidth: '210mm', margin: '0 auto', padding: '20mm', background: 'white', color: '#1f2937', lineHeight: '1.6' }}>
            {/* HEADER */}
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '30px', paddingBottom: '20px', borderBottom: `4px solid ${colors.primary}` }}>
                <div style={{ width: '35%' }}>
                    {logo ? (
                        <img src={logo} alt="Logo" style={{ width: '180px', height: '80px', objectFit: 'contain', borderRadius: '8px' }} />
                    ) : (
                        <div style={{ width: '180px', height: '80px', background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 100%)`, borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold', fontSize: '24px' }}>PILi</div>
                    )}
                </div>
                <div style={{ width: '65%', textAlign: 'right' }}>
                    <div style={{ fontSize: '20px', fontWeight: 'bold', color: colors.primary, marginBottom: '8px', textTransform: 'uppercase' }}>PILi QUARTS - INGENIERÍA Y PROYECTOS</div>
                    <div style={{ fontSize: '11px', color: '#4b5563', lineHeight: '1.5' }}>
                        <div>RUC: 20601138787</div>
                        <div>Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div>
                        <div>Teléfono: 906 315 961</div>
                        <div>Email: contacto@piliquarts.com</div>
                    </div>
                </div>
            </div>

            {/* TITLE */}
            <div style={{ textAlign: 'center', margin: '30px 0', padding: '25px', background: `linear-gradient(135deg, ${colors.light} 0%, ${colors.lightBorder} 100%)`, borderLeft: `6px solid ${colors.primary}`, borderRadius: '4px' }}>
                <h1 style={{ fontSize: '30px', color: colors.primary, fontWeight: 'bold', marginBottom: '8px' }}>INFORME TÉCNICO</h1>
                <input type="text" value={editableData.proyecto.nombre} onChange={(e) => setEditableData({ ...editableData, proyecto: { ...editableData.proyecto, nombre: e.target.value } })} style={{ border: 'none', borderBottom: `2px solid ${colors.accent}`, background: 'transparent', color: colors.secondary, fontWeight: '600', fontSize: '16px', width: '80%', textAlign: 'center', marginTop: '10px' }} />
                <div style={{ fontSize: '14px', color: colors.secondary, marginTop: '10px' }}>Código: INF-TEC-{new Date().getFullYear()}-001</div>
            </div>

            {/* CLIENT INFO */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', margin: '25px 0' }}>
                <div style={{ padding: '15px', border: `2px solid ${colors.lightBorder}`, borderRadius: '6px', background: '#F9FAFB' }}>
                    <h3 style={{ fontSize: '14px', color: colors.primary, fontWeight: 'bold', marginBottom: '10px', textTransform: 'uppercase', borderBottom: `2px solid ${colors.primary}`, paddingBottom: '5px' }}>Datos del Cliente</h3>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colors.secondary }}>Cliente:</strong>{' '}
                        <input type="text" value={editableData.cliente.nombre} onChange={(e) => setEditableData({ ...editableData, cliente: { ...editableData.cliente, nombre: e.target.value } })} style={{ border: 'none', borderBottom: `1px solid ${colors.accent}`, background: 'transparent', fontSize: '12px', width: '70%' }} />
                    </p>
                </div>
                <div style={{ padding: '15px', border: `2px solid ${colors.lightBorder}`, borderRadius: '6px', background: '#F9FAFB' }}>
                    <h3 style={{ fontSize: '14px', color: colors.primary, fontWeight: 'bold', marginBottom: '10px', textTransform: 'uppercase', borderBottom: `2px solid ${colors.primary}`, paddingBottom: '5px' }}>Datos del Informe</h3>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colors.secondary }}>Fecha:</strong> {new Date().toLocaleDateString('es-PE')}</p>
                </div>
            </div>

            {/* EXECUTIVE SUMMARY */}
            <div style={{ margin: '30px 0', padding: '25px', background: `linear-gradient(135deg, ${colors.light} 0%, ${colors.lightBorder} 100%)`, borderLeft: `6px solid ${colors.primary}`, borderRadius: '4px' }}>
                <h3 style={{ fontSize: '18px', color: colors.primary, marginBottom: '15px', textTransform: 'uppercase' }}>Resumen Ejecutivo</h3>
                <textarea value={editableData.proyecto.descripcion} onChange={(e) => setEditableData({ ...editableData, proyecto: { ...editableData.proyecto, descripcion: e.target.value } })} style={{ width: '100%', minHeight: '100px', fontSize: '13px', color: '#374151', lineHeight: '1.8', textAlign: 'justify', border: `1px solid ${colors.lightBorder}`, borderRadius: '4px', padding: '10px', background: 'white' }} />
            </div>

            {/* SECTIONS */}
            {['1. INTRODUCCIÓN', '2. ANÁLISIS TÉCNICO', '3. RESULTADOS'].map((title, idx) => (
                <div key={idx} style={{ margin: '35px 0' }}>
                    <h2 style={{ fontSize: '20px', color: colors.primary, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colors.primary}` }}>{title}</h2>
                    <textarea placeholder={`Contenido de ${title.toLowerCase()}...`} style={{ width: '100%', minHeight: idx === 1 ? '200px' : '150px', fontSize: '12px', color: '#374151', lineHeight: '1.8', textAlign: 'justify', border: `1px solid ${colors.lightBorder}`, borderRadius: '4px', padding: '10px' }} />
                </div>
            ))}

            {/* CONCLUSIONS */}
            <div style={{ margin: '30px 0', padding: '25px', background: `linear-gradient(135deg, ${colors.light} 0%, ${colors.lightBorder} 100%)`, borderLeft: `6px solid ${colors.primary}`, borderRadius: '4px' }}>
                <h3 style={{ fontSize: '18px', color: colors.primary, marginBottom: '15px' }}>CONCLUSIONES</h3>
                <textarea placeholder="Conclusiones del análisis..." style={{ width: '100%', minHeight: '150px', fontSize: '12px', color: '#374151', lineHeight: '1.6', border: `1px solid ${colors.lightBorder}`, borderRadius: '4px', padding: '10px', background: 'white' }} />
            </div>

            {/* RECOMMENDATIONS */}
            <div style={{ margin: '30px 0' }}>
                <h2 style={{ fontSize: '20px', color: colors.primary, marginBottom: '20px', paddingBottom: '10px', borderBottom: `3px solid ${colors.primary}` }}>RECOMENDACIONES</h2>
                <ul style={{ listStyle: 'none', padding: 0 }}>
                    {['Recomendación técnica 1', 'Recomendación técnica 2', 'Recomendación técnica 3'].map((rec, i) => (
                        <li key={i} style={{ fontSize: '12px', color: '#374151', margin: '12px 0', paddingLeft: '30px', position: 'relative', lineHeight: '1.6' }}>
                            <span style={{ position: 'absolute', left: '10px', color: colors.primary, fontSize: '16px' }}>●</span>
                            {rec}
                        </li>
                    ))}
                </ul>
            </div>

            {/* FOOTER */}
            <div style={{ marginTop: '40px', paddingTop: '20px', borderTop: `3px solid ${colors.primary}`, textAlign: 'center', fontSize: '10px', color: '#6B7280' }}>
                <div style={{ fontWeight: 'bold', color: colors.primary, fontSize: '12px', marginBottom: '8px' }}>PILi QUARTS - INGENIERÍA Y PROYECTOS</div>
                <div style={{ margin: '5px 0' }}>RUC: 20601138787 | Teléfono: 906 315 961</div>
                <div style={{ margin: '5px 0' }}>Email: contacto@piliquarts.com</div>
            </div>
        </div>
    );
}
