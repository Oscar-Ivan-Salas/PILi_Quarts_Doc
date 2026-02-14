import { motion } from 'framer-motion'
import { Home, Save, Moon, Sun, User, Palette, Shield } from 'lucide-react'
import { useWorkspaceStore } from '../store/useWorkspaceStore'

export function WorkspaceHeader() {
    const { theme, setTheme, setActiveSection } = useWorkspaceStore()

    const toggleTheme = () => {
        if (theme === 'dark') setTheme('light')
        else if (theme === 'light') setTheme('magenta')
        else if (theme === 'magenta') setTheme('tesla')
        else setTheme('dark')
    }

    return (
        <motion.header
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="border-b-2 border-brand-red tesla:border-yellow-600 bg-white dark:bg-gray-900 tesla:bg-black/80 transition-colors duration-300"
        >
            <div className="flex items-center justify-between px-6 py-4">
                {/* Logo y Título */}
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                        <div className="w-10 h-10 bg-gradient-to-br from-brand-red to-brand-yellow tesla:from-yellow-600 tesla:to-yellow-400 rounded-lg flex items-center justify-center font-bold text-white text-xl shadow-lg shadow-brand-red/20">
                            P
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-gray-900 dark:text-white 
                                          tesla:bg-clip-text tesla:text-transparent tesla:bg-gradient-to-r tesla:from-yellow-400 tesla:via-yellow-300 tesla:to-yellow-500">
                                PILi_Quarts
                            </h1>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                                Workspace Agentic v3.0
                            </p>
                        </div>
                    </div>
                </div>

                {/* Acciones */}
                <div className="flex items-center gap-3">
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setActiveSection('')}
                        className="btn-secondary flex items-center gap-2"
                        title="Volver al inicio"
                    >
                        <Home className="w-4 h-4" />
                        <span className="hidden md:inline">Inicio</span>
                    </motion.button>

                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="btn-primary flex items-center gap-2 shadow-lg shadow-brand-red/20"
                    >
                        <Save className="w-4 h-4" />
                        <span className="hidden md:inline">Guardar</span>
                    </motion.button>

                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setActiveSection('admin-dashboard')}
                        className="btn-secondary flex items-center gap-2 border-2 border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white transition-colors"
                        title="Panel de Administración"
                    >
                        <Shield className="w-4 h-4" />
                        <span className="hidden md:inline">Admin</span>
                    </motion.button>

                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={toggleTheme}
                        className="p-2 rounded-lg bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors"
                        title={`Tema actual: ${theme}`}
                    >
                        {theme === 'dark' ? (
                            <Moon className="w-5 h-5 text-blue-400" />
                        ) : theme === 'light' ? (
                            <Sun className="w-5 h-5 text-yellow-500" />
                        ) : theme === 'tesla' ? (
                            <Palette className="w-5 h-5 text-amber-500" />
                        ) : (
                            <Palette className="w-5 h-5 text-purple-500" />
                        )}
                    </motion.button>

                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="w-10 h-10 rounded-full bg-gradient-to-br from-brand-red to-brand-yellow flex items-center justify-center text-white"
                    >
                        <User className="w-5 h-5" />
                    </motion.button>
                </div>
            </div>
        </motion.header>
    )
}
