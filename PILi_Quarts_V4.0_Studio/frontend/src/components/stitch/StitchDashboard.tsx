import { motion, AnimatePresence } from 'framer-motion'
import { Search, Bell, User, Zap, MessageSquare, Mic, Paperclip, Send, Loader2, RefreshCw } from 'lucide-react'
import { usePILI } from '../../hooks/usePILI'
import { useState, useRef, useEffect } from 'react'
import type { PILIMessage } from '../../lib/websocket-client'

export function StitchDashboard() {
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
        userId: 'default-user', // Podríamos hacerlo dinámico después
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
        <div className="h-full w-full flex gap-6 p-8 overflow-hidden">
            {/* Main Chat / Agent Area */}
            <div className="flex-1 flex flex-col items-center justify-center">
                <motion.div
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="w-full max-w-2xl h-[80vh] bg-black/40 backdrop-blur-2xl rounded-[30px] border border-white/10 flex flex-col overflow-hidden shadow-2xl relative"
                >
                    {/* Header */}
                    <div className="p-6 border-b border-white/5 flex justify-between items-center bg-white/5">
                        <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-blue-500/20">
                                <span className="font-bold text-white">P</span>
                            </div>
                            <div>
                                <h2 className="text-white font-bold tracking-wide">PILI Quarts</h2>
                                <div className="flex items-center gap-2">
                                    <span className={`px-1.5 py-0.5 rounded ${isConnected ? 'bg-blue-500/20 text-blue-300' : 'bg-red-500/20 text-red-300'} text-[10px] font-mono transition-colors`}>
                                        {isConnected ? 'ONLINE' : 'OFFLINE'}
                                    </span>
                                    <span className="text-[10px] text-gray-400">SESSION TOKENS ACTIVE</span>
                                </div>
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <button className="p-2 rounded-full hover:bg-white/10 text-white/60"><Search size={18} /></button>
                            <button className="p-2 rounded-full hover:bg-white/10 text-white/60"><User size={18} /></button>
                        </div>
                    </div>

                    {/* Chat Area */}
                    <div className="flex-1 p-8 overflow-y-auto space-y-6 custom-scrollbar relative">
                        {/* Background Grid */}
                        <div className="absolute inset-0 opacity-[0.02] pointer-events-none"
                            style={{ backgroundImage: 'radial-gradient(circle at 1px 1px, white 1px, transparent 0)', backgroundSize: '20px 20px' }}>
                        </div>

                        <AnimatePresence>
                            {messages.length === 0 && (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="flex flex-col items-center justify-center h-full text-center text-gray-500 space-y-4"
                                >
                                    <div className="w-16 h-16 rounded-full bg-blue-500/10 flex items-center justify-center mb-2">
                                        <Zap className="w-8 h-8 text-blue-500/50" />
                                    </div>
                                    <p>Conectado a Nodo Neural V4.</p>
                                    <p className="text-xs max-w-xs opacity-50">Esperando instrucciones para iniciar protocolos de ingeniería.</p>
                                </motion.div>
                            )}

                            {messages.map((msg) => (
                                <motion.div
                                    key={msg.id}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                                >
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center border shrink-0 ${msg.role === 'user'
                                            ? 'bg-purple-600/20 border-purple-500/30'
                                            : msg.role === 'error'
                                                ? 'bg-red-600/20 border-red-500/30'
                                                : 'bg-cyan-600/20 border-cyan-500/30'
                                        }`}>
                                        {msg.role === 'user' ? <User size={14} className="text-purple-400" /> : <Zap size={14} className={msg.role === 'error' ? 'text-red-400' : 'text-cyan-400'} />}
                                    </div>
                                    <div className={`space-y-2 max-w-[80%] ${msg.role === 'user' ? 'items-end flex flex-col' : ''}`}>
                                        <div className={`flex items-center gap-2 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                                            <span className={`text-xs font-bold ${msg.role === 'user' ? 'text-purple-400' : msg.role === 'error' ? 'text-red-400' : 'text-cyan-400'
                                                }`}>
                                                {msg.role === 'user' ? 'YOU' : 'PILI'}
                                            </span>
                                            <span className="text-[10px] text-gray-500">
                                                {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                            </span>
                                        </div>
                                        <div className={`p-4 rounded-2xl border text-sm leading-relaxed shadow-lg backdrop-blur-sm ${msg.role === 'user'
                                                ? 'bg-[#1a1033] border-purple-500/20 shadow-purple-900/10 text-gray-200 rounded-tr-none'
                                                : msg.role === 'error'
                                                    ? 'bg-[#331010] border-red-500/20 shadow-red-900/10 text-red-200 rounded-tl-none'
                                                    : 'bg-[#0a101f] border-cyan-500/20 shadow-cyan-900/10 text-gray-300 rounded-tl-none'
                                            }`}>
                                            {msg.content}
                                        </div>
                                    </div>
                                </motion.div>
                            ))}

                            {isTyping && (
                                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-4">
                                    <div className="w-8 h-8 rounded-full bg-cyan-600/20 flex items-center justify-center border border-cyan-500/30">
                                        <Loader2 size={14} className="text-cyan-400 animate-spin" />
                                    </div>
                                    <div className="space-y-2">
                                        <div className="flex items-center gap-2">
                                            <span className="text-xs font-bold text-cyan-400">PILI</span>
                                            <span className="text-[10px] text-gray-500">Typing...</span>
                                        </div>
                                        <div className="p-3 rounded-2xl rounded-tl-none bg-[#0a101f] border border-cyan-500/20 shadow-lg shadow-cyan-900/10">
                                            <div className="flex gap-1">
                                                <div className="w-1.5 h-1.5 bg-cyan-500/50 rounded-full animate-bounce" />
                                                <div className="w-1.5 h-1.5 bg-cyan-500/50 rounded-full animate-bounce delay-75" />
                                                <div className="w-1.5 h-1.5 bg-cyan-500/50 rounded-full animate-bounce delay-150" />
                                            </div>
                                        </div>
                                    </div>
                                </motion.div>
                            )}
                            <div ref={messagesEndRef} />
                        </AnimatePresence>
                    </div>

                    {/* Input Area */}
                    <div className="p-4 m-4 mt-0 bg-[#0a1120] rounded-2xl border border-white/10 flex items-center gap-3 relative z-20">
                        <button className="p-2 hover:bg-white/5 rounded-full text-white/40"><Paperclip size={18} /></button>
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder={isConnected ? "Transmitir instrucción a PILI..." : "Conectando al servidor..."}
                            disabled={!isConnected && connectionStatus !== 'connected'}
                            className="flex-1 bg-transparent border-none outline-none text-white text-sm placeholder-white/20"
                        />
                        <button className="p-2 hover:bg-white/5 rounded-full text-white/40"><Mic size={18} /></button>
                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || isLoading}
                            className={`p-2 rounded-xl text-white shadow-lg transition-all ${input.trim() && !isLoading ? 'bg-blue-600 hover:bg-blue-500 shadow-blue-600/20' : 'bg-gray-700 text-gray-400 cursor-not-allowed'
                                }`}
                        >
                            {isLoading ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
                        </button>
                    </div>

                    {/* Agent Status (Overlay) */}
                    {messages.length > 0 && (
                        <div className="absolute top-24 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 pointer-events-none transition-opacity opacity-50 hover:opacity-100">
                            <span className="px-2 py-0.5 rounded-full bg-blue-600/10 text-[9px] text-blue-300 border border-blue-500/20 tracking-widest backdrop-blur-sm">
                                NUCLEO ACTIVO
                            </span>
                        </div>
                    )}

                </motion.div>
            </div>

            {/* Right Panel: Analytics (Based on Admin Dashboard) */}
            <div className="w-80 flex flex-col gap-4">
                {/* TODO: Phase 2 - Integrate Real Admin Data */}
                <div className="p-4 rounded-2xl bg-black/40 border border-white/5 backdrop-blur-xl">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest">PILI Quarts Admin</h3>
                        <Bell size={14} className="text-gray-500" />
                    </div>
                    <div className="space-y-3">
                        <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                            <div className="text-[10px] text-gray-500 mb-1">Total Users</div>
                            <div className="flex justify-between items-end">
                                <span className="text-xl font-bold text-white">1,240</span>
                                <span className="text-[10px] text-green-400 font-bold">+5%</span>
                            </div>
                        </div>
                        <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                            <div className="text-[10px] text-gray-500 mb-1">Docs Generated</div>
                            <div className="flex justify-between items-end">
                                <span className="text-xl font-bold text-white">8,502</span>
                                <span className="text-[10px] text-green-400 font-bold">+12%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex-1 p-4 rounded-2xl bg-black/40 border border-white/5 backdrop-blur-xl flex flex-col items-center justify-center relative overflow-hidden">
                    <div className="absolute inset-0 bg-blue-600/5" />
                    <div className="w-40 h-40 rounded-full border-[6px] border-gray-800 border-t-blue-500 flex flex-col items-center justify-center relative">
                        <Zap className="w-6 h-6 text-blue-500 mb-1" />
                        <span className="text-3xl font-bold text-white">4.2M</span>
                        <span className="text-[9px] text-gray-400 uppercase tracking-widest">Tokens</span>
                    </div>
                    <div className="mt-6 text-center">
                        <div className="text-xs font-bold text-white">System Usage</div>
                        <div className="text-[10px] text-gray-500">Optimal Performance</div>
                        {!isConnected && (
                            <button onClick={retry} className="mt-2 text-[10px] flex items-center gap-1 text-red-400 hover:text-red-300">
                                <RefreshCw size={10} /> Reconnect
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
