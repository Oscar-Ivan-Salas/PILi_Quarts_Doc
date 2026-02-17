/**
 * QuoteComplex - Editable Complex Quote Document
 * 
 * ALINEACIÓN FIDELIDAD TOTAL: PLANTILLA_HTML_COTIZACION_COMPLEJA.html
 */
import { useState, useEffect } from 'react';
import type { DocumentData, ColorScheme } from '../../store/useDocumentStore';

interface QuoteComplexProps {
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

export function QuoteComplex({
    data,
    colorScheme = 'azul-tesla',
    font = 'Calibri',
    onDataChange,
    editable = false,
}: QuoteComplexProps) {
    const colors = COLOR_SCHEMES[colorScheme] || COLOR_SCHEMES['azul-tesla'];

    const [editableData] = useState<DocumentData>({
        cliente: {
            nombre: data?.cliente?.nombre || 'INDUSTRIAL SOLUTIONS PERÚ S.A.',
            ruc: data?.cliente?.ruc || '20555666777',
            direccion: data?.cliente?.direccion || 'Parque Industrial Lote 45, Lurín',
            telefono: data?.cliente?.telefono || '01 666 7777',
            email: data?.cliente?.email || 'gerencia@industrial.com',
        },
        proyecto: {
            nombre: data?.proyecto?.nombre || 'SISTEMA DE AUTOMATIZACIÓN Y CONTROL Q3',
            descripcion: data?.proyecto?.descripcion || 'Solución integral que abarca desde el diseño hasta la puesta en marcha.',
            duracion: data?.proyecto?.duracion || 60, // Días
        },
        suministros: data?.suministros || [
            { item: '01', descripcion: 'Controlador Lógico Programable (PLC) Siemens S7-1200', cantidad: 1, unidad: 'und', precioUnitario: 1250, precioTotal: 1250 },
            { item: '02', descripcion: 'Licencia TIA Portal V17 con Soporte Premium', cantidad: 1, unidad: 'srv', precioUnitario: 800, precioTotal: 800 },
            { item: '03', descripcion: 'Instalación y Configuración en Planta', cantidad: 1, unidad: 'glob', precioUnitario: 2500, precioTotal: 2500 }
        ],
        entregables: data?.entregables || [
            'Planos Eléctricos en AutoCAD',
            'Manuales de Operación y Mantenimiento',
            'Protocolos de Pruebas de Funcionamiento'
        ],
        emisor: {
            nombre: data?.emisor?.nombre || 'TU EMPRESA S.A.C.',
            empresa: data?.emisor?.empresa || data?.emisor?.nombre || 'TU EMPRESA S.A.C.',
            ruc: data?.emisor?.ruc || '00000000000',
            direccion: data?.emisor?.direccion || 'Tu Dirección, Lima',
            logo: data?.emisor?.logo || null
        }
    } as any);

    useEffect(() => {
        onDataChange?.(editableData);
    }, [editableData, onDataChange]);

    const subtotal = editableData.suministros.reduce((acc: number, item: any) => acc + (item.precioTotal || 0), 0);
    const igv = subtotal * 0.18;
    const total = subtotal + igv;

    const handleTextChange = (path: string, value: string) => {
        const newData = { ...editableData };
        const [obj, key] = path.split('.');
        (newData as any)[obj][key] = value;
        onDataChange?.(newData);
    };

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
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '20px', borderBottom: `4px solid ${colors.primary}`, marginBottom: '30px' }}>
                        <div style={{ width: '40%' }}>
                            {editableData.emisor?.logo ? (
                                <img src={editableData.emisor.logo} alt="Logo" style={{ maxWidth: '200px', maxHeight: '90px', objectFit: 'contain' }} />
                            ) : (
                                <div style={{
                                    width: '200px',
                                    height: '90px',
                                    background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 100%)`,
                                    borderRadius: '8px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: 'white',
                                    fontWeight: 'bold',
                                    fontSize: '28px'
                                }}>
                                    {editableData.emisor?.nombre?.substring(0, 10).toUpperCase() || 'PILI'}
                                </div>
                            )}
                        </div>
                        <div style={{ width: '55%', textAlign: 'right' }}>
                            <div style={{ fontSize: '24px', fontWeight: '900', color: colors.primary, marginBottom: '5px' }}>COTIZACIÓN CORPORATIVA</div>
                            <div style={{ fontSize: '13px', color: colors.secondary, fontWeight: 'bold' }}>N° COT-CORP-{new Date().getFullYear()}-{Math.floor(Math.random() * 900) + 100}</div>
                            <div style={{ fontSize: '11px', color: '#6B7280' }}>Fecha: {new Date().toLocaleDateString('es-PE')}</div>
                        </div>
                    </div>

                    {/* CLIENT & PROJECT HEADER */}
                    <section style={{ marginBottom: '30px', display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '20px' }}>
                        <div style={{ border: `1px solid ${colors.primary}`, padding: '15px', borderRadius: '4px' }}>
                            <h3 style={{ fontSize: '12px', color: colors.primary, fontWeight: 'bold', marginBottom: '10px', textTransform: 'uppercase' }}>Información del Solicitante</h3>
                            <div style={{ fontSize: '11px', lineHeight: '1.8' }}>
                                <div><strong>Empresa:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('cliente.nombre', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.cliente.nombre}</span></div>
                                <div><strong>ID/RUC:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('cliente.ruc', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.cliente.ruc}</span></div>
                                <div><strong>Ubicación:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('cliente.direccion', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.cliente.direccion}</span></div>
                                <div><strong>Email:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('cliente.email', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.cliente.email}</span></div>
                            </div>
                        </div>
                        <div style={{ background: colors.contrast, padding: '15px', borderRadius: '4px' }}>
                            <h3 style={{ fontSize: '12px', color: colors.primary, fontWeight: 'bold', marginBottom: '10px' }}>Resumen del Servicio</h3>
                            <div style={{ fontSize: '11px', lineHeight: '1.8' }}>
                                <div><strong>Alcance:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('proyecto.nombre', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.proyecto.nombre}</span></div>
                                <div><strong>Validez:</strong> <span contentEditable={editable} suppressContentEditableWarning onBlur={e => handleTextChange('proyecto.duracion', e.currentTarget.textContent || '')} style={{ outline: 'none' }}>{editableData.proyecto.duracion}</span> días calendario</div>
                            </div>
                        </div>
                    </section>

                    {/* DESCRIPTION */}
                    <div style={{ marginBottom: '30px' }}>
                        <p style={{ fontSize: '13px', lineHeight: '1.6', color: '#374151', textAlign: 'justify' }}>
                            Presentamos la siguiente propuesta técnica-económica diseñada para satisfacer los requerimientos específicos de su organización, garantizando los más altos estándares de calidad y seguridad industrial.
                        </p>
                    </div>

                    {/* DETAILED ITEMS */}
                    <section style={{ marginBottom: '40px' }}>
                        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '11px' }}>
                            <thead>
                                <tr style={{ background: colors.primary, color: 'white' }}>
                                    <th style={{ padding: '10px', textAlign: 'center' }}>Ítem</th>
                                    <th style={{ padding: '10px', textAlign: 'left' }}>Descripción Detallada</th>
                                    <th style={{ padding: '10px', textAlign: 'center' }}>Cant.</th>
                                    <th style={{ padding: '10px', textAlign: 'right' }}>P.Unit</th>
                                    <th style={{ padding: '10px', textAlign: 'right' }}>Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                {editableData.suministros.map((item: any, i: number) => (
                                    <tr key={i} style={{ borderBottom: `1px solid ${colors.contrast}`, background: i % 2 === 0 ? 'white' : '#F9FAFB' }}>
                                        <td style={{ padding: '10px', textAlign: 'center' }}>{item.item}</td>
                                        <td style={{ padding: '10px' }}>
                                            <div style={{ fontWeight: 'bold', color: colors.primary }}>{item.descripcion}</div>
                                            <div style={{ fontSize: '9px', color: '#6B7280' }}>Unidad de medida: {item.unidad}</div>
                                        </td>
                                        <td style={{ padding: '10px', textAlign: 'center' }}>{item.cantidad}</td>
                                        <td style={{ padding: '10px', textAlign: 'right' }}>S/ {item.precioUnitario.toLocaleString()}</td>
                                        <td style={{ padding: '10px', textAlign: 'right', fontWeight: 'bold' }}>S/ {item.precioTotal.toLocaleString()}</td>
                                    </tr>
                                ))}
                            </tbody>
                            <tfoot>
                                <tr>
                                    <td colSpan={3}></td>
                                    <td style={{ padding: '10px', textAlign: 'right', fontWeight: 'bold' }}>Subtotal:</td>
                                    <td style={{ padding: '10px', textAlign: 'right' }}>S/ {subtotal.toLocaleString()}</td>
                                </tr>
                                <tr style={{ background: colors.contrast }}>
                                    <td colSpan={3}></td>
                                    <td style={{ padding: '10px', textAlign: 'right', fontWeight: 'bold' }}>IGV (18%):</td>
                                    <td style={{ padding: '10px', textAlign: 'right' }}>S/ {igv.toLocaleString()}</td>
                                </tr>
                                <tr style={{ fontWeight: 'bold', fontSize: '14px', color: colors.primary }}>
                                    <td colSpan={3}></td>
                                    <td style={{ padding: '10px', textAlign: 'right' }}>TOTAL:</td>
                                    <td style={{ padding: '10px', textAlign: 'right' }}>S/ {total.toLocaleString()}</td>
                                </tr>
                            </tfoot>
                        </table>
                    </section>

                    {/* ENTREGABLES */}
                    <section style={{ marginBottom: '30px' }}>
                        <h2 style={{ fontSize: '14px', color: colors.primary, fontWeight: 'bold', borderBottom: `1px solid ${colors.primary}`, paddingBottom: '5px', marginBottom: '10px' }}>ENTREGABLES Y GARANTÍAS</h2>
                        <ul style={{ fontSize: '11px', lineHeight: '1.8', color: '#4B5563' }}>
                            {editableData.entregables?.map((ent: any, i: number) => (
                                <li key={i}>{typeof ent === 'string' ? ent : ent.nombre}</li>
                            ))}
                            <li>Garantía técnica de 12 meses contra defectos de fábrica.</li>
                        </ul>
                    </section>

                    {/* FOOTER */}
                    <div style={{ marginTop: '60px', paddingTop: '20px', borderTop: `2px solid ${colors.primary}`, display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: '#9CA3AF' }}>
                        <div>
                            <strong>{editableData.emisor?.empresa}</strong><br />
                            RUC: {editableData.emisor?.ruc} | {editableData.emisor?.direccion}
                        </div>
                        <div style={{ textAlign: 'right' }}>
                            Aceptado por: _________________________<br />
                            Fecha: ____/____/2026
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
