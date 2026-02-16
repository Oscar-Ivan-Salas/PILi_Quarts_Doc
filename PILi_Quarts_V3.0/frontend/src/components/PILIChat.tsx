/**
 * PILIChat Component
 * Real-time chat interface for PILI AI
 * Following frontend-design and clean-code principles
 */

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, AlertCircle, Trash2 } from 'lucide-react';
import { usePILI } from '../hooks/usePILI';
import type { PILIMessage } from '../lib/websocket-client';

interface PILIChatProps {
    userId: string;
    className?: string;
}

export function PILIChat({ userId, className = '' }: PILIChatProps) {
    const [input, setInput] = useState('');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const {
        messages,
        isLoading,
        isTyping,
        isConnected,
        error,
        sendMessage,
        clearHistory,
        retry,
    } = usePILI({
        userId,
        useWebSocket: true,
    });

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isTyping]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        await sendMessage(input.trim());
        setInput('');
    };

    const handleClearHistory = async () => {
        if (confirm('¿Estás seguro de que quieres borrar el historial?')) {
            await clearHistory();
        }
    };

    return (
        <div className={`flex flex-col h-full bg-white rounded-lg shadow-lg ${className}`}>
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                        PI
                    </div>
                    <div>
                        <h2 className="font-semibold text-gray-900">PILI AI</h2>
                        <div className="flex items-center gap-2 text-sm">
                            <div
                                className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-gray-400'
                                    }`}
                            />
                            <span className="text-gray-600">
                                {isConnected ? 'Conectado' : 'Desconectado'}
                            </span>
                        </div>
                    </div>
                </div>

                <button
                    onClick={handleClearHistory}
                    className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Borrar historial"
                >
                    <Trash2 className="w-5 h-5" />
                </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 && (
                    <div className="text-center text-gray-500 mt-8">
                        <p className="text-lg font-medium">¡Hola! Soy PILI</p>
                        <p className="text-sm mt-2">
                            Tu asistente inteligente para cotizaciones y proyectos eléctricos.
                        </p>
                    </div>
                )}

                {messages.map((message, index) => (
                    <MessageBubble key={index} message={message} />
                ))}

                {isTyping && (
                    <div className="flex items-start gap-3">
                        <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                            PI
                        </div>
                        <div className="bg-gray-100 rounded-2xl rounded-tl-none px-4 py-3">
                            <div className="flex gap-1">
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                            </div>
                        </div>
                    </div>
                )}

                {error && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
                        <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                        <div className="flex-1">
                            <p className="text-sm text-red-800">{error.message}</p>
                            <button
                                onClick={retry}
                                className="text-sm text-red-600 hover:text-red-700 font-medium mt-2"
                            >
                                Reintentar
                            </button>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Escribe tu mensaje..."
                        className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                    >
                        {isLoading ? (
                            <Loader2 className="w-5 h-5 animate-spin" />
                        ) : (
                            <Send className="w-5 h-5" />
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
}

/**
 * Message Bubble Component
 */
function MessageBubble({ message }: { message: PILIMessage }) {
    const isUser = message.type === 'user';
    const isError = message.type === 'error';

    return (
        <div className={`flex items-start gap-3 ${isUser ? 'flex-row-reverse' : ''}`}>
            {!isUser && (
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
                    PI
                </div>
            )}

            <div
                className={`max-w-[70%] rounded-2xl px-4 py-3 ${isUser
                        ? 'bg-blue-600 text-white rounded-tr-none'
                        : isError
                            ? 'bg-red-50 text-red-900 border border-red-200 rounded-tl-none'
                            : 'bg-gray-100 text-gray-900 rounded-tl-none'
                    }`}
            >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>

                {message.metadata?.suggestions && (
                    <div className="mt-3 pt-3 border-t border-gray-200 space-y-2">
                        <p className="text-xs font-medium text-gray-600">Sugerencias:</p>
                        {(message.metadata.suggestions as string[]).map((suggestion, i) => (
                            <button
                                key={i}
                                className="block w-full text-left text-xs bg-white hover:bg-gray-50 px-3 py-2 rounded-lg border border-gray-200 transition-colors"
                            >
                                {suggestion}
                            </button>
                        ))}
                    </div>
                )}

                <p className="text-xs opacity-70 mt-2">
                    {new Date(message.timestamp).toLocaleTimeString('es-MX', {
                        hour: '2-digit',
                        minute: '2-digit',
                    })}
                </p>
            </div>
        </div>
    );
}
