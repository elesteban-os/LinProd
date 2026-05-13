import asyncio
import random
from datetime import datetime
from typing import Optional
from models import Proceso, Tarea, EstadoSistema


class SimuladorLinea:
    """Simulador de la línea de producción"""
    
    def __init__(self):
        self.ejecutando = False
        self.t_actual = 0
        self.procesos = self._inicializar_procesos()
        self.eventos = []
        self.metricas = {
            "productos_completados": 0,
            "tiempo_flujo": 0,
            "cuello_botella": None
        }
        self.callbacks = []
    
    def _inicializar_procesos(self) -> list[Proceso]:
        """Inicializa los procesos con sus tareas"""
        procesos = []
        
        for i in range(1, 5):
            tareas = []
            for j in range(1, random.randint(3, 5) + 1):
                tarea = Tarea(
                    id=j,
                    nombre=f"Tarea {j}",
                    ciclos_totales=random.randint(1, 3),
                    estado="espera"
                )
                tareas.append(tarea)
            
            proceso = Proceso(
                id=i,
                nombre=f"Proceso {i}",
                en_espera=random.randint(0, 5),
                tareas=tareas
            )
            procesos.append(proceso)
        
        return procesos

    def agregar_proceso(self, nombre: Optional[str] = None, tareas_iniciales: Optional[list[Tarea]] = None) -> Proceso:
        """Crea un nuevo proceso con una tarea inicial"""
        max_id = max((proceso.id for proceso in self.procesos), default=0)
        proceso_id = max_id + 1

        if tareas_iniciales:
            tareas = tareas_iniciales
        else:
            tareas = [
                Tarea(
                    id=1,
                    nombre="Tarea 1",
                    ciclos_totales=random.randint(1, 3),
                    estado="espera"
                )
            ]

        proceso = Proceso(
            id=proceso_id,
            nombre=nombre or f"Proceso {proceso_id}",
            en_espera=random.randint(0, 5),
            tareas=tareas
        )
        self.procesos.append(proceso)
        self.eventos.append(f"t={self.t_actual}: {proceso.nombre} agregado")
        return proceso

    def agregar_tarea_a_proceso(self, proceso_id: int, nombre: Optional[str] = None, ciclos_totales: int = 3) -> Tarea:
        """Agrega una tarea a un proceso existente"""
        proceso = next((item for item in self.procesos if item.id == proceso_id), None)
        if proceso is None:
            raise ValueError(f"Proceso {proceso_id} no encontrado")

        max_id = max((tarea.id for tarea in proceso.tareas), default=0)
        tarea = Tarea(
            id=max_id + 1,
            nombre=nombre or f"Tarea {max_id + 1}",
            ciclos_totales=max(1, ciclos_totales),
            estado="espera"
        )
        proceso.tareas.append(tarea)
        self.eventos.append(f"t={self.t_actual}: {tarea.nombre} agregada en {proceso.nombre}")
        return tarea

    def eliminar_proceso(self, proceso_id: int) -> Proceso:
        """Elimina un proceso existente"""
        for index, proceso in enumerate(self.procesos):
            if proceso.id == proceso_id:
                eliminado = self.procesos.pop(index)
                self.eventos.append(f"t={self.t_actual}: {eliminado.nombre} eliminado")
                return eliminado
        raise ValueError(f"Proceso {proceso_id} no encontrado")

    def eliminar_tarea_de_proceso(self, proceso_id: int, tarea_id: int) -> Tarea:
        """Elimina una tarea de un proceso"""
        proceso = next((item for item in self.procesos if item.id == proceso_id), None)
        if proceso is None:
            raise ValueError(f"Proceso {proceso_id} no encontrado")

        for index, tarea in enumerate(proceso.tareas):
            if tarea.id == tarea_id:
                eliminada = proceso.tareas.pop(index)
                self.eventos.append(
                    f"t={self.t_actual}: {eliminada.nombre} eliminada de {proceso.nombre}"
                )
                return eliminada

        raise ValueError(f"Tarea {tarea_id} no encontrada en Proceso {proceso_id}")
    
    def registrar_callback(self, callback):
        """Registra un callback para ser llamado cuando el estado cambia"""
        self.callbacks.append(callback)
    
    async def _notificar_cambio(self):
        """Notifica a todos los callbacks registrados"""
        estado = self.obtener_estado()
        for callback in self.callbacks:
            try:
                await callback(estado)
            except Exception as e:
                print(f"Error en callback: {e}")
    
    async def simular_paso(self, forzado: bool = False):
        """Simula un paso de tiempo"""
        if not self.ejecutando and not forzado:
            return
        
        self.t_actual += 1
        
        # Actualizar estados de tareas
        for proceso in self.procesos:
            for tarea in proceso.tareas:
                if tarea.estado == "procesando":
                    tarea.ciclos_actuales += 1
                    if tarea.ciclos_actuales >= tarea.ciclos_totales:
                        tarea.estado = "idle"
                        tarea.ciclos_actuales = 0
                        self.eventos.append(
                            f"t={self.t_actual}: {tarea.nombre} completada en {proceso.nombre}"
                        )
                        self.metricas["productos_completados"] += 1
                elif tarea.estado == "idle" and random.random() < 0.4:
                    tarea.estado = "procesando"
                    tarea.ciclos_actuales = 0
                    self.eventos.append(
                        f"t={self.t_actual}: {tarea.nombre} iniciada en {proceso.nombre}"
                    )
                elif tarea.estado == "espera" and random.random() < 0.25:
                    tarea.estado = "idle"
                elif tarea.estado == "idle" and random.random() < 0.15:
                    tarea.estado = "espera"
            
            # Actualizar tareas en espera
            if random.random() < 0.3 and proceso.en_espera > 0:
                proceso.en_espera -= 1
        
        # Calcular cuello de botella (proceso con más tareas en espera)
        cuellos = [(p.id, p.en_espera) for p in self.procesos]
        cuello_max = max(cuellos, key=lambda x: x[1])
        self.metricas["cuello_botella"] = f"Proceso {cuello_max[0]}"
        self.metricas["tiempo_flujo"] = self.t_actual
        
        # Limitar eventos a los últimos 20
        if len(self.eventos) > 20:
            self.eventos = self.eventos[-20:]
        
        await self._notificar_cambio()
    
    def obtener_estado(self) -> EstadoSistema:
        """Retorna el estado actual del sistema"""
        return EstadoSistema(
            t_actual=self.t_actual,
            ejecutando=self.ejecutando,
            procesos=self.procesos,
            eventos=self.eventos[-10:],  # Últimos 10 eventos
            metricas=self.metricas
        )
    
    def start(self):
        """Inicia la simulación"""
        self.ejecutando = True
    
    def pause(self):
        """Pausa la simulación"""
        self.ejecutando = False
    
    def reset(self):
        """Resetea la simulación"""
        self.ejecutando = False
        self.t_actual = 0
        self.procesos = self._inicializar_procesos()
        self.eventos = []
        self.metricas = {
            "productos_completados": 0,
            "tiempo_flujo": 0,
            "cuello_botella": None
        }
    
    async def iniciar_loop(self):
        """Loop de simulación que avanza cada 1 segundo"""
        while True:
            await self.simular_paso()
            await asyncio.sleep(1)


# Instancia global del simulador
simulador = SimuladorLinea()
