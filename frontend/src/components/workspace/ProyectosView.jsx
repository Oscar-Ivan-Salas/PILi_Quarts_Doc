import React from 'react';
import { Plus, Search, Filter } from 'lucide-react';
import ProyectoCard from './ProyectoCard';

/**
 * ProyectosView - Vista de proyectos
 * 
 * Muestra grid de proyectos con filtros y búsqueda
 */
const ProyectosView = () => {
    // Datos de ejemplo
    const proyectos = [
        {
            id: 1,
            nombre: 'Instalación Eléctrica Industrial',
            descripcion: 'Proyecto de instalación eléctrica completa para planta industrial de 5000m²',
            estado: 'activo',
            fecha: '15 Ene 2026',
            presupuesto: 'S/ 150,000'
        },
        {
            id: 2,
            nombre: 'Sistema Contra Incendios',
            descripcion: 'Implementación de sistema contra incendios en edificio comercial',
            estado: 'pendiente',
            fecha: '20 Ene 2026',
            presupuesto: 'S/ 85,000'
        },
        {
            id: 3,
            nombre: 'Automatización Industrial',
            descripcion: 'Automatización de línea de producción con PLC Siemens',
            estado: 'completado',
            fecha: '10 Ene 2026',
            presupuesto: 'S/ 200,000'
        },
        {
            id: 4,
            nombre: 'Red de Datos Empresarial',
            descripcion: 'Instalación de red estructurada Cat6A para oficinas corporativas',
            estado: 'activo',
            fecha: '18 Ene 2026',
            presupuesto: 'S/ 45,000'
        },
        {
            id: 5,
            nombre: 'Sistema CCTV',
            descripcion: 'Instalación de 50 cámaras IP con grabación en la nube',
            estado: 'activo',
            fecha: '22 Ene 2026',
            presupuesto: 'S/ 65,000'
        },
        {
            id: 6,
            nombre: 'Domótica Residencial',
            descripcion: 'Sistema de automatización completo para residencia de lujo',
            estado: 'pendiente',
            fecha: '25 Ene 2026',
            presupuesto: 'S/ 120,000'
        }
    ];

    return (
        <div className="p-6 h-full overflow-y-auto bg-gray-50 dark:bg-gray-950 light:bg-gray-50">
            {/* Header */}
            <div className="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                    <h2 className="text-3xl font-bold text-gray-800 dark:text-white light:text-gray-800">Mis Proyectos</h2>
                    <p className="text-sm text-gray-600 dark:text-gray-400 light:text-gray-600 mt-1">
                        Gestiona todos tus proyectos en un solo lugar
                    </p>
                </div>
                <button className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg font-medium transition-all shadow-md hover:shadow-lg flex items-center gap-2">
                    <Plus className="w-4 h-4" />
                    Nuevo Proyecto
                </button>
            </div>

            {/* Filtros y Búsqueda */}
            <div className="mb-6 flex flex-col sm:flex-row gap-4">
                <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Buscar proyectos..."
                        className="w-full pl-10 pr-4 py-2 border-2 border-gray-300 dark:border-gray-700 light:border-gray-300 rounded-lg focus:border-red-600 focus:outline-none bg-white dark:bg-gray-800 light:bg-white text-gray-800 dark:text-white light:text-gray-800"
                    />
                </div>
                <button className="px-4 py-2 border-2 border-gray-300 dark:border-gray-700 light:border-gray-300 rounded-lg hover:border-red-600 transition-all flex items-center gap-2 bg-white dark:bg-gray-800 light:bg-white text-gray-800 dark:text-white light:text-gray-800">
                    <Filter className="w-4 h-4" />
                    Filtrar
                </button>
            </div>

            {/* Grid de Proyectos */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {proyectos.map(proyecto => (
                    <ProyectoCard
                        key={proyecto.id}
                        proyecto={proyecto}
                        onClick={() => console.log('Proyecto seleccionado:', proyecto.id)}
                    />
                ))}
            </div>
        </div>
    );
};

export default ProyectosView;
