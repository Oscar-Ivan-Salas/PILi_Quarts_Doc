import React, { useState, useRef, useEffect } from 'react';
import {
    Upload, MessageSquare, FileText, Zap, Loader, Save, AlertCircle, CheckCircle,
    X, Home, Users, TrendingUp, Calendar, CheckSquare, Mail, Phone, MapPin, Building2,
    Layout
} from 'lucide-react';
import CalendarioProyecto from './CalendarioProyecto';
import ProyectoResumen from './ProyectoResumen';

const ConfiguracionProyectoComplejo = ({
    datosProyecto,
    onUpdateDatos,
    onNext,
    onBack,
    guardarBorrador
}) => {
    // ============================================
    // ESTADOS LOCALES (MIGRADOS DE APP.JSX)
    // ============================================
    const [guardandoCliente, setGuardandoCliente] = useState(false);
    const [error, setError] = useState('');
    const [exito, setExito] = useState('');

    // Configuración Alcance PMI
    const [complejidad, setComplejidad] = useState(datosProyecto.complejidad || 5);
    const [etapasSeleccionadas, setEtapasSeleccionadas] = useState(
        datosProyecto.etapasSeleccionadas || ['acta_constitucion', 'stakeholders', 'cronograma', 'cierre']
    );

    // Metrado
    const [incluirMetrado, setIncluirMetrado] = useState(!!datosProyecto.areaMetrado);
    const [areaMetrado, setAreaMetrado] = useState(datosProyecto.areaMetrado || '');

    // Cronograma y Fases
    const [fasesCalculadas, setFasesCalculadas] = useState(datosProyecto.cronograma_fases || []);

    // Referencias
    const fileInputRef = useRef(null);
    const fileInputLogoRef = useRef(null);

    // ============================================
    // LÓGICA DE NEGOCIO (MIGRADA)
    // ============================================

    // Sincronizar cambios locales con el padre (datosProyecto)
    useEffect(() => {
        onUpdateDatos({
            ...datosProyecto,
            complejidad,
            etapasSeleccionadas,
            areaMetrado: incluirMetrado ? areaMetrado : null,
            cronograma_fases: fasesCalculadas
        });
    }, [complejidad, etapasSeleccionadas, incluirMetrado, areaMetrado, fasesCalculadas]);


    const handleClienteChange = (e) => {
        const { name, value } = e.target;
        onUpdateDatos({
            ...datosProyecto,
            cliente: { ...datosProyecto.cliente, [name]: value }
        });
    };

    const handleDatosProyectoChange = (field, value) => {
        onUpdateDatos({ ...datosProyecto, [field]: value });
    };

    const handleFileUpload = (e) => {
        const files = Array.from(e.target.files);
        const validFiles = files.filter(file => file.size <= 10 * 1024 * 1024);
        if (validFiles.length < files.length) setError('Algunos archivos exceden 10MB');

        onUpdateDatos({
            ...datosProyecto,
            archivos: [...(datosProyecto.archivos || []), ...validFiles]
        });
    };

    const handleLogoUpload = (e) => {
        const file = e.target.files[0];
        if (file && file.size <= 2 * 1024 * 1024) {
            const reader = new FileReader();
            reader.onloadend = () => handleDatosProyectoChange('logo', reader.result);
            reader.readAsDataURL(file);
        } else {
            setError("El logo debe ser menor a 2MB");
        }
    };

    // CALCULO DE FASES (Logica simplificada para UI)
    const calcularCronogramaPreliminar = () => {
        if (!datosProyecto.fecha_inicio || !datosProyecto.duracion_total) {
            setError('Define fecha inicio y duración primero');
            return;
        }

        // Distribución porcentual basada en complejidad
        const items = complejidad === 5
            ? [
                { nombre: '1. Iniciación (Acta)', pct: 0.10 },
                { nombre: '2. Planificación', pct: 0.20 },
                { nombre: '3. Ejecución', pct: 0.50 },
                { nombre: '4. Control', pct: 0.15 },
                { nombre: '5. Cierre', pct: 0.05 }
            ]
            : [
                { nombre: '1. Iniciación', pct: 0.05 },
                { nombre: '2. Plan. Alcance', pct: 0.15 },
                { nombre: '3. Plan. Riesgos', pct: 0.10 },
                { nombre: '4. Ejecución', pct: 0.40 },
                { nombre: '5. Calidad', pct: 0.10 },
                { nombre: '6. Comunicaciones', pct: 0.10 },
                { nombre: '7. Cierre', pct: 0.10 }
            ];

        let fechaCursor = new Date(datosProyecto.fecha_inicio);
        const nuevasFases = items.map((item, idx) => {
            const diasFase = Math.ceil(datosProyecto.duracion_total * item.pct);
            const fechaFin = new Date(fechaCursor);
            fechaFin.setDate(fechaFin.getDate() + diasFase);

            const fase = {
                id: idx + 1,
                nombre: item.nombre,
                fecha_inicio: fechaCursor.toLocaleDateString(),
                fecha_fin: fechaFin.toLocaleDateString(),
                duracion_dias: diasFase
            };

            fechaCursor = new Date(fechaFin);
            return fase;
        });

        setFasesCalculadas(nuevasFases);
        setExito('✅ Fases recalculadas correctamente');
        setTimeout(() => setExito(''), 3000);
    };

    // DATOS MOCK
    const servicios = [
        { id: 'electricidad', nombre: '⚡ Electricidad', icon: Zap },
        { id: 'itse', nombre: '📋 Certificado ITSE', icon: CheckSquare },
        { id: 'puesta-tierra', nombre: '🔌 Puesta a Tierra', icon: Zap },
        { id: 'contra-incendios', nombre: '🔥 Contra Incendios', icon: AlertCircle },
        { id: 'domotica', nombre: '🏠 Domótica', icon: Home },
        { id: 'cctv', nombre: '📹 CCTV', icon: Users },
        { id: 'redes', nombre: '🌐 Redes', icon: TrendingUp },
        { id: 'automatizacion-industrial', nombre: '⚙️ Automatización', icon: Users },
        { id: 'expedientes', nombre: '📄 Expedientes', icon: FileText },
        { id: 'saneamiento', nombre: '💧 Saneamiento', icon: TrendingUp }
    ];

    const industrias = [
        { id: 'construccion', nombre: '🏗️ Construcción' },
        { id: 'arquitectura', nombre: '🏢 Arquitectura' },
        { id: 'industrial', nombre: '⚙️ Industrial' },
        { id: 'mineria', nombre: '⛏️ Minería' },
        { id: 'educacion', nombre: '🎓 Educación' },
        { id: 'salud', nombre: '🏥 Salud' },
        { id: 'retail', nombre: '🏪 Retail' },
        { id: 'residencial', nombre: '🏘️ Residencial' }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6 animate-fadeIn">
            <div className="max-w-7xl mx-auto space-y-8 pb-32">

                {/* HEADER */}
                <div className="bg-gradient-to-r from-red-950 via-red-900 to-black p-6 rounded-2xl border-2 border-yellow-600 shadow-2xl flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-bold text-yellow-500 flex items-center gap-3">
                            <Layout className="w-8 h-8" />
                            Proyecto Complejo
                        </h1>
                        <p className="text-gray-400 mt-1">Gantt, hitos y seguimiento avanzado - Configuración Inicial</p>
                    </div>
                    <div className="flex gap-4">
                        <div className="flex items-center gap-2">
                            {[1, 2, 3].map(step => (
                                <div key={step} className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${step === 1 ? 'bg-yellow-600 text-black' : 'border border-gray-600'}`}>
                                    {step}
                                </div>
                            ))}
                        </div>
                        <button onClick={onBack} className="px-4 py-2 border border-red-500 text-red-400 rounded-lg hover:bg-red-900/30">
                            Inicio
                        </button>
                    </div>
                </div>

                {/* ALERTA */}
                {(error || exito) && (
                    <div className={`p-4 rounded-xl border flex items-center gap-3 ${error ? 'bg-red-900/50 border-red-600 text-red-200' : 'bg-green-900/50 border-green-600 text-green-200'}`}>
                        {error ? <AlertCircle /> : <CheckCircle />}
                        {error || exito}
                    </div>
                )}

                {/* 1. LOGO */}
                <div className="bg-black/40 backdrop-blur-md rounded-2xl p-6 border-2 border-yellow-600 shadow-xl">
                    <h2 className="text-xl font-bold mb-4 text-yellow-400 flex items-center gap-2">
                        🎨 Logo Empresa (Aparecerá en el documento final)
                    </h2>
                    <button
                        onClick={() => fileInputLogoRef.current.click()}
                        className="w-full bg-gradient-to-r from-yellow-600 to-yellow-500 hover:from-yellow-500 hover:to-yellow-400 text-black font-bold py-3 rounded-xl shadow-lg transition-all flex justify-center items-center gap-2"
                    >
                        <Upload className="w-5 h-5" />
                        {datosProyecto.logo ? 'Cambiar Logo' : 'Subir Logo'}
                    </button>
                    <input ref={fileInputLogoRef} type="file" className="hidden" accept="image/*" onChange={handleLogoUpload} />
                    <p className="text-center text-xs text-gray-500 mt-2">PNG, JPG, WebP - Máx 2MB</p>
                </div>

                {/* 2. DATOS CLIENTE */}
                <div className="bg-black/40 backdrop-blur-md rounded-2xl p-6 border-2 border-yellow-600 shadow-xl">
                    <h2 className="text-xl font-bold mb-6 text-yellow-400 flex items-center gap-2">
                        <Users className="w-5 h-5" /> Datos del Cliente
                    </h2>

                    {/* Selector Cliente (Simulado) */}
                    <div className="mb-4">
                        <label className="block text-yellow-500 font-bold mb-2">Seleccionar Cliente</label>
                        <select className="w-full bg-gray-900 border border-yellow-700/50 rounded-xl p-3 text-gray-300">
                            <option>+ Nuevo Cliente</option>
                        </select>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="text-yellow-500 font-bold text-sm">Nombre/Razón Social *</label>
                            <input
                                name="nombre"
                                value={datosProyecto.cliente?.nombre || ''}
                                onChange={handleClienteChange}
                                className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 mt-1 text-white focus:border-yellow-500 outline-none"
                                placeholder="Ej: Constructora ABC S.A.C."
                            />
                        </div>
                        <div>
                            <label className="text-yellow-500 font-bold text-sm">RUC *</label>
                            <input
                                name="ruc"
                                value={datosProyecto.cliente?.ruc || ''}
                                onChange={handleClienteChange}
                                className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 mt-1 text-white focus:border-yellow-500 outline-none"
                                placeholder="11 dígitos"
                            />
                        </div>
                        <div className="md:col-span-2">
                            <label className="text-yellow-500 font-bold text-sm">Dirección</label>
                            <input
                                name="direccion"
                                value={datosProyecto.cliente?.direccion || ''}
                                onChange={handleClienteChange}
                                className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 mt-1 text-white focus:border-yellow-500 outline-none"
                            />
                        </div>
                        <div>
                            <label className="text-yellow-500 font-bold text-sm">Teléfono</label>
                            <input
                                name="telefono"
                                value={datosProyecto.cliente?.telefono || ''}
                                onChange={handleClienteChange}
                                className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 mt-1 text-white focus:border-yellow-500 outline-none"
                            />
                        </div>
                        <div>
                            <label className="text-yellow-500 font-bold text-sm">Email</label>
                            <input
                                name="email"
                                value={datosProyecto.cliente?.email || ''}
                                onChange={handleClienteChange}
                                className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 mt-1 text-white focus:border-yellow-500 outline-none"
                            />
                        </div>
                    </div>
                </div>

                {/* 3. INFO PROYECTO & CRONOGRAMA */}
                <div className="bg-black/40 backdrop-blur-md rounded-2xl p-6 border-2 border-blue-600/50 shadow-xl">
                    <h2 className="text-xl font-bold mb-6 text-blue-400 flex items-center gap-2">
                        <FileText className="w-5 h-5" /> Información del Proyecto
                    </h2>

                    <div className="space-y-6">
                        {/* Nombre y Presupuesto */}
                        <div>
                            <label className="text-blue-400 font-bold text-sm">Nombre del Proyecto *</label>
                            <input
                                value={datosProyecto.nombre_proyecto || ''}
                                onChange={(e) => handleDatosProyectoChange('nombre_proyecto', e.target.value)}
                                className="w-full bg-gray-900 border border-blue-900 rounded-xl p-3 text-lg font-bold text-white mt-1 focus:border-blue-500 outline-none"
                                placeholder="Ej: Instalación Eléctrica Edificio Central"
                            />
                        </div>

                        <div className="flex gap-4">
                            <div className="flex-1">
                                <label className="text-blue-400 font-bold text-sm">Presupuesto Estimado</label>
                                <input
                                    type="number"
                                    value={datosProyecto.presupuesto || ''}
                                    onChange={(e) => handleDatosProyectoChange('presupuesto', e.target.value)}
                                    className="w-full bg-gray-900 border border-blue-900 rounded-xl p-3 text-white mt-1 focus:border-blue-500 outline-none"
                                    placeholder="50000"
                                />
                            </div>
                            <div className="w-1/3">
                                <label className="text-blue-400 font-bold text-sm">Moneda</label>
                                <select
                                    value={datosProyecto.moneda || 'PEN'}
                                    onChange={(e) => handleDatosProyectoChange('moneda', e.target.value)}
                                    className="w-full bg-gray-900 border border-blue-900 rounded-xl p-3 text-white mt-1"
                                >
                                    <option value="PEN">S/ (PEN)</option>
                                    <option value="USD">$ (USD)</option>
                                </select>
                            </div>
                        </div>

                        {/* GRID CONFIGURACION & FASES */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-4 border-t border-blue-900/30">

                            {/* IZQUIERDA: CALENDARIO */}
                            <div>
                                <CalendarioProyecto
                                    onChange={(datos) => {
                                        onUpdateDatos({
                                            ...datosProyecto,
                                            datosCalendario: datos,
                                            fecha_inicio: datos.fechaInicio,
                                            duracion_total: datos.duracion_dias
                                        });
                                    }}
                                    valoresIniciales={{
                                        fechaInicio: datosProyecto.fecha_inicio ? new Date(datosProyecto.fecha_inicio) : new Date(),
                                        duracionMeses: Math.ceil((datosProyecto.duracion_total || 30) / 30),
                                        usarDiasHabiles: true
                                    }}
                                />

                                {/* CHECKLIST ALCANCE */}
                                <div className="mt-6 border-t border-blue-800 pt-6">
                                    <h3 className="text-lg font-bold text-blue-300 mb-4 flex items-center gap-2">
                                        <CheckSquare className="w-4 h-4" /> Definir Alcance del Proyecto
                                    </h3>

                                    <div className="flex gap-2 mb-4">
                                        <button
                                            onClick={() => { setComplejidad(5); setEtapasSeleccionadas(['acta', 'stakeholders', 'cronograma', 'cierre']); }}
                                            className={`flex-1 p-3 rounded-lg border transition-all ${complejidad === 5 ? 'bg-blue-600 border-blue-400' : 'bg-gray-900 border-gray-700 text-gray-400'}`}
                                        >
                                            <div className="font-bold">5 Fases - Básico</div>
                                            <div className="text-xs">Proyectos estándar</div>
                                        </button>
                                        <button
                                            onClick={() => { setComplejidad(7); setEtapasSeleccionadas(['acta', 'stakeholders', 'riesgos', 'cronograma', 'calidad', 'comms', 'cierre']); }}
                                            className={`flex-1 p-3 rounded-lg border transition-all ${complejidad === 7 ? 'bg-purple-600 border-purple-400' : 'bg-gray-900 border-gray-700 text-gray-400'}`}
                                        >
                                            <div className="font-bold">7 Fases - Avanzado</div>
                                            <div className="text-xs">Gestión integral PMI</div>
                                        </button>
                                    </div>

                                    {/* GRID CHECKBOXES */}
                                    <div className="grid grid-cols-2 gap-2">
                                        {(complejidad === 5
                                            ? ['Acta Constitución', 'Cronograma', 'Cierre', 'Stakeholders']
                                            : ['Acta Constitución', 'Interesados', 'Riesgos', 'Cronograma', 'Calidad', 'Comunicaciones', 'Cierre']
                                        ).map(label => (
                                            <div key={label} className="bg-gray-950 p-2 rounded border border-gray-800 flex items-center gap-2">
                                                <div className="w-4 h-4 bg-blue-500 rounded flex items-center justify-center text-[10px] text-white">✓</div>
                                                <span className="text-sm text-gray-300">{label}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* METRADO */}
                                <div className="mt-6 border-t border-blue-800 pt-6 bg-gray-900/50 rounded-xl p-4">
                                    <div className="flex justify-between items-center">
                                        <div>
                                            <p className="font-bold text-white">¿Definir Metrado Total?</p>
                                            <p className="text-xs text-gray-400">Especificar área total (m²)</p>
                                        </div>
                                        <button
                                            onClick={() => setIncluirMetrado(!incluirMetrado)}
                                            className={`w-12 h-6 rounded-full transition-colors relative ${incluirMetrado ? 'bg-blue-600' : 'bg-gray-700'}`}
                                        >
                                            <div className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${incluirMetrado ? 'translate-x-6' : ''}`} />
                                        </button>
                                    </div>
                                    {incluirMetrado && (
                                        <input
                                            type="number"
                                            value={areaMetrado}
                                            onChange={(e) => setAreaMetrado(e.target.value)}
                                            className="w-full mt-3 bg-gray-950 border border-blue-700 rounded-lg p-2 text-white font-bold"
                                            placeholder="Ej: 150"
                                        />
                                    )}
                                </div>
                            </div>

                            {/* DERECHA: FASES Y RESUMEN */}
                            <div className="space-y-6">
                                <div className="flex justify-between items-center mb-2">
                                    <h3 className="text-xl font-bold text-blue-300">Cronograma Preliminar</h3>
                                    <button onClick={calcularCronogramaPreliminar} className="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1 rounded-lg text-sm font-bold shadow-lg transition-transform hover:scale-105">
                                        🔄 Recalcular Fases
                                    </button>
                                </div>

                                {fasesCalculadas.length > 0 ? (
                                    <div className="space-y-3 max-h-[500px] overflow-y-auto pr-2">
                                        {fasesCalculadas.map((fase) => (
                                            <div key={fase.id} className="bg-gray-900 p-3 rounded-xl border border-blue-900/50 hover:border-blue-500 transition-colors">
                                                <div className="flex justify-between mb-2">
                                                    <div className="flex items-center gap-3">
                                                        <div className="w-6 h-6 rounded-full bg-blue-900 text-blue-300 flex items-center justify-center font-bold text-xs">{fase.id}</div>
                                                        <span className="font-semibold text-sm">{fase.nombre}</span>
                                                    </div>
                                                    <div className="bg-black/30 px-2 rounded text-blue-200 text-sm font-mono">{fase.duracion_dias} días</div>
                                                </div>
                                                {/* Slider Simulado */}
                                                <div className="w-full h-1 bg-gray-800 rounded-full mt-2 relative">
                                                    <div className="absolute left-0 top-0 h-full bg-blue-500 rounded-full" style={{ width: '60%' }}></div>
                                                    <div className="absolute top-[-4px] left-[60%] w-3 h-3 bg-white rounded-full shadow cursor-pointer hover:scale-125 transition-transform"></div>
                                                </div>
                                                <div className="text-[10px] text-gray-500 mt-1 flex justify-between">
                                                    <span>{fase.fecha_inicio}</span>
                                                    <span>{fase.fecha_fin}</span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <div className="border-2 border-dashed border-gray-700 rounded-xl p-8 text-center text-gray-500">
                                        <Calendar className="w-12 h-12 mx-auto mb-2 opacity-50" />
                                        <p>No se han generado fases aún</p>
                                    </div>
                                )}

                                {/* RESUMEN */}
                                <ProyectoResumen
                                    datos={{ ...datosProyecto, duracion_dias: datosProyecto.duracion_total }}
                                    fases={fasesCalculadas}
                                    usarDiasHabiles={true}
                                />
                            </div>
                        </div>
                    </div>
                </div>

                {/* 4. SERVICIO E INDUSTRIA */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-black/40 backdrop-blur-md rounded-2xl p-6 border-2 border-green-600/30 shadow-xl">
                        <h2 className="text-xl font-bold mb-4 text-green-400">⚙️ Servicio</h2>
                        <div className="grid grid-cols-2 gap-3">
                            {servicios.map(s => (
                                <button
                                    key={s.id}
                                    onClick={() => handleDatosProyectoChange('servicio', s.id)}
                                    className={`p-3 rounded-lg border text-left transition-all ${datosProyecto.servicio === s.id ? 'bg-green-900 border-green-500 text-white' : 'bg-gray-900 border-gray-700 text-gray-400'}`}
                                >
                                    <div className="text-xl mb-1">{s.id === 'electricidad' ? '⚡' : '🔧'}</div>
                                    <div className="text-xs font-bold">{s.nombre}</div>
                                </button>
                            ))}
                        </div>
                    </div>
                    <div className="bg-black/40 backdrop-blur-md rounded-2xl p-6 border-2 border-orange-600/30 shadow-xl">
                        <h2 className="text-xl font-bold mb-4 text-orange-400">🏭 Industria</h2>
                        <div className="grid grid-cols-2 gap-3">
                            {industrias.map(i => (
                                <button
                                    key={i.id}
                                    onClick={() => handleDatosProyectoChange('industria', i.id)}
                                    className={`p-3 rounded-lg border text-left transition-all ${datosProyecto.industria === i.id ? 'bg-orange-900 border-orange-500 text-white' : 'bg-gray-900 border-gray-700 text-gray-400'}`}
                                >
                                    <div className="text-xl mb-1">🏭</div>
                                    <div className="text-xs font-bold">{i.nombre}</div>
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                {/* 5. DESCRIPCIÓN & DOCS */}
                <div className="bg-black/40 backdrop-blur-md rounded-2xl p-6 border-2 border-purple-600/30 shadow-xl">
                    <h2 className="text-xl font-bold mb-4 text-purple-400">📝 Descripción Detallada</h2>
                    <textarea
                        value={datosProyecto.descripcion_inicial || ''}
                        onChange={(e) => handleDatosProyectoChange('descripcion_inicial', e.target.value)}
                        className="w-full bg-gray-900 border border-yellow-700/50 rounded-xl p-4 text-white h-32 focus:border-yellow-500 outline-none resize-none"
                        placeholder="Describe los objetivos y alcance del proyecto..."
                    />

                    <div className="mt-6 border-t border-gray-800 pt-4">
                        <label className="block text-gray-300 font-bold mb-2">Documentos (Opcional)</label>
                        <div
                            onClick={() => fileInputRef.current.click()}
                            className="border-2 border-dashed border-gray-700 rounded-xl p-8 hover:border-yellow-500 cursor-pointer transition-colors flex flex-col items-center justify-center bg-gray-900/50"
                        >
                            <Upload className="w-8 h-8 text-yellow-500 mb-2" />
                            <p className="text-gray-400 text-sm">Sube documentos (Máx 10MB)</p>
                        </div>
                        <input ref={fileInputRef} type="file" multiple className="hidden" onChange={handleFileUpload} />

                        {datosProyecto.archivos?.length > 0 && (
                            <div className="mt-4 space-y-2">
                                {datosProyecto.archivos.map((f, i) => (
                                    <div key={i} className="flex justify-between items-center bg-gray-900 p-2 rounded border border-gray-800">
                                        <span className="text-xs text-gray-300">{f.name}</span>
                                        <X className="w-4 h-4 text-red-500 cursor-pointer" />
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>

                {/* FOOTER ACTIONS */}
                <div className="fixed bottom-0 left-0 right-0 bg-black/95 border-t border-yellow-800 p-4 z-50 flex justify-between items-center backdrop-blur-lg">
                    <span className="text-gray-400 text-sm hidden md:block">* Completa los campos obligatorios para continuar</span>
                    <div className="flex gap-4 w-full md:w-auto">
                        <button
                            onClick={() => guardarBorrador && guardarBorrador(datosProyecto)}
                            className="flex-1 md:flex-none bg-gray-800 hover:bg-gray-700 text-white px-6 py-3 rounded-xl font-bold border border-gray-600 flex items-center justify-center gap-2 transition-all"
                        >
                            <Save className="w-4 h-4" /> Guardar Borrador
                        </button>
                        <button
                            onClick={onNext}
                            disabled={!datosProyecto.nombre_proyecto || !datosProyecto.cliente?.nombre}
                            className="flex-1 md:flex-none bg-gradient-to-r from-yellow-600 to-yellow-500 hover:to-yellow-400 text-black px-8 py-3 rounded-xl font-bold shadow-lg shadow-yellow-900/50 flex items-center justify-center gap-2 transition-transform hover:scale-105 disabled:opacity-50 disabled:scale-100"
                        >
                            <MessageSquare className="w-5 h-5" />
                            Comenzar Planificación
                        </button>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default ConfiguracionProyectoComplejo;
