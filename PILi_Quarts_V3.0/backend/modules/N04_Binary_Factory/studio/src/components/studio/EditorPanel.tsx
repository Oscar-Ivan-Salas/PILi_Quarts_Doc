import React from 'react';
import Editor from '@monaco-editor/react';

interface EditorPanelProps {
    code: string;
    onChange: (value: string | undefined) => void;
}

export const EditorPanel: React.FC<EditorPanelProps> = ({ code, onChange }) => {
    return (
        <div className="flex-1 flex flex-col h-full bg-black/40 overflow-hidden relative border-r border-white/5">
            <div className="px-6 py-3 bg-gradient-to-r from-zinc-950/80 to-black/40 border-b border-white/5 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <div className="w-1.5 h-4 bg-blue-500 rounded-full" />
                    <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-[0.2em] font-mono">Source Editor</span>
                </div>
                <div className="flex gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full bg-zinc-800" />
                    <div className="w-2.5 h-2.5 rounded-full bg-zinc-800" />
                    <div className="w-2.5 h-2.5 rounded-full bg-zinc-800" />
                </div>
            </div>
            <div className="flex-1 overflow-hidden">
                <Editor
                    height="100%"
                    defaultLanguage="html"
                    theme="vs-dark"
                    value={code}
                    onChange={onChange}
                    options={{
                        minimap: { enabled: false },
                        fontSize: 14,
                        lineNumbers: "on",
                        roundedSelection: true,
                        scrollBeyondLastLine: false,
                        readOnly: false,
                        automaticLayout: true,
                        padding: { top: 24, bottom: 24 },
                        fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
                        smoothScrolling: true,
                        cursorBlinking: "smooth",
                        cursorSmoothCaretAnimation: "on",
                    }}
                />
            </div>
        </div>
    );
};
