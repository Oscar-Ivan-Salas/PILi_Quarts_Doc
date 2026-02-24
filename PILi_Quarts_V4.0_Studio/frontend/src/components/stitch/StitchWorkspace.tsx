import { motion, AnimatePresence } from 'framer-motion'
import { Search, User, Zap, Mic, Paperclip, Send, Loader2, RefreshCw, FileText, Maximize2 } from 'lucide-react'
import { usePILI } from '../../hooks/usePILI'
import { useState, useRef, useEffect } from 'react'

export function StitchWorkspace() {
    const [input, setInput] = useState('')
    const messagesEndRef = useRef<HTMLDivElement>(null)

    // Conexión con el Cerebro V3 (PILI)
    const {
        messages,
        sendMessage,
        isLoading,
        isTyping,
        isConnected,
        connectionStatus,
        retry
    } = usePILI({
        userId: 'default-user',
        useWebSocket: true
    })

    // Auto-scroll al recibir mensajes
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages, isTyping])

    const handleSend = async () => {
        if (!input.trim() || isLoading) return
        await sendMessage(input)
        setInput('')
    }

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') handleSend()
    }

    return (
        <div className="h-full w-full flex gap-6 p-6 overflow-auto bg-[#0a0a0a] min-w-[1024px]">
            {/* LEFT PANEL: PILI CHAT (Ingeniería) - 35% */}
            <div className="w-[35%] min-w-[350px] flex flex-col h-full max-h-full">
                <motion.div
                    initial={{ x: -20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    className="flex-1 flex flex-col bg-[#121921] rounded-[24px] border border-white/5 overflow-hidden shadow-2xl relative"
                >
                    {/* Header */}
                    <div className="p-4 border-b border-white/5 flex justify-between items-center bg-white/[0.02]">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
                                <span className="font-bold text-white text-xs">P</span>
                            </div>
                            <div>
                                <h2 className="text-gray-200 font-bold text-sm tracking-wide">PILI Engineer</h2>
                                <div className="flex items-center gap-2">
                                    <span className={`w-1.5 h-1.5 rounded-full ${isConnected ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' : 'bg-red-500'}`} />
                                    <span className="text-[10px] text-gray-500 font-mono uppercase tracking-wider">
                                        {isConnected ? 'Neural Link Active' : 'Offline'}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Chat Area */}
                    <div className="flex-1 p-4 overflow-y-auto space-y-4 custom-scrollbar relative">
                        {/* Background Grid */}
                        <div className="absolute inset-0 opacity-[0.03] pointer-events-none"
                            style={{ backgroundImage: 'linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)', backgroundSize: '40px 40px' }}>
                        </div>

                        <AnimatePresence>
                            {messages.length === 0 && (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="flex flex-col items-center justify-center h-full text-center text-gray-600 space-y-3 mt-10"
                                >
                                    <div className="w-12 h-12 rounded-xl bg-blue-500/5 border border-blue-500/10 flex items-center justify-center">
                                        <Zap className="w-6 h-6 text-blue-500/40" />
                                    </div>
                                    <p className="text-sm font-medium">Inicia una sesión de ingeniería</p>
                                    <p className="text-xs max-w-[200px] opacity-60">
                                        "Calcula la caída de tensión para..."<br />
                                        "Genera un presupuesto para..."
                                    </p>
                                </motion.div>
                            )}

                            {messages.map((msg) => (
                                <motion.div
                                    key={msg.id}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                                >
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center border shrink-0 mt-1 shadow-lg ${msg.role === 'user'
                                        ? 'bg-[#1e1b2e] border-purple-500/20'
                                        : msg.role === 'error'
                                            ? 'bg-[#2a1215] border-red-500/20'
                                            : 'bg-[#0f172a] border-cyan-500/20'
                                        }`}>
                                        {msg.role === 'user' ? <User size={14} className="text-purple-400" /> : <Zap size={14} className={msg.role === 'error' ? 'text-red-400' : 'text-cyan-400'} />}
                                    </div>

                                    <div className={`space-y-1 max-w-[85%] ${msg.role === 'user' ? 'items-end flex flex-col' : ''}`}>
                                        <div className={`p-3.5 rounded-2xl border text-sm leading-relaxed shadow-sm backdrop-blur-md ${msg.role === 'user'
                                            ? 'bg-[#2d2b42]/80 border-purple-500/20 text-gray-200 rounded-tr-none'
                                            : msg.role === 'error'
                                                ? 'bg-[#331010]/80 border-red-500/20 text-red-200 rounded-tl-none'
                                                : 'bg-[#1e293b]/80 border-white/5 text-gray-300 rounded-tl-none'
                                            }`}>
                                            {msg.content}
                                        </div>
                                        <span className="text-[9px] text-gray-600 px-1">
                                            {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </span>
                                    </div>
                                </motion.div>
                            ))}

                            {isTyping && (
                                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-3">
                                    <div className="w-8 h-8 rounded-full bg-[#0f172a] border border-cyan-500/20 flex items-center justify-center mt-1">
                                        <Loader2 size={14} className="text-cyan-400/60 animate-spin" />
                                    </div>
                                    <div className="p-3 rounded-2xl rounded-tl-none bg-[#1e293b]/50 border border-white/5">
                                        <div className="flex gap-1">
                                            <div className="w-1.5 h-1.5 bg-cyan-500/40 rounded-full animate-bounce" />
                                            <div className="w-1.5 h-1.5 bg-cyan-500/40 rounded-full animate-bounce delay-75" />
                                            <div className="w-1.5 h-1.5 bg-cyan-500/40 rounded-full animate-bounce delay-150" />
                                        </div>
                                    </div>
                                </motion.div>
                            )}
                            <div ref={messagesEndRef} />
                        </AnimatePresence>
                    </div>

                    {/* Input Area */}
                    <div className="p-3 m-3 mt-0 bg-[#0a0f16] rounded-xl border border-white/10 flex items-center gap-2 relative z-20 shadow-inner">
                        <button className="p-2 hover:bg-white/5 rounded-lg text-gray-500 transition-colors"><Paperclip size={18} /></button>
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder={isConnected ? "Instrucción técnica..." : "Conectando..."}
                            disabled={!isConnected && connectionStatus !== 'connected'}
                            className="flex-1 bg-transparent border-none outline-none text-gray-300 text-sm placeholder-gray-600"
                        />
                        <button className="p-2 hover:bg-white/5 rounded-lg text-gray-500 transition-colors"><Mic size={18} /></button>
                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || isLoading}
                            className={`p-2 rounded-lg text-white shadow-lg transition-all ${input.trim() && !isLoading ? 'bg-blue-600 hover:bg-blue-500' : 'bg-[#1a2333] text-gray-600'
                                }`}
                        >
                            {isLoading ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
                        </button>
                    </div>
                </motion.div>
            </div>

            {/* RIGHT PANEL: LIVE PREVIEW (Hoja A4) - 65% */}
            <div className="flex-1 flex flex-col relative h-full min-w-[600px]">
                <motion.div
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    className="flex-1 bg-[#1a1f2e] rounded-[24px] border border-white/5 shadow-2xl overflow-hidden flex flex-col relative"
                >
                    {/* Toolbar */}
                    <div className="h-14 border-b border-white/5 bg-[#141824] flex items-center justify-between px-6 shrink-0">
                        <div className="flex items-center gap-3">
                            <div className="flex items-center gap-2 px-3 py-1.5 bg-blue-500/10 rounded-lg border border-blue-500/20">
                                <FileText size={14} className="text-blue-400" />
                                <span className="text-xs font-semibold text-blue-300">Vista Previa</span>
                            </div>
                            <span className="text-xs text-gray-500">Documento Generado</span>
                        </div>
                        <div className="flex gap-2">
                            <button className="p-2 hover:bg-white/5 rounded-lg text-gray-400"><RefreshCw size={16} /></button>
                            <button className="p-2 hover:bg-white/5 rounded-lg text-gray-400"><Maximize2 size={16} /></button>
                        </div>
                    </div>

                    {/* Canvas Area (A4 Simulation) */}
                    <div className="flex-1 bg-[#0f121a] overflow-auto p-8 flex justify-center custom-scrollbar">
                        {/* A4 Paper */}
                        <div className="w-[210mm] min-h-[297mm] bg-white text-black shadow-2xl relative transition-transform origin-top hover:scale-[1.01] duration-300 shrink-0">
                            {/* Placeholder Content */}
                            <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-300 pointer-events-none p-10 text-center">
                                <div className="w-24 h-24 mb-6 rounded-full bg-gray-100 flex items-center justify-center">
                                    <FileText size={48} className="text-gray-300" />
                                </div>
                                <h3 className="text-2xl font-bold text-gray-800 mb-2">Lienzo en Blanco</h3>
                                <p className="text-gray-500 max-w-md">
                                    Usa el chat a la izquierda para generar contenido. La vista previa del documento aparecerá aquí en tiempo real.
                                </p>

                                {/* Sello de Agua */}
                                <div className="absolute opacity-[0.03] text-6xl font-black rotate-[-45deg] select-none">
                                    PILI QUARTS PREVIEW
                                </div>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </div>
    )
}
