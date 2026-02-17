import { motion } from 'framer-motion'
import { Home, Save, Moon, Sun, User, Shield, Activity, Wifi, Globe, Command } from 'lucide-react'
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
            className="h-16 border-b border-white/5 bg-[#030712] z-50 relative flex items-center overflow-hidden"
        >
            {/* Cinematic Background Elements */}
            <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-[#0052A3]/50 to-transparent" />
            <div className="absolute inset-0 scanlines opacity-[0.02] pointer-events-none" />

            <div className="w-full flex items-center justify-between px-10">
                {/* Left: Branding & Core Node */}
                <div className="flex items-center gap-8">
                    <div className="flex items-center gap-4 group cursor-pointer">
                        <motion.div
                            whileHover={{ scale: 1.05, rotate: 90 }}
                            className="w-10 h-10 border border-[#0052A3]/40 bg-black flex items-center justify-center rounded-sm shadow-[0_0_15px_rgba(0,82,163,0.2)]"
                        >
                            <span className="text-xl font-black text-white tracking-widest leading-none">P</span>
                        </motion.div>
                        <div className="flex flex-col">
                            <h1 className="text-xs font-black text-white tracking-[0.4em] uppercase leading-none mb-1.5">
                                PILi_Quarts
                            </h1>
                            <div className="flex items-center gap-2">
                                <div className="px-1.5 py-0.5 rounded-[2px] bg-[#0052A3]/20 border border-[#0052A3]/40">
                                    <span className="text-[7px] text-[#0052A3] font-black uppercase tracking-[0.2em]">ENG STUDIO</span>
                                </div>
                                <span className="text-[7px] text-gray-600 font-bold uppercase tracking-widest">Build 4.0.12.0</span>
                            </div>
                        </div>
                    </div>

                    {/* Network Status Nodes */}
                    <div className="hidden xl:flex items-center gap-6 border-l border-white/5 pl-8 h-8">
                        <div className="flex flex-col gap-1">
                            <div className="flex items-center gap-2">
                                <Wifi className="w-2.5 h-2.5 text-green-500/50" />
                                <span className="text-[8px] text-white/30 font-black uppercase tracking-widest leading-none">Link Stable</span>
                            </div>
                            <div className="w-16 h-1 bg-white/5 rounded-full overflow-hidden">
                                <motion.div
                                    animate={{ x: [-64, 64] }}
                                    transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                                    className="w-full h-full bg-[#0052A3]/40"
                                />
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <Globe className="w-3 h-3 text-white/10" />
                            <div className="flex flex-col">
                                <span className="text-[7px] text-gray-700 font-black uppercase">Region</span>
                                <span className="text-[8px] text-white/40 font-bold uppercase tracking-widest uppercase">Latin_South_1</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Center: Live Telemetry (Conceptual) */}
                <div className="hidden lg:flex items-center gap-4 bg-black/40 border border-white/5 px-6 py-2 rounded-full backdrop-blur-md">
                    <Activity className="w-3 h-3 text-[#D4AF37] animate-pulse" />
                    <div className="flex items-center gap-3">
                        <span className="text-[9px] text-white/60 font-black tracking-[0.2em] uppercase">Neural Sync</span>
                        <div className="flex gap-0.5">
                            {[1, 1, 1, 1, 0].map((v, i) => (
                                <div key={i} className={`w-1 h-3 rounded-[1px] ${v ? 'bg-[#0052A3]' : 'bg-white/5'}`} />
                            ))}
                        </div>
                    </div>
                </div>

                {/* Right: User Environment Controls */}
                <div className="flex items-center gap-6">
                    {/* Command Console Toggle */}
                    <motion.button
                        whileHover={{ scale: 1.05, backgroundColor: 'rgba(255,255,255,0.03)' }}
                        className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/5 text-gray-500 hover:text-white transition-all"
                    >
                        <Command className="w-3.5 h-3.5" />
                        <span className="text-[9px] font-black uppercase tracking-widest">Console</span>
                    </motion.button>

                    {/* Quick Launch */}
                    <div className="flex items-center gap-1 bg-white/5 p-1 rounded-lg border border-white/5">
                        <motion.button
                            onClick={() => setActiveSection('')}
                            className="p-2 text-gray-500 hover:text-white transition-colors"
                        >
                            <Home className="w-3.5 h-3.5" />
                        </motion.button>
                        <div className="w-px h-3 bg-white/10 mx-1" />
                        <motion.button className="p-2 text-gray-500 hover:text-[#0052A3] transition-colors">
                            <Save className="w-3.5 h-3.5" />
                        </motion.button>
                    </div>

                    {/* Admin Access Shield */}
                    <motion.button
                        onClick={() => setActiveSection('admin-dashboard')}
                        className="flex items-center gap-3 px-4 py-2 bg-white/5 border border-white/10 rounded-xl hover:border-[#0052A3]/50 transition-all group"
                    >
                        <Shield className="w-3.5 h-3.5 text-[#0052A3] group-hover:animate-pulse" />
                        <span className="text-[10px] font-black uppercase tracking-widest text-gray-500 group-hover:text-white">Admin Privileges</span>
                    </motion.button>

                    {/* User Identity Node */}
                    <div className="flex items-center gap-4 pl-6 border-l border-white/5">
                        <motion.button
                            whileTap={{ scale: 0.9 }}
                            onClick={toggleTheme}
                            className="p-2 text-gray-500 hover:text-white transition-colors"
                        >
                            {theme === 'dark' ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
                        </motion.button>

                        <div className="relative">
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                className="w-9 h-9 border border-[#D4AF37]/30 bg-black flex items-center justify-center rounded-sm text-[#D4AF37]"
                            >
                                <User className="w-4 h-4" />
                            </motion.button>
                            <div className="absolute -bottom-0.5 -right-0.5 w-2 h-2 bg-green-500 rounded-full border-2 border-black" />
                        </div>
                    </div>
                </div>
            </div>
        </motion.header>
    )
}
