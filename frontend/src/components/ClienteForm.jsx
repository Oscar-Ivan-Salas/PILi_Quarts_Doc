import React, { useState, useEffect } from 'react';
import { X, Save, User, Building2, Phone, Mail, MapPin, Briefcase } from 'lucide-react';
import Alerta from './Alerta';

const ClienteForm = ({ clienteEditar, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    ruc: '',
    telefono: '',
    email: '',
    direccion: '',
    ciudad: 'Huancayo',
    departamento: 'Junín',
    industria: '',
    tipo_cliente: 'empresa',
    persona_contacto: '',
    cargo_contacto: '',
    telefono_contacto: '',
    email_contacto: '',
    notas: ''
  });

  const [loading, setLoading] = useState(false);
  const [alerta, setAlerta] = useState(null);

  // Cargar datos del cliente si está editando
  useEffect(() => {
    if (clienteEditar) {
      setFormData(clienteEditar);
    }
  }, [clienteEditar]);

  const industrias = [
    'Construcción',
    'Minería',
    'Manufactura',
    'Comercio',
    'Servicios',
    'Educación',
    'Salud',
    'Gobierno',
    'Tecnología',
    'Otro'
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validarFormulario = () => {
    // Campos obligatorios
    if (!formData.nombre || formData.nombre.trim().length < 3) {
      setAlerta({ tipo: 'error', mensaje: 'El nombre o razón social debe tener al menos 3 caracteres' });
      return false;
    }

    if (!formData.ruc || formData.ruc.trim().length !== 11) {
      setAlerta({ tipo: 'error', mensaje: 'El RUC debe tener exactamente 11 dígitos' });
      return false;
    }

    // Validar que RUC sea numérico
    if (!/^\d{11}$/.test(formData.ruc)) {
      setAlerta({ tipo: 'error', mensaje: 'El RUC debe contener solo números' });
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validarFormulario()) {
      return;
    }

    setLoading(true);
    setAlerta(null);

    try {
      const url = clienteEditar
        ? `http://localhost:8000/api/clientes/${clienteEditar.id}`
        : 'http://localhost:8000/api/clientes/';

      const method = clienteEditar ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al guardar cliente');
      }

      const clienteGuardado = await response.json();

      setAlerta({
        tipo: 'exito',
        mensaje: clienteEditar
          ? 'Cliente actualizado exitosamente'
          : 'Cliente creado exitosamente'
      });

      // Esperar un poco para que el usuario vea el mensaje
      setTimeout(() => {
        onSuccess(clienteGuardado);
        onClose();
      }, 1500);

    } catch (error) {
      console.error('Error:', error);
      setAlerta({
        tipo: 'error',
        mensaje: error.message || 'Error al guardar cliente'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto border border-blue-500">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-blue-700 p-6 flex justify-between items-center border-b border-blue-500 z-10">
          <div className="flex items-center gap-3">
            <Building2 className="text-white" size={28} />
            <h2 className="text-2xl font-bold text-white">
              {clienteEditar ? 'Editar Cliente' : 'Nuevo Cliente'}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-blue-800 p-2 rounded-lg transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {/* Alerta */}
        {alerta && (
          <div className="p-4">
            <Alerta
              tipo={alerta.tipo}
              mensaje={alerta.mensaje}
              onClose={() => setAlerta(null)}
            />
          </div>
        )}

        {/* Formulario */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Información Básica */}
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-blue-400 flex items-center gap-2">
              <Building2 size={20} />
              Información Básica
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Nombre/Razón Social */}
              <div className="md:col-span-2">
                <label className="block text-blue-400 font-semibold mb-2">
                  Nombre/Razón Social *
                </label>
                <input
                  type="text"
                  name="nombre"
                  value={formData.nombre}
                  onChange={handleChange}
                  className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                  placeholder="Ej: Tesla Electricidad y Automatización S.A.C."
                  required
                />
              </div>

              {/* RUC */}
              <div>
                <label className="block text-blue-400 font-semibold mb-2">
                  RUC *
                </label>
                <input
                  type="text"
                  name="ruc"
                  value={formData.ruc}
                  onChange={handleChange}
                  className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                  placeholder="11 dígitos numéricos"
                  maxLength={11}
                  pattern="\d{11}"
                  required
                />
                <p className="text-xs text-gray-500 mt-1">11 dígitos numéricos</p>
              </div>

              {/* Teléfono */}
              <div>
                <label className="block text-blue-400 font-semibold mb-2">
                  Teléfono
                </label>
                <div className="flex items-center gap-2">
                  <Phone className="text-gray-500" size={20} />
                  <input
                    type="tel"
                    name="telefono"
                    value={formData.telefono}
                    onChange={handleChange}
                    className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="Ej: 906315961"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Ubicación */}
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-blue-400 flex items-center gap-2">
              <MapPin size={20} />
              Ubicación
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Dirección */}
              <div className="md:col-span-2">
                <label className="block text-blue-400 font-semibold mb-2">
                  Dirección
                </label>
                <input
                  type="text"
                  name="direccion"
                  value={formData.direccion}
                  onChange={handleChange}
                  className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                  placeholder="Ej: Jr. Los Narcisos Mz H Lote 04"
                />
              </div>

              {/* Ciudad */}
              <div>
                <label className="block text-blue-400 font-semibold mb-2">
                  Ciudad
                </label>
                <input
                  type="text"
                  name="ciudad"
                  value={formData.ciudad}
                  onChange={handleChange}
                  className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                  placeholder="Ej: Huancayo"
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-blue-400 font-semibold mb-2">
                  Email
                </label>
                <div className="flex items-center gap-2">
                  <Mail className="text-gray-500" size={20} />
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="ejemplo@empresa.com"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Clasificación */}
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-blue-400 flex items-center gap-2">
              <Briefcase size={20} />
              Clasificación
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Industria */}
              <div>
                <label className="block text-blue-400 font-semibold mb-2">
                  Industria
                </label>
                <select
                  name="industria"
                  value={formData.industria}
                  onChange={handleChange}
                  className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                >
                  <option value="">Seleccionar...</option>
                  {industrias.map(ind => (
                    <option key={ind} value={ind}>{ind}</option>
                  ))}
                </select>
              </div>

              {/* Tipo Cliente */}
              <div>
                <label className="block text-blue-400 font-semibold mb-2">
                  Tipo de Cliente
                </label>
                <select
                  name="tipo_cliente"
                  value={formData.tipo_cliente}
                  onChange={handleChange}
                  className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                >
                  <option value="empresa">Empresa</option>
                  <option value="persona">Persona Natural</option>
                  <option value="gobierno">Gobierno</option>
                  <option value="otro">Otro</option>
                </select>
              </div>
            </div>
          </div>

          {/* Persona de Contacto */}
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-blue-400 flex items-center gap-2">
              <User size={20} />
              Persona de Contacto
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Persona de Contacto */}
              <div>
                <label className="block text-blue-400 font-semibold mb-2">
                  Persona de Contacto
                </label>
                <input
                  type="text"
                  name="persona_contacto"
                  value={formData.persona_contacto}
                  onChange={handleChange}
                  className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                  placeholder="Nombre completo"
                />
              </div>

              {/* Cargo */}
              <div>
                <label className="block text-blue-400 font-semibold mb-2">
                  Cargo
                </label>
                <input
                  type="text"
                  name="cargo_contacto"
                  value={formData.cargo_contacto}
                  onChange={handleChange}
                  className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                  placeholder="Ej: Gerente General"
                />
              </div>

              {/* Teléfono Contacto */}
              <div>
                <label className="block text-blue-400 font-semibold mb-2">
                  Teléfono de Contacto
                </label>
                <input
                  type="tel"
                  name="telefono_contacto"
                  value={formData.telefono_contacto}
                  onChange={handleChange}
                  className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                  placeholder="Teléfono directo"
                />
              </div>

              {/* Email Contacto */}
              <div>
                <label className="block text-blue-400 font-semibold mb-2">
                  Email de Contacto
                </label>
                <input
                  type="email"
                  name="email_contacto"
                  value={formData.email_contacto}
                  onChange={handleChange}
                  className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors"
                  placeholder="email@empresa.com"
                />
              </div>
            </div>
          </div>

          {/* Notas */}
          <div>
            <label className="block text-blue-400 font-semibold mb-2">
              Notas (opcional)
            </label>
            <textarea
              name="notas"
              value={formData.notas}
              onChange={handleChange}
              rows={4}
              className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg p-3 focus:outline-none focus:border-blue-500 transition-colors resize-none"
              placeholder="Información adicional sobre el cliente..."
            />
          </div>

          {/* Botones */}
          <div className="flex gap-4 pt-4 border-t border-gray-700">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-6 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors font-semibold"
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 transition-colors font-semibold flex items-center justify-center gap-2 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Guardando...
                </>
              ) : (
                <>
                  <Save size={20} />
                  {clienteEditar ? 'Actualizar' : 'Guardar'} Cliente
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ClienteForm;
