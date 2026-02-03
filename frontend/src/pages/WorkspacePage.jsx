import React, { useState } from 'react';
import { ThemeProvider } from '../context/ThemeContext';
import ThreePanelLayout from '../components/ThreePanelLayout';
import WorkspaceHeader from '../components/workspace/WorkspaceHeader';
import NavigationPanel from '../components/workspace/NavigationPanel';
import WorkArea from '../components/workspace/WorkArea';
import AIAssistant from '../components/workspace/AIAssistant';

/**
 * WorkspacePage - Página principal del Workspace
 * 
 * Nueva interfaz moderna con layout de 3 paneles
 * Ruta: /workspace
 * 
 * IMPORTANTE: Esta es una capa NUEVA, no reemplaza nada existente
 */
const WorkspacePage = () => {
    const [activeSection, setActiveSection] = useState('proyectos');

    return (
        <ThemeProvider>
            <div className="h-screen flex flex-col bg-gradient-to-br from-gray-950 via-red-950 to-black dark:from-gray-950 dark:via-red-950 dark:to-black light:from-gray-100 light:via-gray-200 light:to-gray-300">
                {/* Header */}
                <WorkspaceHeader />

                {/* Three Panel Layout */}
                <div className="flex-1 overflow-hidden">
                    <ThreePanelLayout
                        leftPanel={
                            <NavigationPanel
                                activeSection={activeSection}
                                onSectionChange={setActiveSection}
                            />
                        }
                        centerPanel={
                            <WorkArea activeSection={activeSection} />
                        }
                        rightPanel={
                            <AIAssistant context={{ section: activeSection }} />
                        }
                    />
                </div>
            </div>
        </ThemeProvider>
    );
};

export default WorkspacePage;
