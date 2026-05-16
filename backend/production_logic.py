import asyncio
import json
from typing import Any, Awaitable, Callable, Dict, List, Optional

try:
    from Objects.LineaProduccion import LineaProduccion
    from Objects.Proceso import Proceso
    from Objects.Producto import Producto
    from Objects.Tarea import Tarea
    from Objects.GeneradorReportes import GeneradorReportes
except ImportError:  # pragma: no cover - fallback for package-style imports
    from backend.Objects.LineaProduccion import LineaProduccion
    from backend.Objects.Proceso import Proceso
    from backend.Objects.Producto import Producto
    from backend.Objects.Tarea import Tarea
    from backend.Objects.GeneradorReportes import GeneradorReportes


Callback = Callable[[Dict[str, Any]], Awaitable[None]]


class ProductionLogic:
    """Motor de producción basado en el flujo del test legacy."""

    def __init__(self) -> None:
        self._callbacks: List[Callback] = []
        self._loop_task: Optional[asyncio.Task] = None
        self.eventos: List[str] = []
        self._ultimo_finalizados = 0
        self._configuracion_inicial: Dict[str, Any] = self._configuracion_defecto()
        self._reconstruir_linea(self._configuracion_inicial, auto=False)

    @property
    def t_actual(self) -> int:
        return self.linea.tiempo_total_linea

    def _configuracion_defecto(self) -> Dict[str, Any]:
        return {
            "procesos": [
                {"proceso": 1, "tareas": [{"ciclos_totales": 2}, {"ciclos_totales": 3}]},
                {"proceso": 2, "tareas": [{"ciclos_totales": 4}, {"ciclos_totales": 5}]},
                {"proceso": 3, "tareas": [{"ciclos_totales": 2}, {"ciclos_totales": 1}]},
            ],
            "cantidad_productos": 0,
            "auto": False,
        }

    def _extraer_valor(self, item: Any, nombre: str, predeterminado: Any = None) -> Any:
        if isinstance(item, dict):
            return item.get(nombre, predeterminado)
        return getattr(item, nombre, predeterminado)

    def _reconectar_tareas(self, proceso: Proceso) -> None:
        tareas = list(proceso.lista_tareas)
        for indice, tarea in enumerate(tareas):
            if indice < len(tareas) - 1:
                tarea.enlazar_tarea(tareas[indice + 1])
            else:
                tarea.tarea_siguiente = None
                tarea.tarea_final = True

    def _reconectar_procesos(self) -> None:
        procesos = list(self.linea._lista_procesos)
        if procesos:
            self.linea._proceso_inicial = procesos[0]
            self.linea._proceso_final = procesos[-1]
            
        for indice, proceso in enumerate(procesos):
            proceso._proceso_inicial = indice == 0
            proceso._proceso_final = indice == len(procesos) - 1
            proceso._proceso_siguiente = procesos[indice + 1] if indice < len(procesos) - 1 else None
            self._reconectar_tareas(proceso)

    def _crear_proceso_desde_configuracion(self, proceso_configuracion: Any, indice: int) -> Proceso:
        proceso_id = int(self._extraer_valor(proceso_configuracion, "proceso", indice))
        tareas_configuracion = self._extraer_valor(proceso_configuracion, "tareas", []) or []

        proceso = Proceso(proceso_id, proceso_inicial=indice == 1)
        for posicion, tarea_configuracion in enumerate(tareas_configuracion, start=1):
            proceso.agregar_tarea(self._crear_tarea_desde_configuracion(tarea_configuracion, posicion))

        return proceso

    def _crear_tarea_desde_configuracion(self, tarea_configuracion: Any, indice: int) -> Tarea:
        ciclos = int(self._extraer_valor(tarea_configuracion, "ciclos_totales", 1))
        return Tarea(indice, max(1, ciclos))

    def _crear_producto(self, identificador: int) -> Producto:
        producto = Producto(identificador, f"Producto-{identificador}")
        producto.tiempo_ent = 0
        return producto

    def _reconstruir_linea(self, configuracion: Dict[str, Any], auto: bool) -> None:
        self.linea = LineaProduccion()
        self.reportes = GeneradorReportes()
        self.ejecutando = bool(auto)
        self.eventos = []
        self._ultimo_finalizados = 0

        procesos_configuracion = configuracion.get("procesos", []) or []
        for indice, proceso_configuracion in enumerate(procesos_configuracion, start=1):
            self.linea.agregar_proceso(self._crear_proceso_desde_configuracion(proceso_configuracion, indice))

        if not self.linea._lista_procesos:
            self.linea.agregar_proceso(self._crear_proceso_desde_configuracion({"proceso": 1, "tareas": [{"ciclos_totales": 2}]}, 1))

        self._reconectar_procesos()

        cantidad_productos = int(configuracion.get("cantidad_productos", 0) or 0)
        proceso_inicial = self.linea._lista_procesos[0]
        for identificador in range(1, cantidad_productos + 1):
            proceso_inicial.agregar_producto(self._crear_producto(identificador))

        self.linea.en_pausa = not self.ejecutando
        self.eventos.append("t=0: configuración cargada")
        self._configuracion_inicial = {
            "procesos": configuracion.get("procesos", []),
            "cantidad_productos": cantidad_productos,
            "auto": bool(auto),
        }

    def registrar_callback(self, callback: Callback) -> None:
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def _calcular_productos_en_espera(self) -> int:
        return sum(proceso.productos.qsize() for proceso in self.linea._lista_procesos)

    def _calcular_productos_finalizados(self) -> int:
        return self.linea.productos_finalizados.qsize()

    def _serializar_tarea(self, tarea: Tarea) -> Dict[str, Any]:
        if tarea.esta_procesando():
            estado = "procesando"
        elif tarea.producto is not None:
            estado = "idle"
        else:
            estado = "espera"

        ciclos_actuales = tarea.tiempo_proceso - tarea.ciclos_restantes
        return {
            "id": tarea.id,
            "nombre": f"Tarea {tarea.id}",
            "estado": estado,
            "ciclos_actuales": max(0, ciclos_actuales),
            "ciclos_totales": tarea.tiempo_proceso,
            "tiempo_espera_total": tarea.tiempo_espera_promedio,
        }

    def _serializar_proceso(self, proceso: Proceso) -> Dict[str, Any]:
        return {
            "id": proceso.id,
            "nombre": f"Proceso {proceso.id}",
            "en_espera": proceso.productos.qsize(),
            "tareas": [self._serializar_tarea(tarea) for tarea in proceso.lista_tareas],
            "tiempo_total": proceso.tiempo_total,
            "tiempo_inactivo": proceso.tiempo_inactivo,
        }

    def _construir_metricas(self) -> Dict[str, Any]:
        metricas = json.loads(
            self.reportes.mostrar_stats(self.linea._lista_procesos, self.linea.productos_finalizados)
        )
        metricas["productos_completados"] = self._calcular_productos_finalizados()
        metricas["productos_en_espera"] = self._calcular_productos_en_espera()
        return metricas

    def _registrar_productos_finalizados(self) -> None:
        productos_finalizados = list(self.linea.productos_finalizados.queue)
        if len(productos_finalizados) <= self._ultimo_finalizados:
            return

        nuevos = productos_finalizados[self._ultimo_finalizados :]
        for producto in nuevos:
            nombre_producto = getattr(producto, "nombre", f"Producto-{getattr(producto, 'id', '?')}")
            self.eventos.append(f"t={self.t_actual}: {nombre_producto} completado")

        self._ultimo_finalizados = len(productos_finalizados)

    def obtener_estado(self) -> Dict[str, Any]:
        return {
            "t_actual": self.t_actual,
            "ejecutando": self.ejecutando,
            "procesos": [self._serializar_proceso(proceso) for proceso in self.linea._lista_procesos],
            "eventos": self.eventos[-10:],
            "metricas": self._construir_metricas(),
        }

    async def _notificar_cambio(self) -> None:
        estado = self.obtener_estado()
        for callback in list(self._callbacks):
            try:
                await callback(estado)
            except Exception:
                pass

    async def _avanzar_ciclo(self) -> None:
        self.linea.procesar_ciclo()
        self.linea.parar_linea()
        self._registrar_productos_finalizados()
        if self.linea.en_pausa:
            self.ejecutando = False
        await self._notificar_cambio()

    async def simular_paso(self, forzado: bool = False) -> None:
        if not self.ejecutando and not forzado:
            return
        await self._avanzar_ciclo()

    def start(self) -> None:
        self.ejecutando = True
        self.linea.reanudar()

    def pause(self) -> None:
        self.ejecutando = False
        self.linea.pausar()

    def reset(self) -> None:
        self._reconstruir_linea(self._configuracion_inicial, auto=False)

    def configurar_desde_inicio(self, procesos_configuracion: Any, cantidad_productos: int, auto: bool = True) -> None:
        configuracion = {
            "procesos": procesos_configuracion,
            "cantidad_productos": cantidad_productos,
            "auto": auto,
        }
        self._reconstruir_linea(configuracion, auto=auto)

    def agregar_proceso(self, nombre: Optional[str] = None, tareas_iniciales: Optional[List[Tarea]] = None) -> Dict[str, Any]:
        proceso_id = max((proceso.id for proceso in self.linea._lista_procesos), default=0) + 1
        proceso = Proceso(proceso_id, proceso_inicial=False)

        if tareas_iniciales:
            for indice, tarea in enumerate(tareas_iniciales, start=1):
                proceso.agregar_tarea(self._crear_tarea_desde_configuracion(tarea, indice))
        else:
            proceso.agregar_tarea(Tarea(1, 3))

        self.linea.agregar_proceso(proceso)
        self._reconectar_procesos()
        self.eventos.append(f"t={self.t_actual}: Proceso {proceso.id} agregado")
        return self._serializar_proceso(proceso)

    def agregar_tarea_a_proceso(self, proceso_id: int, nombre: Optional[str] = None, ciclos_totales: int = 3) -> Dict[str, Any]:
        proceso = next((item for item in self.linea._lista_procesos if item.id == proceso_id), None)
        if proceso is None:
            raise ValueError(f"Proceso {proceso_id} no encontrado")

        tarea = Tarea(len(proceso.lista_tareas) + 1, max(1, ciclos_totales))
        proceso.agregar_tarea(tarea)
        self._reconectar_tareas(proceso)
        self.eventos.append(f"t={self.t_actual}: Tarea {tarea.id} agregada en Proceso {proceso.id}")
        return self._serializar_tarea(tarea)

    def eliminar_proceso(self, proceso_id: int) -> Dict[str, Any]:
        for indice, proceso in enumerate(self.linea._lista_procesos):
            if proceso.id == proceso_id:
                eliminado = self.linea._lista_procesos.pop(indice)
                self._reconectar_procesos()
                self.eventos.append(f"t={self.t_actual}: Proceso {eliminado.id} eliminado")
                return self._serializar_proceso(eliminado)
        raise ValueError(f"Proceso {proceso_id} no encontrado")

    def eliminar_tarea_de_proceso(self, proceso_id: int, tarea_id: int) -> Dict[str, Any]:
        proceso = next((item for item in self.linea._lista_procesos if item.id == proceso_id), None)
        if proceso is None:
            raise ValueError(f"Proceso {proceso_id} no encontrado")

        for indice, tarea in enumerate(proceso.lista_tareas):
            if tarea.id == tarea_id:
                eliminada = proceso.lista_tareas.pop(indice)
                self._reconectar_tareas(proceso)
                self.eventos.append(
                    f"t={self.t_actual}: Tarea {eliminada.id} eliminada de Proceso {proceso.id}"
                )
                return self._serializar_tarea(eliminada)

        raise ValueError(f"Tarea {tarea_id} no encontrada en Proceso {proceso_id}")

    async def iniciar_loop(self) -> None:
        while True:
            if self.ejecutando:
                await asyncio.sleep(1)
                await self._avanzar_ciclo()
            else:
                await asyncio.sleep(0.2)


simulador = ProductionLogic()