import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Maximize2,
    Minimize2,
    Download,
    Printer,
    Layers,
    Box,
    Grid3X3,
    MousePointer2
} from 'lucide-react';
import { useWorkspaceStore } from '../store/useWorkspaceStore';
import EditableCotizacionSimple from './EditableCotizacionSimple';
import EditableCotizacionCompleja from './EditableCotizacionCompleja';

export function WorkArea() {
    const { activeSection } = useWorkspaceStore();
    const [isFullscreen, setIsFullscreen] = useState(false);
    const [viewAngle, setViewAngle] = useState({ x: 0, y: 0 });

    const [flowData, setFlowData] = useState<any>({
        cliente: "Tesla Engineering Corporation",
        proyecto: "Infraestructura Digital v4.0",
        items: []
    });

    const [docConfig] = useState<any>({
        esquemaColores: 'azul-tesla',
        fuenteDocumento: 'Inter',
        ocultarIGV: false,
    });

    // Subtle parallax effect on mouse move
    const handleMouseMove = (e: React.MouseEvent) => {
        if (!isFullscreen) {
            const { clientX, clientY } = e;
            const x = (clientY - window.innerHeight / 2) / 50;
            const y = (clientX - window.innerWidth / 2) / 50;
            setViewAngle({ x, y });
        }
    };

    return (
        <div
            onMouseMove={handleMouseMove}
            className="flex-1 flex flex-col h-full bg-[#030712] relative overflow-hidden"
        >
            {/* Cinematic Background: Floor Grid and Lights */}
            <div className="absolute inset-0 z-0">
                {/* 3D Floor Grid */}
                <div
                    className="absolute bottom-0 w-full h-1/2 opacity-[0.05]"
                    style={{
                        backgroundImage: 'linear-gradient(to right, #0052A3 1px, transparent 1px), linear-gradient(to bottom, #0052A3 1px, transparent 1px)',
                        backgroundSize: '40px 40px',
                        transform: 'perspective(500px) rotateX(60deg) translateY(50px)',
                        transformOrigin: 'bottom'
                    }}
                />

                {/* Focal Lighting */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1000px] h-[600px] bg-[#0052A3]/5 blur-[120px] rounded-full scale-150" />
            </div>

            {/* Top Toolbar Interface */}
            <div className="z-20 p-4 px-10 studio-glass border-b border-white/5 flex justify-between items-center">
                <div className="flex items-center gap-6">
                    <div className="flex items-center gap-3">
                        <div className="w-2 h-2 rounded-full bg-[#0052A3] animate-pulse" />
                        <span className="text-[10px] font-black tracking-[0.4em] text-white/40 uppercase">Studio Engine</span>
                    </div>
                    <div className="flex items-center gap-2 group cursor-pointer border-l border-white/10 pl-6 h-4">
                        <Grid3X3 className="w-3 h-3 text-white/20 group-hover:text-[#0052A3] transition-colors" />
                        <span className="text-[9px] text-gray-600 font-mono tracking-widest uppercase">Adaptive Layout Active</span>
                    </div>
                </div>

                <div className="flex items-center gap-1 bg-black/30 p-1 rounded-lg border border-white/5">
                    <button onClick={() => setIsFullscreen(!isFullscreen)} className="p-2 text-gray-500 hover:text-white transition-all">
                        {isFullscreen ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
                    </button>
                    <div className="w-px h-3 bg-white/10 mx-1" />
                    <button className="p-2 text-gray-500 hover:text-white transition-all">
                        <Box className="w-3.5 h-3.5" />
                    </button>
                </div>
            </div>

            {/* Main Studio Viewport */}
            <div className="flex-1 flex justify-center items-center relative z-10 overflow-hidden">
                <div
                    className="w-full h-full flex items-center justify-center p-20 overflow-y-auto custom-scrollbar"
                    style={{ perspective: '2500px' }}
                >
                    <motion.div
                        animate={{
                            rotateX: isFullscreen ? 0 : viewAngle.x,
                            rotateY: isFullscreen ? 0 : viewAngle.y,
                            scale: isFullscreen ? 1 : 0.85
                        }}
                        transition={{ duration: 0.8, cubicBezier: [0.16, 1, 0.3, 1] }}
                        className="floating-a4 bg-white min-h-[297mm] w-[210mm] relative rounded-[2px] overflow-hidden"
                    >
                        {/* Realistic Paper Finish Overlay */}
                        <div className="absolute inset-0 pointer-events-none opacity-[0.03] scanlines" />
                        <div
                            className="absolute inset-0 pointer-events-none opacity-[0.01]"
                            style={{ backgroundImage: 'url("https://www.transparenttextures.com/patterns/natural-paper.png")' }}
                        />

                        {/* Document Content Wrapper */}
                        <div className="p-12">
                            <AnimatePresence mode="wait">
                                <motion.div
                                    key={activeSection}
                                    initial={{ opacity: 0, scale: 0.98 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 1.02 }}
                                    transition={{ duration: 0.4 }}
                                >
                                    {activeSection === 'cotizacion-simple' ? (
                                        <EditableCotizacionSimple
                                            datos={flowData}
                                            esquemaColores={docConfig.esquemaColores}
                                            onDatosChange={(newDatos: any) => setFlowData({ ...flowData, ...newDatos })}
                                        />
                                    ) : (
                                        <EditableCotizacionCompleja
                                            datos={{
                                                cliente: flowData?.cliente,
                                                proyecto: flowData?.proyecto,
                                                items: flowData?.items || []
                                            }}
                                            esquemaColores="azul"
                                        />
                                    )}
                                </motion.div>
                            </AnimatePresence>
                        </div>
                    </motion.div>
                </div>
            </div>

            {/* Floating Action HUD */}
            <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className="absolute bottom-10 left-1/2 -translate-x-1/2 z-30 flex gap-4 p-2 studio-glass rounded-2xl border border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.5)] bg-black/60"
            >
                <div className="flex items-center gap-2 px-4 border-r border-white/5 mr-2">
                    <MousePointer2 className="w-3 h-3 text-[#0052A3]" />
                    <span className="text-[9px] font-black text-white/40 uppercase tracking-widest leading-none">Perspective Mode</span>
                </div>

                <button className="flex items-center gap-2 px-4 py-2 hover:bg-white/5 rounded-xl transition-all group">
                    <Download className="w-4 h-4 text-gray-500 group-hover:text-white" />
                    <span className="text-[10px] text-gray-600 group-hover:text-white font-bold uppercase tracking-widest">Doc Export</span>
                </button>

                <button className="flex items-center gap-2 px-4 py-2 hover:bg-white/5 rounded-xl transition-all group border-l border-white/5">
                    <Printer className="w-4 h-4 text-gray-500 group-hover:text-white" />
                    <span className="text-[10px] text-gray-600 group-hover:text-white font-bold uppercase tracking-widest">Direct Print</span>
                </button>

                <button className="flex items-center gap-2 px-4 py-2 bg-[#0052A3]/80 hover:bg-[#0052A3] rounded-xl transition-all group text-white">
                    <Layers className="w-4 h-4" />
                </button>
            </motion.div>
        </div>
    );
}

export default WorkArea;
