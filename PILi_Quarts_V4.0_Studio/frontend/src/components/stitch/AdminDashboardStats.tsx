import { motion } from 'framer-motion'
import { Users, FileText, Zap, Loader2, BarChart3 } from 'lucide-react'
import { useAdminStats } from '../../hooks/useAdminStats'

export function AdminDashboardStats() {
    const { data, isLoading } = useAdminStats();

    if (isLoading && !data) {
        return (
            <div className="w-full p-4 flex flex-col items-center justify-center gap-2">
                <Loader2 size={16} className="text-blue-500 animate-spin" />
                <span className="text-[10px] text-gray-600 uppercase font-mono">Loading Neural Data...</span>
            </div>
        )
    }

    const metrics = [
        { label: 'Total Users', value: data?.metrics.users.total.toLocaleString() || '0', change: '+5%', icon: Users, color: 'text-blue-400' },
        { label: 'Docs Generated', value: data?.metrics.projects.total.toLocaleString() || '0', change: '+12%', icon: FileText, color: 'text-green-400' },
        { label: 'Total Value', value: 'S/' + (data?.metrics.financial.total_value.toLocaleString() || '0'), change: 'LIVE', icon: BarChart3, color: 'text-orange-400' },
    ];

    return (
        <div className="w-full p-4 space-y-4">
            <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-4">Overview Analytics</h3>
            <div className="grid grid-cols-1 gap-3">
                {metrics.map((metric, i) => (
                    <motion.div
                        key={i}
                        whileHover={{ x: 5 }}
                        className="p-4 rounded-xl bg-gray-900/40 border border-white/5 backdrop-blur-sm flex items-center justify-between"
                    >
                        <div className="flex items-center gap-3">
                            <div className={`p-2 rounded-lg bg-white/5 ${metric.color}`}>
                                <metric.icon size={18} />
                            </div>
                            <div>
                                <div className="text-[10px] text-gray-400 uppercase tracking-wider">{metric.label}</div>
                                <div className="text-lg font-bold text-white font-mono leading-tight">{metric.value}</div>
                            </div>
                        </div>
                        <span className={`text-[10px] font-bold ${metric.change.startsWith('+') || metric.change === 'LIVE' ? 'text-green-500' : 'text-red-500'} bg-black/40 px-1.5 py-0.5 rounded border border-white/5`}>
                            {metric.change}
                        </span>
                    </motion.div>
                ))}
            </div>

            {/* Token Usage Circle Replica */}
            <div className="mt-6 p-6 rounded-2xl bg-gray-900/60 border border-white/5 flex flex-col items-center justify-center relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-b from-blue-500/10 to-transparent opacity-50 group-hover:opacity-70 transition-opacity" />
                <div className="w-32 h-32 rounded-full border-4 border-gray-800 border-t-blue-500 flex items-center justify-center relative shadow-[0_0_15px_rgba(59,130,246,0.2)]">
                    <span className="text-2xl font-bold text-white">75%</span>
                    <span className="absolute bottom-6 text-[10px] text-gray-400 uppercase font-mono tracking-tighter">Usage</span>
                </div>
                <div className="mt-4 text-xs text-gray-400 text-center relative z-10">
                    <span className="block text-white font-bold uppercase tracking-wider mb-1">Quota Management</span>
                    System Load Balance
                </div>
            </div>
        </div>
    )
}

