import React from 'react';
import { Cpu, Activity, ShieldCheck, Database, HardDrive, BarChart } from 'lucide-react';
import { motion } from 'framer-motion';

export const ProfessionalFooter: React.FC = () => {
    return (
        <div className="mt-auto bg-black/60 border-t border-white/5 p-6 font-sans relative overflow-hidden">
            {/* Background Glow */}
            <div className="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-[#0052A3]/30 to-transparent" />

            {/* System Metrics HUD */}
            <div className="space-y-6">
                {/* Branding Block */}
                <div className="flex items-center justify-between mb-4">
                    <div className="flex flex-col gap-1">
                        <span className="text-[8px] font-black tracking-[0.5em] text-[#0052A3] uppercase">Engineering Core</span>
                        <div className="flex items-center gap-2">
                            <div className="w-1.5 h-1.5 rounded-sm bg-white animate-pulse shadow-[0_0_8px_white]" />
                            <span className="text-[10px] text-white font-black tracking-widest uppercase">Pili Quarts Studio</span>
                        </div>
                    </div>
                    <div className="flex flex-col items-end">
                        <span className="text-[7px] text-gray-700 font-bold uppercase tracking-widest">Security Level</span>
                        <div className="flex gap-1 mt-1">
                            {[1, 1, 1, 0].map((v, i) => (
                                <div key={i} className={`w-3 h-1 ${v ? 'bg-green-500/40' : 'bg-white/5'}`} />
                            ))}
                        </div>
                    </div>
                </div>

                {/* Performance Visualizers Fictitious */}
                <div className="grid grid-cols-1 gap-4">
                    <div className="bg-white/[0.02] border border-white/5 p-3 rounded-lg flex items-center justify-between group hover:border-[#0052A3]/30 transition-all">
                        <div className="flex items-center gap-3">
                            <div className="p-1.5 rounded bg-black border border-white/5">
                                <Cpu className="w-3 h-3 text-[#0052A3]" />
                            </div>
                            <div className="flex flex-col">
                                <span className="text-[8px] text-gray-600 font-black uppercase">CPU Load</span>
                                <span className="text-[10px] text-white/50 font-mono tracking-tighter">12.4% Optimal</span>
                            </div>
                        </div>
                        <div className="w-16 h-1 bg-white/5 rounded-full overflow-hidden">
                            <motion.div
                                animate={{ width: ['20%', '15%', '25%', '18%'] }}
                                transition={{ duration: 4, repeat: Infinity }}
                                className="h-full bg-[#0052A3]"
                            />
                        </div>
                    </div>

                    <div className="bg-white/[0.02] border border-white/5 p-3 rounded-lg flex items-center justify-between group hover:border-[#D4AF37]/30 transition-all">
                        <div className="flex items-center gap-3">
                            <div className="p-1.5 rounded bg-black border border-white/5">
                                <Database className="w-3 h-3 text-[#D4AF37]" />
                            </div>
                            <div className="flex flex-col">
                                <span className="text-[8px] text-gray-600 font-black uppercase">MEM Buffer</span>
                                <span className="text-[10px] text-white/50 font-mono tracking-tighter">4.2 Gb Cloud</span>
                            </div>
                        </div>
                        <div className="w-16 h-1 bg-white/5 rounded-full overflow-hidden">
                            <motion.div
                                animate={{ width: ['60%', '65%', '58%', '62%'] }}
                                transition={{ duration: 6, repeat: Infinity }}
                                className="h-full bg-[#D4AF37]"
                            />
                        </div>
                    </div>
                </div>

                {/* Bottom Bar: Operational Status */}
                <div className="pt-4 border-t border-white/5 flex items-center justify-between">
                    <div className="flex items-center gap-4 text-[8px] font-black tracking-[0.2em] text-white/20 uppercase">
                        <div className="flex items-center gap-2">
                            <ShieldCheck className="w-3 h-3" />
                            <span>V4.0 SECURED</span>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <motion.div
                            animate={{ opacity: [0.3, 1, 0.3] }}
                            transition={{ duration: 1.5, repeat: Infinity }}
                            className="w-1.5 h-1.5 rounded-full bg-green-500 shadow-[0_0_8px_#22c55e]"
                        />
                        <span className="text-[9px] font-black text-white/40 tracking-widest uppercase">Live Node</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProfessionalFooter;
