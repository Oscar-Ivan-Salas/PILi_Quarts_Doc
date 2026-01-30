import React from 'react';
import ThreePanelLayout from './ThreePanelLayout';
import { Eye, Edit } from 'lucide-react';

/**
 * Paso2ThreePanelWrapper - Envuelve el paso 2 existente en layout de 3 paneles
 * 
 * Este componente simplemente reorganiza visualmente el contenido existente
 * sin cambiar la lógica de negocio.
 */
const Paso2ThreePanelWrapper = ({
    // Props del servicio
    servicioSeleccionado,
    servicios,
    tipoFlujo,

    // Props de navegación
    setPaso,
    mostrarPreview,

    // Props de vista previa
    modoEdicion,
    setModoEdicion,
    ocultarIGV,
    setOcultarIGV,

    // Componente de chat (ya renderizado)
    chatComponent,

    // Props para VistaPreviaProfesional
    vistaPreviaProps
}) => {
    return (
        <ThreePanelLayout
            leftPanel={
                <div className="p-6 space-y-4 h-full flex flex-col">
                    <h2 className="text-2xl font-bold text-yellow-400 mb-4">
                        📋 Información del Documento
                    </h2>

                    <div className="bg-gray-800 rounded-lg p-4 space-y-2">
                        <div className="text-sm text-gray-400">Servicio:</div>
                        <div className="text-lg font-bold text-white">
                            {servicios.find(s => s.id === servicioSeleccionado)?.nombre || 'No seleccionado'}
                        </div>
                    </div>

                    <div className="bg-gray-800 rounded-lg p-4 space-y-2">
                        <div className="text-sm text-gray-400">Tipo:</div>
                        <div className="text-lg font-bold text-white capitalize">
                            {tipoFlujo?.replace('-', ' ') || 'No especificado'}
                        </div>
                    </div>

                    <div className="flex-1" />

                    <div className="space-y-2">
                        <button
                            onClick={() => setPaso(1)}
                            className="w-full px-4 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-all font-medium">
                            ← Cambiar Configuración
                        </button>
                        <button
                            onClick={() => setPaso(3)}
                            disabled={!mostrarPreview}
                            className="w-full px-4 py-3 bg-green-600 hover:bg-green-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-bold rounded-lg transition-all">
                            Finalizar →
                        </button>
                    </div>
                </div>
            }

            centerPanel={
                <div className="h-full flex flex-col bg-white">
                    <div className="bg-gradient-to-r from-blue-600 to-blue-500 p-4 shrink-0 flex justify-between items-center">
                        <div className="flex items-center gap-2">
                            <Eye className="w-6 h-6 text-white" />
                            <h3 className="text-xl font-bold text-white">Vista Previa</h3>
                        </div>

                        {mostrarPreview && (
                            <div className="flex items-center gap-2">
                                <button
                                    onClick={() => setModoEdicion(!modoEdicion)}
                                    className="px-3 py-1 bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded-lg text-sm flex items-center gap-1 transition-all">
                                    <Edit className="w-4 h-4" />
                                    {modoEdicion ? 'Ver' : 'Editar'}
                                </button>

                                {tipoFlujo?.includes('cotizacion') && (
                                    <button
                                        onClick={() => setOcultarIGV(!ocultarIGV)}
                                        className="px-3 py-1 bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded text-sm transition-all">
                                        {ocultarIGV ? 'Mostrar' : 'Ocultar'} IGV
                                    </button>
                                )}
                            </div>
                        )}
                    </div>

                    <div className="flex-1 overflow-y-auto p-4">
                        {!mostrarPreview ? (
                            <div className="text-center text-gray-500 mt-20">
                                <Eye className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                                <p className="text-lg font-semibold">Vista Previa</p>
                                <p className="text-sm">Aparecerá cuando PILI genere contenido</p>
                            </div>
                        ) : (
                            vistaPreviaProps.component
                        )}
                    </div>
                </div>
            }

            rightPanel={chatComponent}
        />
    );
};

export default Paso2ThreePanelWrapper;
