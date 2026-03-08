import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { LayoutGrid, FileText, ChevronRight, Binary, Download, FileType, FileSpreadsheet } from 'lucide-react';
import { UIActionCard } from './UIActionCard';
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';

interface SidebarProps {
    onSelectTemplate: (name: string) => void;
    selectedTemplate: string | null;
    isGenerating: string | null;
    onDownload: (format: 'word' | 'excel' | 'pdf') => void;
}

const getTemplateStyle = (name: string) => {
    const n = name.toUpperCase();
    if (n.includes('COTIZACION')) return { color: 'blue', label: 'Cotización' };
    if (n.includes('INFORME')) return { color: 'red', label: 'Informe' };
    if (n.includes('PROYECTO')) return { color: 'green', label: 'Proyecto' };
    return { color: 'blue', label: 'Documento' };
};

export const Sidebar: React.FC<SidebarProps> = ({
    onSelectTemplate,
    selectedTemplate,
    isGenerating,
    onDownload
}) => {
    const [templates, setTemplates] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchTemplates = async () => {
            try {
                const response = await axios.get('http://localhost:8005/api/studio/templates');
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
        <aside className="w-80 border-r border-white/5 bg-zinc-950 flex flex-col h-full relative z-20">
            <div className="p-6 flex flex-col h-full overflow-hidden">
                {/* Header Section */}
                <div className="flex items-center gap-3 mb-8 px-2 mt-4 flex-shrink-0">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center shadow-lg shadow-blue-500/30">
                        <Binary className="text-white w-6 h-6 animate-pulse" />
                    </div>
                    <div>
                        <h1 className="font-black text-sm tracking-[0.2em] text-white uppercase italic">N04 Studio</h1>
                        <p className="text-[10px] text-zinc-600 font-mono tracking-widest uppercase">Mirror Engine v4.2S</p>
                    </div>
                </div>

                {/* Templates Section */}
                <div className="flex flex-col flex-1 min-h-0">
                    <div className="flex items-center gap-2 px-2 mb-4 flex-shrink-0">
                        <LayoutGrid className="w-3.5 h-3.5 text-zinc-600" />
                        <span className="text-[10px] font-black text-zinc-500 uppercase tracking-[0.15em]">Plantillas Maestras</span>
                    </div>

                    <div className="flex-1 overflow-y-auto px-2 custom-scrollbar pr-2 mb-8">
                        <AnimatePresence>
                            {loading ? (
                                <motion.div
                                    key="skeleton"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    exit={{ opacity: 0 }}
                                    className="flex flex-col gap-3 pt-1"
                                >
                                    {[1, 2, 3].map(i => (
                                        <div key={i} className="h-20 w-full bg-white/5 rounded-2xl animate-pulse" />
                                    ))}
                                </motion.div>
                            ) : (
                                <motion.div
                                    key="list"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    exit={{ opacity: 0 }}
                                    className="flex flex-col gap-3 pt-1"
                                >
                                    {templates.map((template, idx) => {
                                        const { color, label } = getTemplateStyle(template);
                                        const isActive = selectedTemplate === template;

                                        return (
                                            <motion.button
                                                initial={{ opacity: 0, x: -20 }}
                                                animate={{ opacity: 1, x: 0 }}
                                                transition={{ delay: idx * 0.05 }}
                                                key={template}
                                                onClick={() => onSelectTemplate(template)}
                                                className={cn(
                                                    "w-full group relative flex items-center gap-4 px-4 py-4 rounded-2xl border transition-all duration-500 overflow-hidden shrink-0",
                                                    isActive
                                                        ? "bg-zinc-900 border-blue-500/40 shadow-[0_0_20px_rgba(59,130,246,0.1)]"
                                                        : "bg-[#080808] border-white/5 hover:border-white/10"
                                                )}
                                            >
                                                <div className={cn(
                                                    "absolute left-0 top-0 bottom-0 w-1 transition-all duration-500",
                                                    isActive
                                                        ? (color === 'blue' ? 'bg-blue-500' : color === 'red' ? 'bg-rose-500' : 'bg-emerald-500')
                                                        : "bg-transparent group-hover:bg-zinc-800"
                                                )} />

                                                <div className={cn(
                                                    "p-3 rounded-xl bg-black/40 border border-white/5 shadow-inner transition-transform group-hover:scale-110 shrink-0",
                                                    isActive && (color === 'blue' ? 'text-blue-400' : color === 'red' ? 'text-rose-400' : 'text-emerald-400')
                                                )}>
                                                    <FileText size={18} />
                                                </div>

                                                <div className="flex flex-col items-start min-w-0 flex-1 text-left">
                                                    <span className={cn(
                                                        "text-[9px] font-black uppercase tracking-widest mb-0.5",
                                                        isActive ? "text-zinc-300" : "text-zinc-600"
                                                    )}>
                                                        {label}
                                                    </span>
                                                    <span className={cn(
                                                        "text-xs font-bold truncate w-full",
                                                        isActive ? "text-white" : "text-zinc-400 group-hover:text-zinc-200"
                                                    )}>
                                                        {template.replace(/_/g, ' ').replace('.html', '')}
                                                    </span>
                                                </div>

                                                <ChevronRight className={cn(
                                                    "w-4 h-4 ml-auto shrink-0 transition-opacity",
                                                    isActive ? "opacity-100 text-blue-400" : "opacity-0 group-hover:opacity-40"
                                                )} />
                                            </motion.button>
                                        );
                                    })}
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>
                </div>

                {/* Downloads Section */}
                <div className="flex flex-col flex-shrink-0 pt-6 border-t border-white/5 space-y-4">
                    <div className="flex items-center gap-2 px-2">
                        <Download className="w-3.5 h-3.5 text-blue-500" />
                        <span className="text-[10px] font-black text-blue-500/80 uppercase tracking-[0.15em]">Descarga de Documentos</span>
                    </div>

                    <div className="flex flex-col gap-3">
                        <UIActionCard
                            label="Formato Word"
                            icon={<Download className="w-4 h-4" />}
                            status={isGenerating === 'word' ? 'GENERANDO' : 'DOCX v2.1'}
                            color="blue"
                            onClick={() => onDownload('word')}
                            disabled={!selectedTemplate || !!isGenerating}
                        />
                        <UIActionCard
                            label="Certificado PDF"
                            icon={<FileType className="w-4 h-4" />}
                            status={isGenerating === 'pdf' ? 'RENDERIZANDO' : 'PDF/A Pro'}
                            color="red"
                            onClick={() => onDownload('pdf')}
                            disabled={!selectedTemplate || !!isGenerating}
                        />
                        <UIActionCard
                            label="Datos Excel"
                            icon={<FileSpreadsheet className="w-4 h-4" />}
                            status={isGenerating === 'excel' ? 'PROCESANDO' : 'XL-DATA 4.0'}
                            color="green"
                            onClick={() => onDownload('excel')}
                            disabled={!selectedTemplate || !!isGenerating}
                        />
                    </div>

                    <div className="glass-dark rounded-2xl p-3 border border-white/5 flex items-center justify-between opacity-50 hover:opacity-100 transition-opacity">
                        <div className="flex flex-col">
                            <span className="text-[8px] font-black text-zinc-600 uppercase">System Status</span>
                            <span className="text-[9px] text-zinc-400 font-mono tracking-tighter">Sovereign Edition v4.2S</span>
                        </div>
                        <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                    </div>
                </div>
            </div>
        </aside>
    );
};
