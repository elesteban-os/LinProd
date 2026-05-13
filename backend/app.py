import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from models import (
    Proceso, Tarea, EstadoSistema, ComandoSimulacion, 
    NuevoProceso, NuevaTarea,
    ControlResponse, StartRequest
)
from simulacion import simulador

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista de conexiones WebSocket activas
conexiones_ws = set()

# Variable para controlar el loop de simulación
loop_task = None


async def broadcast_estado(estado: EstadoSistema):
    """Envía el estado a todos los clientes WebSocket conectados"""
    mensaje = estado.model_dump_json()
    desconectados = set()
    
    for ws in conexiones_ws:
        try:
            await ws.send_text(mensaje)
        except Exception as e:
            logger.error(f"Error enviando a WebSocket: {e}")
            desconectados.add(ws)
    
    # Limpiar conexiones desconectadas
    conexiones_ws.difference_update(desconectados)


async def iniciar_simulacion():
    """Inicia el loop de simulación"""
    global loop_task
    
    # Registrar callback para notificaciones
    simulador.registrar_callback(broadcast_estado)
    
    # Iniciar loop asíncrono
    loop_task = asyncio.create_task(simulador.iniciar_loop())
    logger.info("Loop de simulación iniciado")


async def detener_simulacion():
    """Detiene el loop de simulación"""
    global loop_task
    if loop_task:
        loop_task.cancel()
        try:
            await loop_task
        except asyncio.CancelledError:
            pass
    logger.info("Loop de simulación detenido")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación"""
    # Startup
    await iniciar_simulacion()
    yield
    # Shutdown
    await detener_simulacion()


# Crear aplicación FastAPI
app = FastAPI(
    title="LinProd API",
    description="API para visualizar línea de producción industrial",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Endpoints REST ====================

@app.get("/health")
async def health_check():
    """Verifica el estado de la API"""
    return {
        "status": "ok",
        "simulacion_ejecutando": simulador.ejecutando,
        "tiempo_actual": simulador.t_actual
    }


@app.get("/estado")
async def obtener_estado():
    """Retorna el estado actual del sistema"""
    return simulador.obtener_estado()


@app.post("/simulacion/control", response_model=ControlResponse)
async def control_simulacion(comando: ComandoSimulacion):
    """Controla la simulación (start, pause, reset)"""
    if comando.comando == "start":
        simulador.start()
        mensaje = "Simulación iniciada"
    elif comando.comando == "pause":
        simulador.pause()
        mensaje = "Simulación pausada"
    elif comando.comando == "reset":
        simulador.reset()
        mensaje = "Simulación reiniciada"
    else:
        return ControlResponse(
            status="error",
            mensaje="Comando no reconocido"
        )
    
    # Enviar estado actualizado a todos
    await broadcast_estado(simulador.obtener_estado())
    
    return ControlResponse(
        status="success",
        mensaje=mensaje
    )


@app.post("/simulacion/start", response_model=ControlResponse)
async def iniciar_simulacion_con_target(start: StartRequest):
    """Inicia o configura la simulación con target y modo (auto/manual)"""
    simulador.set_target(start.target, start.auto)

    if start.auto:
        mensaje = f"Simulación iniciada (target={start.target})"
    else:
        mensaje = f"Target seteado a {start.target} (modo manual)"

    await broadcast_estado(simulador.obtener_estado())

    return ControlResponse(status="success", mensaje=mensaje)


@app.post("/simulacion/step", response_model=ControlResponse)
async def step_simulacion():
    """Avanza la simulación un paso sin iniciar el loop continuo"""
    await simulador.simular_paso(forzado=True)
    await broadcast_estado(simulador.obtener_estado())

    return ControlResponse(
        status="success",
        mensaje="Simulación avanzada un paso"
    )


@app.post("/procesos", response_model=Proceso)
async def crear_proceso(proceso: NuevoProceso):
    """Añade un nuevo proceso a la línea"""
    tareas_iniciales = [
        Tarea(
            id=index + 1,
            nombre=tarea_input.nombre or f"Tarea {index + 1}",
            ciclos_totales=max(1, tarea_input.ciclos_totales),
            estado="espera",
        )
        for index, tarea_input in enumerate(proceso.tareas)
    ]

    nuevo_proceso = simulador.agregar_proceso(proceso.nombre, tareas_iniciales or None)

    if not tareas_iniciales:
        nuevo_proceso = simulador.procesos[-1]

    logger.info(f"Proceso creado: {nuevo_proceso.nombre} (ID: {nuevo_proceso.id})")
    
    # Enviar estado actualizado
    await broadcast_estado(simulador.obtener_estado())
    
    return nuevo_proceso


@app.post("/procesos/{proceso_id}/tareas", response_model=Tarea)
async def crear_tarea(proceso_id: int, tarea: NuevaTarea):
    """Añade una nueva tarea a un proceso"""
    nueva_tarea = simulador.agregar_tarea_a_proceso(
        proceso_id,
        tarea.nombre,
        tarea.ciclos_totales,
    )

    await broadcast_estado(simulador.obtener_estado())

    return nueva_tarea


@app.delete("/procesos/{proceso_id}")
async def eliminar_proceso(proceso_id: int):
    """Elimina un proceso"""
    try:
        eliminado = simulador.eliminar_proceso(proceso_id)
    except ValueError as error:
        return ControlResponse(status="error", mensaje=str(error))

    await broadcast_estado(simulador.obtener_estado())

    return ControlResponse(status="success", mensaje=f"{eliminado.nombre} eliminado")


@app.delete("/procesos/{proceso_id}/tareas/{tarea_id}")
async def eliminar_tarea(proceso_id: int, tarea_id: int):
    """Elimina una tarea de un proceso"""
    try:
        eliminada = simulador.eliminar_tarea_de_proceso(proceso_id, tarea_id)
    except ValueError as error:
        return ControlResponse(status="error", mensaje=str(error))

    await broadcast_estado(simulador.obtener_estado())

    return ControlResponse(status="success", mensaje=f"{eliminada.nombre} eliminada")


@app.get("/procesos")
async def obtener_procesos():
    """Retorna la lista de procesos"""
    return simulador.procesos


# ==================== WebSocket ====================

@app.websocket("/ws/simulacion")
async def websocket_simulacion(websocket: WebSocket):
    """WebSocket para recibir actualizaciones en tiempo real de la simulación"""
    await websocket.accept()
    conexiones_ws.add(websocket)
    logger.info(f"Cliente WebSocket conectado. Total conexiones: {len(conexiones_ws)}")
    
    try:
        # Enviar estado inicial
        await websocket.send_text(simulador.obtener_estado().model_dump_json())
        
        # Mantener la conexión abierta
        while True:
            # Esperar mensajes del cliente (si los hay)
            datos = await websocket.receive_text()
            logger.info(f"Mensaje recibido: {datos}")
            
    except WebSocketDisconnect:
        conexiones_ws.discard(websocket)
        logger.info(f"Cliente WebSocket desconectado. Total conexiones: {len(conexiones_ws)}")
    except Exception as e:
        logger.error(f"Error en WebSocket: {e}")
        conexiones_ws.discard(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
