import React, { useEffect } from 'react';
import { CheckCircle, AlertCircle, Info, X, XCircle } from 'lucide-react';

const Alerta = ({ tipo = 'info', mensaje, visible, onCerrar, duracion = 5000 }) => {
  useEffect(() => {
    if (visible && duracion > 0) {
      const timer = setTimeout(() => {
        onCerrar();
      }, duracion);

      return () => clearTimeout(timer);
    }
  }, [visible, duracion, onCerrar]);

  if (!visible) return null;

  const configuraciones = {
    exito: {
      icono: CheckCircle,
      colorFondo: 'from-green-600 to-green-500',
      colorBorde: 'border-green-400',
      colorIcono: 'text-green-200'
    },
    error: {
      icono: XCircle,
      colorFondo: 'from-red-600 to-red-500',
      colorBorde: 'border-red-400',
      colorIcono: 'text-red-200'
    },
    advertencia: {
      icono: AlertCircle,
      colorFondo: 'from-yellow-600 to-yellow-500',
      colorBorde: 'border-yellow-400',
      colorIcono: 'text-yellow-200'
    },
    info: {
      icono: Info,
      colorFondo: 'from-blue-600 to-blue-500',
      colorBorde: 'border-blue-400',
      colorIcono: 'text-blue-200'
    }
  };

  const config = configuraciones[tipo] || configuraciones.info;
  const Icono = config.icono;

  return (
    <div className="fixed top-8 right-8 z-50 animate-slide-in-right">
      <div className={`bg-gradient-to-r ${config.colorFondo} border-2 ${config.colorBorde} rounded-xl shadow-2xl p-6 min-w-[400px] max-w-[500px]`}>
        <div className="flex items-start gap-4">
          <div className={`${config.colorIcono} mt-1`}>
            <Icono size={28} />
          </div>

          <div className="flex-1">
            <p className="text-white font-semibold text-lg leading-relaxed">
              {mensaje}
            </p>
          </div>

          <button
            onClick={onCerrar}
            className="text-white/80 hover:text-white transition-colors ml-2"
          >
            <X size={24} />
          </button>
        </div>

        {/* Barra de progreso */}
        {duracion > 0 && (
          <div className="mt-4 h-1 bg-white/20 rounded-full overflow-hidden">
            <div
              className="h-full bg-white/60 rounded-full animate-progress"
              style={{ animationDuration: `${duracion}ms` }}
            />
          </div>
        )}
      </div>
    </div>
  );
};

// Estilos CSS deben estar en index.css

export default Alerta;