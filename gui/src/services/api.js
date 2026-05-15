import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const api = {
  // Obtener estado actual
  obtenerEstado: async () => {
    const response = await axios.get(`${API_BASE}/estado`);
    return response.data;
  },

  // Controlar simulación
  iniciarSimulacion: async (configuracion) => {
    const response = await axios.post(`${API_BASE}/simulacion/start`, {
      ...configuracion,
    });
    return response.data;
  },

  pausarSimulacion: async () => {
    const response = await axios.post(`${API_BASE}/simulacion/control`, {
      comando: 'pause',
    });
    return response.data;
  },

  resumeSimulacion: async () => {
    const response = await axios.post(`${API_BASE}/simulacion/control`, {
      comando: 'start',
    });
    return response.data;
  },

  stepSimulacion: async () => {
    const response = await axios.post(`${API_BASE}/simulacion/step`);
    return response.data;
  },

  resetearSimulacion: async () => {
    const response = await axios.post(`${API_BASE}/simulacion/control`, {
      comando: 'reset',
    });
    return response.data;
  },

  // Obtener procesos
  obtenerProcesos: async () => {
    const response = await axios.get(`${API_BASE}/procesos`);
    return response.data;
  },

  // Crear proceso
  crearProceso: async (proceso) => {
    const response = await axios.post(`${API_BASE}/procesos`, proceso);
    return response.data;
  },

  // Crear tarea dentro de un proceso
  crearTarea: async (procesoId, tarea) => {
    const response = await axios.post(`${API_BASE}/procesos/${procesoId}/tareas`, tarea);
    return response.data;
  },

  eliminarProceso: async (procesoId) => {
    const response = await axios.delete(`${API_BASE}/procesos/${procesoId}`);
    return response.data;
  },

  eliminarTarea: async (procesoId, tareaId) => {
    const response = await axios.delete(`${API_BASE}/procesos/${procesoId}/tareas/${tareaId}`);
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await axios.get(`${API_BASE}/health`);
    return response.data;
  },
};
