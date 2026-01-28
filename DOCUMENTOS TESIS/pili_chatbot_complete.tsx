import React, { useState, useEffect, useRef } from 'react';
import { Send, Zap, Phone, MapPin, Clock, CheckCircle, AlertCircle, Menu } from 'lucide-react';

const PiliChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [conversationState, setConversationState] = useState({
    stage: 'initial',
    selectedService: null,
    selectedCategory: null,
    businessType: null,
    area: null,
    floors: 1,
    riskLevel: null,
    clientName: null,
    phone: null,
    preferredDay: null,
    preferredTime: null,
    address: null,
    quantity: null
  });
  const messagesEndRef = useRef(null);

  // Colores corporativos Tesla
  const colors = {
    primary: '#8B0000',
    secondary: '#FFD700',
    fire: '#FF4500',
    dark: '#2C0000',
    light: '#FFF8DC'
  };

  // Base de conocimiento COMPLETA
  const knowledgeBase = {
    // PRECIOS MUNICIPALES (TUPA HUANCAYO)
    municipalPrices: {
      BAJO: { price: 168.30, renewal: 90.30, days: 7 },
      MEDIO: { price: 208.60, renewal: 109.40, days: 7 },
      ALTO: { price: 703.00, renewal: 417.40, days: 7 },
      MUY_ALTO: { price: 1084.60, renewal: 629.20, days: 7 }
    },
    
    // SERVICIOS TESLA
    teslaServices: {
      // 1. CERTIFICADO ITSE
      ITSE: {
        name: 'Certificado ITSE',
        icon: '📋',
        description: 'Inspección Técnica de Seguridad en Edificaciones',
        prices: {
          BAJO: { min: 300, max: 500 },
          MEDIO: { min: 450, max: 650 },
          ALTO: { min: 800, max: 1200 },
          MUY_ALTO: { min: 1200, max: 1800 }
        },
        includes: [
          'Evaluación técnica completa',
          'Elaboración de planos (si necesario)',
          'Gestión del trámite municipal',
          'Seguimiento hasta obtención del certificado'
        ],
        time: '15-20 días hábiles'
      },
      
      // 2. POZO A TIERRA
      POZO_TIERRA: {
        name: 'Pozo a Tierra / Puesta a Tierra',
        icon: '⚡',
        description: 'Sistema de protección eléctrica',
        priceMin: 1500,
        priceMax: 2500,
        includes: [
          'Medición de resistividad del terreno',
          'Diseño según normativa vigente',
          'Excavación e instalación completa',
          'Pruebas y certificación final',
          'Materiales (varillas, conectores, cable)'
        ],
        factors: [
          'Tipo de terreno (arcilloso, arenoso, rocoso)',
          'Resistividad medida del suelo',
          'Profundidad requerida',
          'Cantidad de electrodos necesarios'
        ],
        time: '3-5 días'
      },
      
      // 3. LUCES DE EMERGENCIA
      LUCES_EMERGENCIA: {
        name: 'Luces de Emergencia',
        icon: '💡',
        description: 'Suministro e instalación de iluminación de emergencia',
        pricePerUnit: 150,
        includes: [
          'Luz de emergencia certificada',
          'Instalación completa y cableado',
          'Prueba de funcionamiento',
          'Garantía 1 año'
        ],
        types: [
          'LED recargable (batería integrada)',
          'Con señalización de salida',
          'Autonomía 90 minutos mínimo',
          'Certificada para uso comercial/industrial'
        ],
        time: '1-2 días'
      },
      
      // 4. MANTENIMIENTO ELÉCTRICO
      MANTENIMIENTO: {
        name: 'Mantenimiento Eléctrico',
        icon: '🔧',
        description: 'Mantenimiento preventivo y correctivo',
        types: {
          PREVENTIVO: {
            name: 'Mantenimiento Preventivo',
            priceMin: 200,
            priceMax: 400,
            includes: [
              'Inspección de tableros y conexiones',
              'Medición de aislamientos',
              'Limpieza y ajuste de contactos',
              'Revisión de sistema puesta a tierra',
              'Termografía (opcional)',
              'Informe técnico detallado'
            ]
          },
          CORRECTIVO: {
            name: 'Mantenimiento Correctivo',
            priceMin: 500,
            priceMax: 1200,
            includes: [
              'Diagnóstico de fallas',
              'Reparación de averías',
              'Reemplazo de componentes defectuosos',
              'Pruebas de funcionamiento',
              'Garantía del trabajo realizado'
            ]
          },
          EMERGENCIA: {
            name: 'Servicio de Emergencia 24h',
            priceHour: 150,
            note: 'Por hora + materiales'
          }
        },
        benefits: 'Plan anual: 15% descuento',
        time: '1-3 días'
      },
      
      // 5. SISTEMA CONTRA INCENDIOS
      CONTRA_INCENDIOS: {
        name: 'Sistema Contra Incendios',
        icon: '🧯',
        description: 'Detección y protección contra incendios',
        packages: {
          MINI_KIT: {
            name: 'Mini Kit Detección de Humo',
            price: 1500,
            includes: [
              'Panel de control convencional',
              '2-4 Detectores de humo ópticos',
              'Sirena con luz estroboscópica',
              'Interruptor local manual',
              'Cableado completo',
              'Instalación y programación',
              'Pruebas de funcionamiento'
            ],
            ideal: 'Locales pequeños, oficinas, tiendas (hasta 200m²)'
          },
          COMPLETO: {
            name: 'Sistema Completo',
            note: 'Cotización después de visita técnica',
            additionalItems: [
              'Mangueras y gabinetes',
              'Rociadores automáticos (sprinklers)',
              'Extintores portátiles',
              'Señalización fotoluminiscente',
              'Central de alarma avanzada'
            ]
          }
        },
        time: '5-10 días (Mini Kit), 15-30 días (Completo)'
      },
      
      // 6. LAMINADO DE VIDRIOS
      LAMINADO_VIDRIOS: {
        name: 'Laminado de Vidrios',
        icon: '🪟',
        description: 'Laminado de seguridad para vidrios',
        pricePerM2: 40,
        applications: [
          'Vitrinas comerciales',
          'Estantes de vidrio',
          'Mamparas divisorias',
          'Puertas de vidrio',
          'Ventanas de seguridad'
        ],
        benefits: [
          'Protección anti-impacto',
          'Reducción de UV',
          'Mayor seguridad',
          'Mantiene transparencia'
        ],
        types: [
          'Laminado de seguridad estándar',
          'Laminado anti-impacto reforzado',
          'Laminado con control solar'
        ],
        time: '2-4 días'
      },
      
      // 7. ROTULADO Y SEÑALIZACIÓN
      ROTULADO: {
        name: 'Rotulado y Señalización',
        icon: '🪧',
        description: 'Rotulado comercial y señalización',
        note: 'Incluido en servicio de mantenimiento ITSE',
        types: {
          SENALETICA_SEGURIDAD: {
            name: 'Señalética de Seguridad',
            included: 'Incluido en paquetes ITSE y Mantenimiento',
            items: [
              'Señales de salida de emergencia',
              'Rutas de evacuación',
              'Ubicación de extintores',
              'Zonas de seguridad',
              'Prohibiciones y advertencias'
            ]
          },
          ROTULADO_COMERCIAL: {
            name: 'Rotulado Comercial',
            note: 'Cotización personalizada',
            options: [
              'Letras corpóreas iluminadas',
              'Letreros LED',
              'Rotulado de fachada',
              'Señalización interna'
            ]
          }
        }
      }
    },
    
    // CATEGORÍAS PARA ITSE
    itseCategories: {
      SALUD: {
        name: 'Salud',
        icon: '🏥',
        types: ['Centro de Salud', 'Clínica', 'Consultorio Médico', 'Farmacia', 'Laboratorio'],
        baseRisk: 'MEDIO'
      },
      EDUCACION: {
        name: 'Educación',
        icon: '🎓',
        types: ['Colegio', 'Instituto', 'Universidad', 'Centro de Idiomas', 'Guardería'],
        baseRisk: 'MEDIO'
      },
      HOSPEDAJE: {
        name: 'Hospedaje',
        icon: '🏨',
        types: ['Hotel', 'Hostal', 'Casa de Hospedaje', 'Apart Hotel'],
        baseRisk: 'ALTO'
      },
      COMERCIO: {
        name: 'Comercio',
        icon: '🏪',
        types: ['Tienda', 'Minimarket', 'Ferretería', 'Bodega', 'Librería'],
        baseRisk: 'BAJO'
      },
      RESTAURANTE: {
        name: 'Restaurante',
        icon: '🍽️',
        types: ['Restaurante', 'Cafetería', 'Bar', 'Pollería', 'Fast Food'],
        baseRisk: 'MEDIO'
      },
      OFICINA: {
        name: 'Oficina',
        icon: '🏢',
        types: ['Oficina Administrativa', 'Estudio Contable', 'Estudio Legal', 'Consultora'],
        baseRisk: 'BAJO'
      },
      INDUSTRIAL: {
        name: 'Industrial',
        icon: '🏭',
        types: ['Fábrica', 'Taller', 'Almacén', 'Planta Industrial'],
        baseRisk: 'ALTO'
      },
      ENCUENTRO: {
        name: 'Encuentro',
        icon: '🎭',
        types: ['Auditorio', 'Sala de Eventos', 'Teatro', 'Centro de Convenciones', 'Discoteca'],
        baseRisk: 'ALTO'
      }
    }
  };

  // Determinar nivel de riesgo ITSE
  const determineRiskLevel = (category, businessType, area, floors) => {
    const cat = knowledgeBase.itseCategories[category];
    
    if (category === 'COMERCIO') {
      if (area <= 100 && floors <= 2) return 'BAJO';
      if (area <= 500) return 'MEDIO';
      return 'ALTO';
    }
    
    if (category === 'OFICINA') {
      if (area <= 560 && floors <= 4) return 'BAJO';
      return 'MEDIO';
    }
    
    if (category === 'RESTAURANTE') {
      if (area > 150) return 'ALTO';
      return 'MEDIO';
    }
    
    if (category === 'HOSPEDAJE' || category === 'ENCUENTRO') {
      if (area > 500 || floors > 3) return 'MUY_ALTO';
      return 'ALTO';
    }
    
    if (category === 'INDUSTRIAL') {
      if (area > 300) return 'MUY_ALTO';
      return 'ALTO';
    }
    
    return cat.baseRisk;
  };

  // Calcular cotización ITSE
  const calculateITSEQuote = (riskLevel) => {
    const municipal = knowledgeBase.municipalPrices[riskLevel];
    const tesla = knowledgeBase.teslaServices.ITSE.prices[riskLevel];
    
    return {
      municipal: municipal.price,
      teslaMin: tesla.min,
      teslaMax: tesla.max,
      totalMin: municipal.price + tesla.min,
      totalMax: municipal.price + tesla.max,
      days: municipal.days
    };
  };

  // Generar mensaje WhatsApp
  const generateWhatsAppMessage = () => {
    const { selectedService, clientName, phone, address, preferredDay, preferredTime } = conversationState;
    
    let message = `*SOLICITUD DE SERVICIO - TESLA ELECTRICIDAD* ⚡\n\n`;
    message += `👤 *Nombre:* ${clientName}\n`;
    message += `📱 *Teléfono:* ${phone}\n`;
    message += `📍 *Dirección:* ${address || 'Por confirmar'}\n\n`;
    
    if (selectedService === 'ITSE') {
      const { selectedCategory, businessType, area, floors, riskLevel } = conversationState;
      const quote = calculateITSEQuote(riskLevel);
      message += `🏢 *Servicio:* Certificado ITSE\n`;
      message += `📋 *Tipo:* ${businessType}\n`;
      message += `📐 *Área:* ${area} m²\n`;
      message += `🏗️ *Pisos:* ${floors}\n`;
      message += `🎯 *Nivel Riesgo:* ${riskLevel.replace('_', ' ')}\n\n`;
      message += `💰 *Cotización Estimada:*\n`;
      message += `• Municipal: S/ ${quote.municipal}\n`;
      message += `• Tesla: S/ ${quote.teslaMin} - ${quote.teslaMax}\n`;
      message += `• *Total: S/ ${quote.totalMin} - ${quote.totalMax}*\n`;
    } else {
      const service = knowledgeBase.teslaServices[selectedService];
      message += `⚡ *Servicio:* ${service.name}\n`;
      
      if (conversationState.quantity) {
        message += `🔢 *Cantidad:* ${conversationState.quantity}\n`;
      }
      if (conversationState.area) {
        message += `📐 *Área:* ${conversationState.area} m²\n`;
      }
    }
    
    message += `\n📅 *Disponibilidad:*\n`;
    message += `• Día: ${preferredDay}\n`;
    message += `• Hora: ${preferredTime}\n\n`;
    message += `_Solicito visita técnica gratuita para cotización exacta._`;
    
    return encodeURIComponent(message);
  };

  useEffect(() => {
    addMessage(
      `¡Hola! ⚡ Soy **Pili**, tu asistente especializado de **Tesla Electricidad**, Huancayo.

Te ayudo con información y cotizaciones de nuestros servicios eléctricos.

¿Qué servicio necesitas?`,
      'bot',
      true,
      'services'
    );
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const addMessage = (text, sender, showButtons = false, buttonType = null) => {
    setMessages(prev => [...prev, { text, sender, timestamp: new Date(), showButtons, buttonType }]);
  };

  const simulateTyping = (callback, delay = 1500) => {
    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);
      callback();
    }, delay);
  };

  // Manejar selección de servicio
  const handleServiceSelect = (service) => {
    const serviceData = knowledgeBase.teslaServices[service];
    setConversationState(prev => ({ ...prev, selectedService: service }));
    addMessage(`${serviceData.icon} ${serviceData.name}`, 'user');
    
    simulateTyping(() => {
      if (service === 'ITSE') {
        // Flujo ITSE
        setConversationState(prev => ({ ...prev, stage: 'itse_category' }));
        addMessage(
          `Perfecto, te ayudo con el **Certificado ITSE**.

Para comenzar, selecciona el tipo de establecimiento:`,
          'bot',
          true,
          'itse_categories'
        );
      } else if (service === 'LUCES_EMERGENCIA') {
        // Flujo Luces de Emergencia
        setConversationState(prev => ({ ...prev, stage: 'quantity' }));
        addMessage(
          `**${serviceData.name}**

${serviceData.description}

💰 **Precio:** S/ ${serviceData.pricePerUnit} por unidad instalada

**Incluye:**
${serviceData.includes.map(item => `✅ ${item}`).join('\n')}

⏱️ **Tiempo:** ${serviceData.time}

¿Cuántas luces de emergencia necesitas instalar?

_Ejemplo: 5_`,
          'bot'
        );
      } else if (service === 'LAMINADO_VIDRIOS') {
        // Flujo Laminado
        setConversationState(prev => ({ ...prev, stage: 'area' }));
        addMessage(
          `**${serviceData.name}**

${serviceData.description}

💰 **Precio:** S/ ${serviceData.pricePerM2} por m²

**Aplicaciones:**
${serviceData.applications.map(app => `• ${app}`).join('\n')}

**Beneficios:**
${serviceData.benefits.map(ben => `✅ ${ben}`).join('\n')}

⏱️ **Tiempo:** ${serviceData.time}

¿Cuántos metros cuadrados necesitas laminar?

_Ejemplo: 25_`,
          'bot'
        );
      } else {
        // Otros servicios - mostrar info y agendar
        showServiceInfo(service);
      }
    });
  };

  const showServiceInfo = (service) => {
    const serviceData = knowledgeBase.teslaServices[service];
    let message = `**${serviceData.name}**\n\n${serviceData.description}\n\n`;
    
    if (service === 'POZO_TIERRA') {
      message += `💰 **Precio:** S/ ${serviceData.priceMin} - ${serviceData.priceMax}\n\n`;
      message += `**Incluye:**\n${serviceData.includes.map(item => `✅ ${item}`).join('\n')}\n\n`;
      message += `**Factores que afectan el precio:**\n${serviceData.factors.map(f => `• ${f}`).join('\n')}\n\n`;
      message += `⏱️ **Tiempo:** ${serviceData.time}`;
    } else if (service === 'MANTENIMIENTO') {
      message += `**Tipos de Mantenimiento:**\n\n`;
      message += `🔧 **Preventivo:** S/ ${serviceData.types.PREVENTIVO.priceMin} - ${serviceData.types.PREVENTIVO.priceMax}\n`;
      message += `${serviceData.types.PREVENTIVO.includes.map(i => `✅ ${i}`).join('\n')}\n\n`;
      message += `🔧 **Correctivo:** S/ ${serviceData.types.CORRECTIVO.priceMin} - ${serviceData.types.CORRECTIVO.priceMax}\n`;
      message += `${serviceData.types.CORRECTIVO.includes.map(i => `✅ ${i}`).join('\n')}\n\n`;
      message += `🚨 **Emergencia 24h:** S/ ${serviceData.types.EMERGENCIA.priceHour}/hora + materiales\n\n`;
      message += `💡 ${serviceData.benefits}`;
    } else if (service === 'CONTRA_INCENDIOS') {
      message += `**Mini Kit Detección de Humo**\n`;
      message += `💰 **Precio:** S/ ${serviceData.packages.MINI_KIT.price}\n\n`;
      message += `**Incluye:**\n${serviceData.packages.MINI_KIT.includes.map(i => `✅ ${i}`).join('\n')}\n\n`;
      message += `📏 **Ideal para:** ${serviceData.packages.MINI_KIT.ideal}\n\n`;
      message += `**Sistema Completo:**\n`;
      message += `${serviceData.packages.COMPLETO.additionalItems.map(i => `• ${i}`).join('\n')}\n`;
      message += `_Cotización después de evaluación técnica_\n\n`;
      message += `⏱️ **Tiempo:** ${serviceData.time}`;
    }
    
    message += `\n\n🆓 **¡Visita técnica gratuita!** ¿Agendamos?`;
    
    addMessage(message, 'bot', true, 'schedule');
  };

  // Resto de handlers (ITSE, área, nombre, etc.)
  const handleITSECategorySelect = (category) => {
    setConversationState(prev => ({ ...prev, selectedCategory: category, stage: 'business_type' }));
    const cat = knowledgeBase.itseCategories[category];
    addMessage(`${cat.icon} ${cat.name}`, 'user');
    
    simulateTyping(() => {
      addMessage(
        `Perfecto, trabajamos con establecimientos de **${cat.name}**.

¿Qué tipo específico es tu negocio?`,
        'bot',
        true,
        'business_types'
      );
    });
  };

  const handleBusinessTypeSelect = (type) => {
    setConversationState(prev => ({ ...prev, businessType: type, stage: 'area' }));
    addMessage(type, 'user');
    
    simulateTyping(() => {
      addMessage(
        `Excelente. Para el **${type}**, necesito el área total del establecimiento.

¿Cuántos metros cuadrados (m²) tiene?

_Ejemplo: 150_`,
        'bot'
      );
    });
  };

  const handleAreaInput = (area) => {
    const areaNum = parseInt(area);
    if (isNaN(areaNum) || areaNum <= 0) {
      addMessage('Por favor ingresa un número válido de metros cuadrados.', 'bot');
      return;
    }
    
    if (conversationState.selectedService === 'LAMINADO_VIDRIOS') {
      // Calcular precio laminado
      const total = areaNum * knowledgeBase.teslaServices.LAMINADO_VIDRIOS.pricePerM2;
      setConversationState(prev => ({ ...prev, area: areaNum, stage: 'schedule' }));
      addMessage(`${areaNum} m²`, 'user');
      
      simulateTyping(() => {
        addMessage(
          `Perfecto, **${areaNum} m²** registrado.

💰 **COTIZACIÓN:**
• ${areaNum} m² × S/ 40 = **S/ ${total}**

⏱️ Tiempo estimado: 2-4 días

🆓 **¡Visita técnica gratuita!** ¿Agendamos para confirmar detalles?`,
          'bot',
          true,
          'schedule'
        );
      });
    } else {
      // Flujo ITSE
      setConversationState(prev => ({ ...prev, area: areaNum, stage: 'floors' }));
      addMessage(`${areaNum} m²`, 'user');
      
      simulateTyping(() => {
        addMessage(
          `Perfecto, **${areaNum} m²** registrado.

¿Cuántos pisos tiene el establecimiento?

_Ejemplo: 1, 2, 3..._`,
          'bot'
        );
      });
    }
  };

  const handleQuantityInput = (quantity) => {
    const qty = parseInt(quantity);
    if (isNaN(qty) || qty <= 0) {
      addMessage('Por favor ingresa un número válido.', 'bot');
      return;
    }
    
    const service = knowledgeBase.teslaServices.LUCES_EMERGENCIA;
    const total = qty * service.pricePerUnit;
    
    setConversationState(prev => ({ ...prev, quantity: qty, stage: 'schedule' }));
    addMessage(`${qty} unidades`, 'user');
    
    simulateTyping(() => {
      addMessage(
        `Perfecto, **${qty} luces de emergencia**.

💰 **COTIZACIÓN:**
• ${qty} unidades × S/ ${service.pricePerUnit} = **S/ ${total}**

⏱️ Tiempo de instalación: ${service.time}

🆓 **¡Visita técnica gratuita!** ¿Agendamos?`,
        'bot',
        true,
        'schedule'
      );
    });
  };

  const handleFloorsInput = (floors) => {
    const floorsNum = parseInt(floors);
    if (isNaN(floorsNum) || floorsNum <= 0) {
      addMessage('Por favor ingresa un número válido de pisos.', 'bot');
      return;
    }
    
    const riskLevel = determineRiskLevel(
      conversationState.selectedCategory,
      conversationState.businessType,
      conversationState.area,
      floorsNum
    );
    
    setConversationState(prev => ({ 
      ...prev, 
      floors: floorsNum, 
      riskLevel: riskLevel,
      stage: 'quote' 
    }));
    addMessage(`${floorsNum} ${floorsNum === 1 ? 'piso' : 'pisos'}`, 'user');
    
    simulateTyping(() => {
      const quote = calculateITSEQuote(riskLevel);
      const riskText = riskLevel.replace('_', ' ');
      
      addMessage(
        `📊 **ANÁLISIS COMPLETADO**

**Tu establecimiento:**
• ${conversationState.businessType}
• ${conversationState.area} m²
• ${floorsNum} ${floorsNum === 1 ? 'piso' : 'pisos'}

🎯 **Nivel de Riesgo:** ${riskText}

💰 **COTIZACIÓN ITSE:**

**1️⃣ DERECHO MUNICIPAL** _(pagas en municipalidad)_
└─ S/ ${quote.municipal}

**2️⃣ SERVICIO TÉCNICO TESLA** _(nos pagas)_
└─ S/ ${quote.teslaMin} - ${quote.teslaMax}

**Incluye:**
✅ Evaluación técnica completa
✅ Elaboración de planos
✅ Gestión del trámite municipal
✅ Seguimiento hasta obtención

💵 **INVERSIÓN TOTAL: S/ ${quote.totalMin} - ${quote.totalMax}**

⏱️ Plazo: ${quote.days} días hábiles (municipal) + 15-20 días (servicio Tesla)

⚠️ _El derecho municipal NO lo cobramos nosotros. Tú lo pagas directamente en la Municipalidad de Huancayo._

🆓 **¡Visita técnica gratuita!** ¿Agendamos?`,
        'bot',
        true,
        'schedule'
      );
    }, 2000);
  };

  const handleScheduleVisit = () => {
    setConversationState(prev => ({ ...prev, stage: 'name' }));
    addMessage('Sí, agendar visita técnica', 'user');
    
    simulateTyping(() => {
      addMessage(
        `¡Perfecto! 🎯 Vamos a agendar tu visita técnica gratuita.

¿Cuál es tu nombre completo?`,
        'bot'
      );
    });
  };

  const handleNameInput = (name) => {
    setConversationState(prev => ({ ...prev, clientName: name, stage: 'phone' }));
    addMessage(name, 'user');
    
    simulateTyping(() => {
      addMessage(
        `Mucho gusto, **${name}** 👋

¿Cuál es tu número de teléfono?

_Ejemplo: 906315961_`,
        'bot'
      );
    });
  };

  const handlePhoneInput = (phone) => {
    const phoneClean = phone.replace(/\D/g, '');
    if (phoneClean.length < 9) {
      addMessage('Por favor ingresa un número de teléfono válido (mínimo 9 dígitos).', 'bot');
      return;
    }
    
    setConversationState(prev => ({ ...prev, phone: phoneClean, stage: 'address' }));
    addMessage(phone, 'user');
    
    simulateTyping(() => {
      addMessage(
        `Perfecto 📱

¿Cuál es la dirección exacta del establecimiento/proyecto?

_Ejemplo: Jr. Real 456, Huancayo_`,
        'bot'
      );
    });
  };

  const handleAddressInput = (address) => {
    setConversationState(prev => ({ ...prev, address: address, stage: 'day' }));
    addMessage(address, 'user');
    
    simulateTyping(() => {
      addMessage(
        `Excelente 📍

¿Qué día de la semana prefieres para la visita?

_Ejemplo: Lunes, Martes, Miércoles..._`,
        'bot'
      );
    });
  };

  const handleDayInput = (day) => {
    setConversationState(prev => ({ ...prev, preferredDay: day, stage: 'time' }));
    addMessage(day, 'user');
    
    simulateTyping(() => {
      addMessage(
        `Perfecto 📅

¿En qué horario tienes disponibilidad?

_Ejemplo: 10:00 AM, 3:00 PM, Mañana, Tarde..._`,
        'bot'
      );
    });
  };

  const handleTimeInput = (time) => {
    setConversationState(prev => ({ ...prev, preferredTime: time, stage: 'confirm' }));
    addMessage(time, 'user');
    
    simulateTyping(() => {
      let summary = `✅ **¡DATOS CONFIRMADOS!**\n\n`;
      summary += `👤 **Nombre:** ${conversationState.clientName}\n`;
      summary += `📱 **Teléfono:** ${conversationState.phone}\n`;
      summary += `📍 **Dirección:** ${conversationState.address}\n`;
      summary += `📅 **Día:** ${conversationState.preferredDay}\n`;
      summary += `⏰ **Hora:** ${conversationState.preferredTime}\n\n`;
      
      const service = knowledgeBase.teslaServices[conversationState.selectedService];
      summary += `⚡ **Servicio:** ${service.name}\n\n`;
      
      summary += `🎯 **Siguiente paso:** Un especialista te contactará por WhatsApp para confirmar tu cita en menos de 2 horas.\n\n`;
      summary += `¿Todo correcto?`;
      
      addMessage(summary, 'bot', true, 'confirm');
    }, 1500);
  };

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    const message = inputValue.trim();
    addMessage(message, 'user');
    setInputValue('');

    switch (conversationState.stage) {
      case 'area':
        handleAreaInput(message);
        break;
      case 'floors':
        handleFloorsInput(message);
        break;
      case 'quantity':
        handleQuantityInput(message);
        break;
      case 'name':
        handleNameInput(message);
        break;
      case 'phone':
        handlePhoneInput(message);
        break;
      case 'address':
        handleAddressInput(message);
        break;
      case 'day':
        handleDayInput(message);
        break;
      case 'time':
        handleTimeInput(message);
        break;
      default:
        simulateTyping(() => {
          addMessage('Por favor selecciona una opción de los botones disponibles o escribe tu consulta.', 'bot');
        });
    }
  };

  const QuickButtons = ({ message }) => {
    if (!message.showButtons) return null;

    const buttonStyle = {
      padding: '12px 16px',
      background: `linear-gradient(135deg, ${colors.primary}, ${colors.fire})`,
      color: 'white',
      border: 'none',
      borderRadius: '8px',
      cursor: 'pointer',
      fontSize: '13px',
      fontWeight: '600',
      transition: 'transform 0.2s',
      width: '100%'
    };

    if (message.buttonType === 'services') {
      return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px', marginTop: '12px' }}>
          {Object.entries(knowledgeBase.teslaServices).map(([key, service]) => (
            <button
              key={key}
              onClick={() => handleServiceSelect(key)}
              style={buttonStyle}
              onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
              onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
            >
              {service.icon} {service.name}
            </button>
          ))}
        </div>
      );
    }

    if (message.buttonType === 'itse_categories') {
      return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px', marginTop: '12px' }}>
          {Object.entries(knowledgeBase.itseCategories).map(([key, cat]) => (
            <button
              key={key}
              onClick={() => handleITSECategorySelect(key)}
              style={buttonStyle}
            >
              {cat.icon} {cat.name}
            </button>
          ))}
        </div>
      );
    }

    if (message.buttonType === 'business_types') {
      const types = knowledgeBase.itseCategories[conversationState.selectedCategory].types;
      return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px', marginTop: '12px' }}>
          {types.map((type) => (
            <button
              key={type}
              onClick={() => handleBusinessTypeSelect(type)}
              style={{...buttonStyle, fontSize: '12px'}}
            >
              {type}
            </button>
          ))}
        </div>
      );
    }

    if (message.buttonType === 'schedule') {
      return (
        <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
          <button
            onClick={handleScheduleVisit}
            style={{
              flex: 1,
              padding: '14px',
              background: `linear-gradient(135deg, ${colors.secondary}, #FFA500)`,
              color: colors.dark,
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: 'bold'
            }}
          >
            📅 Sí, agendar visita
          </button>
          <button
            onClick={() => {
              window.open(`https://wa.me/51906315961?text=${encodeURIComponent('Hola, tengo consultas sobre los servicios de Tesla Electricidad')}`, '_blank');
            }}
            style={{
              flex: 1,
              padding: '14px',
              background: 'white',
              color: colors.primary,
              border: `2px solid ${colors.primary}`,
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: 'bold'
            }}
          >
            💬 Tengo dudas
          </button>
        </div>
      );
    }

    if (message.buttonType === 'confirm') {
      return (
        <div style={{ marginTop: '12px' }}>
          <button
            onClick={() => {
              const whatsappMsg = generateWhatsAppMessage();
              window.open(`https://wa.me/51906315961?text=${whatsappMsg}`, '_blank');
              addMessage('Redirigiendo a WhatsApp...', 'user');
              simulateTyping(() => {
                addMessage(
                  `✅ ¡Perfecto! Te redirigimos a WhatsApp Business.

Un especialista de Tesla Electricidad confirmará tu cita en menos de 2 horas.

**Gracias por confiar en nosotros** ⚡

¿Necesitas información sobre otro servicio?`,
                  'bot',
                  true,
                  'services'
                );
              });
            }}
            style={{
              width: '100%',
              padding: '16px',
              background: '#25D366',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '15px',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px'
            }}
          >
            <Phone size={20} />
            Confirmar por WhatsApp
          </button>
        </div>
      );
    }

    return null;
  };

  return (
    <div style={{
      width: '100%',
      maxWidth: '450px',
      height: '700px',
      margin: '0 auto',
      background: 'white',
      borderRadius: '16px',
      boxShadow: '0 8px 32px rgba(139, 0, 0, 0.2)',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden',
      border: `3px solid ${colors.primary}`
    }}>
      {/* Header */}
      <div style={{
        background: `linear-gradient(135deg, ${colors.primary}, ${colors.fire})`,
        padding: '20px',
        color: 'white',
        display: 'flex',
        alignItems: 'center',
        gap: '12px'
      }}>
        <div style={{
          width: '50px',
          height: '50px',
          background: 'white',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '24px'
        }}>
          ⚡
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: '18px', fontWeight: 'bold' }}>Pili - Tesla IA</div>
          <div style={{ fontSize: '12px', opacity: 0.9 }}>Especialista Eléctrico • En línea</div>
        </div>
        <Zap size={24} color={colors.secondary} />
      </div>

      {/* Messages */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '20px',
        background: `linear-gradient(to bottom, ${colors.light}, white)`
      }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{
            display: 'flex',
            justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
            marginBottom: '16px',
            animation: 'slideIn 0.3s ease'
          }}>
            <div style={{
              maxWidth: '85%',
              padding: '12px 16px',
              borderRadius: msg.sender === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
              background: msg.sender === 'user' 
                ? `linear-gradient(135deg, ${colors.secondary}, #FFA500)`
                : 'white',
              color: msg.sender === 'user' ? colors.dark : '#333',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              fontWeight: msg.sender === 'user' ? '600' : '400',
              fontSize: '14px',
              lineHeight: '1.5'
            }}>
              <div dangerouslySetInnerHTML={{ 
                __html: msg.text
                  .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                  .replace(/_(.*?)_/g, '<em style="opacity: 0.8;">$1</em>')
                  .replace(/\n/g, '<br/>')
              }} />
              <QuickButtons message={msg} />
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '12px 16px',
            background: 'white',
            borderRadius: '16px',
            width: 'fit-content',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
          }}>
            <span style={{ fontSize: '14px' }}>Pili está escribiendo</span>
            <div style={{ display: 'flex', gap: '4px' }}>
              {[0, 1, 2].map((i) => (
                <div
                  key={i}
                  style={{
                    width: '8px',
                    height: '8px',
                    background: colors.primary,
                    borderRadius: '50%',
                    animation: `bounce 1.4s infinite ${i * 0.2}s`
                  }}
                />
              ))}
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div style={{
        padding: '16px',
        background: 'white',
        borderTop: `2px solid ${colors.light}`,
        display: 'flex',
        gap: '8px'
      }}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Escribe tu respuesta..."
          style={{
            flex: 1,
            padding: '12px 16px',
            border: `2px solid ${colors.light}`,
            borderRadius: '24px',
            outline: 'none',
            fontSize: '14px'
          }}
        />
        <button
          onClick={handleSendMessage}
          style={{
            width: '48px',
            height: '48px',
            background: `linear-gradient(135deg, ${colors.primary}, ${colors.fire})`,
            border: 'none',
            borderRadius: '50%',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'transform 0.2s'
          }}
          onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
          onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
        >
          <Send size={20} color="white" />
        </button>
      </div>

      <style>{`
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        @keyframes bounce {
          0%, 80%, 100% {
            transform: scale(0);
          }
          40% {
            transform: scale(1);
          }
        }
      `}</style>
    </div>
  );
};

export default PiliChatbot;