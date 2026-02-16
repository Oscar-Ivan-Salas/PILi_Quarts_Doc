
import React from 'react';
import { Settings, PieChart, Type, FileText, Image as ImageIcon, Upload, CheckCircle } from 'lucide-react';

export interface DocumentConfig {
    esquemaColores: string;
    fuenteDocumento: string;
    mostrarLogo: boolean;
    logoBase64: string | null;
    ocultarIGV: boolean;
    ocultarPreciosUnitarios: boolean;
    ocultarTotalesPorItem: boolean;
}

interface DocumentPersonalizerProps {
    config: DocumentConfig;
    onChange: (newConfig: Partial<DocumentConfig>) => void;
}

export function DocumentPersonalizer({ config, onChange }: DocumentPersonalizerProps) {

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
        <div className="bg-gray-900 border-l border-gray-800 h-full overflow-y-auto w-[320px] shadow-2xl flex flex-col">
            <div className="p-4 border-b border-gray-800 bg-gray-900/95 backdrop-blur sticky top-0 z-10">
                <h3 className="text-white font-bold flex items-center gap-2">
                    <Settings className="w-5 h-5 text-yellow-500" />
                    Personalización
                </h3>
            </div>

            <div className="p-6 space-y-8 flex-1">

                {/* 1. Esquema de Colores */}
                <section>
                    <label className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                        <PieChart className="w-4 h-4" />
                        Colores
                    </label>
                    <div className="space-y-2">
                        {[
                            { id: 'azul-tesla', label: 'Azul Tesla', color: '#3B82F6', desc: 'Corporativo' },
                            { id: 'rojo-energia', label: 'Rojo Energía', color: '#EF4444', desc: 'Vibrante' },
                            { id: 'verde-ecologico', label: 'Verde Eco', color: '#22C55E', desc: 'Sostenible' },
                            { id: 'personalizado', label: 'Personalizado', color: '#8B5CF6', desc: 'Moderno' }
                        ].map(theme => (
                            <button
                                key={theme.id}
                                onClick={() => onChange({ esquemaColores: theme.id })}
                                className={`w-full p-3 rounded-xl border transition-all flex items-center gap-3 group ${config.esquemaColores === theme.id
                                        ? 'bg-gray-800 border-yellow-500 shadow-md'
                                        : 'bg-transparent border-gray-800 hover:bg-gray-800/50 hover:border-gray-700'
                                    }`}
                            >
                                <div
                                    className="w-8 h-8 rounded-full shadow-inner flex items-center justify-center transition-transform group-hover:scale-110"
                                    style={{ backgroundColor: theme.color }}
                                >
                                    {config.esquemaColores === theme.id && <CheckCircle className="w-5 h-5 text-white drop-shadow-md" />}
                                </div>
                                <div className="text-left">
                                    <div className="text-sm font-bold text-gray-200">{theme.label}</div>
                                    <div className="text-xs text-gray-500">{theme.desc}</div>
                                </div>
                            </button>
                        ))}
                    </div>
                </section>

                <hr className="border-gray-800" />

                {/* 2. Tipografía */}
                <section>
                    <label className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                        <Type className="w-4 h-4" />
                        Tipografía
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                        {['Calibri', 'Arial', 'Roboto', 'Times New Roman'].map(font => (
                            <button
                                key={font}
                                onClick={() => onChange({ fuenteDocumento: font })}
                                className={`p-2 text-sm rounded-lg border transition-all ${config.fuenteDocumento === font
                                        ? 'bg-gray-800 border-yellow-500 text-white'
                                        : 'bg-gray-900 border-gray-700 text-gray-400 hover:text-white hover:border-gray-500'
                                    }`}
                                style={{ fontFamily: font }}
                            >
                                {font}
                            </button>
                        ))}
                    </div>
                </section>

                <hr className="border-gray-800" />

                {/* 3. Logo */}
                <section>
                    <label className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                        <ImageIcon className="w-4 h-4" />
                        Logo de Empresa
                    </label>

                    <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-800 text-center">
                        {config.logoBase64 ? (
                            <div className="relative group">
                                <img
                                    src={config.logoBase64}
                                    alt="Logo"
                                    className="h-16 mx-auto object-contain mb-3 rounded bg-white p-1"
                                />
                                <button
                                    onClick={() => onChange({ logoBase64: null })}
                                    className="text-xs text-red-400 hover:text-red-300 underline"
                                >
                                    Eliminar Logo
                                </button>
                            </div>
                        ) : (
                            <div className="py-2">
                                <div className="w-12 h-12 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-2 text-gray-600">
                                    <ImageIcon size={20} />
                                </div>
                                <p className="text-xs text-gray-500 mb-3">Sin logo cargado</p>
                            </div>
                        )}

                        <label className="block w-full">
                            <input
                                type="file"
                                accept="image/*"
                                onChange={handleFileUpload}
                                className="hidden"
                            />
                            <div className="w-full bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold py-2 px-4 rounded-lg cursor-pointer transition-colors flex items-center justify-center gap-2">
                                <Upload size={14} />
                                {config.logoBase64 ? 'Cambiar Logo' : 'Subir Logo'}
                            </div>
                        </label>
                    </div>
                </section>

                <hr className="border-gray-800" />

                {/* 4. Opciones de Visualización */}
                <section>
                    <label className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                        <FileText className="w-4 h-4" />
                        Visualización
                    </label>
                    <div className="space-y-2">
                        <label className="flex items-center justify-between p-2 rounded-lg hover:bg-gray-800/50 cursor-pointer transition-colors">
                            <span className="text-sm text-gray-300">Mostrar IGV</span>
                            <input
                                type="checkbox"
                                checked={!config.ocultarIGV}
                                onChange={() => onChange({ ocultarIGV: !config.ocultarIGV })}
                                className="w-4 h-4 rounded border-gray-600 bg-gray-800 text-yellow-500 focus:ring-yellow-500"
                            />
                        </label>
                        <label className="flex items-center justify-between p-2 rounded-lg hover:bg-gray-800/50 cursor-pointer transition-colors">
                            <span className="text-sm text-gray-300">Precios Unitarios</span>
                            <input
                                type="checkbox"
                                checked={!config.ocultarPreciosUnitarios}
                                onChange={() => onChange({ ocultarPreciosUnitarios: !config.ocultarPreciosUnitarios })}
                                className="w-4 h-4 rounded border-gray-600 bg-gray-800 text-yellow-500 focus:ring-yellow-500"
                            />
                        </label>
                    </div>
                </section>

            </div>
        </div>
    );
}

export default DocumentPersonalizer;
