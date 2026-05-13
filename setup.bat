@echo off
echo ================================
echo LinProd - Quick Start Script
echo ================================
echo.

REM Verificar si Python está instalado
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python no esta instalado
    exit /b 1
)

REM Verificar si Node.js está instalado
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Node.js no esta instalado
    exit /b 1
)

echo OK: Python y Node.js detectados
echo.

REM Backend
echo ================================
echo Configurando Backend...
echo ================================
cd backend

if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo OK: Backend listo
echo.

REM Frontend
echo ================================
echo Configurando Frontend...
echo ================================
cd ..\gui

if not exist "node_modules" (
    echo Instalando dependencias...
    call npm install
)

echo.
echo OK: Frontend listo
echo.

REM Instrucciones finales
echo ================================
echo Inicio Rapido
echo ================================
echo.
echo Terminal 1 - Backend:
echo cd backend
echo venv\Scripts\activate.bat
echo python app.py
echo.
echo Terminal 2 - Frontend:
echo cd gui
echo npm run dev
echo.
echo Abre el navegador en: http://localhost:3000
echo.
