"""
Document Store - Zustand State Management
Manages document data, type, settings, and editing state
"""
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

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
}

interface DocumentStore {
    // State
    documentType: DocumentType;
    documentData: DocumentData;
    colorScheme: ColorScheme;
    logo: string | null;
    font: string;
    isEditing: boolean;
    isSaving: boolean;
    lastSaved: Date | null;

    // Actions
    setDocumentType: (type: DocumentType) => void;
    updateData: (data: Partial<DocumentData>) => void;
    setColorScheme: (scheme: ColorScheme) => void;
    setLogo: (logo: string | null) => void;
    setFont: (font: string) => void;
    setIsEditing: (editing: boolean) => void;
    setIsSaving: (saving: boolean) => void;
    resetDocument: () => void;
    loadDocument: (data: DocumentData) => void;
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
    proyecto: {
        nombre: '',
        descripcion: '',
        ubicacion: '',
        presupuesto: 0,
        duracion: 0,
        fechaInicio: '',
        fechaFin: '',
    },
    profesionales: [],
    suministros: [],
    entregables: [],
};

export const useDocumentStore = create<DocumentStore>()(
    persist(
        (set) => ({
            // Initial state
            documentType: 'proyecto-simple',
            documentData: initialDocumentData,
            colorScheme: 'azul-tesla',
            logo: null,
            font: 'Calibri',
            isEditing: false,
            isSaving: false,
            lastSaved: null,

            // Actions
            setDocumentType: (type) => set({ documentType: type }),

            updateData: (data) => set((state) => ({
                documentData: {
                    ...state.documentData,
                    ...data,
                },
                lastSaved: new Date(),
            })),

            setColorScheme: (scheme) => set({ colorScheme: scheme }),

            setLogo: (logo) => set({ logo }),

            setFont: (font) => set({ font }),

            setIsEditing: (editing) => set({ isEditing: editing }),

            setIsSaving: (saving) => set({ isSaving: saving }),

            resetDocument: () => set({
                documentData: initialDocumentData,
                logo: null,
                isEditing: false,
                isSaving: false,
                lastSaved: null,
            }),

            loadDocument: (data) => set({
                documentData: data,
                lastSaved: new Date(),
            }),
        }),
        {
            name: 'document-storage', // LocalStorage key
            partialize: (state) => ({
                documentType: state.documentType,
                documentData: state.documentData,
                colorScheme: state.colorScheme,
                logo: state.logo,
                font: state.font,
            }),
        }
    )
);
