import { useState, useEffect, useCallback } from 'react';

interface MetricGroup {
    total: number;
    [key: string]: any;
}

interface AdminDashboardData {
    success: boolean;
    timestamp: string;
    metrics: {
        users: MetricGroup;
        clients: MetricGroup;
        projects: MetricGroup;
        financial: {
            total_value: number;
            avg_project_value: number;
            currency: string;
        };
        document_types: Array<{ id: string, nombre: string, count: number }>;
        price_references: MetricGroup;
    };
    settings: {
        services: Array<{ id: string, nombre: string, estado: boolean, descripcion: string }>;
        features: Array<{ id: string, nombre: string, estado: boolean }>;
    };
    recent_projects: any[];
}

export function useAdminStats() {
    const [data, setData] = useState<AdminDashboardData | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchStats = useCallback(async () => {
        try {
            setIsLoading(true);
            const response = await fetch('/api/admin/dashboard');
            if (!response.ok) throw new Error('Failed to fetch admin stats');
            const result = await response.json();
            setData(result);
            setError(null);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    }, []);

    const toggleService = async (serviceId: string, newState: boolean) => {
        try {
            const response = await fetch('/api/admin/toggle-service', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: serviceId, estado: newState }),
            });
            if (!response.ok) throw new Error('Failed to toggle service');
            await fetchStats(); // Refresh data
            return true;
        } catch (err) {
            console.error(err);
            return false;
        }
    };

    useEffect(() => {
        fetchStats();
        // Opcional: Polling cada 30 segundos
        const interval = setInterval(fetchStats, 30000);
        return () => clearInterval(interval);
    }, [fetchStats]);

    return {
        data,
        isLoading,
        error,
        refresh: fetchStats,
        toggleService
    };
}
