/**
 * Three Panel Layout - IDE-style workspace
 * 
 * Inspired by VS Code, Cursor, Windsurf
 * - Left (30%): Forms/Configuration
 * - Center (40%): Document Preview
 * - Right (30%): PILI Chat
 * 
 * Features:
 * - Collapsible panels
 * - Maximize center panel
 * - Smooth animations
 * - Responsive design
 */
import { useState, useMemo, ReactNode } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Maximize2, Minimize2, ChevronLeft, ChevronRight } from 'lucide-react';

interface ThreePanelLayoutProps {
    leftPanel: ReactNode;
    centerPanel: ReactNode;
    rightPanel: ReactNode;
    leftTitle?: string;
    centerTitle?: string;
    rightTitle?: string;
}

export function ThreePanelLayout({
    leftPanel,
    centerPanel,
    rightPanel,
    leftTitle = '📋 Configuración',
    centerTitle = '📄 Vista Previa',
    rightTitle = '🤖 PILI AI',
}: ThreePanelLayoutProps) {
    const [leftVisible, setLeftVisible] = useState(true);
    const [rightVisible, setRightVisible] = useState(true);
    const [centerMaximized, setCenterMaximized] = useState(false);

    // Calculate dynamic widths
    const panelWidths = useMemo(() => {
        if (centerMaximized) {
            return { left: '0%', center: '100%', right: '0%' };
        }
        if (!leftVisible && !rightVisible) {
            return { left: '0%', center: '100%', right: '0%' };
        }
        if (!leftVisible) {
            return { left: '0%', center: '70%', right: '30%' };
        }
        if (!rightVisible) {
            return { left: '30%', center: '70%', right: '0%' };
        }
        return { left: '30%', center: '40%', right: '30%' };
    }, [leftVisible, rightVisible, centerMaximized]);

    return (
        <div className="flex h-full bg-gray-100 dark:bg-gray-950 overflow-hidden">
            {/* Left Panel - Forms */}
            <AnimatePresence>
                {leftVisible && !centerMaximized && (
                    <motion.div
                        initial={{ x: -300, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        exit={{ x: -300, opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="bg-white dark:bg-gray-900 border-r-2 border-brand-red overflow-y-auto flex-shrink-0"
                        style={{ width: panelWidths.left }}
                    >
                        {/* Header */}
                        <div className="sticky top-0 z-10 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-4 py-3 flex items-center justify-between">
                            <h2 className="text-brand-yellow font-bold text-lg">{leftTitle}</h2>
                            <button
                                onClick={() => setLeftVisible(false)}
                                className="text-gray-400 hover:text-gray-600 dark:hover:text-white transition-colors"
                                title="Ocultar panel"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        {/* Content */}
                        <div className="p-4">{leftPanel}</div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Center Panel - Preview */}
            <motion.div
                animate={{ width: panelWidths.center }}
                transition={{ duration: 0.3 }}
                className="bg-gray-50 dark:bg-gray-800 overflow-y-auto flex-shrink-0"
            >
                {/* Header */}
                <div className="sticky top-0 z-10 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3 flex items-center justify-between">
                    <h2 className="text-gray-900 dark:text-white font-bold text-lg">{centerTitle}</h2>

                    <div className="flex items-center gap-2">
                        {/* Show left panel button */}
                        {!leftVisible && (
                            <motion.button
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                onClick={() => setLeftVisible(true)}
                                className="text-gray-400 hover:text-brand-yellow transition-colors text-sm px-3 py-1 rounded bg-gray-200 dark:bg-gray-700 flex items-center gap-1"
                            >
                                <ChevronLeft className="w-4 h-4" />
                                Formulario
                            </motion.button>
                        )}

                        {/* Maximize button */}
                        <button
                            onClick={() => setCenterMaximized(!centerMaximized)}
                            className="text-gray-400 hover:text-gray-600 dark:hover:text-white transition-colors"
                            title={centerMaximized ? 'Restaurar' : 'Maximizar'}
                        >
                            {centerMaximized ? (
                                <Minimize2 className="w-5 h-5" />
                            ) : (
                                <Maximize2 className="w-5 h-5" />
                            )}
                        </button>

                        {/* Show right panel button */}
                        {!rightVisible && (
                            <motion.button
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                onClick={() => setRightVisible(true)}
                                className="text-gray-400 hover:text-brand-yellow transition-colors text-sm px-3 py-1 rounded bg-gray-200 dark:bg-gray-700 flex items-center gap-1"
                            >
                                Chat PILI
                                <ChevronRight className="w-4 h-4" />
                            </motion.button>
                        )}
                    </div>
                </div>

                {/* Content */}
                <div className="p-6">{centerPanel}</div>
            </motion.div>

            {/* Right Panel - PILI Chat */}
            <AnimatePresence>
                {rightVisible && !centerMaximized && (
                    <motion.div
                        initial={{ x: 300, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        exit={{ x: 300, opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="bg-white dark:bg-gray-900 border-l-2 border-brand-red flex flex-col flex-shrink-0"
                        style={{ width: panelWidths.right }}
                    >
                        {/* Header */}
                        <div className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-4 py-3 flex items-center justify-between flex-shrink-0">
                            <h2 className="text-brand-yellow font-bold text-lg flex items-center gap-2">
                                {rightTitle}
                            </h2>
                            <button
                                onClick={() => setRightVisible(false)}
                                className="text-gray-400 hover:text-gray-600 dark:hover:text-white transition-colors"
                                title="Ocultar panel"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        {/* Content */}
                        <div className="flex-1 overflow-y-auto">{rightPanel}</div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
