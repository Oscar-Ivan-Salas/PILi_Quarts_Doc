import React, { useEffect, useRef } from 'react';
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

export const MirrorPanel: React.FC<MirrorPanelProps> = ({ html, overrides, isSyncing, isGenerating, onCodeChange, onExpand }) => {
    const iframeRef = useRef<HTMLIFrameElement>(null);
    const lastInternalHtmlRef = useRef<string>('');

    // 1. Generación de Contenido para srcDoc
    const generateContent = () => {
        const styleBlock = `
      <style id="pili-sync-styles">
        :root {
          --pili-primary: ${overrides.primaryColor};
          --pili-secondary: ${overrides.secondaryColor};
          --pili-font: "${overrides.fontFamily}", serif;
          --pili-font-size: ${overrides.fontSize}pt;
        }
        
        body { 
            font-family: var(--pili-font), sans-serif !important; 
            font-size: var(--pili-font-size) !important;
            line-height: 1.5;
            color: #333;
            background: white;
            padding: 40px;
            min-height: 100vh;
            outline: none !important;
        }

        .color-primario, h1, h2, h3, .empresa-nombre { color: var(--pili-primary) !important; }
        .color-secundario { color: var(--pili-secondary) !important; }
        .bg-primario, thead, .fase-numero, .totales-row:last-child { background: var(--pili-primary) !important; background-image: none !important; }
        .border-primario, .header, .info-box h3, .titulo-documento, .tabla-section h2 { border-color: var(--pili-primary) !important; }
        
        .logo-placeholder, .pili-logo { 
            background: #f8fafc !important;
            border: 2px dashed #e2e8f0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            min-height: 80px;
            min-width: 160px;
            border-radius: 8px;
            position: relative;
            overflow: hidden;
        }

        .logo-placeholder::after, .pili-logo::after {
            content: 'IDENTIDAD CORPORATIVA';
            font-family: sans-serif;
            font-size: 8pt;
            font-weight: 900;
            color: #cbd5e1;
            letter-spacing: 0.1em;
        }

        .logo-placeholder img, .pili-logo img {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            max-height: 100%;
            max-width: 100%;
            object-fit: contain;
            z-index: 10;
            background: white;
        }
      </style>
    `;

        const processedHtml = html;

        const hasDoctype = processedHtml.trim().toLowerCase().startsWith('<!doctype');
        return hasDoctype
            ? processedHtml.replace('</head>', `${styleBlock}</head>`)
            : `<!DOCTYPE html>\n<html><head>${styleBlock}</head><body>${processedHtml}</body></html>`;
    };

    const srcDoc = generateContent();

    useEffect(() => {
        const iframe = iframeRef.current;
        if (!iframe) return;

        let isMounted = true;
        let timeoutId: any;

        const setupIframe = () => {
            if (!isMounted) return;
            
            try {
                const doc = iframe.contentDocument || iframe.contentWindow?.document;
                if (!doc || !doc.body) {
                    // Retry if not ready
                    setTimeout(setupIframe, 100);
                    return;
                }

                doc.body.contentEditable = "true";
                doc.body.spellcheck = false;

                const handleInput = () => {
                    if (!doc.body || !onCodeChange) return;
                    clearTimeout(timeoutId);
                    timeoutId = setTimeout(() => {
                        const newBodyContent = doc.body.innerHTML;
                        const hasDoctype = html.trim().toLowerCase().startsWith('<!doctype');
                        let newFullHtml = html;

                        if (hasDoctype) {
                            const bodyRegex = /<body[^>]*>(.*?)<\/body>/s;
                            if (bodyRegex.test(html)) {
                                newFullHtml = html.replace(bodyRegex, `<body>${newBodyContent}</body>`);
                            }
                        } else {
                            newFullHtml = newBodyContent;
                        }

                        lastInternalHtmlRef.current = newFullHtml;
                        onCodeChange(newFullHtml);
                    }, 500);
                };

                doc.addEventListener('input', handleInput);
                
                return () => {
                    doc.removeEventListener('input', handleInput);
                };
            } catch (e) {
                console.error('MirrorPanel iframe error:', e);
            }
        };

        // Wait for iframe to load
        if (iframe.contentDocument?.readyState === 'complete') {
            setupIframe();
        } else {
            iframe.addEventListener('load', setupIframe);
            return () => {
                isMounted = false;
                clearTimeout(timeoutId);
                iframe.removeEventListener('load', setupIframe);
            };
        }

        return () => {
            isMounted = false;
            clearTimeout(timeoutId);
        };
    }, [srcDoc, onCodeChange, html]);

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
                        <Scaling className={cn("w-3 h-3 text-blue-500", isSyncing ? "animate-spin" : "animate-spin-slow")} />
                        <span className="text-[10px] font-mono text-zinc-300 tracking-tighter">
                            {isSyncing ? 'SYNCING...' : 'SYNC ACTIVE'}
                        </span>
                    </div>

                    <button
                        onClick={onExpand}
                        className="p-1.5 rounded-lg bg-white/5 border border-white/10 text-zinc-400 hover:text-white hover:bg-white/10 transition-all"
                        title="Vista Inmersiva"
                    >
                        <Scaling className="w-4 h-4" />
                    </button>
                </div>
            </div>

            <div className="flex-1 p-12 overflow-y-auto custom-scrollbar bg-black relative flex justify-center">
                {/* Visual Sync Flash/Scan Effect */}
                {(isSyncing || isGenerating) && (
                    <div className="absolute inset-0 z-20 pointer-events-none overflow-hidden">
                        <div className="absolute inset-0 bg-blue-500/5 backdrop-blur-[1px] animate-pulse" />
                        <div className="absolute top-0 left-0 w-full h-1 bg-blue-500 shadow-[0_0_20px_rgba(59,130,246,0.8)] animate-[scan_2s_ease-in-out_infinite]" />
                    </div>
                )}
                {/* Mirror Paper Container */}
                <div className="w-full max-w-[850px] bg-white rounded-sm shadow-[0_24px_80px_rgba(0,0,0,0.8)] border border-white/10 overflow-hidden h-fit transition-transform duration-500 hover:scale-[1.01]">
                    <iframe
                        ref={iframeRef}
                        title="Mirror View"
                        srcDoc={srcDoc}
                        className="w-full h-full border-none min-h-[1100px]"
                    />
                </div>

                {/* Decorative elements */}
                <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-blue-500/5 to-transparent pointer-events-none" />
            </div>

            {/* Grid Pattern Background */}
            <div className="absolute inset-0 pointer-events-none opacity-[0.05]"
                style={{ backgroundImage: 'radial-gradient(#fff 1px, transparent 1px)', backgroundSize: '32px 32px' }}
            />
        </div>
    );
};
