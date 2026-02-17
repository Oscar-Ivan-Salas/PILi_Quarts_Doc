/**
 * ProjectSimple - Editable Simple Project Document
 * 
 * ALINEACIÓN FIDELIDAD TOTAL: PLANTILLA_HTML_PROYECTO_SIMPLE.html
 */
import { useState, useEffect } from 'react';
import type { DocumentData, ColorScheme } from '../../store/useDocumentStore';

interface ProjectSimpleProps {
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

export function ProjectSimple({
    data,
    colorScheme = 'azul-tesla',
    font = 'Calibri',
    onDataChange,
    editable = false,
}: ProjectSimpleProps) {
    const colors = COLOR_SCHEMES[colorScheme] || COLOR_SCHEMES['azul-tesla'];

    const [editableData] = useState<DocumentData>({
        cliente: {
            nombre: data?.cliente?.nombre || 'CLIENTE ESTÁNDAR S.A.C.',
            ruc: data?.cliente?.ruc || '20444555666',
            direccion: data?.cliente?.direccion || 'Av. Principal 123, Lima',
            telefono: data?.cliente?.telefono || '01 222 3333',
            email: data?.cliente?.email || 'proyectos@cliente.com',
        },
        proyecto: {
            nombre: data?.proyecto?.nombre || 'PROYECTO DE INSTALACIÓN ELÉCTRICA',
            descripcion: data?.proyecto?.descripcion || 'Ejecución de servicios y suministro de materiales...',
            ubicacion: data?.proyecto?.ubicacion || 'Almacén Central LIMA',
            presupuesto: data?.proyecto?.presupuesto || 25000,
            duracion: data?.proyecto?.duracion || 30,
            fechaInicio: data?.proyecto?.fechaInicio || new Date().toISOString().split('T')[0],
            fechaFin: data?.proyecto?.fechaFin || '',
        },
        fases: data?.fases || [
            { nombre: 'Suministro de Materiales', descripcion: 'Adquisición y transporte a obra', duracion: 1, presupuesto: 10000 },
            { nombre: 'Mano de Obra y Ejecución', descripcion: 'Instalación y conexionado', duracion: 3, presupuesto: 15000 }
        ],
        riesgos: data?.riesgos || [
            { descripcion: 'Clima adverso en zona de obra', probabilidad: 'media', impacto: 'bajo', mitigacion: 'Planificación flexible' }
        ],
        profesionales: data?.profesionales || [
            { nombre: 'Ing. Carlos Ruiz', cargo: 'Supervisor', especialidad: 'Eléctrica', registro: 'CIP 77777' }
        ],
        emisor: {
            nombre: data?.emisor?.nombre || 'TU EMPRESA S.A.C.',
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
                            <div style={{ fontSize: '20px', fontWeight: 'bold', color: colors.primary, marginBottom: '8px', textTransform: 'uppercase' }}>PLAN DE PROYECTO ESTÁNDAR</div>
                            <div style={{ fontSize: '11px', color: '#4b5563', lineHeight: '1.5' }}>
                                <div>N° PROY-SIMP-{new Date().getFullYear()}-045</div>
                                <div>Fecha de Emisión: {new Date().toLocaleDateString('es-PE')}</div>
                            </div>
                        </div>
                    </div>

                    {/* SECTION: CLIENTE */}
                    <div style={{ marginBottom: '30px', padding: '15px', border: `1px solid ${colors.contrast}`, borderRadius: '6px' }}>
                        <h2 style={{ fontSize: '14px', color: colors.primary, fontWeight: 'bold', borderBottom: `2px solid ${colors.primary}`, paddingBottom: '5px', marginBottom: '10px' }}>INFORMACIÓN DEL CLIENTE</h2>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '12px' }}>
                            <div><strong>Razón Social:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('cliente.nombre', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.cliente.nombre}</span></div>
                            <div><strong>RUC:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('cliente.ruc', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.cliente.ruc}</span></div>
                            <div><strong>Ubicación:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('proyecto.ubicacion', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.proyecto.ubicacion}</span></div>
                            <div><strong>Contacto:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('cliente.email', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.cliente.email}</span></div>
                        </div>
                    </div>

                    {/* SECTION: PROYECTO */}
                    <div style={{ marginBottom: '30px' }}>
                        <h1
                            style={{ fontSize: '24px', color: colors.primary, fontWeight: 'bold', marginBottom: '10px', outline: 'none' }}
                            contentEditable={editable}
                            suppressContentEditableWarning
                            onBlur={e => handleTextChange('proyecto.nombre', e.currentTarget.textContent || '')}
                        >
                            {editableData.proyecto.nombre}
                        </h1>
                        <p
                            style={{ fontSize: '13px', lineHeight: '1.6', textAlign: 'justify', outline: 'none' }}
                            contentEditable={editable}
                            suppressContentEditableWarning
                            onBlur={e => handleTextChange('proyecto.descripcion', e.currentTarget.textContent || '')}
                        >
                            {editableData.proyecto.descripcion}
                        </p>
                    </div>

                    {/* SECTION: FASES */}
                    <section style={{ marginBottom: '30px' }}>
                        <h2 style={{ fontSize: '16px', color: colors.primary, fontWeight: 'bold', marginBottom: '15px', borderLeft: `5px solid ${colors.primary}`, paddingLeft: '10px' }}>CRONOGRAMA DE EJECUCIÓN</h2>
                        <div style={{ border: `1px solid ${colors.contrast}`, borderRadius: '8px', overflow: 'hidden' }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
                                <thead style={{ background: colors.primary, color: 'white' }}>
                                    <tr>
                                        <th style={{ padding: '10px', textAlign: 'left' }}>Descripción de la Fase</th>
                                        <th style={{ padding: '10px', textAlign: 'center' }}>Semanas</th>
                                        <th style={{ padding: '10px', textAlign: 'right' }}>Costo Est.</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {(editableData.fases || []).map((f: any, i: number) => (
                                        <tr key={i} style={{ borderBottom: `1px solid ${colors.contrast}`, background: i % 2 === 0 ? 'white' : '#F9FAFB' }}>
                                            <td style={{ padding: '10px' }}>
                                                <div style={{ fontWeight: 'bold', color: colors.secondary }}>{f.nombre}</div>
                                                <div style={{ fontSize: '10px', color: '#6B7280' }}>{f.descripcion}</div>
                                            </td>
                                            <td style={{ padding: '10px', textAlign: 'center' }}>{f.duracion}</td>
                                            <td style={{ padding: '10px', textAlign: 'right' }}>S/ {f.presupuesto.toLocaleString()}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </section>

                    {/* SUMMARY BOX */}
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '20px', marginBottom: '40px' }}>
                        <div style={{ textAlign: 'right', padding: '15px', background: colors.contrast, borderRadius: '8px' }}>
                            <div style={{ fontSize: '10px', color: colors.secondary, fontWeight: 'bold' }}>PRESUPUESTO TOTAL ESTIMADO</div>
                            <div style={{ fontSize: '24px', color: colors.primary, fontWeight: '900' }}>S/ {(editableData.fases || []).reduce((acc: number, f: any) => acc + f.presupuesto, 0).toLocaleString()}</div>
                        </div>
                    </div>

                    {/* FOOTER */}
                    <div style={{ marginTop: '60px', paddingTop: '20px', borderTop: `3px solid ${colors.primary}`, textAlign: 'center', fontSize: '11px', color: '#6B7280' }}>
                        <div style={{ fontWeight: 'bold', color: colors.primary, marginBottom: '5px' }}>{editableData.emisor?.empresa}</div>
                        <div>RUC: {editableData.emisor?.ruc} | {editableData.emisor?.direccion}</div>
                        <div style={{ marginTop: '10px', fontSize: '10px' }}>Plan de Proyecto N° PROY-SIMP-{new Date().getFullYear()}</div>
                    </div>
                </div>
            </div>
        </div>
    );
}
