import { motion, AnimatePresence } from 'framer-motion'
import {
    FileText,
    FolderOpen,
    BarChart3,
    ChevronDown,
    ChevronRight,
    Zap,
    Calculator
} from 'lucide-react'
import { useState } from 'react'
import { useWorkspaceStore } from '../store/useWorkspaceStore'

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
            className="w-full h-full bg-gray-50 dark:bg-gray-900 p-4 overflow-y-auto"
        >
            <div className="space-y-2">
                {navSections.map((section) => {
                    const Icon = section.icon
                    const isExpanded = expandedSections.includes(section.id)

                    return (
                        <div key={section.id} className="space-y-1">
                            <motion.button
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                onClick={() => {
                                    setActiveSection(section.id)
                                    toggleSection(section.id)
                                }}
                                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg transition-all backdrop-blur-sm border ${activeSection === section.id || section.subsections?.some(s => s.id === activeSection)
                                        ? 'bg-red-600/20 text-white border-red-500/30 shadow-lg'
                                        : 'bg-white/5 hover:bg-white/10 text-gray-300 border-white/10'
                                    }`}
                            >
                                <div className="flex items-center gap-2">
                                    <Icon className="w-4 h-4" />
                                    <span className="font-medium text-sm">{section.label}</span>
                                </div>
                                {isExpanded ? (
                                    <ChevronDown className="w-3 h-3" />
                                ) : (
                                    <ChevronRight className="w-3 h-3" />
                                )}
                            </motion.button>

                            <AnimatePresence>
                                {isExpanded && section.subsections && (
                                    <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: 'auto', opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        transition={{ duration: 0.2 }}
                                        className="ml-4 space-y-1 overflow-hidden"
                                    >
                                        {section.subsections.map((subsection) => (
                                            <motion.button
                                                key={subsection.id}
                                                whileHover={{ scale: 1.02, x: 4 }}
                                                whileTap={{ scale: 0.98 }}
                                                onClick={() => setActiveSection(subsection.id)}
                                                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-all backdrop-blur-sm border ${activeSection === subsection.id
                                                        ? 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30 shadow-lg'
                                                        : 'bg-white/5 hover:bg-white/10 text-gray-400 border-white/10'
                                                    }`}
                                            >
                                                <span className="text-xs">{subsection.label}</span>
                                                {subsection.badge && (
                                                    <span className="px-2 py-0.5 bg-red-600/80 text-white text-xs rounded-full backdrop-blur-sm">
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

            {/* Quick Actions */}
            <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-800">
                <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase mb-3">
                    Acciones Rápidas
                </h3>
                <div className="space-y-2">
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="w-full flex items-center gap-2 px-3 py-2 rounded-lg bg-gradient-to-r from-red-600/30 to-yellow-600/30 backdrop-blur-sm border border-yellow-500/30 text-white font-medium shadow-lg transition-all"
                    >
                        <Zap className="w-4 h-4" />
                        <span className="text-sm">Nuevo Proyecto</span>
                    </motion.button>
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="w-full flex items-center gap-2 px-3 py-2 rounded-lg bg-red-600/10 hover:bg-red-600/20 backdrop-blur-sm border border-red-500/30 text-red-400 hover:text-red-300 transition-all"
                    >
                        <Calculator className="w-4 h-4" />
                        <span className="text-sm">Calculadora</span>
                    </motion.button>
                </div>
            </div>
        </motion.nav>
    )
}
