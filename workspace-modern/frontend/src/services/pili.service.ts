/**
 * PILI AI Service
 * API service for PILI AI chat functionality
 * Following clean-code and api-patterns
 */

import { apiClient } from '../lib/api-client';
import type {
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationHistory,
    PILIStats,
} from '../lib/api-types';

/**
 * PILI AI Service
 * 
 * Handles all PILI AI related API calls
 */
export const piliService = {
    /**
     * Send chat message to PILI
     */
    async sendMessage(request: ChatMessageRequest): Promise<ChatMessageResponse> {
        return apiClient.post<ChatMessageResponse>('/api/pili/chat', request);
    },

    /**
     * Get conversation history for user
     */
    async getHistory(userId: string): Promise<ConversationHistory> {
        return apiClient.get<ConversationHistory>(`/api/pili/history/${userId}`);
    },

    /**
     * Clear conversation history
     */
    async clearHistory(userId: string): Promise<{ message: string }> {
        return apiClient.delete<{ message: string }>(`/api/pili/history/${userId}`);
    },

    /**
     * Get PILI statistics
     */
    async getStats(): Promise<PILIStats> {
        return apiClient.get<PILIStats>('/api/pili/stats');
    },

    /**
     * Health check
     */
    async healthCheck(): Promise<{ status: string; service: string }> {
        return apiClient.get('/api/pili/health');
    },
};
