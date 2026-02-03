import { motion } from 'framer-motion'
// @ts-ignore
import CotizacionEditor from './CotizacionEditor'
// @ts-ignore
import CotizacionesView from './workspace/CotizacionesView'
import { useState, useEffect } from 'react'
import { useWorkspaceStore } from '../store/useWorkspaceStore'
import { FileText, FolderOpen, BarChart3, Plus, Search } from 'lucide-react'

export function WorkArea() {
    const { activeSection, projects, quotes, reports } = useWorkspaceStore()

    // State for local view switching ('grid' | 'editor')
    const [viewMode, setViewMode] = useState<'grid' | 'editor'>('grid')
    const [selectedService, setSelectedService] = useState<string | null>(null)

    // Reset view when section changes
    useEffect(() => {
        setViewMode('grid')
        setSelectedService(null)
    }, [activeSection])

    const handleServiceSelect = (serviceId: string) => {
        console.log('Service Selected:', serviceId)
        setSelectedService(serviceId)
        setViewMode('editor')
    }

    const renderContent = () => {
        switch (activeSection) {
            case 'proyecto-simple':
                const simpleProjects = projects.filter(p => p.type === 'simple')
                return (
                    <div className="space-y-6">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                                Proyectos Simples
                            </h2>
                            <p className="text-gray-600 dark:text-gray-400">
                                Gestiona tus proyectos de construcción simples ({simpleProjects.length} activos)
                            </p>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {simpleProjects.map((project) => (
                                <motion.div
                                    key={project.id}
                                    whileHover={{ scale: 1.02 }}
                                    className="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer"
                                >
                                    <FolderOpen className="w-8 h-8 text-brand-red mb-3" />
                                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1">{project.name}</h3>
                                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">{project.description}</p>
                                    <div className="space-y-2">
                                        <div className="flex justify-between text-xs">
                                            <span className="text-gray-500">Progreso</span>
                                            <span className="font-medium text-gray-900 dark:text-white">{project.progress}%</span>
                                        </div>
                                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                                            <div className="bg-brand-red h-2 rounded-full transition-all" style={{ width: `${project.progress}%` }} />
                                        </div>
                                    </div>
                                    <div className="mt-4 flex items-center justify-between text-xs text-gray-500">
                                        <span>Actualizado {new Date(project.updatedAt).toLocaleDateString()}</span>
                                        <span className={`px-2 py-1 rounded ${project.status === 'active' ? 'bg-green-100 text-green-800' : project.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'}`}>
                                            {project.status === 'active' ? 'Activo' : project.status === 'pending' ? 'Pendiente' : 'Completado'}
                                        </span>
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
                const complexProjects = projects.filter(p => p.type === 'complex')
                return (
                    <div className="space-y-6">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Proyectos Complejos</h2>
                            <p className="text-gray-600 dark:text-gray-400">Gestiona proyectos de gran escala ({complexProjects.length} activos)</p>
                        </div>
                        <div className="grid grid-cols-1 gap-4">
                            {complexProjects.map((project) => (
                                <motion.div key={project.id} whileHover={{ scale: 1.01 }} className="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer">
                                    <div className="flex items-start justify-between mb-4">
                                        <div className="flex items-center gap-3">
                                            <FolderOpen className="w-10 h-10 text-brand-yellow" />
                                            <div>
                                                <h3 className="font-semibold text-lg text-gray-900 dark:text-white">{project.name}</h3>
                                                <p className="text-sm text-gray-600 dark:text-gray-400">{project.description}</p>
                                            </div>
                                        </div>
                                        <span className={`px-3 py-1 rounded text-sm ${project.status === 'active' ? 'bg-blue-100 text-blue-800' : project.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}`}>
                                            {project.status === 'active' ? 'En Progreso' : project.status === 'pending' ? 'Pendiente' : 'Completado'}
                                        </span>
                                    </div>
                                    <div className="grid grid-cols-3 gap-4 mb-4">
                                        <div className="text-center p-3 bg-gray-50 dark:bg-gray-900 rounded">
                                            <p className="text-2xl font-bold text-brand-red">{project.progress}%</p>
                                            <p className="text-xs text-gray-600 dark:text-gray-400">Completado</p>
                                        </div>
                                        <div className="text-center p-3 bg-gray-50 dark:bg-gray-900 rounded">
                                            <p className="text-2xl font-bold text-brand-yellow">${(project.budget / 1000).toFixed(0)}K</p>
                                            <p className="text-xs text-gray-600 dark:text-gray-400">Presupuesto</p>
                                        </div>
                                        <div className="text-center p-3 bg-gray-50 dark:bg-gray-900 rounded">
                                            <p className="text-2xl font-bold text-green-600">{project.daysRemaining}</p>
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
                    <div className="space-y-6 h-full flex flex-col">
                        <div className="flex justify-between items-center mb-4">
                            <div>
                                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                                    {activeSection === 'cotizacion-simple' ? 'Cotizaciones Simples' : 'Cotizaciones Complejas'}
                                </h2>
                                <p className="text-gray-600 dark:text-gray-400">
                                    {viewMode === 'grid'
                                        ? 'Selecciona un servicio para comenzar'
                                        : `Editando cotización de ${selectedService || 'Nueva'}`}
                                </p>
                            </div>
                            {viewMode === 'editor' && (
                                <button
                                    onClick={() => setViewMode('grid')}
                                    className="btn-secondary text-sm"
                                >
                                    ← Volver a Servicios
                                </button>
                            )}
                        </div>
                        <div className="flex-1 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden p-1">
                            {viewMode === 'grid' ? (
                                <CotizacionesView onServiceSelect={handleServiceSelect} />
                            ) : (
                                <CotizacionEditor
                                    cotizacionInicial={{
                                        servicio: selectedService,
                                        cliente: '',
                                        items: []
                                    }}
                                    onGuardar={(data: any) => console.log('Guardando:', data)}
                                />
                            )}
                        </div>
                    </div>
                )

            case 'informe-tecnico':
            case 'informe-ejecutivo':
                const filteredReports = reports.filter(r => activeSection === 'informe-tecnico' ? r.type === 'technical' : r.type === 'executive')
                return (
                    <div className="space-y-6">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                                {activeSection === 'informe-tecnico' ? 'Informes Técnicos' : 'Informes Ejecutivos'}
                            </h2>
                            <p className="text-gray-600 dark:text-gray-400">
                                Genera informes detallados de tus proyectos ({filteredReports.length} informes)
                            </p>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {filteredReports.map((report) => (
                                <motion.div key={report.id} whileHover={{ scale: 1.02 }} className="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer">
                                    <BarChart3 className="w-8 h-8 text-brand-yellow mb-3" />
                                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1">{report.name}</h3>
                                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{report.description}</p>
                                    <p className="text-xs text-gray-500 mb-4">Fecha: {report.date}</p>
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
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Bienvenido a PILi_Quarts</h2>
                        <p className="text-gray-600 dark:text-gray-400 max-w-md">Selecciona una sección para comenzar</p>
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
            <div className="mb-6">
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input type="text" placeholder="Buscar..." className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-red" />
                </div>
            </div>
            {renderContent()}
        </motion.main>
    )
}
