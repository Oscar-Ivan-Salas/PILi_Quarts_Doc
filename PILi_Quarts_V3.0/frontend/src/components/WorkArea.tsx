
import { motion } from 'framer-motion'
// @ts-ignore
import CotizacionEditor from './CotizacionEditor'
// @ts-ignore
import CotizacionesView from './workspace/CotizacionesView'
import ProjectsView from './workspace/ProjectsView'
import ReportsView from './workspace/ReportsView'
import { ComplexProjectForm } from './ComplexProjectForm'
// Eliminados componentes antiguos redundantes
import { type DocumentConfig } from './pili/DocumentPersonalizer'
import { FocusPersonalizer } from './pili/FocusPersonalizer'
import { ShaderAnimation } from './ui/ShaderAnimation'
import { AdminDashboard } from './AdminDashboard'
import { QuoteSimple } from './documents/QuoteSimple'
import { QuoteComplex } from './documents/QuoteComplex'
import { ProjectSimple } from './documents/ProjectSimple'
import { ProjectComplex } from './documents/ProjectComplex'
import { ReportTechnical } from './documents/ReportTechnical'
import { ReportExecutive } from './documents/ReportExecutive'

import { useState, useEffect } from 'react'
import { useWorkspaceStore } from '../store/useWorkspaceStore'
import { ArrowLeft, Maximize2, Minimize2, Palette, FileText, BarChart3, CheckCircle } from 'lucide-react'
import { piliApi } from '../services/pili-api'
import { useDocumentStore } from '../store/useDocumentStore'

export function WorkArea() {
    const { activeSection, setActiveSection } = useWorkspaceStore()
    const { setDocumentType, loadDocument, setLogo } = useDocumentStore()
    // UI State for FLOWS
    const [step, setStep] = useState<'form' | 'chat' | 'editor'>('form')
    const [flowData, setFlowData] = useState<any>(null)
    const [isFullscreen, setIsFullscreen] = useState(false)
    const [isDesigning, setIsDesigning] = useState(false) // Focus Mode State

    // Lifted Configuration State (Shared between Personalizer & Preview)
    const [docConfig, setDocConfig] = useState<DocumentConfig>({
        esquemaColores: 'azul-tesla',
        fuenteDocumento: 'Calibri',
        mostrarLogo: true,
        logoBase64: null,
        ocultarIGV: false,
        ocultarPreciosUnitarios: false,
        ocultarTotalesPorItem: false
    })

    // Reset step when section changes
    useEffect(() => {
        setStep('form')
        setFlowData(null)
    }, [activeSection])

    const handleStartFlow = (data: any) => {
        console.log('Starting Flow with:', data)

        // Sync with Global Document Store
        setDocumentType(activeSection as any)
        loadDocument(data)

        if (data.config?.logo) {
            setLogo(data.config.logo)
            setDocConfig(prev => ({ ...prev, logoBase64: data.config.logo }))
        }

        setFlowData({ ...data, config: docConfig })
        setStep('chat')
    }

    const updateConfig = (newConfig: Partial<DocumentConfig>) => {
        setDocConfig(prev => {
            const updated = { ...prev, ...newConfig };
            // Also sync to flowData so final JSON has it
            setFlowData((fd: any) => ({ ...fd, config: updated }));
            return updated;
        });
    }

    const renderContent = () => {
        // --- UNIVERSAL FLOW HANDLING ---
        // 'cotizacion-simple', 'cotizacion-compleja', 'proyecto-simple', 'proyecto-complejo', 'informe-simple'...

        if (activeSection && activeSection !== 'dashboard' && activeSection !== 'admin-dashboard') {

            // Step 1: Configuration Form (The "Universal Start Form")
            if (step === 'form') {
                // Section Landing Pages (before form)
                if (activeSection === 'cotizaciones') {
                    return <CotizacionesView onServiceSelect={(id: string) => setActiveSection(id as any)} />;
                }
                if (activeSection === 'proyectos') {
                    return <ProjectsView onServiceSelect={(id: string) => setActiveSection(id as any)} />;
                }
                if (activeSection === 'informes') {
                    return <ReportsView onServiceSelect={(id: string) => setActiveSection(id as any)} />;
                }

                return (
                    <div className="relative h-full w-full">
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-full overflow-auto relative z-10">
                            <ComplexProjectForm
                                onStartChat={handleStartFlow}
                                tipoFlujo={activeSection} // Pass 'cotizacion-simple', 'proyecto-simple', etc.
                            />
                        </motion.div>
                    </div>
                )
            }


            // Step 2: PILI Chat Interaction + Live Preview + Personalizer (3-Column Layout)
            if (step === 'chat') {
                return (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-full flex flex-col overflow-hidden relative">
                        {/* Botones esquina inferior izquierda */}
                        <div className="absolute bottom-6 left-6 z-20 flex gap-2">
                            <button onClick={() => setStep('form')} className="p-3 bg-black/40 hover:bg-black/60 backdrop-blur-md rounded-xl transition-all shadow-lg">
                                <ArrowLeft className="w-5 h-5 text-white" />
                            </button>
                            <button
                                onClick={() => setIsFullscreen(!isFullscreen)}
                                className="p-3 bg-black/40 hover:bg-black/60 backdrop-blur-md rounded-xl transition-all shadow-lg"
                            >
                                {isFullscreen ? <Minimize2 className="w-5 h-5 text-white" /> : <Maximize2 className="w-5 h-5 text-white" />}
                            </button>
                        </div>

                        {/* Botones esquina inferior derecha */}
                        <div className="absolute bottom-6 right-6 z-20 flex gap-2">
                            <button
                                onClick={() => setIsDesigning(true)}
                                className="px-4 py-3 bg-white/10 hover:bg-white/20 backdrop-blur-md text-white border border-white/20 rounded-xl font-medium transition-all shadow-lg flex items-center gap-2"
                            >
                                <Palette size={18} className="text-green-400" />
                                Personalizar
                            </button>
                            <button onClick={() => setStep('editor')} className="px-6 py-3 bg-green-600 hover:bg-green-500 backdrop-blur-md text-white font-bold rounded-xl transition-all shadow-lg">
                                Finalizar ✓
                            </button>
                        </div>

                        {/* Full Screen Design Overlay (Focus Mode) */}
                        {isDesigning && (
                            <div className="fixed inset-0 z-[100] bg-black/95 backdrop-blur-3xl flex flex-col items-center justify-center animate-in fade-in duration-500">
                                <div className="absolute top-8 right-8 z-50">
                                    <button
                                        onClick={() => setIsDesigning(false)}
                                        className="p-3 bg-white/10 hover:bg-white/20 text-white rounded-full transition-all border border-white/10"
                                    >
                                        <Minimize2 size={24} />
                                    </button>
                                </div>
                                <div className="flex-1 w-full overflow-y-auto p-12 flex justify-center custom-scrollbar">
                                    <div className="bg-white shadow-[0_0_100px_rgba(255,255,255,0.1)] min-h-[297mm] w-[210mm]">
                                        {/* DOCUMENT TEMPLATE ADAPTER (CLONED FOR FOCUS MODE) */}
                                        {(() => {
                                            const commonProps = {
                                                data: flowData,
                                                colorScheme: docConfig.esquemaColores as any,
                                                logo: docConfig.logoBase64,
                                                font: docConfig.fuenteDocumento,
                                                onDataChange: (newDatos: any) => setFlowData((prev: any) => ({ ...prev, ...newDatos }))
                                            };

                                            switch (activeSection) {
                                                case 'cotizacion-simple': return <QuoteSimple {...commonProps} />;
                                                case 'cotizacion-compleja': return <QuoteComplex {...commonProps} />;
                                                case 'proyecto-simple': return <ProjectSimple {...commonProps} />;
                                                case 'proyecto-complejo': return <ProjectComplex {...commonProps} />;
                                                case 'informe-simple': return <ReportExecutive {...commonProps} />;
                                                case 'informe-complejo': return <ReportTechnical {...commonProps} />;
                                                default: return null;
                                            }
                                        })()}
                                    </div>
                                </div>
                                {/* Floating BOTTOM Toolbar */}
                                <FocusPersonalizer
                                    config={docConfig}
                                    onChange={updateConfig}
                                    onFinalize={() => setIsDesigning(false)}
                                />
                            </div>
                        )}

                        {/* 2-Column Split View Container (Chat + Simple Preview) */}
                        <div className="flex-1 flex overflow-hidden relative">

                            {/* LEFT PANEL: Chat (Fixed Width) */}
                            {/* LEFT PANEL: Chat (REMOVED - Using Global Right Panel) */}
                            {/* <div className={`
                                ${isFullscreen ? 'hidden' : 'flex'} 
                                w-full lg:w-[400px] flex-none border-r border-gray-800 bg-black flex-col z-20 shadow-2xl transition-all
                            `}>
                                <AnimatedAIChat />
                            </div> */}

                            {/* CENTER PANEL: Live Preview (Flex Grow - Centered) */}
                            <div className="flex-1 bg-gray-800/20 relative overflow-hidden flex flex-col items-center">
                                {/* Sin barra superior - documento completamente visible */}
                                <div className="flex-1 w-full overflow-y-auto p-4 md:p-12 custom-scrollbar flex justify-center">
                                    <div className={`
                                        bg-white shadow-2xl min-h-[297mm] w-[210mm] transition-all origin-top
                                        ${isFullscreen ? 'scale-100' : 'scale-[0.8]'}
                                    `}>
                                        {/* DOCUMENT TEMPLATE ADAPTER */}
                                        {(() => {
                                            const commonProps = {
                                                data: flowData,
                                                colorScheme: docConfig.esquemaColores as any,
                                                logo: docConfig.logoBase64,
                                                font: docConfig.fuenteDocumento,
                                                onDataChange: (newDatos: any) => setFlowData((prev: any) => ({ ...prev, ...newDatos }))
                                            };

                                            switch (activeSection) {
                                                case 'cotizacion-simple':
                                                    return <QuoteSimple {...commonProps} />;
                                                case 'cotizacion-compleja':
                                                    return <QuoteComplex {...commonProps} />;
                                                case 'proyecto-simple':
                                                    return <ProjectSimple {...commonProps} />;
                                                case 'proyecto-complejo':
                                                    return <ProjectComplex {...commonProps} />;
                                                case 'informe-simple':
                                                    return <ReportExecutive {...commonProps} />;
                                                case 'informe-complejo':
                                                    return <ReportTechnical {...commonProps} />;
                                                default:
                                                    return <div className="p-8 text-center text-gray-400">Plantilla no disponible para: {activeSection}</div>;
                                            }
                                        })()}
                                    </div>
                                </div>
                            </div>

                            {/* RIGHT SIDEBAR REMOVED FOR BETTER UX */}

                        </div>
                    </motion.div>
                )
            }


            // Step 3: The "Paper" Editor / Preview (Final Step)
            if (step === 'editor') {
                return (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-full flex flex-col relative overflow-hidden">
                        {/* Botón Volver - Esquina inferior izquierda */}
                        <div className="absolute bottom-6 left-6 z-20">
                            <button onClick={() => setStep('chat')} className="p-3 bg-black/40 hover:bg-black/60 backdrop-blur-md rounded-xl transition-all shadow-lg">
                                <ArrowLeft className="w-5 h-5 text-white" />
                            </button>
                        </div>

                        {/* Documento a pantalla completa */}
                        <div className="flex-1 overflow-auto bg-gray-800/20 p-4 md:p-12 flex justify-center custom-scrollbar">
                            <div className="transform scale-90 origin-top bg-white shadow-2xl min-h-[297mm]">
                                {(() => {
                                    const commonProps = {
                                        data: flowData,
                                        colorScheme: docConfig.esquemaColores as any,
                                        logo: docConfig.logoBase64,
                                        font: docConfig.fuenteDocumento,
                                        editable: false,
                                        onDataChange: (newDatos: any) => setFlowData((prev: any) => ({ ...prev, ...newDatos }))
                                    };

                                    switch (activeSection) {
                                        case 'cotizacion-simple':
                                            return <QuoteSimple {...commonProps} />;
                                        case 'cotizacion-compleja':
                                            return <QuoteComplex {...commonProps} />;
                                        case 'proyecto-simple':
                                            return <ProjectSimple {...commonProps} />;
                                        case 'proyecto-complejo':
                                            return <ProjectComplex {...commonProps} />;
                                        case 'informe-simple':
                                            return <ReportExecutive {...commonProps} />;
                                        case 'informe-complejo':
                                            return <ReportTechnical {...commonProps} />;
                                        default:
                                            return <div className="p-8 text-center text-gray-400">Documento no disponible</div>;
                                    }
                                })()}
                            </div>
                        </div>

                        {/* Barra inferior minimalista estilo FocusPersonalizer */}
                        <div className="fixed bottom-10 left-1/2 -translate-x-1/2 z-[100] animate-in fade-in slide-in-from-bottom-5 duration-500">
                            <div className="bg-gray-900/80 backdrop-blur-xl border border-white/10 p-4 rounded-3xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] flex items-center gap-6 px-8">
                                {/* Indicador de estado */}
                                <div className="flex items-center gap-3 border-r border-white/10 pr-6">
                                    <CheckCircle className="w-5 h-5 text-green-500" />
                                    <div>
                                        <span className="text-xs font-bold text-white uppercase tracking-wider">Listo</span>
                                        <p className="text-[10px] text-gray-400">Selecciona formato</p>
                                    </div>
                                </div>

                                {/* Botones de descarga */}
                                <div className="flex gap-3">
                                    <button
                                        onClick={async () => {
                                            try {
                                                const response = await fetch('http://localhost:8005/api/generation/excel', {
                                                    method: 'POST',
                                                    headers: { 'Content-Type': 'application/json' },
                                                    body: JSON.stringify({
                                                        title: activeSection || 'Documento',
                                                        data: flowData,
                                                        personalizacion: {
                                                            esquemaColores: docConfig.esquemaColores,
                                                            logoBase64: docConfig.logoBase64
                                                        }
                                                    })
                                                });

                                                if (response.ok) {
                                                    const blob = await response.blob();
                                                    const url = window.URL.createObjectURL(blob);
                                                    const a = document.createElement('a');
                                                    a.href = url;
                                                    a.download = `${activeSection || 'documento'}_${Date.now()}.xlsx`;
                                                    document.body.appendChild(a);
                                                    a.click();
                                                    setTimeout(() => {
                                                        document.body.removeChild(a);
                                                        window.URL.revokeObjectURL(url);
                                                    }, 100);
                                                } else {
                                                    alert('Error al generar Excel');
                                                }
                                            } catch (e: any) { alert('Error: ' + e.message); }
                                        }}
                                        className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 rounded-xl text-white font-medium transition-all shadow-lg flex items-center gap-2"
                                    >
                                        <BarChart3 className="w-4 h-4" />
                                        Excel
                                    </button>

                                    <button
                                        onClick={async () => {
                                            try {
                                                const response = await fetch('http://localhost:8005/api/generation/pdf', {
                                                    method: 'POST',
                                                    headers: { 'Content-Type': 'application/json' },
                                                    body: JSON.stringify({
                                                        title: activeSection || 'Documento',
                                                        data: flowData,
                                                        personalizacion: {
                                                            esquemaColores: docConfig.esquemaColores,
                                                            logoBase64: docConfig.logoBase64
                                                        }
                                                    })
                                                });

                                                if (response.ok) {
                                                    const blob = await response.blob();
                                                    const url = window.URL.createObjectURL(blob);
                                                    const a = document.createElement('a');
                                                    a.href = url;
                                                    a.download = `${activeSection || 'documento'}_${Date.now()}.pdf`;
                                                    document.body.appendChild(a);
                                                    a.click();
                                                    setTimeout(() => {
                                                        document.body.removeChild(a);
                                                        window.URL.revokeObjectURL(url);
                                                    }, 100);
                                                } else {
                                                    alert('Error al generar PDF');
                                                }
                                            } catch (e: any) { alert('Error: ' + e.message); }
                                        }}
                                        className="px-4 py-2.5 bg-rose-600 hover:bg-rose-500 rounded-xl text-white font-medium transition-all shadow-lg flex items-center gap-2"
                                    >
                                        <FileText className="w-4 h-4" />
                                        PDF
                                    </button>

                                    <button
                                        onClick={async () => {
                                            try {
                                                const response = await fetch('http://localhost:8005/api/generation/word', {
                                                    method: 'POST',
                                                    headers: { 'Content-Type': 'application/json' },
                                                    body: JSON.stringify({
                                                        title: activeSection || 'Documento',
                                                        data: flowData,
                                                        doc_type: activeSection,
                                                        personalizacion: {
                                                            esquemaColores: docConfig.esquemaColores,
                                                            logoBase64: docConfig.logoBase64,
                                                            ocultarIGV: docConfig.ocultarIGV
                                                        }
                                                    })
                                                });

                                                if (response.ok) {
                                                    const blob = await response.blob();
                                                    const url = window.URL.createObjectURL(blob);
                                                    const a = document.createElement('a');
                                                    a.href = url;
                                                    a.download = `${activeSection || 'documento'}_${Date.now()}.docx`;
                                                    document.body.appendChild(a);
                                                    a.click();
                                                    setTimeout(() => {
                                                        document.body.removeChild(a);
                                                        window.URL.revokeObjectURL(url);
                                                    }, 100);
                                                } else {
                                                    alert('Error al generar Word');
                                                }
                                            } catch (e: any) { alert('Error: ' + e.message); }
                                        }}
                                        className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 rounded-xl text-white font-medium transition-all shadow-lg flex items-center gap-2"
                                    >
                                        <FileText className="w-4 h-4" />
                                        Word
                                    </button>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )
            }
        }

        // --- Admin Dashboard ---
        if (activeSection === 'admin-dashboard') {
            return <AdminDashboard />
        }

        // --- Default / Fallback (Dashboard View) ---
        return (
            <div className="relative h-full w-full flex flex-col items-center justify-center overflow-hidden rounded-xl border bg-black/60">
                <ShaderAnimation />
                <span className="absolute pointer-events-none z-10 text-center text-7xl leading-none font-semibold tracking-tighter whitespace-pre-wrap text-white drop-shadow-2xl">
                    PILi_Quarts
                </span>
                <p className="absolute mt-24 text-gray-300 z-10 text-xl font-light tracking-widest">
                    ESPACIO DE TRABAJO INTELIGENTE
                </p>
            </div>
        )
    }

    return (
        <div className="flex-1 h-full p-6 overflow-hidden bg-black/40 backdrop-blur-sm">
            {renderContent()}
        </div>
    )
}
