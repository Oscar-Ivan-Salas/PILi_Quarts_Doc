/**
 * Utilidades para cálculo de fechas y cronogramas de proyectos
 * Tipo MS Project - Considera días hábiles, feriados y horarios laborales
 */

import {
    addDays,
    getDay,
    differenceInDays,
    format,
    parse,
    isWeekend,
    isSameDay
} from 'date-fns';
import { es } from 'date-fns/locale';

// ============================================================================
// CONFIGURACIÓN DE FERIADOS PERÚ 2026
// ============================================================================

export const FERIADOS_2026 = [
    new Date(2026, 0, 1),   // Año Nuevo
    new Date(2026, 3, 9),   // Jueves Santo
    new Date(2026, 3, 10),  // Viernes Santo
    new Date(2026, 4, 1),   // Día del Trabajo
    new Date(2026, 5, 29),  // San Pedro y San Pablo
    new Date(2026, 6, 28),  // Fiestas Patrias
    new Date(2026, 6, 29),  // Fiestas Patrias
    new Date(2026, 7, 30),  // Santa Rosa de Lima
    new Date(2026, 9, 8),   // Combate de Angamos
    new Date(2026, 10, 1),  // Todos los Santos
    new Date(2026, 11, 8),  // Inmaculada Concepción
    new Date(2026, 11, 25), // Navidad
];

// ============================================================================
// FUNCIONES AUXILIARES
// ============================================================================

/**
 * Verifica si una fecha es feriado
 */
export function esFeriado(fecha) {
    return FERIADOS_2026.some(feriado => isSameDay(feriado, fecha));
}

/**
 * Verifica si una fecha es día hábil (no es fin de semana ni feriado)
 */
export function esDiaHabil(fecha) {
    return !isWeekend(fecha) && !esFeriado(fecha);
}

// ============================================================================
// CÁLCULO DE FECHAS
// ============================================================================

/**
 * Calcula la fecha de fin del proyecto
 * @param {Date} fechaInicio - Fecha de inicio del proyecto
 * @param {number} duracionMeses - Duración estimada en meses
 * @param {boolean} usarDiasHabiles - Si true, cuenta solo días hábiles
 * @returns {Date} Fecha de fin calculada
 */
export function calcularFechaFin(fechaInicio, duracionMeses, usarDiasHabiles = true) {
    // Convertir meses a días (aproximado: 1 mes = 30 días)
    const diasEstimados = Math.round(duracionMeses * 30);

    if (!usarDiasHabiles) {
        // Días calendario: simplemente sumar días
        return addDays(fechaInicio, diasEstimados);
    }

    // Días hábiles: contar solo días laborables
    let diasContados = 0;
    let fechaActual = new Date(fechaInicio);

    while (diasContados < diasEstimados) {
        fechaActual = addDays(fechaActual, 1);

        // Solo contar si es día hábil
        if (esDiaHabil(fechaActual)) {
            diasContados++;
        }
    }

    return fechaActual;
}

/**
 * Calcula el número de días hábiles entre dos fechas
 * @param {Date} fechaInicio - Fecha de inicio
 * @param {Date} fechaFin - Fecha de fin
 * @returns {number} Número de días hábiles
 */
export function calcularDiasHabiles(fechaInicio, fechaFin) {
    let dias = 0;
    let fechaActual = new Date(fechaInicio);

    while (fechaActual <= fechaFin) {
        if (esDiaHabil(fechaActual)) {
            dias++;
        }
        fechaActual = addDays(fechaActual, 1);
    }

    return dias;
}

/**
 * Calcula el número total de días calendario entre dos fechas
 * @param {Date} fechaInicio - Fecha de inicio
 * @param {Date} fechaFin - Fecha de fin
 * @returns {number} Número de días calendario
 */
export function calcularDiasCalendario(fechaInicio, fechaFin) {
    return differenceInDays(fechaFin, fechaInicio) + 1;
}

// ============================================================================
// CÁLCULO DE HORAS
// ============================================================================

/**
 * Calcula el total de horas de trabajo
 * @param {number} diasHabiles - Número de días hábiles
 * @param {number} horasPorDia - Horas de trabajo por día (default: 8)
 * @returns {number} Total de horas
 */
export function calcularHorasTotales(diasHabiles, horasPorDia = 8) {
    return diasHabiles * horasPorDia;
}

/**
 * Parsea horario en formato "8:00-13:00, 14:00-17:00" y calcula horas por día
 * @param {string} horario - Horario en formato texto
 * @returns {number} Horas totales por día
 */
export function calcularHorasPorDia(horario) {
    if (!horario) return 8; // Default: 8 horas

    try {
        // Ejemplo: "8:00-13:00, 14:00-17:00"
        const bloques = horario.split(',').map(b => b.trim());
        let horasTotales = 0;

        bloques.forEach(bloque => {
            const [inicio, fin] = bloque.split('-').map(h => h.trim());
            const [horaInicio, minInicio] = inicio.split(':').map(Number);
            const [horaFin, minFin] = fin.split(':').map(Number);

            const minutosInicio = horaInicio * 60 + minInicio;
            const minutosFin = horaFin * 60 + minFin;
            const minutosBloque = minutosFin - minutosInicio;

            horasTotales += minutosBloque / 60;
        });

        return horasTotales;
    } catch (error) {
        console.error('Error parseando horario:', error);
        return 8; // Fallback
    }
}

// ============================================================================
// FORMATEO DE FECHAS
// ============================================================================

/**
 * Formatea fecha a formato peruano DD/MM/YYYY
 * @param {Date} fecha - Fecha a formatear
 * @returns {string} Fecha formateada
 */
export function formatearFecha(fecha) {
    return format(fecha, 'dd/MM/yyyy', { locale: es });
}

/**
 * Parsea fecha desde formato DD/MM/YYYY
 * @param {string} fechaStr - Fecha en formato texto
 * @returns {Date} Fecha parseada
 */
export function parsearFecha(fechaStr) {
    return parse(fechaStr, 'dd/MM/yyyy', new Date(), { locale: es });
}

// ============================================================================
// PLANTILLAS DE HORARIO
// ============================================================================

export const PLANTILLAS_HORARIO = {
    construccion: {
        label: 'Construcción (8:00-17:00)',
        horario: '8:00-13:00, 14:00-17:00',
        horasPorDia: 8
    },
    oficina: {
        label: 'Oficina (9:00-18:00)',
        horario: '9:00-13:00, 14:00-18:00',
        horasPorDia: 8
    },
    mineria: {
        label: 'Minería (Turnos 24/7)',
        horario: '24 horas',
        horasPorDia: 24
    },
    personalizado: {
        label: 'Personalizado',
        horario: '',
        horasPorDia: 8
    }
};

// ============================================================================
// FUNCIÓN PRINCIPAL: CALCULAR TODO
// ============================================================================

/**
 * Calcula todos los datos del proyecto de una vez
 * @param {Object} config - Configuración del proyecto
 * @returns {Object} Todos los datos calculados
 */
export function calcularProyecto(config) {
    const {
        fechaInicio,
        duracionMeses,
        usarDiasHabiles = true,
        horario = '8:00-13:00, 14:00-17:00'
    } = config;

    // Calcular fecha fin
    const fechaFin = calcularFechaFin(fechaInicio, duracionMeses, usarDiasHabiles);

    // Calcular días
    const diasHabiles = usarDiasHabiles
        ? calcularDiasHabiles(fechaInicio, fechaFin)
        : calcularDiasCalendario(fechaInicio, fechaFin);

    // Calcular horas
    const horasPorDia = calcularHorasPorDia(horario);
    const horasTotales = calcularHorasTotales(diasHabiles, horasPorDia);

    return {
        fecha_inicio: formatearFecha(fechaInicio),
        fecha_fin: formatearFecha(fechaFin),
        duracion_dias: diasHabiles,
        duracion_horas: horasTotales,
        duracion_meses: duracionMeses,
        horario: horario,
        horas_por_dia: horasPorDia,
        dias_habiles: usarDiasHabiles
    };
}
