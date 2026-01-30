/**
 * PILI Avatar Component
 * Modern TypeScript version with Framer Motion animations
 * 
 * Features:
 * - Multiple size variants
 * - Status indicators
 * - Crown decoration
 * - Smooth animations
 */
import { motion } from 'framer-motion';
import { Crown } from 'lucide-react';

interface PILIAvatarProps {
    size?: 'sm' | 'md' | 'lg' | 'xl';
    showCrown?: boolean;
    status?: 'active' | 'thinking' | 'analyzing' | 'generating' | 'offline';
    className?: string;
}

const sizeMap = {
    sm: 24,
    md: 40,
    lg: 64,
    xl: 96,
};

const statusConfig = {
    active: { color: 'bg-green-500', text: 'Lista para ayudar', icon: '✨' },
    thinking: { color: 'bg-yellow-500', text: 'Pensando...', icon: '🤔' },
    analyzing: { color: 'bg-blue-500', text: 'Analizando...', icon: '🔍' },
    generating: { color: 'bg-purple-500', text: 'Generando...', icon: '📄' },
    offline: { color: 'bg-gray-500', text: 'Offline', icon: '💤' },
};

export function PILIAvatar({
    size = 'md',
    showCrown = true,
    status,
    className = ''
}: PILIAvatarProps) {
    const pixelSize = sizeMap[size];

    return (
        <div className={`relative inline-flex items-center justify-center ${className}`}>
            {/* Crown */}
            {showCrown && (
                <motion.div
                    initial={{ y: -5, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ duration: 0.3 }}
                    className="absolute -top-2 left-1/2 transform -translate-x-1/2 z-10"
                >
                    <Crown className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                </motion.div>
            )}

            {/* Avatar */}
            <motion.div
                whileHover={{ scale: 1.05 }}
                className="relative rounded-full overflow-hidden bg-gradient-to-br from-brand-red to-brand-yellow p-0.5"
                style={{ width: pixelSize, height: pixelSize }}
            >
                <div className="w-full h-full rounded-full overflow-hidden bg-white">
                    <img
                        src="/src/assets/avatars/pili-avatar.png"
                        alt="PILI AI Assistant"
                        className="w-full h-full object-cover"
                        onError={(e) => {
                            // Fallback to gradient if image fails to load
                            e.currentTarget.style.display = 'none';
                            e.currentTarget.parentElement!.style.background =
                                'linear-gradient(135deg, #DC2626 0%, #F59E0B 100%)';
                        }}
                    />
                </div>

                {/* Shine effect */}
                <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white to-transparent opacity-20 pointer-events-none" />
            </motion.div>

            {/* Status indicator */}
            {status && (
                <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className={`absolute -bottom-1 -right-1 w-3 h-3 ${statusConfig[status].color} rounded-full border-2 border-white dark:border-gray-900`}
                >
                    <span className="absolute inset-0 rounded-full animate-ping opacity-75 ${statusConfig[status].color}" />
                </motion.div>
            )}
        </div>
    );
}

/**
 * Large PILI Avatar with animations
 */
export function PILIAvatarLarge({ showCrown = true }: { showCrown?: boolean }) {
    return (
        <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5, type: 'spring' }}
            className="relative inline-block"
        >
            {showCrown && (
                <motion.div
                    animate={{ y: [0, -5, 0] }}
                    transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                    className="absolute -top-6 left-1/2 transform -translate-x-1/2 z-20"
                >
                    <Crown className="w-8 h-8 text-yellow-400 fill-yellow-400 drop-shadow-lg" />
                </motion.div>
            )}

            <div className="relative bg-gradient-to-br from-brand-red via-red-500 to-brand-yellow p-1 rounded-full shadow-2xl">
                <div className="w-20 h-20 rounded-full overflow-hidden bg-white">
                    <img
                        src="/src/assets/avatars/pili-avatar.png"
                        alt="PILI"
                        className="w-full h-full object-cover"
                    />
                </div>

                {/* Animated particles */}
                <div className="absolute inset-0">
                    {[0, 1, 2].map((i) => (
                        <motion.div
                            key={i}
                            animate={{
                                scale: [0, 1, 0],
                                opacity: [0, 1, 0],
                            }}
                            transition={{
                                duration: 2,
                                repeat: Infinity,
                                delay: i * 0.5,
                            }}
                            className="absolute top-2 right-2 w-1 h-1 bg-yellow-200 rounded-full"
                            style={{
                                top: `${20 + i * 20}%`,
                                right: `${10 + i * 15}%`,
                            }}
                        />
                    ))}
                </div>
            </div>
        </motion.div>
    );
}

/**
 * PILI Badge with name and variant
 */
interface PILIBadgeProps {
    name?: string;
    variant?: 'default' | 'cotizadora' | 'analista' | 'coordinadora' | 'projectManager' | 'reportera';
}

export function PILIBadge({ name = 'PILI', variant = 'default' }: PILIBadgeProps) {
    const variants = {
        default: 'bg-brand-yellow text-black',
        cotizadora: 'bg-brand-yellow text-black',
        analista: 'bg-blue-600 text-white',
        coordinadora: 'bg-green-600 text-white',
        projectManager: 'bg-purple-600 text-white',
        reportera: 'bg-indigo-600 text-white',
    };

    return (
        <motion.div
            whileHover={{ scale: 1.05 }}
            className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full ${variants[variant]} font-bold text-sm shadow-lg border-2 border-white/50`}
        >
            <PILIAvatar size="sm" showCrown={true} />
            <span>{name}</span>
            <span className="text-xs opacity-75">IA</span>
        </motion.div>
    );
}

/**
 * PILI Status with text
 */
interface PILIStatusProps {
    status?: 'active' | 'thinking' | 'analyzing' | 'generating' | 'offline';
}

export function PILIStatus({ status = 'active' }: PILIStatusProps) {
    const config = statusConfig[status];

    return (
        <div className="flex items-center gap-2">
            <PILIAvatar size="sm" showCrown={true} status={status} />
            <div className="flex items-center gap-2">
                <div className={`w-2 h-2 ${config.color} rounded-full animate-pulse`} />
                <span className="text-sm text-gray-600 dark:text-gray-300 font-medium">
                    {config.icon} {config.text}
                </span>
            </div>
        </div>
    );
}
