import React from 'react';

/**
 * 👑 PILI Avatar - La cara bonita del proyecto
 *
 * Avatar de PILI (Procesadora Inteligente de Licitaciones Industriales)
 * con su imagen personalizada de Caperucita
 */
const PiliAvatar = ({ size = 24, className = "", showCrown = true }) => {
  const containerSize = size + 8;

  return (
    <div
      className={`relative inline-flex items-center justify-center ${className}`}
      style={{ width: containerSize, height: containerSize }}
    >
      {/* Corona sobre PILI */}
      {showCrown && (
        <div
          className="absolute -top-1 left-1/2 transform -translate-x-1/2 z-10"
          style={{
            fontSize: size * 0.5,
            filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.3))'
          }}
        >
          👑
        </div>
      )}

      {/* Avatar de PILI Caperucita */}
      <div className="relative rounded-full overflow-hidden" style={{ width: size, height: size }}>
        <img
          src="http://localhost:8000/static/avatars/pili.png"
          alt="PILI"
          className="w-full h-full object-cover"
          style={{ imageRendering: 'crisp-edges' }}
        />

        {/* Brillo especial */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: 'radial-gradient(circle at 40% 40%, rgba(255,215,0,0.2) 0%, transparent 60%)'
          }}
        />
      </div>
    </div>
  );
};

/**
 * Variantes del Avatar de PILI para diferentes contextos
 */
export const PiliAvatarLarge = ({ showCrown = true }) => (
  <div className="relative inline-block">
    {showCrown && (
      <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 z-20 text-4xl animate-bounce filter drop-shadow-lg">
        👑
      </div>
    )}
    <div className="bg-gradient-to-br from-red-400 via-red-500 to-red-600 p-0.5 rounded-full shadow-2xl border border-red-300 relative overflow-hidden transition-transform transform hover:scale-105">
      <div className="w-20 h-20 rounded-full overflow-hidden relative z-10 bg-white">
        <img
          src="http://localhost:8000/static/avatars/pili.png"
          alt="PILI"
          className="w-full h-full object-cover object-top"
          style={{ objectPosition: 'center 10%' }}
        />
      </div>

      {/* Efecto de brillo animado */}
      <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white to-transparent opacity-30 animate-pulse" />

      {/* Partículas doradas */}
      <div className="absolute inset-0">
        <div className="absolute top-2 right-2 w-1 h-1 bg-yellow-200 rounded-full animate-ping" />
        <div className="absolute bottom-3 left-3 w-1 h-1 bg-yellow-200 rounded-full animate-ping" style={{ animationDelay: '0.5s' }} />
        <div className="absolute top-1/2 right-1 w-1 h-1 bg-yellow-200 rounded-full animate-ping" style={{ animationDelay: '1s' }} />
      </div>
    </div>
  </div>
);

/**
 * Badge de PILI con nombre
 */
export const PiliBadge = ({ nombre = "PILI", variant = "default" }) => {
  const variants = {
    default: "bg-yellow-600 text-black",
    cotizadora: "bg-yellow-600 text-black",
    analista: "bg-blue-600 text-white",
    coordinadora: "bg-green-600 text-white",
    projectManager: "bg-purple-600 text-white",
    reportera: "bg-indigo-600 text-white",
    analistaSenior: "bg-red-600 text-white"
  };

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full ${variants[variant]} font-bold text-sm shadow-lg border-2 border-opacity-50 border-white`}>
      <PiliAvatar size={16} showCrown={true} />
      <span>{nombre}</span>
      <span className="text-xs opacity-75">IA</span>
    </div>
  );
};

/**
 * Estado de PILI (pensando, escribiendo, etc.)
 */
export const PiliStatus = ({ status = "active" }) => {
  const statusConfig = {
    active: { text: "Lista para ayudar", color: "bg-green-500", icon: "✨" },
    thinking: { text: "Pensando...", color: "bg-yellow-500", icon: "🤔" },
    analyzing: { text: "Analizando...", color: "bg-blue-500", icon: "🔍" },
    generating: { text: "Generando documento...", color: "bg-purple-500", icon: "📄" },
    offline: { text: "Modo offline", color: "bg-gray-500", icon: "💤" }
  };

  const config = statusConfig[status] || statusConfig.active;

  return (
    <div className="flex items-center gap-2">
      <PiliAvatar size={20} showCrown={true} />
      <div className="flex items-center gap-2">
        <div className={`w-2 h-2 ${config.color} rounded-full animate-pulse`} />
        <span className="text-sm text-gray-300 font-medium">
          {config.icon} {config.text}
        </span>
      </div>
    </div>
  );
};

export default PiliAvatar;
