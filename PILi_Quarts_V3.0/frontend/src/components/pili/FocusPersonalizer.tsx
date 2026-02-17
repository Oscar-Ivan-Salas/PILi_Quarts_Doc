
import React from 'react';
import { Type, Image as ImageIcon, Upload, CheckCircle, Save } from 'lucide-react';
import { GradientButton } from '../ui/gradient-button';
import { type DocumentConfig } from './DocumentPersonalizer';

interface FocusPersonalizerProps {
    config: DocumentConfig;
    onChange: (newConfig: Partial<DocumentConfig>) => void;
    onFinalize: () => void;
}

export function FocusPersonalizer({ config, onChange, onFinalize }: FocusPersonalizerProps) {

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                onChange({ logoBase64: reader.result as string });
            };
            reader.readAsDataURL(file);
        }
    };

    return (
        <div className="fixed bottom-10 left-1/2 -translate-x-1/2 z-[100] animate-in fade-in slide-in-from-bottom-5 duration-500">
            <div className="bg-gray-900/80 backdrop-blur-xl border border-white/10 p-4 rounded-3xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] flex items-center gap-8 px-8">

                {/* 1. Colores */}
                <div className="flex items-center gap-3 border-r border-white/10 pr-6">
                    <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Colores</span>
                    <div className="flex gap-2">
                        {[
                            { id: 'azul-tesla', color: '#3B82F6' },
                            { id: 'rojo-energia', color: '#EF4444' },
                            { id: 'verde-ecologico', color: '#22C55E' },
                            { id: 'personalizado', color: '#8B5CF6' }
                        ].map(theme => (
                            <button
                                key={theme.id}
                                onClick={() => onChange({ esquemaColores: theme.id })}
                                className={`w-8 h-8 rounded-full border-2 transition-all hover:scale-110 active:scale-95 flex items-center justify-center ${config.esquemaColores === theme.id ? 'border-white scale-110 shadow-lg' : 'border-transparent'
                                    }`}
                                style={{ backgroundColor: theme.color }}
                            >
                                {config.esquemaColores === theme.id && <CheckCircle className="w-4 h-4 text-white" />}
                            </button>
                        ))}
                    </div>
                </div>

                {/* 2. Tipografía */}
                <div className="flex items-center gap-3 border-r border-white/10 pr-6">
                    <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Fuente</span>
                    <div className="flex gap-1">
                        {['Calibri', 'Arial', 'Roboto'].map(font => (
                            <button
                                key={font}
                                onClick={() => onChange({ fuenteDocumento: font })}
                                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${config.fuenteDocumento === font
                                        ? 'bg-white/20 text-white border border-white/20'
                                        : 'text-gray-400 hover:text-white hover:bg-white/5 border border-transparent'
                                    }`}
                                style={{ fontFamily: font }}
                            >
                                {font}
                            </button>
                        ))}
                    </div>
                </div>

                {/* 3. Logo */}
                <div className="flex items-center gap-3 border-r border-white/10 pr-6">
                    <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Identity</span>
                    <label className="cursor-pointer group relative">
                        <input type="file" accept="image/*" onChange={handleFileUpload} className="hidden" />
                        <div className={`p-2 rounded-xl border transition-all ${config.logoBase64 ? 'border-green-500/50 bg-green-500/10' : 'border-white/10 bg-white/5 hover:border-white/30'
                            }`}>
                            {config.logoBase64 ? (
                                <img src={config.logoBase64} alt="Logo" className="w-6 h-6 object-contain" />
                            ) : (
                                <Upload className="w-5 h-5 text-gray-400 group-hover:text-white" />
                            )}
                        </div>
                        {config.logoBase64 && (
                            <button
                                onClick={(e) => { e.preventDefault(); onChange({ logoBase64: null }); }}
                                className="absolute -top-2 -right-2 w-4 h-4 bg-red-500 rounded-full flex items-center justify-center text-[10px] text-white opacity-0 group-hover:opacity-100 transition-opacity"
                            >
                                ×
                            </button>
                        )}
                    </label>
                </div>

                {/* 4. Finalizar */}
                <GradientButton
                    onClick={onFinalize}
                    className="!min-w-[140px] !px-6 !py-2.5 !rounded-2xl shadow-[0_0_20px_rgba(37,99,235,0.3)]"
                >
                    <div className="flex items-center gap-2">
                        <Save className="w-4 h-4" />
                        Finalizar
                    </div>
                </GradientButton>

            </div>
        </div>
    );
}
