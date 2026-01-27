import React, { useState, useEffect } from 'react';
import { Table, CheckSquare, Save, Info, Users, RotateCcw } from 'lucide-react';

const FormularioRACIPro = ({ onSubmit, complejidad = 7 }) => {
    // Roles estándar
    const roles = [
        { id: 'PM', label: 'PM', full: 'Project Manager' },
        { id: 'Residente', label: 'Ing. Res', full: 'Ingeniero Residente' },
        { id: 'Tecnicos', label: 'Técnicos', full: 'Equipo Técnico' },
        { id: 'QA', label: 'Insp. QA', full: 'Inspector de Calidad/Seguridad' },
        { id: 'Cliente', label: 'Cliente', full: 'Cliente / Supervisor' }
    ];

    // Actividades según complejidad
    const getActividadesBase = (nivel) => {
        const base = [
            { id: 1, nombre: 'Planificación del Proyecto' },
            { id: 2, nombre: 'Diseño e Ingeniería' },
            { id: 3, nombre: 'Ejecución de Obra' },
            { id: 4, nombre: 'Control de Calidad' },
            { id: 5, nombre: 'Aprobación de Entregables' }
        ];

        if (nivel >= 7) {
            return [
                ...base,
                { id: 6, nombre: 'Gestión de Riesgos' },
                { id: 7, nombre: 'Cierre Administrativo' }
            ];
        }
        return base;
    };

    const [matriz, setMatriz] = useState([]);

    // Inicializar matriz vacía
    useEffect(() => {
        const actividades = getActividadesBase(complejidad);
        const inicial = actividades.map(act => {
            const row = { id: act.id, actividad: act.nombre };
            roles.forEach(rol => row[rol.id] = null); // null, 'R', 'A', 'C', 'I'
            return row;
        });

        // Precargar algunos valores lógicos por defecto
        if (inicial.length > 0) {
            inicial[0]['PM'] = 'A'; inicial[0]['Residente'] = 'R'; inicial[0]['Cliente'] = 'C';
            inicial[2]['Residente'] = 'A'; inicial[2]['Tecnicos'] = 'R';
        }

        setMatriz(inicial);
    }, [complejidad]);

    const setRol = (actividadId, rolId, tipo) => {
        setMatriz(matriz.map(row =>
            row.id === actividadId ? { ...row, [rolId]: tipo } : row
        ));
    };

    const getCeldaClass = (tipo) => {
        switch (tipo) {
            case 'R': return 'bg-blue-600 text-white shadow-blue-500/50 scale-105'; // Responsible
            case 'A': return 'bg-red-600 text-white shadow-red-500/50 scale-105';  // Accountable
            case 'C': return 'bg-yellow-500 text-black shadow-yellow-500/50 scale-105'; // Consulted
            case 'I': return 'bg-green-600 text-white shadow-green-500/50 scale-105'; // Informed
            default: return 'bg-gray-800/50 text-gray-600 hover:bg-gray-700 hover:text-gray-400';
        }
    };

    const ciclos = ['R', 'A', 'C', 'I', null];

    const handleClickCelda = (actividadId, rolId) => {
        const fila = matriz.find(r => r.id === actividadId);
        const actual = fila[rolId];
        const nextIndex = (ciclos.indexOf(actual) + 1) % ciclos.length;
        setRol(actividadId, rolId, ciclos[nextIndex]);
    };

    const handleSubmit = () => {
        const raciFinal = matriz.map(row => ({
            actividad: row.actividad,
            roles: roles.map(r => row[r.id] || '-')
        }));
        onSubmit(raciFinal);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-950 via-red-950 to-black text-white p-6 animate-fadeIn">
            <div className="max-w-6xl mx-auto space-y-8 pb-32">

                {/* HEADER */}
                <div className="bg-gradient-to-r from-red-950 via-red-900 to-black p-6 rounded-2xl border-2 border-yellow-600 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-4">
                    <div>
                        <h1 className="text-3xl font-bold text-yellow-500 flex items-center gap-3">
                            <Table className="w-8 h-8" />
                            Matriz RACI - Roles
                        </h1>
                        <p className="text-gray-400 mt-1">Responsible, Accountable, Consulted, Informed</p>
                    </div>

                    {/* Leyenda Compacta */}
                    <div className="flex bg-black/40 p-2 rounded-xl border border-gray-800 gap-3">
                        <div className="flex items-center gap-2 px-3 py-1 bg-red-900/40 rounded border border-red-500/30">
                            <span className="font-bold text-red-400">A</span>
                            <span className="text-[10px] text-gray-400 uppercase">Aprobador</span>
                        </div>
                        <div className="flex items-center gap-2 px-3 py-1 bg-blue-900/40 rounded border border-blue-500/30">
                            <span className="font-bold text-blue-400">R</span>
                            <span className="text-[10px] text-gray-400 uppercase">Responsable</span>
                        </div>
                        <div className="flex items-center gap-2 px-3 py-1 bg-yellow-900/40 rounded border border-yellow-500/30">
                            <span className="font-bold text-yellow-400">C</span>
                            <span className="text-[10px] text-gray-400 uppercase">Consultado</span>
                        </div>
                        <div className="flex items-center gap-2 px-3 py-1 bg-green-900/40 rounded border border-green-500/30">
                            <span className="font-bold text-green-400">I</span>
                            <span className="text-[10px] text-gray-400 uppercase">Informado</span>
                        </div>
                    </div>
                </div>

                {/* MATRIZ */}
                <div className="bg-black/40 backdrop-blur-md rounded-2xl border border-gray-800 shadow-xl overflow-hidden">
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left border-collapse">
                            <thead className="text-xs text-gray-400 uppercase bg-gray-900/80 border-b border-gray-700">
                                <tr>
                                    <th scope="col" className="px-6 py-4 sticky left-0 bg-gray-900 z-20 w-1/3 border-r border-gray-800">
                                        Actividad / Fase
                                    </th>
                                    {roles.map(rol => (
                                        <th key={rol.id} scope="col" className="px-2 py-4 text-center min-w-[100px] border-r border-gray-800/50 last:border-0" title={rol.full}>
                                            <div className="flex flex-col items-center gap-1">
                                                <Users className="w-4 h-4 opacity-50" />
                                                {rol.label}
                                            </div>
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-800">
                                {matriz.map((row) => (
                                    <tr key={row.id} className="hover:bg-white/5 transition-colors group">
                                        <td className="px-6 py-4 font-bold text-white sticky left-0 bg-gray-950/90 border-r border-gray-800 group-hover:bg-gray-900 z-10 shadow-[4px_0_10px_-2px_rgba(0,0,0,0.5)]">
                                            {row.actividad}
                                        </td>
                                        {roles.map(rol => (
                                            <td key={rol.id} className="p-2 text-center border-r border-gray-800/30 last:border-0 relative">
                                                <button
                                                    onClick={() => handleClickCelda(row.id, rol.id)}
                                                    className={`w-12 h-12 rounded-xl font-bold text-lg shadow-lg border border-transparent transition-all duration-200 hover:border-white/20 active:scale-95 mx-auto flex items-center justify-center ${getCeldaClass(row[rol.id])}`}
                                                >
                                                    {row[rol.id] || <span className="w-2 h-2 rounded-full bg-gray-700"></span>}
                                                </button>
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    <div className="p-4 bg-gray-900/50 border-t border-gray-800 flex items-center justify-center gap-2 text-xs text-gray-500">
                        <RotateCcw className="w-3 h-3" />
                        Tip: Haz clic en las celdas para rotar entre R - A - C - I
                    </div>
                </div>

                {/* FOOTER ACTIONS */}
                <div className="fixed bottom-0 left-0 right-0 p-4 bg-black/90 backdrop-blur-md border-t border-yellow-900/50 z-50 flex justify-end">
                    <button
                        onClick={handleSubmit}
                        className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:to-cyan-500 text-white px-8 py-3 rounded-xl font-bold shadow-lg shadow-blue-900/50 flex items-center gap-2 transition-transform hover:scale-105"
                    >
                        <Save className="w-5 h-5" />
                        Guardar Matriz RACI
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FormularioRACIPro;
