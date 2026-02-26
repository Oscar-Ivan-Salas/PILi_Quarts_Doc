import React, { useRef } from 'react';
import { cn } from '@/lib/utils';
import { Upload, Type, Palette, Layout, Hash, CheckCircle2, Sliders } from 'lucide-react';

interface PersonalizerPanelProps {
    settings: {
        logo: string | null;
        primaryColor: string;
        secondaryColor: string;
        fontFamily: string;
        fontSize: number;
        currency: string;
        data: Record<string, string>;
    };
    onUpdate: (settings: any) => void;
    isSyncing: boolean;
    setIsSyncing: (val: boolean) => void;
}

const COLOR_PRESETS = [
    { id: 'blue', label: 'Azul Tesla', primary: '#3b82f6', secondary: '#1d4ed8', glow: 'shadow-blue-500/20' },
    { id: 'green', label: 'Verde Eco', primary: '#22c55e', secondary: '#15803d', glow: 'shadow-emerald-500/20' },
    { id: 'purple', label: 'Morado Tech', primary: '#a855f7', secondary: '#7e22ce', glow: 'shadow-purple-500/20' },
    { id: 'red', label: 'Rojo Energía', primary: '#ef4444', secondary: '#b91c1c', glow: 'shadow-rose-500/20' },
];

const FONTS_APA = [
    { id: 'Times New Roman', name: 'Times New Roman', style: 'Serif Clásico' },
    { id: 'Arial', name: 'Arial', style: 'Sans Moderno' },
    { id: 'Georgia', name: 'Georgia', style: 'Elegante Profesional' },
    { id: 'Calibri', name: 'Calibri', style: 'Corporativo Estándar' },
];

export const PersonalizerPanel: React.FC<PersonalizerPanelProps> = ({ settings, onUpdate, isSyncing, setIsSyncing }) => {
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleSync = () => {
        if (isSyncing) return;
        setIsSyncing(true);
        setTimeout(() => {
            setIsSyncing(false);
        }, 2000);
    };

    const handleLogoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                onUpdate({ logo: reader.result as string });
            };
            reader.readAsDataURL(file);
        }
    };

    const updateData = (key: string, value: string) => {
        onUpdate({ data: { ...settings.data, [key]: value } });
    };

    return (
        <div className="flex-1 flex flex-col h-full bg-[#050505] overflow-y-auto custom-scrollbar border-r border-white/5 relative z-10 p-10 pb-20">
            <header className="mb-12">
                <div className="flex items-center gap-3 mb-2">
                    <div className="w-1.5 h-6 bg-blue-500 rounded-full" />
                    <h2 className="text-2xl font-black text-white tracking-tight uppercase italic">Visual DNA</h2>
                </div>
                <p className="text-[10px] text-zinc-500 font-mono italic uppercase tracking-[0.2em] ml-4">Motor de Identidad Corporativa N04</p>
            </header>

            <div className="space-y-12">
                {/* 1. Branding Section (Logo) */}
                <section className="space-y-6">
                    <div className="flex items-center gap-3 border-b border-white/5 pb-4">
                        <Palette className="w-4 h-4 text-blue-500" />
                        <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-zinc-400">Activo de Marca</h3>
                    </div>

                    <div className="relative group">
                        <div className="p-8 rounded-[2rem] bg-zinc-900/40 border border-white/5 hover:border-blue-500/30 transition-all duration-500 shadow-2xl relative overflow-hidden">
                            <div className="absolute top-0 right-0 p-4">
                                <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse shadow-[0_0_10px_rgba(59,130,246,0.8)]" />
                            </div>

                            <div className="flex flex-col items-center gap-6">
                                <div
                                    onClick={() => fileInputRef.current?.click()}
                                    className="w-32 h-32 rounded-3xl border-2 border-dashed border-zinc-800 hover:border-blue-500/40 transition-all duration-500 flex flex-col items-center justify-center cursor-pointer overflow-hidden bg-black/60 relative group"
                                >
                                    {settings.logo ? (
                                        <div className="relative w-full h-full p-4 flex items-center justify-center">
                                            <img src={settings.logo} className="max-w-full max-h-full object-contain" alt="Logo preview" />
                                            <div className="absolute inset-0 bg-blue-500/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[2px]">
                                                <Upload className="w-8 h-8 text-white scale-75 group-hover:scale-100 transition-transform" />
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="flex flex-col items-center gap-2">
                                            <Upload className="w-8 h-8 text-zinc-700 group-hover:text-blue-500 transition-colors" />
                                            <span className="text-[8px] font-black text-zinc-700 uppercase tracking-widest">Inyectar Logo</span>
                                        </div>
                                    )}
                                </div>
                                <div className="flex gap-3">
                                    <button
                                        onClick={() => fileInputRef.current?.click()}
                                        className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-full text-[10px] font-black transition-all uppercase tracking-widest shadow-lg shadow-blue-500/20"
                                    >
                                        Subir Activo
                                    </button>
                                    {settings.logo && (
                                        <button
                                            onClick={() => onUpdate({ logo: null })}
                                            className="px-6 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-400 rounded-full text-[10px] font-black transition-all uppercase tracking-widest"
                                        >
                                            Limpiar
                                        </button>
                                    )}
                                </div>
                            </div>
                            <input ref={fileInputRef} type="file" className="hidden" accept="image/*" onChange={handleLogoUpload} />
                        </div>
                    </div>
                </section>

                {/* 2. Color Matrix */}
                <section className="space-y-6">
                    <div className="flex items-center gap-3 border-b border-white/5 pb-4">
                        <Palette className="w-4 h-4 text-emerald-500" />
                        <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-zinc-400">Espectro Cromático</h3>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        {COLOR_PRESETS.map((preset) => (
                            <button
                                key={preset.id}
                                onClick={() => onUpdate({ primaryColor: preset.primary, secondaryColor: preset.secondary })}
                                className={cn(
                                    "flex items-center gap-3 p-4 rounded-2xl border transition-all duration-500 group relative overflow-hidden",
                                    settings.primaryColor === preset.primary
                                        ? `bg-zinc-900 border-${preset.id}-500/40 shadow-xl ${preset.glow}`
                                        : "bg-[#080808] border-white/5 hover:border-white/10"
                                )}
                            >
                                <div className="w-8 h-8 rounded-lg shadow-inner flex items-center justify-center shrink-0" style={{ backgroundColor: preset.primary }}>
                                    {settings.primaryColor === preset.primary && <CheckCircle2 className="w-4 h-4 text-white drop-shadow-md" />}
                                </div>
                                <div className="flex flex-col items-start truncate">
                                    <span className="text-[10px] font-black text-white uppercase tracking-tighter truncate">{preset.label}</span>
                                    <span className="text-[8px] text-zinc-600 font-mono uppercase truncate">{preset.primary}</span>
                                </div>
                            </button>
                        ))}
                    </div>
                </section>

                {/* 3. Typography & APA Standards */}
                <section className="space-y-6">
                    <div className="flex items-center gap-3 border-b border-white/5 pb-4">
                        <Type className="w-4 h-4 text-purple-500" />
                        <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-zinc-400">Estándar APA 7 / Tipografía</h3>
                    </div>

                    <div className="grid grid-cols-1 gap-3">
                        {FONTS_APA.map((font) => (
                            <button
                                key={font.id}
                                onClick={() => onUpdate({ fontFamily: font.id })}
                                className={cn(
                                    "flex items-center justify-between p-4 rounded-2xl border transition-all duration-500 group",
                                    settings.fontFamily === font.id
                                        ? "bg-zinc-900 border-purple-500/40 shadow-xl shadow-purple-500/10"
                                        : "bg-[#080808] border-white/5 hover:border-white/10"
                                )}
                            >
                                <div className="flex flex-col items-start">
                                    <span style={{ fontFamily: font.id }} className="text-sm font-bold text-white mb-0.5">{font.name}</span>
                                    <span className="text-[8px] text-zinc-600 uppercase font-black tracking-widest">{font.style}</span>
                                </div>
                                {settings.fontFamily === font.id && <div className="w-2 h-2 rounded-full bg-purple-500 shadow-[0_0_10px_rgba(168,85,247,0.5)]" />}
                            </button>
                        ))}
                    </div>

                    {/* Scale Slider */}
                    <div className="p-6 rounded-3xl bg-zinc-900/30 border border-white/5 space-y-4">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <Sliders className="w-3.5 h-3.5 text-zinc-500" />
                                <span className="text-[10px] font-black text-zinc-500 uppercase tracking-widest">Escala Tipográfica</span>
                            </div>
                            <span className="text-xs font-black text-white italic">{settings.fontSize}pt</span>
                        </div>
                        <input
                            type="range"
                            min="8"
                            max="16"
                            step="0.5"
                            value={settings.fontSize}
                            onChange={(e) => onUpdate({ fontSize: parseFloat(e.target.value) })}
                            className="w-full h-1.5 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
                        />
                        <div className="flex justify-between text-[8px] font-black text-zinc-700 uppercase tracking-tighter">
                            <span>Lectura Móvil (8pt)</span>
                            <span>Impresión HD (16pt)</span>
                        </div>
                    </div>
                </section>

                {/* 4. Currency Engine */}
                <section className="space-y-6">
                    <div className="flex items-center gap-3 border-b border-white/5 pb-4">
                        <Hash className="w-4 h-4 text-emerald-400" />
                        <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-zinc-400">Moneda de Reporte</h3>
                    </div>

                    <div className="grid grid-cols-3 gap-3">
                        {[
                            { id: 'PEN', label: 'Soles (S/)', icon: '🇵🇪' },
                            { id: 'USD', label: 'Dólares ($)', icon: '🇺🇸' },
                            { id: 'EUR', label: 'Euros (€)', icon: '🇪🇺' },
                        ].map((curr) => (
                            <button
                                key={curr.id}
                                onClick={() => onUpdate({ currency: curr.id })}
                                className={cn(
                                    "flex flex-col items-center gap-2 p-4 rounded-2xl border transition-all duration-500",
                                    settings.currency === curr.id
                                        ? "bg-zinc-900 border-emerald-500/40 shadow-xl shadow-emerald-500/10"
                                        : "bg-[#080808] border-white/5 hover:border-white/10"
                                )}
                            >
                                <span className="text-xl">{curr.icon}</span>
                                <span className="text-[9px] font-black text-white uppercase tracking-tighter">{curr.label}</span>
                            </button>
                        ))}
                    </div>
                </section>

                {/* 5. Content Variables */}
                <section className="space-y-6">
                    <div className="flex items-center gap-3 border-b border-white/5 pb-4">
                        <Layout className="w-4 h-4 text-zinc-500" />
                        <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-zinc-400">Content Engine</h3>
                    </div>

                    <div className="space-y-3">
                        {[
                            { id: 'CLIENTE_NOMBRE', label: 'RAZÓN SOCIAL / CLIENTE', icon: <Type className="w-4 h-4" /> },
                            { id: 'PROYECTO_NOMBRE', label: 'TÍTULO DEL PROYECTO', icon: <Hash className="w-4 h-4" /> },
                            { id: 'CODIGO_DOC', label: 'PROTOCOLO DE SEGURIDAD', icon: <Lock className="w-4 h-4" /> }
                        ].map((field) => (
                            <div key={field.id} className="relative group/field">
                                <div className="absolute left-5 top-1/2 -translate-y-1/2 text-zinc-800 group-focus-within/field:text-blue-500 transition-colors">
                                    {field.icon || <Hash className="w-4 h-4" />}
                                </div>
                                <input
                                    type="text"
                                    placeholder={field.label}
                                    value={settings.data[field.id] || ''}
                                    onChange={(e) => updateData(field.id, e.target.value)}
                                    className="w-full bg-zinc-900/20 border border-white/5 rounded-2xl pl-12 pr-6 py-4 text-[11px] font-bold focus:outline-none focus:border-blue-500/20 focus:bg-zinc-900/60 transition-all placeholder:text-zinc-800 shadow-inner"
                                />
                            </div>
                        ))}
                    </div>
                </section>
            </div>

            {/* Final Action Button (Save/Sync) */}
            <div className="mt-12 pt-12 border-t border-white/5 relative z-20">
                <button
                    onClick={handleSync}
                    disabled={isSyncing}
                    className={cn(
                        "w-full py-6 rounded-[2rem] font-black text-xs uppercase tracking-[0.3em] transition-all flex items-center justify-center gap-4 group relative overflow-hidden",
                        isSyncing
                            ? "bg-zinc-800 text-zinc-500 cursor-wait shadow-none"
                            : "bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-[0_20px_40px_-10px_rgba(37,99,235,0.4)] hover:shadow-[0_25px_50px_-12px_rgba(37,99,235,0.6)] hover:-translate-y-1 active:scale-95"
                    )}
                >
                    {isSyncing ? (
                        <>
                            <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                            Sincronizando Visual DNA...
                        </>
                    ) : (
                        <>
                            <CheckCircle2 className="w-5 h-5 group-hover:animate-bounce" />
                            Sincronizar Visual DNA
                        </>
                    )}
                </button>
                <p className="text-[9px] text-zinc-500 font-mono mt-4 text-center uppercase tracking-tighter opacity-40">
                    Protocolo de Inyección V12.1 • Todos los cambios son permanentes
                </p>
            </div>

            {/* Ambient Backgrounds */}
            <div className="absolute top-0 right-0 w-96 h-96 bg-blue-600/5 blur-[150px] pointer-events-none rounded-full" />
            <div className="absolute bottom-20 left-0 w-96 h-96 bg-purple-600/5 blur-[150px] pointer-events-none rounded-full" />
        </div>
    );
};

// Internal Lock Icon for Content Engine
const Lock = ({ className }: { className?: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><rect width="18" height="11" x="3" y="11" rx="2" ry="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /></svg>
);
