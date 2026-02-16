/**
 * ProjectSimple - Editable Simple Project Document
 * 
 * Modern TypeScript version with:
 * - Type safety
 * - Clean code principles
 * - Reusable components
 * - Color scheme support
 * - Logo customization
 */
import { useState, useEffect } from 'react';
import { useDocumentStore, type DocumentData, type ColorScheme } from '../../store/useDocumentStore';

interface ProjectSimpleProps {
    data?: Partial<DocumentData>;
    colorScheme?: ColorScheme;
    logo?: string | null;
    font?: string;
    onDataChange?: (data: DocumentData) => void;
}

// Color schemes
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

export function ProjectSimple({
    data,
    colorScheme = 'azul-tesla',
    logo = null,
    font = 'Calibri',
    onDataChange,
}: ProjectSimpleProps) {
    const colors = COLOR_SCHEMES[colorScheme];

    // Local state for editing
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
            descripcion: data?.proyecto?.descripcion || 'Resumen ejecutivo del proyecto...',
            ubicacion: data?.proyecto?.ubicacion || '',
            presupuesto: data?.proyecto?.presupuesto || 0,
            duracion: data?.proyecto?.duracion || 12,
            fechaInicio: data?.proyecto?.fechaInicio || new Date().toISOString().split('T')[0],
            fechaFin: data?.proyecto?.fechaFin || '',
        },
        profesionales: data?.profesionales || [],
        suministros: data?.suministros || [],
        entregables: data?.entregables || [],
        fases: data?.fases || [
            {
                nombre: 'Fase 1: Planificación',
                descripcion: 'Descripción de la fase...',
                duracion: 2,
                presupuesto: 0,
                actividades: [],
            },
        ],
    });

    // Notify parent of changes
    useEffect(() => {
        onDataChange?.(editableData);
    }, [editableData, onDataChange]);

    // Update phase
    const updatePhase = (index: number, field: string, value: any) => {
        const newPhases = [...(editableData.fases || [])];
        newPhases[index] = { ...newPhases[index], [field]: value };
        setEditableData({ ...editableData, fases: newPhases });
    };

    // Add phase
    const addPhase = () => {
        setEditableData({
            ...editableData,
            fases: [
                ...(editableData.fases || []),
                {
                    nombre: 'Nueva Fase',
                    descripcion: '',
                    duracion: 1,
                    presupuesto: 0,
                    actividades: [],
                },
            ],
        });
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
                    alignItems: 'flex-start',
                    marginBottom: '30px',
                    paddingBottom: '20px',
                    borderBottom: `4px solid ${colors.primary}`,
                }}
            >
                {/* Logo */}
                <div style={{ width: '35%' }}>
                    {logo ? (
                        <img
                            src={logo}
                            alt="Logo"
                            style={{
                                width: '180px',
                                height: '80px',
                                objectFit: 'contain',
                                borderRadius: '8px',
                            }}
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

                {/* Company Info */}
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

            {/* TITLE */}
            <div
                style={{
                    textAlign: 'center',
                    margin: '30px 0',
                    padding: '25px',
                    background: `linear-gradient(135deg, ${colors.light} 0%, ${colors.lightBorder} 100%)`,
                    borderLeft: `6px solid ${colors.primary}`,
                    borderRadius: '4px',
                }}
            >
                <h1
                    style={{
                        fontSize: '30px',
                        color: colors.primary,
                        fontWeight: 'bold',
                        marginBottom: '8px',
                    }}
                >
                    PROYECTO DE SERVICIOS
                </h1>
                <div style={{ fontSize: '16px', color: colors.secondary, fontWeight: '600' }}>
                    Fecha: {new Date().toLocaleDateString('es-PE')}
                </div>
            </div>

            {/* GENERAL INFO */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', margin: '25px 0' }}>
                <div
                    style={{
                        padding: '15px',
                        border: `2px solid ${colors.lightBorder}`,
                        borderRadius: '6px',
                        background: '#F9FAFB',
                    }}
                >
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

                <div
                    style={{
                        padding: '15px',
                        border: `2px solid ${colors.lightBorder}`,
                        borderRadius: '6px',
                        background: '#F9FAFB',
                    }}
                >
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
                        Datos del Proyecto
                    </h3>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colors.secondary }}>Fecha Inicio:</strong>{' '}
                        {editableData.proyecto.fechaInicio}
                    </p>
                    <p style={{ fontSize: '12px', margin: '5px 0' }}>
                        <strong style={{ color: colors.secondary }}>Duración:</strong> {editableData.proyecto.duracion}{' '}
                        semanas
                    </p>
                </div>
            </div>

            {/* EXECUTIVE SUMMARY */}
            <div
                style={{
                    margin: '30px 0',
                    padding: '25px',
                    background: `linear-gradient(135deg, ${colors.light} 0%, ${colors.lightBorder} 100%)`,
                    borderLeft: `6px solid ${colors.primary}`,
                    borderRadius: '4px',
                }}
            >
                <h3
                    style={{
                        fontSize: '18px',
                        color: colors.primary,
                        marginBottom: '15px',
                        textTransform: 'uppercase',
                    }}
                >
                    Resumen del Proyecto
                </h3>
                <textarea
                    value={editableData.proyecto.descripcion}
                    onChange={(e) =>
                        setEditableData({
                            ...editableData,
                            proyecto: { ...editableData.proyecto, descripcion: e.target.value },
                        })
                    }
                    style={{
                        width: '100%',
                        minHeight: '100px',
                        fontSize: '13px',
                        lineHeight: '1.8',
                        border: `1px solid ${colors.lightBorder}`,
                        borderRadius: '4px',
                        padding: '10px',
                        background: 'white',
                    }}
                />
            </div>

            {/* PROJECT PHASES */}
            <div style={{ margin: '35px 0' }}>
                <h2
                    style={{
                        fontSize: '20px',
                        color: colors.primary,
                        marginBottom: '20px',
                        paddingBottom: '10px',
                        borderBottom: `3px solid ${colors.primary}`,
                    }}
                >
                    FASES DEL PROYECTO
                </h2>
                <p style={{ fontSize: '12px', color: '#374151', lineHeight: '1.8', marginBottom: '20px' }}>
                    El proyecto se desarrollará en las siguientes fases principales:
                </p>
                {editableData.fases?.map((fase, index) => (
                    <div
                        key={index}
                        style={{
                            margin: '15px 0',
                            padding: '15px',
                            background: '#F9FAFB',
                            borderLeft: `4px solid ${colors.primary}`,
                            borderRadius: '4px',
                        }}
                    >
                        <div style={{ marginBottom: '10px' }}>
                            <strong style={{ color: colors.primary }}>Fase {index + 1}:</strong>{' '}
                            <input
                                type="text"
                                value={fase.nombre}
                                onChange={(e) => updatePhase(index, 'nombre', e.target.value)}
                                style={{
                                    border: 'none',
                                    borderBottom: `1px solid ${colors.accent}`,
                                    background: 'transparent',
                                    fontSize: '12px',
                                    width: '60%',
                                    fontWeight: 'bold',
                                }}
                            />
                        </div>
                        <div style={{ marginBottom: '8px' }}>
                            <strong style={{ fontSize: '11px', color: colors.secondary }}>Descripción:</strong>
                            <textarea
                                value={fase.descripcion}
                                onChange={(e) => updatePhase(index, 'descripcion', e.target.value)}
                                style={{
                                    width: '100%',
                                    minHeight: '60px',
                                    fontSize: '11px',
                                    border: `1px solid ${colors.lightBorder}`,
                                    borderRadius: '4px',
                                    padding: '8px',
                                    marginTop: '5px',
                                }}
                            />
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '11px' }}>
                            <div>
                                <strong style={{ color: colors.secondary }}>Duración:</strong>{' '}
                                <input
                                    type="number"
                                    value={fase.duracion}
                                    onChange={(e) => updatePhase(index, 'duracion', parseInt(e.target.value))}
                                    style={{
                                        border: 'none',
                                        borderBottom: `1px solid ${colors.accent}`,
                                        background: 'transparent',
                                        fontSize: '11px',
                                        width: '100px',
                                    }}
                                />{' '}
                                semanas
                            </div>
                        </div>
                    </div>
                ))}
                <button
                    onClick={addPhase}
                    style={{
                        marginTop: '10px',
                        padding: '8px 16px',
                        background: colors.primary,
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '12px',
                    }}
                >
                    + Agregar Fase
                </button>
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
