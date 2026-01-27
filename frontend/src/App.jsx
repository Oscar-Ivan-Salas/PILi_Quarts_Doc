// @ts-nocheck
import React, { useState, useRef, useEffect } from 'react';
import { Upload, MessageSquare, FileText, Download, Zap, Send, Loader, Edit, Save, AlertCircle, CheckCircle, X, RefreshCw, Home, FolderOpen, Eye, EyeOff, Folder, Users, TrendingUp, Clock, BarChart3, FileCheck, Briefcase, ChevronDown, ChevronUp, Layout, Layers, BookOpen, Calculator, Calendar, Target, Archive, Settings, PieChart, Maximize2, Minimize2, Plus, Trash2, Building2, MapPin, Phone, Mail, CheckSquare } from 'lucide-react';
import PiliAvatar from './components/PiliAvatar';
import ChatIA from './components/ChatIA';
import AdminDashboard from './components/AdminDashboard';
import PiliITSEChat from './components/PiliITSEChat';
import PiliElectricidadChat from './components/PiliElectricidadChat';
import PiliPuestaTierraChat from './components/PiliPuestaTierraChat';
import PiliContraIncendiosChat from './components/PiliContraIncendiosChat';
import PiliDomoticaChat from './components/PiliDomoticaChat';
import PiliCCTVChat from './components/PiliCCTVChat';
import PiliRedesChat from './components/PiliRedesChat';
import PiliAutomatizacionChat from './components/PiliAutomatizacionChat';
import PiliExpedientesChat from './components/PiliExpedientesChat';
import PiliSaneamientoChat from './components/PiliSaneamientoChat';
import PiliElectricidadComplejoChat from './components/PiliElectricidadComplejoChat';
import PiliAutomatizacionComplejoChat from './components/PiliAutomatizacionComplejoChat';
import PiliContraIncendiosComplejoChat from './components/PiliContraIncendiosComplejoChat';
import PiliElectricidadProyectoSimpleChat from './components/PiliElectricidadProyectoSimpleChat';
import PiliElectricidadProyectoComplejoPMIChat from './components/PiliElectricidadProyectoComplejoPMIChat';
import VistaPreviaProfesional from './components/VistaPreviaProfesional';
import CalendarioProyecto from './components/CalendarioProyecto';
import ProyectoResumen from './components/ProyectoResumen';
import ModuloC from './components/ModuloProyectoComplejo';

// ============================================
// COMPONENTE ALERTA
// ============================================

const Alerta = ({ tipo, mensaje, onClose }) => {
  if (!mensaje) return null;
  const estilos = tipo === 'error' ? 'bg-red-900 border-red-600' : 'bg-green-900 border-green-600';
  const Icono = tipo === 'error' ? AlertCircle : CheckCircle;

  return (
    <div className={`${estilos} border-2 text-white px-4 py-3 rounded-lg mb-4 flex items-center justify-between backdrop-blur-sm bg-opacity-90`}>
      <div className="flex items-center gap-2">
        <Icono className="w-5 h-5" />
        <span>{mensaje}</span>
      </div>
      {onClose && <button onClick={onClose} className="text-white hover:text-gray-300">✕</button>}
    </div>
  );
};

const PILIQuartsApp = () => {
  // ============================================
  // ESTADOS PRINCIPALES
  // ============================================

  const [pantallaActual, setPantallaActual] = useState('inicio');
  const [tipoFlujo, setTipoFlujo] = useState(null);

  // Estados de menús expandibles
  const [menuCotizaciones, setMenuCotizaciones] = useState(false);
  const [menuProyectos, setMenuProyectos] = useState(false);
  const [menuInformes, setMenuInformes] = useState(false);

  // Dashboard State
  const [mostrarDashboard, setMostrarDashboard] = useState(false);
  const [dashboardData, setDashboardData] = useState(null);

  // Estados del flujo general
  const [paso, setPaso] = useState(1);
  const [archivos, setArchivos] = useState([]);
  const [conversacion, setConversacion] = useState([]);
  const [contextoUsuario, setContextoUsuario] = useState('');
  const [inputChat, setInputChat] = useState('');
  const [analizando, setAnalizando] = useState(false);
  const [error, setError] = useState('');
  const [exito, setExito] = useState('');
  const [servicioSeleccionado, setServicioSeleccionado] = useState('');
  const [industriaSeleccionada, setIndustriaSeleccionada] = useState('');
  const [descargando, setDescargando] = useState(null);
  const [logoBase64, setLogoBase64] = useState('');
  const [botonesContextuales, setBotonesContextuales] = useState([]);
  const [datosCalendario, setDatosCalendario] = useState(null);
  const [datosCronograma, setDatosCronograma] = useState({
    duracion_dias: 0,
    fecha_inicio: '',
    fecha_fin: '',
    duracion_horas: 0,
    horas_por_dia: 8
  });
  // ✅ NUEVO: Estado para configuración de Alcance PMI (Checklist)
  const [complejidad, setComplejidad] = useState(7);
  const [etapasSeleccionadas, setEtapasSeleccionadas] = useState([
    'acta_constitucion', 'stakeholders', 'riesgos', 'cronograma', 'calidad', 'comunicaciones', 'cierre'
  ]);
  // ✅ NUEVO: Estado para Metrado (m2)
  const [incluirMetrado, setIncluirMetrado] = useState(false);
  const [areaMetrado, setAreaMetrado] = useState('');

  // Estados para vista previa HTML editable
  const [htmlPreview, setHtmlPreview] = useState('');
  const [mostrarPreview, setMostrarPreview] = useState(false);
  const [modoEdicion, setModoEdicion] = useState(true);  // ✅ TRUE por defecto para mostrar tabla editable
  const [datosEditables, setDatosEditables] = useState(null);
  const [ocultarIGV, setOcultarIGV] = useState(false);
  const [ocultarPreciosUnitarios, setOcultarPreciosUnitarios] = useState(false);
  const [ocultarTotalesPorItem, setOcultarTotalesPorItem] = useState(false);

  // ✅ Estados para personalización de documentos (NEW)
  const [esquemaColores, setEsquemaColores] = useState('azul-tesla'); // azul-tesla, rojo-energia, verde-ecologico, personalizado
  const [fuenteDocumento, setFuenteDocumento] = useState('Calibri'); // Calibri, Arial, Times New Roman
  const [tamañoFuente, setTamañoFuente] = useState(11); // 10, 11, 12
  const [mostrarLogo, setMostrarLogo] = useState(true);
  const [logoUrl, setLogoUrl] = useState(null); // URL del logo subido
  const [posicionLogo, setPosicionLogo] = useState('center'); // left, center, right
  const [mostrarPanelPersonalizacion, setMostrarPanelPersonalizacion] = useState(false);

  // Estados específicos para cada tipo
  const [cotizacion, setCotizacion] = useState(null);
  const [proyecto, setProyecto] = useState(null);
  const [informe, setInforme] = useState(null);

  // Estados específicos para proyectos
  const [nombre_proyecto, setNombre_proyecto] = useState('');
  const [presupuesto, setPresupuesto] = useState('');
  const [moneda, setMoneda] = useState('PEN');
  const [duracion_total, setDuracion_total] = useState('');
  // ❌ ELIMINADO: clienteProyecto (usar datosCliente.nombre)

  // Estados específicos para informes
  const [proyectoSeleccionado, setProyectoSeleccionado] = useState('');
  const [formatoInforme, setFormatoInforme] = useState('word');
  const [incluirGraficos, setIncluirGraficos] = useState(true);

  // ✅ NUEVO: Estado para toggle de vistas (chat/split/preview)
  const [viewMode, setViewMode] = useState('split'); // 'chat' | 'split' | 'preview'

  // ✅ Estados universales de cliente (para todos los 6 tipos de documentos)
  const [datosCliente, setDatosCliente] = useState({
    nombre: '',
    ruc: '',
    direccion: '',
    telefono: '',
    email: ''
  });
  const [clienteSeleccionadoId, setClienteSeleccionadoId] = useState(null);
  const [listaClientes, setListaClientes] = useState([]);
  const [guardandoCliente, setGuardandoCliente] = useState(false);

  // ✅ NUEVO: ID del proyecto guardado en BD
  const [proyectoId, setProyectoId] = useState(null);

  // ✅ NUEVO: Estado para fases calculadas preliminares (Editable en Step 1)
  const [fasesCalculadas, setFasesCalculadas] = useState([]);

  // ✅ NUEVO: Estados para progreso de chat conversacional
  const [datosRecopilados, setDatosRecopilados] = useState([]);
  const [datosFaltantes, setDatosFaltantes] = useState([]);
  const [progresoChat, setProgresoChat] = useState('0/0');

  // ✅ NUEVO: Memoria temporal del chat para no perder conversación al volver
  const [chatMemory, setChatMemory] = useState({
    conversacion: [],
    conversationState: null,
    hasQuote: false,
    tipoChat: null
  });

  // Referencias
  const chatContainerRef = useRef(null);
  const fileInputLogoRef = useRef(null);
  const previewRef = useRef(null);

  // ✅ REF para datos editables - SIEMPRE actualizado (solución profesional)
  const datosEditablesRef = useRef(null);

  // ============================================
  // DATOS DE CONFIGURACIÓN
  // ============================================

  const [datosEmpresa] = useState({
    nombre: 'PILi_Quarts V1.0',
    ruc: '20601138787',
    direccion: 'Dpto de diseño GatoMichuy huacacayo peru',
    email: 'ingenieria.teslaelectricidad@gmail.com',
    ciudad: 'Huancayo, Junin - Perú'
  });

  const servicios = [
    { id: 'electricidad', nombre: '⚡ Electricidad', icon: '⚡', descripcion: 'Instalaciones eléctricas completas' },
    { id: 'itse', nombre: '📋 Certificado ITSE', icon: '📋', descripcion: 'Inspección técnica de seguridad' },
    { id: 'puesta-tierra', nombre: '🔌 Puesta a Tierra', icon: '🔌', descripcion: 'Sistemas de protección eléctrica' },
    { id: 'contra-incendios', nombre: '🔥 Contra Incendios', icon: '🔥', descripcion: 'Sistemas de detección y extinción' },
    { id: 'domotica', nombre: '🏠 Domótica', icon: '🏠', descripcion: 'Automatización inteligente' },
    { id: 'cctv', nombre: '📹 CCTV', icon: '📹', descripcion: 'Videovigilancia profesional' },
    { id: 'redes', nombre: '🌐 Redes', icon: '🌐', descripcion: 'Cableado estructurado' },
    { id: 'automatizacion-industrial', nombre: '⚙️ Automatización Industrial', icon: '⚙️', descripcion: 'PLCs y control de procesos' },
    { id: 'expedientes', nombre: '📄 Expedientes Técnicos', icon: '📄', descripcion: 'Documentación técnica profesional' },
    { id: 'saneamiento', nombre: '💧 Saneamiento', icon: '💧', descripcion: 'Sistemas de agua y desagüe' }
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

  const basePreciosUniversal = {
    electricidad: {
      'Punto luz empotrado': 15, 'Tomacorriente doble': 18, 'Interruptor simple': 12,
      'Tablero general trifásico': 2800, 'Tablero depto monofásico': 800,
      'Cable THW 2.5mm²': 2.0, 'Cable THW 4mm²': 3.08, 'Luminaria LED 18W': 45
    },
    'itse': {
      'Derecho municipal ITSE Bajo': 168.30, 'Derecho municipal ITSE Medio': 208.60,
      'Servicio técnico ITSE Bajo': 400, 'Servicio técnico ITSE Medio': 550
    },
    'puesta-tierra': {
      'Pozo tierra completo': 1760, 'Varilla copperweld': 85, 'Cable desnudo Cu': 12
    },
    'domotica': {
      'Interruptor inteligente': 120, 'Sensor movimiento': 80, 'Central domótica': 1500
    },
    'cctv': {
      'Cámara IP 2MP': 350, 'DVR 8 canales': 800, 'Disco duro 1TB': 180
    }
  };

  const proyectosMock = [
    { id: 'PROJ-2025-001', nombre: 'Instalación Eléctrica Torre Office', cliente: 'Constructora Lima', tipo: 'electricidad' },
    { id: 'PROJ-2025-002', nombre: 'Sistema CCTV Planta Industrial', cliente: 'Industrial Perú S.A.', tipo: 'cctv' },
    { id: 'PROJ-2025-003', nombre: 'Automatización Línea Producción', cliente: 'Manufactura XYZ', tipo: 'automatizacion-industrial' }
  ];

  // ============================================
  // FUNCIONES PRINCIPALES
  // ============================================

  // ✅ NUEVO: Guardar proyecto en BD antes de iniciar chat
  const guardarProyectoEnBD = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/proyectos/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nombre: nombre_proyecto,
          servicio: servicioSeleccionado,
          industria: industriaSeleccionada,
          cliente: datosCliente.nombre,
          descripcion: contextoUsuario,
          presupuesto: presupuesto ? parseFloat(presupuesto) : null,
          moneda: moneda,
          presupuesto: presupuesto ? parseFloat(presupuesto) : null,
          moneda: moneda,
          duracion_total: duracion_total ? parseInt(duracion_total) : null,
          // ✅ ENVIAR FASES PRELIMINARES SI EXISTEN
          cronograma_fases: fasesCalculadas.length > 0 ? fasesCalculadas : null
        })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Proyecto guardado en BD:', data);
        setProyectoId(data.id);
        return data.id;
      } else {
        console.error('❌ Error al guardar proyecto');
        return null;
      }
    } catch (error) {
      console.error('❌ Error guardando proyecto:', error);
      return null;
    }
  };

  const volverAlInicio = () => {
    setPantallaActual('inicio');
    setTipoFlujo(null);
    setPaso(1);
    setConversacion([]);
    setCotizacion(null);
    setProyecto(null);
    setInforme(null);
    setServicioSeleccionado('');
    setIndustriaSeleccionada('');
    setContextoUsuario('');
    setBotonesContextuales([]);
    setArchivos([]);
    setNombre_proyecto('');
    setDatosCliente({ nombre: '', ruc: '', direccion: '', telefono: '', email: '' });
    setPresupuesto('');
    setDuracion_total('');
    setProyectoSeleccionado('');
    setHtmlPreview('');
    setMostrarPreview(false);
    setDatosEditables(null);
    setExito('Sistema reiniciado');
    setTimeout(() => setExito(''), 2000);
    // ✅ NUEVO: Limpiar memoria del chat para evitar conflictos
    setChatMemory({});
  };

  const iniciarFlujo = (tipo) => {
    setTipoFlujo(tipo);
    setPantallaActual('flujo-pasos');
    setPaso(1);
    setConversacion([]);
    setCotizacion(null);
    setProyecto(null);
    setInforme(null);
    setHtmlPreview('');
    setMostrarPreview(false);
    setDatosEditables(null);
    datosEditablesRef.current = null;  // ✅ También limpiar ref
  };

  // ✅ FUNCIÓN HELPER: Actualizar datos editables (state + ref)
  const actualizarDatosEditables = (nuevosDatos) => {
    setDatosEditables(nuevosDatos);
    datosEditablesRef.current = nuevosDatos;  // ✅ Mantener ref sincronizado
    console.log('✅ Datos editables actualizados:', nuevosDatos);
    console.log('💰 Moneda en datos:', nuevosDatos?.moneda);
  };

  // ✅ FUNCIÓN DE GUARDADO DE BORRADOR (Draft System)
  const handleGuardarBorrador = async (dataToSave, currentId = null, silent = false) => {
    try {
      if (!silent) console.log('💾 Iniciando guardado de borrador...', dataToSave);

      const isUpdate = !!currentId;
      const url = isUpdate
        ? `http://localhost:8000/api/proyectos/${currentId}/draft`
        : 'http://localhost:8000/api/proyectos/draft';

      const method = isUpdate ? 'PATCH' : 'POST';

      const bodyData = {
        ...dataToSave,
        nombre_proyecto: dataToSave.nombre_proyecto || 'Proyecto Sin Título',
        cliente_nombre: dataToSave.cliente?.nombre || (typeof dataToSave.cliente === 'string' ? dataToSave.cliente : 'Cliente General'),
        servicio: servicioSeleccionado || 'electricidad',
        metadata_adicional: dataToSave
      };

      const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyData)
      });

      if (response.ok) {
        const saved = await response.json();
        if (!silent) console.log('✅ Borrador guardado exitosamente:', saved);

        if (saved.id && !currentId) {
          setProyectoId(saved.id); // Guardar ID para futuros updates
        }
        return saved;
      } else {
        console.error('❌ Error guardando borrador:', await response.text());
        return null;
      }
    } catch (error) {
      console.error('❌ Error de red al guardar borrador:', error);
      return null;
    }
  };

  // ============================================
  // ✅ FUNCIONES DE GESTIÓN DE CLIENTES
  // ============================================

  // Cargar lista de clientes desde la BD
  const cargarListaClientes = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/clientes/');
      if (response.ok) {
        const clientes = await response.json();
        setListaClientes(clientes);
      }
    } catch (error) {
      console.error('Error cargando clientes:', error);
    }
  };

  // Cargar datos de un cliente específico (auto-relleno)
  const cargarDatosCliente = async (e) => {
    const clienteId = e.target.value;

    if (!clienteId) {
      // Nuevo cliente - limpiar formulario
      setClienteSeleccionadoId(null);
      setDatosCliente({
        nombre: '',
        ruc: '',
        direccion: '',
        telefono: '',
        email: ''
      });
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/clientes/${clienteId}`);
      if (response.ok) {
        const cliente = await response.json();
        setClienteSeleccionadoId(cliente.id);
        setDatosCliente({
          nombre: cliente.nombre || '',
          ruc: cliente.ruc || '',
          direccion: cliente.direccion || '',
          telefono: cliente.telefono || '',
          email: cliente.email || ''
        });
        setExito('✅ Cliente cargado');
      }
    } catch (error) {
      // Error loading client
      setError('Error al cargar cliente');
    }
  };



  // ✅ NUEVO: Calcular cronograma preliminar (llamada al Backend Determinístico)
  const calcularCronogramaPreliminar = async () => {
    if (!duracion_total) return;

    try {
      console.log("🧮 Calculando cronograma preliminar...");
      const response = await fetch('http://localhost:8000/api/calculos/cronograma-pmi', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          duracion_total: parseInt(duracion_total),
          fecha_inicio: datosCalendario?.fecha_inicio || new Date().toISOString().split('T')[0]
        })
      });

      if (response.ok) {
        const data = await response.json();
        console.log("✅ Cronograma calculado:", data);
        setFasesCalculadas(data.fases);
      }
    } catch (error) {
      console.error("❌ Error calculando cronograma:", error);
    }
  };

  // Efecto para recalcular cuando cambia duración o fecha (con debounce)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (duracion_total > 0 && tipoFlujo === 'proyecto-complejo') {
        calcularCronogramaPreliminar();
      }
    }, 800);
    return () => clearTimeout(timer);
  }, [duracion_total, datosCalendario?.fecha_inicio]);

  // Guardar cliente en la BD
  const guardarCliente = async () => {
    // Validación básica
    if (!datosCliente.nombre || !datosCliente.ruc) {
      setError('Nombre y RUC son obligatorios');
      return;
    }

    if (datosCliente.ruc.length !== 11) {
      setError('El RUC debe tener 11 dígitos');
      return;
    }

    setGuardandoCliente(true);

    try {
      const url = clienteSeleccionadoId
        ? `http://localhost:8000/api/clientes/${clienteSeleccionadoId}`
        : 'http://localhost:8000/api/clientes/';

      const method = clienteSeleccionadoId ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datosCliente)
      });

      if (response.ok) {
        const clienteGuardado = await response.json();
        setClienteSeleccionadoId(clienteGuardado.id);
        await cargarListaClientes(); // Recargar lista
        setExito(clienteSeleccionadoId ? '✅ Cliente actualizado' : '✅ Cliente guardado');
      } else {
        const errorData = await response.json();
        console.error('❌ Error del backend:', errorData);
        console.error('📋 Datos enviados:', datosCliente);
        throw new Error(JSON.stringify(errorData.detail || errorData) || 'Error al guardar');
      }
    } catch (error) {
      console.error('Error guardando cliente:', error);
      setError(error.message || 'Error al guardar cliente');
    } finally {
      setGuardandoCliente(false);
    }
  };

  /**
   * ✅ MANEJAR CAMBIOS DESDE LA VISTA PREVIA (Bidireccional)
   * Recibe el objeto completo de datos actualizado desde VistaPreviaProfesional
   */
  const handleDatosChange = (nuevosDatos) => {
    // 0. Sincronización inmediata de Referencia y Estado Local (Vital para descargas)
    setDatosEditables(nuevosDatos);
    datosEditablesRef.current = nuevosDatos;

    console.log('🔄 Sincronizando desde Preview:', nuevosDatos);

    // 1. Identificar qué estamos editando
    const esProyectoComplejo = tipoFlujo === 'proyecto-complejo';
    const esCotizacionCompleja = tipoFlujo === 'cotizacion-compleja';

    // 2. Actualizar el estado principal correspondiente (Source of Truth)
    // 2. Actualizar el estado principal correspondiente (Source of Truth)
    if (esProyectoComplejo) {
      setProyecto(nuevosDatos);

      // ✅ Sincronizar estados primitivos que usa el Chatbot
      if (nuevosDatos.duracion_total) setDuracion_total(nuevosDatos.duracion_total);
      if (nuevosDatos.presupuesto) setPresupuesto(nuevosDatos.presupuesto);
      if (nuevosDatos.nombre_proyecto) setNombre_proyecto(nuevosDatos.nombre_proyecto);
      if (nuevosDatos.moneda) setMoneda(nuevosDatos.moneda);

    } else if (esCotizacionCompleja) {
      setCotizacion(nuevosDatos);
    } else if (tipoFlujo === 'informe-tecnico') {
      setInforme(nuevosDatos);
    }

    // 3. Sincronizar Datos del Cliente (hacia atrás - Sidebar)
    // Si editamos el cliente en el Preview, que se refleje en la izquierda
    if (nuevosDatos.cliente) {
      const c = nuevosDatos.cliente;
      setDatosCliente(prev => ({
        ...prev,
        nombre: c.nombre || prev.nombre,
        ruc: c.ruc || prev.ruc,
        direccion: c.direccion || prev.direccion,
        telefono: c.telefono || prev.telefono,
        email: c.email || prev.email
      }));
    }

    // 4. Persistencia (Debounced) - Borrador de Proyecto
    // Solo si hay un ID de borrador activo y estamos en modo proyecto
    if (proyectoId && (tipoFlujo.includes('proyecto') || tipoFlujo.includes('complejo'))) {
      if (window.saveTimeout) clearTimeout(window.saveTimeout);

      window.saveTimeout = setTimeout(async () => {
        try {
          console.log('💾 Auto-guardando cambios manuales (Draft Sync)...');
          // Enviar SOLO si hay ID
          const response = await fetch(`http://localhost:8000/api/proyectos/${proyectoId}/draft`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              ...nuevosDatos,
              metadata_adicional: nuevosDatos
            })
          });

          if (response.ok) {
            console.log('✅ Cambios sincronizados con el borrador.');
          } else {
            console.error('❌ Error sincronizando borrador:', await response.text());
          }
        } catch (e) {
          console.error('❌ Error de red en auto-guardado:', e);
        }
      }, 2000); // 2 segundos de inactividad
    }
  };

  // ✅ NUEVO: Manejador para el Configurador Maestro
  const handleConfigChange = (newConfig) => {
    // Actualizar primitivos
    if (newConfig.nombre_proyecto) setNombre_proyecto(newConfig.nombre_proyecto);
    if (newConfig.presupuesto) setPresupuesto(newConfig.presupuesto);
    if (newConfig.moneda) setMoneda(newConfig.moneda);
    // No existe state separado de fecha_inicio, se maneja en objeto proyecto

    // Actualizar objeto proyecto complejo
    setProyecto(prev => ({
      ...prev,
      ...newConfig,
      duracion_total: newConfig.duracion_total,
    }));

    // Actualizar datos editables para la vista previa
    setDatosEditables(prev => ({
      ...prev,
      ...newConfig
    }));
  };

  // Manejar cambios en el formulario de cliente (Sidebar Izquierdo)
  const handleClienteChange = (e) => {
    const { name, value } = e.target;
    setDatosCliente(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // ✅ NUEVO: Sincronizar datosCliente con datosEditables automáticamente
  useEffect(() => {
    // Solo sincronizar si hay datos de cliente
    if (datosCliente && (datosCliente.nombre || datosCliente.ruc)) {
      setDatosEditables(prev => {
        const prevSafe = prev || {};

        // Actualizar solo la sección de cliente, preservando el resto
        return {
          ...prevSafe,
          cliente: {
            nombre: datosCliente.nombre || '',
            ruc: datosCliente.ruc || '',
            direccion: datosCliente.direccion || '',
            telefono: datosCliente.telefono || '',
            email: datosCliente.email || ''
          },
          // Asegurar que cliente_nombre también esté sincronizado (algunos componentes viajan planos)
          cliente_nombre: datosCliente.nombre || ''
        };
      });
    }
  }, [datosCliente]); // Se ejecuta cada vez que datosCliente cambia

  // ✅ NUEVO: Cargar lista de clientes al iniciar
  useEffect(() => {
    cargarListaClientes();
  }, []); // Solo una vez al montar el componente

  // ============================================
  // FUNCIONES DEL CHAT + VISTA PREVIA
  // ============================================

  const obtenerBotonesContextuales = async () => {
    try {
      const etapa = conversacion.length === 0 ? 'inicial' : 'refinamiento';
      const response = await fetch(`http://localhost:8000/api/chat/botones-contextuales/${tipoFlujo}?etapa=${etapa}&historial_length=${conversacion.length}`);
      const data = await response.json();
      setBotonesContextuales(data.botones || []);
    } catch (error) {
      console.error('Error obteniendo botones:', error);
      setBotonesContextuales([]);
    }
  };

  const handleEnviarMensajeChat = async () => {
    if (!inputChat.trim() || analizando) return;

    const nuevoMensaje = { tipo: 'usuario', mensaje: inputChat };
    const nuevaConversacion = [...conversacion, nuevoMensaje];
    setConversacion(nuevaConversacion);
    setInputChat('');
    setAnalizando(true);
    setError('');

    try {
      // Preparar contexto según el tipo de flujo
      let contextoPrincipal = `Servicio: ${servicioSeleccionado}, Industria: ${industriaSeleccionada}, Contexto: ${contextoUsuario}`;

      if (tipoFlujo.includes('proyecto')) {
        contextoPrincipal += `, Nombre: ${nombre_proyecto}, Cliente: ${datosCliente.nombre}, Presupuesto: ${presupuesto}, Duración: ${duracion_total} meses`;
      } else if (tipoFlujo.includes('informe')) {
        contextoPrincipal += `, Proyecto: ${proyectoSeleccionado}, Formato: ${formatoInforme}`;
      }

      const response = await fetch('http://localhost:8000/api/chat/chat-contextualizado', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tipo_flujo: tipoFlujo,
          mensaje: inputChat,
          historial: nuevaConversacion,
          contexto_adicional: contextoPrincipal,
          datos_cliente: datosCliente,  // ¡NUEVO! Enviar datos del cliente
          archivos_procesados: archivos.map(a => ({ nombre: a.nombre, contenido: a.contenidoTexto })),
          generar_html: true // Importante: pedimos HTML preview
        })
      });

      const data = await response.json();


      if (data.success) {
        const mensajeIA = { tipo: 'asistente', mensaje: data.respuesta };
        setConversacion(prev => [...prev, mensajeIA]);

        // Manejar datos según el tipo de flujo
        let datosParaHTML = null;

        if (tipoFlujo.includes('cotizacion') && data.cotizacion_generada) {
          setCotizacion(data.cotizacion_generada);
          setDatosEditables(data.cotizacion_generada);
          datosParaHTML = data.cotizacion_generada;
        } else if (tipoFlujo.includes('cotizacion') && data.estructura_generada) {
          setCotizacion(data.estructura_generada);
          setDatosEditables(data.estructura_generada);
          datosParaHTML = data.estructura_generada;
        } else if (tipoFlujo.includes('proyecto') && data.proyecto_generado) {
          setProyecto(data.proyecto_generado);
          setDatosEditables(data.proyecto_generado);
          datosParaHTML = data.proyecto_generado;
        } else if (tipoFlujo.includes('informe') && data.informe_generado) {
          setInforme(data.informe_generado);
          setDatosEditables(data.informe_generado);
          datosParaHTML = data.informe_generado;
        }

        // GENERAR HTML USANDO PLANTILLAS PROFESIONALES
        if (datosParaHTML) {
          try {
            const htmlGenerado = await obtenerHTMLSegunTipo(datosParaHTML);
            setHtmlPreview(htmlGenerado);
            setMostrarPreview(true);
          } catch (error) {
            console.error('Error generando HTML:', error);
            // Fallback al HTML del backend si existe
            if (data.html_preview) {
              setHtmlPreview(data.html_preview);
              setMostrarPreview(true);
            }
          }
        } else if (data.html_preview) {
          // Fallback si no hay datos estructurados
          setHtmlPreview(data.html_preview);
          setMostrarPreview(true);
        }

        // ✅ NUEVO: Actualizar progreso de chat conversacional
        if (data.datos_recopilados) {
          setDatosRecopilados(data.datos_recopilados);
        }
        if (data.datos_faltantes) {
          setDatosFaltantes(data.datos_faltantes);
        }
        if (data.progreso) {
          setProgresoChat(data.progreso);
        }

        // ✅ NUEVO: Auto-rellenado en tiempo real con datos parciales de PILI
        if (data.datos_generados) {
          console.log('📊 Datos generados por PILI:', data.datos_generados);

          // Actualizar datosEditables con los nuevos datos
          setDatosEditables(prev => {
            const nuevosDatos = {
              ...prev,
              ...data.datos_generados,
              // Mantener cliente que ya teníamos del Punto 1
              cliente: prev?.cliente || datosCliente
            };

            console.log('✅ datosEditables actualizados:', nuevosDatos);
            return nuevosDatos;
          });

          // Actualizar el estado específico según el tipo
          if (tipoFlujo.includes('cotizacion')) {
            setCotizacion(prev => ({ ...prev, ...data.datos_generados }));
          } else if (tipoFlujo.includes('proyecto')) {
            setProyecto(prev => ({ ...prev, ...data.datos_generados }));
          } else if (tipoFlujo.includes('informe')) {
            setInforme(prev => ({ ...prev, ...data.datos_generados }));
          }

          // Mostrar vista previa si no está visible
          if (!mostrarPreview) {
            setMostrarPreview(true);
          }
        }

        // Actualizar botones contextuales
        if (data.botones_contextuales) {
          setBotonesContextuales(data.botones_contextuales);
        }
      } else {
        const mensajeError = { tipo: 'asistente', mensaje: data.respuesta || 'Error en la respuesta' };
        setConversacion(prev => [...prev, mensajeError]);
      }
    } catch (error) {
      console.error('Error en chat:', error);
      const mensajeError = { tipo: 'asistente', mensaje: 'Lo siento, hubo un error. Inténtalo de nuevo.' };
      setConversacion(prev => [...prev, mensajeError]);
      setError('Error de conexión con la IA');
    } finally {
      setAnalizando(false);
    }
  };

  const enviarRespuestaRapida = (texto) => {
    setInputChat(texto);
    setTimeout(() => {
      handleEnviarMensajeChat();
    }, 100);
  };

  // ============================================
  // FUNCIÓN DE GENERACIÓN DE DOCUMENTOS
  // ============================================

  // ✅ NUEVO: Determinar tipo de plantilla específico
  const determinarTipoPlantilla = (datos, tipoDocumento) => {
    // Para proyectos, verificar si es PMI (tiene complejidad, cronograma_fases, etc.)
    if (tipoDocumento === 'proyecto') {
      const esPMI = datos.complejidad || datos.cronograma_fases || datos.raci_actividades ||
        datos.kpis || datos.metricas_pmi;

      if (esPMI) {
        console.log('🔍 DETECTADO: Proyecto Complejo PMI');
        return 'proyecto-complejo-pmi';
      } else {
        console.log('🔍 DETECTADO: Proyecto Simple');
        return 'proyecto-simple';
      }
    }

    // Para cotizaciones
    if (tipoDocumento === 'cotizacion') {
      const esCompleja = datos.items && datos.items.length > 10;
      return esCompleja ? 'cotizacion-compleja' : 'cotizacion-simple';
    }

    // Para informes
    if (tipoDocumento === 'informe') {
      return 'informe-tecnico';
    }

    return tipoDocumento;
  };

  const handleGenerarDocumento = async (formato) => {
    try {
      console.log(`📄 Generando ${formato.toUpperCase()}...`);

      // Determinar tipo de documento
      const tipoDocumento = tipoFlujo.includes('cotizacion') ? 'cotizacion' :
        tipoFlujo.includes('proyecto') ? 'proyecto' : 'informe';

      // Obtener datos actuales (USAR DATOS EDITADOS SI EXISTEN)
      const datosOriginales = tipoDocumento === 'cotizacion' ? cotizacion :
        tipoDocumento === 'proyecto' ? proyecto : informe;

      // CRÍTICO: Usar datosEditables si existen (tienen los cambios del usuario)
      const entidad = datosEditables || datosOriginales;

      // Extraer HTML editado de la vista previa
      const previewElement = previewRef.current;
      const htmlEditado = previewElement ? previewElement.innerHTML : htmlPreview;

      // Preparar datos para enviar según tipo de documento
      let datosParaEnviar;

      if (tipoDocumento === 'informe') {
        // Estructura para INFORMES
        datosParaEnviar = {
          tipo_documento: tipoDocumento,
          titulo: entidad.titulo || "Informe Técnico",
          codigo: entidad.codigo || `INF-${Date.now()}`,
          cliente: entidad.cliente || { nombre: "[Cliente]" },
          fecha: entidad.fecha || new Date().toLocaleDateString('es-PE'),
          resumen: entidad.resumen || entidad.resumen_ejecutivo || "",
          introduccion: entidad.introduccion || "",
          analisis_tecnico: entidad.analisis_tecnico || "",
          resultados: entidad.resultados || "",
          conclusiones: entidad.conclusiones || "",
          recomendaciones: entidad.recomendaciones || [],
          normativa: entidad.normativa || "CNE Suministro 2011"
        };
      } else if (tipoDocumento === 'proyecto') {
        // Estructura para PROYECTOS
        datosParaEnviar = {
          tipo_documento: tipoDocumento,
          nombre: entidad.nombre || entidad.nombre_proyecto || "[Proyecto]",
          codigo: entidad.codigo || entidad.codigo_proyecto || `PROY-${Date.now()}`,
          cliente: entidad.cliente || { nombre: "[Cliente]" },
          presupuesto: entidad.presupuesto || 0,
          duracion_total: entidad.duracion_total || entidad.duracion || 30,
          fecha_inicio: entidad.fecha_inicio || new Date().toLocaleDateString('es-PE'),
          fecha_fin: entidad.fecha_fin || "",
          alcance: entidad.alcance || entidad.alcance_proyecto || "",
          fases: entidad.fases || [],
          normativa: entidad.normativa || "CNE Suministro 2011"
        };
      } else {
        // Estructura para COTIZACIONES (default)
        const itemsActuales = entidad.items || [];
        const subtotalCalculado = itemsActuales.reduce((sum, item) =>
          sum + (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || item.precioUnitario || 0)), 0
        );
        const igvCalculado = subtotalCalculado * 0.18;
        const totalCalculado = subtotalCalculado + igvCalculado;

        datosParaEnviar = {
          tipo_documento: tipoDocumento,
          numero: entidad.numero || `COT-${Date.now()}`,
          cliente: entidad.cliente || { nombre: "[Cliente]" },
          proyecto: entidad.proyecto || "[Proyecto]",
          descripcion: entidad.descripcion || "",
          items: itemsActuales,
          subtotal: parseFloat(subtotalCalculado.toFixed(2)),
          igv: parseFloat(igvCalculado.toFixed(2)),
          total: parseFloat(totalCalculado.toFixed(2)),
          fecha: new Date().toLocaleDateString('es-PE'),
          vigencia: "30 días"
        };
      }

      console.log('📦 DEBUG - Datos completos a enviar:');
      console.log('  - Cliente:', datosParaEnviar.cliente);
      console.log('  - Proyecto:', datosParaEnviar.proyecto);
      console.log('  - Items:', datosParaEnviar.items);
      console.log('  - Subtotal:', datosParaEnviar.subtotal);
      console.log('  - IGV:', datosParaEnviar.igv);
      console.log('  - Total:', datosParaEnviar.total);
      console.log('  - datosCliente originales:', datosCliente);

      console.log('📦 Datos a enviar:', datosParaEnviar);

      // Llamar al endpoint de generación directa
      const response = await fetch(
        `http://localhost:8000/api/generar-documento-directo?formato=${formato}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            datos: datosParaEnviar,
            tipo_plantilla: determinarTipoPlantilla(datosParaEnviar, tipoDocumento),  // ✅ NUEVO
            opciones_personalizacion: datosParaEnviar.personalizacion || {
              esquema_colores: esquemaColores,
              fuente: fuenteDocumento,
              tamano_fuente: tamañoFuente,
              mostrar_logo: mostrarLogo,
              posicion_logo: posicionLogo,
              logo_base64: logoBase64 || null,
              ocultar_igv: ocultarIGV,
              ocultar_precios_unitarios: ocultarPreciosUnitarios
            }
          })
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      // DEBUG: Verificar Content-Type
      const contentType = response.headers.get('Content-Type');
      console.log('🔍 Content-Type recibido:', contentType);

      // Si es JSON, es un error del backend
      if (contentType && contentType.includes('application/json')) {
        const errorData = await response.json();
        throw new Error(`Backend devolvió error: ${JSON.stringify(errorData)}`);
      }

      // Descargar archivo
      const blob = await response.blob();
      console.log('💾 Blob recibido:', blob.size, 'bytes, tipo:', blob.type);

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${tipoDocumento}_${Date.now()}.${formato === 'word' ? 'docx' : 'pdf'}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      console.log(`✅ ${formato.toUpperCase()} descargado exitosamente`);
      alert(`✅ Documento ${formato.toUpperCase()} generado y descargado exitosamente`);

    } catch (error) {
      console.error('❌ Error al generar documento:', error);
      alert(`❌ Error al generar el documento: ${error.message}`);
    }
  };

  // ============================================
  // FUNCIONES DE EDICIÓN HTML
  // ============================================

  const actualizarItem = (index, campo, valor) => {
    if (!datosEditables?.items) return;

    const nuevosItems = [...datosEditables.items];

    // Normalizar nombre de campo (precioUnitario -> precio_unitario)
    const campoNormalizado = campo === 'precioUnitario' ? 'precio_unitario' : campo;

    // Actualizar el campo
    if (campoNormalizado === 'descripcion') {
      nuevosItems[index][campoNormalizado] = valor;
    } else {
      nuevosItems[index][campoNormalizado] = parseFloat(valor) || 0;
    }

    // Recalcular total del item
    if (campoNormalizado === 'cantidad' || campoNormalizado === 'precio_unitario') {
      const cantidad = nuevosItems[index].cantidad || 0;
      const precioUnitario = nuevosItems[index].precio_unitario || 0;
      nuevosItems[index].total = cantidad * precioUnitario;
    }

    const nuevosDatos = { ...datosEditables, items: nuevosItems };
    setDatosEditables(nuevosDatos);

    console.log(`✏️ Item ${index} editado - ${campoNormalizado}:`, valor, '| Item completo:', nuevosItems[index]);

    // Actualizar estado específico
    if (tipoFlujo.includes('cotizacion')) {
      setCotizacion(nuevosDatos);
    } else if (tipoFlujo.includes('proyecto')) {
      setProyecto(nuevosDatos);
    } else if (tipoFlujo.includes('informe')) {
      setInforme(nuevosDatos);
    }

    // Regenerar HTML
    actualizarVistaPrevia();
  };

  const agregarItem = () => {
    if (!datosEditables) return;

    const nuevoItem = {
      descripcion: 'Nuevo item',
      cantidad: 1,
      precioUnitario: 0,
      total: 0,
      capitulo: 'GENERAL'
    };

    const nuevosItems = [...(datosEditables.items || []), nuevoItem];
    const nuevosDatos = { ...datosEditables, items: nuevosItems };
    setDatosEditables(nuevosDatos);

    if (tipoFlujo.includes('cotizacion')) {
      setCotizacion(nuevosDatos);
    }

    actualizarVistaPrevia();
  };

  const eliminarItem = (index) => {
    if (!datosEditables?.items) return;

    const nuevosItems = datosEditables.items.filter((_, i) => i !== index);
    const nuevosDatos = { ...datosEditables, items: nuevosItems };
    setDatosEditables(nuevosDatos);

    if (tipoFlujo.includes('cotizacion')) {
      setCotizacion(nuevosDatos);
    }

    actualizarVistaPrevia();
  };

  const actualizarVistaPrevia = async () => {
    if (!datosEditables) return;

    // Generar HTML actualizado basado en los datos editables
    let htmlActualizado = await obtenerHTMLSegunTipo(datosEditables);
    setHtmlPreview(htmlActualizado);
  };

  const obtenerHTMLSegunTipo = async (datos) => {
    if (tipoFlujo.includes('cotizacion')) {
      return await generarHTMLCotizacion(datos);
    } else if (tipoFlujo.includes('proyecto')) {
      return await generarHTMLProyecto(datos);
    } else if (tipoFlujo.includes('informe')) {
      return await generarHTMLInforme(datos);
    }
    return '';
  };

  const generarHTMLCotizacion = async (datos) => {
    try {
      // 1. Cargar plantilla profesional desde API
      // 1. Cargar plantilla profesional desde API o usar fallback
      let html = '';
      try {
        const response = await fetch('http://localhost:8000/api/templates/cotizacion-simple');
        if (response.ok) {
          const data = await response.json();
          html = data.html;
        }
      } catch (e) {
        console.warn('⚠️ No se pudo cargar plantilla del backend, usando local');
      }

      // FALLBACK LOCAL SI FALLA BACKEND
      if (!html) {
        console.log('🔄 Usando plantilla fallback local');
        html = `
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body { font-family: 'Calibri', sans-serif; color: #333; }
            .header { border-bottom: 2px solid #D4AF37; padding-bottom: 20px; margin-bottom: 30px; }
            .title { color: #8B0000; font-size: 24px; font-weight: bold; }
            .info { display: flex; justify-content: space-between; margin-bottom: 30px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th { background-color: #8B0000; color: white; padding: 10px; text-align: left; }
            td { padding: 10px; border-bottom: 1px solid #ddd; }
            .total { font-weight: bold; font-size: 18px; text-align: right; margin-top: 20px; color: #8B0000; }
          </style>
        </head>
        <body>
          <div class="header">
            <div class="title">COTIZACIÓN {{NUMERO_COTIZACION}}</div>
            <p>{{FECHA_COTIZACION}}</p>
          </div>
          <div class="info">
            <div>
              <strong>Cliente:</strong> {{CLIENTE_NOMBRE}}<br>
              <strong>Proyecto:</strong> {{PROYECTO_NOMBRE}}
            </div>
            <div>
              <strong>Vigencia:</strong> {{VIGENCIA}}
            </div>
          </div>
          <table>
            <thead>
              <tr><th>Descripción</th><th>Cant.</th><th>Total</th></tr>
            </thead>
            <tbody>
              <!-- ITEMS_PLACEHOLDER -->
              <tr><td>{{SERVICIO_NOMBRE}}</td><td>1</td><td>{{TOTAL}}</td></tr>
            </tbody>
          </table>
          <div class="total">Total: S/ {{TOTAL}}</div>
        </body>
        </html>
        `;
      }

      // 2. Calcular totales
      const totales = calcularTotales(datos?.items || []);

      // 3. Reemplazar variables básicas
      let htmlFinal = html
        .replace(/\{\{CLIENTE_NOMBRE\}\}/g, datos.cliente?.nombre || datos.cliente || 'Cliente General') // Soporta objeto o string
        .replace(/\{\{NUMERO_COTIZACION\}\}/g, datos.numero || `COT-${new Date().getTime()}`)
        .replace(/\{\{FECHA_COTIZACION\}\}/g, new Date().toLocaleDateString('es-PE'))
        .replace(/\{\{PROYECTO_NOMBRE\}\}/g, datos.proyecto || 'Proyecto General')
        .replace(/\{\{SUBTOTAL\}\}/g, totales.subtotal)
        .replace(/\{\{IGV\}\}/g, totales.igv)
        .replace(/\{\{TOTAL\}\}/g, totales.total)
        .replace(/\{\{VIGENCIA\}\}/g, '30 días')
        .replace(/\{\{SERVICIO_NOMBRE\}\}/g, datos.servicio || 'Servicios Profesionales')
        .replace(/\{\{NORMATIVA_APLICABLE\}\}/g, 'CNE - Código Nacional de Electricidad');

      // 4. Aplicar colores personalizados según esquema actual
      const ESQUEMAS_COLORES = {
        'azul': { primario: '#0052A3', secundario: '#1E40AF', acento: '#3B82F6', claro: '#EFF6FF' },
        'rojo': { primario: '#8B0000', secundario: '#991B1B', acento: '#DC2626', claro: '#FEE2E2' },
        'verde': { primario: '#065F46', secundario: '#047857', acento: '#10B981', claro: '#D1FAE5' },
        'dorado': { primario: '#D4AF37', secundario: '#B8860B', acento: '#FFD700', claro: '#FEF3C7' },
      };

      const colores = ESQUEMAS_COLORES[esquemaColores] || ESQUEMAS_COLORES.azul;
      htmlFinal = htmlFinal
        .replace(/#0052A3/g, colores.primario)
        .replace(/#1E40AF/g, colores.secundario)
        .replace(/#3B82F6/g, colores.acento)
        .replace(/#EFF6FF/g, colores.claro)
        .replace(/#DBEAFE/g, colores.claro);

      return htmlFinal;
    } catch (error) {
      console.error('Error cargando plantilla:', error);
      // Fallback al HTML básico si falla
      const totales = calcularTotales(datos?.items || []);
      return `<div style="padding: 20px;"><h1>Cotización</h1><p>Total: S/ ${totales.total}</p></div>`;
    }
  };

  const generarHTMLProyecto = async (datos) => {
    try {
      // 1. Cargar plantilla profesional
      const response = await fetch('/api/templates/proyecto-simple');
      const { html } = await response.json();

      // 2. Reemplazar variables
      let htmlFinal = html
        .replace(/\{\{NOMBRE_PROYECTO\}\}/g, nombre_proyecto || 'Nuevo Proyecto')
        .replace(/\{\{PROYECTO_NOMBRE\}\}/g, nombre_proyecto || 'Nuevo Proyecto')
        .replace(/\{\{CLIENTE\}\}/g, datosCliente.nombre || 'Cliente')
        .replace(/\{\{CLIENTE_NOMBRE\}\}/g, datosCliente.nombre || 'Cliente')
        .replace(/\{\{PRESUPUESTO\}\}/g, presupuesto || '0.00')
        .replace(/\{\{TOTAL\}\}/g, presupuesto || '0.00')
        .replace(/\{\{DURACION_TOTAL\}\}/g, `${duracion_total} meses`)
        .replace(/\{\{FECHA\}\}/g, new Date().toLocaleDateString('es-PE'))
        .replace(/\{\{DESCRIPCION_PROYECTO\}\}/g, contextoUsuario || 'Descripción del proyecto');

      // 3. Aplicar colores personalizados
      const ESQUEMAS_COLORES = {
        'azul': { primario: '#0052A3', secundario: '#1E40AF', acento: '#3B82F6', claro: '#EFF6FF' },
        'rojo': { primario: '#8B0000', secundario: '#991B1B', acento: '#DC2626', claro: '#FEE2E2' },
        'verde': { primario: '#065F46', secundario: '#047857', acento: '#10B981', claro: '#D1FAE5' },
        'dorado': { primario: '#D4AF37', secundario: '#B8860B', acento: '#FFD700', claro: '#FEF3C7' },
      };

      const colores = ESQUEMAS_COLORES[esquemaColores] || ESQUEMAS_COLORES.azul;
      htmlFinal = htmlFinal
        .replace(/#0052A3/g, colores.primario)
        .replace(/#1E40AF/g, colores.secundario)
        .replace(/#3B82F6/g, colores.acento)
        .replace(/#EFF6FF/g, colores.claro)
        .replace(/#DBEAFE/g, colores.claro);

      return htmlFinal;
    } catch (error) {
      console.error('Error cargando plantilla proyecto:', error);
      return `<div style="padding: 20px;"><h1>Proyecto</h1><p>${nombre_proyecto}</p></div>`;
    }
  };


  const generarHTMLInforme = async (datos) => {
    try {
      // 1. Determinar tipo de informe
      const tipoInforme = tipoFlujo.includes('ejecutivo') ? 'informe-ejecutivo' : 'informe-tecnico';

      // 2. Cargar plantilla profesional
      const response = await fetch(`/api/templates/${tipoInforme}`);
      const { html } = await response.json();

      // 3. Reemplazar variables
      const proyectoNombre = proyectosMock.find(p => p.id === proyectoSeleccionado)?.nombre || 'General';
      let htmlFinal = html
        .replace(/\{\{TITULO_INFORME\}\}/g, proyectoNombre)
        .replace(/\{\{PROYECTO_NOMBRE\}\}/g, proyectoNombre)
        .replace(/\{\{FECHA\}\}/g, new Date().toLocaleDateString('es-PE'))
        .replace(/\{\{FORMATO\}\}/g, formatoInforme.toUpperCase())
        .replace(/\{\{RESUMEN_EJECUTIVO\}\}/g, contextoUsuario || 'Contenido del informe')
        .replace(/\{\{DESCRIPCION_PROYECTO\}\}/g, contextoUsuario || 'Contenido del informe');

      // 4. Aplicar colores personalizados
      const ESQUEMAS_COLORES = {
        'azul': { primario: '#0052A3', secundario: '#1E40AF', acento: '#3B82F6', claro: '#EFF6FF' },
        'rojo': { primario: '#8B0000', secundario: '#991B1B', acento: '#DC2626', claro: '#FEE2E2' },
        'verde': { primario: '#065F46', secundario: '#047857', acento: '#10B981', claro: '#D1FAE5' },
        'dorado': { primario: '#D4AF37', secundario: '#B8860B', acento: '#FFD700', claro: '#FEF3C7' },
      };

      const colores = ESQUEMAS_COLORES[esquemaColores] || ESQUEMAS_COLORES.azul;
      htmlFinal = htmlFinal
        .replace(/#0052A3/g, colores.primario)
        .replace(/#1E40AF/g, colores.secundario)
        .replace(/#3B82F6/g, colores.acento)
        .replace(/#EFF6FF/g, colores.claro)
        .replace(/#DBEAFE/g, colores.claro);

      return htmlFinal;
    } catch (error) {
      console.error('Error cargando plantilla informe:', error);
      return `<div style="padding: 20px;"><h1>Informe</h1><p>${tipoFlujo}</p></div>`;
    }
  };


  const calcularTotales = (items = []) => {
    const subtotal = items.reduce((sum, item) => sum + ((item.cantidad || 0) * (item.precioUnitario || 0)), 0);
    return {
      subtotal: subtotal.toFixed(2),
      igv: (subtotal * 0.18).toFixed(2),
      total: (subtotal * 1.18).toFixed(2)
    };
  };

  // ============================================
  // FUNCIONES DE ARCHIVOS
  // ============================================

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    files.forEach(file => {
      if (file.size > 10 * 1024 * 1024) {
        setError(`El archivo ${file.name} es demasiado grande (máx 10MB)`);
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        const archivo = {
          nombre: file.name,
          extension: file.name.split('.').pop(),
          tamano: `${(file.size / 1024).toFixed(1)} KB`,
          contenido: e.target.result,
          contenidoTexto: file.type.includes('text') ? e.target.result : null
        };

        setArchivos(prev => [...prev, archivo]);
        setExito(`Archivo ${file.name} procesado correctamente`);
        setTimeout(() => setExito(''), 3000);
      };

      if (file.type.includes('text')) {
        reader.readAsText(file);
      } else {
        reader.readAsDataURL(file);
      }
    });
  };

  const cargarLogo = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 2 * 1024 * 1024) {
        setError('El logo debe ser menor a 2MB');
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        setLogoBase64(e.target.result);
        setExito('Logo cargado correctamente');
        setTimeout(() => setExito(''), 3000);
      };
      reader.readAsDataURL(file);
    }
  };

  // ============================================
  // FUNCIONES DE DESCARGA
  // ============================================



  const handleDescargar = async (formato) => {
    const tipoDocumento = tipoFlujo.includes('cotizacion') ? 'cotizacion' :
      tipoFlujo.includes('proyecto') ? 'proyecto' : 'informe';

    const entidad = tipoDocumento === 'cotizacion' ? cotizacion :
      tipoDocumento === 'proyecto' ? proyecto : informe;

    if (!entidad && !datosEditables) {
      setError(`No hay ${tipoDocumento} para descargar`);
      return;
    }

    setDescargando(formato);
    setError('');
    setExito('');

    try {

      setExito(`Generando ${formato.toUpperCase()}...`);

      // ✅ SOLUCIÓN PROFESIONAL: Usar REF para datos SIEMPRE actualizados
      // El ref se actualiza en tiempo real, el state puede estar desactualizado
      const datosFinales = datosEditablesRef.current || datosEditables || entidad;
      const itemsActuales = datosFinales?.items || [];

      // 🐛 DEBUG: Ver qué datos tenemos


      // Recalcular totales
      const subtotalCalculado = itemsActuales.reduce((sum, item) =>
        sum + (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || item.precioUnitario || 0)), 0
      );
      const igvCalculado = subtotalCalculado * 0.18;
      const totalCalculado = subtotalCalculado + igvCalculado;

      // ✅ V2: Preparar datos JSON limpios (SIN HTML)
      // Determinar tipo de documento
      const tipoDocumento = tipoFlujo.includes('cotizacion') ? 'cotizacion' :
        tipoFlujo.includes('proyecto') ? 'proyecto' : 'informe';

      let datosLimpios;

      if (tipoDocumento === 'informe') {
        // Estructura para INFORMES
        datosLimpios = {
          tipo_documento: tipoFlujo,
          titulo: datosFinales?.titulo || "Informe Técnico",
          codigo: datosFinales?.codigo || `INF-${Date.now()}`,
          cliente: {
            nombre: datosCliente.nombre || '[Cliente]',
            ruc: datosCliente.ruc || '',
            direccion: datosCliente.direccion || '',
            telefono: datosCliente.telefono || '',
            email: datosCliente.email || ''
          },
          fecha: new Date().toLocaleDateString('es-PE'),
          resumen: datosFinales?.resumen || datosFinales?.resumen_ejecutivo || "",
          introduccion: datosFinales?.introduccion || "",
          analisis_tecnico: datosFinales?.analisis_tecnico || "",
          resultados: datosFinales?.resultados || "",
          conclusiones: datosFinales?.conclusiones || "",
          recomendaciones: datosFinales?.recomendaciones || [],
          normativa: datosFinales?.normativa || "CNE Suministro 2011",
          personalizacion: {
            esquema_colores: esquemaColores,
            fuente: fuenteDocumento,
            tamano_fuente: tamañoFuente,
            mostrar_logo: mostrarLogo,
            posicion_logo: posicionLogo,
            logo_base64: logoBase64 || null
          }
        };
      } else if (tipoDocumento === 'proyecto') {
        // Estructura para PROYECTOS
        datosLimpios = {
          tipo_documento: tipoFlujo,
          numero: datosFinales?.numero || `PROY-${Date.now()}`,
          codigo_proyecto: datosFinales?.numero || datosFinales?.codigo || `PROY-${Date.now()}`,
          nombre_proyecto: datosFinales?.nombre_proyecto || datosFinales?.nombre || "[Proyecto]",
          codigo: datosFinales?.codigo || datosFinales?.numero || `PROY-${Date.now()}`,
          nombre: datosFinales?.nombre || datosFinales?.nombre_proyecto || "[Proyecto]",
          cliente: {
            nombre: datosCliente.nombre || datosFinales?.cliente?.nombre || '[Cliente]',
            ruc: datosCliente.ruc || '',
            direccion: datosCliente.direccion || '',
            telefono: datosCliente.telefono || '',
            email: datosCliente.email || ''
          },
          presupuesto: datosFinales?.presupuesto || 0,
          moneda: datosFinales?.moneda || moneda || 'PEN',
          duracion_total: datosFinales?.cronograma?.duracion_total || datosFinales?.duracion_total || datosFinales?.duracion || "30 días",
          fecha_inicio: datosFinales?.cronograma?.fecha_inicio || datosFinales?.fecha_inicio || new Date().toLocaleDateString('es-PE'),
          fecha_fin: datosFinales?.cronograma?.fecha_fin || datosFinales?.fecha_fin || "",
          // KPI's PMI
          spi: datosFinales?.spi || "1.00",
          cpi: datosFinales?.cpi || "1.00",
          ev_k: datosFinales?.ev_k || "0",
          pv_k: datosFinales?.pv_k || "0",
          ac_k: datosFinales?.ac_k || "0",

          // Listas complejas
          entregables: datosFinales?.entregables || [],
          cronograma_fases: datosFinales?.cronograma_fases || datosFinales?.fases || [],
          stakeholders: datosFinales?.stakeholders || [],
          riesgos: datosFinales?.riesgos || [],
          raci_actividades: datosFinales?.raci_actividades || [],

          alcance: datosFinales?.resumen || datosFinales?.alcance || datosFinales?.alcance_proyecto || "",
          alcance_proyecto: datosFinales?.resumen || datosFinales?.alcance || datosFinales?.alcance_proyecto || "",

          normativa: datosFinales?.normativa || datosFinales?.normativa_aplicable || "CNE Suministro 2011",
          normativa_aplicable: datosFinales?.normativa_aplicable || datosFinales?.normativa || "CNE Suministro 2011",
          subtitulo_normativa: datosFinales?.subtitulo_normativa || "",

          personalizacion: {
            esquema_colores: esquemaColores,
            fuente: fuenteDocumento,
            tamano_fuente: tamañoFuente,
            mostrar_logo: mostrarLogo,
            posicion_logo: posicionLogo,
            logo_base64: logoBase64 || null
          }
        };
      } else {
        // Estructura para COTIZACIONES (default)
        datosLimpios = {
          tipo_documento: tipoFlujo,
          numero: datosFinales?.numero || `COT-${Date.now()}`,
          fecha: new Date().toLocaleDateString('es-PE'),
          vigencia: datosFinales?.vigencia || datosFinales?.validez_oferta || '30 días',
          moneda: datosFinales?.moneda || 'PEN', // ✅ Moneda
          cliente: {
            nombre: datosCliente.nombre || '[Cliente]',
            ruc: datosCliente.ruc || '',
            direccion: datosCliente.direccion || '',
            telefono: datosCliente.telefono || '',
            email: datosCliente.email || ''
          },
          proyecto: nombre_proyecto || '[Proyecto]',
          descripcion: contextoUsuario || '',

          // Listas complejas de cotización
          garantias: datosFinales?.garantias || [],
          condiciones_pago: datosFinales?.condiciones_pago || [],
          plazo_entrega: datosFinales?.plazo_entrega || '15 días',
          lugar_entrega: datosFinales?.lugar_entrega || 'Almacén de cliente',

          items: itemsActuales.map((item, index) => ({
            item: index + 1,
            descripcion: item.descripcion || '',
            cantidad: parseFloat(item.cantidad || 0),
            unidad: item.unidad || 'und',
            precio_unitario: parseFloat(item.precio_unitario || item.precioUnitario || 0),
            total: (parseFloat(item.cantidad || 0) * parseFloat(item.precio_unitario || item.precioUnitario || 0)).toFixed(2)
          })),
          subtotal: parseFloat(subtotalCalculado.toFixed(2)),
          igv: parseFloat(igvCalculado.toFixed(2)),
          total: parseFloat(totalCalculado.toFixed(2)),
          observaciones: datosFinales?.observaciones || 'Precios incluyen IGV',
          personalizacion: {
            esquema_colores: esquemaColores,
            fuente: fuenteDocumento,
            tamano_fuente: tamañoFuente,
            mostrar_logo: mostrarLogo,
            posicion_logo: posicionLogo,
            logo_base64: logoBase64 || null,
            ocultar_igv: ocultarIGV,
            ocultar_precios_unitarios: ocultarPreciosUnitarios
          }
        };
      }


      console.log('📦 Datos limpios V2 a enviar:', datosLimpios);
      console.log('  - Tipo:', datosLimpios.tipo_documento);
      console.log('  - Cliente:', datosLimpios.cliente.nombre);
      if (tipoDocumento === 'cotizacion') {
        console.log('  - Items:', datosLimpios.items.length);
        console.log('  - Items detalle:', datosLimpios.items);
        console.log('  - Total:', datosLimpios.total);
      } else if (tipoDocumento === 'informe') {
        console.log('  - Código:', datosLimpios.codigo);
        console.log('  - Título:', datosLimpios.titulo);
      } else if (tipoDocumento === 'proyecto') {
        console.log('  - Código:', datosLimpios.codigo);
        console.log('  - Presupuesto:', datosLimpios.presupuesto);
        console.log('  💰 Moneda:', datosLimpios.moneda);  // ✅ DEBUG: Ver moneda
      }
      console.log('  - Personalización:', datosLimpios.personalizacion);

      // ✅ V2: Llamar endpoint limpio (SIN HTML)
      const response = await fetch(
        `http://localhost:8000/api/generar-documento-v2?formato=${formato}&guardar_bd=false`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(datosLimpios)  // Solo JSON, sin HTML
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      // Descargar archivo
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `cotizacion_${datosLimpios.numero}.${formato === 'word' ? 'docx' : 'pdf'}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      console.log(`✅ ${formato.toUpperCase()} V2 descargado exitosamente`);
      setExito(`✅ ${formato.toUpperCase()} descargado exitosamente`);
      setTimeout(() => setExito(''), 4000);

    } catch (error) {
      console.error('❌ Error al descargar V2:', error);
      setError(`Error al generar el documento: ${error.message}`);
    } finally {
      setDescargando(null);
    }
  };







  // ============================================
  // HOOKS
  // ============================================

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [conversacion]);

  useEffect(() => {
    if (tipoFlujo && paso === 2) {
      obtenerBotonesContextuales();
    }
  }, [conversacion, tipoFlujo, paso]);

  // ✅ Cargar lista de clientes al montar el componente
  useEffect(() => {
    cargarListaClientes();
  }, []);

  // ============================================
  // RENDERIZADO - PANTALLA INICIO
  // ============================================

  if (pantallaActual === 'inicio') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6">
        <div className="max-w-5xl mx-auto">
          {/* HEADER PRINCIPAL */}
          <div className="bg-gradient-to-r from-red-950 via-red-900 to-black rounded-2xl p-8 mb-8 border-2 border-yellow-600 shadow-2xl backdrop-blur-md bg-opacity-90 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-yellow-600/10 via-transparent to-yellow-600/10 animate-pulse"></div>
            <div className="relative z-10">
              <h1 className="text-5xl font-bold flex items-center gap-4 text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-yellow-300 to-yellow-500">
                <Zap className="w-12 h-12 text-yellow-400 animate-pulse" />
                {datosEmpresa.nombre}
              </h1>
              <p className="text-yellow-400 mt-3 font-semibold text-xl">Cognitive Document Orchestrator V1.0</p>
              <div className="flex flex-wrap justify-center gap-6 mt-4 text-sm">
                <span className="text-gray-300 flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-yellow-500" />
                  {datosEmpresa.direccion}
                </span>
                <span className="text-gray-300 flex items-center gap-2">
                  <Mail className="w-4 h-4 text-yellow-500" />
                  {datosEmpresa.email}
                </span>
              </div>
            </div>
          </div>

          {error && <Alerta tipo="error" mensaje={error} onClose={() => setError('')} />}
          {exito && <Alerta tipo="exito" mensaje={exito} onClose={() => setExito('')} />}

          {/* TÍTULO PRINCIPAL */}
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-yellow-400 mb-4">¿Qué necesitas hacer?</h2>
            <p className="text-gray-300 text-lg">Selecciona el tipo de trabajo que deseas realizar</p>
          </div>

          {/* MENÚS EXPANDIBLES */}
          <div className="space-y-4">

            {/* MENÚ 1: COTIZACIONES */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl border-2 border-yellow-700 shadow-xl backdrop-blur-md bg-opacity-90 overflow-hidden">
              <button
                onClick={() => setMenuCotizaciones(!menuCotizaciones)}
                className="w-full p-6 flex items-center justify-between hover:bg-gray-800 transition-all duration-300">
                <div className="flex items-center gap-4">
                  <div className="bg-gradient-to-br from-yellow-600 to-yellow-500 p-3 rounded-xl">
                    <FileText className="w-8 h-8 text-black" />
                  </div>
                  <div className="text-left">
                    <h3 className="text-2xl font-bold text-yellow-400">📊 COTIZACIONES</h3>
                    <p className="text-gray-400 text-sm">Genera presupuestos y cotizaciones</p>
                  </div>
                </div>
                {menuCotizaciones ? <ChevronUp className="w-6 h-6 text-yellow-400" /> : <ChevronDown className="w-6 h-6 text-yellow-400" />}
              </button>

              {menuCotizaciones && (
                <div className="px-6 pb-6 space-y-3 animate-fadeIn">
                  <button
                    onClick={() => iniciarFlujo('cotizacion-simple')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-yellow-900 hover:to-yellow-800 p-4 rounded-xl border-2 border-gray-700 hover:border-yellow-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <Zap className="w-6 h-6 text-yellow-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Cotización Simple</p>
                        <p className="text-gray-400 text-sm">Vista previa en tiempo real - 5 a 15 minutos</p>
                      </div>
                    </div>
                  </button>

                  <button
                    onClick={() => iniciarFlujo('cotizacion-compleja')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-purple-900 hover:to-purple-800 p-4 rounded-xl border-2 border-gray-700 hover:border-purple-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <Layers className="w-6 h-6 text-purple-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Cotización Compleja</p>
                        <p className="text-gray-400 text-sm">Análisis detallado con edición avanzada</p>
                      </div>
                    </div>
                  </button>
                </div>
              )}
            </div>

            {/* MENÚ 2: PROYECTOS */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl border-2 border-blue-700 shadow-xl backdrop-blur-md bg-opacity-90 overflow-hidden">
              <button
                onClick={() => setMenuProyectos(!menuProyectos)}
                className="w-full p-6 flex items-center justify-between hover:bg-gray-800 transition-all duration-300">
                <div className="flex items-center gap-4">
                  <div className="bg-gradient-to-br from-blue-600 to-blue-500 p-3 rounded-xl">
                    <Briefcase className="w-8 h-8 text-white" />
                  </div>
                  <div className="text-left">
                    <h3 className="text-2xl font-bold text-blue-400">📁 PROYECTOS</h3>
                    <p className="text-gray-400 text-sm">Gestión integral de proyectos</p>
                  </div>
                </div>
                {menuProyectos ? <ChevronUp className="w-6 h-6 text-blue-400" /> : <ChevronDown className="w-6 h-6 text-blue-400" />}
              </button>

              {menuProyectos && (
                <div className="px-6 pb-6 space-y-3 animate-fadeIn">
                  <button
                    onClick={() => iniciarFlujo('proyecto-simple')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-blue-900 hover:to-blue-800 p-4 rounded-xl border-2 border-gray-700 hover:border-blue-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <Folder className="w-6 h-6 text-blue-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Proyecto Simple</p>
                        <p className="text-gray-400 text-sm">Gestión básica con vista previa</p>
                      </div>
                    </div>
                  </button>

                  <button
                    onClick={() => iniciarFlujo('proyecto-complejo')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-purple-900 hover:to-purple-800 p-4 rounded-xl border-2 border-gray-700 hover:border-purple-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <Layout className="w-6 h-6 text-purple-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Proyecto Complejo</p>
                        <p className="text-gray-400 text-sm">Gantt, hitos y seguimiento avanzado</p>
                      </div>
                    </div>
                  </button>
                </div>
              )}
            </div>

            {/* MENÚ 3: INFORMES */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl border-2 border-green-700 shadow-xl backdrop-blur-md bg-opacity-90 overflow-hidden">
              <button
                onClick={() => setMenuInformes(!menuInformes)}
                className="w-full p-6 flex items-center justify-between hover:bg-gray-800 transition-all duration-300">
                <div className="flex items-center gap-4">
                  <div className="bg-gradient-to-br from-green-600 to-green-500 p-3 rounded-xl">
                    <BookOpen className="w-8 h-8 text-white" />
                  </div>
                  <div className="text-left">
                    <h3 className="text-2xl font-bold text-green-400">📄 INFORMES</h3>
                    <p className="text-gray-400 text-sm">Documentos y reportes profesionales</p>
                  </div>
                </div>
                {menuInformes ? <ChevronUp className="w-6 h-6 text-green-400" /> : <ChevronDown className="w-6 h-6 text-green-400" />}
              </button>

              {menuInformes && (
                <div className="px-6 pb-6 space-y-3 animate-fadeIn">
                  <button
                    onClick={() => iniciarFlujo('informe-simple')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-green-900 hover:to-green-800 p-4 rounded-xl border-2 border-gray-700 hover:border-green-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <FileText className="w-6 h-6 text-green-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Informe Simple</p>
                        <p className="text-gray-400 text-sm">PDF básico con vista previa editable</p>
                      </div>
                    </div>
                  </button>

                  <button
                    onClick={() => iniciarFlujo('informe-ejecutivo')}
                    className="w-full group bg-gradient-to-r from-gray-800 to-gray-900 hover:from-purple-900 hover:to-purple-800 p-4 rounded-xl border-2 border-gray-700 hover:border-purple-600 transition-all duration-300 text-left">
                    <div className="flex items-center gap-3">
                      <BarChart3 className="w-6 h-6 text-purple-400 group-hover:scale-110 transition-transform" />
                      <div>
                        <p className="font-bold text-white text-lg">Informe Ejecutivo</p>
                        <p className="text-gray-400 text-sm">Word APA, tablas y gráficos automáticos</p>
                      </div>
                    </div>
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ============================================
  // PANTALLA: FLUJO DE PASOS MEJORADO
  // ============================================

  if (pantallaActual === 'flujo-pasos') {
    const esCotizacion = tipoFlujo.includes('cotizacion');
    const esProyecto = tipoFlujo.includes('proyecto');
    const esInforme = tipoFlujo.includes('informe');
    const esComplejo = tipoFlujo.includes('complejo') || tipoFlujo.includes('compleja') || tipoFlujo.includes('ejecutivo');

    let colores = { primary: 'yellow', border: 'yellow-700', bg: 'yellow-600' };
    if (esProyecto) colores = { primary: 'blue', border: 'blue-700', bg: 'blue-600' };
    else if (esInforme) colores = { primary: 'green', border: 'green-700', bg: 'green-600' };

    const configuracion = {
      'cotizacion-simple': { titulo: '⚡ Cotización Simple', desc: 'Vista previa en tiempo real - 5 a 15 minutos', icon: Zap },
      'cotizacion-compleja': { titulo: '📄 Cotización Compleja', desc: 'Análisis detallado con edición avanzada', icon: Layers },
      'proyecto-simple': { titulo: '📁 Proyecto Simple', desc: 'Gestión básica con vista previa', icon: Folder },
      'proyecto-complejo': { titulo: '🏗️ Proyecto Complejo', desc: 'Gantt, hitos y seguimiento avanzado', icon: Layout },
      'informe-simple': { titulo: '📄 Informe Simple', desc: 'PDF básico con vista previa editable', icon: FileText },
      'informe-ejecutivo': { titulo: '📊 Informe Ejecutivo', desc: 'Word APA, tablas y gráficos automáticos', icon: BarChart3 }
    };

    if (pantallaActual === 'flujo-pasos' && configuracion[tipoFlujo]) {
      const config = configuracion[tipoFlujo];
      const IconoTitulo = config.icon;

      return (
        <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white">
          <div className="max-w-full mx-auto">
            {/* HEADER FIJO */}
            <div className="bg-gradient-to-r from-red-950 via-red-900 to-black p-4 border-b-2 border-yellow-600 shadow-2xl">
              <div className="max-w-7xl mx-auto flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <IconoTitulo className="w-8 h-8 text-yellow-400" />
                  <div>
                    <h1 className="text-2xl font-bold text-yellow-400">{config.titulo}</h1>
                    <p className="text-gray-300 text-sm">{config.desc}</p>
                  </div>
                </div>

                {/* INDICADOR DE PASOS COMPACTO */}
                <div className="flex items-center gap-4">
                  {[1, 2, 3].map(num => (
                    <div key={num} className="flex items-center gap-2">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${paso >= num ? 'bg-yellow-600 text-black' : 'border border-gray-600 text-gray-600'
                        }`}>
                        {num}
                      </div>
                      {num < 3 && <div className={`w-8 h-1 ${paso > num ? 'bg-yellow-600' : 'bg-gray-600'}`} />}
                    </div>
                  ))}

                  <button onClick={volverAlInicio} className="ml-6 px-4 py-2 bg-red-800 hover:bg-red-700 text-yellow-400 rounded-lg font-semibold flex items-center gap-2 transition-all">
                    <Home className="w-4 h-4" />
                    Inicio
                  </button>
                </div>
              </div>
            </div>

            {/* ALERTAS */}
            <div className="max-w-7xl mx-auto px-6 pt-4">
              {error && <Alerta tipo="error" mensaje={error} onClose={() => setError('')} />}
              {exito && <Alerta tipo="exito" mensaje={exito} onClose={() => setExito('')} />}
            </div>

            {/* CONTENIDO PRINCIPAL */}
            <div className="p-6">
              {/* PASO 1: CONFIGURACIÓN */}
              {paso === 1 && (
                <div className="max-w-5xl mx-auto space-y-6">

                  {/* LOGO UNIVERSAL (TODOS LOS SERVICIOS) */}
                  <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-600 shadow-xl">
                    <h2 className="text-2xl font-bold mb-4 text-yellow-400 flex items-center gap-2">
                      🎨 Logo Empresa (Aparecerá en el documento final)
                    </h2>

                    <div className="flex gap-4 items-center">
                      <div className="flex-1">
                        <input
                          ref={fileInputLogoRef}
                          type="file"
                          onChange={cargarLogo}
                          className="hidden"
                          accept="image/*"
                        />
                        <button
                          onClick={() => fileInputLogoRef.current?.click()}
                          className="w-full bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 text-black px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-xl border-2 border-yellow-400 transition-all duration-300 hover:scale-105">
                          <Upload className="w-5 h-5" />
                          {logoBase64 ? 'Cambiar Logo' : 'Subir Logo'}
                        </button>
                        <p className="text-xs text-gray-400 mt-2 text-center">
                          PNG, JPG, WebP - Máx 2MB • Se integrará automáticamente en Word
                        </p>
                      </div>

                      {logoBase64 && (
                        <div className="bg-white rounded-xl p-3 border-2 border-yellow-400 shadow-lg">
                          <img src={logoBase64} alt="Logo" className="w-24 h-24 object-contain" />
                          <p className="text-xs text-gray-600 mt-2 text-center font-semibold">✅ Cargado</p>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* ✅ FORMULARIO UNIVERSAL DE CLIENTE (TODOS LOS 6 TIPOS DE DOCUMENTOS) */}
                  <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-600 shadow-xl">
                    <h2 className="text-2xl font-bold mb-6 text-yellow-400 flex items-center gap-3">
                      <Users className="w-7 h-7" />
                      Datos del Cliente
                    </h2>

                    {/* Selector de cliente existente o nuevo */}
                    <div className="mb-6">
                      <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2">
                        <Building2 className="w-5 h-5" />
                        Seleccionar Cliente
                      </label>
                      <select
                        value={clienteSeleccionadoId || ''}
                        onChange={cargarDatosCliente}
                        className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                      >
                        <option value="">+ Nuevo Cliente</option>
                        {listaClientes.map(c => (
                          <option key={c.id} value={c.id}>
                            {c.nombre} - RUC: {c.ruc}
                          </option>
                        ))}
                      </select>
                      <p className="text-xs text-gray-400 mt-1">
                        Selecciona un cliente existente o crea uno nuevo
                      </p>
                    </div>

                    {/* Campos del formulario */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                      <div>
                        <label className="block text-yellow-400 font-semibold mb-2">
                          Nombre/Razón Social *
                        </label>
                        <input
                          type="text"
                          name="nombre"
                          value={datosCliente.nombre}
                          onChange={handleClienteChange}
                          className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                          placeholder="Ej: Constructora ABC S.A.C."
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-yellow-400 font-semibold mb-2">
                          RUC *
                        </label>
                        <input
                          type="text"
                          name="ruc"
                          value={datosCliente.ruc}
                          onChange={handleClienteChange}
                          className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                          placeholder="11 dígitos"
                          maxLength={11}
                          required
                        />
                      </div>

                      <div className="md:col-span-2">
                        <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2">
                          <MapPin className="w-4 h-4" />
                          Dirección
                        </label>
                        <input
                          type="text"
                          name="direccion"
                          value={datosCliente.direccion}
                          onChange={handleClienteChange}
                          className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                          placeholder="Ej: Av. Principal 123, Lima"
                        />
                      </div>

                      <div>
                        <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2">
                          <Phone className="w-4 h-4" />
                          Teléfono
                        </label>
                        <input
                          type="tel"
                          name="telefono"
                          value={datosCliente.telefono}
                          onChange={handleClienteChange}
                          className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                          placeholder="Ej: 987654321"
                        />
                      </div>

                      <div>
                        <label className="block text-yellow-400 font-semibold mb-2 flex items-center gap-2">
                          <Mail className="w-4 h-4" />
                          Email
                        </label>
                        <input
                          type="email"
                          name="email"
                          value={datosCliente.email}
                          onChange={handleClienteChange}
                          className="w-full px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                          placeholder="cliente@empresa.com"
                        />
                      </div>
                    </div>

                    {/* Botón guardar cliente */}
                    <button
                      onClick={guardarCliente}
                      disabled={guardandoCliente || !datosCliente.nombre || !datosCliente.ruc}
                      className="w-full bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 disabled:from-gray-800 disabled:to-gray-700 disabled:cursor-not-allowed text-black px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-xl border-2 border-yellow-400 transition-all duration-300 hover:scale-105"
                    >
                      {guardandoCliente ? (
                        <>
                          <Loader className="w-5 h-5 animate-spin" />
                          Guardando...
                        </>
                      ) : (
                        <>
                          <Save className="w-5 h-5" />
                          {clienteSeleccionadoId ? 'Actualizar Cliente' : 'Guardar Cliente'}
                        </>
                      )}
                    </button>
                  </div>

                  {/* CONFIGURACIÓN ESPECÍFICA POR TIPO */}
                  {esProyecto && (
                    <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-blue-700 shadow-xl">
                      <h2 className="text-2xl font-bold mb-4 text-blue-400">📋 Información del Proyecto</h2>
                      <div className="space-y-6">
                        <div>
                          <label className="block text-blue-400 font-semibold mb-2">Nombre del Proyecto *</label>
                          <input
                            type="text"
                            value={nombre_proyecto}
                            onChange={(e) => setNombre_proyecto(e.target.value)}
                            className="w-full px-4 py-3 bg-gray-950 border border-blue-700 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
                            placeholder="Ej: Instalación Eléctrica Edificio Central"
                          />
                        </div>

                        <div className="grid grid-cols-3 gap-4">
                          <div className="col-span-2">
                            <label className="block text-blue-400 font-semibold mb-2">Presupuesto Estimado</label>
                            <input
                              type="number"
                              value={presupuesto}
                              onChange={(e) => setPresupuesto(e.target.value)}
                              className="w-full px-4 py-3 bg-gray-950 border border-blue-700 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
                              placeholder="50000"
                            />
                          </div>
                          <div>
                            <label className="block text-blue-400 font-semibold mb-2">Moneda</label>
                            <select
                              value={moneda}
                              onChange={(e) => setMoneda(e.target.value)}
                              className="w-full px-4 py-3 bg-gray-950 border border-blue-700 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
                            >
                              <option value="PEN">S/ (PEN)</option>
                              <option value="USD">$ (USD)</option>
                              <option value="EUR">€ (EUR)</option>
                            </select>
                          </div>
                        </div>

                        {/* ✅ CALENDARIO PROFESIONAL - Persistencia corregida y Sincronizada */}
                        {/* GRID DE DISEÑO: CALENDARIO IZQUIERDA - FASES DERECHA */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">

                          {/* COLUMNA IZQUIERDA: CONFIGURACIÓN */}
                          <div className="space-y-6">
                            <CalendarioProyecto
                              onChange={(datos) => {
                                setDatosCalendario(datos);
                                setDatosCronograma(datos);
                                if (datos && datos.duracion_dias) {
                                  if (!duracion_total || duracion_total === datos.duracion_dias) {
                                    console.log('🔄 Sincronizando duración desde calendario:', datos.duracion_dias);
                                    setDuracion_total(datos.duracion_dias);
                                  } else {
                                    console.log('⚠️ Preservando duración manual del usuario:', duracion_total);
                                  }
                                }
                              }}
                              valoresIniciales={{
                                fechaInicio: datosCalendario?.fechaInicio ? new Date(datosCalendario.fechaInicio) : new Date(),
                                duracionMeses: 4,
                                usarDiasHabiles: true
                              }}
                            />

                            {/* CONFIGURACIÓN PROYECTO COMPLEJO (Checklist y Metrado) */}
                            {tipoFlujo === 'proyecto-complejo' && (
                              <div className="space-y-6 animate-fadeIn">
                                {/* Checklist Alcance */}
                                <div className="border-t border-blue-800 pt-6">
                                  <h3 className="text-xl font-bold text-blue-300 mb-4 flex items-center gap-2">
                                    <CheckSquare className="w-5 h-5" />
                                    Definir Alcance del Proyecto
                                  </h3>
                                  <div className="flex gap-4 mb-6">
                                    <button
                                      onClick={() => {
                                        setComplejidad(5);
                                        setEtapasSeleccionadas(['acta_constitucion', 'stakeholders', 'cronograma', 'cierre']);
                                      }}
                                      className={`flex-1 p-4 rounded-xl border-2 transition-all ${complejidad === 5 ? 'bg-blue-600 border-blue-400 text-white' : 'bg-gray-900 border-gray-700 text-gray-400'}`}
                                    >
                                      <div className="font-bold text-lg">5 Fases - Básico</div>
                                      <div className="text-xs opacity-80">Proyectos estándar</div>
                                    </button>
                                    <button
                                      onClick={() => {
                                        setComplejidad(7);
                                        setEtapasSeleccionadas(['acta_constitucion', 'stakeholders', 'riesgos', 'cronograma', 'calidad', 'comunicaciones', 'cierre']);
                                      }}
                                      className={`flex-1 p-4 rounded-xl border-2 transition-all ${complejidad === 7 ? 'bg-purple-600 border-purple-400 text-white' : 'bg-gray-900 border-gray-700 text-gray-400'}`}
                                    >
                                      <div className="font-bold text-lg">7 Fases - Avanzado</div>
                                      <div className="text-xs opacity-80">Gestión integral PMI</div>
                                    </button>
                                  </div>
                                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                                    {[
                                      { id: 'acta_constitucion', label: 'Acta de Constitución' },
                                      { id: 'stakeholders', label: 'Interesados (Stakeholders)' },
                                      { id: 'riesgos', label: 'Gestión de Riesgos' },
                                      { id: 'cronograma', label: 'Cronograma Detallado' },
                                      { id: 'calidad', label: 'Plan de Calidad' },
                                      { id: 'comunicaciones', label: 'Plan de Comunicaciones' },
                                      { id: 'cierre', label: 'Informe de Cierre' }
                                    ].map(etapa => (
                                      <label key={etapa.id} className="flex items-center gap-3 p-3 bg-gray-950 rounded-lg border border-gray-800 cursor-pointer hover:border-blue-500 transition-colors">
                                        <input
                                          type="checkbox"
                                          checked={etapasSeleccionadas.includes(etapa.id)}
                                          onChange={(e) => {
                                            if (e.target.checked) setEtapasSeleccionadas([...etapasSeleccionadas, etapa.id]);
                                            else setEtapasSeleccionadas(etapasSeleccionadas.filter(id => id !== etapa.id));
                                          }}
                                          className="w-5 h-5 rounded border-gray-600 text-blue-500 focus:ring-blue-500 bg-gray-800"
                                        />
                                        <span className={etapasSeleccionadas.includes(etapa.id) ? 'text-white font-medium' : 'text-gray-500'}>
                                          {etapa.label}
                                        </span>
                                      </label>
                                    ))}
                                  </div>
                                </div>

                                {/* Metrado */}
                                <div className="border-t border-blue-800 pt-6">
                                  <h3 className="text-xl font-bold text-blue-300 mb-4 flex items-center gap-2">
                                    <TrendingUp className="w-5 h-5" />
                                    Metrado y Dimensiones
                                  </h3>
                                  <div className="bg-gray-950 rounded-xl p-4 border border-blue-900">
                                    <div className="flex items-center justify-between mb-4">
                                      <div>
                                        <p className="font-semibold text-white">¿Definir Metrado Total?</p>
                                        <p className="text-xs text-gray-400">Especificar área total del proyecto (m²)</p>
                                      </div>
                                      <label className="relative inline-flex items-center cursor-pointer">
                                        <input
                                          type="checkbox"
                                          checked={incluirMetrado}
                                          onChange={(e) => setIncluirMetrado(e.target.checked)}
                                          className="sr-only peer"
                                        />
                                        <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                                      </label>
                                    </div>
                                    {incluirMetrado && (
                                      <div className="animate-fadeIn">
                                        <label className="block text-blue-400 font-semibold mb-2">Área Total del Proyecto (m²)</label>
                                        <input
                                          type="number"
                                          value={areaMetrado}
                                          onChange={(e) => setAreaMetrado(e.target.value)}
                                          className="w-full px-4 py-3 bg-gray-900 border border-blue-700 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none text-white text-lg font-bold"
                                          placeholder="Ej: 150"
                                        />
                                      </div>
                                    )}
                                  </div>
                                </div>
                              </div>
                            )}
                          </div>

                          {/* COLUMNA DERECHA: EDITOR DE FASES Y RESUMEN */}
                          <div className="space-y-6">
                            {/* EDITOR DE FASES (Solo Proyecto Complejo) */}
                            {tipoFlujo === 'proyecto-complejo' && (
                              <div className="animate-fadeIn">
                                <div className="flex items-center justify-between mb-4">
                                  <h3 className="text-xl font-bold text-blue-300 flex items-center gap-2">
                                    <Calendar className="w-5 h-5" />
                                    Cronograma Preliminar Detallado
                                  </h3>
                                  <button
                                    onClick={calcularCronogramaPreliminar}
                                    className="px-3 py-1 bg-blue-700 hover:bg-blue-600 rounded text-xs font-bold text-white transition-all shadow hover:shadow-lg"
                                  >
                                    🔄 Recalcular Fases
                                  </button>
                                </div>

                                {fasesCalculadas.length > 0 ? (
                                  <div className="space-y-4">
                                    {fasesCalculadas.map((fase, idx) => (
                                      <div key={idx} className="bg-gray-900/80 rounded-xl p-4 border border-blue-900/50 hover:border-blue-500 transition-all group shadow-md hover:shadow-lg">
                                        <div className="flex justify-between items-center mb-3">
                                          <div className="flex items-center gap-3">
                                            <div className="w-8 h-8 rounded-full bg-blue-900/50 flex items-center justify-center text-blue-300 font-bold border border-blue-700 shadow-inner">
                                              {idx + 1}
                                            </div>
                                            <div>
                                              <h4 className="font-semibold text-white">{fase.nombre}</h4>
                                              <p className="text-xs text-gray-500">{fase.fecha_inicio} - {fase.fecha_fin}</p>
                                            </div>
                                          </div>

                                          {/* Input numérico sincronizado */}
                                          <div className="flex items-center gap-1 bg-black/40 rounded-lg p-1 border border-blue-900/30">
                                            <input
                                              type="number"
                                              min="1"
                                              max={Math.max(60, duracion_total)}
                                              value={fase.duracion_dias}
                                              onChange={(e) => {
                                                const nuevosDias = parseInt(e.target.value) || 1;
                                                const nuevasFases = [...fasesCalculadas];
                                                nuevasFases[idx].duracion_dias = nuevosDias;
                                                setFasesCalculadas(nuevasFases);
                                              }}
                                              className="w-16 bg-transparent text-center font-mono font-bold text-blue-300 focus:outline-none focus:text-white"
                                            />
                                            <span className="text-gray-500 text-xs font-bold px-1">días</span>
                                          </div>
                                        </div>

                                        <div className="flex items-center gap-4">
                                          <input
                                            type="range"
                                            min="1"
                                            max={Math.max(60, duracion_total)}
                                            value={fase.duracion_dias}
                                            onChange={(e) => {
                                              const nuevosDias = parseInt(e.target.value);
                                              const nuevasFases = [...fasesCalculadas];
                                              nuevasFases[idx].duracion_dias = nuevosDias;
                                              setFasesCalculadas(nuevasFases);
                                            }}
                                            className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-blue-500 hover:accent-blue-400"
                                          />
                                        </div>
                                      </div>
                                    ))}

                                    <div className="text-center mt-4 text-xs text-gray-400 italic">
                                      * Ajusta los sliders para redistribuir la duración.
                                    </div>
                                  </div>
                                ) : (
                                  <div className="text-center p-8 border border-dashed border-gray-700 rounded-xl bg-gray-900/30 flex flex-col items-center justify-center">
                                    <Calendar className="w-12 h-12 text-gray-600 mb-4" />
                                    <p className="text-gray-400 mb-4">No se han generado fases aún.</p>
                                    <button
                                      onClick={calcularCronogramaPreliminar}
                                      className="px-6 py-2 bg-gradient-to-r from-blue-700 to-blue-600 hover:from-blue-600 hover:to-blue-500 rounded text-white font-bold transition-all shadow-lg hover:scale-105"
                                    >
                                      🚀 Generar Fases Ahora
                                    </button>
                                  </div>
                                )}
                              </div>
                            )}

                            {/* RESUMEN DEL PROYECTO (Siempre Visible) */}
                            <ProyectoResumen
                              datos={datosCronograma}
                              fases={fasesCalculadas}
                              usarDiasHabiles={datosCalendario?.usarDiasHabiles}
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {esInforme && (
                    <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-green-700 shadow-xl">
                      <h2 className="text-2xl font-bold mb-4 text-green-400">📄 Configuración del Informe</h2>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-green-400 font-semibold mb-2">Proyecto Base *</label>
                          <select
                            value={proyectoSeleccionado}
                            onChange={(e) => setProyectoSeleccionado(e.target.value)}
                            className="w-full px-4 py-3 bg-gray-950 border border-green-700 rounded-xl focus:ring-2 focus:ring-green-500 focus:outline-none text-white">
                            <option value="">Seleccionar proyecto...</option>
                            {proyectosMock.map(p => (
                              <option key={p.id} value={p.id}>{p.nombre} - {p.cliente}</option>
                            ))}
                            <option value="general">📋 Informe General</option>
                          </select>
                        </div>

                        <div>
                          <label className="block text-green-400 font-semibold mb-2">Formato de Salida</label>
                          <select
                            value={formatoInforme}
                            onChange={(e) => setFormatoInforme(e.target.value)}
                            className="w-full px-4 py-3 bg-gray-950 border border-green-700 rounded-xl focus:ring-2 focus:ring-green-500 focus:outline-none text-white">
                            <option value="word">📄 Word (Editable)</option>
                            <option value="pdf">📃 PDF (Final)</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* SERVICIO E INDUSTRIA */}
                  <div className={`bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-${colores.border} shadow-xl`}>
                    <h2 className={`text-2xl font-bold mb-4 text-${colores.primary}-400`}>⚙️ Tipo de Servicio</h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {servicios.map(servicio => (
                        <button
                          key={servicio.id}
                          onClick={() => setServicioSeleccionado(servicio.id)}
                          className={`p-4 rounded-xl border-2 transition-all duration-300 text-left ${servicioSeleccionado === servicio.id
                            ? 'border-yellow-500 bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl scale-105'
                            : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800'
                            }`}>
                          <div className="text-2xl mb-2">{servicio.icon}</div>
                          <div className="text-sm font-semibold">{servicio.nombre.split(' ').slice(1).join(' ')}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className={`bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-${colores.border} shadow-xl`}>
                    <h2 className={`text-2xl font-bold mb-4 text-${colores.primary}-400`}>🏢 Industria</h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {industrias.map(industria => (
                        <button
                          key={industria.id}
                          onClick={() => setIndustriaSeleccionada(industria.id)}
                          className={`p-3 rounded-xl border-2 transition-all duration-300 ${industriaSeleccionada === industria.id
                            ? 'border-yellow-500 bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl'
                            : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800'
                            }`}>
                          <div className="text-sm font-semibold">{industria.nombre}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* DESCRIPCIÓN */}
                  <div className={`bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-${colores.border} shadow-xl`}>
                    <h2 className={`text-2xl font-bold mb-4 text-${colores.primary}-400`}>📝 Descripción Detallada</h2>

                    {esCotizacion && servicioSeleccionado && basePreciosUniversal[servicioSeleccionado] && (
                      <div className="mb-4 p-4 bg-blue-950 bg-opacity-50 border border-blue-700 rounded-xl">
                        <p className="text-sm font-semibold text-blue-300 mb-2">
                          💡 Precios base {servicios.find(s => s.id === servicioSeleccionado)?.nombre}
                        </p>
                        <div className="grid grid-cols-2 gap-2 text-xs text-gray-300">
                          {Object.entries(basePreciosUniversal[servicioSeleccionado]).slice(0, 4).map(([item, precio]) => (
                            <div key={item}>• {item}: S/ {precio}</div>
                          ))}
                        </div>
                      </div>
                    )}

                    <textarea
                      value={contextoUsuario}
                      onChange={(e) => setContextoUsuario(e.target.value)}
                      className="w-full h-32 px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none resize-none mb-4 text-white placeholder-gray-500"
                      placeholder={
                        esCotizacion ? "Describe el proyecto a cotizar detalladamente..." :
                          esProyecto ? "Describe los objetivos y alcance del proyecto..." :
                            "Describe el propósito y contenido del informe..."
                      }
                    />

                    {/* UPLOAD DE DOCUMENTOS */}
                    <div className="border-t-2 border-gray-800 pt-4">
                      <h3 className="text-lg font-semibold mb-3 text-gray-300">Documentos (Opcional)</h3>
                      <div className="border-2 border-dashed border-gray-700 rounded-xl p-6 text-center hover:border-yellow-600 transition-all cursor-pointer mb-4 bg-gray-950 bg-opacity-50">
                        <input type="file" multiple onChange={handleFileUpload} className="hidden" id="fileInput" accept=".pdf,.png,.jpg,.jpeg,.gif,.webp,.xlsx,.xls,.docx,.doc,.html,.json,.txt,.csv" />
                        <label htmlFor="fileInput" className="cursor-pointer">
                          <Upload className="w-12 h-12 mx-auto mb-3 text-yellow-500" />
                          <p className="text-sm text-gray-400 font-semibold">Sube documentos (máx 10MB)</p>
                        </label>
                      </div>

                      {archivos.length > 0 && (
                        <div className="space-y-2">
                          <p className="text-sm font-semibold text-yellow-400 mb-2">📁 Archivos:</p>
                          {archivos.map((archivo, index) => (
                            <div key={index} className="flex items-center justify-between bg-gray-950 bg-opacity-70 p-3 rounded-xl border border-gray-800">
                              <div className="flex items-center gap-2">
                                <FileText className="w-5 h-5 text-yellow-500" />
                                <span className="text-sm font-semibold">{archivo.nombre}</span>
                              </div>
                              <button
                                onClick={() => setArchivos(prev => prev.filter((_, i) => i !== index))}
                                className="text-red-400 hover:text-red-300">
                                <X className="w-5 h-5" />
                              </button>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* BOTÓN CONTINUAR */}
                  <button
                    onClick={async () => {
                      // ✅ Guardar proyecto en BD antes de ir al chat
                      if (esProyecto) {
                        await guardarProyectoEnBD();
                      }
                      setPaso(2);
                    }}
                    disabled={!servicioSeleccionado || !industriaSeleccionada || !contextoUsuario.trim() ||
                      (esProyecto && (!nombre_proyecto || !datosCliente.nombre)) ||
                      (esInforme && !proyectoSeleccionado)}
                    className="w-full bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 disabled:from-gray-800 disabled:to-gray-700 disabled:cursor-not-allowed py-4 rounded-xl font-bold text-lg text-black shadow-2xl border-2 border-yellow-400 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-3">
                    <MessageSquare className="w-6 h-6" />
                    Comenzar Chat con Vista Previa
                  </button>
                </div>
              )}
              {/* PASO 2: CHAT + VISTA PREVIA SPLIT-SCREEN */}
              {paso === 2 && (
                <div className="max-w-full mx-auto h-[calc(100vh-200px)] overflow-hidden flex flex-col">



                  {/* 🔥 MODAL: Preview Pantalla Completa */}
                  {viewMode === 'preview' && (
                    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
                      <div className="relative w-full h-full max-w-7xl bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden">
                        <button
                          onClick={() => setViewMode('split')}
                          className="absolute top-4 right-4 z-10 p-2 bg-red-600 hover:bg-red-500 text-white rounded-lg transition-all shadow-lg"
                        >
                          <X className="w-6 h-6" />
                        </button>
                        <div className="flex-1 overflow-y-auto p-6">
                          <VistaPreviaProfesional
                            cotizacion={cotizacion || proyecto || informe || datosEditables}
                            onGenerarDocumento={handleDescargar}
                            onDatosChange={handleDatosChange}
                            tipoDocumento={tipoFlujo}
                            htmlPreview={htmlPreview}
                            esquemaColores={esquemaColores}
                            logoBase64={logoBase64}
                            fuenteDocumento={fuenteDocumento}
                            ocultarIGV={ocultarIGV}
                            ocultarPreciosUnitarios={ocultarPreciosUnitarios}
                            ocultarTotalesPorItem={ocultarTotalesPorItem}
                            modoEdicion={modoEdicion}
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="flex-1 overflow-hidden grid grid-cols-12 h-full gap-4">


                    {/* CHAT (IZQUIERDA) */}
                    {servicioSeleccionado === 'itse' && tipoFlujo === 'cotizacion-simple' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}>
                        <PiliITSEChat
                          onDatosGenerados={(datos) => { console.log(' DATOS RECIBIDOS DE ITSE:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }}
                          onBotonesUpdate={(botones) => setBotonesContextuales(botones)}
                          onBack={() => setPaso(1)}
                          onFinish={() => setPaso(3)}
                          viewMode={viewMode}
                          setViewMode={setViewMode}
                        />
                      </div>
                    ) : servicioSeleccionado === 'electricidad' && tipoFlujo === 'cotizacion-simple' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}>
                        <PiliElectricidadChat
                          onDatosGenerados={(datos) => { console.log('✅ DATOS RECIBIDOS DE ELECTRICIDAD:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }}
                          onBotonesUpdate={(botones) => setBotonesContextuales(botones)}
                          onBack={() => setPaso(1)}
                          onFinish={() => setPaso(3)}
                          viewMode={viewMode}
                          setViewMode={setViewMode}
                        />
                      </div>
                    ) : servicioSeleccionado === 'puesta-tierra' && tipoFlujo === 'cotizacion-simple' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}>
                        <PiliPuestaTierraChat
                          onDatosGenerados={(datos) => { console.log('✅ DATOS RECIBIDOS DE PUESTA A TIERRA:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }}
                          onBotonesUpdate={(botones) => setBotonesContextuales(botones)}
                          onBack={() => setPaso(1)}
                          onFinish={() => setPaso(3)}
                          viewMode={viewMode}
                          setViewMode={setViewMode}
                        />
                      </div>
                    ) : servicioSeleccionado === 'contra-incendios' && tipoFlujo === 'cotizacion-simple' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}>
                        <PiliContraIncendiosChat
                          onDatosGenerados={(datos) => { console.log('✅ DATOS CONTRA INCENDIOS:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }}
                          onBotonesUpdate={(botones) => setBotonesContextuales(botones)}
                          onBack={() => setPaso(1)}
                          onFinish={() => setPaso(3)}
                          viewMode={viewMode}
                          setViewMode={setViewMode}
                        />
                      </div>
                    ) : servicioSeleccionado === 'domotica' && tipoFlujo === 'cotizacion-simple' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}>
                        <PiliDomoticaChat
                          onDatosGenerados={(datos) => { console.log('✅ DATOS DOMÓTICA:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }}
                          onBotonesUpdate={(botones) => setBotonesContextuales(botones)}
                          onBack={() => setPaso(1)}
                          onFinish={() => setPaso(3)}
                          viewMode={viewMode}
                          setViewMode={setViewMode}
                        />
                      </div>
                    ) : servicioSeleccionado === 'cctv' && tipoFlujo === 'cotizacion-simple' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}><PiliCCTVChat onDatosGenerados={(datos) => { console.log('✅ DATOS CCTV:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }} onBotonesUpdate={(botones) => setBotonesContextuales(botones)} onBack={() => setPaso(1)} onFinish={() => setPaso(3)} viewMode={viewMode} setViewMode={setViewMode} /></div>
                    ) : servicioSeleccionado === 'redes' && tipoFlujo === 'cotizacion-simple' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}><PiliRedesChat onDatosGenerados={(datos) => { console.log('✅ DATOS REDES:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }} onBotonesUpdate={(botones) => setBotonesContextuales(botones)} onBack={() => setPaso(1)} onFinish={() => setPaso(3)} viewMode={viewMode} setViewMode={setViewMode} /></div>
                    ) : servicioSeleccionado === 'automatizacion-industrial' && tipoFlujo === 'cotizacion-simple' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}><PiliAutomatizacionChat onDatosGenerados={(datos) => { console.log('✅ DATOS AUTOMATIZACIÓN:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }} onBotonesUpdate={(botones) => setBotonesContextuales(botones)} onBack={() => setPaso(1)} onFinish={() => setPaso(3)} viewMode={viewMode} setViewMode={setViewMode} /></div>
                    ) : servicioSeleccionado === 'expedientes' && tipoFlujo === 'cotizacion-simple' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}><PiliExpedientesChat onDatosGenerados={(datos) => { console.log('✅ DATOS EXPEDIENTES:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }} onBotonesUpdate={(botones) => setBotonesContextuales(botones)} onBack={() => setPaso(1)} onFinish={() => setPaso(3)} viewMode={viewMode} setViewMode={setViewMode} /></div>
                    ) : servicioSeleccionado === 'saneamiento' && tipoFlujo === 'cotizacion-simple' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}><PiliSaneamientoChat onDatosGenerados={(datos) => { console.log('✅ DATOS SANEAMIENTO:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }} onBotonesUpdate={(botones) => setBotonesContextuales(botones)} onBack={() => setPaso(1)} onFinish={() => setPaso(3)} viewMode={viewMode} setViewMode={setViewMode} /></div>
                    ) : servicioSeleccionado === 'electricidad' && tipoFlujo === 'cotizacion-compleja' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}><PiliElectricidadComplejoChat onDatosGenerados={(datos) => { console.log('✅ DATOS ELECTRICIDAD COMPLEJO:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }} onBotonesUpdate={(botones) => setBotonesContextuales(botones)} onBack={() => setPaso(1)} onFinish={() => setPaso(3)} viewMode={viewMode} setViewMode={setViewMode} /></div>
                    ) : servicioSeleccionado === 'automatizacion-industrial' && tipoFlujo === 'cotizacion-compleja' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}><PiliAutomatizacionComplejoChat onDatosGenerados={(datos) => { console.log('✅ DATOS AUTOMATIZACIÓN COMPLEJO:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }} onBotonesUpdate={(botones) => setBotonesContextuales(botones)} onBack={() => setPaso(1)} onFinish={() => setPaso(3)} viewMode={viewMode} setViewMode={setViewMode} /></div>
                    ) : servicioSeleccionado === 'contra-incendios' && tipoFlujo === 'cotizacion-compleja' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}><PiliContraIncendiosComplejoChat onDatosGenerados={(datos) => { console.log('✅ DATOS CONTRA INCENDIOS COMPLEJO:', datos); setCotizacion(datos); setDatosEditables(datos); setMostrarPreview(true); actualizarVistaPrevia(); }} onBotonesUpdate={(botones) => setBotonesContextuales(botones)} onBack={() => setPaso(1)} onFinish={() => setPaso(3)} viewMode={viewMode} setViewMode={setViewMode} /></div>
                    ) : servicioSeleccionado === 'electricidad' && tipoFlujo === 'proyecto-simple' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}><PiliElectricidadProyectoSimpleChat datosCliente={datosCliente} nombre_proyecto={nombre_proyecto} presupuesto={presupuesto} moneda={moneda} duracion_total={duracion_total} onDatosGenerados={(datos) => { console.log('✅ DATOS PROYECTO SIMPLE:', datos); setProyecto(datos); setDatosEditables(datos); setMostrarPreview(true); }} onBotonesUpdate={(botones) => setBotonesContextuales(botones)} onBack={() => setPaso(1)} onFinish={() => setPaso(3)} viewMode={viewMode} setViewMode={setViewMode} /></div>
                    ) : servicioSeleccionado === 'electricidad' && tipoFlujo === 'proyecto-complejo' ? (
                      <div className={`${viewMode === 'preview' ? 'hidden' : viewMode === 'chat' ? 'fixed inset-0 z-50 bg-black/90 backdrop-blur-sm p-4 flex flex-col' : 'col-span-6'} h-full min-h-0 overflow-y-auto`}>
                        <ModuloC
                          datosIniciales={proyecto}
                          onBack={() => setPaso(1)}
                          onGuardarBorrador={handleGuardarBorrador}
                          proyectoId={proyectoId}
                          setProyectoId={setProyectoId}
                          onGenerarDocumento={(fmt) => {
                            // Solicitud de documento desde Módulo
                            handleDescargar(fmt);
                          }}
                        />

                      </div>
                    ) : (
                      <div className="col-span-6 bg-white rounded-2xl shadow-xl flex flex-col">
                        <div className="bg-gradient-to-r from-yellow-600 to-yellow-500 p-4 rounded-t-2xl">
                          <h3 className="text-xl font-bold text-black flex items-center gap-2">
                            <div className="bg-white p-1 rounded-full">
                              <PiliAvatar size={24} showCrown={true} />
                            </div>
                            👑 PILI - {servicios.find(s => s.id === servicioSeleccionado)?.nombre}
                          </h3>
                        </div>

                        {/* CONVERSACIÓN */}
                        <div ref={chatContainerRef} className="flex-grow bg-gray-100 p-4 overflow-y-auto">
                          {conversacion.length === 0 ? (
                            <div className="text-center text-gray-600 mt-8">
                              <div className="inline-block bg-yellow-600 p-3 rounded-full mb-3">
                                <PiliAvatar size={32} showCrown={true} />
                              </div>
                              <p className="font-semibold text-lg">¡Hola! Soy 👑 PILI - Tu Asistente IA</p>
                              <p className="text-xs text-gray-500 mb-2">Procesadora Inteligente de Licitaciones Industriales v3.0</p>
                              <p className="text-sm mt-1">
                                {esCotizacion && "Empezemos con tu cotización..."}
                                {esProyecto && "Vamos a planificar tu proyecto..."}
                                {esInforme && "Generemos tu informe profesional..."}
                              </p>
                            </div>
                          ) : (
                            <div className="space-y-3">
                              {conversacion.map((mensaje, index) => (
                                <div key={index} className={`flex ${mensaje.tipo === 'usuario' ? 'justify-end' : 'justify-start'}`}>
                                  <div className={`max-w-[85%] p-3 rounded-2xl ${mensaje.tipo === 'usuario'
                                    ? 'bg-yellow-600 text-black'
                                    : 'bg-white border-2 border-gray-300 text-gray-800'
                                    }`}>
                                    <p className="text-sm">{mensaje.mensaje}</p>
                                  </div>
                                </div>
                              ))}

                              {analizando && (
                                <div className="flex justify-start">
                                  <div className="bg-white border-2 border-gray-300 p-3 rounded-2xl">
                                    <div className="flex items-center gap-2 text-gray-600">
                                      <div className="bg-yellow-600 p-1 rounded-full animate-pulse">
                                        <PiliAvatar size={16} showCrown={true} />
                                      </div>
                                      <Loader className="w-4 h-4 animate-spin text-yellow-600" />
                                      <span className="text-sm font-medium">PILI está pensando... 🤔</span>
                                    </div>
                                  </div>
                                </div>
                              )}
                            </div>
                          )}
                        </div>

                        {/* ✅ NUEVO: Indicador de Progreso de Datos */}
                        {(datosRecopilados.length > 0 || datosFaltantes.length > 0) && (
                          <div className="px-4 py-3 bg-gradient-to-r from-blue-50 to-indigo-50 border-t border-blue-200">
                            <div className="bg-white rounded-lg p-3 shadow-sm">
                              <div className="flex justify-between items-center mb-2">
                                <span className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                                  <BarChart3 className="w-4 h-4 text-blue-600" />
                                  Progreso de Datos
                                </span>
                                <span className="text-xs font-bold text-blue-600 bg-blue-100 px-2 py-1 rounded">
                                  {progresoChat}
                                </span>
                              </div>

                              <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                                <div
                                  className="bg-gradient-to-r from-blue-500 to-indigo-600 h-2 rounded-full transition-all duration-500"
                                  style={{
                                    width: `${(datosRecopilados.length / (datosRecopilados.length + datosFaltantes.length)) * 100}%`
                                  }}
                                />
                              </div>

                              <div className="flex flex-wrap gap-2">
                                {datosRecopilados.map(campo => (
                                  <span
                                    key={campo}
                                    className="bg-green-100 text-green-800 px-2 py-1 rounded-md text-xs font-medium flex items-center gap-1"
                                  >
                                    <CheckCircle className="w-3 h-3" />
                                    {campo.replace('_', ' ')}
                                  </span>
                                ))}
                                {datosFaltantes.map(campo => (
                                  <span
                                    key={campo}
                                    className="bg-gray-100 text-gray-600 px-2 py-1 rounded-md text-xs flex items-center gap-1"
                                  >
                                    <Clock className="w-3 h-3" />
                                    {campo.replace('_', ' ')}
                                  </span>
                                ))}
                              </div>
                            </div>
                          </div>
                        )}

                        {/* BOTONES CONTEXTUALES */}
                        {botonesContextuales.length > 0 && (
                          <div className="px-4 py-2 bg-gray-50 border-t">
                            <div className="flex flex-wrap gap-2">
                              {botonesContextuales.map((boton, index) => (
                                <button
                                  key={index}
                                  onClick={() => enviarRespuestaRapida(boton)}
                                  className="px-3 py-1 bg-yellow-100 hover:bg-yellow-200 text-gray-800 rounded-lg text-xs border border-yellow-300 transition-all">
                                  {boton}
                                </button>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* INPUT CHAT */}
                        <div className="p-4 bg-white border-t rounded-b-2xl">
                          <div className="flex gap-2">
                            <input
                              type="text"
                              value={inputChat}
                              onChange={(e) => setInputChat(e.target.value)}
                              onKeyPress={(e) => e.key === 'Enter' && !analizando && handleEnviarMensajeChat()}
                              placeholder="Escribe aquí..."
                              className="flex-grow p-2 border-2 border-gray-300 rounded-xl focus:border-yellow-500 focus:outline-none text-gray-800"
                              disabled={analizando}
                            />
                            <button
                              onClick={handleEnviarMensajeChat}
                              disabled={analizando || !inputChat.trim()}
                              className="p-2 bg-yellow-600 hover:bg-yellow-500 disabled:bg-gray-400 text-black rounded-xl transition-all">
                              <Send className="w-5 h-5" />
                            </button>
                          </div>

                          <div className="flex justify-between items-center mt-3">
                            <button
                              onClick={() => setPaso(1)}
                              className="px-3 py-1 bg-gray-300 hover:bg-gray-400 text-gray-800 rounded-lg text-sm">
                              ← Configuración
                            </button>
                            <button
                              onClick={() => setPaso(3)}
                              disabled={!mostrarPreview}
                              className="px-4 py-1 bg-green-600 hover:bg-green-500 disabled:bg-gray-400 text-white font-bold rounded-lg text-sm">
                              Finalizar →
                            </button>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* VISTA PREVIA (DERECHA) */}
                    <div className={`${viewMode === 'chat' ? 'hidden' : viewMode === 'preview' ? 'col-span-12' : 'col-span-6'} h-full min-h-0 bg-white rounded-2xl shadow-xl flex flex-col overflow-hidden`}>
                      <div className="bg-gradient-to-r from-blue-600 to-blue-500 p-4 shrink-0 flex justify-between items-center">
                        <div className="flex items-center gap-2">
                          <Eye className="w-6 h-6 text-white" />
                          <h3 className="text-xl font-bold text-white">Vista Previa</h3>
                        </div>

                        {mostrarPreview && (
                          <div className="flex items-center gap-2">
                            <button
                              onClick={() => setModoEdicion(!modoEdicion)}
                              className="px-3 py-1 bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded-lg text-sm flex items-center gap-1">
                              <Edit className="w-4 h-4" />
                              {modoEdicion ? 'Ver' : 'Editar'}
                            </button>

                            {esCotizacion && (
                              <div className="flex gap-2">
                                <button
                                  onClick={() => setOcultarIGV(!ocultarIGV)}
                                  className="px-2 py-1 bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded text-xs">
                                  {ocultarIGV ? 'Mostrar' : 'Ocultar'} IGV
                                </button>
                                <button
                                  onClick={() => setOcultarPreciosUnitarios(!ocultarPreciosUnitarios)}
                                  className="px-2 py-1 bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded text-xs">
                                  P. Unit
                                </button>
                              </div>
                            )}
                          </div>
                        )}
                      </div>

                      <div className="flex-1 overflow-y-scroll min-h-0 p-4 bg-white custom-scrollbar scrollbar-gold">
                        {!mostrarPreview ? (
                          <div className="text-center text-gray-500 mt-20">
                            <Eye className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                            <p className="text-lg">Vista Previa</p>
                            <p className="text-sm">Aparecerá cuando la IA genere contenido</p>
                          </div>
                        ) : (() => {
                          // ✅ RENDERIZAR VistaPreviaProfesional en Paso 2
                          return (
                            <VistaPreviaProfesional
                              // ✅ FIX CRÍTICO: Selección explícita de datos para evitar conflictos de estado
                              cotizacion={
                                esCotizacion ? cotizacion :
                                  esProyecto ? proyecto :
                                    esInforme ? informe :
                                      datosEditables
                              }
                              onGenerarDocumento={handleDescargar}
                              onDatosChange={handleDatosChange} // ✅ Conectar callback
                              tipoDocumento={tipoFlujo}
                              htmlPreview={htmlPreview}
                              esquemaColores={esquemaColores}
                              logoBase64={logoBase64}
                              fuenteDocumento={fuenteDocumento}
                              ocultarIGV={ocultarIGV}
                              ocultarPreciosUnitarios={ocultarPreciosUnitarios}
                              ocultarTotalesPorItem={ocultarTotalesPorItem}
                              modoEdicion={modoEdicion}
                            />
                          );
                        })()}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* PASO 3: FINALIZACIÓN */}
              {paso === 3 && (
                <div className="max-w-5xl mx-auto space-y-6">
                  <div className="bg-white rounded-2xl p-8 shadow-xl border-4 border-green-600">
                    <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
                      <CheckCircle className="w-8 h-8 text-green-600" />
                      Documento Listo para Generar
                    </h2>

                    <div className="bg-green-50 p-6 rounded-xl mb-6">
                      <h3 className="text-lg font-bold text-green-800 mb-3">✅ Lo que se incluirá:</h3>
                      <div className="grid grid-cols-2 gap-4 text-sm text-green-700">
                        <div className="space-y-1">
                          <p>• Contenido generado por IA</p>
                          <p>• Datos personalizados</p>
                          <p>• Formato profesional Tesla</p>
                        </div>
                        <div className="space-y-1">
                          {logoBase64 && <p>• Logo de la empresa</p>}
                          <p>• Colores corporativos</p>
                          <p>• Información de contacto</p>
                        </div>
                      </div>
                    </div>

                    {/* ✅ VISTA PREVIA PROFESIONAL A PANTALLA COMPLETA */}
                    <VistaPreviaProfesional
                      cotizacion={cotizacion || proyecto || informe || {}}
                      onGenerarDocumento={handleDescargar}
                      tipoDocumento={tipoFlujo}
                      htmlPreview={htmlPreview}
                      esquemaColores={esquemaColores}
                      logoBase64={logoBase64}
                      fuenteDocumento={fuenteDocumento}
                      ocultarIGV={ocultarIGV}
                      ocultarPreciosUnitarios={ocultarPreciosUnitarios}
                      ocultarTotalesPorItem={ocultarTotalesPorItem}
                    />


                    {/* ✅ PANEL DE PERSONALIZACIÓN */}
                    <div className="mb-6 border-2 border-blue-500 rounded-xl overflow-hidden">
                      {/* Header del Panel */}
                      <button
                        onClick={() => setMostrarPanelPersonalizacion(!mostrarPanelPersonalizacion)}
                        className="w-full bg-gradient-to-r from-blue-600 to-blue-500 p-4 flex items-center justify-between hover:from-blue-700 hover:to-blue-600 transition-all">
                        <div className="flex items-center gap-3">
                          <Settings className="w-6 h-6 text-white" />
                          <h3 className="text-lg font-bold text-white">Personalización del Documento</h3>
                        </div>
                        {mostrarPanelPersonalizacion ? (
                          <ChevronUp className="w-5 h-5 text-white" />
                        ) : (
                          <ChevronDown className="w-5 h-5 text-white" />
                        )}
                      </button>

                      {/* Contenido del Panel (Colapsable) */}
                      {mostrarPanelPersonalizacion && (
                        <div className="bg-gray-900 p-6 space-y-6">
                          {/* Sección: Esquema de Colores */}
                          <div>
                            <label className="block text-blue-400 font-semibold mb-3 flex items-center gap-2">
                              <PieChart className="w-5 h-5" />
                              Esquema de Colores
                            </label>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                              <button
                                onClick={() => setEsquemaColores('azul-tesla')}
                                className={`p-3 rounded-lg border-2 transition-all ${esquemaColores === 'azul-tesla'
                                  ? 'border-blue-500 bg-blue-900 text-white'
                                  : 'border-gray-700 bg-gray-800 text-gray-300 hover:border-blue-600'
                                  }`}>
                                <div className="flex items-center gap-2 mb-1">
                                  <div className="w-4 h-4 rounded-full bg-blue-500"></div>
                                  <span className="font-semibold">Azul Tesla</span>
                                </div>
                                <span className="text-xs">Corporativo</span>
                              </button>
                              <button
                                onClick={() => setEsquemaColores('rojo-energia')}
                                className={`p-3 rounded-lg border-2 transition-all ${esquemaColores === 'rojo-energia'
                                  ? 'border-red-500 bg-red-900 text-white'
                                  : 'border-gray-700 bg-gray-800 text-gray-300 hover:border-red-600'
                                  }`}>
                                <div className="flex items-center gap-2 mb-1">
                                  <div className="w-4 h-4 rounded-full bg-red-500"></div>
                                  <span className="font-semibold">Rojo Energía</span>
                                </div>
                                <span className="text-xs">Vibrante</span>
                              </button>
                              <button
                                onClick={() => setEsquemaColores('verde-ecologico')}
                                className={`p-3 rounded-lg border-2 transition-all ${esquemaColores === 'verde-ecologico'
                                  ? 'border-green-500 bg-green-900 text-white'
                                  : 'border-gray-700 bg-gray-800 text-gray-300 hover:border-green-600'
                                  }`}>
                                <div className="flex items-center gap-2 mb-1">
                                  <div className="w-4 h-4 rounded-full bg-green-500"></div>
                                  <span className="font-semibold">Verde Eco</span>
                                </div>
                                <span className="text-xs">Sostenible</span>
                              </button>
                              <button
                                onClick={() => setEsquemaColores('personalizado')}
                                className={`p-3 rounded-lg border-2 transition-all ${esquemaColores === 'personalizado'
                                  ? 'border-purple-500 bg-purple-900 text-white'
                                  : 'border-gray-700 bg-gray-800 text-gray-300 hover:border-purple-600'
                                  }`}>
                                <div className="flex items-center gap-2 mb-1">
                                  <div className="w-4 h-4 rounded-full bg-gradient-to-r from-purple-500 to-pink-500"></div>
                                  <span className="font-semibold">Personalizado</span>
                                </div>
                                <span className="text-xs">A medida</span>
                              </button>
                            </div>
                          </div>

                          {/* Sección: Fuente */}
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                              <label className="block text-blue-400 font-semibold mb-3">Fuente del Documento</label>
                              <select
                                value={fuenteDocumento}
                                onChange={(e) => setFuenteDocumento(e.target.value)}
                                className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors">
                                <option value="Calibri">Calibri (Recomendada)</option>
                                <option value="Arial">Arial</option>
                                <option value="Times New Roman">Times New Roman</option>
                              </select>
                            </div>

                            <div>
                              <label className="block text-blue-400 font-semibold mb-3">Tamaño de Fuente</label>
                              <select
                                value={tamañoFuente}
                                onChange={(e) => setTamañoFuente(Number(e.target.value))}
                                className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors">
                                <option value={10}>10 pt (Pequeña)</option>
                                <option value={11}>11 pt (Normal)</option>
                                <option value={12}>12 pt (Grande)</option>
                              </select>
                            </div>
                          </div>

                          {/* Sección: Logo */}
                          <div>
                            <label className="block text-blue-400 font-semibold mb-3 flex items-center gap-2">
                              <Upload className="w-5 h-5" />
                              Logo de la Empresa
                            </label>
                            <div className="flex items-center gap-4">
                              <button
                                onClick={() => setMostrarLogo(!mostrarLogo)}
                                className={`px-4 py-2 rounded-lg font-semibold transition-all ${mostrarLogo
                                  ? 'bg-green-600 text-white'
                                  : 'bg-gray-700 text-gray-300'
                                  }`}>
                                {mostrarLogo ? '✓ Mostrar Logo' : '✕ Ocultar Logo'}
                              </button>
                              <input
                                ref={fileInputLogoRef}
                                type="file"
                                accept="image/*"
                                onChange={cargarLogo}
                                className="hidden"
                              />
                              <button
                                onClick={() => fileInputLogoRef.current?.click()}
                                className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-500 transition-all flex items-center gap-2">
                                <Upload className="w-4 h-4" />
                                {logoBase64 ? 'Cambiar Logo' : 'Subir Logo'}
                              </button>
                              {logoBase64 && (
                                <span className="text-green-400 text-sm">✓ Logo cargado</span>
                              )}
                            </div>
                          </div>

                          {/* Sección: Opciones de Visualización */}
                          <div>
                            <label className="block text-blue-400 font-semibold mb-3">Opciones de Visualización</label>
                            <div className="flex flex-wrap gap-4">
                              <button
                                onClick={() => setOcultarIGV(!ocultarIGV)}
                                className={`px-4 py-2 rounded-lg font-semibold transition-all ${ocultarIGV
                                  ? 'bg-blue-600 text-white'
                                  : 'bg-gray-700 text-gray-300'
                                  }`}>
                                {ocultarIGV ? '✓ IGV Oculto' : 'Mostrar IGV'}
                              </button>
                              <button
                                onClick={() => setOcultarPreciosUnitarios(!ocultarPreciosUnitarios)}
                                className={`px-4 py-2 rounded-lg font-semibold transition-all ${ocultarPreciosUnitarios
                                  ? 'bg-blue-600 text-white'
                                  : 'bg-gray-700 text-gray-300'
                                  }`}>
                                {ocultarPreciosUnitarios ? '✓ P. Unit. Ocultos' : 'Mostrar P. Unitarios'}
                              </button>
                              <button
                                onClick={() => setOcultarTotalesPorItem(!ocultarTotalesPorItem)}
                                className={`px-4 py-2 rounded-lg font-semibold transition-all ${ocultarTotalesPorItem
                                  ? 'bg-blue-600 text-white'
                                  : 'bg-gray-700 text-gray-300'
                                  }`}>
                                {ocultarTotalesPorItem ? '✓ Totales Ocultos' : 'Mostrar Totales por Ítem'}
                              </button>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* BOTONES DE ACCIÓN */}
                    <div className="flex gap-4">
                      <button
                        onClick={() => setPaso(2)}
                        className="px-6 py-3 bg-gray-600 hover:bg-gray-500 text-white rounded-xl transition-all">
                        ← Volver al Chat
                      </button>

                      <div className="flex-1 flex gap-4">
                        <button
                          onClick={() => handleDescargar('pdf')}
                          disabled={descargando === 'pdf'}
                          className="flex-1 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 disabled:from-gray-600 disabled:to-gray-500 text-white py-3 rounded-xl font-bold transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2">
                          {descargando === 'pdf' ? (
                            <>
                              <Loader className="w-5 h-5 animate-spin" />
                              Generando PDF...
                            </>
                          ) : (
                            <>
                              <FileText className="w-5 h-5" />
                              Descargar PDF
                            </>
                          )}
                        </button>

                        <button
                          onClick={() => handleDescargar('word')}
                          disabled={descargando === 'word'}
                          className="flex-1 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 disabled:from-gray-600 disabled:to-gray-500 text-white py-3 rounded-xl font-bold transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2">
                          {descargando === 'word' ? (
                            <>
                              <Loader className="w-5 h-5 animate-spin" />
                              Generando Word...
                            </>
                          ) : (
                            <>
                              <Download className="w-5 h-5" />
                              Descargar Word
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      );
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6">
      <div className="max-w-5xl mx-auto text-center">
        <h1 className="text-4xl font-bold text-yellow-400 mb-4">Sistema Tesla v3.0</h1>
        <p className="text-gray-300 mb-6">Sistema profesional completamente funcional</p>
        <button
          onClick={volverAlInicio}
          className="px-6 py-3 bg-yellow-600 text-black rounded-lg font-bold hover:bg-yellow-500 transition-all">
          Ir al Inicio
        </button>
        <div className="mt-8 opacity-0 hover:opacity-100 transition-opacity duration-500">
          <button
            onClick={() => setMostrarDashboard(!mostrarDashboard)}
            className="text-xs text-gray-800 hover:text-red-900"
          >
            🔒 Admin Access
          </button>
        </div>

        {mostrarDashboard && (
          <div className="fixed inset-0 z-[100] bg-black text-white overflow-auto">
            <div className="p-4">
              <button
                onClick={() => setMostrarDashboard(false)}
                className="mb-4 bg-red-600 px-4 py-2 rounded text-white"
              >
                Cerrar Panel
              </button>
              <AdminDashboard />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PILIQuartsApp;