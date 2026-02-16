
import { motion } from 'framer-motion'
// @ts-ignore
import CotizacionEditor from './CotizacionEditor'
// @ts-ignore
import CotizacionesView from './workspace/CotizacionesView'
import { ComplexProjectForm } from './ComplexProjectForm'
// @ts-ignore
import EditableCotizacionCompleja from './EditableCotizacionCompleja'
import EditableCotizacionSimple from './EditableCotizacionSimple'
// import { SimpleServiceChat } from './pili/SimpleServiceChat'
// import { AnimatedAIChat } from './ui/AnimatedAIChat'
import { DocumentPersonalizer, type DocumentConfig } from './pili/DocumentPersonalizer'
import { ShaderAnimation } from './ui/ShaderAnimation'
import { AdminDashboard } from './AdminDashboard'

import { useState, useEffect } from 'react'
import { useWorkspaceStore } from '../store/useWorkspaceStore'
import { ArrowLeft, Maximize2, Minimize2 } from 'lucide-react'
import { piliApi } from '../services/pili-api'

export function WorkArea() {
    const { activeSection } = useWorkspaceStore()
    // UI State for FLOWS
    const [step, setStep] = useState<'form' | 'chat' | 'editor'>('form')
    const [flowData, setFlowData] = useState<any>(null)
    const [isFullscreen, setIsFullscreen] = useState(false)

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
        setFlowData({ ...data, config: docConfig }) // Init with default config
        setStep('chat') // Start at CHAT (Step 2)
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
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-full flex flex-col overflow-hidden">
                        {/* Header for Chat Step */}
                        <div className="flex-none p-4 bg-gray-900/80 border-b border-gray-800 flex justify-between items-center backdrop-blur-md z-10">
                            <div className="flex items-center gap-3">
                                <button onClick={() => setStep('form')} className="p-2 hover:bg-gray-800 rounded-lg text-gray-400 hover:text-white transition-colors">
                                    <ArrowLeft className="w-5 h-5" />
                                </button>
                                <div>
                                    <h2 className="text-lg font-bold text-white flex items-center gap-2">
                                        <span className="bg-yellow-500 text-black text-xs px-2 py-0.5 rounded-full font-bold">Paso 2</span>
                                        Co-Creación con IA
                                    </h2>
                                    <p className="text-xs text-gray-400">PILI te ayudará a completar los detalles</p>
                                </div>
                            </div>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => setIsFullscreen(!isFullscreen)}
                                    className="p-2 hover:bg-gray-800 rounded-lg text-gray-400 transition-colors hidden lg:block"
                                    title="Alternar Vista Completa"
                                >
                                    {isFullscreen ? <Minimize2 size={20} /> : <Maximize2 size={20} />}
                                </button>
                                <button onClick={() => setStep('editor')} className="px-4 py-2 bg-green-600 hover:bg-green-500 text-white text-sm font-bold rounded-xl transition-all shadow-lg hover:shadow-green-500/20">
                                    Finalizar Edición →
                                </button>
                            </div>
                        </div>

                        {/* 3-Column Split View Container */}
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
                            <div className="flex-1 bg-gray-800/50 relative overflow-hidden flex flex-col items-center">
                                <div className="absolute top-0 w-full bg-white/95 backdrop-blur-sm p-2 border-b z-10 flex justify-between items-center px-4 shadow-sm">
                                    <span className="text-xs font-bold text-gray-500 uppercase tracking-wider flex items-center gap-2">
                                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                                        Vista Previa en Tiempo Real
                                    </span>
                                </div>
                                <div className="flex-1 w-full overflow-y-auto p-4 md:p-8 pt-12 custom-scrollbar flex justify-center">
                                    <div className={`
                                        bg-white shadow-2xl min-h-[297mm] w-[210mm] transition-all origin-top
                                        ${isFullscreen ? 'scale-100' : 'scale-[0.85]'}
                                    `}>
                                        {activeSection === 'cotizacion-simple' ? (
                                            <EditableCotizacionSimple
                                                datos={flowData}
                                                // Pass synced config props
                                                esquemaColores={docConfig.esquemaColores}
                                                logoBase64={docConfig.logoBase64}
                                                fuenteDocumento={docConfig.fuenteDocumento}
                                                ocultarIGV={docConfig.ocultarIGV}
                                                ocultarPreciosUnitarios={docConfig.ocultarPreciosUnitarios}
                                                ocultarTotalesPorItem={docConfig.ocultarTotalesPorItem}
                                                onDatosChange={(newDatos: any) => setFlowData({ ...flowData, ...newDatos })}
                                            />
                                        ) : (
                                            <EditableCotizacionCompleja
                                                datos={{
                                                    cliente: flowData?.cliente,
                                                    proyecto: flowData?.proyecto || flowData?.proyecto?.nombre,
                                                    descripcion_proyecto: flowData?.descripcion_proyecto || flowData?.descripcion,
                                                    items: flowData?.items || []
                                                }}
                                                esquemaColores={docConfig.esquemaColores === 'azul-tesla' ? 'azul' : docConfig.esquemaColores}
                                            />
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* RIGHT PANEL: Customization (Collapsible/Fixed) */}
                            <div className={`
                                hidden xl:flex flex-none z-20 transition-all
                                ${isFullscreen ? 'hidden' : 'w-[320px]'}
                            `}>
                                <DocumentPersonalizer
                                    config={docConfig}
                                    onChange={updateConfig}
                                />
                            </div>

                        </div>
                    </motion.div>
                )
            }


            // Step 3: The "Paper" Editor / Preview (Final Step)
            if (step === 'editor') {
                return (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-full flex flex-col">
                        <div className="flex items-center justify-between mb-4 bg-gray-900/50 p-4 rounded-xl border border-gray-800">
                            <div className="flex items-center gap-4">
                                <button onClick={() => setStep('chat')} className="p-2 hover:bg-gray-800 rounded-lg transition-colors">
                                    <ArrowLeft className="w-5 h-5 text-gray-400" />
                                </button>
                                <div>
                                    <h2 className="text-xl font-bold text-yellow-500">
                                        {activeSection.includes('informe') ? 'Generando Informe' : 'Vista Previa del Documento'}
                                    </h2>
                                    <p className="text-xs text-gray-400">
                                        {flowData?.cliente?.nombre || 'Nuevo Documento'}
                                    </p>
                                </div>
                            </div>
                            <div className="flex gap-2">
                                <span className="px-3 py-1 bg-green-900/30 text-green-400 border border-green-800 rounded-full text-xs">Conectado a PILi 🧠</span>
                            </div>
                        </div>

                        {/* Editor View */}
                        <div className="flex-1 overflow-auto bg-gray-500/10 rounded-xl border border-gray-800 shadow-inner p-4 flex justify-center custom-scrollbar">
                            <div className="transform scale-90 origin-top bg-white shadow-2xl min-h-[297mm]">
                                {activeSection === 'cotizacion-simple' ? (
                                    <EditableCotizacionSimple
                                        datos={flowData || {}}
                                        esquemaColores={docConfig.esquemaColores}
                                        logoBase64={docConfig.logoBase64}
                                        fuenteDocumento={docConfig.fuenteDocumento}
                                        ocultarIGV={docConfig.ocultarIGV}
                                        ocultarPreciosUnitarios={docConfig.ocultarPreciosUnitarios}
                                        ocultarTotalesPorItem={docConfig.ocultarTotalesPorItem}
                                        modoEdicion={true} // Allow final edits
                                        onDatosChange={(newDatos: any) => setFlowData({ ...flowData, ...newDatos })}
                                    />
                                ) : (
                                    <EditableCotizacionCompleja
                                        datos={{
                                            cliente: flowData?.cliente,
                                            proyecto: flowData?.proyecto || flowData?.proyecto?.nombre,
                                            descripcion_proyecto: flowData?.descripcion_proyecto || flowData?.descripcion,
                                            items: flowData?.items || []
                                        }}
                                        esquemaColores="azul"
                                    />
                                )}
                            </div>
                        </div>

                        {/* ✅ PANEL DE ACCIONES FINALES */}
                        <div className="flex gap-4 p-6 bg-gray-900 border-t border-gray-800 rounded-b-2xl mt-4">
                            <button
                                onClick={() => setStep('chat')}
                                className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-xl font-bold transition-all flex items-center gap-2">
                                ← Volver al Chat
                            </button>
                            <div className="flex-1"></div>

                            <button
                                onClick={async () => {
                                    alert('Generación de Excel no implementada en Backend aún');
                                }}
                                className="px-6 py-3 bg-green-600 hover:bg-green-500 text-white rounded-xl font-bold transition-all shadow-lg hover:shadow-green-500/20 flex items-center gap-2">
                                📊 Descargar Excel
                            </button>
                            <button
                                onClick={async () => {
                                    alert('Generación de PDF no implementada en Backend aún');
                                }}
                                className="px-6 py-3 bg-red-600 hover:bg-red-500 text-white rounded-xl font-bold transition-all shadow-lg hover:shadow-red-500/20 flex items-center gap-2">
                                📄 Descargar PDF
                            </button>
                            <button
                                onClick={async () => {
                                    try {
                                        // Skill 02 & 09: Execution Hook with Identity
                                        const response = await piliApi.generateDocument({
                                            user_id: 'b2289941-d90c-4d48-b8c2-6e3fafe88944', // Seeded User
                                            project_id: 'default-project-1',             // Seeded Project
                                            format: 'docx',
                                            options: {
                                                esquemaColores: docConfig.esquemaColores,
                                                logoBase64: docConfig.logoBase64,
                                                ocultarIGV: docConfig.ocultarIGV
                                            },
                                            data: flowData // Send current state (Skill 03 - Active Canvas)
                                        });

                                        if (response.success && response.download_url) {
                                            try {
                                                // Fetch the file as a blob
                                                const fileResponse = await fetch(response.download_url);
                                                if (!fileResponse.ok) {
                                                    throw new Error(`Failed to download: ${fileResponse.statusText}`);
                                                }

                                                const blob = await fileResponse.blob();

                                                // Create download link with blob URL
                                                const blobUrl = window.URL.createObjectURL(blob);
                                                const link = document.createElement('a');
                                                link.href = blobUrl;
                                                link.download = response.download_url.split('/').pop() || 'documento.docx';

                                                // Trigger download (browser will show save dialog)
                                                document.body.appendChild(link);
                                                link.click();

                                                // Clean up - defer to avoid React error
                                                setTimeout(() => {
                                                    if (link.parentNode) {
                                                        link.parentNode.removeChild(link);
                                                    }
                                                    window.URL.revokeObjectURL(blobUrl);
                                                }, 100);

                                                // Show success notification
                                                const notification = document.createElement('div');
                                                notification.className = 'fixed bottom-4 right-4 bg-green-600 text-white px-6 py-4 rounded-lg shadow-2xl z-50 max-w-md';
                                                notification.innerHTML = `
                                                    <div class="flex items-start gap-3">
                                                        <svg class="w-6 h-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                                        </svg>
                                                        <div>
                                                            <p class="font-bold">✅ Documento Generado</p>
                                                            <p class="text-sm mt-1">Descarga iniciada - Elige dónde guardar</p>
                                                            <p class="text-xs mt-2 opacity-80">Archivo: ${link.download}</p>
                                                        </div>
                                                    </div>
                                                `;
                                                document.body.appendChild(notification);
                                                setTimeout(() => notification.remove(), 5000);

                                            } catch (downloadError: any) {
                                                console.error('Download error:', downloadError);
                                                alert(`Error descargando archivo: ${downloadError.message}\n\nUbicación del archivo: ${response.file_path}`);
                                            }
                                        } else {
                                            alert('Error: ' + response.message);
                                        }

                                    } catch (e: any) {
                                        console.error(e);
                                        alert('Error generando documento: ' + e.message);
                                    }
                                }}
                                className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-bold transition-all shadow-lg hover:shadow-blue-500/20 flex items-center gap-2">
                                📝 Descargar Word
                            </button>
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
