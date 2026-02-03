import React from 'react';
import ProyectosView from './ProyectosView';
import CotizacionesView from './CotizacionesView';

/**
 * WorkArea - Área de trabajo central
 * 
 * Renderiza el contenido según la sección activa
 */
const WorkArea = ({ activeSection }) => {
    return (
        <div className="h-full overflow-hidden">
            {activeSection === 'proyectos' && <ProyectosView />}

            {activeSection === 'cotizaciones' && <CotizacionesView />}

            {activeSection === 'informes' && (
                <div className="p-6 h-full flex items-center justify-center bg-gray-50 dark:bg-gray-950">
                    <div className="text-center">
                        <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">Informes</h2>
                        <p className="text-gray-600 dark:text-gray-400">Vista de informes en desarrollo...</p>
                    </div>
                </div>
            )}

            {activeSection === 'configuracion' && (
                <div className="p-6 h-full flex items-center justify-center bg-gray-50 dark:bg-gray-950">
                    <div className="text-center">
                        <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">Configuración</h2>
                        <p className="text-gray-600 dark:text-gray-400">Configuración en desarrollo...</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default WorkArea;
