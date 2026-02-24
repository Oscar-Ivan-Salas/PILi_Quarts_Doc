import { motion } from 'framer-motion'
import { Zap, Activity, Wifi, Shield, Box, Database, Sun, Settings } from 'lucide-react'

const services = [
    { title: 'Instalaciones Eléctricas', desc: 'Planos y memorias BT/MT', icon: Zap, color: 'text-blue-400', bg: 'from-blue-600/20 to-blue-900/20', border: 'border-blue-500/30' },
    { title: 'Puesta a Tierra', desc: 'Diseño de mallas IEEE', icon: Activity, color: 'text-yellow-400', bg: 'from-yellow-600/20 to-yellow-900/20', border: 'border-yellow-500/30' },
    { title: 'Energia Solar', desc: 'Dimensionamiento PV', icon: Sun, color: 'text-orange-400', bg: 'from-orange-600/20 to-orange-900/20', border: 'border-orange-500/30' },
    { title: 'Mecánica', desc: 'Sistemas HVAC y bombeo', icon: Settings, color: 'text-gray-400', bg: 'from-gray-600/20 to-gray-900/20', border: 'border-white/10' },
    { title: 'ITSE Security', desc: 'Auditorías de seguridad', icon: Shield, color: 'text-green-400', bg: 'from-green-600/20 to-green-900/20', border: 'border-green-500/30' },
    { title: 'Saneamiento', desc: 'Redes de agua y desagüe', icon: Database, color: 'text-cyan-400', bg: 'from-cyan-600/20 to-cyan-900/20', border: 'border-cyan-500/30' },
]

export function StitchServiceMatrixMain() {
    return (
        <div className="w-full h-full p-12 overflow-y-auto custom-scrollbar flex justify-center">
            <div className="max-w-5xl w-full">
                <motion.div
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    className="mb-12 text-center"
                >
                    <h1 className="text-4xl font-bold text-white mb-2 tracking-tight">Seleccione un Servicio de Ingeniería</h1>
                    <p className="text-gray-400 max-w-xl mx-auto">Automatización de documentos técnicos asistida por inteligencia artificial. Seleccione un módulo para activar el agente especializado.</p>
                </motion.div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {services.map((service, i) => (
                        <motion.button
                            key={i}
                            whileHover={{ scale: 1.02, y: -5 }}
                            whileTap={{ scale: 0.98 }}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.1 }}
                            className={`relative group p-6 h-64 rounded-3xl border backdrop-blur-xl bg-gradient-to-br ${service.bg} ${service.border} flex flex-col justify-between overflow-hidden text-left`}
                        >
                            <div className={`p-4 rounded-2xl bg-black/20 w-fit ${service.color}`}>
                                <service.icon size={32} />
                            </div>

                            <div className="relative z-10">
                                <h3 className="text-xl font-bold text-white mb-1 group-hover:text-blue-300 transition-colors">{service.title}</h3>
                                <p className="text-xs text-white/50">{service.desc}</p>
                            </div>

                            {/* Background Pattern */}
                            <div className="absolute top-0 right-0 p-8 opacity-10 transform translate-x-10 -translate-y-10 group-hover:scale-150 transition-transform duration-700">
                                <service.icon size={120} />
                            </div>
                        </motion.button>
                    ))}
                </div>

                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.8 }}
                    className="mt-12 flex justify-center"
                >
                    <div className="px-6 py-2 rounded-full bg-white/5 border border-white/10 flex items-center gap-3">
                        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                        <span className="text-xs text-gray-400 font-mono">CREDITOS IA: <span className="text-white font-bold">1,250</span> QUARTS</span>
                    </div>
                </motion.div>
            </div>
        </div>
    )
}
