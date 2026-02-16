import { create } from 'zustand'
import { apiClient } from '@/lib/api-client'

// Interfaces
export interface Project {
    id: string
    name: string
    type: 'simple' | 'complex'
    status: 'active' | 'pending' | 'completed'
    progress: number
    budget: number
    daysRemaining: number
    description: string
    updatedAt: string
}

export interface Quote {
    id: string
    clientName: string
    projectName: string
    amount: number
    status: 'approved' | 'pending' | 'draft'
    createdAt: string
}

export interface Report {
    id: string
    name: string
    type: 'technical' | 'executive'
    date: string
    description: string
}

type Theme = 'light' | 'dark' | 'magenta' | 'tesla'

interface WorkspaceStore {
    // UI State
    activeSection: string
    setActiveSection: (section: string) => void
    theme: Theme
    setTheme: (theme: Theme) => void
    sidebarOpen: boolean
    setSidebarOpen: (open: boolean) => void

    // Data State
    projects: Project[]
    quotes: Quote[]
    reports: Report[]
    isLoading: boolean
    error: string | null

    // Async Actions
    fetchProjects: () => Promise<void>
    fetchQuotes: () => Promise<void>
    createProject: (project: Omit<Project, 'id' | 'updatedAt'>) => Promise<void>
    createQuote: (quote: Omit<Quote, 'id' | 'createdAt'>) => Promise<void>

    // Chat State
    chatMessages: Array<{ role: 'user' | 'assistant', content: string, suggestions?: any[], thought_trace?: string[] }>
    addChatMessage: (msg: { role: 'user' | 'assistant', content: string, suggestions?: any[], thought_trace?: string[] }) => void
    clearChat: () => void
}

// Helper: Map Backend Document to Frontend Project
const mapDocToProject = (doc: any): Project => ({
    id: doc.id.toString(),
    name: doc.title,
    type: doc.type === 'proyecto-simple' ? 'simple' : 'complex',
    status: doc.data.status || 'active',
    progress: doc.data.progress || 0,
    budget: doc.data.budget || 0,
    daysRemaining: doc.data.daysRemaining || 0,
    description: doc.data.description || '',
    updatedAt: doc.updated_at || doc.created_at
})

// Helper: Map Backend Document to Frontend Quote
const mapDocToQuote = (doc: any): Quote => ({
    id: doc.id.toString(), // or doc.data.quoteId
    clientName: doc.data.clientName || 'Cliente Desconocido',
    projectName: doc.title, // Quote title usually describes the project/quote
    amount: doc.data.amount || 0,
    status: doc.data.status || 'draft',
    createdAt: doc.created_at
})

const USER_ID = 'demo-user-123'
const API_URL = 'http://localhost:8005/api/documents'

export const useWorkspaceStore = create<WorkspaceStore>((set, get) => ({
    // Initial UI State
    activeSection: 'dashboard', // Set to start at empty/dashboard
    setActiveSection: (section) => set({ activeSection: section }),

    theme: 'dark', // Default Dark Mode
    setTheme: (theme) => set({ theme }),

    sidebarOpen: true,
    setSidebarOpen: (open) => set({ sidebarOpen: open }),

    // Initial Data State
    projects: [],
    quotes: [],
    reports: [],
    isLoading: false,
    error: null,

    // Actions
    fetchProjects: async () => {
        set({ isLoading: true })
        try {
            // Use apiClient to leverage relative path /api and configured base URL
            const docs = await apiClient.get<any[]>(`/api/documents/?user_id=${USER_ID}&type=proyecto`)
            set({ projects: docs.map(mapDocToProject) })
        } catch (err: any) {
            console.error(err)
            set({ error: err.message })
        } finally {
            set({ isLoading: false })
        }
    },

    fetchQuotes: async () => {
        set({ isLoading: true })
        try {
            const docs = await apiClient.get<any[]>(`/api/documents/?user_id=${USER_ID}&type=cotizacion`)
            set({ quotes: docs.map(mapDocToQuote) })
        } catch (err: any) {
            console.error(err)
            set({ error: err.message })
        } finally {
            set({ isLoading: false })
        }
    },

    createProject: async (projectData) => {
        set({ isLoading: true })
        try {
            const payload = {
                title: projectData.name,
                type: projectData.type === 'simple' ? 'proyecto-simple' : 'proyecto-complex',
                data: {
                    description: projectData.description,
                    status: projectData.status,
                    progress: projectData.progress,
                    budget: projectData.budget,
                    daysRemaining: projectData.daysRemaining
                },
                user_id: USER_ID
            }

            const res = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })

            if (!res.ok) throw new Error('Failed to create project')
            await get().fetchProjects() // Refresh list
        } catch (err: any) {
            set({ error: err.message })
        } finally {
            set({ isLoading: false })
        }
    },

    createQuote: async (_quoteData) => {
        // Implementation similar to createProject
        // For brevity, skipping logic until explicitly needed by user interaction
    },

    // Chat Implementation
    chatMessages: [],
    addChatMessage: (msg) => set((state) => ({ chatMessages: [...state.chatMessages, msg] })),
    clearChat: () => set({ chatMessages: [] })
}))
