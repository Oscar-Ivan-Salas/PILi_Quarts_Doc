import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams, useNavigate } from 'react-router-dom';
import { usePili } from '../context/PiliContext';

// Importar componentes de Chat
import PiliElectricidadChat from '../components/PiliElectricidadChat';
import PiliITSEChat from '../components/PiliITSEChat';
import PiliPuestaTierraChat from '../components/PiliPuestaTierraChat';
import PiliContraIncendiosChat from '../components/PiliContraIncendiosChat';
import PiliDomoticaChat from '../components/PiliDomoticaChat';
import PiliCCTVChat from '../components/PiliCCTVChat';
import PiliRedesChat from '../components/PiliRedesChat';
import PiliAutomatizacionChat from '../components/PiliAutomatizacionChat';
import PiliExpedientesChat from '../components/PiliExpedientesChat';
import PiliSaneamientoChat from '../components/PiliSaneamientoChat';

// Importar Vista Previa
import VistaPreviaProfesional from '../components/VistaPreviaProfesional';
import { ChevronLeft } from 'lucide-react';

const DocumentChatPage = () => {
    const { serviceId } = useParams();
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const { datosCliente } = usePili();

    const industria = searchParams.get('industria');
    const contextoInicial = searchParams.get('contexto');

    // Estados locales para manejo del chat y vista previa
    const [cotizacion, setCotizacion] = useState(null);
    const [botonesContextuales, setBotonesContextuales] = useState([]);
    const [mostrarPreview, setMostrarPreview] = useState(false);
    const [viewMode, setViewMode] = useState('split'); // 'chat' | 'split' | 'preview'
    const [htmlPreview, setHtmlPreview] = useState('');

    // Función para manejar datos generados por el Chat
    const handleDatosGenerados = (datos) => {
        console.log('✅ DATOS GENERADOS:', datos);
        setCotizacion(datos);
        setMostrarPreview(true);
    };

    const handleDescargar = () => {
        alert("Generando descarga... (Lógica pendiente de migración completa)");
    };

    // Renderizar componente específico
    const renderChatComponent = () => {
        const commonProps = {
            onDatosGenerados: handleDatosGenerados,
            onCotizacionGenerada: handleDatosGenerados, // Alias para compatibilidad
            onBotonesUpdate: setBotonesContextuales,
            onBack: () => navigate('/'),
            onFinish: () => { }, // TODO: Navegar a pantalla final?
            viewMode,
            setViewMode,
            contextoInicial, // Pasar contexto como prop si el componente lo soporta
            industria,
            datosCliente
        };

        switch (serviceId) {
            case 'electricidad': return <PiliElectricidadChat {...commonProps} />;
            case 'itse': return <PiliITSEChat {...commonProps} />;
            case 'puesta-tierra': return <PiliPuestaTierraChat {...commonProps} />;
            case 'contra-incendios': return <PiliContraIncendiosChat {...commonProps} />;
            case 'domotica': return <PiliDomoticaChat {...commonProps} />;
            case 'cctv': return <PiliCCTVChat {...commonProps} />;
            case 'redes': return <PiliRedesChat {...commonProps} />;
            case 'automatizacion-industrial': return <PiliAutomatizacionChat {...commonProps} />;
            case 'expedientes': return <PiliExpedientesChat {...commonProps} />;
            case 'saneamiento': return <PiliSaneamientoChat {...commonProps} />;
            default: return <div className="text-white text-center p-10">Servicio no encontrado: {serviceId}</div>;
        }
    };

    return (
        <div className="flex h-screen overflow-hidden bg-gray-950">

            {/* SIDEBAR CONTEXTUAL / BACK BUTTON */}
            <div className="w-16 bg-gray-900 border-r border-gray-800 flex flex-col items-center py-4">
                <button onClick={() => navigate('/')} className="p-2 mb-4 hover:bg-gray-800 rounded-lg text-gray-400 hover:text-white transition-colors">
                    <ChevronLeft size={24} />
                </button>
            </div>

            {/* ÁREA PRINCIPAL SPLIT */}
            <div className="flex-1 flex overflow-hidden">

                {/* IZQUIERDA: CHAT */}
                <div className={`flex-1 flex flex-col min-w-0 ${viewMode === 'preview' ? 'hidden' : ''}`}>
                    {renderChatComponent()}
                </div>

                {/* DERECHA: PREVIEW (Condicional) */}
                {mostrarPreview && (
                    <div className={`flex-1 bg-white border-l border-gray-200 overflow-hidden ${viewMode === 'chat' ? 'hidden' : ''}`}>
                        <VistaPreviaProfesional
                            cotizacion={cotizacion || {}}
                            tipoDocumento="cotizacion-simple" // TODO: Dinamizar esto
                            onGenerarDocumento={handleDescargar}
                        />
                    </div>
                )}

            </div>
        </div>
    );
};

export default DocumentChatPage;
