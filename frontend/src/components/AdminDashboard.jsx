import React, { useState, useEffect } from 'react';
import {
  BarChart3, Users, FileText, DollarSign, TrendingUp,
  Settings, ToggleLeft, ToggleRight, AlertCircle, CheckCircle,
  Clock, Activity, Zap, Building2, Factory, Flame, Home,
  ClipboardCheck, Plug, Camera, FileCheck, Droplet
} from 'lucide-react';

/**
 * Panel de Administración - Tesla Cotizador V3.0
 *
 * Requiere autenticación básica: Admin/Admin1234
 *
 * Funcionalidades:
 * - Métricas del sistema (usuarios, documentos, ingresos, tokens)
 * - Switches para habilitar/deshabilitar servicios
 * - Switches para features flags
 * - Actividad reciente
 * - Estadísticas en tiempo real
 */
const AdminDashboard = () => {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);
  const [credentials, setCredentials] = useState({ username: '', password: '' });

  // Cargar dashboard
  const cargarDashboard = async () => {
    try {
      setLoading(true);

      // Autenticación básica
      const auth = btoa(`${credentials.username}:${credentials.password}`);

      const response = await fetch('/api/admin/dashboard', {
        headers: {
          'Authorization': `Basic ${auth}`
        }
      });

      if (response.status === 401) {
        setAuthenticated(false);
        setError('Credenciales incorrectas');
        return;
      }

      if (!response.ok) {
        throw new Error('Error al cargar dashboard');
      }

      const data = await response.json();
      setDashboard(data);
      setAuthenticated(true);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Toggle servicio
  const toggleServicio = async (servicioId) => {
    try {
      const auth = btoa(`${credentials.username}:${credentials.password}`);

      const response = await fetch(`/api/admin/toggle-servicio/${servicioId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Basic ${auth}`
        }
      });

      if (!response.ok) {
        throw new Error('Error al toggle servicio');
      }

      // Recargar dashboard
      await cargarDashboard();
    } catch (err) {
      console.error('Error:', err);
    }
  };

  // Toggle feature
  const toggleFeature = async (featureName) => {
    try {
      const auth = btoa(`${credentials.username}:${credentials.password}`);

      const response = await fetch(`/api/admin/toggle-feature/${featureName}`, {
        method: 'POST',
        headers: {
          'Authorization': `Basic ${auth}`
        }
      });

      if (!response.ok) {
        throw new Error('Error al toggle feature');
      }

      const data = await response.json();

      // Mostrar advertencia si es cambio temporal
      if (data.advertencia) {
        alert(data.advertencia);
      }

      // Recargar dashboard
      await cargarDashboard();
    } catch (err) {
      console.error('Error:', err);
    }
  };

  // Login
  const handleLogin = (e) => {
    e.preventDefault();
    cargarDashboard();
  };

  // Iconos para servicios
  const iconosServicios = {
    'electrico-residencial': Zap,
    'electrico-comercial': Building2,
    'electrico-industrial': Factory,
    'contraincendios': Flame,
    'domotica': Home,
    'itse': ClipboardCheck,
    'pozo-tierra': Plug,
    'redes-cctv': Camera,
    'expedientes': FileCheck,
    'saneamiento': Droplet
  };

  // Si no está autenticado, mostrar login
  if (!authenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
          <div className="text-center mb-8">
            <div className="bg-blue-600 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Settings className="w-10 h-10 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              Panel de Administración
            </h1>
            <p className="text-gray-600">PILi_Quarts V1.0</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Usuario
              </label>
              <input
                type="text"
                value={credentials.username}
                onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Admin"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Contraseña
              </label>
              <input
                type="password"
                value={credentials.password}
                onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Admin1234"
                required
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center">
                <AlertCircle className="w-5 h-5 mr-2" />
                {error}
              </div>
            )}

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-600 to-blue-500 text-white font-semibold py-3 rounded-lg hover:from-blue-700 hover:to-blue-600 transition-all shadow-lg"
            >
              Iniciar Sesión
            </button>

            <div className="bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded-lg text-sm">
              <p className="font-semibold">Credenciales de desarrollo:</p>
              <p>Usuario: <code className="bg-blue-100 px-2 py-1 rounded">Admin</code></p>
              <p>Contraseña: <code className="bg-blue-100 px-2 py-1 rounded">Admin1234</code></p>
            </div>
          </form>
        </div>
      </div>
    );
  }

  // Si está cargando
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Activity className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Cargando dashboard...</p>
        </div>
      </div>
    );
  }

  // Dashboard principal
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-900 via-blue-800 to-blue-900 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold">Panel de Administración</h1>
              <p className="text-blue-200 mt-1">PILi_Quarts V1.0</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="bg-blue-700 px-4 py-2 rounded-lg">
                <p className="text-sm text-blue-200">Administrador</p>
                <p className="font-semibold">{credentials.username}</p>
              </div>
              <button
                onClick={() => setAuthenticated(false)}
                className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition-colors"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Métricas Principales */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Usuarios */}
          <MetricCard
            icon={Users}
            title="Usuarios"
            value={dashboard.metricas.usuarios.total}
            change="+12%"
            color="blue"
            subtitle={`Free: ${dashboard.metricas.usuarios.free} | Pro: ${dashboard.metricas.usuarios.pro} | Enterprise: ${dashboard.metricas.usuarios.enterprise}`}
          />

          {/* Documentos */}
          <MetricCard
            icon={FileText}
            title="Documentos"
            value={dashboard.metricas.documentos.total}
            change={dashboard.metricas.documentos.cambio_24h}
            color="green"
            subtitle={`Hoy: ${dashboard.metricas.documentos.hoy}`}
          />

          {/* Ingresos */}
          <MetricCard
            icon={DollarSign}
            title="Ingresos Mensuales"
            value={`$${dashboard.metricas.ingresos.mensual.toFixed(2)}`}
            change="+28%"
            color="purple"
            subtitle="Ingresos recurrentes"
          />

          {/* Tokens */}
          <MetricCard
            icon={Zap}
            title="Tokens Disponibles"
            value={dashboard.metricas.tokens.tokens_disponibles.toLocaleString()}
            change={`${dashboard.metricas.tokens.porcentaje_usado.toFixed(1)}% usado`}
            color="orange"
            subtitle={`Capacidad: ${dashboard.metricas.tokens.capacidad_total.toLocaleString()}`}
          />
        </div>

        {/* Distribución de Usuarios */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <Users className="w-6 h-6 mr-2 text-blue-600" />
            Distribución de Usuarios
          </h2>
          <div className="space-y-3">
            <ProgressBar
              label="🆓 Free"
              value={dashboard.metricas.usuarios.free}
              total={dashboard.metricas.usuarios.total}
              color="blue"
            />
            <ProgressBar
              label="⭐ Pro"
              value={dashboard.metricas.usuarios.pro}
              total={dashboard.metricas.usuarios.total}
              color="purple"
            />
            <ProgressBar
              label="👑 Enterprise"
              value={dashboard.metricas.usuarios.enterprise}
              total={dashboard.metricas.usuarios.total}
              color="yellow"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Servicios Disponibles */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
              <Settings className="w-6 h-6 mr-2 text-blue-600" />
              Servicios Disponibles
            </h2>
            <div className="space-y-2">
              {Object.entries(dashboard.servicios).map(([id, servicio]) => {
                const IconComponent = iconosServicios[id] || Zap;
                return (
                  <ServiceToggle
                    key={id}
                    id={id}
                    nombre={servicio.nombre}
                    habilitado={servicio.habilitado}
                    icon={IconComponent}
                    color={servicio.color}
                    onToggle={() => toggleServicio(id)}
                  />
                );
              })}
            </div>
          </div>

          {/* Feature Flags */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
              <BarChart3 className="w-6 h-6 mr-2 text-blue-600" />
              Funcionalidades Avanzadas
            </h2>
            <div className="space-y-4">
              <FeatureToggle
                nombre="Sistema de Tokens"
                habilitado={dashboard.features.token_manager}
                onToggle={() => toggleFeature('token_manager')}
                descripcion="Límites de tokens por plan"
              />
              <FeatureToggle
                nombre="Multi-IA Orchestrator"
                habilitado={dashboard.features.multi_ia}
                onToggle={() => toggleFeature('multi_ia')}
                descripcion="Gemini + Claude + GPT-4"
              />
              <FeatureToggle
                nombre="Sistema Multi-Agente"
                habilitado={dashboard.features.multi_agent}
                onToggle={() => toggleFeature('multi_agent')}
                descripcion="3 agentes colaborando"
              />
              <FeatureToggle
                nombre="Autenticación Usuarios"
                habilitado={dashboard.features.auth_usuarios}
                onToggle={() => toggleFeature('auth_usuarios')}
                descripcion="Login/registro de usuarios"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Componente de métrica
const MetricCard = ({ icon: Icon, title, value, change, color, subtitle }) => {
  const colors = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600'
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <div className={`bg-gradient-to-br ${colors[color]} p-3 rounded-lg`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <span className="text-green-600 text-sm font-semibold">{change}</span>
      </div>
      <h3 className="text-gray-600 text-sm font-medium">{title}</h3>
      <p className="text-3xl font-bold text-gray-800 mt-1">{value}</p>
      {subtitle && <p className="text-xs text-gray-500 mt-2">{subtitle}</p>}
    </div>
  );
};

// Componente de progress bar
const ProgressBar = ({ label, value, total, color }) => {
  const percentage = Math.round((value / total) * 100);

  const colors = {
    blue: 'bg-blue-500',
    purple: 'bg-purple-500',
    yellow: 'bg-yellow-500'
  };

  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="font-medium text-gray-700">{label}</span>
        <span className="text-gray-600">{value} ({percentage}%)</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`${colors[color]} h-2 rounded-full transition-all`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

// Componente de toggle de servicio
const ServiceToggle = ({ id, nombre, habilitado, icon: Icon, color, onToggle }) => {
  return (
    <div className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors border border-gray-200">
      <div className="flex items-center space-x-3">
        <div className="p-2 rounded-lg" style={{ backgroundColor: `${color}20` }}>
          <Icon className="w-5 h-5" style={{ color }} />
        </div>
        <span className="font-medium text-gray-700">{nombre}</span>
      </div>
      <button
        onClick={onToggle}
        className={`relative inline-flex items-center h-6 rounded-full w-11 transition-colors ${habilitado ? 'bg-green-500' : 'bg-gray-300'
          }`}
      >
        <span
          className={`inline-block w-4 h-4 transform bg-white rounded-full transition-transform ${habilitado ? 'translate-x-6' : 'translate-x-1'
            }`}
        />
      </button>
    </div>
  );
};

// Componente de toggle de feature
const FeatureToggle = ({ nombre, habilitado, onToggle, descripcion }) => {
  return (
    <div className="flex items-start justify-between p-4 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors">
      <div className="flex-1">
        <h3 className="font-semibold text-gray-800 mb-1">{nombre}</h3>
        <p className="text-sm text-gray-600">{descripcion}</p>
      </div>
      <button
        onClick={onToggle}
        className="ml-4"
      >
        {habilitado ? (
          <ToggleRight className="w-10 h-10 text-green-500" />
        ) : (
          <ToggleLeft className="w-10 h-10 text-gray-400" />
        )}
      </button>
    </div>
  );
};

export default AdminDashboard;
