/**
 * Document Store - Zustand State Management
 * Manages document data, type, settings, and editing state
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { documentService } from '../services/document.service';

// Document types
export type DocumentType =
    | 'proyecto-simple'
    | 'proyecto-complejo'
    | 'cotizacion-simple'
    | 'cotizacion-compleja'
    | 'informe-tecnico'
    | 'informe-ejecutivo';

export type ColorScheme = 'azul-tesla' | 'rojo-pili' | 'amarillo-pili';

// Document data structure
export interface DocumentData {
    // Cliente
    cliente: {
        nombre: string;
        ruc: string;
        direccion: string;
        telefono: string;
        email: string;
    };

    // Emisor (Usuario/Socio) N08 Identity
    emisor: {
        nombre: string;
        empresa: string;
        ruc: string;
        direccion: string;
        logo: string;
        firma: string;
    };

    // Proyecto
    proyecto: {
        nombre: string;
        descripcion: string;
        ubicacion: string;
        presupuesto: number;
        duracion: number;
        fechaInicio: string;
        fechaFin: string;
    };

    // Profesionales
    profesionales: Array<{
        nombre: string;
        cargo: string;
        especialidad: string;
        registro: string;
    }>;

    // Suministros
    suministros: Array<{
        item: string;
        descripcion: string;
        cantidad: number;
        unidad: string;
        precioUnitario: number;
        precioTotal: number;
    }>;

    // Entregables
    entregables: Array<{
        nombre: string;
        descripcion: string;
        fecha: string;
        responsable: string;
    }>;

    // Fases (para proyectos complejos)
    fases?: Array<{
        nombre: string;
        descripcion: string;
        duracion: number;
        presupuesto: number;
        actividades: Array<{
            nombre: string;
            duracion: number;
            responsable: string;
        }>;
    }>;

    // Riesgos (para proyectos complejos)
    riesgos?: Array<{
        descripcion: string;
        probabilidad: 'baja' | 'media' | 'alta';
        impacto: 'bajo' | 'medio' | 'alto';
        mitigacion: string;
    }>;

    // Stakeholders (para proyectos complejos)
    stakeholders?: Array<{
        nombre: string;
        rol: string;
        interes: 'bajo' | 'medio' | 'alto';
        poder: 'bajo' | 'medio' | 'alto';
    }>;

    // Additional data (conclusions, recommendations for reports)
    titulo?: string;
    codigo?: string;
    resumen_ejecutivo?: string;
    introduccion?: string;
    analisis_tecnico?: string;
    resultados?: string;
    conclusiones?: string;
    recomendaciones?: string[];
}

interface DocumentStore {
    // State
    documentId: number | null;
    documentType: DocumentType;
    documentData: DocumentData;
    colorScheme: ColorScheme;
    logo: string | null;
    font: string;
    isEditing: boolean;
    isSaving: boolean;
    lastSaved: Date | null;
    error: string | null;

    // Actions
    setDocumentType: (type: DocumentType) => void;
    updateData: (data: Partial<DocumentData>) => void;
    setColorScheme: (scheme: ColorScheme) => void;
    setLogo: (logo: string | null) => void;
    setFont: (font: string) => void;
    setIsEditing: (editing: boolean) => void;
    resetDocument: () => void;
    loadDocument: (data: DocumentData) => void;

    // Async Actions
    saveDocument: (userId: string, title: string) => Promise<void>;
    fetchDocument: (id: number) => Promise<void>;
}

// Initial document data
const initialDocumentData: DocumentData = {
    cliente: {
        nombre: '',
        ruc: '',
        direccion: '',
        telefono: '',
        email: '',
    },
    emisor: {
        nombre: '',
        empresa: '',
        ruc: '',
        direccion: '',
        logo: '',
        firma: '',
    },
    proyecto: {
        nombre: '',
        descripcion: '',
        ubicacion: '',
        presupuesto: 0,
        duracion: 0,
        fechaInicio: new Date().toISOString().split('T')[0],
        fechaFin: '',
    },
    profesionales: [],
    suministros: [],
    entregables: [],
    recomendaciones: [],
};

export const useDocumentStore = create<DocumentStore>()(
    persist(
        (set, get) => ({
            // Initial state
            documentId: null,
            documentType: 'proyecto-simple',
            documentData: initialDocumentData,
            colorScheme: 'azul-tesla',
            logo: null,
            font: 'Calibri',
            isEditing: false,
            isSaving: false,
            lastSaved: null,
            error: null,

            // Actions
            setDocumentType: (type) => set({ documentType: type }),

            updateData: (data) => set((state) => ({
                documentData: {
                    ...state.documentData,
                    ...data,
                },
            })),

            setColorScheme: (scheme) => set({ colorScheme: scheme }),

            setLogo: (logo) => set({ logo }),

            setFont: (font) => set({ font }),

            setIsEditing: (editing) => set({ isEditing: editing }),

            resetDocument: () => set({
                documentId: null,
                documentData: initialDocumentData,
                logo: null,
                isEditing: false,
                isSaving: false,
                lastSaved: null,
                error: null,
            }),

            loadDocument: (data) => set({
                documentData: data,
                lastSaved: new Date(),
            }),

            // Async Actions
            saveDocument: async (userId, title) => {
                set({ isSaving: true, error: null });
                try {
                    const { documentId, documentType, documentData, colorScheme, font } = get();

                    let response;
                    if (documentId) {
                        // Update existing
                        response = await documentService.updateDocument(documentId, {
                            title,
                            type: documentType,
                            data: documentData,
                            color_scheme: colorScheme,
                            font,
                            user_id: userId,
                        });
                    } else {
                        // Create new
                        response = await documentService.createDocument({
                            title,
                            type: documentType,
                            data: documentData,
                            color_scheme: colorScheme,
                            font,
                            user_id: userId,
                        });
                    }

                    set({
                        documentId: response.id,
                        lastSaved: new Date(),
                        isSaving: false
                    });
                } catch (error) {
                    console.error('Failed to save document:', error);
                    set({
                        isSaving: false,
                        error: 'Error al guardar el documento'
                    });
                }
            },

            fetchDocument: async (id) => {
                set({ isSaving: true, error: null });
                try {
                    const doc = await documentService.getDocument(id);
                    set({
                        documentId: doc.id,
                        documentType: doc.type,
                        documentData: doc.data,
                        colorScheme: doc.color_scheme,
                        font: doc.font,
                        isSaving: false,
                        lastSaved: new Date(doc.updated_at || doc.created_at)
                    });
                } catch (error) {
                    console.error('Failed to fetch document:', error);
                    set({
                        isSaving: false,
                        error: 'Error al cargar el documento'
                    });
                }
            }
        }),
        {
            name: 'document-storage',
            partialize: (state) => ({
                documentId: state.documentId,
                documentType: state.documentType,
                documentData: state.documentData,
                colorScheme: state.colorScheme,
                logo: state.logo,
                font: state.font,
            }),
        }
    )
);
