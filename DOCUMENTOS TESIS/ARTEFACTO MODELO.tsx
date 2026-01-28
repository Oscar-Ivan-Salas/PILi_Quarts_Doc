import React, { useState, useRef } from 'react';
import { Upload, MessageSquare, FileText, Download, Zap, Send, Loader, Edit, Save, AlertCircle, CheckCircle, X, Calculator, RefreshCw, Home, FolderOpen, Eye, EyeOff } from 'lucide-react';

const CotizadorPro = () => {
  const [paso, setPaso] = useState(1);
  const [archivos, setArchivos] = useState([]);
  const [conversacion, setConversacion] = useState([]);
  const [contextoUsuario, setContextoUsuario] = useState('');
  const [inputChat, setInputChat] = useState('');
  const [analizando, setAnalizando] = useState(false);
  const [cotizacion, setCotizacion] = useState(null);
  const [modoEdicion, setModoEdicion] = useState(true);
  const [error, setError] = useState('');
  const [exito, setExito] = useState('');
  const [servicioSeleccionado, setServicioSeleccionado] = useState('');
  const [industriaSeleccionada, setIndustriaSeleccionada] = useState('');
  const [estadoCotizacion, setEstadoCotizacion] = useState('borrador');
  const [versionCotizacion, setVersionCotizacion] = useState(1.0);
  const [historialVersiones, setHistorialVersiones] = useState([]);
  const [ocultarPreciosUnitarios, setOcultarPreciosUnitarios] = useState(false);
  const [ocultarTotalesPorItem, setOcultarTotalesPorItem] = useState(false);
  const [modoVisualizacionIGV, setModoVisualizacionIGV] = useState('sin-igv');
  const [debugMode, setDebugMode] = useState(false);
  const fileInputChatRef = useRef(null);
  const fileInputLoadRef = useRef(null);
  const fileInputLogoRef = useRef(null);
  
  const [logoBase64, setLogoBase64] = useState('');
  const [mostrarModalPreview, setMostrarModalPreview] = useState(false);
  
  const [condicionesComerciales, setCondicionesComerciales] = useState({
    incluye_igv: 'NO incluyen IGV (18%)',
    forma_pago: '50% anticipo, 50% contra entrega',
    validez: '15 días calendario',
    garantia: '6 meses',
    otra: ''
  });
  
  const [resumenEditable, setResumenEditable] = useState('');
  const [recomendacionesEditables, setRecomendacionesEditables] = useState('');
  
  const [datosEmpresa, setDatosEmpresa] = useState({
    nombre: 'TESLA ELECTRICIDAD Y AUTOMATIZACION S.A.C.',
    ruc: '20601138787',
    direccion: 'Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos',
    telefono: '906315961',
    email: 'ingenieria.teslaelectricidad@gmail.com',
    ciudad: 'San Juan de Lurigancho, Lima - Perú'
  });

  const servicios = [
    { id: 'electricidad', nombre: '⚡ Electricidad', icon: '⚡' },
    { id: 'itse', nombre: '📋 Certificado ITSE', icon: '📋' },
    { id: 'puesta-tierra', nombre: '🔌 Puesta a Tierra', icon: '🔌' },
    { id: 'contra-incendios', nombre: '🔥 Contra Incendios', icon: '🔥' },
    { id: 'domotica', nombre: '🏠 Domótica', icon: '🏠' },
    { id: 'cctv', nombre: '📹 CCTV', icon: '📹' },
    { id: 'redes', nombre: '🌐 Redes', icon: '🌐' },
    { id: 'camaras-inteligentes', nombre: '📱 Cámaras IA', icon: '📱' },
    { id: 'automatizacion-industrial', nombre: '⚙️ Automatización Industrial', icon: '⚙️' },
    { id: 'digitalizacion', nombre: '📄 Digitalización Administrativa', icon: '📄' },
    { id: 'multiple', nombre: '🔧 Múltiple', icon: '🔧' }
  ];

  const industrias = [
    { id: 'construccion', nombre: '🏗️ Construcción' },
    { id: 'arquitectura', nombre: '🏢 Arquitectura' },
    { id: 'industrial', nombre: '⚙️ Industrial' },
    { id: 'mineria', nombre: '⛏️ Minería - Automatización' },
    { id: 'educacion', nombre: '🎓 Educación - Colegios' },
    { id: 'salud', nombre: '🏥 Salud - Hospitales/Clínicas' },
    { id: 'retail', nombre: '🏪 Retail' },
    { id: 'residencial', nombre: '🏘️ Residencial' },
    { id: 'administrativo', nombre: '📋 Administrativo - Oficinas' },
    { id: 'otro', nombre: '📋 Otro' }
  ];

  const basePreciosUniversal = {
    electricidad: {
      'Punto luz empotrado': 15, 'Tomacorriente doble': 18, 'Interruptor simple': 12,
      'Tablero general trifásico': 2800, 'Tablero depto monofásico': 800,
      'Cable THW 2.5mm²': 2.0, 'Cable THW 4mm²': 3.08, 'Cable THW 6mm²': 4.54,
      'Cable THW 10mm²': 7.62, 'Tubería PVC-P 3/4"': 3.2, 'Luminaria LED 18W': 45,
      'Reflector LED 50W': 85, 'Electricista oficial/día': 230, 'Ayudante/día': 120
    },
    'itse': {
      'Derecho municipal ITSE Bajo': 168.30, 'Derecho municipal ITSE Medio': 208.60,
      'Derecho municipal ITSE Alto': 703.00, 'Derecho municipal ITSE Muy Alto': 1084.60,
      'Renovación ITSE Bajo': 90.30, 'Renovación ITSE Medio': 109.40,
      'Renovación ITSE Alto': 417.40, 'Renovación ITSE Muy Alto': 629.20,
      'Servicio técnico ITSE Bajo': 400, 'Servicio técnico ITSE Medio': 550,
      'Servicio técnico ITSE Alto': 1000, 'Servicio técnico ITSE Muy Alto': 1500,
      'Evaluación técnica inicial': 0, 'Elaboración de planos': 250,
      'Gestión trámite municipal': 150, 'Seguimiento certificado': 100,
      'Visita técnica': 0
    },
    'puesta-tierra': {
      'Pozo tierra completo': 1760, 'Varilla copperweld 5/8"x2.4m': 85,
      'Cable desnudo Cu 35mm²': 12, 'Bentonita sódica 25kg': 45,
      'Sales Thor Gel': 78, 'Conector grapa': 25, 'Registro 30x30cm': 120,
      'Medición resistividad': 450, 'Certificado PAT': 350
    },
    'contra-incendios': {
      'Rociador automático 68°C': 85, 'Detector humo fotoeléctrico': 120,
      'Detector inteligente': 280, 'Extintor PQS 6kg': 85, 'Extintor CO2 6kg': 180,
      'Gabinete CI completo': 450, 'Manguera 1.5"x30m': 320, 'Válvula siamesa': 650,
      'Panel alarmas 4 zonas': 2800, 'Estación manual': 95, 'Sirena': 78,
      'Bomba jockey': 3500, 'Bomba principal': 12500, 'Mini kit CI básico': 450
    },
    'domotica': {
      'Switch WiFi inteligente': 145, 'Sensor movimiento PIR': 89,
      'Termostato WiFi': 320, 'Hub Zigbee': 580, 'Cerradura inteligente': 450,
      'Control RGB': 165, 'Sensor puerta': 65, 'Enchufe inteligente': 45,
      'Control cortinas': 380, 'Panel táctil 7"': 890
    },
    'cctv': {
      'Cámara domo 2MP': 280, 'Cámara bullet 4MP': 420, 'Cámara PTZ': 1250,
      'DVR 8 canales': 450, 'NVR 16 canales PoE': 780, 'Monitor 24"': 520,
      'Disco 2TB Purple': 280, 'Cable UTP Cat6': 2.0, 'Fuente 12V 10A': 65
    },
    'redes': {
      'Cable UTP Cat6': 1.8, 'Fibra óptica monomodo': 3.5, 'Jack RJ45': 3.2,
      'Patch panel 24p': 180, 'Switch 24p PoE': 850, 'Router empresarial': 680,
      'Rack 12U': 420, 'Face plate doble': 12, 'Certificación punto': 35,
      'Access Point WiFi 6': 480
    },
    'camaras-inteligentes': {
      'Cámara IA facial': 680, 'Cámara térmica': 1850, 'Cámara conteo': 890,
      'Software analíticas': 450, 'Servidor IA 8GB': 3500, 'Cámara LPR': 1280
    },
    'automatizacion-industrial': {
      'PLC Siemens S7-1200': 2800, 'PLC Allen Bradley': 3500, 'HMI 7"': 1200,
      'Sensor inductivo': 85, 'Sensor capacitivo': 95, 'Variador frecuencia 5HP': 1800,
      'Variador frecuencia 10HP': 3200, 'Contactor 25A': 120, 'Relé térmico': 95,
      'Encoder incremental': 450, 'Servo motor': 2800, 'Tablero control industrial': 3500,
      'Cable UTP industrial': 3.5, 'Fuente 24VDC 10A': 280, 'Programación PLC/hora': 150
    },
    'digitalizacion': {
      'Scanner profesional': 2800, 'Scanner portátil': 850, 'Software OCR': 450,
      'Servidor NAS 4TB': 1800, 'Sistema gestión documental': 3500,
      'Digitalización por documento': 1.5, 'Índice y clasificación': 0.5,
      'Capacitación personal': 500, 'Soporte mensual': 350
    }
  };

  const volverAlInicio = () => {
    if (window.confirm('¿Volver al inicio? Se perderá el progreso actual si no guardaste.')) {
      setPaso(1);
      setArchivos([]);
      setConversacion([]);
      setContextoUsuario('');
      setCotizacion(null);
      setServicioSeleccionado('');
      setIndustriaSeleccionada('');
      setVersionCotizacion(1.0);
      setHistorialVersiones([]);
      setExito('Reiniciado correctamente');
    }
  };

  const guardarCotizacion = () => {
    try {
      const datos = {
        version: '1.0',
        fecha: new Date().toISOString(),
        empresa: datosEmpresa,
        servicio: servicioSeleccionado,
        industria: industriaSeleccionada,
        contexto: contextoUsuario,
        archivos: archivos.map(a => ({ nombre: a.nombre, tipo: a.tipo, tamano: a.tamano })),
        cotizacion: cotizacion,
        versionCotizacion: versionCotizacion,
        historialVersiones: historialVersiones,
        conversacion: conversacion,
        condicionesComerciales: condicionesComerciales,
        resumenEditable: resumenEditable,
        recomendacionesEditables: recomendacionesEditables,
        ocultarPreciosUnitarios: ocultarPreciosUnitarios,
        ocultarTotalesPorItem: ocultarTotalesPorItem,
        modoVisualizacionIGV: modoVisualizacionIGV,
        logoBase64: logoBase64
      };

      const blob = new Blob([JSON.stringify(datos, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `TESLA_Cotizacion_v${versionCotizacion}_${new Date().toISOString().slice(0,10)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      setExito('Cotización guardada exitosamente');
      setTimeout(() => setExito(''), 3000);
    } catch (error) {
      setError('Error al guardar: ' + error.message);
    }
  };

  const cargarCotizacion = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      const text = await file.text();
      const datos = JSON.parse(text);

      if (window.confirm('¿Cargar esta cotización? Se reemplazará todo el contenido actual.')) {
        setDatosEmpresa(datos.empresa || datosEmpresa);
        setServicioSeleccionado(datos.servicio || '');
        setIndustriaSeleccionada(datos.industria || '');
        setContextoUsuario(datos.contexto || '');
        setCotizacion(datos.cotizacion || null);
        setVersionCotizacion(datos.versionCotizacion || 1.0);
        setHistorialVersiones(datos.historialVersiones || []);
        setConversacion(datos.conversacion || []);
        setCondicionesComerciales(datos.condicionesComerciales || condicionesComerciales);
        setResumenEditable(datos.resumenEditable || '');
        setRecomendacionesEditables(datos.recomendacionesEditables || '');
        setOcultarPreciosUnitarios(datos.ocultarPreciosUnitarios || false);
        setOcultarTotalesPorItem(datos.ocultarTotalesPorItem || false);
        setModoVisualizacionIGV(datos.modoVisualizacionIGV || 'sin-igv');
        setLogoBase64(datos.logoBase64 || '');
        
        if (datos.cotizacion) {
          setPaso(3);
        } else if (datos.conversacion && datos.conversacion.length > 0) {
          setPaso(2);
        }
        
        setExito('Cotización cargada exitosamente');
        setTimeout(() => setExito(''), 3000);
      }
    } catch (error) {
      setError('Error al cargar archivo: ' + error.message);
    }
    
    e.target.value = '';
  };

  const cargarLogo = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      setError('Solo se permiten imágenes (PNG, JPG, WebP)');
      return;
    }

    if (file.size > 2 * 1024 * 1024) {
      setError('El logo debe pesar menos de 2MB. Usa TinyPNG.com para comprimirlo.');
      return;
    }

    try {
      const reader = new FileReader();
      reader.onload = (event) => {
        setLogoBase64(event.target.result);
        setExito('✅ Logo cargado correctamente');
        setTimeout(() => setExito(''), 3000);
      };
      reader.readAsDataURL(file);
    } catch (error) {
      setError('Error al cargar logo: ' + error.message);
    }

    e.target.value = '';
  };

  const validarDatos = () => {
    if (!datosEmpresa.nombre.trim()) {
      setError('Nombre de empresa obligatorio');
      return false;
    }
    if (datosEmpresa.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(datosEmpresa.email)) {
      setError('Email inválido');
      return false;
    }
    if (!servicioSeleccionado) {
      setError('Selecciona el servicio');
      return false;
    }
    if (!industriaSeleccionada) {
      setError('Selecciona la industria');
      return false;
    }
    if (!contextoUsuario.trim() && archivos.length === 0) {
      setError('Proporciona información del proyecto');
      return false;
    }
    return true;
  };

  const generarPromptServicio = () => {
    const servicioNombre = servicios.find(s => s.id === servicioSeleccionado)?.nombre || servicioSeleccionado;
    const industriaNombre = industrias.find(i => i.id === industriaSeleccionada)?.nombre || industriaSeleccionada;
    
    const promptsEspecializados = {
      'electricidad': 'Ingeniero eléctrico experto. MED-01=áreas comunes, MED-02+=departamentos.',
      'itse': 'Especialista ITSE - Inspección Técnica de Seguridad. Para EDUCACIÓN (colegios), SALUD (hospitales, clínicas, centros médicos), INDUSTRIAL, COMERCIAL. Clasifica nivel riesgo (BAJO/MEDIO/ALTO/MUY ALTO). Incluye derechos municipales + servicio técnico. Visita técnica GRATUITA.',
      'puesta-tierra': 'Especialista PAT. Norma CNE, IEEE 80. Analiza resistividad, pozos, varillas. Certificado obligatorio.',
      'contra-incendios': 'Especialista CI. NFPA 13, 72. Rociadores, detectores, red húmeda. Incluye certificación.',
      'domotica': 'Especialista domótica. KNX, Zigbee, Z-Wave. Automatización integral.',
      'cctv': 'Especialista CCTV. Resolución, almacenamiento, cobertura, DVR/NVR.',
      'redes': 'Especialista redes. TIA/EIA 568. Cableado estructurado, certificación.',
      'camaras-inteligentes': 'Especialista cámaras IA. Facial, conteo, detección, analíticas.',
      'automatizacion-industrial': 'Ingeniero automatización MINERÍA e INDUSTRIAL. PLCs (Siemens, Allen Bradley), SCADA, HMI, sensores industriales, variadores, control de procesos. Sistemas robustos para ambientes extremos.',
      'digitalizacion': 'Especialista digitalización ADMINISTRATIVA. Escaneo masivo, OCR, gestión documental, archivo digital, backup, índice y clasificación. Reducción de espacio físico.',
      'multiple': 'Ingeniero multidisciplinario. Identifica todos los sistemas.'
    };

    return `${promptsEspecializados[servicioSeleccionado] || promptsEspecializados['multiple']}

SERVICIO: ${servicioNombre} | INDUSTRIA: ${industriaNombre}
INFO: ${contextoUsuario || 'Ver docs adjuntos'}
ARCHIVOS: ${archivos.length}

COMO ASESOR:
1. Analiza info/docs
2. Identifica componentes
3. Pregunta detalles técnicos
4. Sugiere mejoras
${servicioSeleccionado === 'itse' ? '\n5. Para ITSE: determina nivel de riesgo según tipo de negocio y área' : ''}

NO cotices aún. Solo asesora.`;
  };

  const convertirABase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result.split(",")[1]);
      reader.onerror = () => reject(new Error("Error al leer"));
      reader.readAsDataURL(file);
    });
  };

  const handleFileUpload = async (e, enChat = false) => {
    const files = Array.from(e.target.files);
    const TAMANO_MAX = 10 * 1024 * 1024;
    
    setError('');
    setAnalizando(true);
    
    try {
      const archivosConBase64 = [];
      
      for (const file of files) {
        if (file.size > TAMANO_MAX) {
          setError(`${file.name} excede 10MB`);
          continue;
        }
        
        let base64Data = null;
        let contenidoTexto = null;
        let tipoArchivo = file.type;
        
        if (file.type.includes('image')) {
          base64Data = await convertirABase64(file);
        } else if (file.type === 'application/pdf') {
          base64Data = await convertirABase64(file);
        } else if (file.type.includes('spreadsheet') || file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
          const XLSX = await import('https://cdn.sheetjs.com/xlsx-0.20.0/package/xlsx.mjs');
          const arrayBuffer = await file.arrayBuffer();
          const workbook = XLSX.read(arrayBuffer);
          
          let textoCompleto = `ARCHIVO EXCEL: ${file.name}\n\n`;
          workbook.SheetNames.forEach(sheetName => {
            textoCompleto += `\n╔══ HOJA: ${sheetName} ══╗\n`;
            const worksheet = workbook.Sheets[sheetName];
            const datos = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' });
            datos.forEach((fila, idx) => {
              textoCompleto += `Fila ${idx + 1}: ${fila.join(' | ')}\n`;
            });
          });
          
          contenidoTexto = textoCompleto;
          tipoArchivo = 'text/plain';
        } else if (file.type.includes('word') || file.name.endsWith('.docx') || file.name.endsWith('.doc')) {
          const mammoth = await import('https://cdn.jsdelivr.net/npm/mammoth@1.6.0/+esm');
          const arrayBuffer = await file.arrayBuffer();
          const result = await mammoth.extractRawText({ arrayBuffer });
          
          contenidoTexto = `ARCHIVO WORD: ${file.name}\n\n${result.value}`;
          tipoArchivo = 'text/plain';
        } else if (file.type === 'text/html' || file.name.endsWith('.html')) {
          const texto = await file.text();
          contenidoTexto = `ARCHIVO HTML: ${file.name}\n\n${texto}`;
          tipoArchivo = 'text/plain';
        } else if (file.type === 'application/json' || file.name.endsWith('.json')) {
          const texto = await file.text();
          const jsonData = JSON.parse(texto);
          contenidoTexto = `ARCHIVO JSON: ${file.name}\n\n${JSON.stringify(jsonData, null, 2)}`;
          tipoArchivo = 'text/plain';
        } else if (file.type.includes('text') || file.name.endsWith('.txt') || file.name.endsWith('.csv')) {
          contenidoTexto = `ARCHIVO: ${file.name}\n\n${await file.text()}`;
          tipoArchivo = 'text/plain';
        } else {
          try {
            contenidoTexto = `ARCHIVO: ${file.name}\n\n${await file.text()}`;
            tipoArchivo = 'text/plain';
          } catch {
            setError(`${file.name}: Tipo no soportado`);
            continue;
          }
        }
        
        archivosConBase64.push({
          nombre: file.name,
          tipo: tipoArchivo,
          base64: base64Data,
          contenidoTexto: contenidoTexto,
          tamano: (file.size / 1024).toFixed(2) + ' KB',
          extension: file.name.split('.').pop()?.toUpperCase() || 'Desconocido'
        });
      }
      
      if (archivosConBase64.length > 0) {
        setArchivos([...archivos, ...archivosConBase64]);
        
        if (enChat) {
          const mensajeArchivo = `🔎 ${archivosConBase64.length} archivo(s) procesado(s): ${archivosConBase64.map(a => `${a.nombre} (${a.extension})`).join(', ')}`;
          setConversacion([...conversacion, { tipo: 'sistema', mensaje: mensajeArchivo }]);
        }
        
        setExito(`✅ ${archivosConBase64.length} archivo(s) procesado(s) completamente`);
        setTimeout(() => setExito(''), 3000);
      }
    } catch (error) {
      setError('Error procesando archivo: ' + error.message);
    } finally {
      setAnalizando(false);
    }
  };

  const eliminarArchivo = (index) => {
    setArchivos(archivos.filter((_, i) => i !== index));
  };

  const iniciarAnalisis = async () => {
    setError('');
    if (!validarDatos()) return;

    setAnalizando(true);
    setPaso(2);

    const contentParts = [{ type: "text", text: generarPromptServicio() }];

    if (archivos.length > 0) {
      archivos.forEach(archivo => {
        if (archivo.base64) {
          if (archivo.tipo.includes('pdf')) {
            contentParts.push({ 
              type: "document", 
              source: { type: "base64", media_type: "application/pdf", data: archivo.base64 }
            });
          } else if (archivo.tipo.includes('image')) {
            contentParts.push({ 
              type: "image", 
              source: { type: "base64", media_type: archivo.tipo, data: archivo.base64 }
            });
          }
        }
      });
    }

    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 2000,
          messages: [{ role: "user", content: contentParts }]
        })
      });

      if (!response.ok) throw new Error(`Error API: ${response.status}`);

      const data = await response.json();
      setConversacion([{ tipo: 'ia', mensaje: data.content[0].text }]);
    } catch (error) {
      setError('Error: ' + error.message);
      setPaso(1);
    } finally {
      setAnalizando(false);
    }
  };

  const enviarMensaje = async () => {
    if (!inputChat.trim()) return;

    const nuevoMensaje = { tipo: 'usuario', mensaje: inputChat };
    setConversacion([...conversacion, nuevoMensaje]);
    setInputChat('');
    setAnalizando(true);
    setError('');

    const servicioActual = servicios.find(s => s.id === servicioSeleccionado)?.nombre || 'Servicio';
    const preciosServicio = basePreciosUniversal[servicioSeleccionado] || {};
    const preciosTexto = Object.entries(preciosServicio)
      .map(([item, precio]) => `- ${item}: S/ ${precio}`)
      .join('\n');

    const contentParts = [{
      type: "text",
      text: `CONVERSACIÓN PREVIA:
${conversacion.map(c => `${c.tipo.toUpperCase()}: ${c.mensaje}`).join('\n')}

NUEVO MENSAJE USUARIO: ${inputChat}

DATOS DEL PROYECTO:
- Servicio: ${servicioActual}
- Industria: ${industrias.find(i => i.id === industriaSeleccionada)?.nombre}
- Contexto: ${contextoUsuario}

PRECIOS BASE DISPONIBLES (Soles S/):
${preciosTexto}

╔═══════════════════════════════════════════════════════════════╗

INSTRUCCIONES IMPORTANTES:

${servicioSeleccionado === 'itse' ? `
🔴 ESPECIAL PARA ITSE:
- Clasifica el nivel de riesgo: BAJO/MEDIO/ALTO/MUY ALTO
- SIEMPRE incluye 2 conceptos separados:
  1. Derecho Municipal (lo que paga el cliente a la municipalidad)
  2. Servicio Técnico TESLA (nuestro servicio profesional)
- Incluye: Evaluación técnica + Planos + Gestión + Seguimiento
- La visita técnica es GRATUITA (precio 0)
- Tiempo estimado: 15-20 días hábiles
- Ejemplo estructura:
  * Derecho municipal ITSE [Nivel]: S/ XXX
  * Servicio técnico TESLA: S/ XXX
  * Total estimado: S/ XXX
` : ''}

1. Si el usuario pide "cotiza", "genera cotización" o similar:
   → Responde SOLO con el JSON (sin texto adicional, sin markdown)
   
2. Si el usuario hace preguntas o conversa:
   → Responde en texto normal

FORMATO JSON REQUERIDO (cuando cotices):
{
  "cliente": {
    "nombre": "Nombre cliente",
    "proyecto": "Nombre proyecto",
    "direccion": "Dirección",
    "pisos": 0,
    "departamentos": 0
  },
  "items": [
    {
      "capitulo": "INSTALACIONES ELÉCTRICAS",
      "categoria": "Materiales",
      "descripcion": "Descripción completa del ítem",
      "cantidad": 100.00,
      "unidad": "m",
      "precioUnitario": 5.50,
      "observacion": "Incluye materiales y mano de obra"
    }
  ],
  "resumen": "Resumen ejecutivo del proyecto y alcance",
  "recomendaciones": "Recomendaciones técnicas importantes"
}

REGLAS PARA LA COTIZACIÓN:
✓ Usa precios base proporcionados + margen 15-20%
✓ Agrupa por CAPÍTULOS (INSTALACIONES ELÉCTRICAS, PUESTA A TIERRA, etc)
✓ Incluye APU en observaciones
✓ Cantidades y precios deben ser números (no texto)
✓ Incluye mano de obra y materiales
✓ NO uses markdown (sin \`\`\`json)

¿Listo para cotizar o necesitas más información?`
    }];

    if (archivos.length > 0) {
      archivos.forEach(archivo => {
        if (archivo.tipo.includes('pdf')) {
          contentParts.push({ 
            type: "document", 
            source: { type: "base64", media_type: "application/pdf", data: archivo.base64 }
          });
        } else if (archivo.tipo.includes('image')) {
          contentParts.push({ 
            type: "image", 
            source: { type: "base64", media_type: archivo.tipo, data: archivo.base64 }
          });
        }
      });
    }

    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 4000,
          messages: [{ role: "user", content: contentParts }]
        })
      });

      if (!response.ok) throw new Error(`Error API: ${response.status}`);

      const data = await response.json();
      let respuestaIA = data.content[0].text;
      
      respuestaIA = respuestaIA.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
      
      if (respuestaIA.includes('{') && respuestaIA.includes('"items"')) {
        let jsonStr = '';
        try {
          const startIndex = respuestaIA.indexOf('{');
          const endIndex = respuestaIA.lastIndexOf('}');
          jsonStr = respuestaIA.substring(startIndex, endIndex + 1);
          
          const cotizacionData = JSON.parse(jsonStr);
          
          if (!cotizacionData.items || !Array.isArray(cotizacionData.items)) {
            throw new Error('Formato inválido: falta array items');
          }
          
          if (cotizacionData.items.length === 0) {
            throw new Error('Formato inválido: items vacío');
          }
          
          const itemValido = cotizacionData.items.every(item => 
            item.descripcion && 
            typeof item.cantidad === 'number' && 
            typeof item.precioUnitario === 'number'
          );
          
          if (!itemValido) {
            throw new Error('Formato inválido: items sin campos requeridos');
          }
          
          setCotizacion(cotizacionData);
          setPaso(3);
          setModoEdicion(true);
          setEstadoCotizacion('borrador');
          setVersionCotizacion(1.0);
          setResumenEditable(cotizacionData.resumen || '');
          setRecomendacionesEditables(cotizacionData.recomendaciones || '');
          setHistorialVersiones([{
            version: 1.0,
            fecha: new Date().toISOString(),
            estado: 'borrador',
            cotizacion: JSON.parse(JSON.stringify(cotizacionData))
          }]);
          setExito('✅ Cotización v1.0 generada correctamente');
          
        } catch (errorParsing) {
          console.error('Error parseando JSON:', errorParsing);
          console.log('Respuesta IA completa:', respuestaIA);
          console.log('JSON extraído:', jsonStr);
          
          setConversacion(prev => [...prev, { 
            tipo: 'ia', 
            mensaje: respuestaIA,
            debug: {
              error: errorParsing.message,
              jsonExtraido: jsonStr,
              respuestaCompleta: respuestaIA
            }
          }]);
          
          setError('⚠️ No pude generar la cotización aún. Proporciona más detalles o pídeme que cotice cuando esté listo.');
        }
      } else {
        setConversacion(prev => [...prev, { tipo: 'ia', mensaje: respuestaIA }]);
      }
    } catch (error) {
      setError('Error: ' + error.message);
      setConversacion(prev => [...prev, { tipo: 'sistema', mensaje: 'Error de conexión.' }]);
    } finally {
      setAnalizando(false);
    }
  };

  const volverARevisar = () => {
    setPaso(2);
    setConversacion([...conversacion, { 
      tipo: 'sistema', 
      mensaje: `📄 Modo revisión v${versionCotizacion} activado.

🔍 CÓMO SOLICITAR CAMBIOS:

Para CONDICIONES COMERCIALES:
• "Cambia la forma de pago a 40% anticipo, 60% a 30 días"
• "Actualiza la validez a 30 días calendario"
• "Cambia la garantía a 12 meses"
• "Los precios deben incluir IGV"

Para ITEMS:
• "Agrega 5 reflectores LED de 100W"
• "Quita el último item de cables"
• "Cambia la cantidad del primer item a 50"
• "Aumenta el precio del tablero a S/ 3000"

Para INFORMACIÓN:
• "Cambia el nombre del cliente a [Nombre]"
• "Actualiza la dirección a [Dirección]"

Escribe tus cambios de forma clara y específica. ¡La IA entenderá!`
    }]);
    setExito('✅ Modo revisión activado - Indica los cambios que necesitas');
  };

  const crearNuevaVersion = async (cambiosSolicitados) => {
    setAnalizando(true);
    
    const nuevaVersion = (Math.round(versionCotizacion * 10) + 1) / 10;
    
    const contentParts = [{
      type: "text",
      text: `╔═══════════════════════════════════════════════════════════════════════════════╗
║              SISTEMA DE REVISIÓN Y ACTUALIZACIÓN - TESLA COTIZADOR           ║
║                         VERSIÓN ${versionCotizacion} → ${nuevaVersion}                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
📋 COTIZACIÓN ACTUAL (v${versionCotizacion}):
═══════════════════════════════════════════════════════════════════════════════
${JSON.stringify(cotizacion, null, 2)}

═══════════════════════════════════════════════════════════════════════════════
💼 CONDICIONES COMERCIALES ACTUALES:
═══════════════════════════════════════════════════════════════════════════════
${JSON.stringify(condicionesComerciales, null, 2)}

═══════════════════════════════════════════════════════════════════════════════
📄 CAMBIOS SOLICITADOS POR EL CLIENTE:
═══════════════════════════════════════════════════════════════════════════════
${cambiosSolicitados}

╔═══════════════════════════════════════════════════════════════════════════════╗
║                         INSTRUCCIONES CRÍTICAS                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🎯 TU TAREA:
Analizar los cambios solicitados y actualizar EXACTAMENTE lo que el cliente pide.

🔍 TIPOS DE CAMBIOS POSIBLES:

1️⃣ CAMBIOS EN CONDICIONES COMERCIALES:
   Palabras clave: "forma de pago", "anticipo", "validez", "garantía", "IGV"
   → Actualizar el objeto "condicionesComerciales" con los nuevos valores
   → Ejemplo: "40% anticipo, 60% a 30 días" → forma_pago: "40% anticipo, 60% a 30 días"

2️⃣ CAMBIOS EN ITEMS:
   Palabras clave: "agregar", "quitar", "cambiar precio", "modificar cantidad"
   → Actualizar el array "items" según lo solicitado

3️⃣ CAMBIOS EN INFORMACIÓN CLIENTE:
   → Actualizar objeto "cliente"

4️⃣ CAMBIOS EN RESUMEN/RECOMENDACIONES:
   → Actualizar campos correspondientes

╔═══════════════════════════════════════════════════════════════════════════════╗
║                    FORMATO DE RESPUESTA REQUERIDO                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Responde SOLO con un JSON válido (sin markdown, sin \`\`\`json).
El JSON DEBE contener TODOS los campos, incluso los que NO cambian:

{
  "cliente": { ...objeto cliente completo... },
  "items": [ ...array items completo... ],
  "resumen": "...",
  "recomendaciones": "...",
  "condicionesComerciales": {
    "incluye_igv": "...",
    "forma_pago": "...",
    "validez": "...",
    "garantia": "...",
    "otra": "..."
  }
}

⚠️ REGLAS ESTRICTAS:
✅ Incluir TODO el JSON completo (no solo lo que cambió)
✅ Si el cliente pide cambiar condiciones comerciales, DEBES actualizarlas
✅ Mantener valores que NO se solicitaron cambiar
✅ Validar que todos los campos estén presentes
✅ NO usar markdown ni código
✅ Solo JSON puro

🔍 VALIDACIÓN ANTES DE RESPONDER:
□ ¿Leí correctamente lo que el cliente pidió cambiar?
□ ¿Actualicé EXACTAMENTE esos campos?
□ ¿El JSON incluye TODOS los campos obligatorios?
□ ¿Las condiciones comerciales están actualizadas si se solicitó?
□ ¿El JSON es válido y parseable?

GENERA LA NUEVA VERSIÓN v${nuevaVersion} AHORA:`
    }];

    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 4000,
          messages: [{ role: "user", content: contentParts }]
        })
      });

      if (!response.ok) throw new Error(`Error API: ${response.status}`);

      const data = await response.json();
      let respuestaIA = data.content[0].text;
      
      respuestaIA = respuestaIA.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
      
      if (respuestaIA.includes('{') && respuestaIA.includes('"items"')) {
        let jsonStr = '';
        try {
          const startIndex = respuestaIA.indexOf('{');
          const endIndex = respuestaIA.lastIndexOf('}');
          jsonStr = respuestaIA.substring(startIndex, endIndex + 1);
          
          const nuevaCotizacion = JSON.parse(jsonStr);
          
          if (!nuevaCotizacion.items || !Array.isArray(nuevaCotizacion.items) || nuevaCotizacion.items.length === 0) {
            throw new Error('Formato inválido en nueva versión');
          }
          
          if (nuevaCotizacion.condicionesComerciales) {
            setCondicionesComerciales(nuevaCotizacion.condicionesComerciales);
          }
          
          setCotizacion(nuevaCotizacion);
          setVersionCotizacion(nuevaVersion);
          setHistorialVersiones([...historialVersiones, {
            version: nuevaVersion,
            fecha: new Date().toISOString(),
            estado: 'borrador',
            cotizacion: JSON.parse(JSON.stringify(nuevaCotizacion))
          }]);
          
          setConversacion([...conversacion, 
            { tipo: 'usuario', mensaje: cambiosSolicitados },
            { tipo: 'sistema', mensaje: `✅ Versión ${nuevaVersion} generada correctamente` }
          ]);
          
          setPaso(3);
          setExito(`v${nuevaVersion} creada exitosamente`);
        } catch (errorParsing) {
          console.error('Error parseando nueva versión:', errorParsing);
          console.log('JSON extraído:', jsonStr);
          
          setConversacion([...conversacion, 
            { tipo: 'usuario', mensaje: cambiosSolicitados },
            { tipo: 'ia', mensaje: respuestaIA }
          ]);
          
          setError('⚠️ No pude actualizar la versión. Intenta ser más específico con los cambios.');
        }
      } else {
        setConversacion([...conversacion, 
          { tipo: 'usuario', mensaje: cambiosSolicitados },
          { tipo: 'ia', mensaje: respuestaIA }
        ]);
        setError('La IA no generó una nueva versión. Intenta reformular tu solicitud.');
      }
    } catch (error) {
      setError('Error: ' + error.message);
    } finally {
      setAnalizando(false);
    }
  };

  const manejarMensajeRevision = async () => {
    if (!inputChat.trim()) return;
    await crearNuevaVersion(inputChat);
    setInputChat('');
  };

  const actualizarItem = (index, campo, valor) => {
    const nuevosItems = [...cotizacion.items];
    
    if (campo === 'cantidad' || campo === 'precioUnitario') {
      const numero = parseFloat(valor);
      if (isNaN(numero) || numero < 0) return;
      nuevosItems[index][campo] = numero;
    } else {
      nuevosItems[index][campo] = valor;
    }
    
    setCotizacion({ ...cotizacion, items: nuevosItems });
  };

  const calcularTotales = () => {
    if (!cotizacion?.items) return { subtotal: 0, igv: 0, total: 0 };
    const subtotal = cotizacion.items.reduce((sum, item) => {
      const cantidad = parseFloat(item.cantidad) || 0;
      const precio = parseFloat(item.precioUnitario) || 0;
      return sum + (cantidad * precio);
    }, 0);
    
    return {
      subtotal: subtotal.toFixed(2),
      igv: (subtotal * 0.18).toFixed(2),
      total: (subtotal * 1.18).toFixed(2)
    };
  };

  const descargarHTML = () => {
    try {
      const elemento = document.getElementById('cotizacion-pdf');
      if (!elemento) {
        setError('No se encuentra cotización');
        return;
      }
      
      const clone = elemento.cloneNode(true);
      
      if (ocultarPreciosUnitarios) {
        const headers = clone.querySelectorAll('th');
        headers.forEach(th => {
          if (th.textContent.includes('P.U.')) {
            th.remove();
          }
        });
        
        const tables = clone.querySelectorAll('table');
        tables.forEach(table => {
          const rows = table.querySelectorAll('tbody tr');
          rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length === 5) {
              cells[3].remove();
            }
          });
        });
      }
      
      const html = clone.innerHTML;
      const htmlCompleto = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Cotización TESLA v${versionCotizacion}</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 900px; margin: 20px auto; padding: 20px; }
    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #8B0000; color: #D4AF37; }
    .bg-gray-50 { background-color: #f9fafb; }
    .bg-gray-200 { background-color: #e5e7eb; }
  </style>
</head>
<body>${html}</body>
</html>`;

      const blob = new Blob([htmlCompleto], { type: 'text/html;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const nombreArchivo = ocultarPreciosUnitarios ? 
        `TESLA_Cotizacion_SinPU_v${versionCotizacion}_${new Date().toISOString().slice(0,10)}.html` :
        `TESLA_Cotizacion_v${versionCotizacion}_${new Date().toISOString().slice(0,10)}.html`;
      a.download = nombreArchivo;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      setExito(`HTML descargado ${ocultarPreciosUnitarios ? '(sin P.U.)' : ''}`);
      setTimeout(() => setExito(''), 3000);
    } catch (error) {
      setError('Error: ' + error.message);
    }
  };

  const descargarPDFNativo = async () => {
    try {
      setAnalizando(true);
      setExito('⏳ Cargando librería PDF... Espera 3 segundos');
      
      console.log('🔍 Iniciando descarga PDF...');
      
      // Intentar cargar jsPDF
      let jsPDF;
      try {
        const module = await import('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
        jsPDF = module.jsPDF;
        console.log('✅ jsPDF cargado');
      } catch (e) {
        console.error('❌ Error cargando jsPDF:', e);
        throw new Error('No se pudo cargar la librería PDF. Usa "Vista Previa" y luego "Ctrl+P" para imprimir a PDF desde el navegador.');
      }
      
      // Intentar cargar autoTable
      try {
        await import('https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.31/jspdf.plugin.autotable.min.js');
        console.log('✅ autoTable cargado');
      } catch (e) {
        console.error('❌ Error cargando autoTable:', e);
        throw new Error('No se pudo cargar la librería de tablas PDF.');
      }

      setExito('📄 Generando PDF...');

      const doc = new jsPDF();
      const pageWidth = doc.internal.pageSize.getWidth();
      const pageHeight = doc.internal.pageSize.getHeight();
      let yPos = 20;

      // LOGO
      if (logoBase64) {
        try {
          console.log('🖼️ Agregando logo...');
          // Limpiar el base64 si tiene el prefijo data:
          const base64Clean = logoBase64.includes(',') ? logoBase64.split(',')[1] : logoBase64;
          const imageType = logoBase64.includes('png') ? 'PNG' : 'JPEG';
          doc.addImage(logoBase64, imageType, pageWidth - 45, 10, 35, 35);
          console.log('✅ Logo agregado');
        } catch (e) {
          console.warn('⚠️ No se pudo agregar logo:', e);
        }
      }

      // HEADER
      doc.setFillColor(139, 0, 0);
      doc.rect(0, 0, pageWidth, 50, 'F');
      
      doc.setTextColor(212, 175, 55);
      doc.setFontSize(18);
      doc.setFont('helvetica', 'bold');
      doc.text(datosEmpresa.nombre, 14, 20);
      
      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      doc.text(`RUC: ${datosEmpresa.ruc}`, 14, 28);
      doc.text(datosEmpresa.direccion, 14, 33);
      doc.text(datosEmpresa.ciudad, 14, 38);

      // COTIZACIÓN BOX
      doc.setFillColor(212, 175, 55);
      doc.rect(pageWidth - 55, 15, 45, 20, 'F');
      doc.setTextColor(139, 0, 0);
      doc.setFontSize(10);
      doc.setFont('helvetica', 'bold');
      doc.text('COTIZACION', pageWidth - 52, 23);
      doc.setFontSize(16);
      doc.text(`v${versionCotizacion}`, pageWidth - 52, 31);

      yPos = 58;

      // FECHA
      doc.setTextColor(80, 80, 80);
      doc.setFontSize(9);
      doc.text(`Fecha: ${new Date().toLocaleDateString('es-PE')}`, pageWidth - 50, yPos);
      yPos += 10;

      // INFO CLIENTE
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(11);
      doc.setFont('helvetica', 'bold');
      doc.text('INFORMACION DEL CLIENTE', 14, yPos);
      yPos += 6;

      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      doc.text(`Cliente: ${cotizacion.cliente?.nombre || 'N/A'}`, 14, yPos);
      yPos += 5;
      doc.text(`Proyecto: ${cotizacion.cliente?.proyecto || 'N/A'}`, 14, yPos);
      yPos += 5;
      doc.text(`Direccion: ${cotizacion.cliente?.direccion || 'N/A'}`, 14, yPos);
      yPos += 10;

      // TABLA
      const headers = [['DESCRIPCION', 'CANT.', 'UND.']];
      if (!ocultarPreciosUnitarios) headers[0].push('P.U. (S/)');
      if (!ocultarTotalesPorItem) headers[0].push('TOTAL (S/)');

      const rows = [];
      let currentCapitulo = '';

      cotizacion.items.forEach(item => {
        const cap = item.capitulo || item.categoria || 'Sin clasificar';
        
        if (cap !== currentCapitulo) {
          currentCapitulo = cap;
          const capRow = [{ content: cap.toUpperCase(), colSpan: headers[0].length, styles: { fillColor: [139, 0, 0], textColor: [212, 175, 55], fontStyle: 'bold' } }];
          rows.push(capRow);
        }

        const row = [
          item.descripcion + (item.observacion ? `\n${item.observacion}` : ''),
          item.cantidad.toString(),
          item.unidad
        ];

        if (!ocultarPreciosUnitarios) {
          row.push(`S/ ${parseFloat(item.precioUnitario).toFixed(2)}`);
        }

        if (!ocultarTotalesPorItem) {
          const total = (parseFloat(item.cantidad) * parseFloat(item.precioUnitario)).toFixed(2);
          row.push(`S/ ${total}`);
        }

        rows.push(row);
      });

      console.log('📊 Generando tabla...');
      doc.autoTable({
        startY: yPos,
        head: headers,
        body: rows,
        theme: 'grid',
        headStyles: {
          fillColor: [200, 200, 200],
          textColor: [0, 0, 0],
          fontStyle: 'bold',
          fontSize: 9
        },
        bodyStyles: {
          fontSize: 8,
          cellPadding: 3
        },
        alternateRowStyles: {
          fillColor: [249, 250, 251]
        },
        columnStyles: {
          0: { cellWidth: 'auto' },
          1: { cellWidth: 20, halign: 'center' },
          2: { cellWidth: 20, halign: 'center' }
        },
        didDrawPage: (data) => {
          doc.setFontSize(8);
          doc.setTextColor(100);
          doc.text(datosEmpresa.nombre, 14, pageHeight - 10);
          doc.text(`${datosEmpresa.telefono} | ${datosEmpresa.email}`, 14, pageHeight - 6);
        }
      });

      yPos = doc.lastAutoTable.finalY + 10;

      // TOTALES
      if (yPos > pageHeight - 60) {
        doc.addPage();
        yPos = 20;
      }

      const totales = calcularTotales();
      const xTotales = pageWidth - 70;

      if (modoVisualizacionIGV !== 'ocultar-igv') {
        doc.setFontSize(10);
        doc.text('Subtotal:', xTotales, yPos);
        doc.text(`S/ ${totales.subtotal}`, xTotales + 35, yPos, { align: 'right' });
        yPos += 7;

        if (modoVisualizacionIGV === 'sin-igv') {
          doc.text('IGV (18%):', xTotales, yPos);
          doc.text(`S/ ${totales.igv}`, xTotales + 35, yPos, { align: 'right' });
          yPos += 7;
        }
      }

      // TOTAL FINAL
      doc.setFillColor(139, 0, 0);
      doc.rect(xTotales - 5, yPos - 5, 65, 12, 'F');
      doc.setTextColor(212, 175, 55);
      doc.setFontSize(14);
      doc.setFont('helvetica', 'bold');
      doc.text('TOTAL:', xTotales, yPos + 3);
      doc.text(`S/ ${totales.total}`, xTotales + 35, yPos + 3, { align: 'right' });

      console.log('💾 Guardando PDF...');
      const nombrePDF = `TESLA_Cotizacion_v${versionCotizacion}_${new Date().toISOString().slice(0,10)}.pdf`;
      doc.save(nombrePDF);

      setExito(`✅ PDF descargado: ${nombrePDF}`);
      console.log('✅ PDF generado exitosamente');
      
    } catch (error) {
      console.error('❌ Error completo:', error);
      setError(`Error: ${error.message}. Usa "Vista Previa" y luego Ctrl+P para imprimir a PDF.`);
    } finally {
      setAnalizando(false);
    }
  };

  const descargarDOCX = async () => {
    try {
      setAnalizando(true);
      
      const { Document, Packer, Paragraph, Table, TableCell, TableRow, WidthType, AlignmentType, TextRun } = await import('https://cdn.jsdelivr.net/npm/docx@8.5.0/+esm');

      const children = [];

      children.push(
        new Paragraph({
          text: datosEmpresa.nombre,
          heading: 'Heading1',
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 }
        }),
        new Paragraph({
          children: [
            new TextRun({ text: `RUC: ${datosEmpresa.ruc}`, size: 20 })
          ],
          alignment: AlignmentType.CENTER
        }),
        new Paragraph({
          children: [
            new TextRun({ text: datosEmpresa.direccion, size: 18 })
          ],
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 }
        }),
        new Paragraph({
          children: [
            new TextRun({ text: `COTIZACIÓN v${versionCotizacion}`, bold: true, size: 28 })
          ],
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 }
        })
      );

      children.push(
        new Paragraph({
          children: [
            new TextRun({ text: 'INFORMACIÓN DEL CLIENTE', bold: true, size: 24 })
          ],
          spacing: { before: 200, after: 200 }
        }),
        new Paragraph({
          children: [
            new TextRun({ text: `Cliente: ${cotizacion.cliente?.nombre || 'N/A'}`, size: 20 })
          ]
        }),
        new Paragraph({
          children: [
            new TextRun({ text: `Proyecto: ${cotizacion.cliente?.proyecto || 'N/A'}`, size: 20 })
          ]
        }),
        new Paragraph({
          children: [
            new TextRun({ text: `Dirección: ${cotizacion.cliente?.direccion || 'N/A'}`, size: 20 })
          ],
          spacing: { after: 400 }
        })
      );

      const itemsPorCapitulo = cotizacion?.items?.reduce((acc, item) => {
        const cap = item.capitulo || item.categoria || 'Sin clasificar';
        if (!acc[cap]) acc[cap] = [];
        acc[cap].push(item);
        return acc;
      }, {}) || {};

      Object.keys(itemsPorCapitulo).forEach(capitulo => {
        children.push(
          new Paragraph({
            children: [
              new TextRun({ text: capitulo.toUpperCase(), bold: true, size: 22 })
            ],
            spacing: { before: 300, after: 200 }
          })
        );

        const tableRows = [
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: 'DESCRIPCIÓN', bold: true })], width: { size: 40, type: WidthType.PERCENTAGE } }),
              new TableCell({ children: [new Paragraph({ text: 'CANT.', bold: true })], width: { size: 15, type: WidthType.PERCENTAGE } }),
              new TableCell({ children: [new Paragraph({ text: 'UND.', bold: true })], width: { size: 15, type: WidthType.PERCENTAGE } }),
              ...(ocultarPreciosUnitarios ? [] : [new TableCell({ children: [new Paragraph({ text: 'P.U.', bold: true })], width: { size: 15, type: WidthType.PERCENTAGE } })]),
              ...(ocultarTotalesPorItem ? [] : [new TableCell({ children: [new Paragraph({ text: 'TOTAL', bold: true })], width: { size: 15, type: WidthType.PERCENTAGE } })])
            ]
          })
        ];

        itemsPorCapitulo[capitulo].forEach(item => {
          const cells = [
            new TableCell({ children: [new Paragraph(item.descripcion)] }),
            new TableCell({ children: [new Paragraph(item.cantidad.toString())] }),
            new TableCell({ children: [new Paragraph(item.unidad)] })
          ];

          if (!ocultarPreciosUnitarios) {
            cells.push(new TableCell({ children: [new Paragraph(`S/ ${parseFloat(item.precioUnitario).toFixed(2)}`)] }));
          }

          if (!ocultarTotalesPorItem) {
            const total = (parseFloat(item.cantidad) * parseFloat(item.precioUnitario)).toFixed(2);
            cells.push(new TableCell({ children: [new Paragraph(`S/ ${total}`)] }));
          }

          tableRows.push(new TableRow({ children: cells }));
        });

        children.push(
          new Table({
            rows: tableRows,
            width: { size: 100, type: WidthType.PERCENTAGE }
          })
        );
      });

      const totales = calcularTotales();
      children.push(
        new Paragraph({
          children: [
            new TextRun({ text: `\nSubtotal: S/ ${totales.subtotal}`, size: 24 })
          ],
          spacing: { before: 400 }
        }),
        new Paragraph({
          children: [
            new TextRun({ text: `IGV (18%): S/ ${totales.igv}`, size: 24 })
          ]
        }),
        new Paragraph({
          children: [
            new TextRun({ text: `TOTAL: S/ ${totales.total}`, bold: true, size: 28 })
          ],
          spacing: { after: 400 }
        })
      );

      children.push(
        new Paragraph({
          children: [
            new TextRun({ text: `\n${datosEmpresa.nombre}`, size: 18 }),
            new TextRun({ text: `\n📱 ${datosEmpresa.telefono} | 📧 ${datosEmpresa.email}`, size: 16 })
          ],
          alignment: AlignmentType.CENTER
        })
      );

      const doc = new Document({
        sections: [{
          properties: {},
          children: children
        }]
      });

      const blob = await Packer.toBlob(doc);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `TESLA_Cotizacion_v${versionCotizacion}_${new Date().toISOString().slice(0,10)}.docx`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      setExito('✅ DOCX editable descargado - Abre en Word y agrega tu logo manualmente');
      setTimeout(() => setExito(''), 4000);
    } catch (error) {
      setError('Error generando DOCX: ' + error.message);
      console.error(error);
    } finally {
      setAnalizando(false);
    }
  };

  const totales = calcularTotales();
  
  const itemsPorCapitulo = cotizacion?.items?.reduce((acc, item) => {
    const cap = item.capitulo || item.categoria || 'Sin clasificar';
    if (!acc[cap]) acc[cap] = [];
    acc[cap].push(item);
    return acc;
  }, {}) || {};

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6">
      <div className="max-w-7xl mx-auto">
        <button onClick={volverAlInicio}
          className="fixed top-6 right-6 z-50 bg-gradient-to-r from-red-900 to-red-800 hover:from-red-800 hover:to-red-700 text-yellow-400 px-4 py-2 rounded-lg font-semibold flex items-center gap-2 shadow-2xl border-2 border-yellow-600 backdrop-blur-md transition-all duration-300 hover:scale-105">
          <Home className="w-5 h-5" />
          Inicio
        </button>

        <div className="bg-gradient-to-r from-red-950 via-red-900 to-black rounded-2xl p-8 mb-6 border-2 border-yellow-600 shadow-2xl backdrop-blur-md bg-opacity-90 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-yellow-600/10 via-transparent to-yellow-600/10 animate-pulse"></div>
          <div className="relative z-10">
            <h1 className="text-4xl font-bold flex items-center gap-3 text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-yellow-300 to-yellow-500">
              <Zap className="w-10 h-10 text-yellow-400 animate-pulse" />
              TESLA ELECTRICIDAD Y AUTOMATIZACIÓN
            </h1>
            <p className="text-yellow-400 mt-2 font-semibold">Sistema Profesional Elite - Clase Mundial</p>
            <div className="flex items-center gap-4 mt-3 text-sm">
              <span className="text-gray-300">📱 WhatsApp: {datosEmpresa.telefono}</span>
              <span className="text-gray-300">📧 {datosEmpresa.email}</span>
            </div>
            {cotizacion && (
              <div className="mt-4 flex items-center gap-4 text-sm">
                <span className="bg-yellow-600 px-3 py-1 rounded-full font-bold">v{versionCotizacion}</span>
                <span className={`px-3 py-1 rounded-full ${
                  estadoCotizacion === 'borrador' ? 'bg-blue-900' :
                  estadoCotizacion === 'revision' ? 'bg-orange-900' :
                  'bg-green-900'
                }`}>
                  {estadoCotizacion === 'borrador' ? '📝 Borrador' :
                   estadoCotizacion === 'revision' ? '🔄 Revisión' :
                   '✅ Aprobado'}
                </span>
              </div>
            )}
          </div>
        </div>

        {error && <Alerta tipo="error" mensaje={error} onClose={() => setError('')} />}
        {exito && <Alerta tipo="exito" mensaje={exito} onClose={() => setExito('')} />}

        {paso === 1 && (
          <div className="space-y-6">
            <div className="bg-gradient-to-br from-purple-900 to-purple-800 rounded-2xl p-6 border-2 border-purple-500 shadow-xl backdrop-blur-md bg-opacity-90">
              <h2 className="text-2xl font-bold mb-4 text-purple-200 flex items-center gap-2">
                🎨 Logo Empresa (Opcional)
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
                    className="w-full bg-gradient-to-r from-purple-700 to-purple-600 hover:from-purple-600 hover:to-purple-500 text-white px-6 py-3 rounded-xl font-semibold flex items-center justify-center gap-2 shadow-xl border-2 border-purple-400 transition-all duration-300 hover:scale-105">
                    <Upload className="w-5 h-5" />
                    {logoBase64 ? 'Cambiar Logo' : 'Subir Logo'}
                  </button>
                  <p className="text-xs text-purple-200 mt-2 text-center">
                    PNG, JPG, WebP - Máx 2MB • Aparecerá en PDF nativo
                  </p>
                </div>
                
                {logoBase64 && (
                  <div className="bg-white rounded-xl p-3 border-2 border-purple-400 shadow-lg">
                    <img 
                      src={logoBase64} 
                      alt="Logo" 
                      className="w-24 h-24 object-contain"
                    />
                    <p className="text-xs text-gray-600 mt-2 text-center font-semibold">✅ Cargado</p>
                  </div>
                )}
              </div>
              
              {!logoBase64 && (
                <div className="mt-4 p-3 bg-purple-950 bg-opacity-50 rounded-lg border border-purple-700">
                  <p className="text-sm text-purple-200">
                    💡 <strong>Tip:</strong> Si tu logo pesa más de 2MB, comprímelo en{' '}
                    <a href="https://tinypng.com" target="_blank" rel="noopener noreferrer" className="text-yellow-300 hover:text-yellow-200 underline">
                      TinyPNG.com
                    </a>
                  </p>
                </div>
              )}
            </div>

            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-700 shadow-xl backdrop-blur-md bg-opacity-90">
              <h2 className="text-2xl font-bold mb-4 text-yellow-400">1. Tipo de Servicio</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {servicios.map(servicio => (
                  <button
                    key={servicio.id}
                    onClick={() => setServicioSeleccionado(servicio.id)}
                    className={`p-4 rounded-xl border-2 transition-all duration-300 text-left ${
                      servicioSeleccionado === servicio.id
                        ? 'border-yellow-500 bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl scale-105'
                        : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800'
                    }`}>
                    <div className="text-2xl mb-2">{servicio.icon}</div>
                    <div className="text-sm font-semibold">{servicio.nombre.split(' ').slice(1).join(' ')}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-700 shadow-xl backdrop-blur-md bg-opacity-90">
              <h2 className="text-2xl font-bold mb-4 text-yellow-400">2. Industria</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {industrias.map(industria => (
                  <button
                    key={industria.id}
                    onClick={() => setIndustriaSeleccionada(industria.id)}
                    className={`p-3 rounded-xl border-2 transition-all duration-300 ${
                      industriaSeleccionada === industria.id
                        ? 'border-yellow-500 bg-gradient-to-br from-red-900 to-red-800 text-white shadow-xl'
                        : 'border-gray-700 bg-gray-900 hover:border-yellow-600 hover:bg-gray-800'
                    }`}>
                    <div className="text-sm font-semibold">{industria.nombre}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-700 shadow-xl backdrop-blur-md bg-opacity-90">
              <h2 className="text-2xl font-bold mb-4 text-yellow-400">3. Información Proyecto</h2>
              
              {servicioSeleccionado && basePreciosUniversal[servicioSeleccionado] && (
                <div className="mb-4 p-4 bg-blue-950 bg-opacity-50 border border-blue-700 rounded-xl backdrop-blur-sm">
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
              
              <textarea value={contextoUsuario} onChange={(e) => setContextoUsuario(e.target.value)}
                className="w-full h-32 px-4 py-3 bg-gray-950 border border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none resize-none mb-4 text-white placeholder-gray-500"
                placeholder="Describe tu proyecto..." />

              <div className="border-t-2 border-gray-800 pt-4">
                <h3 className="text-lg font-semibold mb-3 text-gray-300">Documentos Opcionales</h3>
                <div className="border-2 border-dashed border-gray-700 rounded-xl p-6 text-center hover:border-yellow-600 transition-all cursor-pointer mb-4 bg-gray-950 bg-opacity-50">
                  <input type="file" multiple onChange={handleFileUpload} className="hidden" id="fileInput" accept=".pdf,.png,.jpg,.jpeg,.gif,.webp,.xlsx,.xls,.docx,.doc,.html,.json,.txt,.csv" />
                  <label htmlFor="fileInput" className="cursor-pointer">
                    <Upload className="w-12 h-12 mx-auto mb-3 text-yellow-500" />
                    <p className="text-sm text-gray-400 font-semibold">Sube documentos (máx 10MB)</p>
                    <p className="text-xs text-gray-500 mt-2">Formatos: PDF, Excel, Word, imágenes, JSON, TXT, CSV</p>
                  </label>
                </div>

                {archivos.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-sm font-semibold text-yellow-400 mb-2">📁 Archivos procesados:</p>
                    {archivos.map((archivo, index) => (
                      <div key={index} className="flex items-center justify-between bg-gray-950 bg-opacity-70 p-3 rounded-xl border border-gray-800 hover:border-yellow-600 transition-all">
                        <div className="flex items-center gap-2 flex-1">
                          <FileText className="w-5 h-5 text-yellow-500" />
                          <div className="flex-1">
                            <div className="flex items-center gap-2">
                              <span className="text-sm font-semibold">{archivo.nombre}</span>
                              <span className="text-xs bg-blue-900 text-blue-300 px-2 py-0.5 rounded">{archivo.extension}</span>
                            </div>
                            <div className="flex items-center gap-3 mt-1">
                              <span className="text-xs text-gray-400">{archivo.tamano}</span>
                              {archivo.contenidoTexto && (
                                <span className="text-xs text-green-400 font-semibold flex items-center gap-1">
                                  <CheckCircle className="w-3 h-3" />
                                  Procesado completamente
                                </span>
                              )}
                              {archivo.base64 && !archivo.contenidoTexto && (
                                <span className="text-xs text-blue-400 font-semibold flex items-center gap-1">
                                  <CheckCircle className="w-3 h-3" />
                                  Imagen/PDF cargado
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                        <button onClick={() => eliminarArchivo(index)} className="text-red-400 hover:text-red-300 ml-2">
                          <X className="w-5 h-5" />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div className="flex gap-3">
              <button onClick={iniciarAnalisis} disabled={analizando}
                className="flex-1 bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 disabled:from-gray-800 disabled:to-gray-700 disabled:cursor-not-allowed py-4 rounded-xl font-bold text-lg text-black shadow-2xl border-2 border-yellow-400 transition-all duration-300 hover:scale-105">
                {analizando ? 'Analizando...' : 'Comenzar Cotización'}
              </button>
              
              <input ref={fileInputLoadRef} type="file" onChange={cargarCotizacion} className="hidden" accept=".json" />
              <button onClick={() => fileInputLoadRef.current?.click()}
                className="bg-gradient-to-r from-blue-900 to-blue-800 hover:from-blue-800 hover:to-blue-700 px-6 py-4 rounded-xl font-bold flex items-center gap-2 shadow-xl border-2 border-blue-600 transition-all duration-300">
                <FolderOpen className="w-5 h-5" />
                Cargar
              </button>
            </div>
          </div>
        )}

        {paso === 2 && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-700 shadow-xl backdrop-blur-md bg-opacity-90">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-yellow-400">Chat Profesional</h2>
                <button 
                  onClick={() => setDebugMode(!debugMode)}
                  className={`px-3 py-1 rounded text-xs ${debugMode ? 'bg-green-600' : 'bg-gray-700'} hover:bg-green-700 transition-colors`}
                  title="Modo debug: ver respuestas completas de la IA">
                  {debugMode ? '🐛 Debug ON' : '🐛 Debug'}
                </button>
              </div>
              
              <div className="space-y-4 mb-4 h-96 overflow-y-auto">
                {conversacion.map((msg, index) => (
                  <div key={index} className={`flex ${msg.tipo === 'ia' ? 'justify-start' : 'justify-end'}`}>
                    <div className={`max-w-xl ${
                      msg.tipo === 'ia' ? 'bg-gradient-to-br from-blue-900 to-blue-800 border-blue-600' : 
                      msg.tipo === 'usuario' ? 'bg-gradient-to-br from-yellow-800 to-yellow-700 border-yellow-500' : 
                      'bg-gradient-to-br from-gray-800 to-gray-700 border-gray-600'
                    } rounded-xl p-4 border-2 shadow-lg`}>
                      <p className="whitespace-pre-line">{msg.mensaje}</p>
                      {debugMode && msg.debug && (
                        <div className="mt-3 pt-3 border-t border-gray-600 text-xs">
                          <p className="text-red-300 font-bold">🐛 DEBUG INFO:</p>
                          <p className="text-gray-300 mt-1"><b>Error:</b> {msg.debug.error}</p>
                          {msg.debug.jsonExtraido && (
                            <details className="mt-2">
                              <summary className="cursor-pointer text-yellow-300 hover:text-yellow-200">Ver JSON extraído</summary>
                              <pre className="mt-2 p-2 bg-black rounded text-green-400 text-xs overflow-x-auto">{msg.debug.jsonExtraido}</pre>
                            </details>
                          )}
                          <details className="mt-2">
                            <summary className="cursor-pointer text-yellow-300 hover:text-yellow-200">Ver respuesta completa</summary>
                            <pre className="mt-2 p-2 bg-black rounded text-gray-300 text-xs overflow-x-auto">{msg.debug.respuestaCompleta}</pre>
                          </details>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                {analizando && (
                  <div className="flex justify-start">
                    <div className="bg-gradient-to-br from-blue-900 to-blue-800 rounded-xl p-4 border-2 border-blue-600">
                      <Loader className="w-6 h-6 animate-spin text-yellow-400" />
                    </div>
                  </div>
                )}
              </div>
              
              <div className="flex gap-2">
                <input type="text" value={inputChat} onChange={(e) => setInputChat(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !analizando && (cotizacion ? manejarMensajeRevision() : enviarMensaje())}
                  className="flex-1 px-4 py-3 bg-gray-950 border-2 border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none text-white"
                  placeholder={cotizacion ? "Indica cambios..." : "Escribe aquí..."}
                  disabled={analizando} />
                
                <input ref={fileInputChatRef} type="file" multiple onChange={(e) => handleFileUpload(e, true)}
                  className="hidden" accept=".pdf,.png,.jpg,.jpeg,.gif,.webp,.xlsx,.xls,.docx,.doc,.html,.json,.txt,.csv" />
                
                <button onClick={() => fileInputChatRef.current?.click()}
                  disabled={analizando}
                  className="bg-gray-800 hover:bg-gray-700 disabled:bg-gray-900 disabled:cursor-not-allowed px-4 py-3 rounded-xl transition-colors border-2 border-gray-700"
                  title="Adjuntar">
                  <Upload className="w-5 h-5 text-yellow-400" />
                </button>
                
                <button onClick={cotizacion ? manejarMensajeRevision : enviarMensaje}
                  disabled={!inputChat.trim() || analizando}
                  className="bg-gradient-to-r from-yellow-600 to-yellow-500 hover:from-yellow-500 hover:to-yellow-400 disabled:from-gray-800 disabled:to-gray-700 disabled:cursor-not-allowed px-6 py-3 rounded-xl transition-all border-2 border-yellow-400 shadow-xl">
                  <Send className="w-5 h-5 text-black" />
                </button>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-yellow-700 shadow-xl backdrop-blur-md bg-opacity-90">
              <h3 className="text-xl font-bold mb-3 text-yellow-400">Info Proyecto</h3>
              <div className="mb-3 p-3 bg-gray-950 bg-opacity-70 rounded-xl">
                <p className="text-sm text-gray-300">
                  <strong>Servicio:</strong> {servicios.find(s => s.id === servicioSeleccionado)?.nombre}<br/>
                  <strong>Industria:</strong> {industrias.find(i => i.id === industriaSeleccionada)?.nombre}<br/>
                  <strong>Archivos:</strong> {archivos.length}
                </p>
              </div>
              <textarea value={contextoUsuario} onChange={(e) => setContextoUsuario(e.target.value)}
                className="w-full h-64 px-4 py-3 bg-gray-950 border-2 border-yellow-700 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none resize-none text-sm text-white"
                placeholder="Más info..." />
            </div>
          </div>
        )}

        {paso === 3 && cotizacion && (
          <>
            <div className="no-print mb-6">
              <div className="bg-gradient-to-r from-yellow-900 to-yellow-800 border-2 border-yellow-500 rounded-2xl p-4 mb-4 backdrop-blur-md bg-opacity-90 shadow-2xl">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <h3 className="text-black font-bold text-lg">
                      {modoEdicion ? '✏️ MODO EDICIÓN' : '✅ VISTA FINAL'} v{versionCotizacion}
                    </h3>
                    <div className="flex gap-2">
                      {ocultarPreciosUnitarios && (
                        <span className="bg-purple-600 text-white text-xs px-3 py-1 rounded-full font-bold">
                          🚫 P.U. OCULTOS
                        </span>
                      )}
                      {ocultarTotalesPorItem && (
                        <span className="bg-indigo-600 text-white text-xs px-3 py-1 rounded-full font-bold animate-pulse">
                          💎 SOLO TOTAL FINAL
                        </span>
                      )}
                      {modoVisualizacionIGV === 'con-igv' && (
                        <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full font-bold">
                          💵 CON IGV
                        </span>
                      )}
                      {modoVisualizacionIGV === 'ocultar-igv' && (
                        <span className="bg-blue-800 text-white text-xs px-3 py-1 rounded-full font-bold">
                          🔒 IGV OCULTO
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2 flex-wrap">
                    <button onClick={guardarCotizacion}
                      className="px-4 py-2 bg-green-800 hover:bg-green-700 text-white rounded-xl font-semibold flex items-center gap-2 transition-all border-2 border-green-600 shadow-xl">
                      <Download className="w-5 h-5" /> Guardar
                    </button>
                    <button onClick={volverARevisar}
                      className="px-4 py-2 bg-orange-800 hover:bg-orange-700 text-white rounded-xl font-semibold flex items-center gap-2 transition-all border-2 border-orange-600 shadow-xl">
                      <RefreshCw className="w-5 h-5" /> Revisar
                    </button>
                    
                    <button onClick={() => {
                      setOcultarPreciosUnitarios(!ocultarPreciosUnitarios);
                      setExito(ocultarPreciosUnitarios ? 'Precios unitarios mostrados' : 'Precios unitarios ocultados');
                      setTimeout(() => setExito(''), 2000);
                    }}
                      className={`px-4 py-2 rounded-xl font-semibold flex items-center gap-2 transition-all border-2 shadow-xl ${
                        ocultarPreciosUnitarios ? 'bg-purple-800 hover:bg-purple-700 border-purple-600' : 'bg-gray-700 hover:bg-gray-600 border-gray-500'
                      } text-white`}
                      title={ocultarPreciosUnitarios ? 'Click para mostrar precios unitarios' : 'Click para ocultar precios unitarios'}>
                      {ocultarPreciosUnitarios ? <><Eye className="w-5 h-5" /> P.U.</> : <><EyeOff className="w-5 h-5" /> P.U.</>}
                    </button>
                    
                    <button onClick={() => {
                      setOcultarTotalesPorItem(!ocultarTotalesPorItem);
                      setExito(ocultarTotalesPorItem ? 'Totales por ítem mostrados' : 'Totales por ítem ocultados - Solo total final visible');
                      setTimeout(() => setExito(''), 2000);
                    }}
                      className={`px-4 py-2 rounded-xl font-semibold flex items-center gap-2 transition-all border-2 shadow-xl ${
                        ocultarTotalesPorItem ? 'bg-indigo-800 hover:bg-indigo-700 border-indigo-600' : 'bg-gray-700 hover:bg-gray-600 border-gray-500'
                      } text-white`}
                      title={ocultarTotalesPorItem ? 'Click para mostrar totales por ítem' : 'Click para ocultar totales por ítem'}>
                      {ocultarTotalesPorItem ? <><Eye className="w-5 h-5" /> Totales</> : <><EyeOff className="w-5 h-5" /> Totales</>}
                    </button>
                    
                    <div className="relative group">
                      <button className="px-4 py-2 bg-blue-800 hover:bg-blue-700 text-white rounded-xl font-semibold flex items-center gap-2 transition-all border-2 border-blue-600 shadow-xl">
                        💰 Vista IGV
                      </button>
                      <div className="absolute top-full mt-2 right-0 bg-gray-900 border-2 border-blue-600 rounded-xl shadow-2xl hidden group-hover:block z-50 min-w-64">
                        <div className="p-2">
                          <button 
                            onClick={() => {
                              setModoVisualizacionIGV('sin-igv');
                              setExito('Mostrando precios SIN IGV');
                              setTimeout(() => setExito(''), 2000);
                            }}
                            className={`w-full text-left px-4 py-2 rounded-lg mb-1 ${modoVisualizacionIGV === 'sin-igv' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-800'}`}>
                            📊 Precios SIN IGV (por defecto)
                          </button>
                          <button 
                            onClick={() => {
                              setModoVisualizacionIGV('con-igv');
                              setExito('Mostrando precios CON IGV incluido');
                              setTimeout(() => setExito(''), 2000);
                            }}
                            className={`w-full text-left px-4 py-2 rounded-lg mb-1 ${modoVisualizacionIGV === 'con-igv' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-800'}`}>
                            💵 Precios CON IGV incluido
                          </button>
                          <button 
                            onClick={() => {
                              setModoVisualizacionIGV('ocultar-igv');
                              setExito('IGV oculto - Solo total final');
                              setTimeout(() => setExito(''), 2000);
                            }}
                            className={`w-full text-left px-4 py-2 rounded-lg ${modoVisualizacionIGV === 'ocultar-igv' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-800'}`}>
                            🔒 Ocultar desglose IGV
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <button onClick={() => setModoEdicion(!modoEdicion)}
                      className={`px-4 py-2 rounded-xl font-semibold flex items-center gap-2 transition-all border-2 shadow-xl ${
                        modoEdicion ? 'bg-green-800 hover:bg-green-700 border-green-600' : 'bg-blue-800 hover:bg-blue-700 border-blue-600'
                      } text-white`}>
                      {modoEdicion ? <><Save className="w-5 h-5" /> Finalizar</> : <><Edit className="w-5 h-5" /> Editar</>}
                    </button>
                  </div>
                </div>
                
                {historialVersiones.length > 1 && (
                  <div className="mb-3 p-3 bg-blue-950 bg-opacity-70 rounded-xl">
                    <p className="text-sm text-blue-300 font-semibold mb-2">📊 Historial:</p>
                    <div className="flex gap-2 flex-wrap">
                      {historialVersiones.map((hist, idx) => (
                        <span key={idx} className={`text-xs px-2 py-1 rounded ${
                          hist.version === versionCotizacion ? 'bg-yellow-600 text-black font-bold' : 'bg-gray-700 text-gray-300'
                        }`}>
                          v{hist.version}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* BOTONES DE EXPORTACIÓN - SIEMPRE VISIBLES */}
                <div className="mb-4 p-4 bg-gradient-to-r from-blue-900 to-blue-800 rounded-xl border-2 border-blue-500 text-white">
                  <h4 className="font-bold mb-2 flex items-center gap-2">
                    <Download className="w-5 h-5" />
                    📦 Formatos de Exportación Disponibles
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs mb-3">
                    <div className="bg-purple-800 bg-opacity-50 p-2 rounded">
                      <p className="font-bold">👁️ Vista Previa</p>
                      <p className="text-purple-200">Ver sin descargar</p>
                    </div>
                    <div className="bg-blue-800 bg-opacity-50 p-2 rounded">
                      <p className="font-bold">📄 DOCX</p>
                      <p className="text-blue-200">Editable en Word</p>
                    </div>
                    <div className="bg-red-800 bg-opacity-50 p-2 rounded">
                      <p className="font-bold">📕 PDF Nativo</p>
                      <p className="text-red-200">{logoBase64 ? 'Con logo ✅' : 'Sin encabezados'}</p>
                    </div>
                    <div className="bg-green-800 bg-opacity-50 p-2 rounded">
                      <p className="font-bold">🌐 HTML</p>
                      <p className="text-green-200">Código fuente</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                    <button onClick={() => setPaso(2)} className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-xl transition-all border-2 border-gray-600 flex items-center justify-center gap-2">
                      ← Chat
                    </button>
                    
                    <button 
                      onClick={() => setMostrarModalPreview(true)} 
                      className="bg-purple-800 hover:bg-purple-700 text-white px-4 py-2 rounded-xl flex items-center justify-center gap-2 transition-all border-2 border-purple-600 shadow-xl">
                      <Eye className="w-5 h-5" /> Vista Previa
                    </button>
                    
                    <button 
                      onClick={descargarDOCX}
                      disabled={analizando}
                      className="bg-blue-800 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white px-4 py-2 rounded-xl flex items-center justify-center gap-2 transition-all border-2 border-blue-600 shadow-xl">
                      <Download className="w-5 h-5" /> DOCX
                    </button>
                    
                    <button 
                      onClick={descargarPDFNativo}
                      disabled={analizando}
                      className="bg-red-800 hover:bg-red-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white px-4 py-2 rounded-xl flex items-center justify-center gap-2 transition-all border-2 border-red-600 shadow-xl">
                      <Download className="w-5 h-5" /> PDF {logoBase64 && '🔥'}
                    </button>
                    
                    <button 
                      onClick={descargarHTML} 
                      className="bg-green-800 hover:bg-green-700 text-white px-4 py-2 rounded-xl flex items-center justify-center gap-2 transition-all border-2 border-green-600 shadow-xl">
                      <Download className="w-5 h-5" /> HTML
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white text-gray-900 rounded-2xl p-8 shadow-2xl" id="cotizacion-pdf" key={`cotizacion-${ocultarPreciosUnitarios}-${ocultarTotalesPorItem}-${modoVisualizacionIGV}`}>
              <div className="border-b-4 border-red-900 pb-6 mb-6">
                <div className="flex justify-between">
                  <div>
                    <h1 className="text-4xl font-bold text-red-900">{datosEmpresa.nombre}</h1>
                    <p className="text-gray-600 mt-2">RUC: {datosEmpresa.ruc}</p>
                    <p className="text-sm text-gray-500">{datosEmpresa.direccion}</p>
                    <p className="text-sm text-gray-500">{datosEmpresa.ciudad}</p>
                  </div>
                  <div className="text-right">
                    <div className="bg-gradient-to-r from-red-900 to-red-800 text-yellow-400 px-4 py-2 rounded-lg inline-block border-2 border-yellow-600">
                      <p className="text-sm font-bold">COTIZACIÓN</p>
                      <p className="text-2xl font-bold">v{versionCotizacion}</p>
                    </div>
                    <p className="text-sm text-gray-600 mt-2">{new Date().toLocaleDateString('es-PE')}</p>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-6 mb-8">
                <div>
                  <h3 className="font-bold text-red-900 mb-3">CLIENTE</h3>
                  <p><b>Nombre:</b> {cotizacion.cliente?.nombre || 'N/A'}</p>
                  <p><b>Proyecto:</b> {cotizacion.cliente?.proyecto || 'N/A'}</p>
                  <p><b>Dirección:</b> {cotizacion.cliente?.direccion || 'N/A'}</p>
                </div>
                <div>
                  <h3 className="font-bold text-red-900 mb-3">PROYECTO</h3>
                  <p><b>Pisos:</b> {cotizacion.cliente?.pisos || 0}</p>
                  <p><b>Departamentos:</b> {cotizacion.cliente?.departamentos || 0}</p>
                </div>
              </div>

              {Object.keys(itemsPorCapitulo).map(capitulo => (
                <div key={`${capitulo}-${ocultarPreciosUnitarios}-${ocultarTotalesPorItem}`} className="mb-6">
                  <h3 className="bg-gradient-to-r from-red-900 to-red-800 text-yellow-400 py-2 px-3 font-bold uppercase">{capitulo}</h3>
                  <table className="w-full" key={`table-${capitulo}-${ocultarPreciosUnitarios}-${ocultarTotalesPorItem}`}>
                    <thead>
                      <tr className="bg-gray-200">
                        <th className="text-left py-2 px-3 text-sm">DESCRIPCIÓN</th>
                        <th className="text-center py-2 px-3 text-sm">CANT.</th>
                        <th className="text-center py-2 px-3 text-sm">UND.</th>
                        {ocultarPreciosUnitarios ? null : <th className="text-right py-2 px-3 text-sm">P.U.</th>}
                        {ocultarTotalesPorItem ? null : <th className="text-right py-2 px-3 text-sm">TOTAL</th>}
                      </tr>
                    </thead>
                    <tbody>
                      {itemsPorCapitulo[capitulo].map((item, idx) => {
                        const itemIndex = cotizacion.items.findIndex(i => i === item);
                        const subtotalItem = (parseFloat(item.cantidad) || 0) * (parseFloat(item.precioUnitario) || 0);
                        return (
                          <tr key={`${idx}-${ocultarPreciosUnitarios}-${ocultarTotalesPorItem}`} className={idx % 2 === 0 ? 'bg-gray-50' : ''}>
                            <td className="py-2 px-3 text-sm">
                              {modoEdicion ? (
                                <input type="text" value={item.descripcion}
                                  onChange={(e) => actualizarItem(itemIndex, 'descripcion', e.target.value)}
                                  className="w-full px-2 py-1 border border-gray-300 rounded" />
                              ) : item.descripcion}
                              {item.observacion && <span className="block text-xs text-gray-500 mt-1">{item.observacion}</span>}
                            </td>
                            <td className="text-center py-2 px-3">
                              {modoEdicion ? (
                                <input type="number" step="0.01" value={item.cantidad}
                                  onChange={(e) => actualizarItem(itemIndex, 'cantidad', e.target.value)}
                                  className="w-20 px-2 py-1 border border-gray-300 rounded text-center" />
                              ) : item.cantidad}
                            </td>
                            <td className="text-center py-2 px-3 text-sm">{item.unidad}</td>
                            {ocultarPreciosUnitarios ? null : (
                              <td className="text-right py-2 px-3">
                                {modoEdicion ? (
                                  <input type="number" step="0.01" value={item.precioUnitario}
                                    onChange={(e) => actualizarItem(itemIndex, 'precioUnitario', e.target.value)}
                                    className="w-24 px-2 py-1 border border-gray-300 rounded text-right" />
                                ) : `S/ ${parseFloat(item.precioUnitario).toFixed(2)}`}
                              </td>
                            )}
                            {ocultarTotalesPorItem ? null : (
                              <td className="text-right py-2 px-3 font-bold text-base">S/ {subtotalItem.toFixed(2)}</td>
                            )}
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              ))}

              <div className="flex justify-end mb-8">
                <div className="w-full md:w-96">
                  {modoVisualizacionIGV !== 'ocultar-igv' && (
                    <>
                      <div className="flex justify-between py-3 border-b-2 border-gray-300 text-lg">
                        <span className="font-semibold">Subtotal:</span>
                        <span className="font-bold">S/ {totales.subtotal}</span>
                      </div>
                      {modoVisualizacionIGV === 'sin-igv' && (
                        <div className="flex justify-between py-3 border-b-2 border-gray-300 text-lg">
                          <span className="font-semibold">IGV (18%):</span>
                          <span className="font-bold">S/ {totales.igv}</span>
                        </div>
                      )}
                    </>
                  )}
                  <div className="flex justify-between py-6 bg-gradient-to-r from-red-900 via-red-800 to-red-900 text-yellow-400 px-6 rounded-2xl mt-4 shadow-2xl border-4 border-yellow-600 transform hover:scale-105 transition-all duration-300">
                    <span className="font-black text-3xl tracking-wide">TOTAL:</span>
                    <span className="font-black text-5xl tracking-wider animate-pulse">
                      S/ {modoVisualizacionIGV === 'con-igv' ? totales.total : (modoVisualizacionIGV === 'ocultar-igv' ? totales.total : totales.total)}
                    </span>
                  </div>
                  {modoVisualizacionIGV === 'con-igv' && (
                    <p className="text-center text-sm text-gray-600 mt-2 italic">* Precio incluye IGV (18%)</p>
                  )}
                  {modoVisualizacionIGV === 'ocultar-igv' && (
                    <p className="text-center text-sm text-gray-600 mt-2 italic">* Precio final todo incluido</p>
                  )}
                </div>
              </div>

              {modoEdicion && (
                <div className="mb-6 p-4 bg-blue-50 rounded-lg border-2 border-blue-300">
                  <h3 className="font-bold text-blue-900 mb-3">RESUMEN EJECUTIVO (Editable)</h3>
                  <textarea 
                    value={resumenEditable}
                    onChange={(e) => setResumenEditable(e.target.value)}
                    className="w-full h-24 px-3 py-2 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none text-sm"
                    placeholder="Escribe un resumen ejecutivo del proyecto..."
                  />
                </div>
              )}

              {!modoEdicion && resumenEditable && (
                <div className="mb-6 p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
                  <h3 className="font-bold text-blue-900 mb-2">RESUMEN EJECUTIVO</h3>
                  <p className="text-sm text-gray-700 whitespace-pre-line">{resumenEditable}</p>
                </div>
              )}

              {modoEdicion && (
                <div className="mb-6 p-4 bg-green-50 rounded-lg border-2 border-green-300">
                  <h3 className="font-bold text-green-900 mb-3">RECOMENDACIONES TÉCNICAS (Editable)</h3>
                  <textarea 
                    value={recomendacionesEditables}
                    onChange={(e) => setRecomendacionesEditables(e.target.value)}
                    className="w-full h-24 px-3 py-2 border border-green-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none text-sm"
                    placeholder="Escribe recomendaciones técnicas..."
                  />
                </div>
              )}

              {!modoEdicion && recomendacionesEditables && (
                <div className="mb-6 p-4 bg-green-50 rounded-lg border-2 border-green-200">
                  <h3 className="font-bold text-green-900 mb-2">RECOMENDACIONES TÉCNICAS</h3>
                  <p className="text-sm text-gray-700 whitespace-pre-line">{recomendacionesEditables}</p>
                </div>
              )}

              <div className="border-t-2 pt-6 mb-6">
                <h3 className="font-bold text-red-900 mb-3">CONDICIONES COMERCIALES {modoEdicion && '(Editables)'}</h3>
                {modoEdicion ? (
                  <div className="space-y-3 bg-gray-50 p-4 rounded-lg">
                    <div>
                      <label className="block text-sm font-semibold mb-1">Precios:</label>
                      <input 
                        type="text"
                        value={condicionesComerciales.incluye_igv}
                        onChange={(e) => setCondicionesComerciales({...condicionesComerciales, incluye_igv: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:outline-none text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-semibold mb-1">Forma de pago:</label>
                      <input 
                        type="text"
                        value={condicionesComerciales.forma_pago}
                        onChange={(e) => setCondicionesComerciales({...condicionesComerciales, forma_pago: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:outline-none text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-semibold mb-1">Validez:</label>
                      <input 
                        type="text"
                        value={condicionesComerciales.validez}
                        onChange={(e) => setCondicionesComerciales({...condicionesComerciales, validez: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:outline-none text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-semibold mb-1">Garantía:</label>
                      <input 
                        type="text"
                        value={condicionesComerciales.garantia}
                        onChange={(e) => setCondicionesComerciales({...condicionesComerciales, garantia: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:outline-none text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-semibold mb-1">Otra condición (opcional):</label>
                      <input 
                        type="text"
                        value={condicionesComerciales.otra}
                        onChange={(e) => setCondicionesComerciales({...condicionesComerciales, otra: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:outline-none text-sm"
                        placeholder="Ej: Plazo de entrega: 30 días"
                      />
                    </div>
                  </div>
                ) : (
                  <ul className="text-sm space-y-1">
                    <li>• Precios: {condicionesComerciales.incluye_igv}</li>
                    <li>• Forma de pago: {condicionesComerciales.forma_pago}</li>
                    <li>• Validez: {condicionesComerciales.validez}</li>
                    <li>• Garantía: {condicionesComerciales.garantia}</li>
                    {condicionesComerciales.otra && <li>• {condicionesComerciales.otra}</li>}
                  </ul>
                )}
              </div>

              <div className="mt-8 pt-6 border-t-2 text-center text-sm text-gray-600">
                <p className="font-bold text-red-900">{datosEmpresa.nombre}</p>
                <p>📱 WhatsApp: {datosEmpresa.telefono}</p>
                <p>📧 {datosEmpresa.email}</p>
                <p>{datosEmpresa.direccion}</p>
                <p>{datosEmpresa.ciudad}</p>
              </div>
            </div>
          </>
        )}

        {mostrarModalPreview && (
          <div className="fixed inset-0 bg-black bg-opacity-80 z-50 flex items-center justify-center p-4 backdrop-blur-sm"
            onClick={() => setMostrarModalPreview(false)}>
            <div className="bg-white rounded-2xl max-w-6xl max-h-[90vh] w-full overflow-hidden shadow-2xl border-4 border-yellow-600"
              onClick={(e) => e.stopPropagation()}>
              
              <div className="bg-gradient-to-r from-red-900 to-red-800 text-yellow-400 px-6 py-4 flex items-center justify-between border-b-4 border-yellow-600">
                <div className="flex items-center gap-3">
                  <Eye className="w-6 h-6" />
                  <h2 className="text-xl font-bold">Vista Previa - Cotización v{versionCotizacion}</h2>
                </div>
                <button 
                  onClick={() => setMostrarModalPreview(false)}
                  className="bg-red-700 hover:bg-red-600 text-white p-2 rounded-lg transition-all">
                  <X className="w-6 h-6" />
                </button>
              </div>

              <div className="overflow-y-auto max-h-[calc(90vh-180px)] p-6 bg-gray-100">
                <div className="bg-white rounded-xl shadow-lg p-8" id="preview-content">
                  <div className="border-b-4 border-red-900 pb-6 mb-6">
                    <div className="flex justify-between items-start">
                      <div>
                        <h1 className="text-3xl font-bold text-red-900">{datosEmpresa.nombre}</h1>
                        <p className="text-gray-600 mt-2">RUC: {datosEmpresa.ruc}</p>
                        <p className="text-sm text-gray-500">{datosEmpresa.direccion}</p>
                        <p className="text-sm text-gray-500">{datosEmpresa.ciudad}</p>
                      </div>
                      <div className="text-right">
                        {logoBase64 && (
                          <img src={logoBase64} alt="Logo" className="w-20 h-20 object-contain mb-2" />
                        )}
                        <div className="bg-gradient-to-r from-red-900 to-red-800 text-yellow-400 px-4 py-2 rounded-lg inline-block border-2 border-yellow-600">
                          <p className="text-sm font-bold">COTIZACIÓN</p>
                          <p className="text-xl font-bold">v{versionCotizacion}</p>
                        </div>
                        <p className="text-sm text-gray-600 mt-2">{new Date().toLocaleDateString('es-PE')}</p>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-6 mb-6">
                    <div>
                      <h3 className="font-bold text-red-900 mb-2">CLIENTE</h3>
                      <p className="text-sm"><b>Nombre:</b> {cotizacion?.cliente?.nombre || 'N/A'}</p>
                      <p className="text-sm"><b>Proyecto:</b> {cotizacion?.cliente?.proyecto || 'N/A'}</p>
                      <p className="text-sm"><b>Dirección:</b> {cotizacion?.cliente?.direccion || 'N/A'}</p>
                    </div>
                    <div>
                      <h3 className="font-bold text-red-900 mb-2">PROYECTO</h3>
                      <p className="text-sm"><b>Pisos:</b> {cotizacion?.cliente?.pisos || 0}</p>
                      <p className="text-sm"><b>Departamentos:</b> {cotizacion?.cliente?.departamentos || 0}</p>
                    </div>
                  </div>

                  {Object.keys(itemsPorCapitulo).map(capitulo => (
                    <div key={capitulo} className="mb-6">
                      <h3 className="bg-gradient-to-r from-red-900 to-red-800 text-yellow-400 py-2 px-3 font-bold uppercase text-sm">{capitulo}</h3>
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="bg-gray-200">
                            <th className="text-left py-2 px-3 text-xs">DESCRIPCIÓN</th>
                            <th className="text-center py-2 px-3 text-xs">CANT.</th>
                            <th className="text-center py-2 px-3 text-xs">UND.</th>
                            {!ocultarPreciosUnitarios && <th className="text-right py-2 px-3 text-xs">P.U.</th>}
                            {!ocultarTotalesPorItem && <th className="text-right py-2 px-3 text-xs">TOTAL</th>}
                          </tr>
                        </thead>
                        <tbody>
                          {itemsPorCapitulo[capitulo].map((item, idx) => {
                            const subtotalItem = (parseFloat(item.cantidad) || 0) * (parseFloat(item.precioUnitario) || 0);
                            return (
                              <tr key={idx} className={idx % 2 === 0 ? 'bg-gray-50' : ''}>
                                <td className="py-2 px-3 text-xs">
                                  {item.descripcion}
                                  {item.observacion && <span className="block text-xs text-gray-500 mt-1">{item.observacion}</span>}
                                </td>
                                <td className="text-center py-2 px-3 text-xs">{item.cantidad}</td>
                                <td className="text-center py-2 px-3 text-xs">{item.unidad}</td>
                                {!ocultarPreciosUnitarios && <td className="text-right py-2 px-3 text-xs">S/ {parseFloat(item.precioUnitario).toFixed(2)}</td>}
                                {!ocultarTotalesPorItem && <td className="text-right py-2 px-3 text-xs font-bold">S/ {subtotalItem.toFixed(2)}</td>}
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  ))}

                  <div className="flex justify-end mb-6">
                    <div className="w-full md:w-80">
                      {modoVisualizacionIGV !== 'ocultar-igv' && (
                        <>
                          <div className="flex justify-between py-2 border-b border-gray-300">
                            <span className="font-semibold">Subtotal:</span>
                            <span className="font-bold">S/ {totales.subtotal}</span>
                          </div>
                          {modoVisualizacionIGV === 'sin-igv' && (
                            <div className="flex justify-between py-2 border-b border-gray-300">
                              <span className="font-semibold">IGV (18%):</span>
                              <span className="font-bold">S/ {totales.igv}</span>
                            </div>
                          )}
                        </>
                      )}
                      <div className="flex justify-between py-4 bg-gradient-to-r from-red-900 to-red-800 text-yellow-400 px-4 rounded-xl mt-3 shadow-xl border-2 border-yellow-600">
                        <span className="font-black text-xl">TOTAL:</span>
                        <span className="font-black text-2xl">S/ {totales.total}</span>
                      </div>
                    </div>
                  </div>

                  <div className="border-t-2 pt-4 mb-4">
                    <h3 className="font-bold text-red-900 mb-2 text-sm">CONDICIONES COMERCIALES</h3>
                    <ul className="text-xs space-y-1">
                      <li>• Precios: {condicionesComerciales.incluye_igv}</li>
                      <li>• Forma de pago: {condicionesComerciales.forma_pago}</li>
                      <li>• Validez: {condicionesComerciales.validez}</li>
                      <li>• Garantía: {condicionesComerciales.garantia}</li>
                      {condicionesComerciales.otra && <li>• {condicionesComerciales.otra}</li>}
                    </ul>
                  </div>

                  <div className="mt-6 pt-4 border-t-2 text-center text-xs text-gray-600">
                    <p className="font-bold text-red-900">{datosEmpresa.nombre}</p>
                    <p>📱 {datosEmpresa.telefono} | 📧 {datosEmpresa.email}</p>
                  </div>
                </div>
              </div>

              <div className="bg-gray-100 px-6 py-4 border-t-2 border-gray-300 flex gap-3 justify-end">
                <button 
                  onClick={() => window.print()}
                  className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all">
                  <Download className="w-4 h-4" /> Imprimir
                </button>
                <button 
                  onClick={descargarHTML}
                  className="bg-green-700 hover:bg-green-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all">
                  <Download className="w-4 h-4" /> Descargar HTML
                </button>
                <button 
                  onClick={() => setMostrarModalPreview(false)}
                  className="bg-red-700 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-all">
                  Cerrar
                </button>
              </div>
            </div>
          </div>
        )}

        <style>{`
          @media print {
            .no-print { display: none !important; }
            @page { size: A4; margin: 1.5cm; }
            * { print-color-adjust: exact !important; -webkit-print-color-adjust: exact !important; }
          }
        `}</style>
      </div>
    </div>
  );
};

export default CotizadorPro;