import React, { useMemo } from 'react';
import { FileText, Calendar, Users, Package } from 'lucide-react';

/**
 * VistaPreviaEnTiempoReal - Vista previa del documento que se actualiza en tiempo real
 * 
 * Muestra el documento final mientras el usuario edita el formulario
 */
const VistaPreviaEnTiempoReal = ({ datosProyecto, fases = [] }) => {
    // Calcular fecha fin estimada
    const fechaFinEstimada = useMemo(() => {
        if (!datosProyecto.fecha_inicio || !fases.length) return null;

        const fechaInicio = new Date(datosProyecto.fecha_inicio);
        const totalDias = fases.reduce((acc, f) => acc + (f.duracion || 0), 0);
        const fechaFin = new Date(fechaInicio);
        fechaFin.setDate(fechaFin.getDate() + totalDias);

        return fechaFin.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    }, [datosProyecto.fecha_inicio, fases]);

    const formatearFecha = (fecha) => {
        if (!fecha) return '-';
        const date = new Date(fecha);
        return date.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    };

    return (
        <div className="max-w-4xl mx-auto bg-white text-gray-900 shadow-2xl rounded-lg overflow-hidden">
            {/* Portada */}
            <div className="bg-gradient-to-br from-red-600 to-red-800 text-white p-12 text-center">
                <div className="mb-4">
                    <FileText className="w-16 h-16 mx-auto mb-4" />
                </div>
                <h1 className="text-4xl font-bold mb-4">
                    {datosProyecto.nombre_proyecto || 'Nombre del Proyecto'}
                </h1>
                <div className="text-xl opacity-90">
                    Sistema de Gestión de Documentos Técnicos Profesional
                </div>
                <div className="mt-8 text-sm opacity-75">
                    PILi_Quarts - Generado el {new Date().toLocaleDateString('es-ES')}
                </div>
            </div>

            {/* Contenido del Documento */}
            <div className="p-8 space-y-8">
                {/* 1. Resumen Ejecutivo */}
                <section>
                    <h2 className="text-2xl font-bold text-red-900 mb-4 pb-2 border-b-2 border-red-600">
                        1. Resumen Ejecutivo
                    </h2>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span className="font-semibold text-gray-700">Proyecto:</span>
                            <p className="text-gray-900">{datosProyecto.nombre_proyecto || '-'}</p>
                        </div>
                        <div>
                            <span className="font-semibold text-gray-700">Cliente:</span>
                            <p className="text-gray-900">{datosProyecto.cliente?.nombre || '-'}</p>
                        </div>
                        <div>
                            <span className="font-semibold text-gray-700">Presupuesto:</span>
                            <p className="text-gray-900">
                                {datosProyecto.moneda || 'USD'} {datosProyecto.presupuesto?.toLocaleString() || '-'}
                            </p>
                        </div>
                        <div>
                            <span className="font-semibold text-gray-700">Duración:</span>
                            <p className="text-gray-900">
                                {fases.reduce((acc, f) => acc + (f.duracion || 0), 0)} días laborables
                            </p>
                        </div>
                    </div>
                </section>

                {/* 2. Datos del Cliente */}
                {datosProyecto.cliente && (
                    <section>
                        <h2 className="text-2xl font-bold text-red-900 mb-4 pb-2 border-b-2 border-red-600 flex items-center gap-2">
                            <Users className="w-6 h-6" />
                            2. Datos del Cliente
                        </h2>
                        <div className="bg-gray-50 p-4 rounded-lg space-y-2 text-sm">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <span className="font-semibold text-gray-700">Razón Social:</span>
                                    <p className="text-gray-900">{datosProyecto.cliente.nombre || '-'}</p>
                                </div>
                                <div>
                                    <span className="font-semibold text-gray-700">RUC/NIT:</span>
                                    <p className="text-gray-900">{datosProyecto.cliente.ruc || '-'}</p>
                                </div>
                                <div>
                                    <span className="font-semibold text-gray-700">Email:</span>
                                    <p className="text-gray-900">{datosProyecto.cliente.email || '-'}</p>
                                </div>
                                <div>
                                    <span className="font-semibold text-gray-700">Teléfono:</span>
                                    <p className="text-gray-900">{datosProyecto.cliente.telefono || '-'}</p>
                                </div>
                            </div>
                            <div>
                                <span className="font-semibold text-gray-700">Dirección:</span>
                                <p className="text-gray-900">{datosProyecto.cliente.direccion || '-'}</p>
                            </div>
                        </div>
                    </section>
                )}

                {/* 3. Cronograma Preliminar */}
                {fases.length > 0 && (
                    <section>
                        <h2 className="text-2xl font-bold text-red-900 mb-4 pb-2 border-b-2 border-red-600 flex items-center gap-2">
                            <Calendar className="w-6 h-6" />
                            3. Cronograma Preliminar
                        </h2>
                        <div className="mb-4 grid grid-cols-2 gap-4 text-sm bg-yellow-50 p-4 rounded-lg">
                            <div>
                                <span className="font-semibold text-gray-700">Fecha de Inicio:</span>
                                <p className="text-gray-900">{formatearFecha(datosProyecto.fecha_inicio)}</p>
                            </div>
                            <div>
                                <span className="font-semibold text-gray-700">Fecha Estimada de Fin:</span>
                                <p className="text-gray-900">{fechaFinEstimada || '-'}</p>
                            </div>
                        </div>

                        <table className="w-full text-sm border-collapse">
                            <thead>
                                <tr className="bg-red-900 text-white">
                                    <th className="border border-red-800 p-2 text-left">Fase</th>
                                    <th className="border border-red-800 p-2 text-left">Nombre</th>
                                    <th className="border border-red-800 p-2 text-center">Duración (días)</th>
                                    <th className="border border-red-800 p-2 text-center">% del Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                {fases.map((fase, index) => {
                                    const totalDias = fases.reduce((acc, f) => acc + (f.duracion || 0), 0);
                                    const porcentaje = totalDias > 0 ? ((fase.duracion / totalDias) * 100).toFixed(1) : 0;

                                    return (
                                        <tr key={fase.id} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                                            <td className="border border-gray-300 p-2 font-semibold">Fase {fase.id}</td>
                                            <td className="border border-gray-300 p-2">{fase.nombre}</td>
                                            <td className="border border-gray-300 p-2 text-center font-bold text-red-700">
                                                {fase.duracion}
                                            </td>
                                            <td className="border border-gray-300 p-2 text-center">
                                                <div className="flex items-center gap-2">
                                                    <div className="flex-1 bg-gray-200 rounded-full h-2 overflow-hidden">
                                                        <div
                                                            className="bg-red-600 h-full transition-all duration-300"
                                                            style={{ width: `${porcentaje}%` }}
                                                        />
                                                    </div>
                                                    <span className="text-xs font-semibold w-12 text-right">{porcentaje}%</span>
                                                </div>
                                            </td>
                                        </tr>
                                    );
                                })}
                                <tr className="bg-red-100 font-bold">
                                    <td colSpan="2" className="border border-gray-300 p-2 text-right">TOTAL:</td>
                                    <td className="border border-gray-300 p-2 text-center text-red-900">
                                        {fases.reduce((acc, f) => acc + (f.duracion || 0), 0)} días
                                    </td>
                                    <td className="border border-gray-300 p-2 text-center">100%</td>
                                </tr>
                            </tbody>
                        </table>
                    </section>
                )}

                {/* 4. Requisitos Técnicos (Placeholder) */}
                <section>
                    <h2 className="text-2xl font-bold text-red-900 mb-4 pb-2 border-b-2 border-red-600 flex items-center gap-2">
                        <Package className="w-6 h-6" />
                        4. Requisitos Técnicos
                    </h2>
                    <div className="bg-gray-50 p-4 rounded-lg text-sm text-gray-600 italic">
                        Los requisitos técnicos se completarán durante la fase de análisis con PILI.
                    </div>
                </section>
            </div>

            {/* Footer */}
            <div className="bg-gray-100 p-6 text-center text-sm text-gray-600 border-t-2 border-red-600">
                <p className="font-bold text-red-900 text-lg mb-2">PILi_Quarts</p>
                <p>Sistema de Gestión de Documentos Técnicos Profesional con IA</p>
                <p className="mt-2 text-xs">
                    Documento generado automáticamente - {new Date().toLocaleDateString('es-ES', {
                        day: '2-digit',
                        month: 'long',
                        year: 'numeric'
                    })}
                </p>
            </div>
        </div>
    );
};

export default VistaPreviaEnTiempoReal;
