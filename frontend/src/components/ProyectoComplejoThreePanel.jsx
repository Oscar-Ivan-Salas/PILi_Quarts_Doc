import React, { useState } from 'react';
import ThreePanelLayout from './ThreePanelLayout';
import FormularioProyectoUnificado from './FormularioProyectoUnificado';
import VistaPreviaEnTiempoReal from './VistaPreviaEnTiempoReal';
import PiliElectricidadProyectoComplejoPMIChat from './PiliElectricidadProyectoComplejoPMIChat';

/**
 * ProyectoComplejoThreePanel - Integrador del layout de 3 paneles
 * 
 * Conecta el formulario, vista previa y chat PILI en tiempo real
 */
const ProyectoComplejoThreePanel = ({ proyectoId, onGuardarBorrador }) => {
    // Estado central del proyecto
    const [datosProyecto, setDatosProyecto] = useState({
        nombre_proyecto: '',
        presupuesto: '',
        moneda: 'USD',
        fecha_inicio: '',
        duracion_total: 0,
        complejidad: 7,
        cliente: {
            nombre: '',
            ruc: '',
            email: '',
            telefono: '',
            direccion: ''
        },
        fases: []
    });

    const [complejidad, setComplejidad] = useState(7);

    // Handler para actualizar datos del proyecto
    const handleUpdateDatos = (nuevosDatos) => {
        setDatosProyecto(nuevosDatos);

        // Auto-guardar (debounced en producción)
        if (onGuardarBorrador) {
            onGuardarBorrador(nuevosDatos, proyectoId, true);
        }
    };

    // Handler para cambiar complejidad
    const handleComplejidadChange = (nuevaComplejidad) => {
        setComplejidad(nuevaComplejidad);
        setDatosProyecto(prev => ({
            ...prev,
            complejidad: nuevaComplejidad
        }));
    };

    return (
        <ThreePanelLayout>
            {/* Panel Izquierdo - Formulario */}
            <FormularioProyectoUnificado
                datosProyecto={datosProyecto}
                onUpdateDatos={handleUpdateDatos}
                complejidad={complejidad}
                onComplejidadChange={handleComplejidadChange}
            />

            {/* Panel Central - Vista Previa */}
            <VistaPreviaEnTiempoReal
                datosProyecto={datosProyecto}
                fases={datosProyecto.fases || []}
            />

            {/* Panel Derecho - Chat PILI */}
            <PiliElectricidadProyectoComplejoPMIChat
                complejidad={complejidad}
                contextoProyecto={datosProyecto}
                fases={datosProyecto.fases || []}
                onActualizarDatos={handleUpdateDatos}
            />
        </ThreePanelLayout>
    );
};

export default ProyectoComplejoThreePanel;
