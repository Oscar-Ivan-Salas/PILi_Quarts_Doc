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
    logo?: string | null;
    fontSize?: number;
    onDataChange?: (data: DocumentData) => void;
    editable?: boolean;
}

const COLOR_SCHEMES: Record<string, any> = {
    'azul-tesla': { primary: '#0052A3', secondary: '#1E40AF', accent: '#3B82F6', text: '#1f2937', contrast: '#DBEAFE' },
    'rojo-energia': { primary: '#EF4444', secondary: '#991B1B', accent: '#FCA5A5', text: '#1f2937', contrast: '#FEF2F2' },
    'verde-ecologico': { primary: '#22C55E', secondary: '#166534', accent: '#86EFAC', text: '#1f2937', contrast: '#F0FDF4' },
    'personalizado': { primary: '#8B5CF6', secondary: '#5B21B6', accent: '#C4B5FD', text: '#1f2937', contrast: '#F5F3FF' },
};

export function QuoteSimple({
    data,
    colorScheme = 'azul-tesla',
    font = 'Calibri',
    logo,
    fontSize = 11,
    onDataChange,
    editable = false,
}: QuoteSimpleProps) {
    // Fallback inteligente de colores
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
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [editableData]);

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

    // LOGIC DE LOGO: Prioridad Prop > Data > Fallback
    const logoToRender = logo || editableData.emisor?.logo;

    return (
        <div style={{ backgroundColor: '#f3f4f6', padding: '40px 0', minHeight: '100vh' }}>
            <div className="document-paper" style={{
                fontFamily: font,
                fontSize: `${fontSize}pt`, // ✅ APLICANDO TAMAÑO DE FUENTE
                maxWidth: '210mm',
                margin: '0 auto',
                background: 'white',
                boxShadow: '0 0 20px rgba(0,0,0,0.1)',
                color: '#1f2937'
            }}>
                <div style={{ padding: '20mm' }}>
                    {/* HEADER */}
                    <div className="header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', paddingBottom: '20px', borderBottom: `4px solid ${colors.primary}`, marginBottom: '30px' }}>
                        <div className="logo-section" style={{ width: '40%' }}>
                            {logoToRender ? (
                                <img src={logoToRender} alt="Logo" style={{ maxWidth: '180px', maxHeight: '80px', objectFit: 'contain' }} />
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
                            <div className="empresa-detalles" style={{ fontSize: '10px', color: '#6B7280', marginTop: '8px', lineHeight: '1.4' }}>
                                <strong>RUC: {editableData.emisor?.ruc}</strong><br />
                                {editableData.emisor?.direccion}<br />
                                {editableData.emisor?.empresa}
                            </div>
                        </div>
                        <div className="titulo-documento" style={{ width: '55%', textAlign: 'right' }}>
                            <div className="subtitulo-documento" style={{
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
                            <div className="numero-cotizacion" style={{ fontSize: '12px', marginTop: '10px', color: colors.secondary, fontWeight: 'bold' }}>
                                N° COT-SIMP-{new Date().getFullYear()}-{Math.floor(Math.random() * 900) + 100}
                            </div>
                            <div style={{ fontSize: '11px', color: '#4b5563' }}>Fecha: {new Date().toLocaleDateString('es-PE')}</div>
                        </div>
                    </div>

                    {/* CLIENT INFO - ESTRUCTURA OPTIMIZADA PARA TESLA EXCEL CONVERTER */}
                    {/* El converter espera: .info-section > 2 .info-box > p > .info-label + texto */}
                    <div className="info-section" style={{ marginBottom: '30px', background: colors.contrast, padding: '15px', borderRadius: '4px', display: 'flex', gap: '20px' }}>
                        {/* CAJA 1: Datos del Cliente */}
                        <div className="info-box" style={{ flex: '1' }}>
                            <h3 style={{ fontSize: '12px', color: colors.primary, fontWeight: 'bold', marginBottom: '8px', borderBottom: `1px solid ${colors.primary}` }}>DATOS DEL CLIENTE</h3>
                            <p style={{ margin: '4px 0', fontSize: '11px' }}>
                                <span className="info-label" style={{ fontWeight: 'bold', color: colors.primary, marginRight: '5px' }}>CLIENTE:</span>
                                <span
                                    contentEditable={editable}
                                    suppressContentEditableWarning
                                    onBlur={(e) => handleTextChange('cliente.nombre', e.currentTarget.textContent || '')}
                                >
                                    {editableData.cliente.nombre}
                                </span>
                            </p>
                            <p style={{ margin: '4px 0', fontSize: '11px' }}>
                                <span className="info-label" style={{ fontWeight: 'bold', color: colors.primary, marginRight: '5px' }}>RUC:</span>
                                <span
                                    contentEditable={editable}
                                    suppressContentEditableWarning
                                    onBlur={(e) => handleTextChange('cliente.ruc', e.currentTarget.textContent || '')}
                                >
                                    {editableData.cliente.ruc}
                                </span>
                            </p>
                            <p style={{ margin: '4px 0', fontSize: '11px' }}>
                                <span className="info-label" style={{ fontWeight: 'bold', color: colors.primary, marginRight: '5px' }}>DIRECCIÓN:</span>
                                <span
                                    contentEditable={editable}
                                    suppressContentEditableWarning
                                    onBlur={(e) => handleTextChange('cliente.direccion', e.currentTarget.textContent || '')}
                                >
                                    {editableData.cliente.direccion}
                                </span>
                            </p>
                        </div>

                        {/* CAJA 2: Datos del Proyecto */}
                        <div className="info-box" style={{ flex: '1' }}>
                            <h3 style={{ fontSize: '12px', color: colors.primary, fontWeight: 'bold', marginBottom: '8px', borderBottom: `1px solid ${colors.primary}` }}>DETALLES GENERALES</h3>
                            <p style={{ margin: '4px 0', fontSize: '11px' }}>
                                <span className="info-label" style={{ fontWeight: 'bold', color: colors.primary, marginRight: '5px' }}>PROYECTO:</span>
                                <span
                                    contentEditable={editable}
                                    suppressContentEditableWarning
                                    onBlur={(e) => handleTextChange('proyecto.nombre', e.currentTarget.textContent || '')}
                                >
                                    {editableData.proyecto.nombre}
                                </span>
                            </p>
                            <p style={{ margin: '4px 0', fontSize: '11px' }}>
                                <span className="info-label" style={{ fontWeight: 'bold', color: colors.primary, marginRight: '5px' }}>VIGENCIA:</span>
                                <span
                                    contentEditable={editable}
                                    suppressContentEditableWarning
                                    onBlur={(e) => handleTextChange('proyecto.duracion', e.currentTarget.textContent || '')}
                                >
                                    {editableData.proyecto.duracion} días
                                </span>
                            </p>
                            <p style={{ margin: '4px 0', fontSize: '11px' }}>
                                <span className="info-label" style={{ fontWeight: 'bold', color: colors.primary, marginRight: '5px' }}>FECHA:</span>
                                <span>{new Date().toLocaleDateString('es-PE')}</span>
                            </p>
                        </div>
                    </div>

                    {/* ITEMS TABLE */}
                    {/* ITEMS TABLE */}
                    <div className="tabla-section" style={{ marginBottom: '40px' }}>
                        <table className="items-table" style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
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
                    <div className="totales-section" style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '40px' }}>
                        <table style={{ width: '250px', fontSize: '12px', borderCollapse: 'collapse' }}>
                            <tbody>
                                <tr className="totales-row">
                                    <td className="totales-label" style={{ padding: '8px', borderBottom: `1px solid ${colors.contrast}` }}><strong>SUBTOTAL:</strong></td>
                                    <td className="totales-valor" style={{ padding: '8px', textAlign: 'right', borderBottom: `1px solid ${colors.contrast}` }}>S/ {subtotal.toFixed(2)}</td>
                                </tr>
                                <tr className="totales-row">
                                    <td className="totales-label" style={{ padding: '8px', borderBottom: `1px solid ${colors.contrast}` }}><strong>IGV (18%):</strong></td>
                                    <td className="totales-valor" style={{ padding: '8px', textAlign: 'right', borderBottom: `1px solid ${colors.contrast}` }}>S/ {igv.toFixed(2)}</td>
                                </tr>
                                <tr className="totales-row" style={{ background: colors.primary, color: 'white' }}>
                                    <td className="totales-label" style={{ padding: '10px' }}><strong>TOTAL:</strong></td>
                                    <td className="totales-valor" style={{ padding: '10px', textAlign: 'right', fontWeight: '900', fontSize: '14px' }}>S/ {total.toFixed(2)}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    {/* CONDITIONS */}
                    <div className="seccion" style={{ fontSize: '11px', color: '#4B5563', borderTop: `1px solid ${colors.contrast}`, paddingTop: '20px' }}>
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
