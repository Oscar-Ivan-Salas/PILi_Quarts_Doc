import { useEffect, useState } from 'react';
import axios from 'axios';

export function SystemStatus() {
    const [status, setStatus] = useState<'online' | 'offline' | 'checking'>('checking');
    const [message, setMessage] = useState('Conectando...');

    const checkConnection = async () => {
        try {
            await axios.get('http://localhost:8003/api/documents', {
                params: { user_id: 'test' },
                timeout: 2000
            });
            setStatus('online');
            setMessage('Sistema Conectado');
        } catch (error) {
            console.error('Connection check failed:', error);
            setStatus('offline');
            setMessage('Sin conexión con Backend (Puerto 8003)');
        }
    };

    useEffect(() => {
        checkConnection();
        const interval = setInterval(checkConnection, 10000);
        return () => clearInterval(interval);
    }, []);

    if (status === 'online') return null; // Hide if all good

    return (
        <div className={`fixed bottom-4 right-4 px-4 py-2 rounded-md text-white text-xs font-bold shadow-lg z-50 transition-colors ${status === 'offline' ? 'bg-red-500' : 'bg-yellow-500'
            }`}>
            <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${status === 'checking' ? 'animate-pulse bg-white' : 'bg-white'}`} />
                {message}
            </div>
        </div>
    );
}
