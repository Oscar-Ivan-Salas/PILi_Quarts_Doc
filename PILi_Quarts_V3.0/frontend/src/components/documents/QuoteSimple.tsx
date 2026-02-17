/**
 * QuoteSimple - Editable Simple Quote Document
 * 
 * ALINEACIÓN FIDELIDAD TOTAL: PLANTILLA_HTML_COTIZACION_SIMPLE.html
 */
import { useState, useEffect } from 'react';
import type { DocumentData, ColorScheme } from '../../store/useDocumentStore';

interface QuoteSimpleProps {
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

export function QuoteSimple({
    data,
    colorScheme = 'azul-tesla',
    font = 'Calibri',
    onDataChange,
    editable = false,
}: QuoteSimpleProps) {
    const colors = COLOR_SCHEMES[colorScheme] || COLOR_SCHEMES['azul-tesla'];

    const [editableData] = useState<DocumentData>({
        cliente: {
            nombre: data?.cliente?.nombre || 'CLIENTE EJEMPLO S.A.C.',
            ruc: data?.cliente?.ruc || '20123456789',
            direccion: data?.cliente?.direccion || 'Av. Los Próceres 456, Surco',
            telefono: data?.cliente?.telefono || '01 444 5555',
            email: data?.cliente?.email || 'compras@cliente.com',
        },
        proyecto: {
            nombre: data?.proyecto?.nombre || 'SUMINISTRO DE COMPONENTES ELÉCTRICOS',
            descripcion: data?.proyecto?.descripcion || 'Cotización de materiales según requerimiento.',
            duracion: data?.proyecto?.duracion || 15, // Días de vigencia
        },
        suministros: data?.suministros || [
            { item: '01', descripcion: 'Interruptor Termomagnético 3x20A', cantidad: 5, unidad: 'und', precioUnitario: 45, precioTotal: 225 },
            { item: '02', descripcion: 'Cable Vulcanizado 3x14 AWG x 100m', cantidad: 2, unidad: 'rll', precioUnitario: 350, precioTotal: 700 }
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
        const keys = path.split('.');
        let current: any = newData;
        for (let i = 0; i < keys.length - 1; i++) {
            current = current[keys[i]];
        }
        current[keys[keys.length - 1]] = value;
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
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', paddingBottom: '20px', borderBottom: `4px solid ${colors.primary}`, marginBottom: '30px' }}>
                        <div style={{ width: '40%' }}>
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
                            <div style={{ fontSize: '10px', color: '#6B7280', marginTop: '8px', lineHeight: '1.4' }}>
                                <strong>RUC: {editableData.emisor?.ruc}</strong><br />
                                {editableData.emisor?.direccion}<br />
                                {editableData.emisor?.empresa}
                            </div>
                        </div>
                        <div style={{ width: '55%', textAlign: 'right' }}>
                            <div style={{
                                fontSize: '22px',
                                fontWeight: '900',
                                color: colors.primary,
                                marginBottom: '5px',
                                border: `2px solid ${colors.primary}`,
                                padding: '10px',
                                borderRadius: '4px',
                                display: 'inline-block'
                            }}>
                                COTIZACIÓN SIMPLE
                            </div>
                            <div style={{ fontSize: '12px', marginTop: '10px', color: colors.secondary, fontWeight: 'bold' }}>
                                N° COT-SIMP-{new Date().getFullYear()}-{Math.floor(Math.random() * 900) + 100}
                            </div>
                            <div style={{ fontSize: '11px', color: '#4b5563' }}>Fecha: {new Date().toLocaleDateString('es-PE')}</div>
                        </div>
                    </div>

                    {/* CLIENT INFO */}
                    <div style={{ marginBottom: '30px', background: colors.contrast, padding: '15px', borderRadius: '4px' }}>
                        <table style={{ width: '100%', fontSize: '12px', borderCollapse: 'collapse' }}>
                            <tbody>
                                <tr>
                                    <td style={{ width: '15%', fontWeight: 'bold', color: colors.primary, padding: '4px 0' }}>CLIENTE:</td>
                                    <td
                                        style={{ width: '50%', padding: '4px 0', outline: 'none' }}
                                        contentEditable={editable}
                                        suppressContentEditableWarning
                                        onBlur={(e) => handleTextChange('cliente.nombre', e.currentTarget.textContent || '')}
                                    >
                                        {editableData.cliente.nombre}
                                    </td>
                                    <td style={{ width: '15%', fontWeight: 'bold', color: colors.primary, padding: '4px 0' }}>RUC:</td>
                                    <td
                                        style={{ width: '20%', padding: '4px 0', outline: 'none' }}
                                        contentEditable={editable}
                                        suppressContentEditableWarning
                                        onBlur={(e) => handleTextChange('cliente.ruc', e.currentTarget.textContent || '')}
                                    >
                                        {editableData.cliente.ruc}
                                    </td>
                                </tr>
                                <tr>
                                    <td style={{ fontWeight: 'bold', color: colors.primary, padding: '4px 0' }}>DIRECCIÓN:</td>
                                    <td
                                        colSpan={3}
                                        style={{ padding: '4px 0', outline: 'none' }}
                                        contentEditable={editable}
                                        suppressContentEditableWarning
                                        onBlur={(e) => handleTextChange('cliente.direccion', e.currentTarget.textContent || '')}
                                    >
                                        {editableData.cliente.direccion}
                                    </td>
                                </tr>
                                <tr>
                                    <td style={{ fontWeight: 'bold', color: colors.primary, padding: '4px 0' }}>TELÉFONO:</td>
                                    <td
                                        style={{ padding: '4px 0', outline: 'none' }}
                                        contentEditable={editable}
                                        suppressContentEditableWarning
                                        onBlur={(e) => handleTextChange('cliente.telefono', e.currentTarget.textContent || '')}
                                    >
                                        {editableData.cliente.telefono}
                                    </td>
                                    <td style={{ fontWeight: 'bold', color: colors.primary, padding: '4px 0' }}>VIGENCIA:</td>
                                    <td
                                        style={{ padding: '4px 0', outline: 'none' }}
                                        contentEditable={editable}
                                        suppressContentEditableWarning
                                        onBlur={(e) => handleTextChange('proyecto.duracion', e.currentTarget.textContent || '')}
                                    >
                                        {editableData.proyecto.duracion} Días Calendario
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    {/* ITEMS TABLE */}
                    <div style={{ marginBottom: '40px' }}>
                        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
                            <thead>
                                <tr style={{ background: colors.primary, color: 'white' }}>
                                    <th style={{ padding: '12px', textAlign: 'center', border: '1px solid white' }}>ITEM</th>
                                    <th style={{ padding: '12px', textAlign: 'left', border: '1px solid white' }}>DESCRIPCIÓN</th>
                                    <th style={{ padding: '12px', textAlign: 'center', border: '1px solid white' }}>CANT.</th>
                                    <th style={{ padding: '12px', textAlign: 'center', border: '1px solid white' }}>UND.</th>
                                    <th style={{ padding: '12px', textAlign: 'right', border: '1px solid white' }}>P. UNIT.</th>
                                    <th style={{ padding: '12px', textAlign: 'right', border: '1px solid white' }}>TOTAL</th>
                                </tr>
                            </thead>
                            <tbody>
                                {editableData.suministros.map((item: any, i: number) => (
                                    <tr key={i} style={{ borderBottom: `1px solid ${colors.contrast}` }}>
                                        <td style={{ padding: '10px', textAlign: 'center' }}>{String(i + 1).padStart(2, '0')}</td>
                                        <td style={{ padding: '10px' }}>{item.descripcion}</td>
                                        <td style={{ padding: '10px', textAlign: 'center' }}>{item.cantidad}</td>
                                        <td style={{ padding: '10px', textAlign: 'center' }}>{item.unidad}</td>
                                        <td style={{ padding: '10px', textAlign: 'right' }}>S/ {item.precioUnitario.toFixed(2)}</td>
                                        <td style={{ padding: '10px', textAlign: 'right', fontWeight: 'bold' }}>S/ {item.precioTotal.toFixed(2)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* TOTALS */}
                    <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '40px' }}>
                        <table style={{ width: '250px', fontSize: '12px', borderCollapse: 'collapse' }}>
                            <tbody>
                                <tr>
                                    <td style={{ padding: '8px', borderBottom: `1px solid ${colors.contrast}` }}><strong>SUBTOTAL:</strong></td>
                                    <td style={{ padding: '8px', textAlign: 'right', borderBottom: `1px solid ${colors.contrast}` }}>S/ {subtotal.toFixed(2)}</td>
                                </tr>
                                <tr>
                                    <td style={{ padding: '8px', borderBottom: `1px solid ${colors.contrast}` }}><strong>IGV (18%):</strong></td>
                                    <td style={{ padding: '8px', textAlign: 'right', borderBottom: `1px solid ${colors.contrast}` }}>S/ {igv.toFixed(2)}</td>
                                </tr>
                                <tr style={{ background: colors.primary, color: 'white' }}>
                                    <td style={{ padding: '10px' }}><strong>TOTAL:</strong></td>
                                    <td style={{ padding: '10px', textAlign: 'right', fontWeight: '900', fontSize: '14px' }}>S/ {total.toFixed(2)}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    {/* CONDITIONS */}
                    <div style={{ fontSize: '11px', color: '#4B5563', borderTop: `1px solid ${colors.contrast}`, paddingTop: '20px' }}>
                        <p><strong>CONDICIONES COMERCIALES:</strong></p>
                        <ul
                            style={{ paddingLeft: '20px', margin: '5px 0', outline: 'none' }}
                            contentEditable={editable}
                            suppressContentEditableWarning
                        >
                            <li>Forma de pago: Contado contra entrega.</li>
                            <li>Tiempo de entrega: Inmediato sujeto a disponibilidad.</li>
                            <li>Los precios incluyen IGV.</li>
                        </ul>
                    </div>

                    {/* FOOTER */}
                    <div style={{ marginTop: '60px', textAlign: 'center', borderTop: `1px solid ${colors.contrast}`, paddingTop: '20px' }}>
                        <div style={{ fontSize: '11px', color: colors.secondary, fontWeight: 'bold' }}>{editableData.emisor?.empresa}</div>
                        <div style={{ fontSize: '10px', color: '#9CA3AF' }}>{editableData.emisor?.direccion} | RUC: {editableData.emisor?.ruc}</div>
                    </div>
                </div>
            </div>
        </div>
    );
}
