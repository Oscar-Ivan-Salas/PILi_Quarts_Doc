import React from 'react';
import { Moon, Sun, Monitor } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

/**
 * ThemeToggle - Selector de tema (Oscuro / Claro / Sistema)
 * 
 * Permite al usuario cambiar entre:
 * - Modo oscuro
 * - Modo claro
 * - Modo sistema (automático según preferencias del SO)
 */
const ThemeToggle = () => {
    const { theme, setTheme } = useTheme();

    const themes = [
        { id: 'dark', icon: Moon, label: 'Oscuro' },
        { id: 'light', icon: Sun, label: 'Claro' },
        { id: 'system', icon: Monitor, label: 'Sistema' }
    ];

    return (
        <div className="flex items-center gap-1 bg-gray-800 dark:bg-gray-800 light:bg-gray-200 rounded-lg p-1">
            {themes.map(({ id, icon: Icon, label }) => (
                <button
                    key={id}
                    onClick={() => setTheme(id)}
                    className={`
            flex items-center gap-2 px-3 py-2 rounded-md transition-all text-sm font-medium
            ${theme === id
                            ? 'bg-red-600 text-white shadow-lg'
                            : 'text-gray-400 hover:text-white hover:bg-gray-700 dark:hover:bg-gray-700 light:hover:bg-gray-300'
                        }
          `}
                    title={label}>
                    <Icon className="w-4 h-4" />
                    <span className="hidden sm:inline">{label}</span>
                </button>
            ))}
        </div>
    );
};

export default ThemeToggle;
