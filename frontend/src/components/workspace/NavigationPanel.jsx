import React, { useState } from 'react';
import { FileText, ChevronRight, Zap, FileCheck, BarChart3 } from 'lucide-react';
import ProfessionalFooter from './ProfessionalFooter';

/**
 * NavigationPanel - Panel de navegación mejorado
 * 
 * Muestra secciones con submenús para Simple/Complejo
 */
const NavigationPanel = ({ activeSection, onSectionChange }) => {
    const [expandedSection, setExpandedSection] = useState(null);

    const sections = [
        {
            id: 'proyectos',
            icon: FileText,
            label: 'Proyectos',
            badge: 5,
            color: 'text-blue-400',
            subsections: [
                { id: 'proyectos-simple', label: 'Proyecto Simple', count: 3 },
                { id: 'proyectos-complejo', label: 'Proyecto Complejo (PMI)', count: 2 }
            ]
        },
        {
            id: 'cotizaciones',
            icon: FileCheck,
            label: 'Cotizaciones',
            badge: 13,
            color: 'text-green-400',
            subsections: [
                { id: 'cotizaciones-simple', label: 'Cotización Simple', count: 10 },
                { id: 'cotizaciones-compleja', label: 'Cotización Compleja', count: 3 }
            ]
        },
        {
            id: 'informes',
            icon: BarChart3,
            label: 'Informes',
            badge: 2,
            color: 'text-purple-400',
            subsections: [
                { id: 'informes-tecnico', label: 'Informe Técnico', count: 1 },
                { id: 'informes-ejecutivo', label: 'Informe Ejecutivo', count: 1 }
            ]
        }
    ];

    const handleSectionClick = (sectionId) => {
        if (expandedSection === sectionId) {
            setExpandedSection(null);
        } else {
            setExpandedSection(sectionId);
        }
        onSectionChange(sectionId);
    };

    const handleSubsectionClick = (subsectionId) => {
        onSectionChange(subsectionId);
    };

    return (
        <div className="h-full bg-gray-900 dark:bg-gray-900 light:bg-white border-r-2 border-gray-800 dark:border-gray-800 light:border-gray-200 flex flex-col">
            {/* Header */}
            <div className="p-4 border-b-2 border-gray-800 dark:border-gray-800 light:border-gray-200">
                <h2 className="text-xl font-bold text-yellow-400 dark:text-yellow-400 light:text-yellow-600">
                    Navegación
                </h2>
            </div>

            {/* Sections */}
            <div className="flex-1 overflow-y-auto p-2">
                {sections.map((section) => {
                    const Icon = section.icon;
                    const isExpanded = expandedSection === section.id;
                    const isActive = activeSection === section.id || activeSection?.startsWith(section.id);

                    return (
                        <div key={section.id} className="mb-2">
                            {/* Main Section */}
                            <button
                                onClick={() => handleSectionClick(section.id)}
                                className={`
                  w-full flex items-center justify-between p-3 rounded-lg transition-all
                  ${isActive
                                        ? 'bg-red-600 text-white'
                                        : 'bg-gray-800 dark:bg-gray-800 light:bg-gray-100 text-gray-300 dark:text-gray-300 light:text-gray-700 hover:bg-gray-700 dark:hover:bg-gray-700 light:hover:bg-gray-200'
                                    }
                `}>
                                <div className="flex items-center gap-3">
                                    <Icon className={`w-5 h-5 ${isActive ? 'text-white' : section.color}`} />
                                    <span className="font-medium">{section.label}</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    {section.badge && (
                                        <span className={`
                      px-2 py-0.5 text-xs font-bold rounded-full
                      ${isActive
                                                ? 'bg-white text-red-600'
                                                : 'bg-yellow-400 dark:bg-yellow-400 light:bg-yellow-500 text-black'
                                            }
                    `}>
                                            {section.badge}
                                        </span>
                                    )}
                                    <ChevronRight
                                        className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
                                    />
                                </div>
                            </button>

                            {/* Subsections */}
                            {isExpanded && section.subsections && (
                                <div className="mt-1 ml-4 space-y-1">
                                    {section.subsections.map((subsection) => {
                                        const isSubActive = activeSection === subsection.id;
                                        return (
                                            <button
                                                key={subsection.id}
                                                onClick={() => handleSubsectionClick(subsection.id)}
                                                className={`
                          w-full flex items-center justify-between p-2 pl-4 rounded-lg text-sm transition-all
                          ${isSubActive
                                                        ? 'bg-red-500 text-white'
                                                        : 'bg-gray-800/50 dark:bg-gray-800/50 light:bg-gray-50 text-gray-400 dark:text-gray-400 light:text-gray-600 hover:bg-gray-700/50 dark:hover:bg-gray-700/50 light:hover:bg-gray-100'
                                                    }
                        `}>
                                                <span>{subsection.label}</span>
                                                <span className={`
                          px-1.5 py-0.5 text-xs rounded
                          ${isSubActive
                                                        ? 'bg-white text-red-600'
                                                        : 'bg-gray-700 dark:bg-gray-700 light:bg-gray-200 text-gray-300 dark:text-gray-300 light:text-gray-600'
                                                    }
                        `}>
                                                    {subsection.count}
                                                </span>
                                            </button>
                                        );
                                    })}
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>

            {/* New Button */}
            <div className="p-4 border-t-2 border-gray-800 dark:border-gray-800 light:border-gray-200">
                <button className="w-full px-4 py-3 bg-red-600 hover:bg-red-500 text-white rounded-lg font-bold transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2">
                    <Zap className="w-5 h-5" />
                    Nuevo
                </button>
            </div>

            {/* Footer Técnico Profesional */}
            <ProfessionalFooter version="v3.0.2" />
        </div>
    );
};

export default NavigationPanel;
