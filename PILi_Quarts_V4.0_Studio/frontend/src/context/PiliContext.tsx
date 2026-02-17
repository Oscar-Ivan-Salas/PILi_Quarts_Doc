import React, { createContext, useState, useContext } from 'react';

// Crear el contexto
const PiliContext = createContext<any>(null);

// Hook personalizado para usar el contexto
export const usePili = () => {
    const context = useContext(PiliContext);
    if (!context) {
        throw new Error('usePili debe usarse dentro de un PiliProvider');
    }
    return context;
};

// Proveedor del contexto
export const PiliProvider = ({ children }: { children: React.ReactNode }) => {
    // ============================================
    // ESTADOS GLOBALES (Migrados de App.jsx)
    // ============================================

    // 1. Datos del Cliente
    const [datosCliente, setDatosCliente] = useState({
        nombre: '',
        ruc: '',
        direccion: '',
        telefono: '',
        email: ''
    });

    // 2. Datos del Proyecto Actual
    const [proyectoActual, setProyectoActual] = useState({
        id: null,
        nombre: '',
        tipo: '',
        presupuesto: '',
        moneda: 'PEN'
    });

    // 3. Configuración UI / UX
    const [theme, setTheme] = useState({
        esquemaColores: 'azul-tesla',
        fuente: 'Inter',
        mostrarLogo: true
    });

    // 4. Datos de la Empresa (Constante)
    const datosEmpresa = {
        nombre: 'TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.',
        ruc: '20601138787',
        direccion: 'Dpto de diseño GatoMichuy, Huancayo - Perú',
        email: 'ingenieria.teslaelectricidad@gmail.com',
        telefono: '906 315 961'
    };

    // ============================================
    // FUNCIONES GLOBALES
    // ============================================

    const actualizarCliente = (nuevosDatos: any) => {
        setDatosCliente(prev => ({ ...prev, ...nuevosDatos }));
    };

    const seleccionarProyecto = (proyecto: any) => {
        setProyectoActual(proyecto);
    };

    const reiniciarSesion = () => {
        setDatosCliente({ nombre: '', ruc: '', direccion: '', telefono: '', email: '' });
        setProyectoActual({ id: null, nombre: '', tipo: '', presupuesto: '', moneda: 'PEN' });
    };

    const value = {
        datosCliente,
        actualizarCliente,
        proyectoActual,
        seleccionarProyecto,
        theme,
        setTheme,
        datosEmpresa,
        reiniciarSesion
    };

    return <PiliContext.Provider value={value}>{children}</PiliContext.Provider>;
};
