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
        self.en_pausa: bool = False
        
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
                producto_terminado.tiempo_sal = self.tiempo_total_linea
                self.productos_finalizados.put(producto_terminado)

    def actualizacion(self) -> None:
        if self.en_pausa:
            # Si esta pausado, igual simulamos el tiempo de retardo para la GUI 
            # pero no avanzamos ciclo ni cálculos
            time.sleep(1)
            return

        self._reloj = True
        time.sleep(1) # Pausa de 1 segundo para simular tiempo real
        self.procesar_ciclo()

    def pausar(self) -> None:
        """Pausa la línea de producción"""
        self.en_pausa = True

    def reanudar(self) -> None:
        """Reanuda la línea de producción"""
        self.en_pausa = False

    def parar_linea(self) -> None:
        """Verifica que la línea de producción esté vacía y detiene (pausa) todo si es así."""
        linea_vacia = True
        for proceso in self._lista_procesos:
            # Chequea que la cola de productos esté vacía y que ninguna tarea esté procesando
            hay_procesando = any(tarea.esta_procesando() for tarea in proceso.lista_tareas)
            
            if not proceso.productos.empty() or hay_procesando:
                linea_vacia = False
                break
                
        if linea_vacia:
            self.en_pausa = True
       

