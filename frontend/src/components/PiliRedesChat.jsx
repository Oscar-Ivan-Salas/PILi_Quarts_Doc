import React, { useState, useRef, useEffect } from 'react';
import { Send, Network, Phone, MapPin, Clock } from 'lucide-react';
import ViewToggleButtons from './ViewToggleButtons';
import { PiliAvatarLarge } from './PiliAvatar';

const PiliRedesChat = ({ onDatosGenerados, onBotonesUpdate, onBack, onFinish ,
    viewMode,
    setViewMode}) => {
    const [conversacion, setConversacion] = useState([{ sender: 'bot', text: `¡Hola! 👋 Soy **Pili**, tu especialista en redes de **Tesla Electricidad**.\n\n🌐 Servicios disponibles:\n✅ Red estructurada Cat6\n✅ Fibra óptica\n✅ WiFi empresarial\n\n**¿Qué necesitas?**`, buttons: [{ text: '🔌 Red Cat6', value: 'ESTRUCTURADA' }, { text: '💡 Fibra Óptica', value: 'FIBRA' }, { text: '📶 WiFi', value: 'WIFI' }], timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' }) }]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [conversationState, setConversationState] = useState(null);
    const [hasQuote, setHasQuote] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [conversacion]);

    const addMessage = (sender, text, buttons = null) => {
        setConversacion(prev => [...prev, { sender, text, buttons, timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' }) }]);
        if (buttons && onBotonesUpdate) onBotonesUpdate(buttons);
    };

    const enviarMensaje = async (mensaje) => {
        if (isTyping) return;
        setIsTyping(true);
        try {
            const res = await fetch('http://localhost:8000/api/chat/pili-redes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ mensaje, conversation_state: conversationState }) });
            const data = await res.json();
            if (data.success) {
                addMessage('bot', data.respuesta, data.botones);
                setConversationState(data.conversation_state);
                if (data.datos_generados) { setHasQuote(true); if (onDatosGenerados) onDatosGenerados(data.datos_generados); }
            }
        } catch (e) { addMessage('bot', 'Error'); } finally { setIsTyping(false); }
    };

    return (
        <div className="flex flex-col h-full bg-gradient-to-br from-indigo-900 via-indigo-800 to-indigo-950 rounded-2xl shadow-2xl overflow-hidden border-2 border-indigo-600">
            <div className="bg-gradient-to-r from-indigo-800 to-indigo-900 p-4 border-b-2 border-blue-500 shadow-lg">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <PiliAvatarLarge showCrown={false} />
                        <div><h3 className="text-xl font-bold text-blue-400">PILI Redes</h3><p className="text-xs text-indigo-200">Especialista en Redes de Datos</p></div>
                    </div>
                    <ViewToggleButtons viewMode={viewMode} setViewMode={setViewMode} /> {onBack &&                     <button onClick={onBack} className="px-4 py-2 bg-indigo-700 hover:bg-indigo-600 text-white rounded-lg font-semibold transition-all">← Volver</button>}
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-indigo-950 to-black">
                {conversacion.map((msg, i) => (
                    <div key={i} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className="max-w-[80%]">
                            <div className={`rounded-2xl p-4 shadow-lg ${msg.sender === 'user' ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-indigo-900' : 'bg-gradient-to-br from-indigo-800 to-indigo-900 text-white border-2 border-indigo-600'}`}>
                                <div dangerouslySetInnerHTML={{ __html: (msg.text || '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br />') }} />
                            </div>
                            {msg.buttons && (<div className="mt-3 flex flex-wrap gap-2">{msg.buttons.map((btn, j) => (<button key={j} onClick={() => { addMessage('user', btn.value); setTimeout(() => enviarMensaje(btn.value), 100); }} disabled={isTyping} className="px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-400 hover:to-blue-500 text-indigo-900 rounded-lg font-semibold shadow-md transition-all transform hover:scale-105 disabled:opacity-50">{btn.text}</button>))}</div>)}
                            <div className={`text-xs mt-1 ${msg.sender === 'user' ? 'text-right text-indigo-300' : 'text-left text-indigo-400'}`}>{msg.timestamp}</div>
                        </div>
                    </div>
                ))}
                {isTyping && (<div className="flex justify-start"><div className="bg-indigo-800 rounded-2xl p-4 border-2 border-indigo-600"><div className="flex gap-2">{[0, 150, 300].map((delay, i) => (<div key={i} className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: `${delay}ms` }}></div>))}</div></div></div>)}
                <div ref={messagesEndRef} />
            </div>

            <div className="bg-indigo-900 p-4 border-t-2 border-blue-500">
                <div className="flex gap-2">
                    <input type="text" value={inputValue} onChange={(e) => setInputValue(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), inputValue.trim() && (addMessage('user', inputValue.trim()), enviarMensaje(inputValue.trim()), setInputValue('')))} placeholder="Escribe..." disabled={isTyping} className="flex-1 px-4 py-3 bg-indigo-800 text-white border-2 border-indigo-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-indigo-400 disabled:opacity-50" />
                    <button onClick={() => { if (inputValue.trim()) { addMessage('user', inputValue.trim()); enviarMensaje(inputValue.trim()); setInputValue(''); } }} disabled={!inputValue.trim() || isTyping} className="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-400 hover:to-blue-500 text-indigo-900 rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105 disabled:opacity-50 flex items-center gap-2"><Send className="w-5 h-5" />Enviar</button>
                </div>
                {hasQuote && onFinish && (<button onClick={onFinish} className="w-full mt-3 px-6 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 text-white rounded-lg font-bold shadow-lg transition-all transform hover:scale-105">✅ Finalizar</button>)}
            </div>

            <div className="bg-indigo-950 p-3 border-t border-indigo-800">
                <div className="flex justify-around text-xs text-indigo-300">
                    <div className="flex items-center gap-1"><Phone className="w-3 h-3" /><span>906 315 961</span></div>
                    <div className="flex items-center gap-1"><MapPin className="w-3 h-3" /><span>Huancayo</span></div>
                    <div className="flex items-center gap-1"><Clock className="w-3 h-3" /><span>Lun-Sáb 8am-6pm</span></div>
                </div>
            </div>
        </div>
    );
};

export default PiliRedesChat;
