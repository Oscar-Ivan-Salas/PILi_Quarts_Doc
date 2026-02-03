import React, { useState, useRef, useEffect } from 'react';
import { Send, Lightbulb, BookOpen, Sparkles } from 'lucide-react';
import PiliAvatar from '../PiliAvatar';

/**
 * AIAssistant - Asistente IA (Panel Derecho)
 * 
 * Chat contextual con PILI que ayuda al usuario
 */
const AIAssistant = ({ context }) => {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: '¡Hola! Soy PILI, tu asistente inteligente. ¿En qué puedo ayudarte hoy?'
        }
    ]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const chatRef = useRef(null);

    useEffect(() => {
        if (chatRef.current) {
            chatRef.current.scrollTop = chatRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSend = () => {
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsTyping(true);

        // Simular respuesta de PILI
        setTimeout(() => {
            const aiMessage = {
                role: 'assistant',
                content: 'Entiendo tu consulta. Estoy aquí para ayudarte con tus proyectos y cotizaciones.'
            };
            setMessages(prev => [...prev, aiMessage]);
            setIsTyping(false);
        }, 1000);
    };

    const suggestions = [
        { icon: Lightbulb, text: 'Crear nuevo proyecto' },
        { icon: BookOpen, text: 'Ver documentación' },
        { icon: Sparkles, text: 'Optimizar cotización' }
    ];

    return (
        <div className="h-full bg-gray-900 dark:bg-gray-900 light:bg-gray-100 border-l-2 border-gray-800 dark:border-gray-800 light:border-gray-200 flex flex-col">
            {/* Header */}
            <div className="p-4 border-b-2 border-gray-800 dark:border-gray-800 light:border-gray-200 bg-gradient-to-r from-yellow-600 to-yellow-500">
                <h3 className="text-xl font-bold text-black flex items-center gap-2">
                    <PiliAvatar size={24} showCrown={true} />
                    PILI Assistant
                </h3>
                <p className="text-xs text-gray-800 mt-1">Tu asistente inteligente</p>
            </div>

            {/* Chat Messages */}
            <div ref={chatRef} className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`
              max-w-[80%] p-3 rounded-lg
              ${msg.role === 'user'
                                ? 'bg-red-600 text-white'
                                : 'bg-gray-800 dark:bg-gray-800 light:bg-white text-white dark:text-white light:text-gray-800 border-2 border-gray-700 dark:border-gray-700 light:border-gray-200'
                            }
            `}>
                            {msg.content}
                        </div>
                    </div>
                ))}

                {isTyping && (
                    <div className="flex justify-start">
                        <div className="bg-gray-800 dark:bg-gray-800 light:bg-white p-3 rounded-lg border-2 border-gray-700 dark:border-gray-700 light:border-gray-200">
                            <div className="flex gap-1">
                                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Suggestions */}
            <div className="p-4 border-t-2 border-gray-800 dark:border-gray-800 light:border-gray-200 space-y-2">
                <p className="text-xs text-gray-400 dark:text-gray-400 light:text-gray-600 mb-2">Sugerencias rápidas:</p>
                {suggestions.map((suggestion, idx) => (
                    <button
                        key={idx}
                        onClick={() => setInput(suggestion.text)}
                        className="w-full flex items-center gap-2 p-2 bg-gray-800 dark:bg-gray-800 light:bg-white hover:bg-gray-700 dark:hover:bg-gray-700 light:hover:bg-gray-100 rounded-lg transition-all text-sm text-gray-300 dark:text-gray-300 light:text-gray-700 border border-gray-700 dark:border-gray-700 light:border-gray-200">
                        <suggestion.icon className="w-4 h-4 text-yellow-400" />
                        {suggestion.text}
                    </button>
                ))}
            </div>

            {/* Input */}
            <div className="p-4 border-t-2 border-gray-800 dark:border-gray-800 light:border-gray-200">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Escribe tu mensaje..."
                        className="flex-1 px-4 py-2 bg-gray-800 dark:bg-gray-800 light:bg-white border-2 border-gray-700 dark:border-gray-700 light:border-gray-200 rounded-lg focus:border-yellow-400 focus:outline-none text-white dark:text-white light:text-gray-800"
                    />
                    <button
                        onClick={handleSend}
                        disabled={!input.trim()}
                        className="px-4 py-2 bg-red-600 hover:bg-red-500 disabled:bg-gray-700 text-white rounded-lg transition-all">
                        <Send className="w-5 h-5" />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default AIAssistant;
