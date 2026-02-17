import { motion, AnimatePresence } from 'framer-motion'
import {
    FileText,
    FolderOpen,
    BarChart3,
    ChevronDown,
    ChevronRight,
    Zap,
    Calculator,
    LayoutDashboard,
    Globe,
    Cpu,
    Workflow
} from 'lucide-react'
import { useState } from 'react'
import { useWorkspaceStore } from '../store/useWorkspaceStore'
import { ProfessionalFooter } from './ProfessionalFooter'

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

            <div className="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar">
                {/* System Nodes Section */}
                <div className="space-y-6">
                    <div className="px-2">
                        <h3 className="text-[9px] font-black text-white/20 tracking-[0.4em] uppercase mb-6">
                            System Node Control
                        </h3>
                    </div>

                    {navSections.map((section) => {
                        const Icon = section.icon
                        const isExpanded = expandedSections.includes(section.id)
                        const isSectionActive = section.subsections?.some(s => s.id === activeSection)

                        return (
                            <div key={section.id} className="space-y-2">
                                <motion.button
                                    whileHover={{ backgroundColor: "rgba(255,255,255,0.02)" }}
                                    onClick={() => toggleSection(section.id)}
                                    className={`w-full flex items-center justify-between px-3 py-3 rounded-lg transition-all group ${isSectionActive
                                        ? 'bg-white/5 text-white'
                                        : 'text-white/40 hover:text-white'
                                        }`}
                                >
                                    <div className="flex items-center gap-4">
                                        <div className={`p-1.5 rounded-md border transition-all ${isSectionActive ? 'border-[#0052A3]/50 bg-[#0052A3]/10' : 'border-white/5 bg-white/5'}`}>
                                            <Icon className={`w-3.5 h-3.5 ${isSectionActive ? 'text-[#0052A3]' : 'text-white/20'}`} strokeWidth={1.5} />
                                        </div>
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
                                            className="ml-6 pl-5 border-l border-[#0052A3]/10 space-y-1 overflow-hidden"
                                        >
                                            {section.subsections?.map((subsection) => (
                                                <motion.button
                                                    key={subsection.id}
                                                    whileHover={{ x: 4, color: "#fff" }}
                                                    onClick={() => setActiveSection(subsection.id)}
                                                    className={`w-full flex items-center justify-between px-3 py-2.5 rounded-md text-[9px] transition-all uppercase tracking-[0.15em] ${activeSection === subsection.id
                                                        ? 'text-[#0052A3] font-black'
                                                        : 'text-white/30 font-bold hover:text-white/60'
                                                        }`}
                                                >
                                                    <div className="flex items-center gap-3">
                                                        <div className={`w-1 h-1 rounded-full ${activeSection === subsection.id ? 'bg-[#0052A3] shadow-[0_0_5px_#0052A3]' : 'bg-transparent'}`} />
                                                        <span>{subsection.label}</span>
                                                    </div>
                                                    {subsection.badge && (
                                                        <span className="text-[8px] font-mono text-white/20 bg-white/5 px-1.5 py-0.5 rounded border border-white/5">
                                                            {subsection.badge}
                                                        </span>
                                                    )}
                                                </motion.button>
                                            ))}
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>
                        )
                    })}
                </div>

                {/* Operations Layer */}
                <div className="pt-8 border-t border-white/5">
                    <h3 className="text-[9px] font-black text-white/20 tracking-[0.4em] uppercase mb-6 px-2">
                        Execution Layer
                    </h3>
                    <div className="space-y-4 px-2">
                        <motion.button
                            whileHover={{ scale: 1.02, backgroundColor: "#0052A3" }}
                            whileTap={{ scale: 0.98 }}
                            className="w-full flex items-center justify-center gap-3 py-4 rounded-xl bg-[#0052A3]/80 text-white text-[10px] font-black tracking-[0.3em] shadow-[0_15px_30px_rgba(0,82,163,0.3)] transition-all uppercase"
                        >
                            <Zap className="w-4 h-4" />
                            DEPLOY V4
                        </motion.button>

                        <div className="grid grid-cols-2 gap-3 mt-4">
                            <button className="flex flex-col items-center justify-center p-4 rounded-xl border border-white/5 bg-white/5 hover:bg-white/10 transition-all gap-2 group">
                                <Globe className="w-4 h-4 text-white/20 group-hover:text-[#0052A3]" />
                                <span className="text-[8px] text-white/40 font-black uppercase">Net</span>
                            </button>
                            <button className="flex flex-col items-center justify-center p-4 rounded-xl border border-white/5 bg-white/5 hover:bg-white/10 transition-all gap-2 group">
                                <Cpu className="w-4 h-4 text-white/20 group-hover:text-[#0052A3]" />
                                <span className="text-[8px] text-white/40 font-black uppercase">Proc</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <ProfessionalFooter />
        </motion.nav>
    )
}
