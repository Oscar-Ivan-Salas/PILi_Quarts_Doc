import { motion, AnimatePresence } from 'framer-motion'
import {
    FileText,
    FolderOpen,
    BarChart3,
    ChevronDown,
    ChevronRight,
    Zap,
    Calculator,
    LayoutDashboard
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
            { id: 'cotizacion-simple', label: 'Simple', badge: 10 },
            { id: 'cotizacion-compleja', label: 'Compleja', badge: 3 },
        ],
    },
    {
        id: 'proyectos',
        label: 'Proyectos',
        icon: FolderOpen,
        subsections: [
            { id: 'proyecto-simple', label: 'Simple', badge: 3 },
            { id: 'proyecto-complejo', label: 'Complejo', badge: 1 },
        ],
    },
    {
        id: 'informes',
        label: 'Informes',
        icon: BarChart3,
        subsections: [
            { id: 'informe-simple', label: 'Simple' },
            { id: 'informe-complejo', label: 'Complejo' },
        ],
    },
]

export function NavigationPanel() {
    const { activeSection, setActiveSection } = useWorkspaceStore()
    const [expandedSections, setExpandedSections] = useState<string[]>(['proyectos'])

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
            className="w-full h-full studio-glass flex flex-col overflow-hidden border-r border-white/5 font-sans"
        >
            <div className="flex-1 overflow-y-auto p-5 space-y-4 custom-scrollbar">
                {/* Branding Mini indicator */}
                <div className="mb-8 px-2">
                    <div className="flex items-center gap-3">
                        <div className="p-1.5 rounded bg-[#0052A3]/10 border border-[#0052A3]/20 shadow-[0_0_15px_rgba(0,82,163,0.2)]">
                            <LayoutDashboard className="w-4 h-4 text-[#0052A3]" />
                        </div>
                        <div className="flex flex-col">
                            <span className="text-[10px] font-black tracking-[0.2em] uppercase text-white/90">PILi_Quarts</span>
                            <span className="text-[8px] tracking-[0.1em] uppercase text-gray-500 font-medium">Studio Engine v4.0</span>
                        </div>
                    </div>
                </div>

                {navSections.map((section) => {
                    const Icon = section.icon
                    const isExpanded = expandedSections.includes(section.id)

                    return (
                        <div key={section.id} className="space-y-1.5">
                            <motion.button
                                whileHover={{ scale: 1.01, backgroundColor: "rgba(255,255,255,0.02)" }}
                                whileTap={{ scale: 0.98 }}
                                onClick={() => toggleSection(section.id)}
                                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg transition-all border border-transparent ${activeSection === section.id
                                    ? 'bg-[#0052A3]/10 text-white border-[#0052A3]/20'
                                    : 'text-gray-400 hover:text-white'
                                    }`}
                            >
                                <div className="flex items-center gap-3">
                                    <Icon className={`w-4 h-4 ${activeSection === section.id ? 'text-[#0052A3]' : 'text-gray-500'}`} strokeWidth={1.5} />
                                    <span className="text-[11px] font-bold tracking-wider uppercase">{section.label}</span>
                                </div>
                                {isExpanded ? (
                                    <ChevronDown className="w-3.5 h-3.5 opacity-30" />
                                ) : (
                                    <ChevronRight className="w-3.5 h-3.5 opacity-30" />
                                )}
                            </motion.button>

                            <AnimatePresence>
                                {isExpanded && (
                                    <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: 'auto', opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        className="ml-5 pl-4 border-l border-white/5 space-y-1 overflow-hidden"
                                    >
                                        {section.subsections?.map((subsection) => (
                                            <motion.button
                                                key={subsection.id}
                                                whileHover={{ x: 2, color: "#fff" }}
                                                onClick={() => setActiveSection(subsection.id)}
                                                className={`w-full flex items-center justify-between px-3 py-1.5 rounded-md text-[10px] transition-all uppercase tracking-tight ${activeSection === subsection.id
                                                    ? 'text-[#0052A3] font-black'
                                                    : 'text-gray-600 font-medium'
                                                    }`}
                                            >
                                                <span>{subsection.label}</span>
                                                {subsection.badge && (
                                                    <span className="px-1.5 py-0.5 bg-[#0052A3]/5 text-[#0052A3] text-[9px] rounded-full border border-[#0052A3]/10">
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

                {/* Quick Actions Sections */}
                <div className="mt-10 pt-8 border-t border-white/5 px-2">
                    <h3 className="text-[9px] font-bold text-gray-700 uppercase mb-5 tracking-[0.2em]">
                        Operaciones
                    </h3>
                    <div className="space-y-3">
                        <motion.button
                            whileHover={{ scale: 1.02, backgroundColor: "#0052A3" }}
                            whileTap={{ scale: 0.98 }}
                            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-[#0052A3] text-white text-[10px] font-black shadow-[0_0_20px_rgba(0,82,163,0.3)] transition-all uppercase"
                        >
                            <Zap className="w-4 h-4" strokeWidth={2} />
                            Nuevo Proyecto
                        </motion.button>
                        <motion.button
                            whileHover={{ scale: 1.02, backgroundColor: "rgba(255,255,255,0.04)" }}
                            whileTap={{ scale: 0.98 }}
                            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg border border-white/10 text-gray-500 text-[10px] font-bold transition-all uppercase"
                        >
                            <Calculator className="w-4 h-4" strokeWidth={1.5} />
                            Calculadora
                        </motion.button>
                    </div>
                </div>
            </div>

            <ProfessionalFooter />
        </motion.nav>
    )
}
