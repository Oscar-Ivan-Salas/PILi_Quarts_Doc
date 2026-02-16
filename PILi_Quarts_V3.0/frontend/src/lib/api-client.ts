/**
 * API Client Configuration
 * Enterprise-grade HTTP client for PILi Quarts backend
 * Following clean-code and frontend-design principles
 */

// Use relative URL in development to leverage Vite proxy, absolute in production
const API_BASE_URL = import.meta.env.DEV ? '' : (import.meta.env.VITE_API_URL || 'http://localhost:8005');
const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8005';

/**
 * API Client class
 * 
 * Features:
 * - Automatic token handling
 * - Request/response interceptors
 * - Error handling
 * - Type-safe responses
 */
class APIClient {
    private baseURL: string;
    private token: string | null = null;

    constructor(baseURL: string = API_BASE_URL) {
        this.baseURL = baseURL;
        this.loadToken();
    }

    /**
     * Load token from localStorage
     */
    private loadToken(): void {
        this.token = localStorage.getItem('access_token');
    }

    /**
     * Save token to localStorage
     */
    public setToken(token: string): void {
        this.token = token;
        localStorage.setItem('access_token', token);
    }

    /**
     * Remove token from localStorage
     */
    public clearToken(): void {
        this.token = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }

    /**
     * Get authorization headers
     */
    private getHeaders(): HeadersInit {
        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        return headers;
    }

    /**
     * Handle API response
     */
    private async handleResponse<T>(response: Response): Promise<T> {
        if (!response.ok) {
            // Handle 401 Unauthorized
            if (response.status === 401) {
                this.clearToken();
                window.location.href = '/login';
                throw new Error('Unauthorized');
            }

            // Handle other errors
            const error = await response.json().catch(() => ({
                error: 'UnknownError',
                message: 'An error occurred',
            }));

            throw new Error(error.message || `HTTP ${response.status}`);
        }

        return response.json();
    }

    /**
     * GET request
     */
    async get<T>(endpoint: string): Promise<T> {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'GET',
            headers: this.getHeaders(),
        });

        return this.handleResponse<T>(response);
    }

    /**
     * POST request
     */
    async post<T>(endpoint: string, data?: unknown): Promise<T> {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: data ? JSON.stringify(data) : undefined,
        });

        return this.handleResponse<T>(response);
    }

    /**
     * PUT request
     */
    async put<T>(endpoint: string, data?: unknown): Promise<T> {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: data ? JSON.stringify(data) : undefined,
        });

        return this.handleResponse<T>(response);
    }

    /**
     * DELETE request
     */
    async delete<T>(endpoint: string): Promise<T> {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'DELETE',
            headers: this.getHeaders(),
        });

        return this.handleResponse<T>(response);
    }

    /**
     * PATCH request
     */
    async patch<T>(endpoint: string, data?: unknown): Promise<T> {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'PATCH',
            headers: this.getHeaders(),
            body: data ? JSON.stringify(data) : undefined,
        });

        return this.handleResponse<T>(response);
    }

    /**
     * Upload file
     */
    async upload<T>(endpoint: string, file: File, additionalData?: Record<string, unknown>): Promise<T> {
        const formData = new FormData();
        formData.append('file', file);

        if (additionalData) {
            Object.entries(additionalData).forEach(([key, value]) => {
                formData.append(key, String(value));
            });
        }

        const headers: HeadersInit = {};
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers,
            body: formData,
        });

        return this.handleResponse<T>(response);
    }
}

// Export singleton instance
export const apiClient = new APIClient();

// Export base URLs for WebSocket
export { API_BASE_URL, WS_BASE_URL };

// Export types
export type { APIClient };
