import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Send,
    Paperclip,
    Crown,
    Sparkles,
    Cpu,
    Activity,
    Shield,
    Zap,
    Terminal
} from 'lucide-react';
import { useWorkspaceStore } from '../../store/useWorkspaceStore';
import { useAutoResizeTextarea } from '../../hooks/useAutoResizeTextarea';

export function AnimatedAIChat() {
    const { chatMessages, addChatMessage } = useWorkspaceStore();
    const [value, setValue] = useState("");
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // PILI Neural Core (Cinematic Design)
    const NeuralCore = () => (
        <div className="relative w-32 h-32 mb-12 flex items-center justify-center">
            {/* Background Glow */}
            <div className="absolute inset-0 bg-[#0052A3]/10 blur-[60px] rounded-full animate-pulse" />

            {/* Spinning Outer Ring */}
            <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                className="absolute inset-0 border-[0.5px] border-white/5 rounded-full"
            />

            {/* Segmented Progress Ring */}
            <svg className="absolute inset-0 w-full h-full -rotate-90">
                <circle
                    cx="64" cy="64" r="60"
                    fill="none"
                    stroke="#0052A3"
                    strokeWidth="1"
                    strokeDasharray="10 180"
                    className="opacity-40"
                />
            </svg>

            {/* Inner Power Core */}
            <motion.div
                animate={{ scale: [1, 1.05, 1], opacity: [0.7, 1, 0.7] }}
                transition={{ duration: 4, repeat: Infinity }}
                className="w-16 h-16 rounded-full border border-[#0052A3]/30 bg-black flex items-center justify-center shadow-[0_0_30px_rgba(0,82,163,0.3)]"
            >
                <motion.div
                    animate={{ rotate: -360 }}
                    transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-2 border border-[#D4AF37]/20 rounded-full border-t-[#D4AF37]/60"
                />
                <Crown className="w-6 h-6 text-white drop-shadow-[0_0_8px_rgba(255,255,255,0.4)]" strokeWidth={1} />
            </motion.div>

            {/* Orbiting Data Points */}
            {[0, 120, 240].map((angle, i) => (
                <motion.div
                    key={i}
                    animate={{ rotate: 360 }}
                    transition={{ duration: 12 + i * 2, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-0"
                >
                    <div
                        className="w-1 h-1 bg-[#0052A3] rounded-full absolute shadow-[0_0_8px_#0052A3]"
                        style={{ top: '50%', left: '0', transform: `translateY(-50%)` }}
                    />
                </motion.div>
            ))}
        </div>
    );

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [chatMessages]);

    useEffect(() => {
        if (chatMessages.length === 0) {
            const timer = setTimeout(() => {
                addChatMessage({
                    role: 'assistant',
                    content: "Neural Systems Synchronized. I am PILI, your Engineering Intelligence. Studio V4.0 is now operating in Maximum Fidelity mode.",
                    thought_trace: ["Tesla Core Loaded", "Cinematic HUD active", "Visual Processing 100%"]
                });
            }, 1000);
            return () => clearTimeout(timer);
        }
    }, [chatMessages.length, addChatMessage]);

    const textareaRef = useAutoResizeTextarea(value);

    return (
        <div className="w-[400px] h-full flex flex-col bg-[#030712] border-l border-white/5 font-sans relative overflow-hidden">
            {/* Subtle Scanline Overlay */}
            <div className="absolute inset-0 scanlines opacity-[0.03] pointer-events-none" />

            {/* Top Status Bar */}
            <div className="p-4 border-b border-white/5 flex items-center justify-between bg-black/40">
                <div className="flex items-center gap-2">
                    <Activity className="w-3 h-3 text-[#0052A3] animate-pulse" />
                    <span className="text-[9px] font-black tracking-[0.2em] text-white/40 uppercase">Intelligence Node</span>
                </div>
                <div className="flex gap-3">
                    <div className="flex items-center gap-1">
                        <div className="w-1 h-1 rounded-full bg-green-500 shadow-[0_0_5px_rgba(34,197,94,0.5)]" />
                        <span className="text-[8px] text-gray-600 font-mono">LAT: 12ms</span>
                    </div>
                </div>
            </div>

            <div className="flex-1 flex flex-col min-h-0 relative z-10">
                <div className="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-8">
                    {chatMessages.length <= 1 && (
                        <div className="flex flex-col items-center justify-center py-10 opacity-80 scale-90">
                            <NeuralCore />
                            <h2 className="text-sm font-black tracking-[0.4em] text-white uppercase mb-2">PILI CORE ENGINE</h2>
                            <p className="text-[8px] text-[#0052A3] font-black tracking-[0.5em] uppercase">Neural Lattice Alpha v4.2</p>
                        </div>
                    )}

                    {chatMessages.map((msg, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
                        >
                            <div className="flex items-center gap-2 mb-2 px-1">
                                {msg.role === 'assistant' ? (
                                    <Sparkles className="w-3 h-3 text-[#D4AF37]" />
                                ) : (
                                    <Terminal className="w-3 h-3 text-[#0052A3]" />
                                )}
                                <span className="text-[8px] font-black text-white/30 uppercase tracking-widest">
                                    {msg.role === 'assistant' ? 'Intelligence Service' : 'Root Command'}
                                </span>
                            </div>
                            <div className={`
                                max-w-[90%] p-5 rounded-xl text-[12px] leading-relaxed font-medium
                                ${msg.role === 'user'
                                    ? 'bg-[#0052A3]/80 text-white rounded-tr-none border border-white/10 shadow-[0_10px_30px_rgba(0,82,163,0.2)]'
                                    : 'studio-glass text-white/90 rounded-tl-none relative before:absolute before:top-0 before:left-0 before:w-full before:h-full before:bg-white/5 before:rounded-inherit'}
                            `}>
                                {msg.content}
                            </div>
                        </motion.div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-6 pt-2 bg-gradient-to-t from-[#030712] via-[#030712] to-transparent">
                    <div className="relative group">
                        <div className="absolute -inset-0.5 bg-gradient-to-r from-[#0052A3]/20 to-transparent rounded-2xl blur opacity-0 group-focus-within:opacity-100 transition duration-1000" />
                        <div className="relative studio-glass rounded-2xl border border-white/10 overflow-hidden shadow-2xl">
                            <textarea
                                ref={textareaRef}
                                value={value}
                                onChange={(e) => setValue(e.target.value)}
                                placeholder="Transmit technical instruction..."
                                className="w-full bg-transparent border-none focus:ring-0 text-white text-[12px] p-4 min-h-[80px] resize-none placeholder:text-white/10 italic"
                            />
                            <div className="flex items-center justify-between p-3 border-t border-white/5 bg-black/20">
                                <div className="flex gap-4 px-2">
                                    <Paperclip className="w-4 h-4 text-white/20 hover:text-white transition-colors cursor-pointer" />
                                    <Cpu className="w-4 h-4 text-[#0052A3]/40 hover:text-[#0052A3] transition-colors cursor-pointer" />
                                </div>
                                <motion.button
                                    whileHover={{ scale: 1.05, backgroundColor: '#0052A3' }}
                                    whileTap={{ scale: 0.95 }}
                                    className="px-4 py-2 bg-[#0052A3]/80 rounded-lg text-white text-[10px] font-black tracking-widest uppercase shadow-lg shadow-[#0052A3]/20 flex items-center gap-2"
                                >
                                    Execute
                                    <Send className="w-3 h-3" />
                                </motion.button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AnimatedAIChat;
