import React from 'react';

/**
 * NavItem - Item de navegación del panel izquierdo
 * 
 * Props:
 * - icon: Componente de icono (Lucide)
 * - label: Texto del item
 * - active: Si está activo
 * - onClick: Callback al hacer click
 * - badge: Número opcional para mostrar badge
 */
const NavItem = ({ icon: Icon, label, active, onClick, badge }) => {
    return (
        <button
            onClick={onClick}
            className={`
        w-full flex items-center justify-between px-4 py-3 rounded-lg transition-all group
        ${active
                    ? 'bg-red-600 text-white shadow-lg'
                    : 'text-gray-400 hover:bg-gray-800 hover:text-white dark:hover:bg-gray-800 light:hover:bg-gray-100'
                }
      `}>
            <div className="flex items-center gap-3">
                <Icon className={`w-5 h-5 ${active ? 'text-white' : 'text-gray-400 group-hover:text-yellow-400'}`} />
                <span className="font-medium">{label}</span>
            </div>

            {badge !== undefined && badge > 0 && (
                <span className={`
          px-2 py-0.5 rounded-full text-xs font-bold
          ${active
                        ? 'bg-white text-red-600'
                        : 'bg-yellow-400 text-gray-900'
                    }
        `}>
                    {badge}
                </span>
            )}
        </button>
    );
};

export default NavItem;
