import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface UIActionCardProps {
    label: string;
    icon: React.ReactNode;
    status: string;
    color: 'blue' | 'green' | 'red';
    onClick: () => void;
    disabled?: boolean;
}

export const UIActionCard: React.FC<UIActionCardProps> = ({
    label,
    icon,
    status,
    color,
    onClick,
    disabled
}) => {
    const colorMap = {
        blue: 'border-blue-500/30 text-blue-400',
        green: 'border-emerald-500/30 text-emerald-400',
        red: 'border-rose-500/30 text-rose-400'
    };

    const glowMap = {
        blue: 'bg-blue-500/20 shadow-[0_0_15px_rgba(59,130,246,0.3)]',
        green: 'bg-emerald-500/20 shadow-[0_0_15px_rgba(16,185,129,0.3)]',
        red: 'bg-rose-500/20 shadow-[0_0_15px_rgba(244,63,94,0.3)]'
    };

    return (
        <motion.button
            whileHover={{ y: -4, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onClick}
            disabled={disabled}
            className={cn(
                "group relative flex items-center gap-4 px-6 py-4 rounded-2xl border transition-all duration-500 overflow-hidden bg-zinc-950/80",
                disabled ? "opacity-30 grayscale cursor-not-allowed" : "cursor-pointer",
                colorMap[color]
            )}
        >
            {/* Animated Glow Overlay */}
            <div className={cn(
                "absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-xl -z-10",
                glowMap[color].split(' ')[0]
            )} />

            {/* Burning Border Effect */}
            <div className={cn(
                "absolute inset-0 border-[1.5px] rounded-2xl opacity-0 group-hover:opacity-100 transition-all duration-700",
                glowMap[color]
            )} />

            <div className="relative z-10 p-2 rounded-xl bg-black/50 border border-white/5 shadow-inner">
                {icon}
            </div>

            <div className="flex flex-col items-start relative z-10 text-left">
                <span className="text-[10px] font-black uppercase tracking-widest text-zinc-500 group-hover:text-zinc-300 transition-colors">
                    {label}
                </span>
                <span className={cn(
                    "text-[9px] font-mono font-bold transition-all",
                    color === 'blue' ? 'text-blue-400' : color === 'green' ? 'text-emerald-400' : 'text-rose-400'
                )}>
                    {status}
                </span>
            </div>

            {/* Shimmer Effect */}
            <div className="absolute top-0 -inset-full h-full w-1/2 z-5 block transform -skew-x-12 bg-gradient-to-r from-transparent to-white/5 opacity-0 group-hover:animate-shimmer" />
        </motion.button>
    );
};
