/**
 * DocumentPreview - Universal Document Renderer
 * 
 * Renders any document type based on documentType prop
 * Supports all 6 document types:
 * - proyecto-simple
 * - proyecto-complejo
 * - cotizacion-simple
 * - cotizacion-compleja
 * - informe-tecnico
 * - informe-ejecutivo
 */
import { ProjectSimple } from '../documents/ProjectSimple';
import { useDocumentStore, type DocumentType } from '../../store/useDocumentStore';

interface DocumentPreviewProps {
    documentType?: DocumentType;
}

export function DocumentPreview({ documentType }: DocumentPreviewProps) {
    const { documentData, colorScheme, logo, font } = useDocumentStore();

    // Use prop or store value
    const type = documentType || useDocumentStore((state) => state.documentType);

    const renderDocument = () => {
        switch (type) {
            case 'proyecto-simple':
                return (
                    <ProjectSimple
                        data={documentData}
                        colorScheme={colorScheme}
                        logo={logo}
                        font={font}
                    />
                );

            case 'proyecto-complejo':
                return (
                    <div className="p-8 text-center text-gray-500">
                        <p>Proyecto Complejo - En desarrollo</p>
                    </div>
                );

            case 'cotizacion-simple':
                return (
                    <div className="p-8 text-center text-gray-500">
                        <p>Cotización Simple - En desarrollo</p>
                    </div>
                );

            case 'cotizacion-compleja':
                return (
                    <div className="p-8 text-center text-gray-500">
                        <p>Cotización Compleja - En desarrollo</p>
                    </div>
                );

            case 'informe-tecnico':
                return (
                    <div className="p-8 text-center text-gray-500">
                        <p>Informe Técnico - En desarrollo</p>
                    </div>
                );

            case 'informe-ejecutivo':
                return (
                    <div className="p-8 text-center text-gray-500">
                        <p>Informe Ejecutivo - En desarrollo</p>
                    </div>
                );

            default:
                return (
                    <div className="p-8 text-center text-gray-500">
                        <p>Selecciona un tipo de documento</p>
                    </div>
                );
        }
    };

    return (
        <div className="document-preview bg-white dark:bg-gray-900 rounded-lg shadow-lg overflow-hidden">
            {renderDocument()}
        </div>
    );
}
