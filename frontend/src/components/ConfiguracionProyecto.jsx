import React, { useState, useEffect } from 'react';
import { Calendar, DollarSign, Network, Clock, CheckCircle2, Building2 } from 'lucide-react';

const ConfiguracionProyecto = ({ onConfigChange, initialData }) => {
    // Estado local para la configuración
    const [config, setConfig] = useState({
        nombre_proyecto: initialData?.nombre_proyecto || '',
        presupuesto: initialData?.presupuesto || 50000,
        moneda: initialData?.moneda || 'S/',
        fecha_inicio: initialData?.fecha_inicio || new Date().toISOString().split('T')[0],
        duracion_total: initialData?.duracion_total || 120, // Días
        tipo_calendario: 'habiles', // 'habiles' o 'calendario'
        fases: {
            acta: true,
            stakeholders: true,
            riesgos: true,
            cronograma: true,
            calidad: true,
            comunicaciones: true,
            cierre: true
        }
    });

    // Notificar cambios al padre (App.jsx)
    useEffect(() => {
        if (onConfigChange) {
            onConfigChange(config);
        }
    }, [config, onConfigChange]);

    // Estilos (Inline para Glassmorphism rápido y robusto)
    const styles = {
        container: {
            background: 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)',
            padding: '30px',
            borderRadius: '16px',
            color: 'white',
            fontFamily: "'Inter', sans-serif",
            boxShadow: '0 20px 50px rgba(0,0,0,0.5)',
            border: '1px solid rgba(255,255,255,0.1)',
            marginBottom: '2rem'
        },
        header: {
            marginBottom: '25px',
            borderBottom: '1px solid rgba(255,255,255,0.1)',
            paddingBottom: '15px',
            display: 'flex',
            alignItems: 'center',
            gap: '15px'
        },
        grid: {
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '20px'
        },
        card: {
            background: 'rgba(255, 255, 255, 0.05)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '12px',
            padding: '20px',
            display: 'flex',
            flexDirection: 'column',
            gap: '15px'
        },
        inputGroup: {
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
        },
        label: {
            fontSize: '12px',
            color: '#94a3b8',
            fontWeight: '600',
            textTransform: 'uppercase',
            letterSpacing: '0.5px'
        },
        input: {
            background: 'rgba(0, 0, 0, 0.2)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '8px',
            padding: '12px',
            color: 'white',
            fontSize: '14px',
            outline: 'none',
            transition: 'border-color 0.3s'
        },
        sliderContainer: {
            marginTop: '10px'
        },
        toggleRow: {
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '8px 0',
            borderBottom: '1px solid rgba(255,255,255,0.05)'
        },
        toggle: (active) => ({
            width: '40px',
            height: '20px',
            background: active ? '#3b82f6' : '#334155',
            borderRadius: '20px',
            position: 'relative',
            cursor: 'pointer',
            transition: 'background 0.3s'
        }),
        toggleKnob: (active) => ({
            width: '16px',
            height: '16px',
            background: 'white',
            borderRadius: '50%',
            position: 'absolute',
            top: '2px',
            left: active ? '22px' : '2px',
            transition: 'left 0.3s'
        })
    };

    return (
        <div style={styles.container}>
            <div style={styles.header}>
                <div style={{ padding: '10px', background: 'rgba(59, 130, 246, 0.2)', borderRadius: '8px' }}>
                    <Network size={24} color="#60a5fa" />
                </div>
                <div>
                    <h2 style={{ margin: 0, fontSize: '20px', fontWeight: 'bold' }}>Configuración del Proyecto</h2>
                    <p style={{ margin: 0, fontSize: '13px', color: '#94a3b8' }}>Define los parámetros maestros para el cálculo PMI</p>
                </div>
            </div>

            <div style={styles.grid}>
                {/* PANEL 1: IDENTIDAD */}
                <div style={styles.card}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                        <Building2 color="#a78bfa" /> <span style={{ fontWeight: 'bold', color: '#e2e8f0' }}>Identidad</span>
                    </div>

                    <div style={styles.inputGroup}>
                        <label style={styles.label}>Nombre del Proyecto</label>
                        <input
                            type="text"
                            style={styles.input}
                            value={config.nombre_proyecto}
                            onChange={(e) => setConfig({ ...config, nombre_proyecto: e.target.value })}
                            placeholder="Ej. Construcción Torre A"
                        />
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                        <div style={styles.inputGroup}>
                            <label style={styles.label}>Presupuesto</label>
                            <input
                                type="number"
                                style={styles.input}
                                value={config.presupuesto}
                                onChange={(e) => setConfig({ ...config, presupuesto: e.target.value })}
                            />
                        </div>
                        <div style={styles.inputGroup}>
                            <label style={styles.label}>Moneda</label>
                            <select
                                style={styles.input}
                                value={config.moneda}
                                onChange={(e) => setConfig({ ...config, moneda: e.target.value })}
                            >
                                <option value="S/">S/ (Soles)</option>
                                <option value="$">$ (USD)</option>
                                <option value="€">€ (EUR)</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* PANEL 2: CRONOGRAMA */}
                <div style={styles.card}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                        <Clock color="#38bdf8" /> <span style={{ fontWeight: 'bold', color: '#e2e8f0' }}>Cronograma Maestro</span>
                    </div>

                    <div style={styles.inputGroup}>
                        <label style={styles.label}>Fecha de Inicio</label>
                        <input
                            type="date"
                            style={styles.input}
                            value={config.fecha_inicio}
                            onChange={(e) => setConfig({ ...config, fecha_inicio: e.target.value })}
                        />
                    </div>

                    <div style={styles.sliderContainer}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                            <label style={styles.label}>Duración Total</label>
                            <span style={{ fontSize: '14px', fontWeight: 'bold', color: '#60a5fa' }}>{config.duracion_total} días</span>
                        </div>
                        <input
                            type="range"
                            min="10"
                            max="720"
                            step="1"
                            value={config.duracion_total}
                            onChange={(e) => setConfig({ ...config, duracion_total: e.target.value })}
                            style={{ width: '100%', cursor: 'pointer', accentColor: '#3b82f6' }}
                        />
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: '#64748b', marginTop: '4px' }}>
                            <span>10 días</span>
                            <span>2 años</span>
                        </div>
                    </div>

                    <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                        <button
                            onClick={() => setConfig({ ...config, tipo_calendario: 'habiles' })}
                            style={{ flex: 1, padding: '8px', borderRadius: '6px', border: 'none', background: config.tipo_calendario === 'habiles' ? '#3b82f6' : 'rgba(255,255,255,0.05)', color: 'white', cursor: 'pointer', fontSize: '12px' }}
                        >
                            Días Hábiles
                        </button>
                        <button
                            onClick={() => setConfig({ ...config, tipo_calendario: 'calendario' })}
                            style={{ flex: 1, padding: '8px', borderRadius: '6px', border: 'none', background: config.tipo_calendario === 'calendario' ? '#3b82f6' : 'rgba(255,255,255,0.05)', color: 'white', cursor: 'pointer', fontSize: '12px' }}
                        >
                            Días Calendario
                        </button>
                    </div>
                </div>

                {/* PANEL 3: ALCANCE */}
                <div style={styles.card}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                        <CheckCircle2 color="#34d399" /> <span style={{ fontWeight: 'bold', color: '#e2e8f0' }}>Alcance (Fases PMI)</span>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '5px', overflowY: 'auto', maxHeight: '180px' }}>
                        {Object.keys(config.fases).map((fase) => (
                            <div key={fase} style={styles.toggleRow}>
                                <span style={{ fontSize: '13px', textTransform: 'capitalize', color: '#cbd5e1' }}>{fase.replace('_', ' ')}</span>
                                <div
                                    style={styles.toggle(config.fases[fase])}
                                    onClick={() => setConfig({
                                        ...config,
                                        fases: { ...config.fases, [fase]: !config.fases[fase] }
                                    })}
                                >
                                    <div style={styles.toggleKnob(config.fases[fase])}></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ConfiguracionProyecto;
