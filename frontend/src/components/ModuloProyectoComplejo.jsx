import React, { useState, useEffect } from 'react';
import PiliElectricidadProyectoComplejoPMIChat from './PiliElectricidadProyectoComplejoPMIChat';
import EditablePhaseTable from './EditablePhaseTable';
import ProyectoResumen from './ProyectoResumen';
import VistaPreviaProfesional from './VistaPreviaProfesional';
import ConfiguracionProyectoComplejo from './ConfiguracionProyectoComplejo';
import FormularioStakeholdersPro from './FormularioStakeholdersPro';
import FormularioEntregablesPro from './FormularioEntregablesPro';
import FormularioRACIPro from './FormularioRACIPro';
import FormularioSuministrosPro from './FormularioSuministrosPro';
import FormularioRiesgosPro from './FormularioRiesgosPro';
import { FileText, Loader, Download, Edit3, Eye, Users, TrendingUp, Clock, Award, Save } from 'lucide-react';
import Alerta from './Alerta';

const ModuloProyectoComplejo = ({
    datosIniciales,
    onBack,
    onGuardarBorrador,
    proyectoId,
    setProyectoId,
    onGenerarDocumento // ✅ Prop para generación real
}) => {
    // ESTADO DE ETAPA DEL MÓDULO (Config -> Planificación -> Preview)
    // Si ya viene con nombre de proyecto (desde App.jsx), salta directo a 'planificacion'
    const [etapaModulo, setEtapaModulo] = useState(datosIniciales?.nombre_proyecto ? 'planificacion' : 'config');

    // ESTADOS PRINCIPALES MIGRADOS DE APP.JSX
    const [paso, setPaso] = useState(1); // 1: Config/Planificacion, 2: Documento Final

    // Estado Central del Proyecto (Fuente de Verdad)
    const [datosProyecto, setDatosProyecto] = useState(datosIniciales || {
        nombre_proyecto: '',
        cliente: '',
        presupuesto: 0,
        duracion_total: 0,
        datosCalendario: null,
        fases: [],
        riesgos: [],
        stakeholders: [],
        kpis: {}
    });

    // Estados de UI
    const [descargando, setDescargando] = useState(null);
    const [alerta, setAlerta] = useState(null);
    const [activeTab, setActiveTab] = useState('general');

    // Mapeo de Etapas para la UI - ICONOS IMPORTADOS
    const etapas = [
        { id: 'general', label: '1. General', icon: FileText },
        { id: 'stakeholders', label: '2. Stakeholders', icon: Users },
        { id: 'entregables', label: '3. Entregables', icon: Award },
        { id: 'gantt', label: '4. Cronograma', icon: Clock },
        { id: 'raci', label: '5. Rec. & RACI', icon: Users },
        { id: 'suministros', label: '6. Suministros', icon: TrendingUp },
        { id: 'riesgos', label: '7. Riesgos', icon: Loader },
        { id: 'analisis', label: '8. Análisis Pili', icon: Edit3 },
    ];

    // Persistencia Automática (Debounced)
    useEffect(() => {
        const timer = setTimeout(() => {
            if (proyectoId && datosProyecto) {
                // Auto-save silent
                if (onGuardarBorrador) onGuardarBorrador(datosProyecto, proyectoId, true); // true = silencioso
            }
        }, 2000);
        return () => clearTimeout(timer);
    }, [datosProyecto, proyectoId]);

    // HANDLERS
    const handleDatosGenerados = (nuevosDatos) => {


        setDatosProyecto(prev => {
            const actualizado = { ...prev, ...nuevosDatos };
            return actualizado;
        });

        // Si tenemos datos críticos, guardar inmediatamente en BD
        if (proyectoId && onGuardarBorrador) {
            onGuardarBorrador({ ...datosProyecto, ...nuevosDatos }, proyectoId, false);
        }
    };

    const handleFasesChange = (nuevasFases, totalDias, fechaFinEstimada) => {
        // Actualización bidireccional desde la tabla/gantt
        setDatosProyecto(prev => ({
            ...prev,
            fases: nuevasFases,
            duracion_total: totalDias,
            fecha_fin: fechaFinEstimada
        }));
    };

    const handleGenerarDocumento = (formato) => {
        setDescargando(formato);
        if (onGenerarDocumento) {
            // Llamar a la función real de App.jsx
            onGenerarDocumento(formato, datosProyecto);

            // Resetear estado de carga después de unos segundos (la descarga real es asíncrona)
            setTimeout(() => setDescargando(null), 3000);
        } else {
            setDescargando(null);
        }
    };

    // RENDERIZADO CONDICIONAL POR ETAPAS
    if (etapaModulo === 'config') {
        return (
            <ConfiguracionProyectoComplejo
                datosProyecto={datosProyecto}
                onUpdateDatos={setDatosProyecto}
                onNext={() => setEtapaModulo('planificacion')}
                onBack={onBack}
                guardarBorrador={(datos) => onGuardarBorrador && onGuardarBorrador(datos, proyectoId, false)}
            />
        );
    }



    // RENDERIZADO DEL CONTENIDO PRINCIPAL POR PESTAÑA
    const renderContent = () => {
        switch (activeTab) {
            case 'general':
                return (
                    <ConfiguracionProyectoComplejo
                        datosProyecto={datosProyecto}
                        onUpdateDatos={setDatosProyecto}
                        onNext={() => setActiveTab('stakeholders')}
                        onBack={onBack}
                        guardarBorrador={onGuardarBorrador}
                    />
                );
            case 'stakeholders':
                return (
                    <div className="h-full flex flex-col">
                        <h2 className="text-2xl font-bold text-yellow-500 mb-4 px-8 pt-6 border-b border-yellow-600/30 pb-2">
                            2. Mapa de Involucrados (Stakeholders)
                        </h2>
                        <div className="flex-1 overflow-hidden px-8 pb-8 custom-scrollbar overflow-y-auto">
                            <FormularioStakeholdersPro
                                valoresIniciales={datosProyecto.stakeholders || []}
                                onSubmit={(nuevosStakeholders) => {
                                    setDatosProyecto(prev => ({ ...prev, stakeholders: nuevosStakeholders }));
                                    setActiveTab('entregables');
                                }}
                            />
                        </div>
                        <div className="px-8 py-4 border-t border-gray-800 flex justify-end bg-black/50">
                            <button onClick={() => setActiveTab('entregables')} className="px-6 py-2 bg-yellow-600 text-black font-bold rounded hover:bg-yellow-500 transition-colors shadow-lg shadow-yellow-900/20">
                                Guardar y Continuar
                            </button>
                        </div>
                    </div>
                );
            case 'entregables':
                return (
                    <div className="h-full flex flex-col">
                        <h2 className="text-2xl font-bold text-yellow-500 mb-4 px-8 pt-6 border-b border-yellow-600/30 pb-2">
                            3. Alcance y Entregables
                        </h2>
                        <div className="flex-1 overflow-hidden px-8 pb-8 custom-scrollbar overflow-y-auto">
                            <FormularioEntregablesPro
                                tipoProyecto={datosProyecto.servicio || 'residencial'}
                                area={datosProyecto.area_proyecto || 0}
                                presupuesto={datosProyecto.presupuesto || 0}
                                onSubmit={(nuevosEntregables) => {
                                    setDatosProyecto(prev => ({ ...prev, entregables: nuevosEntregables }));
                                    setActiveTab('gantt');
                                }}
                            />
                        </div>
                        <div className="px-8 py-4 border-t border-gray-800 flex justify-end bg-black/50">
                            <button onClick={() => setActiveTab('gantt')} className="px-6 py-2 bg-yellow-600 text-black font-bold rounded hover:bg-yellow-500 transition-colors shadow-lg shadow-yellow-900/20">
                                Guardar y Continuar
                            </button>
                        </div>
                    </div>
                );
            case 'gantt':
                return (
                    <div className="p-8 h-full overflow-y-auto flex flex-col">
                        <h2 className="text-2xl font-bold text-yellow-500 mb-6 border-b border-yellow-600/30 pb-2">
                            4. Cronograma Maestro (Gantt)
                        </h2>
                        <div className="flex-1 bg-black/40 border border-yellow-600/30 rounded-xl p-4 overflow-hidden mb-4 min-h-[500px]">
                            <EditablePhaseTable
                                fasesIniciales={datosProyecto.fases}
                                duracionTotal={datosProyecto.duracion_total}
                                fechaInicio={datosProyecto.fecha_inicio}
                                onFasesChange={handleFasesChange}
                            />
                        </div>
                        <div className="flex justify-end">
                            <button onClick={() => setActiveTab('raci')} className="px-6 py-2 bg-yellow-600 text-black font-bold rounded hover:bg-yellow-500 transition-colors shadow-lg shadow-yellow-900/20">
                                Guardar Cronograma
                            </button>
                        </div>
                    </div>
                );
            case 'raci':
                return (
                    <div className="h-full flex flex-col">
                        <h2 className="text-2xl font-bold text-yellow-500 mb-4 px-8 pt-6 border-b border-yellow-600/30 pb-2">
                            5. Recursos y Matriz RACI
                        </h2>
                        <div className="flex-1 overflow-hidden px-8 pb-8 custom-scrollbar overflow-y-auto">
                            <FormularioRACIPro
                                complejidad={datosProyecto.complejidad || 7}
                                onSubmit={(raciData) => {
                                    setDatosProyecto(prev => ({ ...prev, raci: raciData }));
                                    setActiveTab('suministros');
                                }}
                            />
                        </div>
                        {/* El botón de guardar está dentro del formulario RACI, pero podemos agregar navegación extra si se desea */}
                    </div>
                );
            case 'suministros':
                return (
                    <div className="h-full flex flex-col">
                        <h2 className="text-2xl font-bold text-yellow-500 mb-4 px-8 pt-6 border-b border-yellow-600/30 pb-2">
                            6. Suministros y Logística
                        </h2>
                        <div className="flex-1 overflow-hidden px-8 pb-8 custom-scrollbar overflow-y-auto">
                            <FormularioSuministrosPro
                                tipoProyecto={datosProyecto.servicio || 'residencial'}
                                area={datosProyecto.area_proyecto || 0}
                                presupuesto={datosProyecto.presupuesto || 0}
                                onSubmit={(nuevosSuministros) => {
                                    setDatosProyecto(prev => ({ ...prev, suministros: nuevosSuministros }));
                                    setActiveTab('riesgos');
                                }}
                            />
                        </div>
                        <div className="px-8 py-4 border-t border-gray-800 flex justify-end bg-black/50">
                            <button onClick={() => setActiveTab('riesgos')} className="px-6 py-2 bg-yellow-600 text-black font-bold rounded hover:bg-yellow-500 transition-colors shadow-lg shadow-yellow-900/20">
                                Guardar y Continuar
                            </button>
                        </div>
                    </div>
                );
            case 'riesgos':
                return (
                    <div className="h-full flex flex-col">
                        <h2 className="text-2xl font-bold text-yellow-500 mb-4 px-8 pt-6 border-b border-yellow-600/30 pb-2">
                            7. Matriz de Riesgos (Risk Register)
                        </h2>
                        <div className="flex-1 overflow-hidden px-8 pb-8 custom-scrollbar overflow-y-auto">
                            <FormularioRiesgosPro
                                valoresIniciales={datosProyecto.riesgos || []}
                                onSubmit={(nuevosRiesgos) => {
                                    setDatosProyecto(prev => ({ ...prev, riesgos: nuevosRiesgos }));
                                    setActiveTab('analisis');
                                }}
                            />
                        </div>
                        <div className="px-8 py-4 border-t border-gray-800 flex justify-end bg-black/50">
                            <button onClick={() => setActiveTab('analisis')} className="px-6 py-2 bg-yellow-600 text-black font-bold rounded hover:bg-yellow-500 transition-colors shadow-lg shadow-yellow-900/20">
                                Ir a Auditoría Final
                            </button>
                        </div>
                    </div>
                );
            case 'analisis':
                return (
                    <div className="h-full flex flex-col bg-gray-950">
                        <div className="bg-red-950/20 p-4 border-b border-red-900/50 flex justify-between items-center">
                            <div>
                                <h3 className="text-yellow-400 font-bold flex items-center gap-2">
                                    <span className="text-xl">🤖</span> Auditoría de Proyecto con PILI
                                </h3>
                                <p className="text-xs text-gray-400">Pili analizará los formularios completados y generará el informe final.</p>
                            </div>
                            <button onClick={() => handleGenerarDocumento('pdf')} className="px-4 py-2 bg-red-600 text-white text-xs font-bold rounded hover:bg-red-500 transition">
                                Generar PDF Final
                            </button>
                        </div>
                        <div className="flex-1 relative">
                            <PiliElectricidadProyectoComplejoPMIChat
                                datosCliente={datosProyecto.cliente}
                                nombre_proyecto={datosProyecto.nombre_proyecto}
                                presupuesto={datosProyecto.presupuesto}
                                moneda={datosProyecto.moneda}
                                duracion_total={datosProyecto.duracion_total}
                                datosCalendario={datosProyecto.datosCalendario}
                                servicio={datosProyecto.servicio}
                                industria={datosProyecto.industria}
                                descripcion_inicial={datosProyecto.alcance_proyecto}
                                proyectoId={proyectoId}
                                onDatosGenerados={handleDatosGenerados}
                                onFinish={() => handleGenerarDocumento('pdf')}
                                onBack={onBack}
                                complejidad={datosProyecto.complejidad || 7}
                                etapasSeleccionadas={datosProyecto.etapas_seleccionadas}
                                contextoProyecto={datosProyecto} // ✅ Contexto completo para análisis

                                incluirMetrado={datosProyecto.incluir_metrado}
                                areaMetrado={datosProyecto.area_proyecto}
                                viewMode="full"
                                setViewMode={() => { }}
                            />
                        </div>
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div className="flex flex-col h-screen overflow-hidden bg-gradient-to-br from-gray-950 via-red-950 to-black animate-fadeIn text-white font-sans">
            {alerta && <Alerta tipo={alerta.tipo} mensaje={alerta.mensaje} onClose={() => setAlerta(null)} />}

            {/* HEADER TESLA PREMIUM */}
            <div className="bg-black/95 border-b border-yellow-600/50 p-4 flex justify-between items-center shadow-lg z-50 backdrop-blur-md">
                <div className="flex items-center gap-6">
                    <button
                        onClick={onBack}
                        className="text-gray-400 hover:text-yellow-500 transition-colors flex items-center gap-2 text-sm font-semibold uppercase tracking-wider"
                    >
                        ← Volver
                    </button>
                    <div>
                        <h1 className="text-xl font-bold text-white flex items-center gap-2 tracking-wide">
                            <span className="text-yellow-500 text-2xl">⚡</span>
                            {datosProyecto.nombre_proyecto || 'NUEVO PROYECTO PMI'}
                        </h1>
                        <div className="flex items-center gap-4 text-xs text-gray-500 mt-1">
                            <span className="flex items-center gap-1"><Users className="w-3 h-3 text-yellow-600" /> {datosProyecto.cliente?.nombre || 'Sin Cliente'}</span>
                            <span className="flex items-center gap-1"><TrendingUp className="w-3 h-3 text-green-600" /> {datosProyecto.presupuesto ? `Presupuesto: ${datosProyecto.presupuesto}` : 'Sin Presupuesto'}</span>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-3">
                    <button
                        onClick={() => {
                            if (onGuardarBorrador) {
                                onGuardarBorrador(datosProyecto, proyectoId);
                                setAlerta({ tipo: 'success', mensaje: 'Proyecto guardado correctamente' });
                                setTimeout(() => setAlerta(null), 3000);
                            }
                        }}
                        className="px-4 py-2 bg-yellow-900/20 border border-yellow-600 text-yellow-100 hover:bg-yellow-600 hover:text-black rounded transition-all text-xs font-bold uppercase tracking-widest flex items-center gap-2"
                    >
                        <Save className="w-4 h-4" /> Guardar
                    </button>
                    <button
                        onClick={() => handleGenerarDocumento('pdf')}
                        className="px-4 py-2 bg-red-900/20 border border-red-600 text-red-100 hover:bg-red-600 hover:text-white rounded transition-all text-xs font-bold uppercase tracking-widest flex items-center gap-2"
                    >
                        <FileText className="w-4 h-4" /> PDF Preliminar
                    </button>
                    <div className="h-8 w-[1px] bg-gray-800 mx-2"></div>
                    <div className="text-right">
                        <div className="text-[10px] text-gray-400 uppercase tracking-widest">Estado</div>
                        <div className="text-xs font-bold text-yellow-500">BORRADOR</div>
                    </div>
                </div>
            </div>

            {/* CONTENIDO: SIDEBAR DE NAVEGACIÓN + ÁREA DE TRABAJO */}
            <div className="flex flex-1 overflow-hidden">
                {/* SIDEBAR DE NAVEGACIÓN (7 PASOS) */}
                <div className="w-64 bg-black/80 border-r border-gray-800 flex flex-col pt-4">
                    <div className="px-6 pb-4 border-b border-gray-800/50 mb-2">
                        <div className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Fases de Configuración</div>
                    </div>
                    <nav className="flex-1 overflow-y-auto px-2 space-y-1 custom-scrollbar">
                        {etapas.map((etapa) => {
                            const isActive = activeTab === etapa.id;
                            const Icon = etapa.icon || FileText; // Fallback
                            return (
                                <button
                                    key={etapa.id}
                                    onClick={() => setActiveTab(etapa.id)}
                                    className={`w-full text-left px-4 py-3 flex items-center gap-3 text-sm transition-all rounded-lg group relative
                                    ${isActive
                                            ? 'bg-gradient-to-r from-yellow-900/30 to-transparent text-yellow-400 font-bold border border-yellow-600/30'
                                            : 'text-gray-400 hover:text-white hover:bg-white/5 border border-transparent'
                                        }`}
                                >
                                    <Icon className={`w-4 h-4 ${isActive ? 'text-yellow-500' : 'text-gray-600 group-hover:text-gray-300'}`} />
                                    {etapa.label}
                                    {isActive && <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-yellow-500 rounded-r"></div>}
                                </button>
                            );
                        })}
                    </nav>
                </div>

                {/* ÁREA PRINCIPAL */}
                <div className="flex-1 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] relative flex flex-col">
                    {/* Overlay para oscurecer el fondo */}
                    <div className="absolute inset-0 bg-gray-950/90 pointer-events-none"></div>

                    {/* Contenido Real */}
                    <div className="relative z-10 flex-1 overflow-y-auto custom-scrollbar">
                        {renderContent()}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModuloProyectoComplejo;
