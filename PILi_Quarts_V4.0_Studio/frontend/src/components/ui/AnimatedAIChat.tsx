import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Send,
    Paperclip,
    Crown,
    Sparkles
} from 'lucide-react';
import { useWorkspaceStore } from '../../store/useWorkspaceStore';
import { useAutoResizeTextarea } from '../../hooks/useAutoResizeTextarea';

export function AnimatedAIChat() {
    // PILI Core - The Visual Brain ( इंजीनियरिंग स्टूडियो संस्करण )
    const PiliBrainCore = () => (
        <div className="relative mb-8">
            <div className="absolute inset-0 bg-[#0052A3]/10 blur-[50px] rounded-full scale-[2] animate-pulse" />
            <motion.div
                className="w-20 h-20 relative z-10 pili-core-pulse rounded-full border border-white/10 bg-gradient-to-br from-[#0052A3]/20 via-black/80 to-[#030712] flex items-center justify-center backdrop-blur-3xl shadow-[0_0_30px_rgba(0,82,163,0.15)]"
            >
                {/* Orbital Rings */}
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-2 border border-[#D4AF37]/10 rounded-full border-t-[#D4AF37]/40"
                />
                <motion.div
                    animate={{ rotate: -360 }}
                    transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-4 border border-[#0052A3]/10 rounded-full border-b-[#0052A3]/40"
                />

                <div className="w-10 h-10 rounded-full bg-[#0052A3]/30 filter blur-md animate-ping" />
                <Crown className="w-8 h-8 text-white/90 absolute drop-shadow-[0_0_10px_rgba(255,255,255,0.5)]" strokeWidth={1} />
            </motion.div>
        </div>
    );

    const { chatMessages, addChatMessage } = useWorkspaceStore();
    const [value, setValue] = useState("");
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [chatMessages]);

    useEffect(() => {
        if (chatMessages.length === 0) {
            const timer = setTimeout(() => {
                addChatMessage({
                    role: 'assistant',
                    content: "Sistemas Core V4.0 Sincronizados.\n\nSoy PILI, tu motor de inteligencia técnica. He configurado el espacio de trabajo en modo 'Estudio de Ingeniería'.\n\n¿En qué misión trabajaremos hoy? ⚡",
                    thought_trace: ["Protocolos Tesla Cargados.", "Malla de ingeniería proyectada.", "Esperando órdenes de comando."]
                });
            }, 1000);
            return () => clearTimeout(timer);
        }
    }, [chatMessages.length, addChatMessage]);

    const textareaRef = useAutoResizeTextarea(value);

    return (
        <div className="w-[380px] h-full flex flex-col p-6 bg-[#030712] border-l border-white/5 font-sans relative">
            <div className="flex-1 flex flex-col min-h-0">
                <div className="flex-1 overflow-y-auto custom-scrollbar space-y-6 pb-4">
                    {chatMessages.length <= 1 && (
                        <div className="text-center py-12 flex flex-col items-center">
                            <PiliBrainCore />
                            <motion.div
                                initial={{ opacity: 0, y: 15 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="block"
                            >
                                <h1 className="text-xl font-black tracking-[0.2em] bg-clip-text text-transparent bg-gradient-to-b from-white to-white/40 uppercase pb-2">
                                    PILI INTELLIGENCE
                                </h1>
                                <p className="text-[9px] text-[#0052A3] uppercase tracking-[0.5em] font-black opacity-80">
                                    Studio Synced • V4.0.1
                                </p>
                            </motion.div>
                        </div>
                    )}

                    {chatMessages.map((msg, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, x: 10 }}
                            animate={{ opacity: 1, x: 0 }}
                            className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
                        >
                            <div className={`
                                max-w-[90%] p-4 rounded-2xl text-[12px] leading-relaxed
                                ${msg.role === 'user'
                                    ? 'bg-[#0052A3] text-white rounded-tr-none'
                                    : 'studio-glass text-white/90 rounded-tl-none border border-white/10 shadow-lg'}
                            `}>
                                {msg.content}
                            </div>
                        </motion.div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                <div className="pt-4">
                    <div className="relative studio-glass rounded-2xl border border-white/10 p-2 shadow-2xl">
                        <textarea
                            ref={textareaRef}
                            value={value}
                            onChange={(e) => setValue(e.target.value)}
                            placeholder="Escribe un comando técnico..."
                            className="w-full bg-transparent border-none focus:ring-0 text-white text-[12px] p-2 min-h-[60px] resize-none placeholder:text-white/20"
                        />
                        <div className="flex justify-between items-center p-2 border-t border-white/5">
                            <div className="flex gap-2">
                                <Paperclip className="w-4 h-4 text-white/30 hover:text-white transition-colors cursor-pointer" />
                                <Sparkles className="w-4 h-4 text-[#D4AF37]/40 hover:text-[#D4AF37] transition-colors cursor-pointer" />
                            </div>
                            <motion.button
                                whileTap={{ scale: 0.95 }}
                                className="p-2 bg-[#0052A3] rounded-lg text-white shadow-lg shadow-[#0052A3]/20"
                            >
                                <Send className="w-4 h-4" />
                            </motion.button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AnimatedAIChat;
