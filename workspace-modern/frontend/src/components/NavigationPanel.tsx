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
        id: 'proyectos',
        label: 'Proyectos',
        icon: FolderOpen,
        subsections: [
            { id: 'proyecto-simple', label: 'Simple', badge: 3 },
            { id: 'proyecto-complejo', label: 'Complejo', badge: 1 },
        ],
    },
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
        id: 'informes',
        label: 'Informes',
        icon: BarChart3,
        subsections: [
            { id: 'informe-tecnico', label: 'Técnico' },
            { id: 'informe-ejecutivo', label: 'Ejecutivo' },
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
            className="w-64 bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 p-4 overflow-y-auto"
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
                                onClick={() => toggleSection(section.id)}
                                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg transition-colors ${activeSection === section.id
                                        ? 'bg-brand-red text-white'
                                        : 'hover:bg-gray-200 dark:hover:bg-gray-800'
                                    }`}
                            >
                                <div className="flex items-center gap-2">
                                    <Icon className="w-5 h-5" />
                                    <span className="font-medium">{section.label}</span>
                                </div>
                                {isExpanded ? (
                                    <ChevronDown className="w-4 h-4" />
                                ) : (
                                    <ChevronRight className="w-4 h-4" />
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
                                                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-colors ${activeSection === subsection.id
                                                        ? 'bg-brand-yellow text-gray-900'
                                                        : 'hover:bg-gray-200 dark:hover:bg-gray-800'
                                                    }`}
                                            >
                                                <span>{subsection.label}</span>
                                                {subsection.badge && (
                                                    <span className="px-2 py-0.5 bg-brand-red text-white text-xs rounded-full">
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
                        className="w-full flex items-center gap-2 px-3 py-2 rounded-lg bg-gradient-to-r from-brand-red to-brand-yellow text-white font-medium"
                    >
                        <Zap className="w-4 h-4" />
                        Nuevo Proyecto
                    </motion.button>
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="w-full flex items-center gap-2 px-3 py-2 rounded-lg border border-brand-red text-brand-red hover:bg-brand-red hover:text-white transition-colors"
                    >
                        <Calculator className="w-4 h-4" />
                        Calculadora
                    </motion.button>
                </div>
            </div>
        </motion.nav>
    )
}
