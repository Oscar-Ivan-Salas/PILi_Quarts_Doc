import { motion, AnimatePresence } from 'framer-motion'
import {
    FileText,
    FolderOpen,
    Workflow,
    Zap,
    Globe,
    Cpu,
    ChevronDown,
    ChevronRight
} from 'lucide-react'
import { useState } from 'react'
import { useWorkspaceStore } from '../store/useWorkspaceStore'
import { ProfessionalFooter } from './ProfessionalFooter'
import { ServiceMatrix } from './stitch/ServiceMatrix'
import { AdminDashboardStats } from './stitch/AdminDashboardStats'

interface NavSection {
    id: string
    label: string
    icon: any
    subsections?: { id: string; label: string; badge?: number }[]
}

const navSections: NavSection[] = [
    {
        id: 'cotizaciones',
        label: 'Cotizaciones',
        icon: FileText,
        subsections: [
            { id: 'cotizacion-simple', label: 'Simple', badge: 12 },
            { id: 'cotizacion-compleja', label: 'Ingeniería', badge: 5 },
        ],
    },
    {
        id: 'proyectos',
        label: 'Proyectos',
        icon: FolderOpen,
        subsections: [
            { id: 'proyecto-simple', label: 'Activos', badge: 8 },
            { id: 'proyecto-complejo', label: 'Archivados' },
        ],
    },
    {
        id: 'informes',
        label: 'Intelligence',
        icon: Workflow,
        subsections: [
            { id: 'informe-simple', label: 'Reportes' },
            { id: 'informe-complejo', label: 'Métricas' },
        ],
    },
]

export function NavigationPanel() {
    const { activeSection, setActiveSection } = useWorkspaceStore()
    const [expandedSections, setExpandedSections] = useState<string[]>(['cotizaciones'])

    const toggleSection = (sectionId: string) => {
        setExpandedSections((prev) =>
            prev.includes(sectionId)
                ? prev.filter((id) => id !== sectionId)
                : [...prev, sectionId]
        )
    }

    return (
        <motion.nav
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="w-full h-full bg-black/40 flex flex-col overflow-hidden border-r border-white/5 font-sans relative"
        >
            {/* Subtle Vertical Scanning Line */}
            <div className="absolute right-0 top-0 w-[0.5px] h-full bg-gradient-to-b from-transparent via-[#0052A3]/40 to-transparent animate-tech-pulse" />

            {/* STITCH HEADER INTEGRATION */}
            <div className="p-6 border-b border-white/5 cursor-pointer hover:bg-white/5 transition-colors" onClick={() => setActiveSection('stitch-workspace')}>
                <div className="flex items-center gap-3">
                    <div className="relative">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-blue-500/20">
                            <span className="font-bold text-white text-lg">P</span>
                        </div>
                        <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-black"></div>
                    </div>
                    <div>
                        <h1 className="font-bold text-white text-lg tracking-tight">PILI Quarts</h1>
                        <p className="text-[10px] text-blue-400 font-mono tracking-widest uppercase">Studio Edition v4.0</p>
                    </div>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto custom-scrollbar">

                {/* 1. STITCH SERVICE MATRIX (Now points to Admin Console) */}
                <div className="mt-4 px-2">
                    <div
                        className="px-3 mb-2 flex items-center justify-between cursor-pointer group"
                        onClick={() => setActiveSection('stitch-admin')}
                    >
                        <span className="text-[9px] font-black text-white/40 tracking-[0.2em] uppercase group-hover:text-white transition-colors">Admin Console</span>
                        <span className="text-[9px] bg-blue-500/10 text-blue-400 px-1.5 rounded font-mono group-hover:bg-blue-500 group-hover:text-white transition-colors">System Active</span>
                    </div>
                    {/* Tiny Matrix Preview or Just the Link? Keeping Matrix for visual density but maybe make it link too */}
                    <div onClick={() => setActiveSection('stitch-admin')} className="cursor-pointer">
                        <ServiceMatrix />
                    </div>
                </div>

                {/* 2. LEGACY NAVIGATION (Redesigned) */}
                <div className="mt-8 px-4 space-y-2">
                    <h3 className="text-[9px] font-black text-white/20 tracking-[0.4em] uppercase mb-4 px-2">
                        System Node Control
                    </h3>

                    {navSections.map((section) => {
                        const Icon = section.icon
                        const isExpanded = expandedSections.includes(section.id)
                        const isSectionActive = section.subsections?.some(s => s.id === activeSection)

                        return (
                            <div key={section.id} className="space-y-1">
                                <motion.button
                                    whileHover={{ backgroundColor: "rgba(255,255,255,0.02)" }}
                                    onClick={() => toggleSection(section.id)}
                                    className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg transition-all group ${isSectionActive
                                        ? 'bg-white/5 text-white'
                                        : 'text-white/40 hover:text-white'
                                        }`}
                                >
                                    <div className="flex items-center gap-3">
                                        <Icon className={`w-3.5 h-3.5 ${isSectionActive ? 'text-[#0052A3]' : 'text-white/20'}`} strokeWidth={1.5} />
                                        <span className="text-[10px] font-black tracking-[0.2em] uppercase">{section.label}</span>
                                    </div>
                                    <AnimatePresence mode="wait">
                                        <motion.div
                                            key={isExpanded ? 'down' : 'right'}
                                            initial={{ rotate: 0, opacity: 0 }}
                                            animate={{ rotate: 0, opacity: 1 }}
                                        >
                                            {isExpanded ? (
                                                <ChevronDown className="w-3 h-3 text-white/10" />
                                            ) : (
                                                <ChevronRight className="w-3 h-3 text-white/10" />
                                            )}
                                        </motion.div>
                                    </AnimatePresence>
                                </motion.button>

                                <AnimatePresence>
                                    {isExpanded && (
                                        <motion.div
                                            initial={{ height: 0, opacity: 0 }}
                                            animate={{ height: 'auto', opacity: 1 }}
                                            exit={{ height: 0, opacity: 0 }}
                                            className="ml-4 pl-4 border-l border-[#0052A3]/10 space-y-1 overflow-hidden"
                                        >
                                            {section.subsections?.map((subsection) => (
                                                <motion.button
                                                    key={subsection.id}
                                                    whileHover={{ x: 4, color: "#fff" }}
                                                    onClick={() => setActiveSection(subsection.id)}
                                                    className={`w-full flex items-center justify-between px-3 py-2 rounded-md text-[9px] transition-all uppercase tracking-[0.15em] ${activeSection === subsection.id
                                                        ? 'text-[#0052A3] font-black'
                                                        : 'text-white/30 font-bold hover:text-white/60'
                                                        }`}
                                                >
                                                    <div className="flex items-center gap-2">
                                                        <div className={`w-1 h-1 rounded-full ${activeSection === subsection.id ? 'bg-[#0052A3] shadow-[0_0_5px_#0052A3]' : 'bg-transparent'}`} />
                                                        <span>{subsection.label}</span>
                                                    </div>
                                                </motion.button>
                                            ))}
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>
                        )
                    })}
                </div>

                {/* 3. STITCH ADMIN DASHBOARD STATS */}
                <div className="mt-8 px-2 border-t border-white/5 pt-4 cursor-pointer hover:bg-white/5 rounded-xl transition-colors" onClick={() => setActiveSection('stitch-admin')}>
                    <AdminDashboardStats />
                </div>
            </div>

            <ProfessionalFooter />
        </motion.nav>
    )
}
