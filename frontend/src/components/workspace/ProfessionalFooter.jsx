import React from 'react';
import { Activity, ShieldCheck, Cpu } from 'lucide-react';

/**
 * ProfessionalFooter - Componente de pie de página de alta gama
 * 
 * Implementa una estética de glassmorphism con desenfoque de fondo,
 * indicadores de estado técnicos y branding refinado.
 */
const ProfessionalFooter = ({ version = "v3.0.2" }) => {
    return (
        <div className="mt-auto p-4 border-t border-white/5 bg-gray-950/40 backdrop-blur-md">
            {/* Branding & Version */}
            <div className="flex items-center justify-between mb-3 text-[10px] tracking-widest uppercase text-gray-500 font-semibold">
                <div className="flex items-center gap-1.5">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.6)]"></div>
                    <span className="text-gray-400">PILI QUARTS</span>
                </div>
                <span className="bg-gray-800/80 px-2 py-0.5 rounded text-gray-300 border border-white/5">
                    {version}
                </span>
            </div>

            {/* System Status Indicators */}
            <div className="grid grid-cols-2 gap-2 mb-4">
                <div className="flex items-center gap-2 p-2 rounded bg-white/[0.03] border border-white/5">
                    <Cpu className="w-3.5 h-3.5 text-blue-400" />
                    <div className="flex flex-col">
                        <span className="text-[9px] text-gray-500 leading-none">AI ENGINE</span>
                        <span className="text-[10px] text-blue-100 font-medium">OPTIMIZED</span>
                    </div>
                </div>
                <div className="flex items-center gap-2 p-2 rounded bg-white/[0.03] border border-white/5">
                    <Activity className="w-3.5 h-3.5 text-green-400" />
                    <div className="flex flex-col">
                        <span className="text-[9px] text-gray-500 leading-none">LATENCY</span>
                        <span className="text-[10px] text-green-100 font-medium">12ms</span>
                    </div>
                </div>
            </div>

            {/* Bottom Rights & Heartbeat */}
            <div className="flex items-center justify-between pt-3 border-t border-white/5 text-[9px] text-gray-600">
                <div className="flex items-center gap-2">
                    <ShieldCheck className="w-3 h-3 text-gray-500" />
                    <span>ENCRYPTED END-TO-END</span>
                </div>
                <div className="flex items-center gap-1.5">
                    <span className="w-1 h-1 rounded-full bg-green-500 animate-pulse"></span>
                    <span className="uppercase font-bold tracking-tighter">LIVE</span>
                </div>
            </div>

            {/* Copyright Disclaimer (Subtle) */}
            <p className="mt-4 text-[8px] text-center text-gray-700 font-medium tracking-tight">
                © 2026 PILi_Quarts Engineering. All rights reserved.
            </p>
        </div>
    );
};

export default ProfessionalFooter;
