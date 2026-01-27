/**
 * Componente de Calendario Profesional para Gestión de Proyectos PMI
 * Tipo MS Project - Calcula automáticamente fechas, días hábiles y horas
 */

import React, { useState, useEffect } from 'react';
import DatePicker, { registerLocale } from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { es } from 'date-fns/locale';
import {
    calcularProyecto,
    PLANTILLAS_HORARIO,
    esFeriado,
    esDiaHabil
} from '../utils/calculadoraProyecto';
import './CalendarioProyecto.css';

// Registrar locale español para react-datepicker
registerLocale('es', es);

const CalendarioProyecto = ({ onChange, valoresIniciales = {} }) => {
    // Estados
    const [fechaInicio, setFechaInicio] = useState(valoresIniciales.fechaInicio || new Date());
    const [duracionMeses, setDuracionMeses] = useState(valoresIniciales.duracionMeses || 4);
    const [usarDiasHabiles, setUsarDiasHabiles] = useState(valoresIniciales.usarDiasHabiles !== false);
    const [plantillaSeleccionada, setPlantillaSeleccionada] = useState('construccion');
    const [horarioPersonalizado, setHorarioPersonalizado] = useState('');

    // Obtener horario actual
    const horarioActual = plantillaSeleccionada === 'personalizado'
        ? horarioPersonalizado
        : PLANTILLAS_HORARIO[plantillaSeleccionada].horario;

    // Calcular todos los datos del proyecto
    const datosCalculados = calcularProyecto({
        fechaInicio,
        duracionMeses,
        usarDiasHabiles,
        horario: horarioActual
    });

    // Notificar cambios al componente padre
    useEffect(() => {
        if (onChange) {
            onChange(datosCalculados);
        }
    }, [fechaInicio, duracionMeses, usarDiasHabiles, horarioActual]);

    // Función para resaltar días especiales en el calendario
    const getDayClassName = (date) => {
        if (esFeriado(date)) return 'dia-feriado';
        if (!esDiaHabil(date)) return 'dia-no-habil';
        return 'dia-habil';
    };

    return (
        <div className="calendario-proyecto">
            <h3 className="calendario-titulo">
                📅 Configuración de Cronograma
            </h3>

            <div className="calendario-grid">
                {/* COLUMNA IZQUIERDA: Configuración */}
                <div className="calendario-config">

                    {/* Fecha de Inicio */}
                    <div className="campo-grupo">
                        <label className="campo-label">
                            📆 Fecha de Inicio
                        </label>
                        <DatePicker
                            selected={fechaInicio}
                            onChange={(date) => setFechaInicio(date)}
                            dateFormat="dd/MM/yyyy"
                            className="campo-input fecha-picker"
                            dayClassName={getDayClassName}
                            locale="es"
                            showWeekNumbers
                        />
                    </div>

                    {/* Duración Estimada */}
                    <div className="campo-grupo">
                        <label className="campo-label">
                            ⏱️ Duración Estimada (Meses)
                        </label>
                        <input
                            type="number"
                            min="1"
                            max="24"
                            value={duracionMeses}
                            onChange={(e) => setDuracionMeses(Number(e.target.value))}
                            className="campo-input"
                        />
                        <span className="campo-ayuda">
                            Duración aproximada del proyecto
                        </span>
                    </div>

                    {/* Tipo de Días */}
                    <div className="campo-grupo">
                        <label className="campo-label">
                            📊 Tipo de Cálculo
                        </label>
                        <div className="toggle-grupo">
                            <button
                                className={`toggle-btn ${usarDiasHabiles ? 'activo' : ''}`}
                                onClick={() => setUsarDiasHabiles(true)}
                            >
                                📅 Días Hábiles
                            </button>
                            <button
                                className={`toggle-btn ${!usarDiasHabiles ? 'activo' : ''}`}
                                onClick={() => setUsarDiasHabiles(false)}
                            >
                                📆 Días Calendario
                            </button>
                        </div>
                        <span className="campo-ayuda">
                            {usarDiasHabiles
                                ? 'Excluye fines de semana y feriados'
                                : 'Incluye todos los días'}
                        </span>
                    </div>

                    {/* Plantilla de Horario */}
                    <div className="campo-grupo">
                        <label className="campo-label">
                            ⏰ Horario de Trabajo
                        </label>
                        <select
                            value={plantillaSeleccionada}
                            onChange={(e) => setPlantillaSeleccionada(e.target.value)}
                            className="campo-input"
                        >
                            {Object.entries(PLANTILLAS_HORARIO).map(([key, plantilla]) => (
                                <option key={key} value={key}>
                                    {plantilla.label}
                                </option>
                            ))}
                        </select>

                        {plantillaSeleccionada === 'personalizado' && (
                            <input
                                type="text"
                                placeholder="Ej: 8:00-13:00, 14:00-17:00"
                                value={horarioPersonalizado}
                                onChange={(e) => setHorarioPersonalizado(e.target.value)}
                                className="campo-input mt-2"
                            />
                        )}

                        <span className="campo-ayuda">
                            {horarioActual || 'Configura tu horario personalizado'}
                        </span>
                    </div>
                </div>

            </div>
        </div>

    );
};

export default CalendarioProyecto;
