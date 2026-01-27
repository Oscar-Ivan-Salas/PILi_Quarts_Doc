import React, { useState, useRef, forwardRef, useImperativeHandle } from 'react';
import { FileText } from 'lucide-react';

// ✅ IMPORTAR COMPONENTES EDITABLE
import EDITABLE_COTIZACION_COMPLEJA from './EDITABLE_COTIZACION_COMPLEJA';
import EDITABLE_COTIZACION_SIMPLE from './EDITABLE_COTIZACION_SIMPLE';
import EDITABLE_PROYECTO_SIMPLE from './EDITABLE_PROYECTO_SIMPLE';
import EDITABLE_PROYECTO_COMPLEJO from './EDITABLE_PROYECTO_COMPLEJO';
import EDITABLE_INFORME_TECNICO from './EDITABLE_INFORME_TECNICO';
import EDITABLE_INFORME_EJECUTIVO from './EDITABLE_INFORME_EJECUTIVO';



/**
 * VistaPreviaProfesional - Componente que renderiza SOLO componentes EDITABLE
 * SIN HTML inline - 100% componentes reutilizables
 */
const VistaPreviaProfesional = forwardRef((props, ref) => {
  const {
    cotizacion,
    proyecto,
    informe,
    onGenerarDocumento,
    tipoDocumento = 'cotizacion',
    htmlPreview = '',
    esquemaColores = 'azul-tesla',
    logoBase64 = null,
    fuenteDocumento = 'Calibri',
    ocultarIGV = false,
    ocultarPreciosUnitarios = false,
    ocultarTotalesPorItem = false,

    onDatosChange, // ✨ NUEVO: Callback del padre
    modoEdicion = true // Default true para compatibilidad si no se pasa
  } = props;



  // Estado editable de la cotizacion/proyecto/informe
  const [datosEditables, setDatosEditables] = useState(cotizacion || proyecto || informe || {});
  const documentoRef = useRef(null);

  // ✅ SINCRONIZACIÓN: Actualizar cuando cambien los datos del chat
  // ⚠️ CRÍTICO: Prevenir loop infinito comparando datos
  React.useEffect(() => {
    const nuevosDatos = cotizacion || proyecto || informe;
    if (nuevosDatos && JSON.stringify(nuevosDatos) !== JSON.stringify(datosEditables)) {

      setDatosEditables(nuevosDatos);
    }
  }, [cotizacion, proyecto, informe]); // NO incluir datosEditables aquí

  // Callback para recibir cambios del componente EDITABLE
  const handleDatosChange = (nuevosDatos) => {

    setDatosEditables(nuevosDatos);

    // ✨ NUEVO: Notificar al padre (App.jsx) de los cambios
    if (onDatosChange) {
      onDatosChange(nuevosDatos);
    }
  };

  // Exponer métodos al componente padre
  useImperativeHandle(ref, () => ({
    getEditedHTML: () => {
      return documentoRef.current ? documentoRef.current.innerHTML : '';
    },
    getEditedData: () => datosEditables
  }));

  // ✅ RENDERIZAR COMPONENTE EDITABLE SEGÚN TIPO DE DOCUMENTO
  const renderComponenteEditable = () => {


    // COTIZACIÓN COMPLEJA
    if (tipoDocumento === 'cotizacion-compleja' || tipoDocumento === 'cotizacion') {

      return (
        <EDITABLE_COTIZACION_COMPLEJA
          datos={datosEditables}
          esquemaColores={esquemaColores}
          logoBase64={logoBase64}
          fuenteDocumento={fuenteDocumento}
          onDatosChange={handleDatosChange}
          ocultarIGV={ocultarIGV}
          ocultarPreciosUnitarios={ocultarPreciosUnitarios}

          ocultarTotalesPorItem={ocultarTotalesPorItem}
          modoEdicion={modoEdicion}
        />
      );
    }

    // COTIZACIÓN SIMPLE
    if (tipoDocumento === 'cotizacion-simple') {

      return (
        <EDITABLE_COTIZACION_SIMPLE
          datos={datosEditables}
          esquemaColores={esquemaColores}
          logoBase64={logoBase64}
          fuenteDocumento={fuenteDocumento}
          onDatosChange={handleDatosChange}
          ocultarPreciosUnitarios={ocultarPreciosUnitarios}
          ocultarTotalesPorItem={ocultarTotalesPorItem}
          modoEdicion={modoEdicion}
        />
      );
    }

    // PROYECTO SIMPLE
    if (tipoDocumento === 'proyecto-simple') {

      return (
        <EDITABLE_PROYECTO_SIMPLE
          datos={datosEditables}
          esquemaColores={esquemaColores}
          logoBase64={logoBase64}
          fuenteDocumento={fuenteDocumento}
          onDatosChange={handleDatosChange}
          modoEdicion={modoEdicion}
        />
      );
    }

    // PROYECTO COMPLEJO
    if (tipoDocumento === 'proyecto-complejo') {

      return (
        <EDITABLE_PROYECTO_COMPLEJO
          datos={datosEditables}
          esquemaColores={esquemaColores}
          logoBase64={logoBase64}
          fuenteDocumento={fuenteDocumento}
          onDatosChange={handleDatosChange}
          modoEdicion={modoEdicion}
        />
      );
    }


    // INFORME TÉCNICO (también responde a informe-simple)
    if (tipoDocumento === 'informe-tecnico' || tipoDocumento === 'informe-simple') {

      return (
        <EDITABLE_INFORME_TECNICO
          datos={datosEditables}
          esquemaColores={esquemaColores}
          logoBase64={logoBase64}
          fuenteDocumento={fuenteDocumento}
          onDatosChange={handleDatosChange}
          modoEdicion={modoEdicion}
        />
      );
    }

    // INFORME EJECUTIVO
    if (tipoDocumento === 'informe-ejecutivo') {

      return (
        <EDITABLE_INFORME_EJECUTIVO
          datos={datosEditables}
          esquemaColores={esquemaColores}
          logoBase64={logoBase64}
          fuenteDocumento={fuenteDocumento}
          onDatosChange={handleDatosChange}
          modoEdicion={modoEdicion}
        />
      );
    }

    // Tipo desconocido

    return (
      <div style={{ padding: '40px', textAlign: 'center', background: '#FEF2F2', borderRadius: '8px', border: '2px dashed #DC2626' }}>
        <FileText size={48} style={{ color: '#DC2626', margin: '0 auto 20px' }} />
        <h3 style={{ color: '#DC2626', marginBottom: '10px' }}>Tipo de Documento Desconocido</h3>
        <p style={{ color: '#7F1D1D' }}>Tipo: {tipoDocumento}</p>
      </div>
    );
  };

  return (
    <div className="vista-previa-container overflow-y-auto" style={{ width: '100%', height: '100%', maxHeight: '100vh' }}>
      {/* DOCUMENTO PROFESIONAL */}
      <div className="cotizacion-profesional" ref={documentoRef} style={{
        background: 'white',
        minHeight: '100vh',
        padding: '0'
      }}>
        {/* ✅ RENDERIZAR SOLO COMPONENTE EDITABLE - SIN HTML INLINE */}
        {renderComponenteEditable()}
      </div>
    </div>
  );
});

VistaPreviaProfesional.displayName = 'VistaPreviaProfesional';

export default VistaPreviaProfesional;
