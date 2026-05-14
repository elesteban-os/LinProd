from queue import Queue

class Proceso:
    def __init__(self, id: int, proceso_inicial: bool, proceso_final: bool) -> None:
        self._id = id
        self._proceso_inicial = proceso_inicial
        self._proceso_final = proceso_final
        
        self.productos = Queue()
        self.lista_tareas = []
        self.contador_ciclos = 0
        self.tiempo_total = 0

    def agregar_tarea(self, tarea) -> None:
        self.lista_tareas.append(tarea)

    def agregar_producto(self, producto) -> None:
        self.productos.put(producto)
    
    def obtener_tiempo_total(self) -> int:
        return self.tiempo_total
    
    def procesar_ciclo(self) -> None:
        for tarea in self.lista_tareas:
            if not self.productos.empty():
                if not tarea.esta_procesando():
                    producto_actual = self.productos.get()  # Obtener el producto al frente de la cola
                    tarea.asignar_producto(producto_actual)

                tarea.procesar_ciclo()
                self.contador_ciclos += 1

                if tarea.esta_completa():
                    tarea.extraer_producto()  
                    self.tiempo_total += self.contador_ciclos
                    self.contador_ciclos = 0  
                    tarea.reiniciar_tarea()  