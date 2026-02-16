import { useState, useEffect } from 'react'
import {
    Users, FileText, DollarSign, TrendingUp, Building2,
    BarChart3, Activity, Clock, AlertCircle,
    Zap, Factory
} from 'lucide-react'
import { motion } from 'framer-motion'
import DatabaseWithRestApi from './ui/database-with-rest-api'

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
    price_references: {
        total: number
        active: number
        categories: Array<{ categoria: string; count: number }>
    }
}

interface DashboardData {
    success: boolean
    timestamp: string
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

    useEffect(() => {
        loadDashboard()
        const interval = setInterval(loadDashboard, 30000)
        return () => clearInterval(interval)
    }, [])

    const loadDashboard = async () => {
        try {
            setLoading(true)
            const response = await fetch('http://localhost:8005/api/admin/dashboard')

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

    if (loading && !dashboard) {
        return (
            <div className="h-full flex items-center justify-center">
                <div className="text-center">
                    <Activity className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
                    <p className="text-gray-400">Cargando dashboard...</p>
                </div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="h-full flex items-center justify-center">
                <div className="bg-red-900/20 border border-red-800 rounded-xl p-6 max-w-md">
                    <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
                    <p className="text-red-400 text-center">{error}</p>
                    <button
                        onClick={loadDashboard}
                        className="mt-4 w-full bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
                    >
                        Reintentar
                    </button>
                </div>
            </div>
        )
    }

    if (!dashboard) return null

    const { metrics } = dashboard

    return (
        <div className="h-full overflow-auto p-6 space-y-6 custom-scrollbar">
            {/* Header with Database Animation */}
            <div className="flex justify-between items-start gap-6">
                <div className="flex-1">
                    <h1 className="text-3xl font-bold text-white mb-2">Dashboard Administrativo</h1>
                    <p className="text-gray-400">PILi_Quarts - Métricas en Tiempo Real</p>

                    <div className="flex items-center gap-3 mt-4">
                        <div className="bg-green-900/30 border border-green-800 px-4 py-2 rounded-lg">
                            <div className="flex items-center gap-2">
                                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                                <span className="text-green-400 text-sm font-medium">Sistema Operacional</span>
                            </div>
                        </div>
                        <button
                            onClick={loadDashboard}
                            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
                        >
                            <Activity className="w-4 h-4" />
                            Actualizar
                        </button>
                    </div>
                </div>

                {/* Animated Database Visualization */}
                <div className="flex-shrink-0">
                    <DatabaseWithRestApi
                        circleText="SQL"
                        badgeTexts={{
                            first: "Users",
                            second: "Clients",
                            third: "Projects",
                            fourth: "Reports"
                        }}
                        buttonTexts={{
                            first: "PILi_Quarts",
                            second: "Production"
                        }}
                        title="Base de Datos en Tiempo Real - REST API"
                        lightColor="#00A6F5"
                    />
                </div>
            </div>

            {/* Main Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                    icon={Users}
                    title="Usuarios"
                    value={metrics.users.total}
                    subtitle={`${metrics.users.admins} admins | ${metrics.users.regular} usuarios`}
                    color="blue"
                    trend="+12%"
                />
                <MetricCard
                    icon={Building2}
                    title="Clientes"
                    value={metrics.clients.total}
                    subtitle={`${metrics.clients.active} activos`}
                    color="green"
                    trend="+8%"
                />
                <MetricCard
                    icon={FileText}
                    title="Proyectos"
                    value={metrics.projects.total}
                    subtitle={`${metrics.projects.recent_7_days} últimos 7 días`}
                    color="purple"
                    trend="+15%"
                />
                <MetricCard
                    icon={DollarSign}
                    title="Valor Total"
                    value={`S/ ${(metrics.financial.total_value / 1000000).toFixed(2)}M`}
                    subtitle={`Promedio: S/ ${(metrics.financial.avg_project_value / 1000).toFixed(1)}K`}
                    color="orange"
                    trend="+28%"
                />
            </div>

            {/* Project Status Distribution */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-gray-900/60 border border-gray-800 rounded-xl p-6">
                    <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        <BarChart3 className="w-6 h-6 text-blue-500" />
                        Estado de Proyectos
                    </h2>
                    <div className="space-y-3">
                        <ProgressBar
                            label="📝 Borrador"
                            value={metrics.projects.by_status.draft || 0}
                            total={metrics.projects.total}
                            color="gray"
                        />
                        <ProgressBar
                            label="⏳ En Revisión"
                            value={metrics.projects.by_status.pending_review || 0}
                            total={metrics.projects.total}
                            color="yellow"
                        />
                        <ProgressBar
                            label="✅ Aprobados"
                            value={metrics.projects.by_status.approved || 0}
                            total={metrics.projects.total}
                            color="green"
                        />
                        <ProgressBar
                            label="📤 Enviados"
                            value={metrics.projects.by_status.sent || 0}
                            total={metrics.projects.total}
                            color="blue"
                        />
                    </div>
                </div>

                <div className="bg-gray-900/60 border border-gray-800 rounded-xl p-6">
                    <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        <Zap className="w-6 h-6 text-orange-500" />
                        Prioridad de Proyectos
                    </h2>
                    <div className="space-y-3">
                        <ProgressBar
                            label="🔴 Alta"
                            value={metrics.projects.by_priority.high}
                            total={metrics.projects.total}
                            color="red"
                        />
                        <ProgressBar
                            label="🟡 Normal"
                            value={metrics.projects.by_priority.normal}
                            total={metrics.projects.total}
                            color="yellow"
                        />
                        <ProgressBar
                            label="🟢 Baja"
                            value={metrics.projects.by_priority.low}
                            total={metrics.projects.total}
                            color="green"
                        />
                    </div>
                </div>
            </div>

            {/* Top Clients */}
            <div className="bg-gray-900/60 border border-gray-800 rounded-xl p-6">
                <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                    <TrendingUp className="w-6 h-6 text-green-500" />
                    Top 10 Clientes por Valor
                </h2>
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="border-b border-gray-800">
                                <th className="text-left text-gray-400 font-medium py-3 px-4">#</th>
                                <th className="text-left text-gray-400 font-medium py-3 px-4">Cliente</th>
                                <th className="text-right text-gray-400 font-medium py-3 px-4">Proyectos</th>
                                <th className="text-right text-gray-400 font-medium py-3 px-4">Valor Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {dashboard.top_clients.map((client, index) => (
                                <tr key={index} className="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors">
                                    <td className="py-3 px-4 text-gray-500">{index + 1}</td>
                                    <td className="py-3 px-4 text-white font-medium">{client.razon_social}</td>
                                    <td className="py-3 px-4 text-right text-gray-300">{client.project_count}</td>
                                    <td className="py-3 px-4 text-right text-green-400 font-bold">
                                        S/ {client.total_value.toLocaleString('es-PE', { minimumFractionDigits: 2 })}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Recent Projects */}
            <div className="bg-gray-900/60 border border-gray-800 rounded-xl p-6">
                <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                    <Clock className="w-6 h-6 text-blue-500" />
                    Proyectos Recientes
                </h2>
                <div className="space-y-2">
                    {dashboard.recent_projects.map((project) => (
                        <div
                            key={project.id}
                            className="bg-gray-800/50 border border-gray-700 rounded-lg p-4 hover:bg-gray-800 transition-colors"
                        >
                            <div className="flex justify-between items-start">
                                <div className="flex-1">
                                    <h3 className="text-white font-medium">{project.nombre}</h3>
                                    <p className="text-gray-400 text-sm mt-1">{project.client_name}</p>
                                </div>
                                <div className="text-right">
                                    <p className="text-green-400 font-bold">S/ {project.total.toLocaleString('es-PE')}</p>
                                    <StatusBadge status={project.estado} />
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Industries */}
            <div className="bg-gray-900/60 border border-gray-800 rounded-xl p-6">
                <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                    <Factory className="w-6 h-6 text-purple-500" />
                    Top Industrias
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                    {metrics.clients.top_industries.map((industry, index) => (
                        <div key={index} className="bg-gray-800/50 border border-gray-700 rounded-lg p-4 text-center">
                            <p className="text-2xl font-bold text-white">{industry.count}</p>
                            <p className="text-gray-400 text-sm mt-1 capitalize">{industry.industria}</p>
                        </div>
                    ))}
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
        blue: 'from-blue-500 to-blue-600',
        green: 'from-green-500 to-green-600',
        purple: 'from-purple-500 to-purple-600',
        orange: 'from-orange-500 to-orange-600'
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gray-900/60 border border-gray-800 rounded-xl p-6"
        >
            <div className="flex justify-between items-start mb-4">
                <div className={`bg-gradient-to-br ${colors[color]} p-3 rounded-lg`}>
                    <Icon className="w-6 h-6 text-white" />
                </div>
                <span className="text-green-400 text-sm font-semibold">{trend}</span>
            </div>
            <h3 className="text-gray-400 text-sm font-medium">{title}</h3>
            <p className="text-3xl font-bold text-white mt-1">{value}</p>
            <p className="text-xs text-gray-500 mt-2">{subtitle}</p>
        </motion.div>
    )
}

// Progress Bar Component
interface ProgressBarProps {
    label: string
    value: number
    total: number
    color: 'gray' | 'yellow' | 'green' | 'blue' | 'red'
}

function ProgressBar({ label, value, total, color }: ProgressBarProps) {
    const percentage = Math.round((value / total) * 100)

    const colors = {
        gray: 'bg-gray-500',
        yellow: 'bg-yellow-500',
        green: 'bg-green-500',
        blue: 'bg-blue-500',
        red: 'bg-red-500'
    }

    return (
        <div>
            <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-300 font-medium">{label}</span>
                <span className="text-gray-400">{value} ({percentage}%)</span>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-2">
                <div
                    className={`${colors[color]} h-2 rounded-full transition-all duration-500`}
                    style={{ width: `${percentage}%` }}
                />
            </div>
        </div>
    )
}

// Status Badge Component
function StatusBadge({ status }: { status: string }) {
    const statusConfig: Record<string, { label: string; color: string }> = {
        draft: { label: 'Borrador', color: 'bg-gray-700 text-gray-300' },
        pending_review: { label: 'En Revisión', color: 'bg-yellow-900/50 text-yellow-400 border-yellow-800' },
        approved: { label: 'Aprobado', color: 'bg-green-900/50 text-green-400 border-green-800' },
        sent: { label: 'Enviado', color: 'bg-blue-900/50 text-blue-400 border-blue-800' },
        generated: { label: 'Generado', color: 'bg-purple-900/50 text-purple-400 border-purple-800' }
    }

    const config = statusConfig[status] || statusConfig.draft

    return (
        <span className={`text-xs px-2 py-1 rounded-full border ${config.color} mt-1 inline-block`}>
            {config.label}
        </span>
    )
}
