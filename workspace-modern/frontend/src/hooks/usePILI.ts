/**
 * usePILI Hook
 * React hook for PILI AI chat functionality
 * Following clean-code and React best practices
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { piliService } from '../services/pili.service';
import { PILIWebSocketClient, PILIMessage } from '../lib/websocket-client';
import type { ChatMessageResponse } from '../lib/api-types';

export interface UsePILIOptions {
    userId: string;
    useWebSocket?: boolean;
    onMessage?: (message: PILIMessage) => void;
    onError?: (error: Error) => void;
}

export interface UsePILIReturn {
    messages: PILIMessage[];
    isLoading: boolean;
    isTyping: boolean;
    isConnected: boolean;
    error: Error | null;
    sendMessage: (message: string, context?: Record<string, unknown>) => Promise<void>;
    clearHistory: () => Promise<void>;
    retry: () => void;
}

/**
 * usePILI Hook
 * 
 * Provides PILI AI chat functionality with WebSocket support
 */
export function usePILI(options: UsePILIOptions): UsePILIReturn {
    const { userId, useWebSocket = true, onMessage, onError } = options;

    const [messages, setMessages] = useState<PILIMessage[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [isConnected, setIsConnected] = useState(false);
    const [error, setError] = useState<Error | null>(null);

    const wsClient = useRef<PILIWebSocketClient | null>(null);
    const lastMessageRef = useRef<string>('');

    /**
     * Initialize WebSocket
     */
    useEffect(() => {
        if (!useWebSocket) return;

        wsClient.current = new PILIWebSocketClient(userId, {
            onMessage: (message) => {
                setMessages((prev) => [...prev, message]);
                setIsTyping(false);
                onMessage?.(message);
            },
            onTyping: (typing) => {
                setIsTyping(typing);
            },
            onConnect: () => {
                setIsConnected(true);
                setError(null);
            },
            onDisconnect: () => {
                setIsConnected(false);
            },
            onError: (err) => {
                setError(err);
                onError?.(err);
            },
        });

        wsClient.current.connect();

        return () => {
            wsClient.current?.disconnect();
        };
    }, [userId, useWebSocket, onMessage, onError]);

    /**
     * Send message via WebSocket or HTTP
     */
    const sendMessage = useCallback(
        async (message: string, context?: Record<string, unknown>) => {
            if (!message.trim()) return;

            setError(null);
            lastMessageRef.current = message;

            // Add user message to UI
            const userMessage: PILIMessage = {
                type: 'user',
                content: message,
                timestamp: new Date().toISOString(),
            };
            setMessages((prev) => [...prev, userMessage]);

            try {
                if (useWebSocket && wsClient.current?.isConnected()) {
                    // Send via WebSocket
                    wsClient.current.sendMessage(message, context);
                    setIsTyping(true);
                } else {
                    // Fallback to HTTP
                    setIsLoading(true);
                    const response = await piliService.sendMessage({ message, context });

                    const assistantMessage: PILIMessage = {
                        type: 'assistant',
                        content: response.response,
                        timestamp: response.timestamp,
                        metadata: {
                            suggestions: response.suggestions,
                            extracted_data: response.extracted_data,
                        },
                    };

                    setMessages((prev) => [...prev, assistantMessage]);
                }
            } catch (err) {
                const error = err instanceof Error ? err : new Error('Failed to send message');
                setError(error);
                onError?.(error);

                // Add error message to UI
                const errorMessage: PILIMessage = {
                    type: 'error',
                    content: 'Lo siento, hubo un error al procesar tu mensaje. Por favor intenta de nuevo.',
                    timestamp: new Date().toISOString(),
                };
                setMessages((prev) => [...prev, errorMessage]);
            } finally {
                setIsLoading(false);
                setIsTyping(false);
            }
        },
        [useWebSocket, onError]
    );

    /**
     * Clear conversation history
     */
    const clearHistory = useCallback(async () => {
        try {
            await piliService.clearHistory(userId);
            setMessages([]);
            setError(null);
        } catch (err) {
            const error = err instanceof Error ? err : new Error('Failed to clear history');
            setError(error);
            onError?.(error);
        }
    }, [userId, onError]);

    /**
     * Retry last message
     */
    const retry = useCallback(() => {
        if (lastMessageRef.current) {
            sendMessage(lastMessageRef.current);
        }
    }, [sendMessage]);

    return {
        messages,
        isLoading,
        isTyping,
        isConnected,
        error,
        sendMessage,
        clearHistory,
        retry,
    };
}
