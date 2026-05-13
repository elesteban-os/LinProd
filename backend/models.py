from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Any, Optional
from datetime import datetime


class Tarea(BaseModel):
    """Modelo para una tarea dentro de un proceso"""
    id: int
    nombre: str
    estado: Literal["espera", "idle", "procesando"] = "espera"
    ciclos_actuales: int = 0
    ciclos_totales: int = 3


class NuevaTarea(BaseModel):
    """Datos para crear una nueva tarea"""
    nombre: Optional[str] = None
    ciclos_totales: int = 3


class NuevoProceso(BaseModel):
    """Datos para crear un nuevo proceso"""
    nombre: Optional[str] = None
    tareas: List[NuevaTarea] = Field(default_factory=list)


class Proceso(BaseModel):
    """Modelo para un proceso en la línea de producción"""
    id: int
    nombre: str
    en_espera: int = 0
    tareas: List[Tarea] = Field(default_factory=list)


class EstadoSistema(BaseModel):
    """Modelo para el estado completo del sistema"""
    t_actual: int = 0
    ejecutando: bool = False
    procesos: List[Proceso] = Field(default_factory=list)
    eventos: List[str] = Field(default_factory=list)
    metricas: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)


class ComandoSimulacion(BaseModel):
    """Modelo para comandos de control de simulación"""
    comando: Literal["start", "pause", "reset"]


class ControlResponse(BaseModel):
    """Respuesta a comandos de control"""
    status: str
    mensaje: str
    timestamp: datetime = Field(default_factory=datetime.now)
