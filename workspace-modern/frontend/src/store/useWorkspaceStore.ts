import { create } from 'zustand'

// Mock data interfaces
interface Project {
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

interface Quote {
    id: string
    clientName: string
    projectName: string
    amount: number
    status: 'approved' | 'pending' | 'draft'
    createdAt: string
}

interface Report {
    id: string
    name: string
    type: 'technical' | 'executive'
    date: string
    description: string
}

interface WorkspaceStore {
    activeSection: string
    setActiveSection: (section: string) => void
    theme: 'light' | 'dark' | 'system'
    setTheme: (theme: 'light' | 'dark' | 'system') => void
    sidebarOpen: boolean
    setSidebarOpen: (open: boolean) => void

    // Mock data
    projects: Project[]
    quotes: Quote[]
    reports: Report[]

    // Actions
    addProject: (project: Project) => void
    addQuote: (quote: Quote) => void
    addReport: (report: Report) => void
}

// Mock data
const mockProjects: Project[] = [
    {
        id: '1',
        name: 'Instalación Residencial Norte',
        type: 'simple',
        status: 'active',
        progress: 65,
        budget: 15000,
        daysRemaining: 12,
        description: 'Instalación eléctrica completa para residencia de 3 pisos',
        updatedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: '2',
        name: 'Sistema Comercial Plaza Central',
        type: 'simple',
        status: 'active',
        progress: 40,
        budget: 28000,
        daysRemaining: 25,
        description: 'Sistema eléctrico para local comercial',
        updatedAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: '3',
        name: 'Proyecto Industrial Zona Este',
        type: 'simple',
        status: 'pending',
        progress: 15,
        budget: 45000,
        daysRemaining: 60,
        description: 'Instalación industrial con subestación',
        updatedAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: '4',
        name: 'Edificio Comercial - Centro',
        type: 'complex',
        status: 'active',
        progress: 75,
        budget: 250000,
        daysRemaining: 45,
        description: 'Sistema eléctrico completo + iluminación LED + automatización',
        updatedAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    },
]

const mockQuotes: Quote[] = [
    {
        id: 'COT-1001',
        clientName: 'Constructora ABC',
        projectName: 'Instalación eléctrica residencial',
        amount: 15750.50,
        status: 'approved',
        createdAt: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: 'COT-1002',
        clientName: 'Inmobiliaria XYZ',
        projectName: 'Sistema eléctrico comercial',
        amount: 28900.00,
        status: 'pending',
        createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: 'COT-1003',
        clientName: 'Desarrollos del Norte',
        projectName: 'Instalación industrial',
        amount: 45200.75,
        status: 'draft',
        createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: 'COT-1004',
        clientName: 'Grupo Empresarial Sur',
        projectName: 'Edificio corporativo',
        amount: 125000.00,
        status: 'approved',
        createdAt: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: 'COT-1005',
        clientName: 'Inversiones Pacífico',
        projectName: 'Centro comercial',
        amount: 89500.50,
        status: 'pending',
        createdAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: 'COT-1006',
        clientName: 'Constructora Moderna',
        projectName: 'Complejo residencial',
        amount: 67800.00,
        status: 'approved',
        createdAt: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: 'COT-1007',
        clientName: 'Desarrollos Urbanos',
        projectName: 'Torre de oficinas',
        amount: 198000.00,
        status: 'draft',
        createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: 'COT-1008',
        clientName: 'Inmuebles del Centro',
        projectName: 'Renovación eléctrica',
        amount: 34500.25,
        status: 'pending',
        createdAt: new Date(Date.now() - 12 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: 'COT-1009',
        clientName: 'Proyectos Integrales',
        projectName: 'Parque industrial',
        amount: 275000.00,
        status: 'approved',
        createdAt: new Date(Date.now() - 25 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
        id: 'COT-1010',
        clientName: 'Constructora Elite',
        projectName: 'Hotel boutique',
        amount: 156000.75,
        status: 'pending',
        createdAt: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString(),
    },
]

const mockReports: Report[] = [
    {
        id: '1',
        name: 'Informe Mensual - Enero 2026',
        type: 'technical',
        date: new Date().toLocaleDateString(),
        description: 'Análisis técnico de proyectos en curso y métricas de rendimiento',
    },
    {
        id: '2',
        name: 'Resumen Ejecutivo Q1 2026',
        type: 'executive',
        date: new Date().toLocaleDateString(),
        description: 'Resumen ejecutivo del primer trimestre con indicadores clave',
    },
    {
        id: '3',
        name: 'Análisis de Costos - Diciembre 2025',
        type: 'technical',
        date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toLocaleDateString(),
        description: 'Desglose detallado de costos por proyecto',
    },
    {
        id: '4',
        name: 'Informe de Progreso - Semana 4',
        type: 'executive',
        date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toLocaleDateString(),
        description: 'Progreso semanal de todos los proyectos activos',
    },
]

export const useWorkspaceStore = create<WorkspaceStore>((set) => ({
    activeSection: 'proyectos',
    setActiveSection: (section) => set({ activeSection: section }),

    theme: 'dark',
    setTheme: (theme) => set({ theme }),

    sidebarOpen: true,
    setSidebarOpen: (open) => set({ sidebarOpen: open }),

    // Mock data
    projects: mockProjects,
    quotes: mockQuotes,
    reports: mockReports,

    // Actions
    addProject: (project) =>
        set((state) => ({ projects: [...state.projects, project] })),
    addQuote: (quote) =>
        set((state) => ({ quotes: [...state.quotes, quote] })),
    addReport: (report) =>
        set((state) => ({ reports: [...state.reports, report] })),
}))
