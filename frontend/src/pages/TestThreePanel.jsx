import React from 'react';
import ProyectoComplejoThreePanel from '../components/ProyectoComplejoThreePanel';

/**
 * TestThreePanel - Página de prueba para el layout de 3 paneles
 * 
 * Acceder en: http://localhost:3005/test-three-panel
 */
const TestThreePanel = () => {
    const handleGuardarBorrador = (datos, proyectoId, esAutoguardado) => {
        console.log('📝 Guardando borrador:', { datos, proyectoId, esAutoguardado });
    };

    return (
        <div className="w-full h-screen">
            <ProyectoComplejoThreePanel
                proyectoId="test-001"
                onGuardarBorrador={handleGuardarBorrador}
            />
        </div>
    );
};

export default TestThreePanel;
