import { motion } from 'framer-motion'
import { Bell, Search, User, FileText, Activity, Shield, Wifi, Zap, Settings, BarChart3, Database } from 'lucide-react'

export function StitchAdminDashboard() {
    return (
        <div className="h-full w-full flex flex-col p-8 overflow-auto custom-scrollbar bg-[#050505] min-w-[800px]">

            {/* Header */}
            <div className="flex justify-between items-end mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white tracking-tight mb-2">Panel de Control</h1>
                    <p className="text-gray-400 text-sm">Monitoreo de sistema y servicios de ingeniería.</p>
                </div>
                <div className="flex gap-4">
                    <div className="px-4 py-2 bg-[#121921] rounded-xl border border-white/10 flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]"></div>
                        <span className="text-xs font-mono text-gray-300">SISTEMA NOMINAL</span>
                    </div>
                </div>
            </div>

            {/* Top Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {[
                    { label: 'Usuarios Activos', value: '1,240', trend: '+12%', color: 'blue', icon: User },
                    { label: 'Docs Generados', value: '8,502', trend: '+5%', color: 'purple', icon: FileText },
                    { label: 'Tokens IA (Mes)', value: '4.2M', trend: '75%', color: 'yellow', icon: Zap },
                    { label: 'Uptime Servicio', value: '99.9%', trend: 'Stable', color: 'green', icon: Activity },
                ].map((stat, idx) => (
                    <motion.div
                        key={idx}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.1 }}
                        className="p-5 rounded-2xl bg-[#0f131a] border border-white/5 hover:border-white/10 transition-colors group"
                    >
                        <div className="flex justify-between items-start mb-4">
                            <div className={`p-2 rounded-lg bg-${stat.color}-500/10 text-${stat.color}-400 group-hover:bg-${stat.color}-500/20 transition-colors`}>
                                <stat.icon size={20} />
                            </div>
                            <span className="text-[10px] bg-white/5 px-2 py-1 rounded text-gray-400">{stat.trend}</span>
                        </div>
                        <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
                        <div className="text-xs text-gray-500 font-medium">{stat.label}</div>
                    </motion.div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 flex-1">

                {/* Main: Service Matrix (Controls) */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="flex items-center justify-between">
                        <h2 className="text-lg font-bold text-white">Matriz de Servicios</h2>
                        <button className="text-xs text-blue-400 hover:text-blue-300">Configurar Integraciones</button>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        {/* Service Card: Electricity */}
                        <div className="p-6 rounded-3xl bg-[#0f131a] border border-blue-500/20 relative overflow-hidden group hover:border-blue-500/40 transition-all cursor-pointer">
                            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                            <div className="flex justify-between items-start mb-8">
                                <div className="p-3 bg-blue-500/10 rounded-2xl border border-blue-500/20 text-blue-400">
                                    <Zap size={24} />
                                </div>
                                <div className="w-10 h-6 bg-blue-500/20 rounded-full p-1 relative">
                                    <div className="w-4 h-4 bg-blue-500 rounded-full shadow-lg absolute right-1" />
                                </div>
                            </div>
                            <h3 className="text-xl font-bold text-white mb-2">Electricidad</h3>
                            <p className="text-xs text-gray-400 leading-relaxed mb-4">
                                Cálculos de carga, dimensionamiento de conductores y normativa CNE.
                            </p>
                            <div className="flex gap-2">
                                <span className="px-2 py-1 bg-black/40 rounded text-[10px] text-gray-400 border border-white/5">CNE 2024</span>
                                <span className="px-2 py-1 bg-black/40 rounded text-[10px] text-gray-400 border border-white/5">NTP</span>
                            </div>
                        </div>

                        {/* Service Card: ITSE */}
                        <div className="p-6 rounded-3xl bg-[#0f131a] border border-red-500/20 relative overflow-hidden group hover:border-red-500/40 transition-all cursor-pointer">
                            <div className="absolute inset-0 bg-gradient-to-br from-red-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                            <div className="flex justify-between items-start mb-8">
                                <div className="p-3 bg-red-500/10 rounded-2xl border border-red-500/20 text-red-400">
                                    <Shield size={24} />
                                </div>
                                <div className="w-10 h-6 bg-red-500/20 rounded-full p-1 relative">
                                    <div className="w-4 h-4 bg-red-500 rounded-full shadow-lg absolute right-1" />
                                </div>
                            </div>
                            <h3 className="text-xl font-bold text-white mb-2">ITSE & Seguridad</h3>
                            <p className="text-xs text-gray-400 leading-relaxed mb-4">
                                Protocolos de defensa civil, planes de contingencia y mapas de riesgo.
                            </p>
                            <div className="flex gap-2">
                                <span className="px-2 py-1 bg-black/40 rounded text-[10px] text-gray-400 border border-white/5">INDECI</span>
                                <span className="px-2 py-1 bg-black/40 rounded text-[10px] text-gray-400 border border-white/5">NFPA</span>
                            </div>
                        </div>

                        {/* Service Card: Teleco - OFFLINE */}
                        <div className="p-6 rounded-3xl bg-[#0a0c10] border border-white/5 relative overflow-hidden group opacity-60">
                            <div className="flex justify-between items-start mb-8">
                                <div className="p-3 bg-white/5 rounded-2xl border border-white/10 text-gray-500">
                                    <Wifi size={24} />
                                </div>
                                <div className="w-10 h-6 bg-white/5 rounded-full p-1 relative">
                                    <div className="w-4 h-4 bg-gray-600 rounded-full absolute left-1" />
                                </div>
                            </div>
                            <h3 className="text-xl font-bold text-gray-500 mb-2">Telecomunicaciones</h3>
                            <p className="text-xs text-gray-600 leading-relaxed">
                                Módulo de cableado estructurado y fibra óptica no activo.
                            </p>
                        </div>
                        {/* Service Card: Data - OFFLINE */}
                        <div className="p-6 rounded-3xl bg-[#0a0c10] border border-white/5 relative overflow-hidden group opacity-60">
                            <div className="flex justify-between items-start mb-8">
                                <div className="p-3 bg-white/5 rounded-2xl border border-white/10 text-gray-500">
                                    <Database size={24} />
                                </div>
                                <div className="w-10 h-6 bg-white/5 rounded-full p-1 relative">
                                    <div className="w-4 h-4 bg-gray-600 rounded-full absolute left-1" />
                                </div>
                            </div>
                            <h3 className="text-xl font-bold text-gray-500 mb-2">Base de Datos</h3>
                            <p className="text-xs text-gray-600 leading-relaxed">
                                Conexión directa a bases de datos de ingeniería y precios unitarios.
                            </p>
                        </div>
                    </div>
                </div>

                {/* Sidebar: System Logs & Quick Actions */}
                <div className="space-y-6">
                    <div className="p-6 rounded-3xl bg-[#0f131a] border border-white/5">
                        <h3 className="text-base font-bold text-white mb-4">Registro del Sistema</h3>
                        <div className="space-y-4">
                            {[1, 2, 3].map((_, i) => (
                                <div key={i} className="flex gap-3 items-start pb-3 border-b border-white/5 last:border-0 last:pb-0">
                                    <div className="w-2 h-2 rounded-full bg-blue-500 mt-1.5 shrink-0" />
                                    <div>
                                        <p className="text-xs text-gray-300">Generación de Exp. Técnico completada</p>
                                        <p className="text-[10px] text-gray-500 mt-1">Hace 2 min • Usuario Admin</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="p-6 rounded-3xl bg-gradient-to-br from-purple-900/20 to-blue-900/10 border border-white/5 relative overflow-hidden">
                        <h3 className="text-base font-bold text-white mb-2 relative z-10">Optimización AI</h3>
                        <p className="text-xs text-gray-400 mb-4 relative z-10">Tu índice de eficiencia ha subido un 15% esta semana.</p>
                        <button className="w-full py-2 bg-white/10 hover:bg-white/20 rounded-xl text-xs font-semibold text-white border border-white/10 transition-colors relative z-10">
                            Ver Reporte Detallado
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
