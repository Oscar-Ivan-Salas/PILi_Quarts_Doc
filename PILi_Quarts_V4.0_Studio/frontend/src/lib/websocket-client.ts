/**
 * PILI WebSocket Client
 * Real-time WebSocket connection for PILI AI chat
 * Following clean-code and python-patterns (async patterns)
 */

import { io, Socket } from 'socket.io-client';
// Hardcoded fallback because API_URL not exported from document.service
const WS_URL = 'http://127.0.0.1:8005'; // Use IP to avoid localhost resolution issues

export interface PILIMessage {
    id: string;
    role: 'user' | 'assistant' | 'system' | 'error';
    content: string;
    timestamp: string;
    metadata?: Record<string, unknown>;
}

export interface PILIWebSocketCallbacks {
    onMessage?: (message: PILIMessage) => void;
    onTyping?: (isTyping: boolean) => void;
    onConnect?: () => void;
    onDisconnect?: () => void;
    onError?: (error: Error) => void;
}

/**
 * PILI WebSocket Client
 * 
 * Features:
 * - Real-time messaging
 * - Automatic reconnection
 * - Typing indicators
 * - Heartbeat
 */
export class PILIWebSocketClient {
    private socket: Socket | null = null;
    private userId: string;
    private callbacks: PILIWebSocketCallbacks;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;

    constructor(userId: string, callbacks: PILIWebSocketCallbacks = {}) {
        this.userId = userId;
        this.callbacks = callbacks;
    }

    /**
     * Connect to WebSocket
     */
    connect(): void {
        const token = localStorage.getItem('access_token');

        this.socket = io(`${WS_URL}`, {
            auth: {
                token,
            },
            transports: ['polling', 'websocket'], // Allow polling fallback
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            reconnectionAttempts: this.maxReconnectAttempts,
        });

        this.setupEventListeners();
    }

    /**
     * Setup event listeners
     */
    private setupEventListeners(): void {
        if (!this.socket) return;

        // Connection events
        this.socket.on('connect', () => {
            console.log('✅ PILI WebSocket connected');
            this.reconnectAttempts = 0;
            this.callbacks.onConnect?.();
        });

        this.socket.on('disconnect', (reason) => {
            console.log('❌ PILI WebSocket disconnected:', reason);
            this.callbacks.onDisconnect?.();
        });

        this.socket.on('connect_error', (error) => {
            console.error('WebSocket connection error:', error);
            this.reconnectAttempts++;

            if (this.reconnectAttempts >= this.maxReconnectAttempts) {
                this.callbacks.onError?.(new Error('Max reconnection attempts reached'));
            }
        });

        // Message events
        this.socket.on('message', (data: any) => {
            // Map 'response' to 'content' for compatibility with modern backend
            if (data.response && !data.content) {
                data.content = data.response;
            }

            // Ensure ID exists
            if (!data.id) {
                data.id = crypto.randomUUID();
            }

            // Map 'type' to 'role'
            if (data.type && !data.role) {
                data.role = data.type;
            }

            // Ensure role is valid
            if (!['user', 'assistant', 'system', 'error'].includes(data.role)) {
                data.role = 'assistant'; // Default to assistant
            }

            this.callbacks.onMessage?.(data as PILIMessage);
        });

        this.socket.on('typing', (data: { is_typing: boolean }) => {
            this.callbacks.onTyping?.(data.is_typing);
        });

        this.socket.on('error', (data: { error: string }) => {
            this.callbacks.onError?.(new Error(data.error));
        });

        // Heartbeat
        this.socket.on('pong', () => {
            // Heartbeat received
        });
    }

    /**
     * Send message
     */
    sendMessage(message: string, context?: Record<string, unknown>): void {
        if (!this.socket || !this.socket.connected) {
            throw new Error('WebSocket not connected');
        }

        this.socket.emit('message', {
            message,
            context,
        });
    }

    /**
     * Send typing indicator
     */
    sendTyping(isTyping: boolean): void {
        if (!this.socket || !this.socket.connected) return;

        this.socket.emit('typing', { is_typing: isTyping });
    }

    /**
     * Disconnect
     */
    disconnect(): void {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
        }
    }

    /**
     * Check if connected
     */
    isConnected(): boolean {
        return this.socket?.connected ?? false;
    }

    /**
     * Update callbacks
     */
    updateCallbacks(callbacks: PILIWebSocketCallbacks): void {
        this.callbacks = { ...this.callbacks, ...callbacks };
    }
}
