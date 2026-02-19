
import { useState } from 'react'
import { Upload, X, Check } from 'lucide-react'

export interface DocumentConfig {
    esquemaColores: string
    fuenteDocumento: string
    tamanoFuente: number
    logoBase64: string | null
    ocultarIGV?: boolean
    formato?: 'excel' | 'pdf' | 'word'
}

interface FocusPersonalizerProps {
    config: DocumentConfig
    onChange: (newConfig: Partial<DocumentConfig>) => void
    onFinalize: () => void
}

export function FocusPersonalizer({ config, onChange, onFinalize }: FocusPersonalizerProps) {

    // Función helper para procesar la subida del logo
    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (file) {
            const reader = new FileReader()
            reader.onloadend = () => {
                const base64String = reader.result as string
                onChange({ logoBase64: base64String })
            }
            reader.readAsDataURL(file)
        }
    }

    return (
        <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-[100] animate-in fade-in slide-in-from-bottom-5 duration-300">
            <div className="bg-gray-900/95 backdrop-blur-xl border border-white/10 p-3 rounded-2xl shadow-2xl flex flex-col gap-2 w-[420px]">

                {/* FILA 1: Identidad y Estilo */}
                <div className="flex items-center justify-between gap-3 border-b border-white/5 pb-2">
                    {/* Logo Upload */}
                    <div className="flex items-center gap-2">
                        <label className="cursor-pointer group relative w-8 h-8 flex-none" title="Cambiar Logo">
                            <input type="file" accept="image/*" onChange={handleFileUpload} className="hidden" />
                            <div className={`w-full h-full rounded-lg border flex items-center justify-center transition-all ${config.logoBase64 ? 'border-green-500/50 bg-green-500/10' : 'border-white/10 bg-white/5 hover:bg-white/10'}`}>
                                {config.logoBase64 ? (
                                    <img src={config.logoBase64} alt="Logo" className="w-5 h-5 object-contain" />
                                ) : (
                                    <Upload className="w-4 h-4 text-gray-400 group-hover:text-white" />
                                )}
                            </div>
                        </label>
                        <span className="text-[10px] font-bold text-gray-500 uppercase">Logo</span>
                    </div>

                    {/* Colores Compactos */}
                    <div className="flex gap-1.5 border-l border-white/10 pl-3">
                        {[
                            { id: 'azul-tesla', color: '#3B82F6', label: 'Tesla Blue' },
                            { id: 'rojo-energia', color: '#EF4444', label: 'Red' },
                            { id: 'verde-ecologico', color: '#22C55E', label: 'Eco' },
                            { id: 'personalizado', color: '#8B5CF6', label: 'Pro' }
                        ].map((scheme) => (
                            <button
                                key={scheme.id}
                                onClick={() => onChange({ esquemaColores: scheme.id })}
                                className={`w-5 h-5 rounded-full transition-all border ${config.esquemaColores === scheme.id ? 'scale-110 border-white shadow-lg shadow-' + scheme.color + '/50' : 'border-transparent opacity-60 hover:opacity-100 hover:border-white/30'}`}
                                style={{ backgroundColor: scheme.color }}
                                title={scheme.label}
                            />
                        ))}
                    </div>

                    {/* Botón Cerrar Explicito */}
                    <button
                        onClick={onFinalize}
                        className="ml-auto p-1.5 hover:bg-white/10 rounded-lg text-gray-400 hover:text-white transition-colors"
                        title="Cerrar Personalizador"
                    >
                        <X size={16} />
                    </button>
                </div>

                {/* FILA 2: Tipografía */}
                <div className="flex items-center justify-between gap-3">
                    {/* Fuentes Compactas */}
                    <div className="flex gap-1">
                        {['Calibri', 'Arial'].map(font => ( // Limitado a 2 para espacio
                            <button
                                key={font}
                                onClick={() => onChange({ fuenteDocumento: font })}
                                className={`px-2 py-1 rounded text-[10px] font-medium transition-all ${config.fuenteDocumento === font ? 'bg-white/20 text-white border border-white/10' : 'text-gray-500 hover:text-gray-300 border border-transparent'}`}
                                style={{ fontFamily: font }}
                            >
                                {font}
                            </button>
                        ))}
                    </div>

                    {/* Slider Compacto */}
                    <div className="flex items-center gap-2 flex-1 justify-end pl-2">
                        <span className="text-[9px] text-gray-500">Tt</span>
                        <input
                            type="range"
                            min="8"
                            max="16"
                            step="0.5"
                            value={config.tamanoFuente || 11}
                            onChange={(e) => onChange({ tamanoFuente: parseFloat(e.target.value) })}
                            className="w-24 h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-white hover:accent-gray-400"
                        />
                        <span className="text-[10px] text-gray-400 w-8 text-right font-mono">{config.tamanoFuente}pt</span>
                    </div>
                </div>
            </div>
        </div>
    )
}
