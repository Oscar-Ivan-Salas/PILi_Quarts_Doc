import { useState } from 'react'
import { motion } from 'framer-motion'
import { MessageSquare, Send, Bot, User, Loader2 } from 'lucide-react'
import { usePILI } from '../hooks/usePILI'

export function ChatPanel() {
    const [isOpen, setIsOpen] = useState(true)
    const {
        messages,
        isLoading,
        isTyping,
        connectionStatus,
        sendMessage,
        clearHistory,
    } = usePILI({ userId: 'demo-user-123', useWebSocket: true })

    const [input, setInput] = useState('')

    const handleSend = async () => {
        if (!input.trim() || isLoading) return

        await sendMessage(input)
        setInput('')
    }

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    return (
        <motion.div
            initial={{ x: 20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className={`${isOpen ? 'w-96' : 'w-14'
                } bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-800 flex flex-col transition-all duration-300`}
        >
            {/* Header */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between">
                {isOpen && (
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-gradient-to-br from-brand-red to-brand-yellow rounded-full flex items-center justify-center">
                            <Bot className="w-5 h-5 text-white" />
                        </div>
                        <div>
                            <h3 className="font-semibold text-gray-900 dark:text-white">PILI AI</h3>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                                {connectionStatus === 'connected' ? (
                                    <span className="flex items-center gap-1">
                                        <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                                        Conectado
                                    </span>
                                ) : connectionStatus === 'connecting' ? (
                                    'Conectando...'
                                ) : (
                                    <span className="flex items-center gap-1">
                                        <span className="w-2 h-2 bg-red-500 rounded-full"></span>
                                        Desconectado
                                    </span>
                                )}
                            </p>
                        </div>
                    </div>
                )}
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="p-1.5 bg-white/5 hover:bg-white/10 backdrop-blur-sm rounded-lg transition-all"
                >
                    <MessageSquare className="w-4 h-4" />
                </button>
            </div>

            {isOpen && (
                <>
                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        {messages.length === 0 ? (
                            <div className="text-center text-gray-500 dark:text-gray-400 mt-8">
                                <Bot className="w-12 h-12 mx-auto mb-2 opacity-50" />
                                <p className="text-sm">Inicia una conversación con PILI</p>
                            </div>
                        ) : (
                            messages.map((message) => (
                                <motion.div
                                    key={message.id}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`flex gap-2 ${message.role === 'user' ? 'justify-end' : 'justify-start'
                                        }`}
                                >
                                    {message.role === 'assistant' && (
                                        <div className="w-8 h-8 bg-gradient-to-br from-brand-red to-brand-yellow rounded-full flex items-center justify-center flex-shrink-0">
                                            <Bot className="w-5 h-5 text-white" />
                                        </div>
                                    )}
                                    <div
                                        className={`max-w-[80%] rounded-lg px-4 py-2 ${message.role === 'user'
                                            ? 'bg-brand-red text-white'
                                            : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white'
                                            }`}
                                    >
                                        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                                        <span className="text-xs opacity-70 mt-1 block">
                                            {new Date(message.timestamp).toLocaleTimeString()}
                                        </span>
                                    </div>
                                    {message.role === 'user' && (
                                        <div className="w-8 h-8 bg-gray-300 dark:bg-gray-700 rounded-full flex items-center justify-center flex-shrink-0">
                                            <User className="w-5 h-5" />
                                        </div>
                                    )}
                                </motion.div>
                            ))
                        )}

                        {isTyping && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="flex gap-2"
                            >
                                <div className="w-8 h-8 bg-gradient-to-br from-brand-red to-brand-yellow rounded-full flex items-center justify-center">
                                    <Bot className="w-5 h-5 text-white" />
                                </div>
                                <div className="bg-gray-100 dark:bg-gray-800 rounded-lg px-4 py-2">
                                    <div className="flex gap-1">
                                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
                                    </div>
                                </div>
                            </motion.div>
                        )}
                    </div>

                    {/* Input */}
                    <div className="p-4 border-t border-gray-200 dark:border-gray-800">
                        <div className="flex gap-2">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Escribe un mensaje..."
                                disabled={isLoading || connectionStatus !== 'connected'}
                                className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-brand-red disabled:opacity-50"
                            />
                            <button
                                onClick={handleSend}
                                disabled={!input.trim() || isLoading || connectionStatus !== 'connected'}
                                className="px-3 py-2 bg-green-600/90 hover:bg-green-500 backdrop-blur-sm text-white rounded-lg transition-all disabled:opacity-50 flex items-center gap-2"
                            >
                                {isLoading ? (
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                ) : (
                                    <Send className="w-4 h-4" />
                                )}
                            </button>
                        </div>
                        {messages.length > 0 && (
                            <button
                                onClick={clearHistory}
                                className="mt-2 text-xs text-gray-500 hover:text-gray-300 transition-colors"
                            >
                                Limpiar historial
                            </button>
                        )}
                    </div>
                </>
            )}
        </motion.div>
    )
}
