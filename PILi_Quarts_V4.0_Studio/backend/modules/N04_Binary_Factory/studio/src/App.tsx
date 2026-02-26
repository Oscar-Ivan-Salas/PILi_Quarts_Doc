import { useState, useEffect } from 'react';
import { Sidebar } from './components/studio/Sidebar';
import { EditorPanel } from './components/studio/EditorPanel';
import { MirrorPanel } from './components/studio/MirrorPanel';
import { PersonalizerPanel } from './components/studio/PersonalizerPanel';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { Sparkles, Binary, Settings2, Code2, Cpu, Download, FileType, FileSpreadsheet } from 'lucide-react';
import { cn } from './lib/utils';

function App() {
    const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
    const [htmlCode, setHtmlCode] = useState<string>('<!-- Selecciona un modelo soberano para iniciar el espejo -->');
    const [isGenerating, setIsGenerating] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState<'editor' | 'design' | 'system'>('editor');
    const [isSyncing, setIsSyncing] = useState(false);
    const [progress, setProgress] = useState(0);
    const [isFullscreen, setIsFullscreen] = useState(false);
    const [renderedHtml, setRenderedHtml] = useState<string>('');

    const [settings, setSettings] = useState({
        // ... (líneas intermedias omitidas por brevedad en el pensamiento, pero el reemplazo será total en el rango especificado o usaré chunks mejor)
        logo: null as string | null,
        primaryColor: '#0052A3',
        secondaryColor: '#1E40AF',
        fontFamily: 'Calibri',
        fontSize: 11,
        currency: 'PEN',
        data: {
            CLIENTE: 'INDUSTRIAL SOLUTIONS PERÚ S.A.',
            CLIENTE_RUC: '20555666777',
            CLIENTE_DIRECCION: 'Parque Industrial Lote 45, Lurín',
            NOMBRE_EMISOR: 'TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.',
            RUC_EMISOR: '20601138787',
            PROYECTO_NOMBRE: 'SISTEMA DE CONTROL N04',
            CODIGO_DOC: 'N04-STUDIO-2026',
            FECHA_DOC: new Date().toLocaleDateString('es-PE')
        } as Record<string, string>
    });

    const handleSelectTemplate = async (name: string) => {
        try {
            setSelectedTemplate(name);
            const response = await axios.get(`http://localhost:8005/api/studio/template/${name}`);
            setHtmlCode(response.data.content);
            setRenderedHtml(response.data.content); // Inicializar render
        } catch (error) {
            console.error("Error loading template:", error);
        }
    };

    // 🔄 Renderizado en Tiempo Real (Sincronización Soberana)
    useEffect(() => {
        const renderTemplate = async () => {
            if (!htmlCode || htmlCode.includes('Selecciona un modelo')) return;

            setIsSyncing(true);
            try {
                // Sincronizar con el motor Jinja2 del backend
                const response = await axios.post('http://localhost:8005/api/studio/render', {
                    html: htmlCode,
                    settings: {
                        ...settings,
                        data: {
                            ...settings.data,
                            logo_url: settings.logo // Inyectar logo para el motor de plantillas
                        }
                    }
                });

                if (response.data.html) {
                    setRenderedHtml(response.data.html);
                }
            } catch (error) {
                console.error("❌ [STUDIO RENDER ERROR]:", error);
            } finally {
                setIsSyncing(false);
            }
        };

        const timeoutId = setTimeout(renderTemplate, 600); // Debounce para no saturar el socket
        return () => clearTimeout(timeoutId);
    }, [htmlCode, settings.currency, settings.data, selectedTemplate]);

    const handleDownload = async (format: 'word' | 'excel' | 'pdf') => {
        if (!selectedTemplate) return;

        setIsGenerating(format);
        try {
            const response = await axios.post(
                'http://localhost:8005/api/studio/generate',
                {
                    html: htmlCode,
                    format: format,
                    name: selectedTemplate,
                    settings: settings
                },
                {
                    responseType: 'blob',
                    timeout: 30000 // Timeout de 30s para evitar esperas infinitas
                }
            );

            if (!response.data) throw new Error("No data received from engine");

            const blob = new Blob([response.data], {
                type: format === 'pdf' ? 'application/pdf' :
                    format === 'word' ? 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' :
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            });

            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;

            const extensionMap: Record<string, string> = { 'word': 'docx', 'excel': 'xlsx', 'pdf': 'pdf' };
            const ext = extensionMap[format] || format;

            link.setAttribute('download', `STUDIO_${selectedTemplate}_${new Date().getTime()}.${ext}`);
            document.body.appendChild(link);
            link.click();

            // Cleanup
            setTimeout(() => {
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
            }, 100);

            setProgress(100);
        } catch (error: any) {
            console.error(`[STUDIO ERROR] ${format} generation failed:`, error);
            // Intentar extraer mensaje de error del blob si es posible
            alert(`Error al generar ${format.toUpperCase()}. Por favor verifique la conexión con el motor N04.`);
        } finally {
            setTimeout(() => {
                setIsGenerating(null);
                setProgress(0);
            }, 800);
        }
    };

    return (
        <div className="flex h-screen w-full bg-[#000000] text-zinc-300 selection:bg-blue-500/20 font-sans overflow-hidden">
            {/* Background decoration */}
            <div className="absolute inset-0 pointer-events-none opacity-[0.02] z-0"
                style={{ backgroundImage: 'radial-gradient(#fff 1px, transparent 1px)', backgroundSize: '40px 40px' }}
            />

            {/* Top Loading Bar (La "barrita" premium) */}
            <AnimatePresence>
                {(isSyncing || isGenerating) && (
                    <motion.div
                        initial={{ opacity: 0, width: "0%" }}
                        animate={{ opacity: 1, width: isSyncing ? "100%" : "95%" }}
                        exit={{ opacity: 0, transition: { duration: 0.5 } }}
                        className="fixed top-0 left-0 h-[3px] bg-gradient-to-r from-blue-500 via-indigo-500 to-blue-400 z-[100] shadow-[0_0_15px_rgba(59,130,246,0.8)]"
                    >
                        <motion.div
                            animate={{ x: ["-100%", "100%"] }}
                            transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                            className="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent w-32"
                        />
                    </motion.div>
                )}
            </AnimatePresence>

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

            {/* Sidebar: Plantillas y Centro de Control (Contextual) */}
            <Sidebar
                onSelectTemplate={handleSelectTemplate}
                selectedTemplate={selectedTemplate}
                isGenerating={isGenerating}
                onDownload={handleDownload}
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
                <div className="flex-1 flex min-h-0 overflow-hidden relative">
                    {/* Editor / Personalizer side */}
                    <section className="flex-[0.45] min-w-0 border-r border-white/5 bg-zinc-950/20 overflow-y-auto custom-scrollbar relative">
                        <AnimatePresence mode="wait">
                            {activeTab === 'editor' ? (
                                <motion.div
                                    key="editor"
                                    initial={{ opacity: 0, scale: 0.98 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.98 }}
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
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: 10 }}
                                    className="h-full"
                                >
                                    <PersonalizerPanel
                                        settings={settings}
                                        onUpdate={(newSettings: any) => setSettings(prev => ({ ...prev, ...newSettings }))}
                                        isSyncing={isSyncing}
                                        setIsSyncing={setIsSyncing}
                                    />
                                </motion.div>
                            ) : (
                                <motion.div
                                    key="system"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="p-12 space-y-8 h-full overflow-y-auto"
                                >
                                    <div className="space-y-2">
                                        <h3 className="text-sm font-black text-zinc-400 uppercase tracking-[0.3em]">Parámetros del Sistema</h3>
                                        <div className="h-1 w-12 bg-blue-500 rounded-full" />
                                    </div>

                                    <p className="text-xs text-zinc-600 leading-relaxed font-mono uppercase tracking-tighter">
                                        Estado: <span className="text-green-500">Preparado para Inyección Directa</span>.<br />
                                        Versión: N04 Studio Core v4.2S<br />
                                        Seguridad: Enlace Encriptado (127.0.0.1)<br />
                                        Espejo: <span className="text-blue-500">Protocolo Sovereign Activo</span>
                                    </p>

                                    <div className="grid grid-cols-1 gap-6">
                                        <div className="p-6 rounded-2xl bg-[#0a0a0a] border border-white/5 shadow-2xl relative overflow-hidden group">
                                            <div className="absolute top-0 right-0 p-2 opacity-5 text-white"><Cpu size={48} /></div>
                                            <span className="text-[10px] text-zinc-500 block mb-1 uppercase font-black tracking-widest">Latencia de Espejo</span>
                                            <span className="text-2xl font-black text-white italic">2.4ms</span>
                                        </div>
                                        <div className="p-6 rounded-2xl bg-[#0a0a0a] border border-white/5 shadow-2xl relative overflow-hidden group">
                                            <div className="absolute top-0 right-0 p-2 opacity-5 text-white"><Binary size={48} /></div>
                                            <span className="text-[10px] text-zinc-500 block mb-1 uppercase font-black tracking-widest">Capacidad de Nodos</span>
                                            <span className="text-2xl font-black text-white italic">UNLIMITED</span>
                                        </div>
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </section>

                    {/* Mirror (Preview) side */}
                    <section className="flex-[0.55] min-w-0 bg-[#020202] overflow-y-auto custom-scrollbar">
                        <MirrorPanel
                            html={renderedHtml || htmlCode}
                            overrides={settings}
                            isSyncing={isSyncing}
                            isGenerating={isGenerating}
                            onCodeChange={(newHtml) => setHtmlCode(newHtml)}
                            onExpand={() => setIsFullscreen(true)}
                        />
                    </section>
                </div>
            </main>

            {/* Immersive View Overlay (Fullscreen Mirror) */}
            <AnimatePresence>
                {isFullscreen && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-[100] bg-black/95 backdrop-blur-2xl flex flex-col p-8 overflow-hidden"
                    >
                        {/* Immersive Header */}
                        <div className="flex items-center justify-between mb-8 px-4">
                            <div className="flex items-center gap-4">
                                <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center">
                                    <Cpu className="w-6 h-6 text-white" />
                                </div>
                                <div className="flex flex-col">
                                    <h2 className="text-xl font-black text-white italic tracking-tighter uppercase">Inspección Soberana</h2>
                                    <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-widest">Aseguramiento de Calidad Nodo N04</span>
                                </div>
                            </div>

                            <button
                                onClick={() => setIsFullscreen(false)}
                                className="w-12 h-12 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-zinc-400 hover:text-white hover:bg-white/10 transition-all hover:scale-110 active:scale-95"
                            >
                                <motion.span animate={{ rotate: 180 }} transition={{ duration: 0.5 }}>✕</motion.span>
                            </button>
                        </div>

                        {/* Document Display Area */}
                        <div className="flex-1 overflow-y-auto flex justify-center custom-scrollbar p-12">
                            <div className="w-full max-w-[900px] shadow-[0_0_100px_rgba(59,130,246,0.15)] bg-white rounded-lg h-fit">
                                <MirrorPanel
                                    html={renderedHtml || htmlCode}
                                    overrides={settings}
                                    isSyncing={isSyncing}
                                    isGenerating={isGenerating}
                                />
                            </div>
                        </div>

                        {/* Sovereign Action Bar (La Tabla de Generación) */}
                        <motion.div
                            initial={{ y: 100 }}
                            animate={{ y: 0 }}
                            className="h-24 bg-zinc-950/80 border-t border-white/10 backdrop-blur-md rounded-t-[32px] flex items-center justify-center p-6 gap-6 shadow-[0_-20px_50px_rgba(0,0,0,0.5)]"
                        >
                            <div className="flex items-center gap-6 px-8 border-r border-white/10 mr-4">
                                <div className="flex flex-col">
                                    <span className="text-[10px] font-black text-zinc-500 uppercase tracking-widest">Generar Documento</span>
                                    <span className="text-sm font-bold text-white uppercase italic">Protocolo Final</span>
                                </div>
                            </div>

                            <div className="flex items-center gap-4">
                                <button
                                    onClick={() => handleDownload('word')}
                                    disabled={!!isGenerating}
                                    className="px-8 py-3 rounded-2xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition-all flex items-center gap-3 shadow-lg shadow-blue-500/20 active:scale-95 disabled:opacity-50"
                                >
                                    <Download className="w-4 h-4" />
                                    WORD DOCX
                                </button>
                                <button
                                    onClick={() => handleDownload('pdf')}
                                    disabled={!!isGenerating}
                                    className="px-8 py-3 rounded-2xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs transition-all flex items-center gap-3 shadow-lg shadow-rose-500/20 active:scale-95 disabled:opacity-50"
                                >
                                    <FileType className="w-4 h-4" />
                                    CERTIFICADO PDF
                                </button>
                                <button
                                    onClick={() => handleDownload('excel')}
                                    disabled={!!isGenerating}
                                    className="px-8 py-3 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition-all flex items-center gap-3 shadow-lg shadow-emerald-500/20 active:scale-95 disabled:opacity-50"
                                >
                                    <FileSpreadsheet className="w-4 h-4" />
                                    DATOS EXCEL
                                </button>
                            </div>

                            <div className="ml-8 pl-8 border-l border-white/10 flex items-center gap-3 opacity-50">
                                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                                <span className="text-[10px] font-mono text-zinc-400">READY TO TRANSMIT</span>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div >
    );
}

export default App;
