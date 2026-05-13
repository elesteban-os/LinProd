/* eslint-disable react/prop-types */
import React from 'react';

export const Header = ({ onInicio, onPausa, onNext, ejecutando, tabActivo, setTabActivo }) => {
  return (
    <header className="bg-slate-900 text-white shadow-lg">
      <div className="flex items-center justify-between px-6 py-4">
        {/* Logo y título */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center font-bold text-lg">
            LP
          </div>
          <h1 className="text-2xl font-bold">LinProd</h1>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 flex-1 ml-8">
          <button
            onClick={() => setTabActivo('procesos')}
            className={`px-4 py-2 font-semibold transition-all ${
              tabActivo === 'procesos'
                ? 'border-b-2 border-blue-500 text-blue-400'
                : 'text-gray-300 hover:text-white'
            }`}
          >
            Procesos
          </button>
          <button
            onClick={() => setTabActivo('reportes')}
            className={`px-4 py-2 font-semibold transition-all ${
              tabActivo === 'reportes'
                ? 'border-b-2 border-blue-500 text-blue-400'
                : 'text-gray-300 hover:text-white'
            }`}
          >
            Reportes
          </button>
        </div>

        {/* Botones de control */}
        <div className="flex gap-3">
          <button
            onClick={onNext}
            className="px-4 py-2 rounded-lg font-semibold transition-all bg-blue-500 hover:bg-blue-600 text-white"
          >
            Next
          </button>
          <button
            onClick={onPausa}
            disabled={!ejecutando}
            className={`px-4 py-2 rounded-lg font-semibold transition-all ${
              ejecutando
                ? 'bg-yellow-500 hover:bg-yellow-600 text-white'
                : 'bg-gray-600 text-gray-400 cursor-not-allowed'
            }`}
          >
            ⏸ Pausa
          </button>
          <button
            onClick={onInicio}
            disabled={ejecutando}
            className={`px-4 py-2 rounded-lg font-semibold transition-all ${
              !ejecutando
                ? 'bg-green-500 hover:bg-green-600 text-white'
                : 'bg-gray-600 text-gray-400 cursor-not-allowed'
            }`}
          >
            ▶ Inicio
          </button>
        </div>
      </div>
    </header>
  );
};
