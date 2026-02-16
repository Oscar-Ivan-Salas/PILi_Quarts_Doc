
import { apiClient } from '@/lib/api-client';

export interface GenerateDocumentRequest {
    user_id: string;
    project_id: string;
    format: 'docx' | 'pdf';
    options?: Record<string, unknown>;
    data?: Record<string, unknown>; // Added to support flowData from WorkArea
}

export interface GenerateDocumentResponse {
    success: boolean;
    message: string;
    file_path?: string;
    download_url?: string;
    document_type: string;
    timestamp: string;
}

export const piliApi = {
    generateDocument: async (data: GenerateDocumentRequest): Promise<GenerateDocumentResponse> => {
        return apiClient.post<GenerateDocumentResponse>('/api/pili/v2/generate', data);
    },

    getChatHistory: async (userId: string) => {
        return apiClient.get(`/api/pili/history/${userId}`);
    },

    clearChatHistory: async (userId: string) => {
        return apiClient.delete(`/api/pili/history/${userId}`);
    }
};
