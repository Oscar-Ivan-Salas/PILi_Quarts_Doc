import React, { useRef } from 'react';
import { cn } from '@/lib/utils';
import { Upload, Type, Palette, Layout, Hash } from 'lucide-react';

interface PersonalizerPanelProps {
    settings: {
        logo: string | null;
        primaryColor: string;
        secondaryColor: string;
        fontFamily: string;
        fontSize: string;
        data: Record<string, string>;
    };
    onUpdate: (settings: any) => void;
}

export const PersonalizerPanel: React.FC<PersonalizerPanelProps> = ({ settings, onUpdate }) => {
    const fileInputRef = useRef<HTMLInputElement>(null);

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
        <div className="flex-1 flex flex-col h-full bg-[#050505] overflow-y-auto custom-scrollbar border-r border-white/5 relative z-10">
            <div className="p-10 space-y-12">
                <header>
                    <h2 className="text-xl font-bold text-white tracking-tight mb-2">Protocolo de Identidad</h2>
                    <p className="text-xs text-zinc-500 font-mono italic uppercase tracking-tighter">Configuración de Marca y Variables Maestras</p>
                </header>

                {/* Branding Section */}
                <section className="space-y-8">
                    <div className="flex items-center gap-3 border-b border-white/5 pb-4">
                        <Palette className="w-5 h-5 text-blue-500" />
                        <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-zinc-400">Visual DNA</h3>
                    </div>

                    <div className="grid grid-cols-1 gap-8">
                        {/* Logo Upload Card Premium */}
                        <div className="relative group">
                            <div className="p-8 rounded-3xl bg-zinc-900/40 border border-white/5 hover:border-blue-500/40 transition-all duration-500 shadow-2xl shadow-black/50">
                                <div className="flex items-center justify-between mb-6">
                                    <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Logo Principal</span>
                                    <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
                                </div>

                                <div className="flex items-center gap-8">
                                    <div
                                        onClick={() => fileInputRef.current?.click()}
                                        className="w-28 h-28 rounded-3xl border-2 border-dashed border-zinc-800 hover:border-blue-500/50 transition-all duration-500 flex flex-col items-center justify-center cursor-pointer overflow-hidden bg-black/60 group-hover:bg-blue-500/5 relative"
                                    >
                                        {settings.logo ? (
                                            <div className="relative w-full h-full p-4">
                                                <img src={settings.logo} className="w-full h-full object-contain" alt="Logo preview" />
                                                <div className="absolute inset-0 bg-blue-500/10 opacity-0 group-hover:opacity-100 transition-opacity" />
                                            </div>
                                        ) : (
                                            <Upload className="w-8 h-8 text-zinc-700 group-hover:text-blue-500 transition-colors" />
                                        )}
                                    </div>
                                    <div className="flex flex-col gap-2 text-left">
                                        <button
                                            onClick={() => fileInputRef.current?.click()}
                                            className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl text-[10px] font-bold transition-all uppercase"
                                        >
                                            Subir Activo
                                        </button>
                                        <button
                                            onClick={() => onUpdate({ logo: null })}
                                            className="text-[9px] text-zinc-600 hover:text-red-500 transition-colors font-mono uppercase text-left"
                                        >
                                            Eliminar
                                        </button>
                                    </div>
                                </div>
                                <input ref={fileInputRef} type="file" className="hidden" accept="image/*" onChange={handleLogoUpload} />
                            </div>
                        </div>

                        {/* Colors & Typography Cards */}
                        <div className="grid grid-cols-2 gap-4">
                            <div className="p-5 rounded-2xl bg-zinc-900/30 border border-white/5 space-y-3">
                                <span className="text-[10px] font-bold text-zinc-500 uppercase">Colores</span>
                                <div className="flex gap-4">
                                    <input
                                        type="color"
                                        value={settings.primaryColor}
                                        onChange={(e) => onUpdate({ primaryColor: e.target.value })}
                                        className="w-10 h-10 rounded-xl bg-transparent border-none cursor-pointer hover:scale-110 transition-transform"
                                    />
                                    <input
                                        type="color"
                                        value={settings.secondaryColor}
                                        onChange={(e) => onUpdate({ secondaryColor: e.target.value })}
                                        className="w-10 h-10 rounded-xl bg-transparent border-none cursor-pointer hover:scale-110 transition-transform"
                                    />
                                </div>
                            </div>

                            <div className="p-5 rounded-2xl bg-zinc-900/30 border border-white/5 space-y-3">
                                <span className="text-[10px] font-bold text-zinc-500 uppercase">Tipografía</span>
                                <select
                                    value={settings.fontFamily}
                                    onChange={(e) => onUpdate({ fontFamily: e.target.value })}
                                    className="w-full bg-black/40 border border-white/10 rounded-xl px-3 py-2 text-[10px] font-bold uppercase text-zinc-400 focus:outline-none focus:border-blue-500/50 appearance-none"
                                >
                                    <option value="Inter">Inter</option>
                                    <option value="Outfit">Outfit</option>
                                    <option value="'JetBrains Mono'">Monospaced</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Dynamic Data Section */}
                <section className="space-y-6">
                    <div className="flex items-center gap-3 border-b border-white/5 pb-4">
                        <Layout className="w-5 h-5 text-green-500" />
                        <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-zinc-400">Content Engine</h3>
                    </div>

                    <div className="space-y-4">
                        {[
                            { id: 'CLIENTE_NOMBRE', label: 'Nombre / Razón Social del Cliente', icon: <Type className="w-4 h-4" /> },
                            { id: 'CLIENTE_RUC', label: 'RUC del Cliente', icon: <Hash className="w-4 h-4" /> },
                            { id: 'CLIENTE_DIRECCION', label: 'Dirección del Cliente', icon: <Layout className="w-4 h-4" /> },
                            { id: 'NOMBRE_EMISOR', label: 'Nombre del Emisor (Tu Empresa)', icon: <Type className="w-4 h-4" /> },
                            { id: 'RUC_EMISOR', label: 'RUC del Emisor', icon: <Hash className="w-4 h-4" /> },
                            { id: 'FECHA_DOC', label: 'Fecha del Documento', icon: <Layout className="w-4 h-4" /> },
                            { id: 'MONEDA_SIMBOLO', label: 'Símbolo de Moneda (S/, $)', icon: <Hash className="w-4 h-4" /> },
                            { id: 'MONEDA_NOMBRE', label: 'Nombre de Moneda (Soles, USD)', icon: <Hash className="w-4 h-4" /> },
                        ].map((field) => (
                            <div key={field.id} className="relative group/field">
                                <div className="absolute left-5 top-1/2 -translate-y-1/2 text-zinc-700 group-focus-within/field:text-blue-500 transition-colors">
                                    {field.icon}
                                </div>
                                <input
                                    type="text"
                                    placeholder={field.label}
                                    value={settings.data[field.id] || ''}
                                    onChange={(e) => updateData(field.id, e.target.value)}
                                    className="w-full bg-zinc-900/50 border border-white/5 rounded-2xl pl-12 pr-6 py-4 text-xs font-medium focus:outline-none focus:border-blue-500/30 focus:bg-zinc-900 transition-all placeholder:text-zinc-800 shadow-inner"
                                />
                                <div className="absolute inset-0 rounded-2xl border border-blue-500/10 opacity-0 group-focus-within/field:opacity-100 transition-opacity pointer-events-none" />
                            </div>
                        ))}
                    </div>
                </section>
            </div>

            {/* Decorative Blur Backgrounds */}
            <div className="absolute top-0 right-0 w-80 h-80 bg-blue-600/5 blur-[120px] pointer-events-none rounded-full" />
            <div className="absolute bottom-40 left-0 w-80 h-80 bg-purple-600/5 blur-[120px] pointer-events-none rounded-full" />
        </div>
    );
};
