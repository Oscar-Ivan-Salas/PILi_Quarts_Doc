/**
 * DocumentEditor Page
 * 
 * Main page for document creation and editing
 * Uses ThreePanelLayout with:
 * - Left: Forms
 * - Center: Document Preview
 * - Right: PILI Chat
 */
import { ThreePanelLayout } from '../components/layout/ThreePanelLayout';
import { DocumentPreview } from '../components/preview/DocumentPreview';
import { PILIChat } from '../components/pili/PILIChat';
import { useDocumentStore } from '../store/useDocumentStore';

export function DocumentEditor() {
    const { documentType } = useDocumentStore();

    return (
        <ThreePanelLayout
            leftPanel={
                <div className="p-4">
                    <h3 className="text-lg font-bold mb-4">Formulario</h3>
                    <p className="text-sm text-gray-600">Formularios en desarrollo...</p>
                </div>
            }
            centerPanel={<DocumentPreview documentType={documentType} />}
            rightPanel={<PILIChat chatType="electricidad" />}
            leftTitle="📋 Configuración"
            centerTitle="📄 Vista Previa"
            rightTitle="🤖 PILI AI"
        />
    );
}
