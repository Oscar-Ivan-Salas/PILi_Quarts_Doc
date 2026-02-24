import { useState } from 'react';
import { Sidebar } from './components/studio/Sidebar';
import { EditorPanel } from './components/studio/EditorPanel';
import { MirrorPanel } from './components/studio/MirrorPanel';
import { UIActionCard } from './components/studio/UIActionCard';
import { PersonalizerPanel } from './components/studio/PersonalizerPanel';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { Sparkles, Download, FileType, FileSpreadsheet, Binary, Settings2, Code2, Cpu } from 'lucide-react';
import { cn } from './lib/utils';

function App() {
    const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
    const [htmlCode, setHtmlCode] = useState<string>('<!-- Selecciona un modelo soberano para iniciar el espejo -->');
    const [isGenerating, setIsGenerating] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState<'editor' | 'design' | 'system'>('editor');

    const [settings, setSettings] = useState({
        logo: null as string | null,
        primaryColor: '#0052A3',
        secondaryColor: '#1E40AF',
        fontFamily: 'Calibri',
        fontSize: '11pt',
        data: {
            CLIENTE_NOMBRE: 'INDUSTRIAL SOLUTIONS PERÚ S.A.',
            CLIENTE_RUC: '20555666777',
            CLIENTE_DIRECCION: 'Parque Industrial Lote 45, Lurín',
            NOMBRE_EMISOR: 'EMPRESA SOBERANA S.A.C.',
            RUC_EMISOR: '20600000001',
            PROYECTO_NOMBRE: 'SISTEMA DE CONTROL N04',
            CODIGO_DOC: 'N04-STUDIO-2026',
            FECHA_DOC: new Date().toLocaleDateString('es-PE')
        } as Record<string, string>
    });

    const handleSelectTemplate = async (name: string) => {
        try {
            setSelectedTemplate(name);
            const response = await axios.get(`http://127.0.0.1:8004/api/studio/template/${name}`);
            setHtmlCode(response.data.content);
        } catch (error) {
            console.error("Error loading template:", error);
        }
    };

    const handleDownload = async (format: 'word' | 'excel' | 'pdf') => {
        if (!selectedTemplate) return;

        setIsGenerating(format);
        try {
            const response = await axios.post(
                'http://127.0.0.1:8004/api/studio/generate',
                {
                    html: htmlCode,
                    format: format,
                    name: selectedTemplate,
                    settings: settings
                },
                { responseType: 'blob' }
            );

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            const ext = format === 'word' ? 'docx' : format;
            link.setAttribute('download', `STUDIO_${selectedTemplate}.${ext}`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error(`Error generating ${format}:`, error);
        } finally {
            setIsGenerating(null);
        }
    };

    return (
        <div className="flex h-screen w-full bg-[#000000] text-zinc-300 selection:bg-blue-500/20 font-sans overflow-hidden">
            {/* Background decoration */}
            <div className="absolute inset-0 pointer-events-none opacity-[0.02] z-0"
                style={{ backgroundImage: 'radial-gradient(#fff 1px, transparent 1px)', backgroundSize: '40px 40px' }}
            />

            {/* Activity Bar (Iconos Verticales Estilo Pro) */}
            <nav className="w-16 border-r border-white/5 bg-zinc-950 flex flex-col items-center py-6 gap-4 z-30">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center mb-4 shadow-lg shadow-blue-500/20">
                    <Cpu className="w-6 h-6 text-white" />
                </div>

                {[
                    { id: 'editor', icon: <Code2 className="w-5 h-5" />, label: 'Editor de Estructura' },
                    { id: 'design', icon: <Settings2 className="w-5 h-5" />, label: 'Personalización Visual' },
                    { id: 'system', icon: <Binary className="w-5 h-5" />, label: 'Parámetros del Sistema' },
                ].map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id as any)}
                        className={cn(
                            "w-12 h-12 rounded-xl flex items-center justify-center transition-all group relative",
                            activeTab === tab.id ? "bg-white/10 text-white" : "text-zinc-500 hover:text-zinc-300 hover:bg-white/5"
                        )}
                        title={tab.label}
                    >
                        {tab.icon}
                        {activeTab === tab.id && (
                            <motion.div layoutId="active-tab-indicator" className="absolute left-0 w-1 h-6 bg-blue-500 rounded-r-full" />
                        )}
                    </button>
                ))}
            </nav>

            {/* Sidebar: Plantillas (Contextual) */}
            <Sidebar
                onSelectTemplate={handleSelectTemplate}
                selectedTemplate={selectedTemplate}
            />

            <main className="flex-1 flex flex-col min-w-0 relative z-10">
                {/* Top Header */}
                <header className="h-14 border-b border-white/5 flex items-center justify-between px-6 bg-black/40 backdrop-blur-md">
                    <div className="flex items-center gap-4">
                        <div className="px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 flex items-center gap-2">
                            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
                            <span className="text-[10px] font-bold text-blue-400 uppercase tracking-widest">N04 Workspace Pro</span>
                        </div>
                        {selectedTemplate && (
                            <span className="text-xs text-zinc-600 font-mono">
                                {selectedTemplate.toLowerCase()}.sob
                            </span>
                        )}
                    </div>

                    <div className="flex items-center gap-4">
                        <div className="flex flex-col items-end">
                            <span className="text-[9px] font-bold text-zinc-500 uppercase">Status Operativo</span>
                            <span className="text-[10px] text-green-500 font-mono tracking-tighter">PROTOCOLO ACTIVO</span>
                        </div>
                        <div className="w-8 h-8 rounded-full border border-white/10 p-0.5 bg-zinc-900 overflow-hidden flex items-center justify-center">
                            {settings.logo ? (
                                <img src={settings.logo} className="w-full h-full object-contain" />
                            ) : (
                                <Binary className="w-4 h-4 text-zinc-800" />
                            )}
                        </div>
                    </div>
                </header>

                {/* Workspace Central */}
                <div className="flex-1 flex min-h-0 overflow-hidden">
                    {/* Editor / Personalizer side */}
                    <section className="flex-[0.45] min-w-0 border-r border-white/5 bg-zinc-950/20 overflow-hidden relative">
                        <AnimatePresence mode="wait">
                            {activeTab === 'editor' ? (
                                <motion.div
                                    key="editor"
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -10 }}
                                    className="h-full"
                                >
                                    <EditorPanel
                                        code={htmlCode}
                                        onChange={(val) => setHtmlCode(val || '')}
                                    />
                                </motion.div>
                            ) : activeTab === 'design' ? (
                                <motion.div
                                    key="design"
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -10 }}
                                    className="h-full"
                                >
                                    <PersonalizerPanel
                                        settings={settings}
                                        onUpdate={(newSettings: any) => setSettings(prev => ({ ...prev, ...newSettings }))}
                                    />
                                </motion.div>
                            ) : (
                                <motion.div
                                    key="system"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="p-12 space-y-4"
                                >
                                    <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-widest">Parámetros del Sistema</h3>
                                    <p className="text-xs text-zinc-600 leading-relaxed font-mono">
                                        Estado: Preparado para Inyección Directa.<br />
                                        Versión: N04 Studio Core v4.2<br />
                                        Seguridad: Enlace Encriptado (127.0.0.1)
                                    </p>
                                    <div className="h-px w-full bg-white/5" />
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="p-4 rounded-xl bg-zinc-900/50 border border-white/5">
                                            <span className="text-[10px] text-zinc-500 block mb-1 uppercase">Latencia</span>
                                            <span className="text-sm font-bold text-green-500">2ms</span>
                                        </div>
                                        <div className="p-4 rounded-xl bg-zinc-900/50 border border-white/5">
                                            <span className="text-[10px] text-zinc-500 block mb-1 uppercase">Espejo</span>
                                            <span className="text-sm font-bold text-blue-500">Activo</span>
                                        </div>
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </section>

                    {/* Mirror (Preview) side */}
                    <section className="flex-[0.55] min-w-0 bg-[#020202]">
                        <MirrorPanel
                            html={htmlCode}
                            overrides={settings}
                        />
                    </section>
                </div>

                {/* Action Center - Floating Downloads */}
                <footer className="absolute bottom-6 left-1/2 -translate-x-1/2 px-8 py-5 rounded-[2.5rem] glass-dark border border-white/10 shadow-2xl shadow-black flex items-center gap-10 z-40">
                    <div className="flex flex-col border-r border-white/10 pr-10">
                        <span className="text-[10px] font-black text-blue-500 uppercase tracking-widest mb-1">Mirror Output</span>
                        <span className="text-xs font-bold text-white uppercase italic">Sovereign Protocol</span>
                    </div>

                    <div className="flex gap-6">
                        <UIActionCard
                            label="Formato Word"
                            icon={<Download className="w-5 h-5 text-blue-400" />}
                            status={isGenerating === 'word' ? 'GENERANDO' : 'DOCX v2.1'}
                            color="blue"
                            onClick={() => handleDownload('word')}
                            disabled={!selectedTemplate || !!isGenerating}
                        />
                        <UIActionCard
                            label="Certificado PDF"
                            icon={<FileType className="w-5 h-5 text-red-500" />}
                            status={isGenerating === 'pdf' ? 'RENDERIZANDO' : 'PDF/A Pro'}
                            color="red"
                            onClick={() => handleDownload('pdf')}
                            disabled={!selectedTemplate || !!isGenerating}
                        />
                        <UIActionCard
                            label="Datos Excel"
                            icon={<FileSpreadsheet className="w-5 h-5 text-green-500" />}
                            status={isGenerating === 'excel' ? 'PROCESANDO' : 'XL-DATA 4.0'}
                            color="green"
                            onClick={() => handleDownload('excel')}
                            disabled={!selectedTemplate || !!isGenerating}
                        />
                    </div>
                </footer>
            </main>
        </div>
    );
}

export default App;
