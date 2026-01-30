import { motion } from 'framer-motion'
import { useWorkspaceStore } from '../store/useWorkspaceStore'
import { FileText, FolderOpen, BarChart3, Plus, Search } from 'lucide-react'

export function WorkArea() {
    const { activeSection } = useWorkspaceStore()

    const renderContent = () => {
        switch (activeSection) {
            case 'proyecto-simple':
                return (
                    <div className="space-y-6">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                                Proyectos Simples
                            </h2>
                            <p className="text-gray-600 dark:text-gray-400">
                                Gestiona tus proyectos de construcción simples
                            </p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {[1, 2, 3].map((i) => (
                                <motion.div
                                    key={i}
                                    whileHover={{ scale: 1.02 }}
                                    className="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer"
                                >
                                    <FolderOpen className="w-8 h-8 text-brand-red mb-3" />
                                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                                        Proyecto {i}
                                    </h3>
                                    <p className="text-sm text-gray-600 dark:text-gray-400">
                                        Instalación eléctrica residencial
                                    </p>
                                    <div className="mt-4 flex items-center justify-between text-xs text-gray-500">
                                        <span>Actualizado hace 2 días</span>
                                        <span className="px-2 py-1 bg-green-100 text-green-800 rounded">Activo</span>
                                    </div>
                                </motion.div>
                            ))}
                        </div>

                        <button className="btn-primary flex items-center gap-2">
                            <Plus className="w-4 h-4" />
                            Nuevo Proyecto Simple
                        </button>
                    </div>
                )

            case 'proyecto-complejo':
                return (
                    <div className="space-y-6">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                                Proyectos Complejos
                            </h2>
                            <p className="text-gray-600 dark:text-gray-400">
                                Gestiona proyectos de gran escala con múltiples fases
                            </p>
                        </div>

                        <div className="grid grid-cols-1 gap-4">
                            {[1].map((i) => (
                                <motion.div
                                    key={i}
                                    whileHover={{ scale: 1.01 }}
                                    className="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer"
                                >
                                    <div className="flex items-start justify-between mb-4">
                                        <div className="flex items-center gap-3">
                                            <FolderOpen className="w-10 h-10 text-brand-yellow" />
                                            <div>
                                                <h3 className="font-semibold text-lg text-gray-900 dark:text-white">
                                                    Edificio Comercial - Centro
                                                </h3>
                                                <p className="text-sm text-gray-600 dark:text-gray-400">
                                                    Sistema eléctrico completo + iluminación LED
                                                </p>
                                            </div>
                                        </div>
                                        <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                                            En Progreso
                                        </span>
                                    </div>

                                    <div className="grid grid-cols-3 gap-4 mb-4">
                                        <div className="text-center p-3 bg-gray-50 dark:bg-gray-900 rounded">
                                            <p className="text-2xl font-bold text-brand-red">75%</p>
                                            <p className="text-xs text-gray-600 dark:text-gray-400">Completado</p>
                                        </div>
                                        <div className="text-center p-3 bg-gray-50 dark:bg-gray-900 rounded">
                                            <p className="text-2xl font-bold text-brand-yellow">$250K</p>
                                            <p className="text-xs text-gray-600 dark:text-gray-400">Presupuesto</p>
                                        </div>
                                        <div className="text-center p-3 bg-gray-50 dark:bg-gray-900 rounded">
                                            <p className="text-2xl font-bold text-green-600">45</p>
                                            <p className="text-xs text-gray-600 dark:text-gray-400">Días restantes</p>
                                        </div>
                                    </div>

                                    <div className="flex gap-2">
                                        <button className="btn-secondary flex-1">Ver Detalles</button>
                                        <button className="btn-primary flex-1">Editar</button>
                                    </div>
                                </motion.div>
                            ))}
                        </div>

                        <button className="btn-primary flex items-center gap-2">
                            <Plus className="w-4 h-4" />
                            Nuevo Proyecto Complejo
                        </button>
                    </div>
                )

            case 'cotizacion-simple':
            case 'cotizacion-compleja':
                return (
                    <div className="space-y-6">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                                {activeSection === 'cotizacion-simple' ? 'Cotizaciones Simples' : 'Cotizaciones Complejas'}
                            </h2>
                            <p className="text-gray-600 dark:text-gray-400">
                                Genera y gestiona cotizaciones para tus proyectos
                            </p>
                        </div>

                        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
                            <table className="w-full">
                                <thead className="bg-gray-50 dark:bg-gray-900">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cliente</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Proyecto</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                                    {[1, 2, 3, 4, 5].map((i) => (
                                        <tr key={i} className="hover:bg-gray-50 dark:hover:bg-gray-900">
                                            <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">COT-{1000 + i}</td>
                                            <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">Cliente {i}</td>
                                            <td className="px-6 py-4 text-sm text-gray-600 dark:text-gray-400">Instalación eléctrica</td>
                                            <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">${(Math.random() * 50000 + 10000).toFixed(2)}</td>
                                            <td className="px-6 py-4 text-sm">
                                                <span className={`px-2 py-1 rounded text-xs ${i % 3 === 0 ? 'bg-green-100 text-green-800' :
                                                        i % 3 === 1 ? 'bg-yellow-100 text-yellow-800' :
                                                            'bg-gray-100 text-gray-800'
                                                    }`}>
                                                    {i % 3 === 0 ? 'Aprobada' : i % 3 === 1 ? 'Pendiente' : 'Borrador'}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-sm">
                                                <button className="text-brand-red hover:text-red-700">Ver</button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>

                        <button className="btn-primary flex items-center gap-2">
                            <Plus className="w-4 h-4" />
                            Nueva Cotización
                        </button>
                    </div>
                )

            case 'informe-tecnico':
            case 'informe-ejecutivo':
                return (
                    <div className="space-y-6">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                                {activeSection === 'informe-tecnico' ? 'Informes Técnicos' : 'Informes Ejecutivos'}
                            </h2>
                            <p className="text-gray-600 dark:text-gray-400">
                                Genera informes detallados de tus proyectos
                            </p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {[1, 2, 3, 4].map((i) => (
                                <motion.div
                                    key={i}
                                    whileHover={{ scale: 1.02 }}
                                    className="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer"
                                >
                                    <BarChart3 className="w-8 h-8 text-brand-yellow mb-3" />
                                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                                        Informe {i} - {new Date().toLocaleDateString()}
                                    </h3>
                                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                                        Análisis de progreso y costos del proyecto
                                    </p>
                                    <div className="flex gap-2">
                                        <button className="btn-secondary flex-1 text-sm">Descargar PDF</button>
                                        <button className="btn-primary flex-1 text-sm">Ver</button>
                                    </div>
                                </motion.div>
                            ))}
                        </div>

                        <button className="btn-primary flex items-center gap-2">
                            <Plus className="w-4 h-4" />
                            Generar Nuevo Informe
                        </button>
                    </div>
                )

            default:
                return (
                    <div className="flex flex-col items-center justify-center h-full text-center">
                        <FileText className="w-16 h-16 text-gray-400 mb-4" />
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                            Bienvenido a PILi_Quarts
                        </h2>
                        <p className="text-gray-600 dark:text-gray-400 max-w-md">
                            Selecciona una sección del menú lateral para comenzar a trabajar en tus proyectos
                        </p>
                    </div>
                )
        }
    }

    return (
        <motion.main
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex-1 overflow-y-auto p-8 bg-gray-50 dark:bg-gray-950"
        >
            {/* Search Bar */}
            <div className="mb-6">
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Buscar proyectos, cotizaciones, informes..."
                        className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-brand-red"
                    />
                </div>
            </div>

            {/* Content */}
            {renderContent()}
        </motion.main>
    )
}
