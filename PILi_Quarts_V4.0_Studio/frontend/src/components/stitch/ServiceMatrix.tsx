import { motion } from 'framer-motion'
import { Zap, Activity, Wifi, Shield, Box, Database } from 'lucide-react'

// Datos simulados extraídos visualmente de Stitch
const services = [
    { id: 'electricity', label: 'Electricity', icon: Zap, status: 'active', color: 'text-blue-400', bg: 'bg-blue-500/20' },
    { id: 'security', label: 'ITSE Security', icon: Shield, status: 'active', color: 'text-green-400', bg: 'bg-green-500/20' },
    { id: 'grounding', label: 'Grounding', icon: Activity, status: 'offline', color: 'text-yellow-400', bg: 'bg-yellow-500/20' },
    { id: 'saneamiento', label: 'Saneamiento', icon: Database, status: 'active', color: 'text-cyan-400', bg: 'bg-cyan-500/20' },
    { id: 'automation', label: 'Automation', icon: Box, status: 'active', color: 'text-purple-400', bg: 'bg-purple-500/20' },
    { id: 'networking', label: 'Networking', icon: Wifi, status: 'offline', color: 'text-gray-400', bg: 'bg-gray-500/20' },
]

export function ServiceMatrix() {
    return (
        <div className="p-4 grid grid-cols-2 gap-3 h-full overflow-y-auto custom-scrollbar">
            {services.map((service) => (
                <motion.div
                    key={service.id}
                    whileHover={{ scale: 1.02 }}
                    className={`relative p-4 rounded-xl border border-white/5 backdrop-blur-md bg-gray-900/60 flex flex-col items-center justify-center gap-2 cursor-pointer group hover:bg-white/5 transition-all`}
                >
                    <div className={`p-3 rounded-full ${service.bg} ${service.color} group-hover:scale-110 transition-transform`}>
                        <service.icon size={24} />
                    </div>
                    <span className="text-xs font-medium text-gray-300 tracking-wide uppercase">{service.label}</span>
                    <div className="absolute top-2 right-2">
                        <div className={`w-2 h-2 rounded-full ${service.status === 'active' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
                    </div>
                    <div className="absolute top-2 left-2">
                        <input type="checkbox" defaultChecked={service.status === 'active'} className="w-3 h-3 accent-blue-500 rounded cursor-pointer opacity-50 group-hover:opacity-100" />
                    </div>
                </motion.div>
            ))}
        </div>
    )
}
