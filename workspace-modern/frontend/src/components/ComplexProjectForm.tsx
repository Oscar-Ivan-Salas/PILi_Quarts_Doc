
import React, { useState, useRef } from 'react';
import { Upload, FileText, Users, MessageSquare, Zap, Folder, ArrowDown, Building2, MapPin, Phone, Mail, Save, Loader, Video, Settings, School, ShoppingBag, HeartPulse } from 'lucide-react';

// --- DATA CONSTANTS (Direct copy from App.jsx) ---
const servicios = [
    { id: 'electricidad', nombre: 'Electricidad', icon: <Zap className="w-8 h-8" />, descripcion: 'Instalaciones eléctricas completas' },
    { id: 'itse', nombre: 'Certificado ITSE', icon: <FileText className="w-8 h-8" />, descripcion: 'Inspección técnica de seguridad' },
    { id: 'puesta-tierra', nombre: 'Puesta a Tierra', icon: <ArrowDown className="w-8 h-8" />, descripcion: 'Sistemas de protección eléctrica' },
    { id: 'contra-incendios', nombre: 'Contra Incendios', icon: <div className="text-3xl">🔥</div>, descripcion: 'Sistemas de detección y extinción' },
    { id: 'domotica', nombre: 'Domótica', icon: <div className="text-3xl">🏠</div>, descripcion: 'Automatización inteligente' },
    { id: 'cctv', nombre: 'CCTV', icon: <Video className="w-8 h-8" />, descripcion: 'Videovigilancia profesional' },
    { id: 'redes', nombre: 'Redes', icon: <div className="text-3xl">🌐</div>, descripcion: 'Cableado estructurado' },
    { id: 'automatizacion-industrial', nombre: 'Automatización Ind.', icon: <Settings className="w-8 h-8" />, descripcion: 'PLCs y control de procesos' },
    { id: 'expedientes', nombre: 'Expedientes Técnicos', icon: <FileText className="w-8 h-8" />, descripcion: 'Documentación técnica profesional' },
    { id: 'saneamiento', nombre: 'Saneamiento', icon: <div className="text-3xl">💧</div>, descripcion: 'Sistemas de agua y desagüe' }
];

const industrias = [
    { id: 'construccion', nombre: 'Construcción', icon: <div className="text-xl">🏗️</div> },
    { id: 'arquitectura', nombre: 'Arquitectura', icon: <Building2 className="w-5 h-5" /> },
    { id: 'industrial', nombre: 'Industrial', icon: <Settings className="w-5 h-5" /> },
    { id: 'mineria', nombre: 'Minería', icon: <div className="text-xl">⛏️</div> },
    { id: 'educacion', nombre: 'Educación', icon: <School className="w-5 h-5" /> },
    { id: 'salud', nombre: 'Salud', icon: <HeartPulse className="w-5 h-5" /> },
    { id: 'retail', nombre: 'Retail', icon: <ShoppingBag className="w-5 h-5" /> },
    { id: 'residencial', nombre: 'Residencial', icon: <Folder className="w-5 h-5" /> },
];

const proyectosMock = [
    { id: 'PROJ-2025-001', nombre: 'Instalación Eléctrica Torre Office', cliente: 'Constructora Lima', tipo: 'electricidad' },
    { id: 'PROJ-2025-002', nombre: 'Sistema CCTV Planta Industrial', cliente: 'Industrial Perú S.A.', tipo: 'cctv' },
    // ...
];

interface ComplexProjectFormProps {
    onStartChat: (data: any) => void;
    initialData?: any;
    tipoFlujo?: string; // 'cotizacion-simple', 'proyecto-complejo', 'informe-ejecutivo', etc.
}

export function ComplexProjectForm({ onStartChat, initialData = {}, tipoFlujo = 'cotizacion-compleja' }: ComplexProjectFormProps) {
    // --- STATE ---
    const [logoBase64, setLogoBase64] = useState<string | null>(null);
    const fileInputLogoRef = useRef<HTMLInputElement>(null);
    const [datosCliente, setDatosCliente] = useState({
        nombre: initialData.cliente?.nombre || '',
        ruc: initialData.cliente?.ruc || '',
        direccion: initialData.cliente?.direccion || '',
        telefono: initialData.cliente?.telefono || '',
        email: initialData.cliente?.email || ''
    });
    const [clienteSeleccionadoId, setClienteSeleccionadoId] = useState('');
    const [guardandoCliente, setGuardandoCliente] = useState(false);

    // Project Specific
    const [nombreProyecto, setNombreProyecto] = useState(initialData.proyecto?.nombre || '');
    const [presupuesto, setPresupuesto] = useState(initialData.proyecto?.presupuesto || '');
    const [moneda, setMoneda] = useState(initialData.proyecto?.moneda || 'PEN');

    // Informe Specific
    const [proyectoSeleccionado, setProyectoSeleccionado] = useState('');
    const [formatoInforme, setFormatoInforme] = useState('word');

    // Universal
    const [servicioSeleccionado, setServicioSeleccionado] = useState(initialData.servicio || '');
    const [industriaSeleccionada, setIndustriaSeleccionada] = useState(initialData.industria || '');
    const [contextoUsuario, setContextoUsuario] = useState(initialData.descripcion || '');
    const [archivos, setArchivos] = useState<any[]>([]);

    // Determine type capabilities
    const esProyecto = tipoFlujo.includes('proyecto');
    const esInforme = tipoFlujo.includes('informe');

    // --- HANDLERS ---
    const cargarLogo = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = (ev) => setLogoBase64(ev.target?.result as string);
            reader.readAsDataURL(e.target.files[0]);
        }
    };

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setArchivos([...archivos, ...Array.from(e.target.files).map(f => ({ nombre: f.name, size: f.size }))]);
        }
    };

    const guardarCliente = () => {
        setGuardandoCliente(true);
        setTimeout(() => setGuardandoCliente(false), 1500); // Mock save
    };

    const handleSubmit = () => {
        onStartChat({
            cliente: datosCliente,
            proyecto: {
                nombre: nombreProyecto,
                presupuesto,
                moneda,
                base: proyectoSeleccionado
            },
            servicio: servicioSeleccionado,
            industria: industriaSeleccionada,
            descripcion: contextoUsuario,
            archivos,
            config: {
                logo: logoBase64,
                formato: formatoInforme
            }
        });
    };

    // --- RENDER ---
    return (
        <div className="max-w-5xl mx-auto space-y-6 pb-20 font-sans">

            {/* 0. LOGO EMPRESA (Universal) */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-600 shadow-xl">
                <h2 className="text-2xl font-bold mb-4 text-yellow-400 flex items-center gap-2">
                    🎨 Logo Empresa (Aparecerá en el documento final)
                </h2>
                <div className="flex gap-4 items-center">
                    <div className="flex-1">
                        <input ref={fileInputLogoRef} type="file" onChange={cargarLogo} className="hidden" accept="image/*" />
                        <button
                            onClick={() => fileInputLogoRef.current?.click()}
                            className="w-full bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 text-black px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-xl border-2 border-yellow-400 transition-all duration-300 hover:scale-105">
                            <Upload className="w-5 h-5" />
                            {logoBase64 ? 'Cambiar Logo' : 'Subir Logo'}
                        </button>
                    </div>
                    {logoBase64 && (
                        <div className="bg-white rounded-xl p-3 border-2 border-yellow-400 shadow-lg">
                            <img src={logoBase64} alt="Logo" className="w-24 h-24 object-contain" />
                        </div>
                    )}
                </div>
            </div>

            {/* 1. DATOS DEL CLIENTE (Universal Form) */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-600 shadow-xl">
                <h2 className="text-2xl font-bold mb-6 text-yellow-400 flex items-center gap-3">
                    <Users className="w-7 h-7" /> Datos del Cliente
                </h2>

                {/* Cliente Selector */}
                <div className="mb-6">
                    <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2">
                        <Building2 className="w-5 h-5" /> Seleccionar Cliente
                    </label>
                    <select
                        value={clienteSeleccionadoId}
                        onChange={e => setClienteSeleccionadoId(e.target.value)}
                        className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white appearance-none"
                    >
                        <option value="">+ Nuevo Cliente</option>
                        <option value="1">Cliente Demo 1</option>
                    </select>
                </div>

                {/* Fields Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div>
                        <label className="block text-yellow-400 font-semibold mb-2">Nombre/Razón Social *</label>
                        <input
                            value={datosCliente.nombre}
                            onChange={e => setDatosCliente({ ...datosCliente, nombre: e.target.value })}
                            className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white placeholder-gray-600"
                            placeholder="Ej: Constructora ABC S.A.C."
                        />
                    </div>
                    <div>
                        <label className="block text-yellow-400 font-semibold mb-2">RUC *</label>
                        <input
                            value={datosCliente.ruc}
                            onChange={e => setDatosCliente({ ...datosCliente, ruc: e.target.value })}
                            className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white placeholder-gray-600"
                            placeholder="11 dígitos"
                        />
                    </div>
                    <div className="md:col-span-2">
                        <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2"><MapPin className="w-4 h-4" /> Dirección</label>
                        <input
                            value={datosCliente.direccion}
                            onChange={e => setDatosCliente({ ...datosCliente, direccion: e.target.value })}
                            className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white placeholder-gray-600"
                            placeholder="Ej: Av. Principal 123, Lima"
                        />
                    </div>
                    <div>
                        <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2"><Phone className="w-4 h-4" /> Teléfono</label>
                        <input
                            value={datosCliente.telefono}
                            onChange={e => setDatosCliente({ ...datosCliente, telefono: e.target.value })}
                            className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white placeholder-gray-600"
                            placeholder="Ej: 987654321"
                        />
                    </div>
                    <div>
                        <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2"><Mail className="w-4 h-4" /> Email</label>
                        <input
                            value={datosCliente.email}
                            onChange={e => setDatosCliente({ ...datosCliente, email: e.target.value })}
                            className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white placeholder-gray-600"
                            placeholder="cliente@empresa.com"
                        />
                    </div>
                </div>

                <button
                    onClick={guardarCliente}
                    disabled={guardandoCliente}
                    className="w-full bg-slate-800 hover:bg-slate-700 text-white px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 border border-slate-600 shadow-lg transition-all"
                >
                    {guardandoCliente ? <Loader className="animate-spin w-5 h-5" /> : <Save className="w-5 h-5" />}
                    {guardandoCliente ? 'Guardando...' : 'Guardar Cliente'}
                </button>
            </div>

            {/* 2. CONFIGURACIÓN ESPECÍFICA (Proyecto / Informe) */}
            {esProyecto && (
                <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-blue-700 shadow-xl">
                    <h2 className="text-2xl font-bold mb-4 text-blue-400">📋 Información del Proyecto</h2>
                    {/* Campos Proyecto... */}
                    <div className="space-y-4">
                        <input value={nombreProyecto} onChange={e => setNombreProyecto(e.target.value)} placeholder="Nombre del Proyecto" className="w-full px-4 py-3 bg-gray-950 border border-blue-700 rounded-xl text-white" />
                        <div className="grid grid-cols-2 gap-4">
                            <input type="number" value={presupuesto} onChange={e => setPresupuesto(e.target.value)} placeholder="Presupuesto" className="w-full px-4 py-3 bg-gray-950 border border-blue-700 rounded-xl text-white" />
                            <select value={moneda} onChange={e => setMoneda(e.target.value)} className="w-full px-4 py-3 bg-gray-950 border border-blue-700 rounded-xl text-white">
                                <option value="PEN">S/ (PEN)</option>
                                <option value="USD">$ (USD)</option>
                            </select>
                        </div>
                    </div>
                </div>
            )}

            {esInforme && (
                <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-green-700 shadow-xl">
                    <h2 className="text-2xl font-bold mb-4 text-green-400">📄 Configuración del Informe</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <select value={proyectoSeleccionado} onChange={e => setProyectoSeleccionado(e.target.value)} className="w-full px-4 py-3 bg-gray-950 border border-green-700 rounded-xl text-white">
                            <option value="">Seleccionar Proyecto...</option>
                            {proyectosMock.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
                        </select>
                        <select value={formatoInforme} onChange={e => setFormatoInforme(e.target.value)} className="w-full px-4 py-3 bg-gray-950 border border-green-700 rounded-xl text-white">
                            <option value="word">Word (Editable)</option>
                            <option value="pdf">PDF (Final)</option>
                        </select>
                    </div>
                </div>
            )}

            {/* 3. TIPO DE SERVICIO (Universal) */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-600 shadow-xl">
                <h2 className="text-2xl font-bold mb-4 text-yellow-400">⚙️ Tipo de Servicio</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {servicios.map(servicio => (
                        <button
                            key={servicio.id}
                            onClick={() => setServicioSeleccionado(servicio.id)}
                            className={`p-4 rounded-xl border-2 transition-all duration-300 text-left flex flex-col items-start gap-2 ${servicioSeleccionado === servicio.id
                                ? 'border-yellow-500 bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl scale-105'
                                : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800 text-gray-300'
                                }`}
                        >
                            <div className="text-yellow-400">{servicio.icon}</div>
                            <span className="font-bold text-sm block">{servicio.nombre}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* 4. INDUSTRIA (Nueva Sección Requerida) */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-600 shadow-xl">
                <h2 className="text-2xl font-bold mb-4 text-yellow-400 flex items-center gap-2">
                    <Building2 className="w-6 h-6" /> Industria
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {industrias.map(industria => (
                        <button
                            key={industria.id}
                            onClick={() => setIndustriaSeleccionada(industria.id)}
                            className={`p-4 rounded-xl border-2 transition-all duration-300 flex items-center justify-center gap-2 ${industriaSeleccionada === industria.id
                                ? 'border-yellow-500 bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl scale-105'
                                : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800 text-gray-300'
                                }`}
                        >
                            <div className="text-yellow-400">{industria.icon}</div>
                            <span className="font-bold text-sm">{industria.nombre}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* 5. DESCRIPCIÓN Y DOCUMENTOS */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-600 shadow-xl">
                <h2 className="text-2xl font-bold mb-4 text-yellow-400 flex items-center gap-2">
                    <FileText className="w-6 h-6" /> Descripción Detallada
                </h2>

                <textarea
                    value={contextoUsuario}
                    onChange={e => setContextoUsuario(e.target.value)}
                    className="w-full h-32 px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none resize-none mb-4 text-white placeholder-gray-500"
                    placeholder="Describe el proyecto a cotizar detalladamente..."
                />

                <div className="border-t-2 border-gray-800 pt-4">
                    <h3 className="text-lg font-semibold mb-3 text-gray-300">Documentos (Opcional)</h3>
                    <div className="border-2 border-dashed border-gray-700 rounded-xl p-6 text-center hover:border-yellow-600 transition-all cursor-pointer bg-gray-950/50">
                        <input type="file" multiple onChange={handleFileUpload} className="hidden" id="fileInput" />
                        <label htmlFor="fileInput" className="cursor-pointer block">
                            <Upload className="w-12 h-12 mx-auto mb-3 text-yellow-500" />
                            <p className="text-sm text-gray-400 font-semibold">Sube documentos (máx 10MB)</p>
                        </label>
                    </div>
                </div>
            </div>

            {/* 6. BOTÓN DE ACCIÓN */}
            <button
                onClick={handleSubmit}
                className="w-full bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 text-black py-4 rounded-xl font-bold text-lg shadow-2xl border-2 border-yellow-400 transition-all hover:scale-105 flex items-center justify-center gap-3"
            >
                <MessageSquare className="w-6 h-6" />
                Comenzar Chat con Vista Previa
            </button>
        </div>
    );
}
