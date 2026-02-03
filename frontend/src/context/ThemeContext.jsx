import React, { createContext, useContext, useState, useEffect } from 'react';

/**
 * ThemeContext - Gestiona el tema de la aplicación (oscuro/claro/sistema)
 * 
 * Colores de marca:
 * - Rojo: #dc2626
 * - Amarillo: #fbbf24
 */

const ThemeContext = createContext();

export const useTheme = () => {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme debe usarse dentro de ThemeProvider');
    }
    return context;
};

export const ThemeProvider = ({ children }) => {
    // 'dark' | 'light' | 'system'
    const [theme, setTheme] = useState(() => {
        const saved = localStorage.getItem('pili-theme');
        return saved || 'system';
    });

    const [resolvedTheme, setResolvedTheme] = useState('dark');

    useEffect(() => {
        const root = document.documentElement;

        const applyTheme = (isDark) => {
            if (isDark) {
                root.classList.add('dark');
                root.classList.remove('light');
            } else {
                root.classList.add('light');
                root.classList.remove('dark');
            }
            setResolvedTheme(isDark ? 'dark' : 'light');
        };

        if (theme === 'system') {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            applyTheme(mediaQuery.matches);

            const handler = (e) => applyTheme(e.matches);
            mediaQuery.addEventListener('change', handler);
            return () => mediaQuery.removeEventListener('change', handler);
        } else {
            applyTheme(theme === 'dark');
        }
    }, [theme]);

    const setThemeMode = (newTheme) => {
        setTheme(newTheme);
        localStorage.setItem('pili-theme', newTheme);
    };

    return (
        <ThemeContext.Provider value={{ theme, setTheme: setThemeMode, resolvedTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};
