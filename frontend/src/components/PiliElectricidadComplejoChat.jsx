import React, { useState, useRef, useEffect } from 'react';
import { Send, Zap, Phone, MapPin, Clock } from 'lucide-react';
import { PiliAvatarLarge } from './PiliAvatar';
import ViewToggleButtons from './ViewToggleButtons';

const PiliElectricidadComplejoChat = ({ onDatosGenerados, onBotonesUpdate, onBack, onFinish ,
    viewMode,
    setViewMode}) => {
    const [conversacion, setConversacion] = useState([{ sender: 'bot', text: `¡Hola! 👋 **Pili** - Electricidad **COMPLEJA**\n\n⚡ **COTIZACIÓN TÉCNICA DETALLADA**\n✅ Cálculo de cargas\n✅ Dimensionamiento cables\n✅ Cronograma 4 fases\n\n**¿Tipo de instalación?**`, buttons: [{ text: '🏠 Residencial', value: 'RESIDENCIAL' }, { text: '🏪 Comercial', value: 'COMERCIAL' }, { text: '🏭 Industrial', value: 'INDUSTRIAL' }], timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' }) }]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [conversationState, setConversationState] = useState(null);
    const [hasQuote, setHasQuote] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [conversacion]);

    const addMessage = (sender, text, buttons = null) => {
        setConversacion(prev => [...prev, { sender, text, buttons, timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' }) }]);
        if (buttons && onBotonesUpdate) onBotonesUpdate(buttons)
    };

    const enviarMensaje = async (mensaje) => {
        if (isTyping) return;
        setIsTyping(true);
        try {
            const res = await fetch('http://localhost:8000/api/chat/pili-electricidad-complejo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ mensaje, conversation_state: conversationState })
            });
            const data = await res.json();
            if (data.success) {
                addMessage('bot', data.respuesta, data.botones);
                setConversationState(data.conversation_state);
                if (data.datos_generados) {
                    setHasQuote(true);
                    if (onDatosGenerados) onDatosGenerados(data.datos_generados)
                }
            }
        } catch (e) {
            addMessage('bot', 'Error')
        } finally {
            setIsTyping(false)
        }
    };

    return (
        <div className="flex flex-col h-full bg-gradient-to-br from-blue-900 via-blue-800 to-blue-950 rounded-2xl shadow-2xl overflow-hidden border-2 border-blue-600">
            <div className="bg-gradient-to-r from-blue-800 to-blue-900 p-4 border-b-2 border-yellow-500 shadow-lg">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <PiliAvatarLarge showCrown={false} />
                        <div>
                            <h3 className="text-xl font-bold text-yellow-400">
                                <span className="relative inline-block">
                                    P
                                    <span className="absolute -top-4 -left-2 text-xl animate-bounce filter drop-shadow-md">👑</span>
                                </span>ILI Electricidad COMPLEJO
                            </h3>
                            <p className="text-xs text-blue-200">Cotización Técnica Detallada</p>
                        </div>
                    </div>
                    <ViewToggleButtons viewMode={viewMode} setViewMode={setViewMode} /> {onBack &&                     <button onClick={onBack} className="px-4 py-2 bg-blue-700 hover:bg-blue-600 text-white rounded-lg font-semibold transition-all">← Volver</button>}
                </div>
            </div>
            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-blue-950 to-black custom-scrollbar scrollbar-gold">
                {conversacion.map((msg, i) => (
                    <div key={i} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className="max-w-[80%]">
                            <div className={`rounded-2xl p-4 shadow-lg ${msg.sender === 'user' ? 'bg-gradient-to-br from-yellow-500 to-yellow-600 text-blue-900' : 'bg-gradient-to-br from-blue-800 to-blue-900 text-white border-2 border-blue-600'}`}>
                                <div dangerouslySetInnerHTML={{ __html: (msg.text || '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br />') }} />
                            </div>
                            {msg.buttons && (
                                <div className="mt-3 flex flex-wrap gap-2">
                                    {msg.buttons.map((btn, j) => (
                                        <button
                                            key={j}
                                            onClick={() => { addMessage('user', btn.value); setTimeout(() => enviarMensaje(btn.value), 100) }}
                                            disabled={isTyping}
                                            className="px-4 py-2 bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-400 hover:to-yellow-500 text-blue-900 rounded-lg font-semibold shadow-md transition-all transform hover:scale-105 disabled:opacity-50"
                                        >
                                            {btn.text}
                                        </button>
                                    ))}
                                </div>
                            )}
                            <div className={`text-xs mt-1 ${msg.sender === 'user' ? 'text-right text-blue-300' : 'text-left text-blue-400'}`}>{msg.timestamp}</div>
                        </div>
                    </div>
                ))}
                {isTyping && (
                    <div className="flex justify-start">
                        <div className="bg-blue-800 rounded-2xl p-4 border-2 border-blue-600">
                            <div className="flex gap-2">
                                {[0, 150, 300].map((delay, i) => (
                                    <div key={i} className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{ animationDelay: `${delay}ms` }}></div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>
            <div className="bg-blue-900 p-4 border-t-2 border-yellow-500">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), inputValue.trim() && (addMessage('user', inputValue.trim()), enviarMensaje(inputValue.trim()), setInputValue('')))}
                        placeholder="Escribe..."
                        disabled={isTyping}
                        className="flex-1 px-4 py-3 bg-blue-800 text-white border-2 border-blue-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 placeholder-blue-400 disabled:opacity-50"
                    />
                    <button
                        onClick={() => { if (inputValue.trim()) { addMessage('user', inputValue.trim()); enviarMensaje(inputValue.trim()); setInputValue('') } }}
                        disabled={!inputValue.trim() || isTyping}
                        className="px-6 py-3 bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-400 hover:to-yellow-500 text-blue-900 rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105 disabled:opacity-50 flex items-center gap-2"
                    >
                        <Send className="w-5 h-5" />Enviar
                    </button>
                </div>
                {hasQuote && onFinish && (
                    <button onClick={onFinish} className="w-full mt-3 px-6 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 text-white rounded-lg font-bold shadow-lg transition-all transform hover:scale-105">✅ Finalizar</button>
                )}
            </div>
            <div className="bg-blue-950 p-3 border-t border-blue-800">
                <div className="flex justify-around text-xs text-blue-300">
                    <div className="flex items-center gap-1"><Phone className="w-3 h-3" /><span>906 315 961</span></div>
                    <div className="flex items-center gap-1"><MapPin className="w-3 h-3" /><span>Huancayo</span></div>
                    <div className="flex items-center gap-1"><Clock className="w-3 h-3" /><span>Lun-Sáb 8am-6pm</span></div>
                </div>
            </div>
        </div>
    )
};

export default PiliElectricidadComplejoChat;
