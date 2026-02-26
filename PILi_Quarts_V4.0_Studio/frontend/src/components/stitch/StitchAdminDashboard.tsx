import { motion } from 'framer-motion'
import { Bell, Search, User, FileText, Activity, Shield, Wifi, Zap, Settings, BarChart3, Database, Loader2 } from 'lucide-react'
import { useAdminStats } from '../../hooks/useAdminStats'

export function StitchAdminDashboard() {
    const { data, isLoading, toggleService } = useAdminStats();

    if (isLoading && !data) {
        return (
            <div className="h-full w-full flex items-center justify-center bg-[#050505]">
                <div className="flex flex-col items-center gap-4">
                    <Loader2 className="w-10 h-10 text-blue-500 animate-spin" />
                    <p className="text-gray-400 font-mono text-sm tracking-widest uppercase">Initializing Admin Console...</p>
                </div>
            </div>
        );
    }

    const metrics = [
        { label: 'Usuarios Activos', value: data?.metrics.users.total.toLocaleString() || '0', trend: '+12%', color: 'blue', icon: User },
        { label: 'Docs Generados', value: data?.metrics.projects.total.toLocaleString() || '0', trend: '+5%', color: 'purple', icon: FileText },
        { label: 'Valor Total (S/)', value: data?.metrics.financial.total_value.toLocaleString() || '0', trend: 'STABLE', color: 'yellow', icon: BarChart3 },
        { label: 'Uptime Sistema', value: '99.9%', trend: 'Stable', color: 'green', icon: Activity },
    ];

    return (
        <div className="h-full w-full flex flex-col p-8 overflow-auto custom-scrollbar bg-[#050505] min-w-[800px]">

            {/* Header */}
            <div className="flex justify-between items-end mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white tracking-tight mb-2">Panel de Control</h1>
                    <p className="text-gray-400 text-sm">Monitoreo de sistema y servicios de ingeniería vinculados.</p>
                </div>
                <div className="flex gap-4">
                    <div className="px-4 py-2 bg-[#121921] rounded-xl border border-white/10 flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${data?.success ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' : 'bg-red-500 animate-pulse'}`}></div>
                        <span className="text-xs font-mono text-gray-300 uppercase">{data?.success ? 'Neural Link Active' : 'Offline'}</span>
                    </div>
                </div>
            </div>

            {/* Top Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {metrics.map((stat, idx) => (
                    <motion.div
                        key={idx}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.1 }}
                        className="p-5 rounded-2xl bg-[#0f131a] border border-white/5 hover:border-white/10 transition-colors group shadow-lg"
                    >
                        <div className="flex justify-between items-start mb-4">
                            <div className={`p-2 rounded-lg bg-white/5 text-blue-400 group-hover:bg-blue-500/10 transition-colors`}>
                                <stat.icon size={20} />
                            </div>
                            <span className="text-[10px] bg-white/5 px-2 py-1 rounded text-gray-400">{stat.trend}</span>
                        </div>
                        <div className="text-2xl font-bold text-white mb-1 font-mono tracking-tight">{stat.value}</div>
                        <div className="text-xs text-gray-500 font-medium uppercase tracking-wider">{stat.label}</div>
                    </motion.div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 flex-1">

                {/* Main: Service Matrix (Controls) */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="flex items-center justify-between">
                        <h2 className="text-lg font-bold text-white">Servicios Core de Ingeniería</h2>
                        <button className="text-xs text-blue-400 hover:text-blue-300 font-medium">Gestionar Credenciales</button>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        {data?.settings.services.map((service) => {
                            const Icon = service.id === 'doc_gen' ? FileText
                                : service.id === 'pili_brain' ? Zap
                                    : service.id === 'database' ? Database
                                        : service.id === 'previsualizacion' ? Activity : Activity;

                            return (
                                <div key={service.id} className={`p-6 rounded-3xl bg-[#0f131a] border transition-all cursor-pointer relative overflow-hidden group ${service.estado ? 'border-blue-500/20 hover:border-blue-500/40' : 'border-white/5 opacity-60'
                                    }`}>
                                    <div className={`absolute inset-0 bg-gradient-to-br transition-opacity ${service.estado ? 'from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100' : 'from-transparent to-transparent'
                                        }`} />
                                    <div className="flex justify-between items-start mb-8 relative z-10">
                                        <div className={`p-3 rounded-2xl border ${service.estado ? 'bg-blue-500/10 border-blue-500/20 text-blue-400' : 'bg-white/5 border-white/10 text-gray-500'
                                            }`}>
                                            <Icon size={24} />
                                        </div>
                                        <div
                                            onClick={() => toggleService(service.id, !service.estado)}
                                            className={`w-10 h-6 rounded-full p-1 relative transition-colors duration-300 ${service.estado ? 'bg-blue-500/30' : 'bg-white/10'
                                                }`}
                                        >
                                            <motion.div
                                                animate={{ x: service.estado ? 16 : 0 }}
                                                className={`w-4 h-4 rounded-full shadow-lg ${service.estado ? 'bg-blue-500 shadow-blue-500/40' : 'bg-gray-600'
                                                    }`}
                                            />
                                        </div>
                                    </div>
                                    <h3 className={`text-xl font-bold mb-2 relative z-10 ${service.estado ? 'text-white' : 'text-gray-500'}`}>
                                        {service.nombre}
                                    </h3>
                                    <p className={`text-xs leading-relaxed mb-4 relative z-10 ${service.estado ? 'text-gray-400' : 'text-gray-600'}`}>
                                        {service.descripcion}
                                    </p>
                                    <div className="flex gap-2 relative z-10">
                                        <span className={`px-2 py-1 rounded text-[10px] border ${service.estado ? 'bg-black/40 text-gray-400 border-white/5' : 'bg-transparent text-gray-700 border-white/5'
                                            }`}>V3.0 Backend</span>
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                </div>

                {/* Sidebar: Recent Activity from Backend */}
                <div className="space-y-6">
                    <div className="p-6 rounded-3xl bg-[#0f131a] border border-white/5 shadow-xl">
                        <h3 className="text-base font-bold text-white mb-4">Actividad Reciente</h3>
                        <div className="space-y-4">
                            {data?.recent_projects.length === 0 && <p className="text-[10px] text-gray-600">No hay actividad reciente.</p>}
                            {data?.recent_projects.map((proj) => (
                                <div key={proj.id} className="flex gap-3 items-start pb-3 border-b border-white/5 last:border-0 last:pb-0">
                                    <div className="w-2 h-2 rounded-full bg-blue-500 mt-1.5 shrink-0 shadow-[0_0_5px_#3b82f6]" />
                                    <div>
                                        <p className="text-xs text-gray-300 font-medium">{proj.client_name}</p>
                                        <p className="text-[10px] text-gray-500 mt-0.5">{proj.nombre} • <span className="uppercase">{proj.estado}</span></p>
                                        <p className="text-[9px] text-gray-600 mt-1">{new Date(proj.created_at).toLocaleDateString()}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
