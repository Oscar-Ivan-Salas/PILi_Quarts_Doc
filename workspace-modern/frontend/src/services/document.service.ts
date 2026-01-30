/**
 * Document Service
 * API service for document generation and management
 * Following clean-code and api-patterns
 */

import { apiClient } from '../lib/api-client';
import type {
    Documento,
    DocumentoVersion,
    Folder,
    GenerateDocumentRequest,
} from '../lib/api-types';

/**
 * Document Service
 * 
 * Handles document generation, upload, download, versioning
 */
export const documentService = {
    /**
     * Generate document (PDF, Word, Excel)
     */
    async generateDocument(request: GenerateDocumentRequest): Promise<Blob> {
        const response = await fetch(`${apiClient['baseURL']}/api/documents/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            throw new Error('Failed to generate document');
        }

        return response.blob();
    },

    /**
     * Upload document
     */
    async uploadDocument(
        proyectoId: string,
        file: File,
        metadata?: Record<string, unknown>
    ): Promise<Documento> {
        return apiClient.upload<Documento>('/api/documents/upload', file, {
            proyecto_id: proyectoId,
            ...metadata,
        });
    },

    /**
     * Get document by ID
     */
    async getDocument(documentId: string): Promise<Documento> {
        return apiClient.get<Documento>(`/api/documents/${documentId}`);
    },

    /**
     * Get documents for project
     */
    async getProjectDocuments(proyectoId: string): Promise<Documento[]> {
        return apiClient.get<Documento[]>(`/api/projects/${proyectoId}/documents`);
    },

    /**
     * Download document
     */
    async downloadDocument(documentId: string): Promise<Blob> {
        const response = await fetch(
            `${apiClient['baseURL']}/api/documents/${documentId}/download`,
            {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                },
            }
        );

        if (!response.ok) {
            throw new Error('Failed to download document');
        }

        return response.blob();
    },

    /**
     * Delete document
     */
    async deleteDocument(documentId: string): Promise<{ message: string }> {
        return apiClient.delete<{ message: string }>(`/api/documents/${documentId}`);
    },

    /**
     * Get document versions
     */
    async getDocumentVersions(documentId: string): Promise<DocumentoVersion[]> {
        return apiClient.get<DocumentoVersion[]>(`/api/documents/${documentId}/versions`);
    },

    /**
     * Create folder
     */
    async createFolder(
        proyectoId: string,
        nombre: string,
        parentId?: string
    ): Promise<Folder> {
        return apiClient.post<Folder>('/api/folders', {
            proyecto_id: proyectoId,
            nombre,
            parent_id: parentId,
        });
    },

    /**
     * Get folders for project
     */
    async getProjectFolders(proyectoId: string): Promise<Folder[]> {
        return apiClient.get<Folder[]>(`/api/projects/${proyectoId}/folders`);
    },
};
