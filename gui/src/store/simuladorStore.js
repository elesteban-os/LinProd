import { create } from 'zustand';

export const useSimuladorStore = create((set) => ({
  // Estado
  t_actual: 0,
  ejecutando: false,
  procesos: [],
  eventos: [],
  metricas: {
    productos_completados: 0,
    tiempo_flujo: 0,
    cuello_botella: null,
  },
  
  // Acciones
  setEstado: (estado) => set(estado),
  
  actualizarEstado: (nuevoEstado) => set({
    t_actual: nuevoEstado.t_actual,
    ejecutando: nuevoEstado.ejecutando,
    procesos: nuevoEstado.procesos,
    eventos: nuevoEstado.eventos,
    metricas: nuevoEstado.metricas,
  }),
  
  conectarWebSocket: () => {
    const ws = new WebSocket('ws://localhost:8000/ws/simulacion');
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        set({
          t_actual: data.t_actual,
          ejecutando: data.ejecutando,
          procesos: data.procesos,
          eventos: data.eventos,
          metricas: data.metricas,
        });
      } catch (error) {
        console.error('Error parseando WebSocket:', error);
      }
    };
    
    ws.onerror = (error) => {
      console.error('Error WebSocket:', error);
    };
    
    return ws;
  },
}));
