import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Maximize2,
    Minimize2,
    Settings,
    Download,
    Share2,
    Printer,
    FileCode,
    Cpu,
    Zap
} from 'lucide-react';
import { useWorkspaceStore } from '../store/useWorkspaceStore';
import EditableCotizacionSimple from './EditableCotizacionSimple';
import EditableCotizacionCompleja from './EditableCotizacionCompleja';

export function WorkArea() {
    const { activeSection } = useWorkspaceStore();
    const [isFullscreen, setIsFullscreen] = useState(false);
    const [flowData, setFlowData] = useState<any>({
        cliente: "Empresa de Ingeniería Tesla",
        proyecto: "Sistema Quarts v4.0",
        items: []
    });

    const [docConfig, setDocConfig] = useState<any>({
        esquemaColores: 'azul-tesla',
        fuenteDocumento: 'Inter',
        ocultarIGV: false,
        ocultarPreciosUnitarios: false,
        ocultarTotalesPorItem: false,
        logoBase64: null
    });

    return (
        <div className="flex-1 flex flex-col h-full bg-[#030712] font-sans">
            <div className="flex-1 flex overflow-hidden">
                {/* CENTER PANEL: Live Preview Studio (Engineering Excellence) */}
                <div className="flex-1 bg-[#030712] relative overflow-hidden flex flex-col items-center">
                    {/* Subtle Architectural Grid Overlay */}
                    <div className="absolute inset-0 opacity-[0.03] pointer-events-none"
                        style={{ backgroundImage: 'radial-gradient(circle, #fff 1px, transparent 1px)', backgroundSize: '32px 32px' }}>
                    </div>

                    <div className="absolute top-0 w-full studio-glass p-3 border-b border-white/5 z-10 flex justify-between items-center px-6 shadow-2xl">
                        <div className="flex items-center gap-3">
                            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse shadow-[0_0_10px_rgba(34,197,94,0.6)]"></div>
                            <span className="text-[10px] font-black text-white/50 uppercase tracking-[0.3em]">
                                Studio Preview v4.0.1
                            </span>
                        </div>
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2 group cursor-pointer">
                                <span className="text-[9px] text-gray-600 font-mono uppercase tracking-widest group-hover:text-[#0052A3] transition-colors">A4 Scale: 90%</span>
                            </div>
                            <div className="w-px h-3 bg-white/10" />
                            <button onClick={() => setIsFullscreen(!isFullscreen)} className="text-gray-500 hover:text-white transition-colors">
                                {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
                            </button>
                        </div>
                    </div>

                    <div className="flex-1 w-full overflow-y-auto p-4 md:p-12 pt-20 custom-scrollbar flex justify-center perspective-[2000px]">
                        <motion.div
                            layout
                            initial={{ y: 40, opacity: 0, rotateX: 5 }}
                            animate={{ y: 0, opacity: 1, rotateX: 0 }}
                            className={`
                                floating-a4 bg-white min-h-[297mm] w-[210mm] origin-top relative
                                ${isFullscreen ? 'scale-100' : 'scale-[0.88]'}
                            `}
                        >
                            {/* Paper Texture Overlay (Subtle) */}
                            <div className="absolute inset-0 pointer-events-none opacity-[0.01]"
                                style={{ backgroundImage: 'url("https://www.transparenttextures.com/patterns/paper-fibers.png")' }}>
                            </div>

                            <div className="p-12">
                                {activeSection === 'cotizacion-simple' ? (
                                    <EditableCotizacionSimple
                                        datos={flowData}
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
                        </motion.div>
                    </div>

                    {/* Quick Tools HUD */}
                    <div className="absolute bottom-8 right-8 flex gap-3">
                        <motion.button
                            whileHover={{ scale: 1.1, backgroundColor: "#0052A3" }}
                            className="w-10 h-10 rounded-full studio-glass flex items-center justify-center text-white/70 border border-white/10 shadow-xl"
                        >
                            <Download className="w-4 h-4" />
                        </motion.button>
                        <motion.button
                            whileHover={{ scale: 1.1, backgroundColor: "#D4AF37" }}
                            className="w-10 h-10 rounded-full studio-glass flex items-center justify-center text-white/70 border border-white/10 shadow-xl"
                        >
                            <Printer className="w-4 h-4" />
                        </motion.button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default WorkArea;
