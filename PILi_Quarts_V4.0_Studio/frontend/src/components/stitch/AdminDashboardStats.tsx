import { motion } from 'framer-motion'
import { Users, FileText, Zap, Cpu } from 'lucide-react'

// Datos simulados de Stitch Admin Dashboard
const metrics = [
    { label: 'Total Users', value: '1,240', change: '+5%', icon: Users, color: 'text-blue-400' },
    { label: 'Docs Generated', value: '8,502', change: '+12%', icon: FileText, color: 'text-green-400' },
    { label: 'Tokens Consumed', value: '4.2M', change: '-2%', icon: Zap, color: 'text-orange-400' },
]

export function AdminDashboardStats() {
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
                                <div className="text-lg font-bold text-white font-mono">{metric.value}</div>
                            </div>
                        </div>
                        <span className={`text-xs font-bold ${metric.change.startsWith('+') ? 'text-green-500' : 'text-red-500'}`}>
                            {metric.change}
                        </span>
                    </motion.div>
                ))}
            </div>

            {/* Token Usage Circle Replica */}
            <div className="mt-6 p-6 rounded-2xl bg-gray-900/60 border border-white/5 flex flex-col items-center justify-center relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-b from-blue-500/10 to-transparent opacity-50" />
                <div className="w-32 h-32 rounded-full border-4 border-gray-800 border-t-blue-500 flex items-center justify-center relative">
                    <span className="text-2xl font-bold text-white">75%</span>
                    <span className="absolute bottom-6 text-[10px] text-gray-400 uppercase">Usage</span>
                </div>
                <div className="mt-4 text-xs text-gray-400 text-center">
                    <span className="block text-white font-bold">Token Management</span>
                    System Load Balance
                </div>
            </div>
        </div>
    )
}
