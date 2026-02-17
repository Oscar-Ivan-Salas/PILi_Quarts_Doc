import React from 'react';
import { Cpu, Activity, ShieldCheck } from 'lucide-react';

export const ProfessionalFooter: React.FC = () => {
    return (
        <div className="mt-auto p-4 border-t border-white/5 bg-gray-950/40 backdrop-blur-md font-sans">
            {/* Branding & Version */}
            <div className="flex items-center justify-between mb-3 text-[10px] tracking-widest uppercase text-gray-500 font-semibold">
                <div className="flex items-center gap-1.5">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#0052A3] shadow-[0_0_8px_rgba(0,82,163,0.6)]"></div>
                    <span className="text-gray-400">PILI QUARTS STUDIO</span>
                </div>
                <span className="bg-white/5 px-2 py-0.5 rounded text-gray-400 border border-white/5 font-mono text-[9px]">
                    v4.0.1 ALPHA
                </span>
            </div>

            {/* System Status Indicators */}
            <div className="grid grid-cols-2 gap-2 mb-4">
                <div className="flex items-center gap-2 p-2 rounded bg-white/[0.02] border border-white/5">
                    <Cpu className="w-3.5 h-3.5 text-[#0052A3]" />
                    <div className="flex flex-col">
                        <span className="text-[9px] text-gray-600 leading-none uppercase">AI Engine</span>
                        <span className="text-[10px] text-white/80 font-medium tracking-tight">Tesla Core</span>
                    </div>
                </div>
                <div className="flex items-center gap-2 p-2 rounded bg-white/[0.02] border border-white/5">
                    <Activity className="w-3.5 h-3.5 text-[#D4AF37]" />
                    <div className="flex flex-col">
                        <span className="text-[9px] text-gray-600 leading-none uppercase">Studio Sync</span>
                        <span className="text-[10px] text-white/80 font-medium tracking-tight">Active</span>
                    </div>
                </div>
            </div>

            {/* Bottom Rights & Heartbeat */}
            <div className="flex items-center justify-between pt-3 border-t border-white/5 text-[9px] text-gray-600">
                <div className="flex items-center gap-2">
                    <ShieldCheck className="w-3 h-3 text-gray-500" />
                    <span>ENGR. STUDIO</span>
                </div>
                <div className="flex items-center gap-1.5">
                    <span className="w-1 h-1 rounded-full bg-[#D4AF37] animate-pulse"></span>
                    <span className="uppercase font-bold tracking-tighter text-[#D4AF37]">LIVE</span>
                </div>
            </div>
        </div>
    );
};

export default ProfessionalFooter;
