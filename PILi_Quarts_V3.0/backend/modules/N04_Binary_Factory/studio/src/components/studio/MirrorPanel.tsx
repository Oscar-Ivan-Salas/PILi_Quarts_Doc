import React, { useEffect, useRef } from 'react';
import { Monitor, Scaling } from 'lucide-react';

interface MirrorPanelProps {
    html: string;
    overrides: {
        logo: string | null;
        primaryColor: string;
        secondaryColor: string;
        fontFamily: string;
        fontSize: string;
        data: Record<string, string>;
    };
}

export const MirrorPanel: React.FC<MirrorPanelProps> = ({ html, overrides }) => {
    const iframeRef = useRef<HTMLIFrameElement>(null);

    useEffect(() => {
        if (iframeRef.current) {
            const doc = iframeRef.current.contentDocument;
            if (doc) {
                doc.open();

                // Inyección de variables CSS y Logo
                const styleBlock = `
          <style>
            :root {
              --pili-primary: ${overrides.primaryColor};
              --pili-secondary: ${overrides.secondaryColor};
              --pili-font: ${overrides.fontFamily}, sans-serif;
            }
            body { font-family: var(--pili-font) !important; }
            .pili-logo { content: url("${overrides.logo || ''}") !important; }
            .dynamic-primary { color: var(--pili-primary) !important; }
            .dynamic-bg-primary { background-color: var(--pili-primary) !important; }
          </style>
        `;

                // Procesar HTML para reemplazar placeholdes de datos {{TAG}}
                let processedHtml = html;
                Object.entries(overrides.data).forEach(([key, value]) => {
                    const regex = new RegExp(`{{${key}.*?}}`, 'g'); // Soporta filtros jinja |default
                    processedHtml = processedHtml.replace(regex, value);
                });

                const hasDoctype = processedHtml.trim().toLowerCase().startsWith('<!doctype');
                const content = hasDoctype
                    ? processedHtml.replace('</head>', `${styleBlock}</head>`)
                    : `<!DOCTYPE html>\n<html><head>${styleBlock}</head><body>${processedHtml}</body></html>`;

                doc.write(content);
                doc.close();
            }
        }
    }, [html, overrides]);

    return (
        <div className="flex-1 flex flex-col h-full bg-[#050505] overflow-hidden relative">
            <div className="px-6 py-3 bg-black/60 backdrop-blur-md border-b border-white/5 flex items-center justify-between z-10">
                <div className="flex items-center gap-3">
                    <Monitor className="w-4 h-4 text-blue-500" />
                    <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-widest">Espejo de Soberanía</span>
                </div>
                <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900 border border-white/5">
                    <Scaling className="w-3 h-3 text-zinc-600" />
                    <span className="text-[10px] font-mono text-zinc-500">REALTIME SYNC</span>
                </div>
            </div>

            <div className="flex-1 p-12 overflow-y-auto custom-scrollbar bg-black relative flex justify-center">
                {/* Mirror Paper Container */}
                <div className="w-full max-w-[850px] bg-white rounded-sm shadow-[0_24px_80px_rgba(0,0,0,0.8)] border border-white/10 overflow-hidden h-fit transition-transform duration-500 hover:scale-[1.01]">
                    <iframe
                        ref={iframeRef}
                        title="Mirror View"
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
