/**
 * Authentication Service
 * API service for user authentication
 * Following clean-code and api-patterns
 */

import { apiClient } from '../lib/api-client';
import type {
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    User,
} from '../lib/api-types';

/**
 * Authentication Service
 * 
 * Handles login, register, token refresh, etc.
 */
export const authService = {
    /**
     * Login user
     */
    async login(credentials: LoginRequest): Promise<TokenResponse> {
        const response = await apiClient.post<TokenResponse>('/api/auth/login', credentials);

        // Store tokens
        apiClient.setToken(response.access_token);
        localStorage.setItem('refresh_token', response.refresh_token);

        return response;
    },

    /**
     * Register new user
     */
    async register(data: RegisterRequest): Promise<TokenResponse> {
        const response = await apiClient.post<TokenResponse>('/api/auth/register', data);

        // Store tokens
        apiClient.setToken(response.access_token);
        localStorage.setItem('refresh_token', response.refresh_token);

        return response;
    },

    /**
     * Logout user
     */
    async logout(): Promise<void> {
        apiClient.clearToken();
    },

    /**
     * Get current user
     */
    async getCurrentUser(): Promise<User> {
        return apiClient.get<User>('/api/auth/me');
    },

    /**
     * Refresh access token
     */
    async refreshToken(): Promise<TokenResponse> {
        const refreshToken = localStorage.getItem('refresh_token');

        if (!refreshToken) {
            throw new Error('No refresh token available');
        }

        const response = await apiClient.post<TokenResponse>('/api/auth/refresh', {
            refresh_token: refreshToken,
        });

        // Update tokens
        apiClient.setToken(response.access_token);
        localStorage.setItem('refresh_token', response.refresh_token);

        return response;
    },

    /**
     * Check if user is authenticated
     */
    isAuthenticated(): boolean {
        return !!localStorage.getItem('access_token');
    },
};
