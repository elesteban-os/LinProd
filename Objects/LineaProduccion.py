import time
from typing import List, Optional
from queue import Queue
from Objects.Proceso import Proceso
from Objects.Producto import Producto

class LineaProduccion:
    def __init__(self):
        self._lista_procesos: List[Proceso] = []
        self._proceso_inicial: Optional[Proceso] = None
        self._proceso_final: Optional[Proceso] = None
        self._reloj: bool = False
        
        self.tiempo_total_linea: int = 0
        self.productos_finalizados: Queue[Producto] = Queue()

    def agregar_proceso(self, proceso: Proceso) -> None:
        self._lista_procesos.append(proceso)

    def conectar_proceso(self, p1: Proceso, p2: Proceso) -> None:
        p1.enlazar_proceso(p2)

    def definir_proceso_inicial(self, proceso: Proceso) -> None:
        self._proceso_inicial = proceso
        proceso._proceso_inicial = True

    def definir_proceso_final(self, proceso: Proceso) -> None:
        self._proceso_final = proceso
        proceso._proceso_final = True

    def procesar_ciclo(self) -> None:
        self.tiempo_total_linea += 1
        for proceso in self._lista_procesos:
            producto_terminado = proceso.procesar_ciclo()
            if producto_terminado is not None and proceso == self._proceso_final:
                self.productos_finalizados.put(producto_terminado)

    def actualizacion(self) -> None:
        self._reloj = True
        time.sleep(1) # Pausa de 1 segundo para simular tiempo real
        self.procesar_ciclo()
       

