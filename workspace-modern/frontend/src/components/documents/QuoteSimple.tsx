/**
 * QuoteSimple - Editable Simple Quote Document
 * 
 * Features:
 * - Itemized table with calculations
 * - Currency selector (PEN, USD, EUR)
 * - Subtotal, IGV, Total calculations
 * - Editable client and project info
 * - Add/remove items dynamically
 */
import { useState, useEffect } from 'react';
import { Plus, Trash2 } from 'lucide-react';
import { useDocumentStore, type DocumentData, type ColorScheme } from '../../store/useDocumentStore';

interface QuoteSimpleProps {
    data?: Partial<DocumentData>;
    colorScheme?: ColorScheme;
    logo?: string | null;
    font?: string;
    onDataChange?: (data: DocumentData) => void;
}

type Currency = 'PEN' | 'USD' | 'EUR';

const CURRENCY_SYMBOLS: Record<Currency, string> = {
    PEN: 'S/',
    USD: '$',
    EUR: '€',
};

const COLOR_SCHEMES = {
    'azul-tesla': {
        primary: '#0052A3',
        secondary: '#1E40AF',
        accent: '#3B82F6',
        light: '#EFF6FF',
        lightBorder: '#DBEAFE',
    },
    'rojo-pili': {
        primary: '#DC2626',
        secondary: '#991B1B',
        accent: '#EF4444',
        light: '#FEF2F2',
        lightBorder: '#FECACA',
    },
    'amarillo-pili': {
        primary: '#D97706',
        secondary: '#B45309',
        accent: '#F59E0B',
        light: '#FFFBEB',
        lightBorder: '#FDE68A',
    },
};

export function QuoteSimple({
    data,
    colorScheme = 'azul-tesla',
    logo = null,
    font = 'Calibri',
    onDataChange,
}: QuoteSimpleProps) {
    const colors = COLOR_SCHEMES[colorScheme];
    const [currency, setCurrency] = useState<Currency>('PEN');

    const [editableData, setEditableData] = useState<DocumentData>({
        cliente: {
            nombre: data?.cliente?.nombre || '',
            ruc: data?.cliente?.ruc || '',
            direccion: data?.cliente?.direccion || '',
            telefono: data?.cliente?.telefono || '',
            email: data?.cliente?.email || '',
        },
        proyecto: {
            nombre: data?.proyecto?.nombre || '',
            descripcion: data?.proyecto?.descripcion || '',
            ubicacion: data?.proyecto?.ubicacion || '',
            presupuesto: data?.proyecto?.presupuesto || 0,
            duracion: data?.proyecto?.duracion || 30,
            fechaInicio: data?.proyecto?.fechaInicio || new Date().toISOString().split('T')[0],
            fechaFin: data?.proyecto?.fechaFin || '',
        },
        profesionales: [],
        suministros: data?.suministros || [
            {
                item: '01',
                descripcion: 'Tablero eléctrico',
                cantidad: 1,
                unidad: 'und',
                precioUnitario: 450,
                precioTotal: 450,
            },
        ],
        entregables: [],
    });

    // Calculate totals
    const calculateTotals = () => {
        const subtotal = editableData.suministros.reduce(
            (sum, item) => sum + (item.cantidad * item.precioUnitario),
            0
        );
        const igv = subtotal * 0.18;
        const total = subtotal + igv;

        return {
            subtotal: subtotal.toFixed(2),
            igv: igv.toFixed(2),
            total: total.toFixed(2),
        };
    };

    const totals = calculateTotals();

    // Notify parent of changes
    useEffect(() => {
        onDataChange?.({ ...editableData });
    }, [editableData, onDataChange]);

    // Update item
    const updateItem = (index: number, field: string, value: any) => {
        const newSupplies = [...editableData.suministros];
        newSupplies[index] = {
            ...newSupplies[index],
            [field]: field === 'descripcion' || field === 'unidad' ? value : parseFloat(value) || 0,
        };

        // Recalculate total for this item
        if (field === 'cantidad' || field === 'precioUnitario') {
            newSupplies[index].precioTotal = newSupplies[index].cantidad * newSupplies[index].precioUnitario;
        }

        setEditableData({ ...editableData, suministros: newSupplies });
    };

    // Add item
    const addItem = () => {
        setEditableData({
            ...editableData,
            suministros: [
                ...editableData.suministros,
                {
                    item: String(editableData.suministros.length + 1).padStart(2, '0'),
                    descripcion: '',
                    cantidad: 1,
                    unidad: 'und',
                    precioUnitario: 0,
                    precioTotal: 0,
                },
            ],
        });
    };

    // Remove last item
    const removeLastItem = () => {
        if (editableData.suministros.length > 1) {
            setEditableData({
                ...editableData,
                suministros: editableData.suministros.slice(0, -1),
            });
        }
    };

    return (
        <div
            style={{
                fontFamily: font,
                maxWidth: '210mm',
                margin: '0 auto',
                padding: '20mm',
                background: 'white',
                color: '#1f2937',
                lineHeight: '1.6',
            }}
        >
            {/* HEADER */}
            <div
                style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    marginBottom: '30px',
                    paddingBottom: '20px',
                    borderBottom: `4px solid ${colors.primary}`,
                }}
            >
                <div style={{ width: '35%' }}>
                    {logo ? (
                        <img
                            src={logo}
                            alt="Logo"
                            style={{ width: '180px', height: '80px', objectFit: 'contain', borderRadius: '8px' }}
                        />
                    ) : (
                        <div
                            style={{
                                width: '180px',
                                height: '80px',
                                background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 100%)`,
                                borderRadius: '8px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: 'white',
                                fontWeight: 'bold',
                                fontSize: '24px',
                            }}
                        >
                            PILi
                        </div>
                    )}
                </div>

                <div style={{ width: '65%', textAlign: 'right' }}>
                    <div
                        style={{
                            fontSize: '20px',
                            fontWeight: 'bold',
                            color: colors.primary,
                            marginBottom: '8px',
                            textTransform: 'uppercase',
                        }}
                    >
                        PILi QUARTS - INGENIERÍA Y PROYECTOS
                    </div>
                    <div style={{ fontSize: '11px', color: '#4b5563', lineHeight: '1.5' }}>
                        <div>RUC: 20601138787</div>
                        <div>Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos, SJL</div>
                        <div>Teléfono: 906 315 961</div>
                        <div>Email: contacto@piliquarts.com</div>
                    </div>
                </div>
            </div>

            {/* CURRENCY SELECTOR */}
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '20px', gap: '10px', alignItems: 'center' }}>
                <span style={{ fontSize: '12px', fontWeight: '600', color: colors.secondary }}>Moneda:</span>
                {(['PEN', 'USD', 'EUR'] as Currency[]).map((curr) => (
                    <button
                        key={curr}
                        onClick={() => setCurrency(curr)}
                        style={{
                            padding: '6px 12px',
                            background: currency === curr ? colors.primary : '#E5E7EB',
                            color: currency === curr ? 'white' : '#6B7280',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontSize: '11px',
                            fontWeight: '600',
                        }}
                    >
                        {CURRENCY_SYMBOLS[curr]} {curr}
                    </button>
                ))}
            </div>

            {/* TITLE */}
            <div
                style={{
                    textAlign: 'center',
                    margin: '30px 0',
                    padding: '20px',
                    background: `linear-gradient(135deg, ${colors.light} 0%, ${colors.lightBorder} 100%)`,
                    borderLeft: `6px solid ${colors.primary}`,
                    borderRadius: '4px',
                }}
            >
                <h1 style={{ fontSize: '28px', color: colors.primary, fontWeight: 'bold', marginBottom: '8px' }}>
                    COTIZACIÓN DE SERVICIOS
                </h1>
                <div style={{ fontSize: '16px', color: colors.secondary, fontWeight: '600' }}>
                    N° COT-{new Date().getFullYear()}-001
                </div>
            </div>

            {/* CLIENT INFO */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', margin: '25px 0' }}>
                <div style={{ padding: '15px', border: `2px solid ${colors.lightBorder}`, borderRadius: '6px', background: '#F9FAFB' }}>
                    <h3
                        style={{
                            fontSize: '14px',
                            color: colors.primary,
                            fontWeight: 'bold',
                            marginBottom: '10px',
                            textTransform: 'uppercase',
                            borderBottom: `2px solid ${colors.primary}`,
                            paddingBottom: '5px',
                        }}
                    >
                        Datos del Cliente
                    </h3>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colors.secondary }}>Cliente:</strong>{' '}
                        <input
                            type="text"
                            value={editableData.cliente.nombre}
                            onChange={(e) =>
                                setEditableData({
                                    ...editableData,
                                    cliente: { ...editableData.cliente, nombre: e.target.value },
                                })
                            }
                            style={{
                                border: 'none',
                                borderBottom: `1px solid ${colors.accent}`,
                                background: 'transparent',
                                fontSize: '12px',
                                width: '70%',
                            }}
                        />
                    </p>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colors.secondary }}>Proyecto:</strong>{' '}
                        <input
                            type="text"
                            value={editableData.proyecto.nombre}
                            onChange={(e) =>
                                setEditableData({
                                    ...editableData,
                                    proyecto: { ...editableData.proyecto, nombre: e.target.value },
                                })
                            }
                            style={{
                                border: 'none',
                                borderBottom: `1px solid ${colors.accent}`,
                                background: 'transparent',
                                fontSize: '12px',
                                width: '70%',
                            }}
                        />
                    </p>
                </div>

                <div style={{ padding: '15px', border: `2px solid ${colors.lightBorder}`, borderRadius: '6px', background: '#F9FAFB' }}>
                    <h3
                        style={{
                            fontSize: '14px',
                            color: colors.primary,
                            fontWeight: 'bold',
                            marginBottom: '10px',
                            textTransform: 'uppercase',
                            borderBottom: `2px solid ${colors.primary}`,
                            paddingBottom: '5px',
                        }}
                    >
                        Datos de la Cotización
                    </h3>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colors.secondary }}>Fecha:</strong> {new Date().toLocaleDateString('es-PE')}
                    </p>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colors.secondary }}>Vigencia:</strong> {editableData.proyecto.duracion} días
                    </p>
                </div>
            </div>

            {/* ITEMS TABLE */}
            <div style={{ margin: '30px 0' }}>
                <h2
                    style={{
                        fontSize: '18px',
                        color: colors.primary,
                        marginBottom: '15px',
                        paddingBottom: '8px',
                        borderBottom: `3px solid ${colors.primary}`,
                    }}
                >
                    Detalle de la Cotización
                </h2>
                <table style={{ width: '100%', borderCollapse: 'collapse', margin: '15px 0', boxShadow: '0 2px 8px rgba(0, 82, 163, 0.1)' }}>
                    <thead style={{ background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 100%)`, color: 'white' }}>
                        <tr>
                            <th style={{ padding: '14px 10px', textAlign: 'left', fontSize: '12px', fontWeight: '700', width: '8%' }}>ITEM</th>
                            <th style={{ padding: '14px 10px', textAlign: 'left', fontSize: '12px', fontWeight: '700', width: '42%' }}>DESCRIPCIÓN</th>
                            <th style={{ padding: '14px 10px', textAlign: 'right', fontSize: '12px', fontWeight: '700', width: '10%' }}>CANT.</th>
                            <th style={{ padding: '14px 10px', textAlign: 'right', fontSize: '12px', fontWeight: '700', width: '10%' }}>UNIDAD</th>
                            <th style={{ padding: '14px 10px', textAlign: 'right', fontSize: '12px', fontWeight: '700', width: '15%' }}>P. UNIT.</th>
                            <th style={{ padding: '14px 10px', textAlign: 'right', fontSize: '12px', fontWeight: '700', width: '15%' }}>TOTAL</th>
                        </tr>
                    </thead>
                    <tbody>
                        {editableData.suministros.map((item, index) => (
                            <tr key={index} style={{ borderBottom: '1px solid #E5E7EB', background: index % 2 === 0 ? '#F9FAFB' : 'white' }}>
                                <td style={{ padding: '12px 10px', textAlign: 'center', fontSize: '11px' }}>
                                    {String(index + 1).padStart(2, '0')}
                                </td>
                                <td style={{ padding: '12px 10px', fontSize: '11px' }}>
                                    <input
                                        type="text"
                                        value={item.descripcion}
                                        onChange={(e) => updateItem(index, 'descripcion', e.target.value)}
                                        style={{ width: '100%', border: 'none', background: 'transparent', fontSize: '11px' }}
                                    />
                                </td>
                                <td style={{ padding: '12px 10px', textAlign: 'right', fontSize: '11px' }}>
                                    <input
                                        type="number"
                                        value={item.cantidad}
                                        onChange={(e) => updateItem(index, 'cantidad', e.target.value)}
                                        style={{ width: '60px', border: 'none', background: 'transparent', fontSize: '11px', textAlign: 'right' }}
                                    />
                                </td>
                                <td style={{ padding: '12px 10px', textAlign: 'right', fontSize: '11px' }}>
                                    <input
                                        type="text"
                                        value={item.unidad}
                                        onChange={(e) => updateItem(index, 'unidad', e.target.value)}
                                        style={{ width: '50px', border: 'none', background: 'transparent', fontSize: '11px', textAlign: 'right' }}
                                    />
                                </td>
                                <td style={{ padding: '12px 10px', textAlign: 'right', fontSize: '11px' }}>
                                    {CURRENCY_SYMBOLS[currency]}{' '}
                                    <input
                                        type="number"
                                        value={item.precioUnitario}
                                        onChange={(e) => updateItem(index, 'precioUnitario', e.target.value)}
                                        style={{ width: '80px', border: 'none', background: 'transparent', fontSize: '11px', textAlign: 'right' }}
                                    />
                                </td>
                                <td style={{ padding: '12px 10px', textAlign: 'right', fontSize: '11px', fontWeight: '600' }}>
                                    {CURRENCY_SYMBOLS[currency]} {item.precioTotal.toFixed(2)}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                <div style={{ marginTop: '10px', display: 'flex', gap: '10px' }}>
                    <button
                        onClick={addItem}
                        style={{
                            padding: '8px 16px',
                            background: colors.primary,
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontSize: '12px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px',
                        }}
                    >
                        + Agregar Item
                    </button>
                    {editableData.suministros.length > 1 && (
                        <button
                            onClick={removeLastItem}
                            style={{
                                padding: '8px 16px',
                                background: '#DC2626',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: 'pointer',
                                fontSize: '12px',
                            }}
                        >
                            - Eliminar Último
                        </button>
                    )}
                </div>
            </div>

            {/* TOTALS */}
            <div style={{ marginTop: '25px', display: 'flex', justifyContent: 'flex-end' }}>
                <div style={{ width: '350px', border: `2px solid ${colors.primary}`, borderRadius: '6px', overflow: 'hidden' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 20px', borderBottom: `1px solid ${colors.lightBorder}` }}>
                        <span style={{ fontWeight: '600', color: colors.secondary }}>SUBTOTAL:</span>
                        <span style={{ fontWeight: '700', color: colors.primary }}>
                            {CURRENCY_SYMBOLS[currency]} {totals.subtotal}
                        </span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 20px', borderBottom: `1px solid ${colors.lightBorder}` }}>
                        <span style={{ fontWeight: '600', color: colors.secondary }}>IGV (18%):</span>
                        <span style={{ fontWeight: '700', color: colors.primary }}>
                            {CURRENCY_SYMBOLS[currency]} {totals.igv}
                        </span>
                    </div>
                    <div
                        style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            padding: '12px 20px',
                            background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 100%)`,
                            color: 'white',
                            fontWeight: 'bold',
                            fontSize: '16px',
                        }}
                    >
                        <span>TOTAL:</span>
                        <span>
                            {CURRENCY_SYMBOLS[currency]} {totals.total}
                        </span>
                    </div>
                </div>
            </div>

            {/* FOOTER */}
            <div
                style={{
                    marginTop: '40px',
                    paddingTop: '20px',
                    borderTop: `3px solid ${colors.primary}`,
                    textAlign: 'center',
                    fontSize: '10px',
                    color: '#6B7280',
                }}
            >
                <div style={{ fontWeight: 'bold', color: colors.primary, fontSize: '12px', marginBottom: '8px' }}>
                    PILi QUARTS - INGENIERÍA Y PROYECTOS
                </div>
                <div style={{ margin: '5px 0' }}>RUC: 20601138787 | Teléfono: 906 315 961</div>
                <div style={{ margin: '5px 0' }}>Email: contacto@piliquarts.com</div>
            </div>
        </div>
    );
}
