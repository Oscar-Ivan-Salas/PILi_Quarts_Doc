
import React from 'react';

const ProyectoResumen = ({ datos, fases = [], usarDiasHabiles }) => {

    // Calcular duración total real basada en fases si existen
    const duracionReal = fases.length > 0
        ? fases.reduce((acc, f) => acc + (parseInt(f.duracion_dias) || 0), 0)
        : datos.duracion_dias;

    // Calcular fecha fin estimada basada en duración real
    // Nota: Para cálculo exacto de fecha fin requeriría la utilidad de fechas, 
    // pero por ahora podemos usar la del calendario o una aproximación visual si cambia mucho.
    // Para simplificar, si la duración cambia por fases, idealmente el backend recalcula fechas.
    // Aquí mostraremos la duración sumada.

    // Si la duración real difiere de la calculada inicialmente, mostrar advertencia o color
    const esDiferente = duracionReal !== datos.duracion_dias;

    return (
        <div className="bg-gradient-to-br from-blue-950 to-gray-900 rounded-xl p-5 border border-blue-800 shadow-lg animate-fadeIn">
            <h4 className="text-xl font-bold text-white mb-4 border-b border-blue-800 pb-2 flex items-center justify-between">
                📊 Resumen del Proyecto
                {esDiferente && (
                    <span className="text-xs bg-yellow-600 text-white px-2 py-1 rounded-full animate-pulse">
                        Modificado
                    </span>
                )}
            </h4>

            <div className="space-y-4">
                <div className="flex justify-between items-center bg-gray-900/50 p-3 rounded-lg border border-gray-800">
                    <span className="text-gray-400 font-medium">📅 Fecha de Inicio:</span>
                    <span className="text-white font-bold text-lg">{datos.fecha_inicio}</span>
                </div>

                <div className="flex justify-between items-center bg-gray-900/50 p-3 rounded-lg border border-gray-800">
                    <span className="text-gray-400 font-medium">🏁 Fecha de Fin:</span>
                    {/* Si tenemos fases, la fecha fin debería venir del último elemento de fases si está ordenado, o del cálculo global */}
                    <span className="text-white font-bold text-lg">{datos.fecha_fin}</span>
                </div>

                <div className="border-t border-gray-700 my-2"></div>

                <div className={`flex justify-between items-center p-3 rounded-lg border ${esDiferente ? 'bg-blue-900/40 border-blue-500' : 'bg-gray-900/50 border-gray-800'}`}>
                    <span className="text-gray-300 font-medium">📆 Duración Total:</span>
                    <div className="text-right">
                        <span className={`font-bold text-2xl ${esDiferente ? 'text-yellow-400' : 'text-blue-400'}`}>
                            {duracionReal} días
                        </span>
                        {esDiferente && (
                            <p className="text-xs text-blue-300">Personalizada (Original: {datos.duracion_dias})</p>
                        )}
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                    <div className="bg-gray-900/30 p-2 rounded border border-gray-800">
                        <span className="block text-xs text-gray-500 mb-1">Horas Totales</span>
                        <span className="block text-white font-semibold">{Math.round(duracionReal * 8)} hrs</span>
                    </div>
                    <div className="bg-gray-900/30 p-2 rounded border border-gray-800">
                        <span className="block text-xs text-gray-500 mb-1">Jornada</span>
                        <span className="block text-white font-semibold">8 hrs/día</span>
                    </div>
                </div>

                <div className="border-t border-gray-700 my-2"></div>

                <div className="flex justify-between items-center">
                    <span className="text-gray-400 text-sm">Modo Cálculo:</span>
                    <span className="text-blue-300 text-sm font-medium border border-blue-900 px-2 py-1 rounded bg-blue-950/30">
                        {usarDiasHabiles ? '📅 Días Hábiles' : '📆 Días Calendario'}
                    </span>
                </div>
            </div>

            {/* Leyenda Compacta */}
            <div className="mt-4 pt-3 border-t border-gray-800 flex justify-center gap-4 text-xs">
                <div className="flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-green-500/50"></span>
                    <span className="text-gray-500">Hábil</span>
                </div>
                <div className="flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-gray-700"></span>
                    <span className="text-gray-500">FinDeSem</span>
                </div>
                <div className="flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-red-500/50"></span>
                    <span className="text-gray-500">Feriado</span>
                </div>
            </div>
        </div>
    );
};

export default ProyectoResumen;
