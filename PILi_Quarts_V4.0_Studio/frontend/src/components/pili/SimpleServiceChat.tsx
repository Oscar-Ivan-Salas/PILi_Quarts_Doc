
import { useState, useRef, useEffect } from 'react';
import { Send, ArrowLeft, Phone, MapPin, Clock } from 'lucide-react';
import { PILIAvatarLarge } from './PILIAvatar';
import { motion } from 'framer-motion';

// --- CONFIGURATION TYPES ---
interface ServiceConfig {
    id: string;
    endpoint: string;
    theme: {
        primary: string;
        secondary: string;
        dark: string;
        light: string;
        accent: string;
        gradient: string;
    };
    titles: {
        main: string;
        subtitle: string;
    };
    initialMessage: string;
    initialButtons: { text: string; value: string }[];
}

// --- SERVICE CONFIGURATIONS ---
const SERVICES: Record<string, ServiceConfig> = {
    'electricidad': {
        id: 'electricidad',
        endpoint: '/api/chat/pili-electricidad',
        theme: {
            primary: '#1E40AF',      // Azul eléctrico
            secondary: '#FBBF24',    // Amarillo
            dark: '#1E3A8A',         // Azul oscuro
            light: '#3B82F6',        // Azul claro
            accent: '#60A5FA',       // Azul acento
            gradient: 'from-blue-900 via-blue-800 to-blue-950'
        },
        titles: {
            main: 'PILI Electricidad',
            subtitle: 'Especialista en Instalaciones Eléctricas'
        },
        initialMessage: `¡Hola! 👋 Soy **Pili**, tu especialista en instalaciones eléctricas de **Tesla Electricidad - Huancayo**.\n\n⚡ Te ayudo a cotizar tu proyecto eléctrico con:\n✅ Precios competitivos\n✅ Materiales de primera calidad\n✅ Garantía de 2 años\n✅ Personal certificado\n\n**¿Qué tipo de instalación necesitas?**`,
        initialButtons: [
            { text: '🏠 Residencial', value: 'RESIDENCIAL' },
            { text: '🏪 Comercial', value: 'COMERCIAL' },
            { text: '🏭 Industrial', value: 'INDUSTRIAL' }
        ]
    },
    'itse': {
        id: 'itse',
        endpoint: '/api/chat/pili-itse',
        theme: {
            primary: '#8B0000',      // Rojo Tesla
            secondary: '#D4AF37',    // Dorado
            dark: '#450a0a',         // Rojo oscuro
            light: '#b91c1c',        // Rojo claro
            accent: '#facc15',       // Dorado brillo
            gradient: 'from-red-950 via-red-900 to-black'
        },
        titles: {
            main: 'PILI ITSE',
            subtitle: 'Especialista en Certificados ITSE'
        },
        initialMessage: `¡Hola! 👋 Soy **Pili**, tu especialista en certificados ITSE de **Tesla Electricidad - Huancayo**.\n\n🎯 Te ayudo a obtener tu certificado ITSE con:\n✅ Visita técnica GRATUITA\n✅ Precios oficiales TUPA\n✅ Trámite 100% gestionado\n\n**Selecciona tu tipo de establecimiento:**`,
        initialButtons: [
            { text: '🏥 Salud', value: 'SALUD' },
            { text: '🎓 Educación', value: 'EDUCACION' },
            { text: '🏨 Hospedaje', value: 'HOSPEDAJE' },
            { text: '🏪 Comercio', value: 'COMERCIO' }
        ]
    }
};

// Default config for other services
const getDefaultConfig = (serviceId: string): ServiceConfig => ({
    id: serviceId,
    endpoint: `/api/chat/pili-${serviceId}`,
    theme: {
        primary: '#0F172A',
        secondary: '#38BDF8',
        dark: '#020617',
        light: '#1E293B',
        accent: '#7DD3FC',
        gradient: 'from-slate-900 via-slate-800 to-slate-950'
    },
    titles: {
        main: `PILI ${serviceId.charAt(0).toUpperCase() + serviceId.slice(1)}`,
        subtitle: 'Asistente Especializado'
    },
    initialMessage: `¡Hola! Soy **Pili**, tu asistente especializada en **${serviceId}**.\n\n¿En qué puedo ayudarte hoy?`,
    initialButtons: []
});

interface SimpleServiceChatProps {
    serviceId: string;
    initialContext?: any; // New prop for form data
    onCotizacionGenerada?: (datos: any) => void;
    onDatosGenerados?: (datos: any) => void;
    onBotonesUpdate?: (botones: any[]) => void;
    onBack?: () => void;
    onFinish?: () => void;
}

export function SimpleServiceChat({
    serviceId,
    initialContext,
    onCotizacionGenerada,
    onDatosGenerados,
    onBotonesUpdate,
    onBack,
    onFinish
}: SimpleServiceChatProps) {
    const config = SERVICES[serviceId] || getDefaultConfig(serviceId);

    // Generate Dynamic Initial Message
    const getInitialMessage = () => {
        if (initialContext?.cliente?.nombre) {
            return `Hola **${initialContext.cliente.nombre}** 👋,\n\nSoy **Pili**, tu especialista en **${config.titles.main.replace('PILI ', '')}**. Veo que te interesa un proyecto de tipo **${initialContext.servicio}**.\n\nPara generar una cotización precisa, necesito algunos detalles técnicos.\n\n**¿Podrías describir el alcance del trabajo o qué equipos necesitas instalar?**`;
        }
        return config.initialMessage;
    };

    // State
    const [conversacion, setConversacion] = useState<Array<{
        sender: string;
        text: string;
        buttons: { text: string; value: string }[];
        timestamp: string;
        thought_trace?: string[]; // Add optional property
    }>>([{
        sender: 'bot',
        text: getInitialMessage(),
        buttons: config.initialButtons,
        timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
    }]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [conversationState, setConversationState] = useState(null); // Restored
    const [hasQuote, setHasQuote] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const hasInitialized = useRef(false); // Track initialization

    // --- PROACTIVE CHAT START ---
    useEffect(() => {
        if (!hasInitialized.current && initialContext?.servicio) {
            hasInitialized.current = true;
            // Send hidden startup message
            const startupMsg = `Hola, quiero cotizar ${initialContext.servicio}`;
            enviarMensajeBackend(startupMsg, true); // true = hidden message
        }
    }, [initialContext]);

    // Scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [conversacion]);

    // Initial buttons report
    useEffect(() => {
        if (config.initialButtons && onBotonesUpdate) {
            onBotonesUpdate(config.initialButtons);
        }
    }, []);

    const addBotMessage = (text: string, buttons: any[] = [], thought_trace: string[] = []) => {
        const newMessage = {
            sender: 'bot',
            text,
            buttons,
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' }),
            thought_trace
        };
        setConversacion(prev => [...prev, newMessage]);
        if (buttons && onBotonesUpdate) onBotonesUpdate(buttons);
    };

    const addUserMessage = (text: string) => {
        const newMessage = {
            sender: 'user',
            text,
            buttons: [],
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        };
        setConversacion(prev => [...prev, newMessage]);
    };

    const enviarMensajeBackend = async (mensaje: string, isHidden: boolean = false) => {
        if (isTyping) return;
        setIsTyping(true);

        try {
            // Use MODERN Endpoint
            const response = await fetch('http://localhost:8005/api/pili/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: "user-123", // TODO: Real user ID
                    message: mensaje,
                    context: {
                        ...initialContext,
                        ...(conversationState || {}), // Persist state SAFE SPREAD
                        data: initialContext // ensure legacy integrator gets data
                    }
                })
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();

            // Map Modern Response to Legacy UI State
            // data = { response, suggestions, extracted_data }

            if (isHidden) {
                // Should replace conversation? Or just add?
                // For proactive chat, we want the bot to speak first.
                setConversacion([{
                    sender: 'bot',
                    text: data.response,
                    buttons: data.suggestions?.map((s: any) => ({ text: s.label, value: s.payload })) || [],
                    timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' }),
                    thought_trace: data.extracted_data?.thought_trace || []
                }]);
            } else {
                addBotMessage(
                    data.response,
                    data.suggestions?.map((s: any) => ({ text: s.label, value: s.payload })),
                    data.extracted_data?.thought_trace || []
                );
            }

            // Update State & Data
            if (data.extracted_data) {
                setConversationState((prev: any) => ({ ...(prev || {}), ...data.extracted_data }));

                // If quote generated
                if (data.extracted_data.generated_data) {
                    setHasQuote(true);
                    if (onDatosGenerados) {
                        onDatosGenerados(data.extracted_data.generated_data);
                    }
                    if (onCotizacionGenerada) {
                        onCotizacionGenerada(data.extracted_data.generated_data);
                    }
                }
            }

        } catch (error) {
            console.error('Error al enviar mensaje:', error);
            if (!isHidden) addBotMessage('Error de conexión. Por favor verifica que el backend (uvicorn) esté corriendo en el puerto 8003.');
        } finally {
            setIsTyping(false);
        }
    };

    const handleSendMessage = () => {
        if (!inputValue.trim() || isTyping) return;
        const msg = inputValue.trim();
        addUserMessage(msg);
        setInputValue('');
        setTimeout(() => enviarMensajeBackend(msg), 100);
    };

    const handleButtonClick = (val: string) => {
        if (isTyping) return;
        addUserMessage(val);
        setTimeout(() => enviarMensajeBackend(val), 100);
    };

    return (
        <div className={`flex flex-col h-full bg-gradient-to-br ${config.theme.gradient} rounded-2xl shadow-2xl overflow-hidden border-2`}
            style={{ borderColor: config.theme.primary }}>

            {/* Header */}
            <div className="p-4 border-b-2 shadow-lg flex justify-between items-center"
                style={{ background: `linear-gradient(90deg, ${config.theme.primary}, ${config.theme.dark})`, borderColor: config.theme.secondary }}>
                <div className="flex items-center gap-3">
                    <PILIAvatarLarge showCrown={true} />
                    <div>
                        <h3 className="text-xl font-bold text-white flex items-center gap-2">
                            {config.titles.main}
                        </h3>
                        <p className="text-xs text-gray-300">{config.titles.subtitle}</p>
                    </div>
                </div>
                {onBack && (
                    <button onClick={onBack} className="text-white hover:text-yellow-400 p-2 rounded-full hover:bg-white/10 transition-colors">
                        <ArrowLeft className="w-6 h-6" />
                    </button>
                )}
            </div>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-black/40 custom-scrollbar scroll-smooth">
                {conversacion.map((msg: any, idx) => (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        key={idx}
                        className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div className={`max-w-[85%] ${msg.sender === 'user' ? 'order-2' : 'order-1'}`}>
                            <div className={`rounded-2xl p-4 shadow-lg ${msg.sender === 'user'
                                ? 'bg-gradient-to-br from-yellow-500 to-yellow-600 text-black'
                                : 'bg-white/10 backdrop-blur-md text-white border border-white/20'
                                }`}>

                                {/* THOUGHT TRACE (if available) - Added for PILI Brain debugging */}
                                {msg.thought_trace && msg.thought_trace.length > 0 && (
                                    <div className="mb-3 rounded-lg bg-black/20 border border-white/5 overflow-hidden text-left">
                                        <details className="group">
                                            <summary className="flex items-center gap-2 px-3 py-2 cursor-pointer hover:bg-white/5 transition-colors text-[10px] text-white/50 select-none uppercase tracking-wider font-bold">
                                                <div className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" />
                                                <span>Proceso de Pensamiento ({msg.thought_trace.length})</span>
                                            </summary>
                                            <div className="px-3 pb-3 pt-1 space-y-1">
                                                {msg.thought_trace.map((step: string, stepIdx: number) => (
                                                    <div key={stepIdx} className="text-[10px] text-white/40 font-mono flex gap-2">
                                                        <span className="text-white/20 select-none">{stepIdx + 1}.</span>
                                                        <span>{step}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </details>
                                    </div>
                                )}

                                <div className="prose prose-sm prose-invert max-w-none"
                                    dangerouslySetInnerHTML={{
                                        __html: (msg.text || '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br />')
                                    }}
                                />
                            </div>

                            {/* Buttons */}
                            {msg.buttons && msg.buttons.length > 0 && (
                                <div className="mt-3 flex flex-wrap gap-2">
                                    {msg.buttons.map((btn: any, i: number) => (
                                        <button
                                            key={i}
                                            onClick={() => handleButtonClick(btn.value)}
                                            disabled={isTyping}
                                            className="px-4 py-2 bg-white/10 hover:bg-white/20 disabled:opacity-50 text-white rounded-lg text-sm font-semibold border border-white/30 transition-all hover:scale-105"
                                        >
                                            {btn.text}
                                        </button>
                                    ))}
                                </div>
                            )}
                            <div className={`text-xs mt-1 ${msg.sender === 'user' ? 'text-right text-yellow-500' : 'text-left text-blue-300'}`}>
                                {msg.timestamp}
                            </div>
                        </div>
                    </motion.div>
                ))}

                {isTyping && (
                    <div className="flex justify-start">
                        <div className="bg-white/10 rounded-2xl p-4 border border-white/20">
                            <div className="flex gap-2">
                                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 border-t-2" style={{ background: config.theme.dark, borderColor: config.theme.secondary }}>
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                        placeholder="Escribe tu mensaje..."
                        disabled={isTyping}
                        className="flex-1 px-4 py-3 bg-black/30 text-white border border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:border-transparent placeholder-gray-500"
                        style={{ '--tw-ring-color': config.theme.secondary } as any}
                    />
                    <button
                        onClick={handleSendMessage}
                        disabled={!inputValue.trim() || isTyping}
                        className="px-4 py-3 bg-yellow-500 hover:bg-yellow-400 text-black rounded-xl font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </div>

                {hasQuote && onFinish && (
                    <motion.button
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        onClick={onFinish}
                        className="w-full mt-3 py-3 bg-green-600 hover:bg-green-500 text-white rounded-xl font-bold shadow-lg transition-all flex items-center justify-center gap-2"
                    >
                        ✅ Finalizar y Ver Documento
                    </motion.button>
                )}
            </div>

            {/* Footer */}
            <div className="bg-black/80 p-2 text-xs text-gray-400 flex justify-center gap-4 border-t border-white/10">
                <span className="flex items-center gap-1"><Phone size={12} /> 906 315 961</span>
                <span className="flex items-center gap-1"><MapPin size={12} /> Huancayo, Junín</span>
                <span className="flex items-center gap-1"><Clock size={12} /> Lun-Sáb 8am-6pm</span>
            </div>
        </div>
    );
}
