/**
 * Document Service - API Client for Documents
 * Handles communication with the backend for document operations
 */
import axios from 'axios';
import type { DocumentType, DocumentData, ColorScheme } from '../store/useDocumentStore';

const API_URL = 'http://127.0.0.1:8003/api'; // Use IP for reliability

export interface DocumentResponse {
    id: number;
    title: string;
    type: DocumentType;
    data: DocumentData;
    color_scheme: ColorScheme;
    font: string;
    user_id: string;
    created_at: string;
    updated_at: string;
}

export const documentService = {
    /**
     * Get all documents for a user
     */
    async getDocuments(userId: string): Promise<DocumentResponse[]> {
        const response = await axios.get(`${API_URL}/documents`, {
            params: { user_id: userId }
        });
        return response.data;
    },

    /**
     * Get a single document by ID
     */
    async getDocument(id: number): Promise<DocumentResponse> {
        const response = await axios.get(`${API_URL}/documents/${id}`);
        return response.data;
    },

    /**
     * Create a new document
     */
    async createDocument(doc: {
        title: string;
        type: DocumentType;
        data: DocumentData;
        color_scheme: ColorScheme;
        font: string;
        user_id: string;
    }): Promise<DocumentResponse> {
        const response = await axios.post(`${API_URL}/documents/`, doc);
        return response.data;
    },

    /**
     * Update an existing document
     */
    async updateDocument(id: number, doc: {
        title: string;
        type: DocumentType;
        data: DocumentData;
        color_scheme: ColorScheme;
        font: string;
        user_id: string;
    }): Promise<DocumentResponse> {
        const response = await axios.put(`${API_URL}/documents/${id}`, doc);
        return response.data;
    },

    /**
     * Delete a document
     */
    async deleteDocument(id: number): Promise<void> {
        await axios.delete(`${API_URL}/documents/${id}`);
    }
};
