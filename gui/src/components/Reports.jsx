/* eslint-disable react/prop-types */
import React from 'react';

export const EventLog = ({ eventos }) => {
  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
      <div className="bg-slate-900 text-white px-4 py-3">
        <h3 className="font-bold text-lg">Eventos</h3>
      </div>
      
      <div className="p-4 max-h-48 overflow-y-auto bg-slate-50">
        {eventos.length === 0 ? (
          <p className="text-gray-500 text-sm italic">Esperando eventos...</p>
        ) : (
          <div className="space-y-2 font-mono text-sm">
            {eventos.map((evento, index) => (
              <div key={index} className="text-gray-700 flex gap-2">
                <span className="text-gray-400 flex-shrink-0">t = 12</span>
                <span className="text-gray-600">{evento}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export const ReportCard = ({ titulo, valor, subtitulo, acento = false }) => {
  return (
    <div className={`rounded-lg p-4 text-center ${
      acento
        ? 'bg-red-50 border border-red-200'
        : 'bg-white border border-gray-200'
    }`}>
      <p className={`text-sm font-semibold ${
        acento ? 'text-red-600' : 'text-gray-600'
      }`}>
        {titulo}
      </p>
      <p className={`text-3xl font-bold my-2 ${
        acento ? 'text-red-700' : 'text-slate-900'
      }`}>
        {valor}
      </p>
      {subtitulo && (
        <p className="text-xs text-gray-500">{subtitulo}</p>
      )}
    </div>
  );
};

export const ReporteDashboard = ({ metricas }) => {
  // Calcular métrica de cuello de botella (porcentaje)
  const porcentajeCuello = 35; // Placeholder
  
  return (
    <div className="bg-slate-50 rounded-lg p-6">
      <h2 className="text-2xl font-bold text-slate-900 mb-6">Reportes de la línea de producción</h2>
      
      {/* Grid de reportes */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="grid grid-cols-3 gap-4">
          <ReportCard 
            titulo="Tiempo (t)" 
            valor={metricas.tiempo_flujo || 0}
            subtitulo="segundos"
          />
          <ReportCard 
            titulo="Completadas" 
            valor={metricas.productos_completados || 0}
            subtitulo="productos"
          />
          <ReportCard 
            titulo="Procesando" 
            valor="7"
            subtitulo="tareas"
          />
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          <ReportCard 
            titulo="Tiempo promedio" 
            valor="16.6"
            subtitulo="ciclos"
          />
          <ReportCard 
            titulo="Ciclos/tiempo" 
            valor="6.21"
            subtitulo="ciclos/seg"
          />
          <ReportCard 
            titulo="Cuello de Botella" 
            valor={porcentajeCuello + '%'}
            subtitulo={metricas.cuello_botella || 'Proceso 3'}
            acento={true}
          />
        </div>
      </div>
      
      {/* Barra de estado del sistema */}
      <div className="mt-8">
        <p className="text-sm font-semibold text-gray-600 mb-2">Estado del sistema:</p>
        <div className="flex gap-4">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-700">En ejecución</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
            <span className="text-sm text-gray-700">Idle</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <span className="text-sm text-gray-700">En espera</span>
          </div>
        </div>
      </div>
    </div>
  );
};
