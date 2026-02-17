import { motion } from 'framer-motion'
import { Home, Save, Moon, Sun, User, Shield, Activity } from 'lucide-react'
import { useWorkspaceStore } from '../store/useWorkspaceStore'

export function WorkspaceHeader() {
    const { theme, setTheme, setActiveSection } = useWorkspaceStore()

    const toggleTheme = () => {
        if (theme === 'dark') setTheme('light')
        else setTheme('dark')
    }

    return (
        <motion.header
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="border-b border-white/5 bg-[#030712] z-50 relative"
        >
            {/* Top scanning line effect */}
            <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-[#0052A3] to-transparent opacity-50" />

            <div className="flex items-center justify-between px-8 py-3">
                {/* Logo y Título Studio v4.0 */}
                <div className="flex items-center gap-6">
                    <div className="flex items-center gap-3">
                        <div className="w-9 h-9 border border-[#0052A3]/30 bg-gradient-to-br from-[#0052A3]/20 to-black rounded flex items-center justify-center font-black text-[#0052A3] text-lg shadow-[0_0_20px_rgba(0,82,163,0.1)]">
                            PQ
                        </div>
                        <div className="flex flex-col">
                            <h1 className="text-sm font-black text-white tracking-[0.3em] uppercase">
                                PILi_Quarts
                            </h1>
                            <div className="flex items-center gap-2">
                                <span className="text-[8px] text-[#0052A3] font-bold tracking-[0.2em] uppercase">
                                    Engineering Studio
                                </span>
                                <div className="w-1 h-1 bg-white/20 rounded-full" />
                                <span className="text-[8px] text-gray-600 font-medium uppercase tracking-widest">
                                    V4.0.1 Stable
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Central Status Indicators */}
                <div className="hidden lg:flex items-center gap-8 translate-x-12">
                    <div className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-[#0052A3] animate-pulse" />
                        <span className="text-[9px] text-white/40 font-bold uppercase tracking-[0.2em]">Sync Active</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <Activity className="w-3 h-3 text-[#D4AF37]/50" />
                        <span className="text-[9px] text-white/40 font-bold uppercase tracking-[0.2em]">Pili Core Online</span>
                    </div>
                </div>

                {/* Acciones Studio UI */}
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-1 bg-white/5 p-1 rounded-lg border border-white/5">
                        <motion.button
                            whileHover={{ scale: 1.05, backgroundColor: "rgba(255,255,255,0.05)" }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => setActiveSection('')}
                            className="p-2 text-gray-500 hover:text-white transition-colors"
                            title="Workspace Hub"
                        >
                            <Home className="w-3.5 h-3.5" />
                        </motion.button>

                        <div className="w-px h-4 bg-white/10 mx-1" />

                        <motion.button
                            whileHover={{ scale: 1.05, backgroundColor: "rgba(0, 82, 163, 0.2)" }}
                            whileTap={{ scale: 0.95 }}
                            className="p-2 text-gray-500 hover:text-[#0052A3] transition-colors"
                            title="Save Project (Ctrl+S)"
                        >
                            <Save className="w-3.5 h-3.5" />
                        </motion.button>
                    </div>

                    <motion.button
                        whileHover={{ scale: 1.05, borderColor: "rgba(0, 82, 163, 0.4)" }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setActiveSection('admin-dashboard')}
                        className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/10 text-gray-500 hover:text-white transition-all"
                    >
                        <Shield className="w-3.5 h-3.5" />
                        <span className="text-[10px] font-black uppercase tracking-widest">Admin</span>
                    </motion.button>

                    <div className="flex items-center gap-3 ml-2 border-l border-white/10 pl-4">
                        <motion.button
                            whileTap={{ scale: 0.9 }}
                            onClick={toggleTheme}
                            className="p-2 rounded bg-white/5 border border-white/5 text-gray-500 hover:text-white transition-colors"
                        >
                            {theme === 'dark' ? <Moon className="w-3.5 h-3.5" /> : <Sun className="w-3.5 h-3.5" />}
                        </motion.button>

                        <motion.button
                            whileHover={{ scale: 1.1 }}
                            className="w-8 h-8 rounded border border-[#D4AF37]/30 bg-gradient-to-br from-[#D4AF37]/10 to-black flex items-center justify-center text-[#D4AF37]"
                        >
                            <User className="w-4 h-4" />
                        </motion.button>
                    </div>
                </div>
            </div>
        </motion.header>
    )
}
