import React, { useState, useRef, useEffect } from 'react';
import { Send, FileText, Phone, MapPin, Clock, Award, TrendingUp, Users } from 'lucide-react';
import { PiliAvatarLarge } from './PiliAvatar';

// ✨ IMPORTAR FORMULARIOS PRO
import FormularioEntregablesPro from './FormularioEntregablesPro';
import FormularioProfesionalesPro from './FormularioProfesionalesPro';
import FormularioSuministrosPro from './FormularioSuministrosPro';

const PiliElectricidadProyectoComplejoPMIChat = ({
    datosCliente,
    nombreProyecto,
    clienteProyecto,
    presupuestoEstimado,
    monedaProyecto,
    duracionMeses,
    onDatosGenerados,
    onBotonesUpdate,
    onBack,
    onFinish
}) => {
    const [conversacion, setConversacion] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [conversationState, setConversationState] = useState(null);
    const [hasQuote, setHasQuote] = useState(false);
    const messagesEndRef = useRef(null);
    const hasSentInitialMessage = useRef(false);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [conversacion]);

    useEffect(() => {
        if (!hasSentInitialMessage.current) {
            hasSentInitialMessage.current = true;

            const estadoInicial = {
                cliente_nombre: datosCliente?.nombre || clienteProyecto || null,
                cliente_ruc: datosCliente?.ruc || null,
                cliente_direccion: datosCliente?.direccion || null,
                cliente_telefono: datosCliente?.telefono || null,
                cliente_email: datosCliente?.email || null,
                proyecto_nombre: nombreProyecto || null,
                presupuesto: presupuestoEstimado ? parseFloat(presupuestoEstimado) : null,
                moneda: monedaProyecto || 'USD',
                duracion_meses: duracionMeses ? parseInt(duracionMeses) : null
            };

            setConversationState(estadoInicial);
            enviarMensaje('', estadoInicial);
        }
    }, []);

    const addMessage = (sender, text, buttons = null, formulario = null) => {
        setConversacion(prev => [...prev, {
            sender,
            text,
            buttons,
            formulario, // ✨ NUEVO: Soporte para formularios
            timestamp: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
        }]);
        if (buttons && onBotonesUpdate) onBotonesUpdate(buttons);
    };

    const enviarMensaje = async (mensaje, estadoCustom = null) => {
        if (isTyping) return;
        setIsTyping(true);

        try {
            const res = await fetch('http://localhost:8000/api/chat/pili-electricidad-proyecto-complejo-pmi', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mensaje,
                    conversation_state: estadoCustom || conversationState
                })
            });

            const data = await res.json();

            if (data.success) {
                // ✨ NUEVO: Detectar si viene formulario
                addMessage('bot', data.respuesta, data.botones, data.formulario);
                setConversationState(data.conversation_state);

                if (data.datos_generados) {
                    setHasQuote(true);
                    if (onDatosGenerados) onDatosGenerados(data.datos_generados);
                }
            }
        } catch (e) {
            addMessage('bot', '❌ Error de conexión. Por favor intenta de nuevo.');
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-gradient-to-br from-purple-900/40 via-blue-900/40 to-slate-900/40 rounded-3xl shadow-2xl backdrop-blur-2xl border border-white/10 overflow-hidden">
            {/* Background Premium con gradiente complejo */}
            <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-purple-950 to-blue-950">
                <div className="absolute inset-0 opacity-10" style={{
                    backgroundImage: `radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3), transparent 50%),
                                     radial-gradient(circle at 80% 80%, rgba(99, 102, 241, 0.3), transparent 50%),
                                     radial-gradient(circle at 40% 20%, rgba(168, 85, 247, 0.2), transparent 50%)`
                }}></div>
            </div>

            {/* Header Premium PMI */}
            <div className="relative z-10 backdrop-blur-xl bg-gradient-to-r from-purple-900/30 via-blue-900/30 to-slate-900/30 border-b border-purple-500/20 shadow-2xl">
                <div className="p-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <PiliAvatarLarge showCrown={false} />
                            <div>
                                <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent flex items-center">
                                    <span className="relative inline-block text-purple-400">
                                        P
                                        <span className="absolute -top-4 -left-2 text-2xl animate-bounce filter drop-shadow-md opacity-100 text-yellow-400">👑</span>
                                    </span>ILI Proyecto Complejo PMI
                                    <TrendingUp className="w-5 h-5 text-yellow-400 ml-2" />
                                </h3>
                                <p className="text-sm text-purple-300/80">Electricidad • Metodología PMI PMBOK 7th</p>
                            </div>
                        </div>
                        {onBack && (
                            <button
                                onClick={onBack}
                                className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold transition-all backdrop-blur-sm border border-white/20 hover:scale-105 transform shadow-lg"
                            >
                                ← Volver
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4 relative z-10 custom-scrollbar scrollbar-purple h-full">
                {conversacion.map((msg, i) => {
                    return (
                        <div key={i} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
                            <div className="max-w-[85%]">
                                <div className={`rounded-2xl p-4 shadow-2xl backdrop-blur-xl border ${msg.sender === 'user'
                                    ? 'bg-gradient-to-br from-purple-600/90 via-blue-600/90 to-cyan-600/90 text-white border-purple-400/30 shadow-purple-500/30'
                                    : 'bg-white/10 text-white border-purple-500/20 shadow-purple-900/50'
                                    }`}>
                                    <div
                                        className="prose prose-invert max-w-none"
                                        dangerouslySetInnerHTML={{
                                            __html: (msg.text || '')
                                                .replace(/\*\*(.*?)\*\*/g, '<strong class="text-purple-300">$1</strong>')
                                                .replace(/\n/g, '<br />')
                                        }}
                                    />
                                </div>

                                {/* ✨ NUEVO: Renderizar formularios Pro */}
                                {msg.formulario && (
                                    <div className="mt-4">
                                        {msg.formulario.tipo === 'profesionales' && (
                                            <FormularioProfesionalesPro
                                                tipoProyecto={msg.formulario.tipoProyecto}
                                                presupuesto={msg.formulario.presupuesto}
                                                area={msg.formulario.area}
                                                onSubmit={(profesionales) => {
                                                    console.log('✅ Profesionales seleccionados:', profesionales);
                                                    // Convertir array a string para enviar al backend
                                                    const texto = profesionales.map(p => `${p.rol} (${p.cantidad})`).join(', ');
                                                    addMessage('user', texto);
                                                    setTimeout(() => enviarMensaje(texto), 100);
                                                }}
                                            />
                                        )}
                                        {msg.formulario.tipo === 'entregables' && (
                                            <FormularioEntregablesPro
                                                tipoProyecto={msg.formulario.tipoProyecto}
                                                presupuesto={msg.formulario.presupuesto}
                                                area={msg.formulario.area}
                                                onSubmit={(entregables) => {
                                                    console.log('✅ Entregables seleccionados:', entregables);
                                                    const texto = entregables.map(e => e.nombre).join(', ');
                                                    addMessage('user', texto);
                                                    setTimeout(() => enviarMensaje(texto), 100);
                                                }}
                                            />
                                        )}
                                        {msg.formulario.tipo === 'suministros' && (
                                            <FormularioSuministrosPro
                                                tipoProyecto={msg.formulario.tipoProyecto}
                                                presupuesto={msg.formulario.presupuesto}
                                                area={msg.formulario.area}
                                                onSubmit={(suministros) => {
                                                    console.log('✅ Suministros seleccionados:', suministros);
                                                    const texto = suministros.map(s => `${s.nombre} (${s.cantidad} ${s.unidad})`).join(', ');
                                                    addMessage('user', texto);
                                                    setTimeout(() => enviarMensaje(texto), 100);
                                                }}
                                            />
                                        )}
                                    </div>
                                )}

                                {msg.buttons && (
                                    <div className="mt-3 flex flex-wrap gap-2">
                                        {msg.buttons.map((btn, j) => (
                                            <button
                                                key={j}
                                                onClick={() => {
                                                    addMessage('user', btn.value);
                                                    setTimeout(() => enviarMensaje(btn.value), 100);
                                                }}
                                                disabled={isTyping}
                                                className="px-4 py-2 rounded-xl bg-gradient-to-r from-purple-500/80 via-blue-600/80 to-cyan-600/80 hover:from-purple-400 hover:to-cyan-500 text-white font-semibold shadow-lg backdrop-blur-sm border border-purple-400/30 transition-all transform hover:scale-105 disabled:opacity-50"
                                            >
                                                {btn.text}
                                            </button>
                                        ))}
                                    </div>
                                )}

                                <div className={`text-xs mt-2 ${msg.sender === 'user' ? 'text-right text-purple-200/60' : 'text-left text-gray-400'}`}>
                                    {msg.timestamp}
                                </div>
                            </div>
                        </div>
                    );
                })}

                {isTyping && (
                    <div className="flex justify-start animate-fadeIn">
                        <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-4 border border-purple-500/20 shadow-xl">
                            <div className="flex gap-2">
                                {[0, 150, 300].map((delay, i) => (
                                    <div
                                        key={i}
                                        className="w-2 h-2 bg-gradient-to-r from-purple-400 to-cyan-400 rounded-full animate-bounce shadow-lg shadow-purple-400/50"
                                        style={{ animationDelay: `${delay}ms` }}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input Area Premium */}
            <div className="relative z-10 backdrop-blur-xl bg-gradient-to-r from-purple-900/30 via-blue-900/30 to-slate-900/30 border-t border-purple-500/20 shadow-2xl">
                <div className="p-4">
                    <div className="flex gap-3">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                    e.preventDefault();
                                    if (inputValue.trim()) {
                                        addMessage('user', inputValue.trim());
                                        enviarMensaje(inputValue.trim());
                                        setInputValue('');
                                    }
                                }
                            }}
                            placeholder="Escribe tu mensaje..."
                            disabled={isTyping}
                            className="flex-1 px-4 py-3 bg-white/10 backdrop-blur-sm text-white border border-purple-500/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400/50 focus:border-purple-400/50 placeholder-gray-400 disabled:opacity-50 transition-all"
                        />
                        <button
                            onClick={() => {
                                if (inputValue.trim()) {
                                    addMessage('user', inputValue.trim());
                                    enviarMensaje(inputValue.trim());
                                    setInputValue('');
                                }
                            }}
                            disabled={!inputValue.trim() || isTyping}
                            className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500 via-blue-600 to-cyan-600 hover:from-purple-400 hover:to-cyan-500 text-white font-semibold shadow-lg shadow-purple-500/30 transition-all transform hover:scale-105 disabled:opacity-50 flex items-center gap-2"
                        >
                            <Send className="w-5 h-5" />
                            Enviar
                        </button>
                    </div>

                    {hasQuote && onFinish && (
                        <button
                            onClick={onFinish}
                            className="w-full mt-3 px-6 py-3 rounded-xl bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-400 hover:to-emerald-500 text-white font-bold shadow-lg shadow-green-500/30 transition-all transform hover:scale-105 flex items-center justify-center gap-2"
                        >
                            <Award className="w-5 h-5" />
                            ✅ Finalizar y Ver PROJECT CHARTER
                        </button>
                    )}
                </div>
            </div>

            {/* Footer Info Premium */}
            <div className="relative z-10 backdrop-blur-xl bg-gradient-to-r from-purple-900/20 via-blue-900/20 to-slate-900/20 border-t border-purple-500/10">
                <div className="p-3">
                    <div className="flex justify-around text-xs text-gray-300">
                        <div className="flex items-center gap-1 hover:text-purple-400 transition-colors cursor-pointer">
                            <Phone className="w-3 h-3" />
                            <span>906 315 961</span>
                        </div>
                        <div className="flex items-center gap-1 hover:text-purple-400 transition-colors cursor-pointer">
                            <MapPin className="w-3 h-3" />
                            <span>Huancayo</span>
                        </div>
                        <div className="flex items-center gap-1 hover:text-purple-400 transition-colors cursor-pointer">
                            <Clock className="w-3 h-3" />
                            <span>Lun-Sáb 8am-6pm</span>
                        </div>
                        <div className="flex items-center gap-1 hover:text-purple-400 transition-colors cursor-pointer">
                            <Users className="w-3 h-3" />
                            <span>PMI PMBOK 7th</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PiliElectricidadProyectoComplejoPMIChat;
