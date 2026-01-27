import React, { useState, useRef, useEffect } from 'react';
import { Send, Zap, Phone, MapPin, Clock, ArrowLeft } from 'lucide-react';
import { PiliAvatarLarge } from './PiliAvatar';
import ViewToggleButtons from './ViewToggleButtons';

/**
 * 🔌 PiliElectricidadChat - Componente para PILI especialista en Electricidad
 * 
 * Diseño profesional con:
 * - Fondo degradado azul eléctrico
 * - Burbujas de chat estilizadas
 * - Botones interactivos con hover
 * - Conectado con backend Python (/api/chat/pili-electricidad)
 */
const PiliElectricidadChat = ({ onCotizacionGenerada, onDatosGenerados, onBotonesUpdate, onBack, onFinish,
    viewMode,
    setViewMode }) => {
    const [conversacion, setConversacion] = useState([
        {
            sender: 'bot',
            text: `¡Hola! 👋 Soy **Pili**, tu especialista en instalaciones eléctricas de **Tesla Electricidad - Huancayo**.

⚡ Te ayudo a cotizar tu proyecto eléctrico con:
✅ Precios competitivos
✅ Materiales de primera calidad
✅ Garantía de 2 años
✅ Personal certificado

**¿Qué tipo de instalación necesitas?**`,
            buttons: [
                { text: '🏠 Residencial', value: 'RESIDENCIAL' },
                { text: '🏪 Comercial', value: 'COMERCIAL' },
                { text: '🏭 Industrial', value: 'INDUSTRIAL' }
            ],
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [conversationState, setConversationState] = useState(null);
    const [hasQuote, setHasQuote] = useState(false);
    const messagesEndRef = useRef(null);

    // Colores corporativos para Electricidad (azul eléctrico)
    const colors = {
        primary: '#1E40AF',      // Azul eléctrico
        secondary: '#FBBF24',    // Amarillo
        dark: '#1E3A8A',         // Azul oscuro
        light_blue: '#3B82F6',   // Azul claro
        accent: '#60A5FA'        // Azul acento
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [conversacion]);

    const addBotMessage = (text, buttons = null) => {
        const newMessage = {
            sender: 'bot',
            text,
            buttons,
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        };
        setConversacion(prev => [...prev, newMessage]);

        if (buttons && onBotonesUpdate) {
            onBotonesUpdate(buttons);
        }
    };

    const addUserMessage = (text) => {
        const newMessage = {
            sender: 'user',
            text,
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        };
        setConversacion(prev => [...prev, newMessage]);
    };

    const enviarMensajeBackend = async (mensaje) => {
        if (isTyping) return;

        setIsTyping(true);

        try {
            const response = await fetch('http://localhost:8000/api/chat/pili-electricidad', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mensaje: mensaje,
                    conversation_state: conversationState
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                addBotMessage(data.respuesta, data.botones);
                setConversationState(data.conversation_state);

                // Si hay cotización generada, notificar al padre
                if (data.datos_generados) {
                    setHasQuote(true);
                    if (onDatosGenerados) {
                        onDatosGenerados(data.datos_generados);
                    }
                }
            } else {
                addBotMessage('Lo siento, hubo un error. Por favor intenta de nuevo.');
            }
        } catch (error) {
            console.error('Error al enviar mensaje:', error);
            addBotMessage('Error de conexión. Por favor verifica que el servidor esté corriendo.');
        } finally {
            setIsTyping(false);
        }
    };

    const handleButtonClick = (buttonValue) => {
        if (isTyping) return;

        addUserMessage(buttonValue);

        setTimeout(() => {
            enviarMensajeBackend(buttonValue);
        }, 100);
    };

    const handleSendMessage = () => {
        if (!inputValue.trim() || isTyping) return;

        const mensaje = inputValue.trim();
        addUserMessage(mensaje);
        setInputValue('');

        setTimeout(() => {
            enviarMensajeBackend(mensaje);
        }, 100);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <div className="flex flex-col h-full bg-gradient-to-br from-blue-900 via-blue-800 to-blue-950 rounded-2xl shadow-2xl overflow-hidden border-2 border-blue-600">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-800 to-blue-900 p-4 border-b-2 border-yellow-500 shadow-lg">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <PiliAvatarLarge showCrown={false} />
                        <div>
                            <h3 className="text-xl font-bold text-yellow-400">
                                <span className="relative inline-block">
                                    P
                                    <span className="absolute -top-4 -left-2 text-xl animate-bounce filter drop-shadow-md">👑</span>
                                </span>PILI Electricidad
                            </h3>
                            <p className="text-xs text-blue-200">Especialista en Instalaciones Eléctricas</p>
                        </div>
                    </div>
                    <ViewToggleButtons viewMode={viewMode} setViewMode={setViewMode} />
                    {onBack && (
                        <button onClick={onBack} className="text-white hover:text-yellow-400 transition-colors">
                            <ArrowLeft className="w-6 h-6" />
                        </button>
                    )}
                </div>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar scrollbar-gold bg-gradient-to-b from-blue-950 to-black">
                {conversacion.map((msg, index) => (
                    <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] ${msg.sender === 'user' ? 'order-2' : 'order-1'}`}>
                            {/* Burbuja de mensaje */}
                            <div
                                className={`rounded-2xl p-4 shadow-lg ${msg.sender === 'user'
                                    ? 'bg-gradient-to-br from-yellow-500 to-yellow-600 text-blue-900'
                                    : 'bg-gradient-to-br from-blue-800 to-blue-900 text-white border-2 border-blue-600'
                                    }`}
                            >
                                <div
                                    className="prose prose-sm max-w-none"
                                    style={{
                                        color: msg.sender === 'user' ? '#1E3A8A' : '#FFFFFF'
                                    }}
                                    dangerouslySetInnerHTML={{
                                        __html: (msg.text || '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                            .replace(/\n/g, '<br />')
                                    }}
                                />
                            </div>

                            {/* Botones */}
                            {msg.buttons && msg.buttons.length > 0 && (
                                <div className="mt-3 flex flex-wrap gap-2">
                                    {msg.buttons.map((btn, btnIndex) => (
                                        <button
                                            key={btnIndex}
                                            onClick={() => handleButtonClick(btn.value)}
                                            disabled={isTyping}
                                            className="px-4 py-2 bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-400 hover:to-yellow-500 text-blue-900 rounded-lg font-semibold shadow-md transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                                            style={{
                                                cursor: isTyping ? 'not-allowed' : 'pointer',
                                                opacity: isTyping ? 0.5 : 1
                                            }}
                                        >
                                            {btn.text}
                                        </button>
                                    ))}
                                </div>
                            )}

                            {/* Timestamp */}
                            <div className={`text-xs mt-1 ${msg.sender === 'user' ? 'text-right text-blue-300' : 'text-left text-blue-400'}`}>
                                {msg.timestamp}
                            </div>
                        </div>
                    </div>
                ))}

                {/* Typing indicator */}
                {isTyping && (
                    <div className="flex justify-start">
                        <div className="bg-blue-800 rounded-2xl p-4 border-2 border-blue-600">
                            <div className="flex gap-2">
                                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="bg-blue-900 p-4 border-t-2 border-yellow-500">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Escribe tu mensaje..."
                        disabled={isTyping}
                        className="flex-1 px-4 py-3 bg-blue-800 text-white border-2 border-blue-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 placeholder-blue-400 disabled:opacity-50"
                    />
                    <button
                        onClick={handleSendMessage}
                        disabled={!inputValue.trim() || isTyping}
                        className="px-6 py-3 bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-400 hover:to-yellow-500 text-blue-900 rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                        <Send className="w-5 h-5" />
                        Enviar
                    </button>
                </div>

                {/* Botón Finalizar (solo si hay cotización) */}
                {hasQuote && onFinish && (
                    <div className="mt-3">
                        <button
                            onClick={onFinish}
                            className="w-full px-6 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 text-white rounded-lg font-bold shadow-lg transition-all transform hover:scale-105"
                        >
                            ✅ Finalizar y Ver Cotización
                        </button>
                    </div>
                )}
            </div>

            {/* Footer Info */}
            <div className="bg-blue-950 p-3 border-t border-blue-800">
                <div className="flex justify-around text-xs text-blue-300">
                    <div className="flex items-center gap-1">
                        <Phone className="w-3 h-3" />
                        <span>906 315 961</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <MapPin className="w-3 h-3" />
                        <span>Huancayo, Junín</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        <span>Lun-Sáb 8am-6pm</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PiliElectricidadChat;
