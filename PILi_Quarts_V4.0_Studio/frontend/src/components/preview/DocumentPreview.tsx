/**
 * DocumentPreview - Universal Document Renderer
 * Renders all 6 document types
 */
import { ProjectSimple } from '../documents/ProjectSimple';
import { ProjectComplex } from '../documents/ProjectComplex';
import { QuoteSimple } from '../documents/QuoteSimple';
import { QuoteComplex } from '../documents/QuoteComplex';
import { ReportTechnical } from '../documents/ReportTechnical';
import { ReportExecutive } from '../documents/ReportExecutive';
import { useDocumentStore, type DocumentType } from '../../store/useDocumentStore';

interface DocumentPreviewProps {
    documentType?: DocumentType;
}

export function DocumentPreview({ documentType }: DocumentPreviewProps) {
    const { documentData, colorScheme, logo, font } = useDocumentStore();
    const type = documentType || useDocumentStore((state) => state.documentType);

    const commonProps = { data: documentData, colorScheme, logo, font };

    const renderDocument = () => {
        switch (type) {
            case 'proyecto-simple':
                return <ProjectSimple {...commonProps} />;
            case 'proyecto-complejo':
                return <ProjectComplex {...commonProps} />;
            case 'cotizacion-simple':
                return <QuoteSimple {...commonProps} />;
            case 'cotizacion-compleja':
                return <QuoteComplex {...commonProps} />;
            case 'informe-tecnico':
                return <ReportTechnical {...commonProps} />;
            case 'informe-ejecutivo':
                return <ReportExecutive {...commonProps} />;
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
