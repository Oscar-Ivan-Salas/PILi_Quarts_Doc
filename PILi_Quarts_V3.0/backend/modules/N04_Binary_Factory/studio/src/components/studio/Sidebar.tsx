import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { LayoutGrid, FileText, ChevronRight, Binary } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';

interface SidebarProps {
    onSelectTemplate: (name: string) => void;
    selectedTemplate: string | null;
}

export const Sidebar: React.FC<SidebarProps> = ({ onSelectTemplate, selectedTemplate }) => {
    const [templates, setTemplates] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchTemplates = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8005/api/studio/templates');
                setTemplates(response.data);
            } catch (error) {
                console.error("Error fetching templates:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchTemplates();
    }, []);

    return (
        <aside className="w-72 border-r border-white/5 bg-black flex flex-col h-full relative z-20">
            <div className="p-8 pb-4">
                <div className="flex items-center gap-3 mb-8">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
                        <Binary className="text-white w-6 h-6" />
                    </div>
                    <div>
                        <h1 className="font-bold text-lg tracking-tight text-white">N04 Studio</h1>
                        <p className="text-[10px] text-zinc-500 font-mono tracking-widest uppercase">Mirror Engine</p>
                    </div>
                </div>

                <div className="space-y-1">
                    <div className="flex items-center gap-2 px-2 py-2 mb-2">
                        <LayoutGrid className="w-4 h-4 text-zinc-500" />
                        <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Plantillas Maestras</span>
                    </div>

                    <div className="space-y-1 py-2 overflow-y-auto custom-scrollbar max-h-[calc(100vh-280px)]">
                        <AnimatePresence mode="popLayout">
                            {loading ? (
                                <div className="p-4 text-zinc-600 text-xs animate-pulse">Detectando nodos...</div>
                            ) : (
                                templates.map((template, idx) => (
                                    <motion.button
                                        initial={{ opacity: 0, x: -10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: idx * 0.05 }}
                                        key={template}
                                        onClick={() => onSelectTemplate(template)}
                                        className={cn(
                                            "w-full flex items-center justify-between px-4 py-3 rounded-xl transition-all duration-300 group relative overflow-hidden",
                                            selectedTemplate === template
                                                ? "bg-blue-600/10 text-blue-400 border border-blue-500/20 shadow-inner shadow-blue-500/5"
                                                : "text-zinc-500 hover:text-zinc-200 hover:bg-white/5 border border-transparent"
                                        )}
                                    >
                                        <div className="flex items-center gap-3 relative z-10">
                                            <FileText className={cn("w-4 h-4 transition-colors", selectedTemplate === template ? "text-blue-400" : "text-zinc-600 group-hover:text-zinc-400")} />
                                            <span className="truncate text-sm font-medium">
                                                {template.replace(/_/g, ' ')}
                                            </span>
                                        </div>
                                        <ChevronRight className={cn(
                                            "w-4 h-4 transition-all duration-300",
                                            selectedTemplate === template ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0"
                                        )} />
                                    </motion.button>
                                ))
                            )}
                        </AnimatePresence>
                    </div>
                </div>
            </div>

            <div className="mt-auto p-6">
                <div className="glass rounded-2xl p-4 border border-white/5 space-y-3">
                    <div className="flex items-center justify-between">
                        <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-tighter">System Status</span>
                        <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]" />
                    </div>
                    <div className="h-1 w-full bg-zinc-900 rounded-full overflow-hidden">
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: "100%" }}
                            className="h-full bg-blue-500"
                        />
                    </div>
                    <p className="text-[9px] text-zinc-600 font-mono leading-tight">
                        CORE: SOBERANO V4.0<br />
                        MIRROR: READY
                    </p>
                </div>
            </div>
        </aside>
    );
};
