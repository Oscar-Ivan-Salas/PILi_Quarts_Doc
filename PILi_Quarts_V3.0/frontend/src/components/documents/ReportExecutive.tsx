/**
 * ReportExecutive - Executive Report Document
 * High-level summary for executives
 */
import { ReportTechnical } from './ReportTechnical';
import type { DocumentData, ColorScheme } from '../../store/useDocumentStore';

interface ReportExecutiveProps {
    data?: Partial<DocumentData>;
    colorScheme?: ColorScheme;
    logo?: string | null;
    font?: string;
    onDataChange?: (data: DocumentData) => void;
}

export function ReportExecutive(props: ReportExecutiveProps) {
    // For now, use ReportTechnical as base (can be extended later)
    return <ReportTechnical {...props} />;
}
