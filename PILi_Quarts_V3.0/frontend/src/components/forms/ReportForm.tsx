/**
 * ReportForm - Form for Report Documents
 * Handles editing of technical and executive reports sections
 */
import { FileText, AlignLeft, List, CheckCircle } from 'lucide-react';
import { useDocumentStore } from '../../store/useDocumentStore';

export function ReportForm() {
    const { documentData, updateData } = useDocumentStore();

    const updateField = (field: string, value: string) => {
        updateData({ [field]: value });
    };

    const updateProject = (field: string, value: string) => {
        updateData({
            proyecto: {
                ...documentData.proyecto,
                [field]: value
            }
        });
    };

    const updateRecommendation = (index: number, value: string) => {
        const newRecommendations = [...(documentData.recomendaciones || [])];
        newRecommendations[index] = value;
        updateData({ recomendaciones: newRecommendations });
    };

    const addRecommendation = () => {
        updateData({
            recomendaciones: [...(documentData.recomendaciones || []), '']
        });
    };

    const removeRecommendation = (index: number) => {
        const newRecommendations = [...(documentData.recomendaciones || [])];
        newRecommendations.splice(index, 1);
        updateData({ recomendaciones: newRecommendations });
    };

    return (
        <div className="space-y-6 pb-20">
            {/* Información General */}
            <div className="space-y-4">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-2">
                    <FileText size={16} /> Información General
                </h3>
                <div className="grid gap-4">
                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Título del Informe</label>
                        <input
                            type="text"
                            value={documentData.proyecto.nombre}
                            onChange={(e) => updateProject('nombre', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Código</label>
                        <input
                            type="text"
                            value={documentData.codigo || ''}
                            onChange={(e) => updateField('codigo', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                            placeholder="INF-TEC-2024-001"
                        />
                    </div>
                </div>
            </div>

            {/* Secciones de Texto */}
            <div className="border-t pt-6 space-y-4">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-2">
                    <AlignLeft size={16} /> Contenido
                </h3>

                <div className="space-y-4">
                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Resumen Ejecutivo</label>
                        <textarea
                            value={documentData.proyecto.descripcion}
                            onChange={(e) => updateProject('descripcion', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none min-h-[100px]"
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Introducción</label>
                        <textarea
                            value={documentData.introduccion || ''}
                            onChange={(e) => updateField('introduccion', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none min-h-[100px]"
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Análisis Técnico</label>
                        <textarea
                            value={documentData.analisis_tecnico || ''}
                            onChange={(e) => updateField('analisis_tecnico', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none min-h-[150px]"
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-medium text-gray-600">Conclusiones</label>
                        <textarea
                            value={documentData.conclusiones || ''}
                            onChange={(e) => updateField('conclusiones', e.target.value)}
                            className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none min-h-[100px]"
                        />
                    </div>
                </div>
            </div>

            {/* Recomendaciones */}
            <div className="border-t pt-6 space-y-4">
                <div className="flex justify-between items-center">
                    <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-2">
                        <List size={16} /> Recomendaciones
                    </h3>
                    <button
                        onClick={addRecommendation}
                        className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded hover:bg-blue-100 transition-colors"
                    >
                        + Añadir
                    </button>
                </div>

                <div className="space-y-2">
                    {(documentData.recomendaciones || []).map((rec, index) => (
                        <div key={index} className="flex gap-2 items-start">
                            <CheckCircle size={14} className="mt-2 text-green-500 flex-shrink-0" />
                            <textarea
                                value={rec}
                                onChange={(e) => updateRecommendation(index, e.target.value)}
                                className="w-full text-sm p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none min-h-[60px]"
                                placeholder="Escribe una recomendación..."
                            />
                            <button
                                onClick={() => removeRecommendation(index)}
                                className="mt-2 text-gray-400 hover:text-red-500 flex-shrink-0"
                            >
                                ×
                            </button>
                        </div>
                    ))}
                    {(documentData.recomendaciones?.length === 0) && (
                        <p className="text-xs text-gray-400 text-center py-4">No hay recomendaciones</p>
                    )}
                </div>
            </div>
        </div>
    );
}
