import React, { useState, useRef, useEffect } from 'react';
import { Send, Flame, Phone, MapPin, Clock } from 'lucide-react';
import { PiliAvatarLarge } from './PiliAvatar';
import ViewToggleButtons from './ViewToggleButtons';

const PiliContraIncendiosChat = ({ onDatosGenerados, onBotonesUpdate, onBack, onFinish,
    viewMode,
    setViewMode }) => {
    const [conversacion, setConversacion] = useState([
        {
            sender: 'bot',
            text: `¡Hola! 👋 Soy **Pili**, tu especialista en sistemas contra incendios de **Tesla Electricidad**.

🔥 Sistemas disponibles:
✅ Rociadores automáticos
✅ Gabinetes contra incendios
✅ Red de extintores
✅ Sistemas de detección

**¿Qué sistema necesitas?**`,
            buttons: [
                { text: '💧 Rociadores', value: 'ROCIADORES' },
                { text: '🚪 Gabinetes', value: 'GABINETES' },
                { text: '🧯 Extintores', value: 'EXTINTORES' },
                { text: '🔔 Detección', value: 'DETECCION' }
            ],
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [conversationState, setConversationState] = useState(null);
    const [hasQuote, setHasQuote] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [conversacion]);

    const addBotMessage = (text, buttons = null) => {
        setConversacion(prev => [...prev, {
            sender: 'bot',
            text,
            buttons,
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        }]);
        if (buttons && onBotonesUpdate) onBotonesUpdate(buttons);
    };

    const addUserMessage = (text) => {
        setConversacion(prev => [...prev, {
            sender: 'user',
            text,
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        }]);
    };

    const enviarMensajeBackend = async (mensaje) => {
        if (isTyping) return;
        setIsTyping(true);

        try {
            const response = await fetch('http://localhost:8000/api/chat/pili-contra-incendios', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mensaje: mensaje,
                    conversation_state: conversationState
                })
            });

            const data = await response.json();

            if (data.success) {
                addBotMessage(data.respuesta, data.botones);
                setConversationState(data.conversation_state);

                if (data.datos_generados) {
                    setHasQuote(true);
                    if (onDatosGenerados) onDatosGenerados(data.datos_generados);
                }
            } else {
                addBotMessage('Lo siento, hubo un error.');
            }
        } catch (error) {
            console.error('Error:', error);
            addBotMessage('Error de conexión.');
        } finally {
            setIsTyping(false);
        }
    };

    const handleButtonClick = (buttonValue) => {
        if (isTyping) return;
        addUserMessage(buttonValue);
        setTimeout(() => enviarMensajeBackend(buttonValue), 100);
    };

    const handleSendMessage = () => {
        if (!inputValue.trim() || isTyping) return;
        const mensaje = inputValue.trim();
        addUserMessage(mensaje);
        setInputValue('');
        setTimeout(() => enviarMensajeBackend(mensaje), 100);
    };

    return (
        <div className="flex flex-col h-full bg-gradient-to-br from-red-900 via-red-800 to-red-950 rounded-2xl shadow-2xl overflow-hidden border-2 border-red-600">
            {/* Header */}
            <div className="bg-gradient-to-r from-red-800 to-red-900 p-4 border-b-2 border-orange-500 shadow-lg">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <PiliAvatarLarge showCrown={false} />
                        <div>
                            <h3 className="text-xl font-bold text-orange-400">PILI Contra Incendios</h3>
                            <p className="text-xs text-red-200">Especialista en Sistemas Contra Incendios</p>
                        </div>
                    </div>
                    <ViewToggleButtons viewMode={viewMode} setViewMode={setViewMode} />
                    {onBack && (
                        <button onClick={onBack} className="px-4 py-2 bg-red-700 hover:bg-red-600 text-white rounded-lg font-semibold transition-all">
                            ← Volver
                        </button>
                    )}
                </div>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-red-950 to-black">
                {conversacion.map((msg, index) => (
                    <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%]`}>
                            <div className={`rounded-2xl p-4 shadow-lg ${msg.sender === 'user'
                                ? 'bg-gradient-to-br from-orange-500 to-orange-600 text-red-900'
                                : 'bg-gradient-to-br from-red-800 to-red-900 text-white border-2 border-red-600'
                                }`}>
                                <div
                                    dangerouslySetInnerHTML={{
                                        __html: (msg.text || '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br />')
                                    }}
                                />
                            </div>

                            {msg.buttons && msg.buttons.length > 0 && (
                                <div className="mt-3 flex flex-wrap gap-2">
                                    {msg.buttons.map((btn, btnIndex) => (
                                        <button
                                            key={btnIndex}
                                            onClick={() => handleButtonClick(btn.value)}
                                            disabled={isTyping}
                                            className="px-4 py-2 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-400 hover:to-orange-500 text-red-900 rounded-lg font-semibold shadow-md transition-all transform hover:scale-105 disabled:opacity-50"
                                        >
                                            {btn.text}
                                        </button>
                                    ))}
                                </div>
                            )}

                            <div className={`text-xs mt-1 ${msg.sender === 'user' ? 'text-right text-red-300' : 'text-left text-red-400'}`}>
                                {msg.timestamp}
                            </div>
                        </div>
                    </div>
                ))}

                {isTyping && (
                    <div className="flex justify-start">
                        <div className="bg-red-800 rounded-2xl p-4 border-2 border-red-600">
                            <div className="flex gap-2">
                                <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce"></div>
                                <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="bg-red-900 p-4 border-t-2 border-orange-500">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSendMessage())}
                        placeholder="Escribe tu mensaje..."
                        disabled={isTyping}
                        className="flex-1 px-4 py-3 bg-red-800 text-white border-2 border-red-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 placeholder-red-400 disabled:opacity-50"
                    />
                    <button
                        onClick={handleSendMessage}
                        disabled={!inputValue.trim() || isTyping}
                        className="px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-400 hover:to-orange-500 text-red-900 rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105 disabled:opacity-50 flex items-center gap-2"
                    >
                        <Send className="w-5 h-5" />
                        Enviar
                    </button>
                </div>

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

            {/* Footer */}
            <div className="bg-red-950 p-3 border-t border-red-800">
                <div className="flex justify-around text-xs text-red-300">
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

export default PiliContraIncendiosChat;
