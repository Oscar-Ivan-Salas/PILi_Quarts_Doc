/**
 * PILIChat - Base Chat Component
 * 
 * Generic PILI chat component for all specialized chats
 * Supports different chat types:
 * - electricidad
 * - puesta-tierra
 * - contra-incendios
 * - automatizacion
 * - domotica
 * - cctv
 * - redes
 * - saneamiento
 * - itse
 * - expedientes
 */
import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Loader2 } from 'lucide-react';
import { PILIAvatar, PILIStatus } from './PILIAvatar';

export type ChatType =
    | 'electricidad'
    | 'puesta-tierra'
    | 'contra-incendios'
    | 'automatizacion'
    | 'domotica'
    | 'cctv'
    | 'redes'
    | 'saneamiento'
    | 'itse'
    | 'expedientes';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

interface PILIChatProps {
    chatType: ChatType;
    onExtractData?: (data: any) => void;
}

const CHAT_TITLES: Record<ChatType, string> = {
    electricidad: 'Electricidad',
    'puesta-tierra': 'Puesta a Tierra',
    'contra-incendios': 'Contra Incendios',
    automatizacion: 'Automatización',
    domotica: 'Domótica',
    cctv: 'CCTV',
    redes: 'Redes',
    saneamiento: 'Saneamiento',
    itse: 'ITSE',
    expedientes: 'Expedientes',
};

export function PILIChat({ chatType, onExtractData }: PILIChatProps) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        // Simulate PILI response (replace with actual API call)
        setTimeout(() => {
            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: `Entiendo tu consulta sobre ${CHAT_TITLES[chatType]}. ¿Podrías darme más detalles?`,
                timestamp: new Date(),
            };

            setMessages((prev) => [...prev, assistantMessage]);
            setIsLoading(false);
        }, 1000);
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-gray-900">
            {/* Header */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-800">
                <PILIStatus status={isLoading ? 'thinking' : 'active'} />
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                    Especialista en {CHAT_TITLES[chatType]}
                </p>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 ? (
                    <div className="text-center text-gray-500 dark:text-gray-400 mt-8">
                        <PILIAvatar size="xl" showCrown={true} className="mx-auto mb-4" />
                        <p className="text-sm">
                            ¡Hola! Soy PILI, tu asistente especializado en {CHAT_TITLES[chatType]}.
                        </p>
                        <p className="text-xs mt-2">¿En qué puedo ayudarte hoy?</p>
                    </div>
                ) : (
                    <AnimatePresence>
                        {messages.map((message) => (
                            <motion.div
                                key={message.id}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0 }}
                                className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                {message.role === 'assistant' && (
                                    <PILIAvatar size="sm" showCrown={true} />
                                )}

                                <div
                                    className={`max-w-[80%] rounded-lg px-4 py-2 ${message.role === 'user'
                                            ? 'bg-brand-red text-white'
                                            : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white'
                                        }`}
                                >
                                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                                    <span className="text-xs opacity-70 mt-1 block">
                                        {message.timestamp.toLocaleTimeString()}
                                    </span>
                                </div>

                                {message.role === 'user' && (
                                    <div className="w-8 h-8 bg-gray-300 dark:bg-gray-700 rounded-full flex items-center justify-center flex-shrink-0">
                                        <span className="text-xs">👤</span>
                                    </div>
                                )}
                            </motion.div>
                        ))}
                    </AnimatePresence>
                )}

                {isLoading && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex gap-3"
                    >
                        <PILIAvatar size="sm" showCrown={true} />
                        <div className="bg-gray-100 dark:bg-gray-800 rounded-lg px-4 py-2">
                            <div className="flex gap-1">
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                            </div>
                        </div>
                    </motion.div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-200 dark:border-gray-800">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Escribe tu mensaje..."
                        disabled={isLoading}
                        className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-brand-red disabled:opacity-50"
                    />
                    <button
                        onClick={handleSend}
                        disabled={!input.trim() || isLoading}
                        className="px-4 py-2 bg-brand-red text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                    >
                        {isLoading ? (
                            <Loader2 className="w-5 h-5 animate-spin" />
                        ) : (
                            <Send className="w-5 h-5" />
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
