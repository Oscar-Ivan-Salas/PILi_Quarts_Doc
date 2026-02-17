/**
 * ProjectComplex - Complex Project Document
 * Extended version with phases, risks, stakeholders
 */
import { ProjectSimple } from './ProjectSimple';
import type { DocumentData, ColorScheme } from '../../store/useDocumentStore';

interface ProjectComplexProps {
    data?: Partial<DocumentData>;
    colorScheme?: ColorScheme;
    logo?: string | null;
    font?: string;
    onDataChange?: (data: DocumentData) => void;
}

export function ProjectComplex(props: ProjectComplexProps) {
    // For now, use ProjectSimple as base (can be extended later)
    return <ProjectSimple {...props} />;
}
