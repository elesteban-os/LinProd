# LinProd - Control de Línea de Producción Industrial en Tiempo Real

Una aplicación web moderna para visualizar y controlar una línea de producción industrial con actualización en tiempo real mediante WebSockets.

## Características

✨ **Backend Robusto**
- API REST con FastAPI
- WebSockets para actualización en tiempo real
- Simulador de producción con lógica de estados
- Modelos Pydantic para validación de datos

🎨 **Frontend Moderno**
- Interfaz responsiva con React
- Diseño SaaS limpio con Tailwind CSS
- Gestión de estado global con Zustand
- Dashboard con métricas y reportes
- Animaciones suaves y transiciones

⚙️ **Características Funcionales**
- Control de simulación (Inicio, Pausa, Reset)
- Visualización de 4 procesos secuenciales
- Seguimiento de tareas por proceso
- Log de eventos en tiempo real
- Dashboard de métricas y reportes
- Indicador de cuello de botella

## Estructura del Proyecto

```
LinProd/
├── backend/
│   ├── app.py              # Aplicación FastAPI principal
│   ├── models.py           # Modelos Pydantic
│   ├── simulacion.py       # Lógica de simulación
│   └── requirements.txt    # Dependencias Python
└── gui/
    ├── src/
    │   ├── components/     # Componentes React
    │   ├── services/       # Servicios de API
    │   ├── store/          # Estado global (Zustand)
    │   ├── App.jsx         # Componente principal
    │   ├── main.jsx        # Punto de entrada
    │   └── index.css       # Estilos globales
    ├── index.html          # HTML principal
    ├── vite.config.js      # Configuración Vite
    ├── tailwind.config.js  # Configuración Tailwind
    ├── package.json        # Dependencias Node
    └── .eslintrc.json      # Configuración ESLint
```

## Instalación

### Requisitos Previos

- Python 3.8+
- Node.js 18+
- npm o yarn

### Backend

1. **Navegar al directorio backend:**
```bash
cd backend
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar el servidor:**
```bash
python app.py
```

El servidor estará disponible en `http://localhost:8000`

### Frontend

1. **Navegar al directorio gui:**
```bash
cd gui
```

2. **Instalar dependencias:**
```bash
npm install
```

3. **Ejecutar el servidor de desarrollo:**
```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:3000`

## Uso

1. **Abre el navegador** en `http://localhost:3000`
2. **Usa los botones de control:**
   - ▶ **Inicio**: Comienza la simulación
   - ⏸ **Pausa**: Pausa la simulación
3. **Navega entre tabs:**
   - **Procesos**: Vista detallada de la línea de producción
   - **Reportes**: Métricas y estadísticas

## API Endpoints

### REST

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Verifica el estado de la API |
| GET | `/estado` | Obtiene el estado actual del sistema |
| POST | `/simulacion/control` | Controla la simulación (start, pause, reset) |
| GET | `/procesos` | Obtiene la lista de procesos |
| POST | `/procesos` | Crea un nuevo proceso |

### WebSocket

| Endpoint | Descripción |
|----------|-------------|
| `/ws/simulacion` | Recibe actualizaciones en tiempo real del estado |

## Modelos de Datos

### Tarea
```python
{
  "id": int,
  "nombre": str,
  "estado": "libre" | "procesando",
  "ciclos_actuales": int,
  "ciclos_totales": int
}
```

### Proceso
```python
{
  "id": int,
  "nombre": str,
  "en_espera": int,
  "tareas": [Tarea]
}
```

### EstadoSistema
```python
{
  "t_actual": int,
  "ejecutando": bool,
  "procesos": [Proceso],
  "eventos": [str],
  "metricas": {
    "productos_completados": int,
    "tiempo_flujo": int,
    "cuello_botella": str
  },
  "timestamp": datetime
}
```

## Diseño UI

El frontend utiliza:
- **Paleta de colores:**
  - Primario: Azul oscuro (slate-900)
  - Secundario: Azul (blue-500)
  - Éxito: Verde (green-500)
  - Advertencia: Naranja (orange-500)
  - Error: Rojo (red-500)

- **Componentes clave:**
  - Header con navegación y controles
  - ProcessCard para cada proceso
  - EventLog para registro de eventos
  - Dashboard de reportes con métricas
  - Animaciones suaves en estados

## Desarrollo

### Ejecutar ambos servicios

**Terminal 1 (Backend):**
```bash
cd backend
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd gui
npm run dev
```

### Build para Producción

**Frontend:**
```bash
cd gui
npm run build
```

## Características Futuras

- [ ] Autenticación y autorización
- [ ] Persistencia de datos en base de datos
- [ ] Histórico de simulaciones
- [ ] Exportar reportes (PDF, CSV)
- [ ] Alertas personalizables
- [ ] Configuración de parámetros de simulación
- [ ] Multi-idioma
- [ ] Tema oscuro

## Tecnologías Utilizadas

**Backend:**
- FastAPI
- Pydantic
- Python-SocketIO
- Uvicorn

**Frontend:**
- React 18
- Tailwind CSS
- Zustand
- Axios
- Vite

## Licencia

MIT

## Autor

Desarrollado como solución de visualización en tiempo real para líneas de producción industriales.
