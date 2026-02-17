import { useState, useEffect } from 'react'
import {
    Users, FileText, DollarSign, TrendingUp, Building2,
    BarChart3, Activity, Clock, AlertCircle,
    Zap, Factory, Shield, Cpu, Layout, Bell, Save
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import DatabaseWithRestApi from './ui/database-with-rest-api'

interface ServiceSetting {
    id: string
    nombre: string
    estado: boolean
    descripcion: string
}

interface FeatureSetting {
    id: string
    nombre: string
    estado: boolean
}

interface DashboardMetrics {
    users: {
        total: number
        admins: number
        regular: number
        active: number
    }
    clients: {
        total: number
        active: number
        top_industries: Array<{ industria: string; count: number }>
    }
    projects: {
        total: number
        by_status: Record<string, number>
        by_priority: {
            high: number
            normal: number
            low: number
        }
        recent_7_days: number
    }
    financial: {
        total_value: number
        avg_project_value: number
        currency: string
    }
    document_types: Array<{ id: string; nombre: string; count: number }>
}

interface DashboardData {
    success: boolean
    timestamp: string
    settings: {
        services: ServiceSetting[]
        features: FeatureSetting[]
    }
    metrics: DashboardMetrics
    top_clients: Array<{
        razon_social: string
        total_value: number
        project_count: number
    }>
    recent_projects: Array<{
        id: string
        nombre: string
        client_name: string
        total: number
        estado: string
        created_at: string
    }>
}

export function AdminDashboard() {
    const [dashboard, setDashboard] = useState<DashboardData | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [toggling, setToggling] = useState<string | null>(null)

    useEffect(() => {
        loadDashboard()
        const interval = setInterval(loadDashboard, 30000)
        return () => clearInterval(interval)
    }, [])

    const loadDashboard = async () => {
        try {
            // Use relative path to leverage Vite proxy
            const response = await fetch('/api/admin/dashboard')

            if (!response.ok) {
                throw new Error('Error loading dashboard')
            }

            const data = await response.json()
            setDashboard(data)
            setError(null)
        } catch (err: any) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleToggle = async (type: 'service' | 'feature', id: string, currentState: boolean) => {
        try {
            setToggling(id)
            const response = await fetch(`/api/admin/toggle-${type}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, estado: !currentState })
            })

            if (!response.ok) throw new Error('Failed to update')

            // Reload dashboard to reflect changes
            await loadDashboard()
        } catch (err) {
            console.error(err)
        } finally {
            setToggling(null)
        }
    }

    if (loading && !dashboard) {
        return (
            <div className="h-full flex items-center justify-center bg-black/50 backdrop-blur-sm">
                <div className="text-center">
                    <Activity className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
                    <p className="text-gray-400 font-medium">Sincronizando con el servidor...</p>
                </div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="h-full flex items-center justify-center">
                <div className="bg-red-900/10 border border-red-800/50 rounded-2xl p-8 max-w-md backdrop-blur-md">
                    <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4 animate-pulse" />
                    <h3 className="text-xl font-bold text-white text-center mb-2">Error de Conexión</h3>
                    <p className="text-red-400 text-center mb-6">{error}</p>
                    <button
                        onClick={loadDashboard}
                        className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-xl transition-all active:scale-95 shadow-lg shadow-red-900/40"
                    >
                        Reintentar Conexión
                    </button>
                </div>
            </div>
        )
    }

    if (!dashboard) return null

    const { metrics, settings } = dashboard

    return (
        <div className="h-full overflow-auto p-6 space-y-8 custom-scrollbar bg-black/40 backdrop-blur-3xl">
            {/* Header with System Status */}
            <div className="flex flex-col lg:flex-row justify-between items-start gap-8 border-b border-gray-800 pb-8">
                <div className="flex-1">
                    <div className="flex items-center gap-4 mb-2">
                        <div className="p-3 bg-blue-600 rounded-2xl shadow-lg shadow-blue-900/40">
                            <Shield className="w-8 h-8 text-white" />
                        </div>
                        <div>
                            <h1 className="text-4xl font-black text-white tracking-tight">MISSION CONTROL</h1>
                            <p className="text-blue-400 font-mono text-sm tracking-widest uppercase">PILi_Quarts Professional v3.0</p>
                        </div>
                    </div>

                    <div className="flex flex-wrap items-center gap-3 mt-6">
                        <div className="bg-green-950/30 border border-green-800/50 px-4 py-2 rounded-xl flex items-center gap-3">
                            <div className="w-2.5 h-2.5 bg-green-500 rounded-full animate-ping" />
                            <span className="text-green-400 text-sm font-bold uppercase tracking-wider">Online</span>
                        </div>
                        <div className="bg-gray-900/50 border border-gray-800 px-4 py-2 rounded-xl text-gray-400 text-xs font-mono">
                            LAST SYNC: {new Date(dashboard.timestamp).toLocaleTimeString()}
                        </div>
                        <button
                            onClick={loadDashboard}
                            disabled={loading}
                            className="bg-white/5 hover:bg-white/10 text-white px-4 py-2 rounded-xl transition-all border border-white/10 flex items-center gap-2 group"
                        >
                            <Activity className={`w-4 h-4 text-blue-400 group-hover:rotate-180 transition-transform duration-500 ${loading ? 'animate-spin' : ''}`} />
                            <span className="text-sm font-bold">RECARGAR</span>
                        </button>
                    </div>
                </div>

                {/* Animated Database Visualization */}
                <div className="hidden xl:block bg-gradient-to-br from-gray-900 to-black rounded-3xl p-4 border border-white/5 shadow-2xl">
                    <DatabaseWithRestApi
                        circleText="N08"
                        badgeTexts={{
                            first: "Users",
                            second: "Clients",
                            third: "Projects",
                            fourth: "Fin"
                        }}
                        buttonTexts={{
                            first: "PILi_Core",
                            second: "V3_Prod"
                        }}
                        title="Infraestructura N08 Identity"
                        lightColor="#00A6F5"
                    />
                </div>
            </div>

            {/* SERVICE CONTROLS - RECOVERED FEATURE */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
                <div className="bg-gray-900/40 border border-gray-800/50 rounded-3xl p-6 backdrop-blur-md">
                    <div className="flex items-center gap-3 mb-6">
                        <Cpu className="w-6 h-6 text-purple-500" />
                        <h2 className="text-xl font-black text-white tracking-tight uppercase">Servicios del Core</h2>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {settings.services.map((service) => (
                            <div
                                key={service.id}
                                className={`p-4 rounded-2xl border transition-all duration-300 ${service.estado
                                        ? 'bg-blue-900/10 border-blue-500/30'
                                        : 'bg-gray-950 border-gray-800/50 grayscale opacity-60'
                                    }`}
                            >
                                <div className="flex justify-between items-start mb-2">
                                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${service.estado ? 'bg-blue-500 text-white' : 'bg-gray-800 text-gray-400'
                                        }`}>
                                        {service.estado ? 'ACTIVO' : 'PAUSADO'}
                                    </span>
                                    <button
                                        onClick={() => handleToggle('service', service.id, service.estado)}
                                        disabled={toggling === service.id}
                                        className={`w-10 h-5 rounded-full relative transition-colors ${service.estado ? 'bg-blue-600' : 'bg-gray-700'
                                            }`}
                                    >
                                        <div className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all ${service.estado ? 'right-1' : 'left-1'
                                            }`} />
                                    </button>
                                </div>
                                <h3 className="text-white font-bold text-sm">{service.nombre}</h3>
                                <p className="text-gray-500 text-xs mt-1 leading-relaxed">{service.descripcion}</p>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-gray-900/40 border border-gray-800/50 rounded-3xl p-6 backdrop-blur-md">
                    <div className="flex items-center gap-3 mb-6">
                        <Layout className="w-6 h-6 text-orange-500" />
                        <h2 className="text-xl font-black text-white tracking-tight uppercase">Feature Flags</h2>
                    </div>
                    <div className="space-y-4">
                        {settings.features.map((feature) => (
                            <div key={feature.id} className="flex items-center justify-between p-4 bg-white/5 rounded-2xl border border-white/5">
                                <div className="flex items-center gap-4">
                                    <div className={`p-2 rounded-xl ${feature.id === 'notifications' ? 'bg-yellow-500/20 text-yellow-500' : 'bg-green-500/20 text-green-500'}`}>
                                        {feature.id === 'notifications' ? <Bell className="w-5 h-5" /> : feature.id === 'auto_save' ? <Save className="w-5 h-5" /> : <TrendingUp className="w-5 h-5" />}
                                    </div>
                                    <span className="text-white font-bold">{feature.nombre}</span>
                                </div>
                                <button
                                    onClick={() => handleToggle('feature', feature.id, feature.estado)}
                                    disabled={toggling === feature.id}
                                    className={`w-12 h-6 rounded-full relative transition-colors ${feature.estado ? 'bg-green-600' : 'bg-gray-700'
                                        }`}
                                >
                                    <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${feature.estado ? 'right-1' : 'left-1'
                                        }`} />
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Main Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                    icon={Users}
                    title="Usuarios Totales"
                    value={metrics.users.total}
                    subtitle="Registros en Identity"
                    color="blue"
                    trend={`${metrics.users.active} activos`}
                />
                <MetricCard
                    icon={Building2}
                    title="Cartera Clientes"
                    value={metrics.clients.total}
                    subtitle="Empresas registradas"
                    color="green"
                    trend="Ver Sectores"
                />
                <MetricCard
                    icon={FileText}
                    title="Expedientes"
                    value={metrics.projects.total}
                    subtitle={`+${metrics.projects.recent_7_days} esta semana`}
                    color="purple"
                    trend="Actualizado"
                />
                <MetricCard
                    icon={DollarSign}
                    title="Volumen Negocio"
                    value={`S/ ${(metrics.financial.total_value / 1000).toFixed(1)}K`}
                    subtitle={`Tick. Prom: S/ ${metrics.financial.avg_project_value.toFixed(0)}`}
                    color="orange"
                    trend="Estimado"
                />
            </div>

            {/* Proyectos y Estados */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 space-y-8">
                    {/* Recent Projects Table */}
                    <div className="bg-gray-900/60 border border-gray-800 rounded-3xl overflow-hidden shadow-2xl">
                        <div className="p-6 border-b border-gray-800 flex justify-between items-center">
                            <h2 className="text-xl font-bold text-white flex items-center gap-3">
                                <Clock className="w-6 h-6 text-blue-500" />
                                Monitor de Actividad Reciente
                            </h2>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead>
                                    <tr className="bg-white/5">
                                        <th className="text-left text-gray-400 font-bold py-4 px-6 text-xs uppercase tracking-widest">Código</th>
                                        <th className="text-left text-gray-400 font-bold py-4 px-6 text-xs uppercase tracking-widest">Cliente</th>
                                        <th className="text-right text-gray-400 font-bold py-4 px-6 text-xs uppercase tracking-widest">Monto</th>
                                        <th className="text-center text-gray-400 font-bold py-4 px-6 text-xs uppercase tracking-widest">Status</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-800/50">
                                    {dashboard.recent_projects.length > 0 ? (
                                        dashboard.recent_projects.map((project) => (
                                            <tr key={project.id} className="hover:bg-blue-600/5 transition-colors group">
                                                <td className="py-4 px-6 text-white font-mono font-medium">{project.nombre}</td>
                                                <td className="py-4 px-6 text-gray-400">{project.client_name}</td>
                                                <td className="py-4 px-6 text-right text-green-400 font-bold">S/ {project.total.toLocaleString()}</td>
                                                <td className="py-4 px-6 text-center">
                                                    <StatusBadge status={project.estado} />
                                                </td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr>
                                            <td colSpan={4} className="py-12 text-center text-gray-600 font-mediumitalic">No hay proyectos registrados recientemente</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <div className="space-y-8">
                    {/* Status Distribution */}
                    <div className="bg-gray-900/60 border border-gray-800 rounded-3xl p-6">
                        <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
                            <BarChart3 className="w-6 h-6 text-blue-500" />
                            Pipeline Status
                        </h2>
                        <div className="space-y-5">
                            <ProgressBar label="📋 Borradores" value={metrics.projects.by_status.draft} total={metrics.projects.total} color="gray" />
                            <ProgressBar label="📑 Generados" value={metrics.projects.by_status.generated} total={metrics.projects.total} color="purple" />
                            <ProgressBar label="🔍 Revisión" value={metrics.projects.by_status.pending_review} total={metrics.projects.total} color="yellow" />
                            <ProgressBar label="✅ Aprobados" value={metrics.projects.by_status.approved} total={metrics.projects.total} color="green" />
                        </div>
                    </div>

                    {/* Industrial Sectors */}
                    <div className="bg-gray-900/60 border border-gray-800 rounded-3xl p-6">
                        <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-3">
                            <Factory className="w-6 h-6 text-orange-500" />
                            Sectores Estratégicos
                        </h2>
                        <div className="space-y-4">
                            {metrics.clients.top_industries.map((ind, idx) => (
                                <div key={idx} className="flex items-center justify-between p-3 bg-white/5 rounded-2xl border border-white/5">
                                    <span className="text-gray-300 text-sm font-medium">{ind.industria}</span>
                                    <span className="text-white font-black">{ind.count}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

// Metric Card Component
interface MetricCardProps {
    icon: React.ElementType
    title: string
    value: number | string
    subtitle: string
    color: 'blue' | 'green' | 'purple' | 'orange'
    trend: string
}

function MetricCard({ icon: Icon, title, value, subtitle, color, trend }: MetricCardProps) {
    const colors = {
        blue: 'from-blue-600 to-blue-800 shadow-blue-900/40',
        green: 'from-green-600 to-green-800 shadow-green-900/40',
        purple: 'from-purple-600 to-purple-800 shadow-purple-900/40',
        orange: 'from-orange-600 to-orange-800 shadow-orange-900/40'
    }

    return (
        <motion.div
            whileHover={{ y: -5 }}
            className="bg-gray-900/60 border border-gray-800 rounded-3xl p-6 relative overflow-hidden group shadow-2xl"
        >
            <div className="relative z-10">
                <div className="flex justify-between items-start mb-6">
                    <div className={`bg-gradient-to-br ${colors[color]} p-4 rounded-2xl shadow-xl group-hover:scale-110 transition-transform`}>
                        <Icon className="w-7 h-7 text-white" />
                    </div>
                </div>
                <h3 className="text-gray-400 text-sm font-bold uppercase tracking-wider mb-1">{title}</h3>
                <p className="text-4xl font-black text-white mb-2">{value}</p>
                <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />
                    <p className="text-xs text-blue-400 font-mono italic">{trend}</p>
                </div>
            </div>

            {/* Background Decoration */}
            <div className="absolute -right-4 -bottom-4 opacity-5 group-hover:opacity-10 transition-opacity">
                <Icon size={120} />
            </div>
        </motion.div>
    )
}

// Progress Bar Component
interface ProgressBarProps {
    label: string
    value: number
    total: number
    color: 'gray' | 'yellow' | 'green' | 'blue' | 'purple' | 'red'
}

function ProgressBar({ label, value, total, color }: ProgressBarProps) {
    const percentage = total > 0 ? Math.round((value / total) * 100) : 0

    const colors = {
        gray: 'bg-gray-500',
        yellow: 'bg-yellow-500',
        green: 'bg-green-500',
        blue: 'bg-blue-500',
        purple: 'bg-purple-500',
        red: 'bg-red-500'
    }

    return (
        <div>
            <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-300 font-bold uppercase text-[10px] tracking-widest">{label}</span>
                <span className="text-white font-mono font-bold">{value}</span>
            </div>
            <div className="w-full bg-black/40 rounded-full h-3 border border-white/5 p-0.5">
                <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${percentage}%` }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className={`${colors[color]} h-full rounded-full shadow-inner shadow-black/20`}
                />
            </div>
        </div>
    )
}

// Status Badge Component
function StatusBadge({ status }: { status: string }) {
    const statusConfig: Record<string, { label: string; color: string }> = {
        draft: { label: 'BORRADOR', color: 'bg-gray-900 border-gray-700 text-gray-500' },
        pending_review: { label: 'EN REVISIÓN', color: 'bg-yellow-950/40 border-yellow-800 text-yellow-400' },
        approved: { label: 'APROBADO', color: 'bg-green-950/40 border-green-800 text-green-400' },
        sent: { label: 'ENVIADO', color: 'bg-blue-950/40 border-blue-800 text-blue-400' },
        generated: { label: 'GENERADO', color: 'bg-purple-950/40 border-purple-800 text-purple-400' }
    }

    const config = statusConfig[status.toLowerCase()] || statusConfig.draft

    return (
        <span className={`text-[10px] px-3 py-1 rounded-full border font-black tracking-widest ${config.color}`}>
            {config.label}
        </span>
    )
}
