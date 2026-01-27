import React, { useState, useCallback } from 'react';
import { Upload, File, X, CheckCircle, Loader, AlertCircle } from 'lucide-react';

const UploadZone = ({ onArchivosSubidos }) => {
  const [archivos, setArchivos] = useState([]);
  const [arrastrando, setArrastrando] = useState(false);
  const [subiendo, setSubiendo] = useState(false);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragIn = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setArrastrando(true);
    }
  }, []);

  const handleDragOut = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setArrastrando(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setArrastrando(false);

    const files = Array.from(e.dataTransfer.files);
    procesarArchivos(files);
  }, []);

  const handleFileInput = (e) => {
    const files = Array.from(e.target.files);
    procesarArchivos(files);
  };

  const procesarArchivos = async (files) => {
    const nuevosArchivos = files.map(file => ({
      file,
      nombre: file.name,
      tamano: (file.size / 1024).toFixed(2) + ' KB',
      tipo: file.type,
      estado: 'pendiente',
      progreso: 0,
      id: Math.random().toString(36).substr(2, 9)
    }));

    setArchivos(prev => [...prev, ...nuevosArchivos]);

    // Subir archivos al backend
    for (const archivoData of nuevosArchivos) {
      await subirArchivo(archivoData);
    }
  };

  const subirArchivo = async (archivoData) => {
    setSubiendo(true);
    
    // Actualizar estado a "subiendo"
    setArchivos(prev => prev.map(a => 
      a.id === archivoData.id ? { ...a, estado: 'subiendo', progreso: 0 } : a
    ));

    const formData = new FormData();
    formData.append('file', archivoData.file);

    try {
      const response = await fetch('http://localhost:8000/api/documentos/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        
        setArchivos(prev => prev.map(a => 
          a.id === archivoData.id 
            ? { ...a, estado: 'completado', progreso: 100, contenidoExtraido: data.contenido }
            : a
        ));

        // Notificar al padre
        if (onArchivosSubidos) {
          onArchivosSubidos(data);
        }
      } else {
        throw new Error('Error al subir archivo');
      }
    } catch (error) {
      console.error('Error:', error);
      setArchivos(prev => prev.map(a => 
        a.id === archivoData.id ? { ...a, estado: 'error', progreso: 0 } : a
      ));
    } finally {
      setSubiendo(false);
    }
  };

  const eliminarArchivo = (id) => {
    setArchivos(prev => prev.filter(a => a.id !== id));
  };

  const obtenerIconoEstado = (estado) => {
    switch (estado) {
      case 'completado':
        return <CheckCircle className="text-green-500" size={20} />;
      case 'error':
        return <AlertCircle className="text-red-500" size={20} />;
      case 'subiendo':
        return <Loader className="text-yellow-400 animate-spin" size={20} />;
      default:
        return <File className="text-gray-400" size={20} />;
    }
  };

  return (
    <div className="space-y-4">
      {/* Zona de arrastre */}
      <div
        onDragEnter={handleDragIn}
        onDragLeave={handleDragOut}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`border-4 border-dashed rounded-2xl p-12 text-center transition-all ${
          arrastrando
            ? 'border-yellow-400 bg-yellow-900/20 scale-105'
            : 'border-gray-600 bg-gray-800/50 hover:border-yellow-600'
        }`}
      >
        <input
          type="file"
          multiple
          onChange={handleFileInput}
          className="hidden"
          id="file-upload"
          accept=".pdf,.doc,.docx,.xls,.xlsx,.txt,.jpg,.jpeg,.png"
        />
        
        <label htmlFor="file-upload" className="cursor-pointer">
          <div className="flex flex-col items-center gap-4">
            <div className={`p-6 rounded-full ${arrastrando ? 'bg-yellow-600' : 'bg-gray-700'} transition-all`}>
              <Upload size={48} className={arrastrando ? 'text-black' : 'text-yellow-400'} />
            </div>
            
            <div>
              <p className="text-xl font-bold text-white mb-2">
                {arrastrando ? '¡Suelta los archivos aquí!' : 'Arrastra archivos o haz clic'}
              </p>
              <p className="text-gray-400">
                PDF, Word, Excel, imágenes, textos
              </p>
              <p className="text-sm text-gray-500 mt-2">
                La IA extraerá información automáticamente
              </p>
            </div>
          </div>
        </label>
      </div>

      {/* Lista de archivos */}
      {archivos.length > 0 && (
        <div className="bg-gray-900 rounded-2xl p-6 border-2 border-gray-700">
          <h3 className="text-yellow-400 font-bold text-lg mb-4">
            Archivos ({archivos.length})
          </h3>
          
          <div className="space-y-3">
            {archivos.map((archivo) => (
              <div
                key={archivo.id}
                className="bg-gray-800 rounded-xl p-4 flex items-center gap-4 border-2 border-gray-700"
              >
                {obtenerIconoEstado(archivo.estado)}
                
                <div className="flex-1">
                  <p className="text-white font-semibold">{archivo.nombre}</p>
                  <p className="text-gray-400 text-sm">{archivo.tamano}</p>
                  
                  {archivo.estado === 'subiendo' && (
                    <div className="mt-2 bg-gray-700 rounded-full h-2 overflow-hidden">
                      <div
                        className="bg-yellow-400 h-full transition-all duration-300"
                        style={{ width: `${archivo.progreso}%` }}
                      />
                    </div>
                  )}
                </div>

                <button
                  onClick={() => eliminarArchivo(archivo.id)}
                  className="text-red-500 hover:text-red-400 transition-colors"
                  disabled={archivo.estado === 'subiendo'}
                >
                  <X size={20} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadZone;