/**
 * ReportTechnical - Technical Report Document
 * 
 * ALINEACIÓN FIDELIDAD TOTAL: PLANTILLA_HTML_INFORME_TECNICO.html
 */
import { useState, useEffect } from 'react';
import type { DocumentData, ColorScheme } from '../../store/useDocumentStore';

interface ReportTechnicalProps {
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

export function ReportTechnical({
    data,
    colorScheme = 'azul-tesla',
    font = 'Calibri',
    onDataChange,
    editable = false,
}: ReportTechnicalProps) {
    const colors = COLOR_SCHEMES[colorScheme] || COLOR_SCHEMES['azul-tesla'];

    const [editableData] = useState<DocumentData>({
        cliente: {
            nombre: data?.cliente?.nombre || 'CLIENTE INDUSTRIAL S.A.',
            ruc: data?.cliente?.ruc || '20123456789',
            direccion: data?.cliente?.direccion || 'Zona Industrial, Callao',
            telefono: data?.cliente?.telefono || '01 444 5555',
            email: data?.cliente?.email || 'ingenieria@cliente.com',
        },
        proyecto: {
            nombre: data?.proyecto?.nombre || 'MANTENIMIENTO DE SUBESTACIÓN ELÉCTRICA',
            descripcion: data?.proyecto?.descripcion || 'Informe detallado de actividades...',
            ubicacion: data?.proyecto?.ubicacion || 'SE-01 Planta Principal',
            presupuesto: data?.proyecto?.presupuesto || 0,
            duracion: data?.proyecto?.duracion || 0,
            fechaInicio: data?.proyecto?.fechaInicio || new Date().toISOString().split('T')[0],
            fechaFin: data?.proyecto?.fechaFin || '',
        },
        introduccion: data?.introduccion || 'El presente informe detalla las actividades de mantenimiento preventivo ejecutadas...',
        analisis_tecnico: data?.analisis_tecnico || 'Se realizó la termografía y medición de resistencia de aislamiento...',
        resultados: data?.resultados || 'Los equipos se encuentran operativos pero con observaciones en el transformador T-02.',
        conclusiones: data?.conclusiones || [
            'El sistema eléctrico general está en estado satisfactorio.',
            'Se requiere cambio de aceite en el transformador principal.',
            'Los niveles de armónicos están dentro de los límites permisibles.'
        ],
        recomendaciones: data?.recomendaciones || [
            'Programar mantenimiento correctivo para el transformador T-02.',
            'Instalar filtros de armónicos en la barra principal.',
            'Realizar seguimiento bimestral de temperatura.'
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
                            <p style={{ fontSize: '10px', color: '#6B7280', marginTop: '5px' }}>{editableData.emisor?.nombre}</p>
                        </div>
                        <div style={{ width: '65%', textAlign: 'right' }}>
                            <div style={{ fontSize: '18px', fontWeight: 'bold', color: colors.primary, marginBottom: '8px', textTransform: 'uppercase' }}>{editableData.emisor?.empresa}</div>
                            <div style={{ fontSize: '11px', color: '#4b5563', lineHeight: '1.5' }}>
                                <div>RUC: {editableData.emisor?.ruc}</div>
                                <div>{editableData.emisor?.direccion}</div>
                            </div>
                        </div>
                    </div>

                    {/* TITLE */}
                    <div style={{ textAlign: 'center', margin: '30px 0', padding: '25px', background: `linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)`, borderLeft: `6px solid ${colors.primary}`, borderRadius: '4px' }}>
                        <h1 style={{ fontSize: '30px', color: colors.primary, fontWeight: 'bold', margin: '0 0 8px 0' }}>INFORME TÉCNICO</h1>
                        <div style={{ fontSize: '14px', color: colors.secondary, fontWeight: '600' }}>Versión Industrial - Registro de Ingeniería</div>
                        <div style={{ fontSize: '16px', color: colors.primary, fontWeight: 'bold', marginTop: '10px' }}>N° {new Date().getFullYear()}-{Math.floor(Math.random() * 1000).toString().padStart(3, '0')}</div>
                    </div>

                    {/* INFO BOXES */}
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '25px' }}>
                        <div style={{ padding: '15px', border: `2px solid ${colors.contrast}`, borderRadius: '6px', background: '#F9FAFB' }}>
                            <h3 style={{ fontSize: '14px', color: colors.primary, fontWeight: 'bold', marginBottom: '10px', textTransform: 'uppercase', borderBottom: `2px solid ${colors.primary}`, paddingBottom: '5px' }}>Información del Cliente</h3>
                            <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colors.secondary }}>Nombre:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('cliente.nombre', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.cliente.nombre}</span></p>
                            <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colors.secondary }}>Proyecto:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('proyecto.nombre', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.proyecto.nombre}</span></p>
                            <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colors.secondary }}>Ubicación:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('proyecto.ubicacion', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.proyecto.ubicacion}</span></p>
                        </div>
                        <div style={{ padding: '15px', border: `2px solid ${colors.contrast}`, borderRadius: '6px', background: '#F9FAFB' }}>
                            <h3 style={{ fontSize: '14px', color: colors.primary, fontWeight: 'bold', marginBottom: '10px', textTransform: 'uppercase', borderBottom: `2px solid ${colors.primary}`, paddingBottom: '5px' }}>Datos del Informe</h3>
                            <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colors.secondary }}>Fecha de Actividad:</strong> {editableData.proyecto.fechaInicio}</p>
                            <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colors.secondary }}>Normativa Aplicable:</strong> Código Nacional de Electricidad</p>
                            <p style={{ fontSize: '12px', margin: '5px 0' }}><strong style={{ color: colors.secondary }}>Especialidad:</strong> Ingeniería Eléctrica</p>
                        </div>
                    </div>

                    {/* SECTIONS */}
                    {[
                        { title: '1. INTRODUCCIÓN Y ALCANCE', content: editableData.introduccion },
                        { title: '2. ANÁLISIS TÉCNICO Y HALLAZGOS', content: editableData.analisis_tecnico },
                        { title: '3. RESULTADOS DE PRUEBAS', content: editableData.resultados }
                    ].map((section, idx) => (
                        <div key={idx} style={{ margin: '30px 0' }}>
                            <h2 style={{ fontSize: '18px', color: colors.primary, marginBottom: '15px', borderBottom: `2px solid ${colors.primary}`, paddingBottom: '8px', fontWeight: 'bold' }}>{section.title}</h2>
                            <div style={{ fontSize: '13px', lineHeight: '1.8', textAlign: 'justify', color: '#374151' }}>
                                {section.content}
                            </div>
                        </div>
                    ))}

                    {/* CONCLUSIONES STYLED */}
                    <div style={{ margin: '40px 0', padding: '25px', background: '#F9FAFB', borderLeft: `6px solid ${colors.primary}`, borderRadius: '4px' }}>
                        <h3 style={{ fontSize: '18px', color: colors.primary, marginBottom: '15px', fontWeight: 'bold' }}>4. CONCLUSIONES TÉCNICAS</h3>
                        <ul style={{ listStyle: 'none', padding: 0 }}>
                            {(Array.isArray(editableData.conclusiones) ? editableData.conclusiones : [editableData.conclusiones]).map((concl: any, i: number) => (
                                <li key={i} style={{ fontSize: '13px', color: '#1f2937', margin: '12px 0', paddingLeft: '30px', position: 'relative', lineHeight: '1.6' }}>
                                    <span style={{ position: 'absolute', left: 0, color: colors.primary, fontWeight: 'bold', fontSize: '18px' }}>✓</span>
                                    {concl}
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* RECOMENDACIONES */}
                    <div style={{ margin: '40px 0' }}>
                        <h3 style={{ fontSize: '18px', color: colors.primary, marginBottom: '15px', fontWeight: 'bold' }}>5. RECOMENDACIONES</h3>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px' }}>
                            {(editableData.recomendaciones || []).map((rec: any, i: number) => (
                                <div key={i} style={{ padding: '15px', border: `1px solid ${colors.contrast}`, borderRadius: '8px', fontSize: '11px', background: 'white' }}>
                                    <div style={{ color: colors.primary, fontWeight: 'bold', marginBottom: '8px' }}>R-{i + 1}</div>
                                    {rec}
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* FOOTER */}
                    <div style={{ marginTop: '60px', paddingTop: '20px', borderTop: `3px solid ${colors.primary}`, textAlign: 'center', fontSize: '11px', color: '#6B7280' }}>
                        <div style={{ fontWeight: 'bold', color: colors.primary, marginBottom: '5px' }}>{editableData.emisor?.empresa}</div>
                        <div>RUC: {editableData.emisor?.ruc} | {editableData.emisor?.direccion}</div>
                        <div style={{ marginTop: '10px', fontStyle: 'italic' }}>Este informe es un documento técnico confidencial.</div>
                    </div>
                </div>
            </div>
        </div>
    );
}
