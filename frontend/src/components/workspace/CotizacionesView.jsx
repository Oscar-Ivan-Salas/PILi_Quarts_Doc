import React, { useState } from 'react';
import { Plus, Search, Filter, FileText, DollarSign, Calendar } from 'lucide-react';

// Importar componentes PILI existentes
import PiliElectricidadChat from '../PiliElectricidadChat';
import PiliITSEChat from '../PiliITSEChat';
import PiliPuestaTierraChat from '../PiliPuestaTierraChat';
import PiliContraIncendiosChat from '../PiliContraIncendiosChat';
import PiliDomoticaChat from '../PiliDomoticaChat';
import PiliCCTVChat from '../PiliCCTVChat';
import PiliRedesChat from '../PiliRedesChat';
import PiliAutomatizacionChat from '../PiliAutomatizacionChat';
import PiliExpedientesChat from '../PiliExpedientesChat';
import PiliSaneamientoChat from '../PiliSaneamientoChat';

/**
 * CotizacionesView - Vista de cotizaciones
 * 
 * Usa los componentes PILI existentes sin modificarlos
 */
const CotizacionesView = () => {
    const [servicioSeleccionado, setServicioSeleccionado] = useState(null);
    const [cotizaciones, setCotizaciones] = useState([]);

    const servicios = [
        { id: 'electricidad', nombre: 'Electricidad', icon: '⚡', component: PiliElectricidadChat },
        { id: 'itse', nombre: 'ITSE', icon: '📋', component: PiliITSEChat },
        { id: 'puesta-tierra', nombre: 'Puesta a Tierra', icon: '🔌', component: PiliPuestaTierraChat },
        { id: 'contra-incendios', nombre: 'Contra Incendios', icon: '🔥', component: PiliContraIncendiosChat },
        { id: 'domotica', nombre: 'Domótica', icon: '🏠', component: PiliDomoticaChat },
        { id: 'cctv', nombre: 'CCTV', icon: '📹', component: PiliCCTVChat },
        { id: 'redes', nombre: 'Redes', icon: '🌐', component: PiliRedesChat },
        { id: 'automatizacion', nombre: 'Automatización', icon: '🤖', component: PiliAutomatizacionChat },
        { id: 'expedientes', nombre: 'Expedientes', icon: '📄', component: PiliExpedientesChat },
        { id: 'saneamiento', nombre: 'Saneamiento', icon: '🚰', component: PiliSaneamientoChat }
    ];

    const handleDatosGenerados = (datos) => {
        setCotizaciones(prev => [...prev, datos]);
    };

    if (servicioSeleccionado) {
        const servicio = servicios.find(s => s.id === servicioSeleccionado);
        const ComponentePILI = servicio.component;

        return (
            <div className="h-full flex flex-col bg-gray-50 dark:bg-gray-950">
                <div className="p-4 bg-white dark:bg-gray-900 border-b-2 border-gray-200 dark:border-gray-800">
                    <button
                        onClick={() => setServicioSeleccionado(null)}
                        className="px-4 py-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-800 dark:text-white rounded-lg transition-all">
                        ← Volver a Servicios
                    </button>
                </div>
                <div className="flex-1 overflow-hidden">
                    <ComponentePILI
                        onDatosGenerados={handleDatosGenerados}
                        onBotonesUpdate={() => { }}
                        onBack={() => setServicioSeleccionado(null)}
                        onFinish={() => { }}
                    />
                </div>
            </div>
        );
    }

    return (
        <div className="p-6 h-full overflow-y-auto bg-gray-50 dark:bg-gray-950">
            {/* Header */}
            <div className="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 dark:text-white">Cotizaciones</h2>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        Selecciona un servicio para crear una nueva cotización
                    </p>
                </div>
            </div>

            {/* Grid de Servicios */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
                {servicios.map(servicio => (
                    <button
                        key={servicio.id}
                        onClick={() => setServicioSeleccionado(servicio.id)}
                        className="bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-xl p-6 hover:border-red-600 hover:shadow-xl transition-all text-left group">
                        <div className="flex items-start justify-between mb-4">
                            <div className="text-4xl">{servicio.icon}</div>
                            <Plus className="w-5 h-5 text-gray-400 group-hover:text-red-600 transition-colors" />
                        </div>
                        <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-2 group-hover:text-red-600 transition-colors">
                            {servicio.nombre}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                            Click para crear cotización
                        </p>
                    </button>
                ))}
            </div>

            {/* Lista de Cotizaciones Recientes */}
            {cotizaciones.length > 0 && (
                <div>
                    <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">
                        Cotizaciones Recientes
                    </h3>
                    <div className="space-y-2">
                        {cotizaciones.map((cot, idx) => (
                            <div
                                key={idx}
                                className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:border-red-600 transition-all">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                        <FileText className="w-5 h-5 text-red-600" />
                                        <div>
                                            <div className="font-medium text-gray-800 dark:text-white">
                                                {cot.cliente?.nombre || 'Cliente'}
                                            </div>
                                            <div className="text-sm text-gray-600 dark:text-gray-400">
                                                {cot.servicio || 'Servicio'}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <div className="font-bold text-yellow-600">
                                            {cot.total || 'S/ 0.00'}
                                        </div>
                                        <div className="text-xs text-gray-500">
                                            {new Date().toLocaleDateString()}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CotizacionesView;
