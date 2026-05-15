/* eslint-disable react/prop-types */
import React, { useState } from 'react';

export const TareaItem = ({ tarea }) => {
  const isEspera = tarea.estado === 'espera';
  const isIdle = tarea.estado === 'idle';
  const isProcesando = tarea.estado === 'procesando';
  
  return (
    <div className="flex items-center gap-3 py-2 px-2 rounded hover:bg-slate-100 transition-colors">
      {/* Indicador de estado */}
      <div
        className={`w-3 h-3 rounded-full ${
          isProcesando
            ? 'bg-green-500 animate-pulse'
            : isIdle
            ? 'bg-yellow-400'
            : isEspera
            ? 'bg-red-500'
            : 'bg-gray-300'
        }`}
      />
      
      {/* Nombre de tarea */}
      <span className="text-sm font-medium flex-1 truncate">
        {tarea.nombre}
      </span>
      
      {/* Ciclos */}
      <span className="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded">
        {tarea.ciclos_actuales}/{tarea.ciclos_totales}
      </span>
    </div>
  );
};

export const ProcessCard = ({ proceso, onAddTarea, onDeleteProceso, onDeleteTarea }) => {
  const [mostrarForm, setMostrarForm] = useState(false);
  const [ciclosTarea, setCiclosTarea] = useState(3);

  const handleSubmit = (event) => {
    event.preventDefault();
    onAddTarea(proceso.id, {
      ciclos_totales: Number(ciclosTarea) || 3,
    });
    setCiclosTarea(3);
    setMostrarForm(false);
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow min-w-[340px] shrink-0">
      {/* Header de la tarjeta */}
      <div className="px-4 py-3 bg-blue-900 text-white flex items-center justify-between gap-3">
        <h3 className="text-lg font-bold">{proceso.nombre}</h3>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setMostrarForm((value) => !value)}
            className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 text-white font-bold transition-colors"
            aria-label={`Agregar tarea a ${proceso.nombre}`}
          >
            +
          </button>
          <button
            type="button"
            onClick={() => onDeleteProceso(proceso.id)}
            className="w-8 h-8 rounded-full bg-white/10 hover:bg-red-500/90 text-white font-bold transition-colors"
            aria-label={`Eliminar ${proceso.nombre}`}
          >
            ×
          </button>
        </div>
      </div>
      
      {/* Contenido */}
      <div className="p-4 flex flex-col gap-4">
        {/* En espera */}
        <div className="flex items-center gap-2 mb-4 pb-3 border-b border-gray-200">
          <span className="text-sm font-semibold text-gray-600">En espera:</span>
          <div className="flex items-center gap-2 ml-auto">
            <svg className="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded font-semibold">
              {proceso.en_espera}
            </span>
          </div>
        </div>
        
        {/* Lista de tareas */}
        <div className="space-y-1 max-h-[280px] overflow-y-auto pr-1">
          {proceso.tareas.map((tarea) => (
            <div key={tarea.id} className="group">
              <div className="flex items-center gap-2">
                <div className="flex-1 min-w-0">
                  <TareaItem tarea={tarea} />
                </div>
                <button
                  type="button"
                  onClick={() => onDeleteTarea(proceso.id, tarea.id)}
                  className="opacity-0 group-hover:opacity-100 transition-opacity w-7 h-7 rounded-full bg-slate-200 hover:bg-red-100 text-slate-600 hover:text-red-600 font-bold"
                  aria-label={`Eliminar ${tarea.nombre}`}
                >
                  ×
                </button>
              </div>
            </div>
          ))}
        </div>

        {mostrarForm && (
          <form onSubmit={handleSubmit} className="border border-dashed border-slate-300 rounded-lg p-3 bg-slate-50 space-y-3">
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">Ciclos necesarios</label>
              <input
                type="number"
                min="1"
                value={ciclosTarea}
                onChange={(event) => setCiclosTarea(event.target.value)}
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </div>
            <div className="flex gap-2">
              <button type="submit" className="flex-1 rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-700">
                Agregar
              </button>
              <button type="button" onClick={() => setMostrarForm(false)} className="rounded-md border border-slate-300 px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100">
                Cancelar
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export const ProductionView = ({ procesos, onAddProceso, onAddTarea, onDeleteProceso, onDeleteTarea }) => {
  return (
    <div className="bg-slate-50 rounded-lg p-6">
      <div className="flex items-center justify-between gap-4 mb-6">
        <h2 className="text-2xl font-bold text-slate-900">Vista de la línea de producción</h2>
        <p className="text-sm text-slate-500">Desliza horizontalmente para ver más procesos</p>
      </div>

      {/* Lista horizontal de procesos */}
      <div className="flex gap-4 overflow-x-auto pb-4 pr-2 items-stretch">
        {procesos.map((proceso) => (
          <React.Fragment key={proceso.id}>
            <ProcessCard
              proceso={proceso}
              onAddTarea={onAddTarea}
              onDeleteProceso={onDeleteProceso}
              onDeleteTarea={onDeleteTarea}
            />
          </React.Fragment>
        ))}

        <button
          type="button"
          onClick={onAddProceso}
          className="min-w-[340px] shrink-0 rounded-lg border-2 border-dashed border-slate-300 bg-white/70 hover:bg-white hover:border-blue-400 transition-colors flex flex-col items-center justify-center text-slate-500 hover:text-blue-600"
        >
          <span className="text-5xl leading-none font-light">+</span>
          <span className="mt-2 text-sm font-semibold">Agregar proceso</span>
          <span className="text-xs text-slate-400 mt-1">Crea otro bloque a la derecha</span>
        </button>
      </div>
    </div>
  );
};
