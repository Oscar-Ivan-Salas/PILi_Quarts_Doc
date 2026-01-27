import React, { useState, useEffect } from 'react';
import { Calendar, Clock, CheckCircle, Settings, ChevronDown, ChevronUp } from 'lucide-react';

const FormularioGanttDiasPro = ({ onSubmit, datosCalendario, maxDuracion }) => {
    // Fases estándar PMI (7 fases)
    const [fases, setFases] = useState([
        { id: 1, nombre: 'Inicio', duracion: 5 },
        { id: 2, nombre: 'Planificación Detallada', duracion: 10 },
        { id: 3, nombre: 'Gestión de Riesgos y Calidad', duracion: 5 },
        { id: 4, nombre: 'Ingeniería y Diseño', duracion: 25 },
        { id: 5, nombre: 'Ejecución y Monitoreo', duracion: 45 },
        { id: 6, nombre: 'Pruebas Integrales (FAT/SAT)', duracion: 10 },
        { id: 7, nombre: 'Cierre y Lecciones Aprendidas', duracion: 5 }
    ]);

    // Configuración de Calendario
    const [mostrarConfigCalendario, setMostrarConfigCalendario] = useState(false);
    const [diasLaborables, setDiasLaborables] = useState({
        lun: true, mar: true, mie: true, jue: true, vie: true, sab: true, dom: false
    });
    const [horasPorDia, setHorasPorDia] = useState(8);

    const [fechaFinEstimada, setFechaFinEstimada] = useState(null);
    const [duracionTotal, setDuracionTotal] = useState(0);

    // Límite máximo
    const limiteDias = maxDuracion ? parseInt(maxDuracion) : 999;
    const excedeLimite = duracionTotal > limiteDias;

    // ✅ NUEVO: Pre-llenar con datos del calendario inicial
    useEffect(() => {
        if (datosCalendario) {
            // Pre-llenar días laborables si vienen del backend
            if (datosCalendario.dias_laborables && Array.isArray(datosCalendario.dias_laborables)) {
                const nuevosDias = {
                    lun: false, mar: false, mie: false, jue: false, vie: false, sab: false, dom: false
                };
                datosCalendario.dias_laborables.forEach(dia => {
                    if (nuevosDias.hasOwnProperty(dia)) {
                        nuevosDias[dia] = true;
                    }
                });
                setDiasLaborables(nuevosDias);
                console.log('✅ Días laborables pre-llenados:', nuevosDias);
            }

            // Pre-llenar horas por día
            if (datosCalendario.horas_dia) {
                setHorasPorDia(datosCalendario.horas_dia);
                console.log('✅ Horas por día pre-llenadas:', datosCalendario.horas_dia);
            }
        }
    }, [datosCalendario]);

    // ✅ ALGORITMO AUTO-FIT (Estilo MS Project)
    const ajustarFasesAlLimite = (limite) => {
        if (!limite || limite >= 999) return fases;

        console.log(`⚖️ Ajustando cronograma (Auto-Fit) a ${limite} días...`);

        // 1. Calcular proporciones originales
        const totalOriginal = fases.reduce((acc, f) => acc + f.duracion, 0);

        // 2. Escalar cada fase
        let sumaNueva = 0;
        const fasesAjustadas = fases.map(f => {
            const nuevaDuracion = Math.max(1, Math.floor((f.duracion / totalOriginal) * limite));
            sumaNueva += nuevaDuracion;
            return { ...f, duracion: nuevaDuracion };
        });

        // 3. Distribuir el remanente (por redondeo) a las fases más largas (Ejecución/Ingeniería)
        let remanente = limite - sumaNueva;

        if (remanente > 0) {
            // Priorizar fases más largas para asignar días extra
            const indicesPrioridad = [4, 3, 1, 5, 2, 6, 0]; // IDs 5(Ejecución), 4(Ingeniería), etc. (indices array: ID-1)

            let i = 0;
            while (remanente > 0 && i < indicesPrioridad.length) {
                const index = indicesPrioridad[i];
                if (fasesAjustadas[index]) {
                    fasesAjustadas[index].duracion += 1;
                    remanente -= 1;
                }
                i++;
            }
        }

        return fasesAjustadas;
    };

    // ✅ EFECTO: Ajuste inicial automático si hay límite definido
    useEffect(() => {
        const limite = maxDuracion ? parseInt(maxDuracion) : 999;
        const totalActual = fases.reduce((acc, f) => acc + f.duracion, 0);

        // Solo ajustar si la diferencia es significativa o si excede el límite
        // Y aseguramos que solo corra una vez si es necesario para no sobreescribir ediciones manuales posteriores
        if (limite < totalActual && limite > 0) {
            const fasesAjustadas = ajustarFasesAlLimite(limite);
            setFases(fasesAjustadas);
        }
    }, []); // Solo al montar (o podríamos depender de maxDuracion si cambia dinámicamente)

    // Actualizar cálculos
    useEffect(() => {
        const total = fases.reduce((acc, fase) => acc + fase.duracion, 0);
        setDuracionTotal(total);

        // Lógica de cálculo de fecha fin...
        if (datosCalendario?.fechaInicio || datosCalendario?.fecha_inicio) {
            // ✅ FIX: Manejo robusto de fechas (DD/MM/YYYY o ISO)
            const fechaStr = datosCalendario.fechaInicio || datosCalendario.fecha_inicio;
            let fecha;

            if (fechaStr.includes('/')) {
                const [dia, mes, anio] = fechaStr.split('/');
                fecha = new Date(`${anio}-${mes}-${dia}`); // Convertir a ISO
            } else {
                fecha = new Date(fechaStr);
            }

            // Validar si la fecha es válida
            if (isNaN(fecha.getTime())) {
                console.warn('⚠️ Fecha inválida en Gantt:', fechaStr);
                setFechaFinEstimada(null);
                return;
            }

            let diasAgregados = 0;
            const mapDias = ['dom', 'lun', 'mar', 'mie', 'jue', 'vie', 'sab'];
            const hayDiasLaborables = Object.values(diasLaborables).some(v => v);

            if (hayDiasLaborables) {
                let safetyCounter = 0;
                // Safety break: 5 años * 365 días = ~1825 iteraciones. 5000 es super seguro.
                while (diasAgregados < total && safetyCounter < 5000) {
                    fecha.setDate(fecha.getDate() + 1);
                    const diaSemana = fecha.getDay(); // 0-6
                    const keyDia = mapDias[diaSemana];

                    if (diasLaborables[keyDia]) {
                        diasAgregados++;
                    }
                    safetyCounter++;
                }

                if (safetyCounter >= 5000) {
                    console.error('❌ Loop infinito detectado en cálculo de fechas');
                }
                setFechaFinEstimada(fecha);
            } else {
                setFechaFinEstimada(null);
            }
        }
    }, [fases, datosCalendario, diasLaborables]);

    const handleDuracionChange = (id, nuevaDuracion) => {
        setFases(fases.map(f =>
            f.id === id ? { ...f, duracion: parseInt(nuevaDuracion) || 0 } : f
        ));
    };

    const toggleDia = (dia) => {
        setDiasLaborables(prev => ({ ...prev, [dia]: !prev[dia] }));
    };

    const handleSubmit = () => {
        if (excedeLimite) return;

        // Generar texto resumen del calendario
        const diasActivos = Object.entries(diasLaborables)
            .filter(([_, activo]) => activo)
            .map(([dia]) => dia.toUpperCase())
            .join('-');

        const resumen = fases.map(f => `${f.nombre}: ${f.duracion}d`).join(', ');

        // Detalles del calendario
        const configCalendarioTexto = `Calendario: ${diasActivos} (${horasPorDia}h/día)`;

        onSubmit({
            fases: fases,
            total: duracionTotal,
            fechaFin: fechaFinEstimada,
            textoResumen: resumen,
            configuracionCalendario: {
                diasLaborables: diasLaborables,
                horasPorDia: horasPorDia
            },
            textoCompleto: `${resumen}\n${configCalendarioTexto}`
        });
    };

    const diasPorSemana = Object.values(diasLaborables).filter(Boolean).length;

    return (
        <div className="bg-gray-900/95 p-6 rounded-2xl border border-blue-500/30 shadow-2xl w-full max-w-2xl animate-fadeIn backdrop-blur-xl">
            {/* Header con Configuración */}
            <div className="flex flex-col gap-4 mb-6 border-b border-blue-500/20 pb-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-500/20 rounded-lg">
                            <Calendar className="w-6 h-6 text-blue-400" />
                        </div>
                        <div>
                            <h3 className="text-xl font-bold text-white">Cronograma Maestro</h3>
                            <p className="text-xs text-blue-300">Configuración PMI Completa</p>
                        </div>
                    </div>

                    <button
                        onClick={() => setMostrarConfigCalendario(!mostrarConfigCalendario)}
                        className="flex items-center gap-2 px-3 py-1.5 bg-gray-800 hover:bg-gray-700 rounded-lg text-xs text-gray-300 border border-gray-600 transition-colors"
                    >
                        <Settings className="w-3 h-3" />
                        Configurar Calendario
                        {mostrarConfigCalendario ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                    </button>
                </div>

                {/* Panel Configuración Calendario */}
                {mostrarConfigCalendario && (
                    <div className="bg-gray-800/80 p-4 rounded-xl border border-blue-500/30 animate-slideDown">
                        <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
                            <Clock className="w-4 h-4 text-blue-400" />
                            Días y Horarios Laborables
                        </h4>

                        <div className="grid grid-cols-7 gap-2 mb-4">
                            {['lun', 'mar', 'mie', 'jue', 'vie', 'sab', 'dom'].map(dia => (
                                <button
                                    key={dia}
                                    onClick={() => toggleDia(dia)}
                                    className={`p-2 rounded-lg text-xs font-bold uppercase transition-all
                                        ${diasLaborables[dia]
                                            ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
                                            : 'bg-gray-700 text-gray-500 hover:bg-gray-600'}`}
                                >
                                    {dia}
                                </button>
                            ))}
                        </div>

                        <div className="flex items-center gap-4 text-sm text-gray-300">
                            <div className="flex items-center gap-2 bg-gray-900 px-3 py-1.5 rounded-lg border border-gray-600">
                                <span>Horas/Día:</span>
                                <input
                                    type="number"
                                    value={horasPorDia}
                                    onChange={(e) => setHorasPorDia(e.target.value)}
                                    className="w-12 bg-transparent text-white font-bold focus:outline-none text-center"
                                />
                            </div>
                            <span className="text-xs text-gray-500">Semana de {diasPorSemana * horasPorDia} horas</span>
                        </div>
                    </div>
                )}

                {/* ✅ NUEVO: Badge de Resumen de Calendario (Siempre visible si no está expandido) */}
                {!mostrarConfigCalendario && (
                    <div className="mt-2 bg-blue-900/20 border border-blue-500/20 rounded-lg p-2 flex items-center justify-between animate-fadeIn">
                        <div className="flex items-center gap-2">
                            <Clock className="w-4 h-4 text-blue-400" />
                            <span className="text-xs text-blue-300 font-medium">Configuración Activa:</span>
                            <span className="text-xs font-bold text-white uppercase">
                                {Object.keys(diasLaborables).filter(d => diasLaborables[d]).map(d => d.toUpperCase()).join('-')}
                            </span>
                            <span className="text-xs text-gray-400">({horasPorDia}h/día)</span>
                        </div>
                        <button
                            onClick={() => setMostrarConfigCalendario(true)}
                            className="text-[10px] text-blue-400 hover:text-blue-300 underline"
                        >
                            Cambiar
                        </button>
                    </div>
                )}
            </div>

            {/* Barra de Progreso */}
            <div className="mb-6 bg-gray-800 rounded-lg p-3 border border-gray-700">
                <div className="flex justify-between items-center mb-2 text-xs font-semibold uppercase tracking-wider">
                    <span className={excedeLimite ? "text-red-400" : "text-blue-400"}>
                        Días Asignados: {duracionTotal} / {limiteDias}
                    </span>
                    <span className="text-gray-500">Máximo permitido</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2.5 overflow-hidden">
                    <div
                        className={`h-2.5 rounded-full transition-all duration-500 ${excedeLimite ? 'bg-red-500' : 'bg-blue-500'}`}
                        style={{ width: `${Math.min((duracionTotal / limiteDias) * 100, 100)}%` }}
                    ></div>
                </div>
            </div>

            <div className="space-y-3 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
                {fases.map((fase) => (
                    <div key={fase.id} className="bg-gray-800/50 p-3 rounded-xl border border-gray-700 flex items-center gap-3 hover:border-blue-500/30 transition-colors">
                        <div className="bg-blue-900/30 text-blue-400 text-xs font-bold w-6 h-6 flex items-center justify-center rounded-full flex-shrink-0">
                            {fase.id}
                        </div>
                        <div className="flex-1">
                            <div className="flex justify-between items-center mb-1">
                                <span className="text-gray-200 text-sm font-medium">{fase.nombre}</span>
                                <span className="text-blue-400 text-xs font-bold bg-blue-500/10 px-2 py-0.5 rounded">
                                    {fase.duracion}d
                                </span>
                            </div>
                            <input
                                type="range"
                                min="1"
                                max="60"
                                value={fase.duracion}
                                onChange={(e) => handleDuracionChange(fase.id, e.target.value)}
                                className={`w-full h-1.5 rounded-lg appearance-none cursor-pointer ${excedeLimite ? 'bg-red-900 accent-red-500' : 'bg-gray-700 accent-blue-500'}`}
                            />
                        </div>
                    </div>
                ))}
            </div>

            {/* Footer Resumen */}
            <div className="bg-black/40 rounded-xl p-4 border border-gray-700 mt-6 grid grid-cols-2 gap-4">
                <div>
                    <div className="flex items-center gap-2 mb-1">
                        <Clock className="w-4 h-4 text-gray-400" />
                        <span className="text-gray-400 text-xs uppercase font-bold tracking-wider">Total Días Hábiles</span>
                    </div>
                    <div className={`text-3xl font-bold ${excedeLimite ? 'text-red-500' : 'text-white'}`}>
                        {duracionTotal}
                    </div>
                </div>

                <div className="text-right border-l border-gray-700 pl-4">
                    <div className="flex items-center justify-end gap-2 mb-1">
                        <Calendar className="w-4 h-4 text-green-400" />
                        <span className="text-green-400 text-xs uppercase font-bold tracking-wider">Fecha Fin Real</span>
                    </div>
                    <div className="text-xl font-bold text-white font-mono">
                        {fechaFinEstimada ? fechaFinEstimada.toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' }) : '---'}
                    </div>
                    <p className="text-[10px] text-gray-500 mt-1">
                        Sincronizado: {diasPorSemana} días/semana
                    </p>
                </div>
            </div>

            <button
                onClick={handleSubmit}
                disabled={excedeLimite}
                className={`w-full mt-6 py-4 font-bold rounded-xl shadow-lg transform transition-all flex items-center justify-center gap-2 text-lg
                    ${excedeLimite
                        ? 'bg-gray-700 text-gray-400 cursor-not-allowed opacity-50'
                        : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white shadow-blue-600/20 hover:scale-[1.02] active:scale-95'
                    }`}
            >
                {excedeLimite ? '⚠️ Reduce la duración' : '✅ Guardar Configuración'}
            </button>
        </div>
    );
};

export default FormularioGanttDiasPro;
