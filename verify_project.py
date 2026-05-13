#!/usr/bin/env python3
"""
Script de verificación del proyecto LinProd
Verifica que todos los archivos necesarios existan y sean accesibles
"""

import os
import sys
from pathlib import Path

# Colores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_file(path: str) -> bool:
    """Verifica si un archivo existe"""
    exists = os.path.isfile(path)
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    print(f"  {status} {path}")
    return exists

def check_dir(path: str) -> bool:
    """Verifica si un directorio existe"""
    exists = os.path.isdir(path)
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    print(f"  {status} {path}")
    return exists

def main():
    print(f"\n{YELLOW}═══════════════════════════════════════════════════════{RESET}")
    print(f"{YELLOW}  LinProd Project Verification{RESET}")
    print(f"{YELLOW}═══════════════════════════════════════════════════════{RESET}\n")
    
    all_ok = True
    
    # Verificar archivos de documentación
    print(f"{YELLOW}Documentación:{RESET}")
    docs = [
        'README.md',
        'QUICKSTART.md',
        'DEVELOPMENT.md',
        'ARCHITECTURE.md',
        'API.md',
        'TESTING.md',
        'EXAMPLES.md',
        'CONTRIBUTING.md',
        'PROJECT_STRUCTURE.md',
        'INDEX.md',
        'CHANGELOG.md',
        'START_HERE.md'
    ]
    for doc in docs:
        all_ok &= check_file(doc)
    
    # Verificar archivos de configuración
    print(f"\n{YELLOW}Configuración:{RESET}")
    config_files = [
        '.gitignore',
        'docker-compose.yml',
        'setup.sh',
        'setup.bat'
    ]
    for config in config_files:
        all_ok &= check_file(config)
    
    # Verificar backend
    print(f"\n{YELLOW}Backend:{RESET}")
    all_ok &= check_dir('backend')
    backend_files = [
        'backend/app.py',
        'backend/models.py',
        'backend/simulacion.py',
        'backend/test_app.py',
        'backend/requirements.txt',
        'backend/requirements-dev.txt',
        'backend/.env.example',
        'backend/Dockerfile'
    ]
    for file in backend_files:
        all_ok &= check_file(file)
    
    # Verificar frontend
    print(f"\n{YELLOW}Frontend:{RESET}")
    all_ok &= check_dir('gui')
    frontend_files = [
        'gui/package.json',
        'gui/index.html',
        'gui/vite.config.js',
        'gui/tailwind.config.js',
        'gui/postcss.config.js',
        'gui/.eslintrc.json',
        'gui/.env.example',
        'gui/Dockerfile',
        'gui/src/App.jsx',
        'gui/src/main.jsx',
        'gui/src/index.css',
        'gui/src/components/Header.jsx',
        'gui/src/components/ProductionView.jsx',
        'gui/src/components/Reports.jsx',
        'gui/src/store/simuladorStore.js',
        'gui/src/services/api.js'
    ]
    for file in frontend_files:
        all_ok &= check_file(file)
    
    # Resumen
    print(f"\n{YELLOW}═══════════════════════════════════════════════════════{RESET}")
    if all_ok:
        print(f"{GREEN}✓ ¡TODOS LOS ARCHIVOS ESTÁN PRESENTES!{RESET}")
        print(f"{GREEN}El proyecto está listo para usar.{RESET}")
    else:
        print(f"{RED}✗ Faltan algunos archivos.{RESET}")
        print(f"{RED}Por favor, verifica la instalación.{RESET}")
        sys.exit(1)
    
    print(f"\n{YELLOW}Próximos pasos:{RESET}")
    print(f"  1. Lee: START_HERE.md o QUICKSTART.md")
    print(f"  2. Ejecuta: setup.sh (Linux/Mac) o setup.bat (Windows)")
    print(f"  3. Backend: cd backend && python app.py")
    print(f"  4. Frontend: cd gui && npm run dev")
    print(f"  5. Abre: http://localhost:3000\n")

if __name__ == '__main__':
    main()
