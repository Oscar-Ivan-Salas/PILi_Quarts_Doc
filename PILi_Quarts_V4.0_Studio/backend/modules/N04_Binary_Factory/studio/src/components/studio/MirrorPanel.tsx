import React, { useEffect, useRef, useCallback } from 'react';
import { Monitor, Scaling } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MirrorPanelProps {
    html: string;
    overrides: {
        logo: string | null;
        primaryColor: string;
        secondaryColor: string;
        fontFamily: string;
        fontSize: number;
        data: Record<string, string>;
    };
    isSyncing: boolean;
    isGenerating?: string | null;
    onCodeChange?: (newHtml: string) => void;
    onExpand?: () => void;
}

// Genera el bloque CSS del ADN Visual para inyectar en el iframe
function buildStyleBlock(p: string, s: string, f: string, fs: number, logo: string): string {
    return `<style id="pili-adn-visual">
  :root { --pili-primary: ${p}; --pili-secondary: ${s}; --pili-font: "${f}", sans-serif; --pili-font-size: ${fs}pt; }
  body { font-family: var(--pili-font) !important; font-size: var(--pili-font-size) !important; line-height: 1.5; color: #333; background: white; }
  .color-primario,.empresa-nombre,.footer-empresa,.titulo-documento h1,.info-box h3,.tabla-section h2,.observaciones h3,.totales-valor,.dynamic-primary { color: ${p} !important; }
  .color-secundario,.info-label,.numero-cotizacion { color: ${s} !important; }
  .header { border-bottom-color: ${p} !important; }
  .titulo-documento { border-left-color: ${p} !important; background: linear-gradient(135deg, ${p}18 0%, ${s}28 100%) !important; }
  .info-box h3 { border-bottom-color: ${p} !important; }
  .tabla-section h2 { border-bottom-color: ${p} !important; }
  .totales-box { border-color: ${p} !important; }
  .footer { border-top-color: ${p} !important; }
  .observaciones { border-left-color: ${s} !important; }
  .observaciones li:before { color: ${p} !important; }
  thead { background: linear-gradient(135deg, ${p} 0%, ${s} 100%) !important; color: white !important; }
  thead th { color: white !important; }
  tbody tr:hover { background-color: ${p}15 !important; }
  .totales-row:last-child { background: linear-gradient(135deg, ${p} 0%, ${s} 100%) !important; color: white !important; }
  .totales-row:last-child .totales-label, .totales-row:last-child .totales-valor { color: white !important; }
  .dynamic-bg-primary { background-color: ${p} !important; }
  .logo-placeholder,.pili-logo { border: 2px dashed ${p} !important; display: flex !important; align-items: center !important; justify-content: center !important; min-height: 80px; min-width: 160px; border-radius: 8px; position: relative; overflow: hidden; }
  .logo-placeholder img,.pili-logo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; z-index: 10; background: white; }
  ${logo ? `.pili-logo { content: url("${logo}") !important; }` : ''}
</style>`;
}

export const MirrorPanel: React.FC<MirrorPanelProps> = ({ html, overrides, isSyncing, isGenerating, onCodeChange, onExpand }) => {
    const iframeRef = useRef<HTMLIFrameElement>(null);
    const isWritingRef = useRef(false); // guard para evitar re-render durante doc.write

    // Escribe el HTML base completo en el iframe (solo cuando cambia el html del template)
    const writeHtml = useCallback((htmlContent: string, ov: typeof overrides) => {
        const iframe = iframeRef.current;
        if (!iframe || isWritingRef.current) return;

        const p = ov.primaryColor;
        const s = ov.secondaryColor;
        const f = ov.fontFamily;
        const fs = ov.fontSize;
        const logo = ov.logo || '';

        const styleBlock = buildStyleBlock(p, s, f, fs, logo);

        // Procesar placeholders {{TAG}} como el V3.0
        let processed = htmlContent;
        Object.entries(ov.data).forEach(([key, value]) => {
            processed = processed.replace(new RegExp(`{{${key}.*?}}`, 'g'), value);
        });

        const hasDoctype = processed.trim().toLowerCase().startsWith('<!doctype');
        let content: string;
        if (hasDoctype) {
            content = processed.includes('</body>')
                ? processed.replace('</body>', `${styleBlock}</body>`)
                : processed.replace('</head>', `${styleBlock}</head>`);
        } else {
            content = `<!DOCTYPE html>\n<html><head></head><body>${processed}${styleBlock}</body></html>`;
        }

        try {
            isWritingRef.current = true;
            // setTimeout(0) desacopla doc.open() del ciclo de reconciliación de React → elimina crash
            setTimeout(() => {
                try {
                    const doc = iframe.contentDocument;
                    if (!doc) return;
                    doc.open();
                    doc.write(content);
                    doc.close();
                } finally {
                    isWritingRef.current = false;
                }

                // Setup editable tras la escritura
                setTimeout(() => {
                    try {
                        const doc = iframe.contentDocument;
                        if (!doc?.body) return;
                        doc.body.contentEditable = 'true';
                        doc.body.spellcheck = false;
                        if (onCodeChange) {
                            doc.addEventListener('input', () => {
                                if (!doc.body) return;
                                const body = doc.body.innerHTML;
                                const updated = html.includes('</body>')
                                    ? html.replace(/<body[^>]*>[\s\S]*<\/body>/i, `<body>${body}</body>`)
                                    : body;
                                onCodeChange(updated);
                            });
                        }
                    } catch (_) { /* cross-origin safety */ }
                }, 200);
            }, 0);
        } catch (e) {
            isWritingRef.current = false;
        }
    }, [onCodeChange]);

    // Actualiza SOLO el tag de estilo en el iframe (sin reescribir todo el HTML)
    const updateStyle = useCallback((ov: typeof overrides) => {
        const iframe = iframeRef.current;
        if (!iframe || isWritingRef.current) return;

        try {
            const doc = iframe.contentDocument;
            if (!doc) return;

            const p = ov.primaryColor;
            const s = ov.secondaryColor;
            const f = ov.fontFamily;
            const fs = ov.fontSize;
            const logo = ov.logo || '';

            // Buscar el style tag existente y actualizarlo directamente
            let styleEl = doc.getElementById('pili-adn-visual') as HTMLStyleElement | null;
            if (!styleEl) {
                styleEl = doc.createElement('style');
                styleEl.id = 'pili-adn-visual';
                doc.head?.appendChild(styleEl);
            }

            styleEl.textContent = `
  :root { --pili-primary: ${p}; --pili-secondary: ${s}; --pili-font: "${f}", sans-serif; --pili-font-size: ${fs}pt; }
  body { font-family: var(--pili-font) !important; font-size: var(--pili-font-size) !important; }
  .color-primario,.empresa-nombre,.footer-empresa,.titulo-documento h1,.info-box h3,.tabla-section h2,.observaciones h3,.totales-valor,.dynamic-primary { color: ${p} !important; }
  .color-secundario,.info-label,.numero-cotizacion { color: ${s} !important; }
  .header { border-bottom-color: ${p} !important; }
  .titulo-documento { border-left-color: ${p} !important; background: linear-gradient(135deg, ${p}18 0%, ${s}28 100%) !important; }
  .info-box h3 { border-bottom-color: ${p} !important; }
  .tabla-section h2 { border-bottom-color: ${p} !important; }
  .totales-box { border-color: ${p} !important; }
  .footer { border-top-color: ${p} !important; }
  .observaciones { border-left-color: ${s} !important; }
  .observaciones li:before { color: ${p} !important; }
  thead { background: linear-gradient(135deg, ${p} 0%, ${s} 100%) !important; color: white !important; }
  thead th { color: white !important; }
  tbody tr:hover { background-color: ${p}15 !important; }
  .totales-row:last-child { background: linear-gradient(135deg, ${p} 0%, ${s} 100%) !important; color: white !important; }
  .totales-row:last-child .totales-label, .totales-row:last-child .totales-valor { color: white !important; }
  .dynamic-bg-primary { background-color: ${p} !important; }
  .logo-placeholder,.pili-logo { border: 2px dashed ${p} !important; }`;

            // ── INYECCIÓN DE LOGO DIRECTA EN DOM (no CSS) ──────────────────
            // content:url() no funciona en divs normales — manipulamos el DOM
            const logoPlaceholder = doc.querySelector('.logo-placeholder') as HTMLElement | null;
            if (logoPlaceholder) {
                if (logo && logo.startsWith('data:image')) {
                    // Insertar imagen — marcar con data-pili-logo para poder reemplazarla
                    const existingImg = logoPlaceholder.querySelector('img[data-pili-logo]') as HTMLImageElement | null;
                    if (existingImg) {
                        existingImg.src = logo; // Actualizar si ya existe
                    } else {
                        logoPlaceholder.innerHTML = `<img data-pili-logo="true" src="${logo}" alt="Logo" style="max-height:80px;max-width:160px;object-fit:contain;border:none;" />`;
                    }
                } else {
                    // Sin logo: restaurar placeholder de texto si fue reemplazado
                    const hasCustomImg = !!logoPlaceholder.querySelector('img[data-pili-logo]');
                    if (hasCustomImg) {
                        logoPlaceholder.innerHTML = `<div style="font-weight:bold;color:${p};">TU EMPRESA</div>`;
                    }
                }
            }
        } catch (_) { /* cross-origin safety */ }
    }, []);

    // Efecto 1: Recargar el iframe completo solo cuando cambia el HTML del template
    useEffect(() => {
        writeHtml(html, overrides);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [html]);

    // Efecto 2: Solo actualizar el <style> en el iframe cuando cambian los overrides visuales
    useEffect(() => {
        updateStyle(overrides);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [overrides.primaryColor, overrides.secondaryColor, overrides.fontFamily, overrides.fontSize, overrides.logo]);

    return (
        <div className="flex-1 flex flex-col h-full bg-[#050505] overflow-hidden relative">
            <div className="px-6 py-3 bg-black/60 backdrop-blur-md border-b border-white/5 flex items-center justify-between z-10">
                <div className="flex items-center gap-3">
                    <Monitor className="w-4 h-4 text-blue-500" />
                    <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-widest">Espejo de Soberanía</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className={cn(
                        "flex items-center gap-2 px-3 py-1 rounded-full border transition-all duration-500 relative overflow-hidden group",
                        isSyncing ? "bg-blue-500/20 border-blue-500/40 shadow-[0_0_15px_rgba(59,130,246,0.3)]" : "bg-zinc-900 border-white/5"
                    )}>
                        <div className={cn(
                            "absolute inset-0 bg-blue-500/10 transition-opacity",
                            isSyncing ? "opacity-100 animate-pulse" : "opacity-0 group-hover:opacity-100"
                        )} />
                        <Scaling className={cn("w-3 h-3 text-blue-500", isSyncing ? "animate-spin" : "")} />
                        <span className="text-[10px] font-mono text-zinc-300 tracking-tighter">
                            {isSyncing ? 'SYNCING...' : 'SYNC ACTIVE'}
                        </span>
                    </div>

                    {onExpand && (
                        <button
                            onClick={onExpand}
                            className="p-1.5 rounded-lg bg-white/5 border border-white/10 text-zinc-400 hover:text-white hover:bg-white/10 transition-all"
                            title="Vista Inmersiva"
                        >
                            <Scaling className="w-4 h-4" />
                        </button>
                    )}
                </div>
            </div>

            <div className="flex-1 p-12 overflow-y-auto custom-scrollbar bg-black relative flex justify-center">
                {(isSyncing || isGenerating) && (
                    <div className="absolute inset-0 z-20 pointer-events-none overflow-hidden">
                        <div className="absolute inset-0 bg-blue-500/5 backdrop-blur-[1px] animate-pulse" />
                        <div className="absolute top-0 left-0 w-full h-[2px] bg-blue-500 shadow-[0_0_15px_rgba(59,130,246,1),0_0_30px_rgba(59,130,246,0.6)] animate-scan" />
                        <div className="absolute top-0 left-0 w-full h-40 bg-gradient-to-b from-blue-500/20 to-transparent animate-scan" />
                    </div>
                )}
                <div className="w-full max-w-[850px] bg-white rounded-sm shadow-[0_24px_80px_rgba(0,0,0,0.8)] border border-white/10 overflow-hidden h-fit transition-transform duration-500 hover:scale-[1.01]">
                    <iframe
                        ref={iframeRef}
                        title="Mirror View"
                        className="w-full h-full border-none min-h-[1100px]"
                    />
                </div>
                <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-blue-500/5 to-transparent pointer-events-none" />
            </div>

            <div className="absolute inset-0 pointer-events-none opacity-[0.05]"
                style={{ backgroundImage: 'radial-gradient(#fff 1px, transparent 1px)', backgroundSize: '32px 32px' }}
            />
        </div>
    );
};
