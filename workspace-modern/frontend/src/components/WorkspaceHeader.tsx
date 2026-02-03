import { motion } from 'framer-motion'
import { Home, Save, Moon, Sun, User, Palette } from 'lucide-react'
import { useWorkspaceStore } from '../store/useWorkspaceStore'

export function WorkspaceHeader() {
    const { theme, setTheme } = useWorkspaceStore()

    const toggleTheme = () => {
        if (theme === 'dark') setTheme('light')
        else if (theme === 'light') setTheme('magenta')
        else setTheme('dark')
    }

    return (
        <motion.header
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="border-b-2 border-brand-red bg-white dark:bg-gray-900 transition-colors duration-300"
        >
            <div className="flex items-center justify-between px-6 py-4">
                {/* Logo y Título */}
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                        <div className="w-10 h-10 bg-gradient-to-br from-brand-red to-brand-yellow rounded-lg flex items-center justify-center font-bold text-white text-xl shadow-lg shadow-brand-red/20">
                            P
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
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
                        className="btn-secondary flex items-center gap-2"
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
                        onClick={toggleTheme}
                        className="p-2 rounded-lg bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors"
                        title={`Tema actual: ${theme}`}
                    >
                        {theme === 'dark' ? (
                            <Moon className="w-5 h-5 text-blue-400" />
                        ) : theme === 'light' ? (
                            <Sun className="w-5 h-5 text-yellow-500" />
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
