import { create } from 'zustand'

interface WorkspaceStore {
    activeSection: string
    setActiveSection: (section: string) => void
    theme: 'light' | 'dark' | 'system'
    setTheme: (theme: 'light' | 'dark' | 'system') => void
    sidebarOpen: boolean
    setSidebarOpen: (open: boolean) => void
}

export const useWorkspaceStore = create<WorkspaceStore>((set) => ({
    activeSection: 'proyectos',
    setActiveSection: (section) => set({ activeSection: section }),

    theme: 'dark',
    setTheme: (theme) => set({ theme }),

    sidebarOpen: true,
    setSidebarOpen: (open) => set({ sidebarOpen: open }),
}))
