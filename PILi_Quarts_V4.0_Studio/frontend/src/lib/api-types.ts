/**
 * API Type Definitions
 * Type-safe interfaces for backend API
 * Following clean-code: Type safety
 */

// ============================================================================
// PILI AI Types
// ============================================================================

export interface ChatMessageRequest {
    message: string;
    context?: Record<string, unknown>;
}

export interface ChatMessageResponse {
    response: string;
    timestamp: string;
    suggestions: string[];
    extracted_data?: Record<string, unknown>;
}

export interface ConversationHistory {
    history: Array<{
        user: string;
        assistant: string;
        timestamp: string;
    }>;
    total: number;
}

export interface PILIStats {
    active_conversations: number;
    total_messages: number;
    settings: {
        max_history: number;
        context_window: number;
        timeout_seconds: number;
    };
}

// ============================================================================
// Authentication Types
// ============================================================================

export interface LoginRequest {
    email: string;
    password: string;
}

export interface RegisterRequest {
    email: string;
    password: string;
    nombre: string;
}

export interface TokenResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
}

export interface User {
    id: string;
    email: string;
    nombre: string;
    rol_global: 'owner' | 'admin' | 'member' | 'viewer' | 'guest';
    email_verified: boolean;
    avatar_url?: string;
    created_at: string;
    updated_at: string;
}

// ============================================================================
// Workspace Types
// ============================================================================

export interface Workspace {
    id: string;
    nombre: string;
    slug: string;
    descripcion?: string;
    owner_id: string;
    plan: 'free' | 'pro' | 'enterprise';
    settings: Record<string, unknown>;
    created_at: string;
    updated_at: string;
}

export interface WorkspaceMember {
    id: string;
    workspace_id: string;
    user_id: string;
    rol: 'owner' | 'admin' | 'member' | 'viewer';
    joined_at: string;
}

// ============================================================================
// Project Types
// ============================================================================

export interface Proyecto {
    id: string;
    nombre: string;
    workspace_id: string;
    descripcion?: string;
    tipo: 'residencial' | 'comercial' | 'industrial' | 'otro';
    estado: 'activo' | 'pausado' | 'completado' | 'cancelado';
    fecha_inicio?: string;
    fecha_fin?: string;
    presupuesto?: number;
    metadata: Record<string, unknown>;
    created_at: string;
    updated_at: string;
}

export interface ProyectoMember {
    id: string;
    proyecto_id: string;
    user_id: string;
    rol: 'gerente' | 'ingeniero' | 'tecnico' | 'viewer';
    joined_at: string;
}

// ============================================================================
// Document Types
// ============================================================================

export interface Folder {
    id: string;
    nombre: string;
    proyecto_id: string;
    parent_id?: string;
    path: string;
    created_at: string;
    updated_at: string;
}

export interface Documento {
    id: string;
    nombre: string;
    proyecto_id: string;
    folder_id?: string;
    tipo: 'cotizacion' | 'informe' | 'plano' | 'contrato' | 'otro';
    formato: 'pdf' | 'docx' | 'xlsx' | 'dwg' | 'otro';
    size_bytes: number;
    storage_path: string;
    version: number;
    metadata: Record<string, unknown>;
    created_by: string;
    created_at: string;
    updated_at: string;
}

export interface DocumentoVersion {
    id: string;
    documento_id: string;
    version: number;
    storage_path: string;
    size_bytes: number;
    cambios?: string;
    created_by: string;
    created_at: string;
}

// ============================================================================
// Document Generation Types
// ============================================================================

export interface CotizacionData {
    numero: string;
    fecha: string;
    valida_hasta: string;
    cliente: {
        nombre: string;
        empresa?: string;
        email: string;
        telefono: string;
        direccion: string;
    };
    items: Array<{
        descripcion: string;
        cantidad: number;
        precio_unitario: number;
        subtotal: number;
    }>;
    totales: {
        subtotal: number;
        iva: number;
        total: number;
    };
    terminos?: string;
    empresa_nombre?: string;
    empresa_contacto?: string;
}

export interface GenerateDocumentRequest {
    document_type: 'cotizacion' | 'informe' | 'presupuesto' | 'contrato' | 'plano';
    format: 'pdf' | 'docx' | 'xlsx';
    data: CotizacionData | Record<string, unknown>;
}

// ============================================================================
// Activity Types
// ============================================================================

export interface Actividad {
    id: string;
    user_id: string;
    proyecto_id?: string;
    workspace_id?: string;
    tipo: 'crear' | 'editar' | 'eliminar' | 'compartir' | 'comentar' | 'otro';
    entidad_tipo: 'proyecto' | 'documento' | 'workspace' | 'usuario' | 'otro';
    entidad_id: string;
    descripcion: string;
    metadata: Record<string, unknown>;
    created_at: string;
}

// ============================================================================
// API Response Types
// ============================================================================

export interface APIError {
    error: string;
    message: string;
    details?: unknown;
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
}

export interface HealthResponse {
    status: 'healthy' | 'unhealthy';
    service: string;
    version: string;
}

export interface APIInfoResponse {
    name: string;
    version: string;
    description: string;
    modules: Record<string, string>;
    features: string[];
}
