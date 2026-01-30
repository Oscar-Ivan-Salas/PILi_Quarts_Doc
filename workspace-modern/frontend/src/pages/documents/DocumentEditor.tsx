/**
 * DocumentEditor - Main Page
 * Integrates Layout, Forms, Preview, and Chat
 */
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { ThreePanelLayout } from '../../components/layout/ThreePanelLayout';
import { DocumentPreview } from '../../components/preview/DocumentPreview';
import { PILIChat } from '../../components/pili/PILIChat';
import { ProjectForm } from '../../components/forms/ProjectForm';
import { QuoteForm } from '../../components/forms/QuoteForm';
import { ReportForm } from '../../components/forms/ReportForm';
import { useDocumentStore } from '../../store/useDocumentStore';
import { Save, Download, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export function DocumentEditor() {
    const { id } = useParams();
    const {
        documentType,
        setDocumentType,
        fetchDocument,
        saveDocument,
        isSaving,
        lastSaved,
        resetDocument
    } = useDocumentStore();

    // Load document if ID is provided
    useEffect(() => {
        if (id) {
            fetchDocument(parseInt(id));
        } else {
            resetDocument();
        }
    }, [id]);

    const handleSave = async () => {
        await saveDocument('user-123', 'Nuevo Documento'); // TODO: Get user ID and handle title
    };

    const renderForm = () => {
        switch (documentType) {
            case 'proyecto-simple':
            case 'proyecto-complejo':
                return <ProjectForm />;
            case 'cotizacion-simple':
            case 'cotizacion-compleja':
                return <QuoteForm />;
            case 'informe-tecnico':
            case 'informe-ejecutivo':
                return <ReportForm />;
            default:
                return <ProjectForm />;
        }
    };

    return (
        <div className="h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
            {/* Header */}
            <header className="h-14 bg-white dark:bg-gray-800 border-b flex items-center justify-between px-4 sticky top-0 z-10">
                <div className="flex items-center gap-4">
                    <Link to="/" className="p-2 hover:bg-gray-100 rounded-full dark:hover:bg-gray-700">
                        <ArrowLeft size={20} className="text-gray-600 dark:text-gray-300" />
                    </Link>
                    <h1 className="font-semibold text-gray-800 dark:text-white">
                        {id ? 'Editar Documento' : 'Nuevo Documento'}
                    </h1>
                    {lastSaved && (
                        <span className="text-xs text-green-600 flex items-center gap-1">
                            • Guardado {lastSaved.toLocaleTimeString()}
                        </span>
                    )}
                </div>

                <div className="flex items-center gap-2">
                    <button
                        onClick={handleSave}
                        disabled={isSaving}
                        className="flex items-center gap-2 px-3 py-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition disabled:opacity-50"
                    >
                        <Save size={16} />
                        {isSaving ? 'Guardando...' : 'Guardar'}
                    </button>

                    <button className="flex items-center gap-2 px-3 py-1.5 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600">
                        <Download size={16} />
                        Exportar
                    </button>
                </div>
            </header>

            {/* Main Layout */}
            <div className="flex-1 overflow-hidden">
                <ThreePanelLayout
                    leftPanel={
                        <div className="h-full flex flex-col">
                            <div className="p-4 border-b bg-gray-50 dark:bg-gray-800">
                                <h2 className="font-semibold text-gray-700 dark:text-gray-200">Editor</h2>
                                <select
                                    value={documentType}
                                    onChange={(e) => setDocumentType(e.target.value as any)}
                                    className="mt-2 w-full p-2 text-sm border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
                                >
                                    <option value="proyecto-simple">Proyecto Simple</option>
                                    <option value="cotizacion-simple">Cotización Simple</option>
                                    <option value="informe-tecnico">Informe Técnico</option>
                                    <option value="proyecto-complejo">Proyecto Complejo</option>
                                    <option value="cotizacion-compleja">Cotización Compleja</option>
                                    <option value="informe-ejecutivo">Informe Ejecutivo</option>
                                </select>
                            </div>
                            <div className="flex-1 overflow-y-auto p-4 scrollbar-thin">
                                {renderForm()}
                            </div>
                        </div>
                    }
                    centerPanel={
                        <div className="h-full bg-gray-100 dark:bg-gray-900 overflow-y-auto p-8 flex justify-center scrollbar-thin">
                            <DocumentPreview />
                        </div>
                    }
                    rightPanel={
                        <PILIChat
                            chatType={
                                documentType.includes('proyecto') ? 'project_assistant' :
                                    documentType.includes('cotizacion') ? 'quote_generator' : 'technical_writer'
                            }
                            onExtractData={(data) => {
                                // Handle AI extracted data
                                console.log('Extracted:', data);
                            }}
                        />
                    }
                    defaultLeftWidth={350}
                    defaultRightWidth={380}
                />
            </div>
        </div>
    );
}
