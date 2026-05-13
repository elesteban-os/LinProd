#!/bin/bash

echo "================================"
echo "LinProd - Quick Start Script"
echo "================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Por favor, instálalo primero."
    exit 1
fi

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado. Por favor, instálalo primero."
    exit 1
fi

echo "✅ Python3 y Node.js detectados"
echo ""

# Backend
echo "================================"
echo "Configurando Backend..."
echo "================================"
cd backend

if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Instalando dependencias..."
pip install -r requirements.txt

echo ""
echo "✅ Backend listo"
echo ""

# Frontend
echo "================================"
echo "Configurando Frontend..."
echo "================================"
cd ../gui

if [ ! -d "node_modules" ]; then
    echo "Instalando dependencias..."
    npm install
fi

echo ""
echo "✅ Frontend listo"
echo ""

# Instrucciones finales
echo "================================"
echo "Inicio Rápido"
echo "================================"
echo ""
echo "Terminal 1 - Backend:"
echo "cd backend"
echo "source venv/bin/activate"
echo "python app.py"
echo ""
echo "Terminal 2 - Frontend:"
echo "cd gui"
echo "npm run dev"
echo ""
echo "Abre el navegador en: http://localhost:3000"
echo ""
