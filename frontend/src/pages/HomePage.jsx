import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePili } from '../context/PiliContext';
import PiliAvatar from '../components/PiliAvatar';
import { Upload, MessageSquare, FileText, X } from 'lucide-react';

const HomePage = () => {
    const navigate = useNavigate();
    const { servicios, industrias, datosCliente, actualizarCliente, datosEmpresa } = usePili();

    const [servicioSeleccionado, setServicioSeleccionado] = useState('');
    const [industriaSeleccionada, setIndustriaSeleccionada] = useState('');
    const [contextoUsuario, setContextoUsuario] = useState('');
    const [archivos, setArchivos] = useState([]);

    // Validación básica antes de navegar
    const puedeContinuar = servicioSeleccionado && industriaSeleccionada && contextoUsuario.trim();

    const handleComenzar = () => {
        if (!puedeContinuar) return;

        // Navegar a la página de chat con los parámetros
        // La URL será: /chat/electricidad?industria=mineria&contexto=...
        const params = new URLSearchParams({
            industria: industriaSeleccionada,
            contexto: contextoUsuario
        });

        navigate(`/chat/${servicioSeleccionado}?${params.toString()}`);
    };

    const handleFileUpload = (e) => {
        const files = Array.from(e.target.files);
        setArchivos(prev => [...prev, ...files]);
    };

    return (
        <div className="max-w-7xl mx-auto space-y-8 animate-fadeIn p-6">

            {/* HEADER */}
            <div className="text-center space-y-4 mb-8">
                <div className="inline-block relative">
                    <div className="absolute inset-0 bg-blue-500 blur-3xl opacity-20 rounded-full animate-pulse"></div>
                    <PiliAvatar size={48} showCrown={true} />
                </div>
                <h1 className="text-5xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-blue-200 to-blue-400 drop-shadow-lg">
                    {datosEmpresa.nombre.split(' ')[0]} <span className="text-yellow-400">PILI</span>
                </h1>
                <p className="text-xl text-blue-200 font-light">
                    Procesadora Inteligente de Licitaciones Industriales <span className="text-yellow-500 font-bold">v3.0</span>
                </p>
            </div>

            {/* TIPO DE SERVICIO */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-blue-900 shadow-xl">
                <h2 className="text-2xl font-bold mb-4 text-blue-400">⚙️ Tipo de Servicio</h2>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                    {servicios.map(servicio => (
                        <button
                            key={servicio.id}
                            onClick={() => setServicioSeleccionado(servicio.id)}
                            className={`p-4 rounded-xl border-2 transition-all duration-300 text-left group ${servicioSeleccionado === servicio.id
                                    ? 'border-yellow-500 bg-gradient-to-br from-blue-900 to-blue-800 text-white shadow-xl scale-105'
                                    : 'border-gray-800 bg-gray-900/50 hover:border-yellow-600 hover:bg-gray-800'
                                }`}>
                            <div className="text-2xl mb-2 group-hover:scale-110 transition-transform">{servicio.icon}</div>
                            <div className="text-sm font-semibold">{servicio.nombre.split(' ').slice(1).join(' ')}</div>
                        </button>
                    ))}
                </div>
            </div>

            {/* INDUSTRIA */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-blue-900 shadow-xl">
                <h2 className="text-2xl font-bold mb-4 text-blue-400">🏢 Industria</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {industrias.map(industria => (
                        <button
                            key={industria.id}
                            onClick={() => setIndustriaSeleccionada(industria.id)}
                            className={`p-3 rounded-xl border-2 transition-all duration-300 ${industriaSeleccionada === industria.id
                                    ? 'border-yellow-500 bg-gradient-to-br from-blue-900 to-blue-800 text-white shadow-xl'
                                    : 'border-gray-800 bg-gray-900/50 hover:border-yellow-600 hover:bg-gray-800'
                                }`}>
                            <div className="text-sm font-semibold">{industria.nombre}</div>
                        </button>
                    ))}
                </div>
            </div>

            {/* DESCRIPCIÓN */}
            <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border-2 border-blue-900 shadow-xl">
                <h2 className="text-2xl font-bold mb-4 text-blue-400">📝 Descripción del Requerimiento</h2>

                <textarea
                    value={contextoUsuario}
                    onChange={(e) => setContextoUsuario(e.target.value)}
                    className="w-full h-32 px-4 py-3 bg-gray-950 border border-blue-800 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:outline-none resize-none mb-4 text-white placeholder-gray-600"
                    placeholder="Describe detalladamente qué necesitas cotizar o proyectar..."
                />

                {/* UPLOAD DE DOCUMENTOS */}
                <div className="border-t-2 border-gray-800 pt-4">
                    <div className="border-2 border-dashed border-gray-800 rounded-xl p-6 text-center hover:border-yellow-600 transition-all cursor-pointer mb-4 bg-gray-950/30">
                        <input type="file" multiple onChange={handleFileUpload} className="hidden" id="fileInput" accept=".pdf,.docx,.xlsx,.txt" />
                        <label htmlFor="fileInput" className="cursor-pointer">
                            <Upload className="w-10 h-10 mx-auto mb-3 text-yellow-600" />
                            <p className="text-sm text-gray-400 font-semibold">Adjuntar planos o TDR (Opcional)</p>
                        </label>
                    </div>

                    {archivos.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                            {archivos.map((file, i) => (
                                <div key={i} className="bg-blue-900/40 px-3 py-1 rounded-full text-xs text-blue-200 flex items-center gap-2 border border-blue-800">
                                    <FileText size={12} /> {file.name}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* BOTÓN CONTINUAR */}
            <button
                onClick={handleComenzar}
                disabled={!puedeContinuar}
                className="w-full bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 disabled:from-gray-800 disabled:to-gray-700 disabled:cursor-not-allowed py-4 rounded-xl font-bold text-lg text-black shadow-2xl border-2 border-yellow-400 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-3">
                <MessageSquare className="w-6 h-6" />
                Iniciar Asistente Inteligente
            </button>

            <div className="text-center text-gray-600 text-xs mt-8 pb-8">
                Desarrollado por GatoMichuy para Tesla Electricidad S.A.C. © 2025
            </div>
        </div>
    );
};

export default HomePage;
