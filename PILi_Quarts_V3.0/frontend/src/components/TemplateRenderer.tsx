import { useEffect, useState } from 'react';

interface TemplateRendererProps {
    tipo: string;
    data: any;
    editable?: boolean;
    onDataChange?: (newData: any) => void;
}

/**
 * TemplateRenderer - Carga plantillas HTML de N04 y las rellena con datos dinámicos
 * 
 * Flujo:
 * 1. Carga plantilla HTML desde backend (/api/templates/{tipo})
 * 2. Reemplaza placeholders {{VARIABLE}} con datos reales
 * 3. Renderiza HTML con clases CSS que TeslaExcelConverter entiende
 */
export function TemplateRenderer({ tipo, data, editable = false, onDataChange }: TemplateRendererProps) {
    const [html, setHtml] = useState<string>('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadAndFillTemplate();
    }, [tipo, data]);

    const loadAndFillTemplate = async () => {
        try {
            setLoading(true);
            setError(null);

            // 1. Cargar plantilla de N04
            console.log(`📄 Cargando plantilla: ${tipo}`);
            const response = await fetch(`http://localhost:8005/api/templates/${tipo}`);

            if (!response.ok) {
                throw new Error(`Error loading template: ${response.statusText}`);
            }

            const result = await response.json();
            let htmlContent = result.html;

            console.log(`✅ Plantilla cargada: ${result.archivo} (${htmlContent.length} caracteres)`);

            // 2. Reemplazar placeholders con datos reales
            htmlContent = fillPlaceholders(htmlContent, data);

            setHtml(htmlContent);
            setLoading(false);

        } catch (err) {
            console.error('❌ Error loading template:', err);
            setError(err instanceof Error ? err.message : 'Unknown error');
            setLoading(false);
        }
    };

    const fillPlaceholders = (template: string, datos: any): string => {
        if (!datos) return template;

        let filled = template;

        // Crear objeto de reemplazos
        const replacements: Record<string, string> = {
            // === EMISOR ===
            'NOMBRE_EMISOR': datos.emisor?.nombre || 'SIN NOMBRE',
            'RUC_EMISOR': datos.emisor?.ruc || '00000000000',
            'DIRECCION_EMISOR': datos.emisor?.direccion || 'Sin dirección',
            'EMAIL_EMISOR': datos.emisor?.email || 'sin@email.com',
            'TELEFONO_EMISOR': datos.emisor?.telefono || 'Sin teléfono',
            'EMPRESA_EMISOR': datos.emisor?.empresa || datos.emisor?.nombre || 'SIN EMPRESA',

            // === CLIENTE ===
            'CLIENTE_NOMBRE': datos.cliente?.nombre || 'SIN CLIENTE',
            'CLIENTE_RUC': datos.cliente?.ruc || '',
            'CLIENTE_DIRECCION': datos.cliente?.direccion || '',
            'CLIENTE_EMAIL': datos.cliente?.email || '',

            // === DOCUMENTO ===
            'NUMERO_COTIZACION': datos.numero || `COT-${new Date().getFullYear()}-${Math.floor(Math.random() * 1000)}`,
            'CODIGO_COTIZACION': datos.codigo || datos.numero || 'COT-0001',
            'FECHA_COTIZACION': datos.fecha || new Date().toLocaleDateString('es-PE'),
            'FECHA': datos.fecha || new Date().toLocaleDateString('es-PE'),

            // === PROYECTO ===
            'PROYECTO_NOMBRE': datos.proyecto?.nombre || datos.nombre || 'SIN NOMBRE',
            'AREA_M2': datos.area || datos.proyecto?.area || '0',
            'DESCRIPCION_PROYECTO': datos.descripcion || datos.proyecto?.descripcion || 'Sin descripción',

            // === SERVICIO ===
            'SERVICIO_NOMBRE': datos.servicio?.nombre || 'SERVICIO ELÉCTRICO',
            'VIGENCIA': datos.vigencia || '15 Días',
            'VALIDEZ': datos.vigencia || '15 Días',

            // === TOTALES ===
            'SUBTOTAL': formatCurrency(datos.subtotal || 0),
            'IGV': formatCurrency(datos.igv || (datos.subtotal || 0) * 0.18),
            'TOTAL': formatCurrency(datos.total || (datos.subtotal || 0) * 1.18),

            // === NORMATIVA ===
            'NORMATIVA_APLICABLE': datos.normativa || 'CNE Suministro 2011',
        };

        // Reemplazar todos los placeholders
        for (const [key, value] of Object.entries(replacements)) {
            const regex = new RegExp(`{{${key}}}`, 'g');
            filled = filled.replace(regex, value);
        }

        // Reemplazar items de tabla (si existen)
        if (datos.suministros && Array.isArray(datos.suministros)) {
            filled = fillTableItems(filled, datos.suministros);
        }

        return filled;
    };

    const fillTableItems = (template: string, items: any[]): string => {
        // Buscar sección de tabla y reemplazar con items reales
        // Por ahora retornar template sin cambios
        // TODO: Implementar lógica de reemplazo de items
        return template;
    };

    const formatCurrency = (value: number): string => {
        return value.toLocaleString('es-PE', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center p-12">
                <div className="text-gray-400">Cargando plantilla...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center p-12">
                <div className="text-red-400">Error: {error}</div>
            </div>
        );
    }

    return (
        <div
            className="template-container"
            dangerouslySetInnerHTML={{ __html: html }}
            suppressContentEditableWarning
            contentEditable={editable}
            onBlur={(e) => {
                if (editable && onDataChange) {
                    // Capturar cambios y actualizar datos
                    // TODO: Implementar sincronización de cambios
                }
            }}
        />
    );
}
