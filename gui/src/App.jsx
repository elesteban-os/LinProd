import React, { useState, useEffect } from 'react';
import { useSimuladorStore } from './store/simuladorStore';
import { api } from './services/api';
import { Header } from './components/Header';
import { ProductionView } from './components/ProductionView';
import { EventLog, ReporteDashboard } from './components/Reports';
import './index.css';

export default function App() {
  const [tabActivo, setTabActivo] = useState('procesos');
  const [ws, setWs] = useState(null);
  const [cargando, setCargando] = useState(true);
  
  // Estado global
  const {
    t_actual,
    ejecutando,
    procesos,
    eventos,
    metricas,
    actualizarEstado,
    conectarWebSocket,
  } = useSimuladorStore();

  // Inicializar conexión y cargar estado
  useEffect(() => {
    const inicializar = async () => {
      try {
        // Conectar WebSocket
        const websocket = conectarWebSocket();
        setWs(websocket);
        
        // Obtener estado inicial
        const estado = await api.obtenerEstado();
        actualizarEstado(estado);
        
        setCargando(false);
      } catch (error) {
        console.error('Error al inicializar:', error);
        setCargando(false);
      }
    };
    
    inicializar();
    
    // Cleanup
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  // Handlers de control
  const handleInicio = async () => {
    try {
      await api.iniciarSimulacion();
    } catch (error) {
      console.error('Error al iniciar:', error);
    }
  };

  const handlePausa = async () => {
    try {
      await api.pausarSimulacion();
    } catch (error) {
      console.error('Error al pausar:', error);
    }
  };

  const handleNext = async () => {
    try {
      await api.stepSimulacion();
    } catch (error) {
      console.error('Error al avanzar un paso:', error);
    }
  };

  const handleAgregarProceso = async () => {
    try {
      await api.crearProceso({
        nombre: `Proceso ${procesos.length + 1}`,
        tareas: [
          {
            nombre: 'Tarea 1',
            ciclos_totales: 3,
          },
        ],
      });
    } catch (error) {
      console.error('Error al agregar proceso:', error);
    }
  };

  const handleAgregarTarea = async (procesoId, tarea) => {
    try {
      await api.crearTarea(procesoId, tarea);
    } catch (error) {
      console.error('Error al agregar tarea:', error);
    }
  };

  const handleEliminarProceso = async (procesoId) => {
    try {
      await api.eliminarProceso(procesoId);
    } catch (error) {
      console.error('Error al eliminar proceso:', error);
    }
  };

  const handleEliminarTarea = async (procesoId, tareaId) => {
    try {
      await api.eliminarTarea(procesoId, tareaId);
    } catch (error) {
      console.error('Error al eliminar tarea:', error);
    }
  };

  if (cargando) {
    return (
      <div className="h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 font-semibold">Cargando LinProd...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <Header
        onInicio={handleInicio}
        onPausa={handlePausa}
        onNext={handleNext}
        ejecutando={ejecutando}
        tabActivo={tabActivo}
        setTabActivo={setTabActivo}
      />

      {/* Contenido principal */}
      <main className="p-6 max-w-7xl mx-auto">
        {/* Tab: Procesos */}
        {tabActivo === 'procesos' && (
          <div className="space-y-6">
            {/* Vista de producción */}
            <ProductionView
              procesos={procesos}
              onAddProceso={handleAgregarProceso}
              onAddTarea={handleAgregarTarea}
              onDeleteProceso={handleEliminarProceso}
              onDeleteTarea={handleEliminarTarea}
            />
            
            {/* Panel inferior */}
            <div className="grid grid-cols-2 gap-6">
              <EventLog eventos={eventos} />
              <div className="bg-white rounded-lg shadow-md border border-gray-200 p-4">
                <h3 className="font-bold text-lg text-slate-900 mb-4">Información</h3>
                <div className="space-y-3 text-sm text-gray-700">
                  <p>
                    <span className="font-semibold">Tiempo actual:</span> {t_actual}s
                  </p>
                  <p>
                    <span className="font-semibold">Estado:</span>{' '}
                    {ejecutando ? (
                      <span className="text-green-600 font-semibold">Ejecutando</span>
                    ) : (
                      <span className="text-gray-600">Pausado</span>
                    )}
                  </p>
                  <p>
                    <span className="font-semibold">Procesos activos:</span> {procesos.length}
                  </p>
                  <p>
                    <span className="font-semibold">Tareas totales:</span>{' '}
                    {procesos.reduce((acc, p) => acc + p.tareas.length, 0)}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab: Reportes */}
        {tabActivo === 'reportes' && (
          <ReporteDashboard metricas={metricas} />
        )}
      </main>
    </div>
  );
}
