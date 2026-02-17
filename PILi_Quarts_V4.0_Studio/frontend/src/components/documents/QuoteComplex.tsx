/**
 * QuoteComplex - Complex Quote Document
 * Extended version with detailed breakdown
 */
import { QuoteSimple } from './QuoteSimple';
import type { DocumentData, ColorScheme } from '../../store/useDocumentStore';

interface QuoteComplexProps {
    data?: Partial<DocumentData>;
    colorScheme?: ColorScheme;
    logo?: string | null;
    font?: string;
    onDataChange?: (data: DocumentData) => void;
}

export function QuoteComplex(props: QuoteComplexProps) {
    // For now, use QuoteSimple as base (can be extended later)
    return <QuoteSimple {...props} />;
}
