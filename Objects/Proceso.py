from queue import Queue

class Proceso:
    def __init__(self, id: int, proceso_inicial: bool) -> None:
        self.id = id
        self._proceso_inicial = proceso_inicial
        self._proceso_final = True
        self._proceso_siguiente = None
        self._contador_inactivo = 0
        self._primer_producto_recibido = False

        
        self.productos = Queue()
        self.lista_tareas = []
        self.contador_ciclos = 0
        self.tiempo_total = 0
        self.tiempo_inactivo = 0
    
    def reiniciar_proceso(self) -> bool:
        while not self.productos.empty():
            try:
                self.productos.get_nowait()
            except self.productos.Empty:
                break
        self.lista_tareas = []
        self.contador_ciclos = 0
        self.tiempo_total = 0
        self._contador_inactivo = 0
        self.tiempo_inactivo = 0
        self._primer_producto_recibido = False

    def agregar_tarea(self, tarea) -> None:
        if self.lista_tareas == []:
            self.lista_tareas.append(tarea)
        else:
            self.lista_tareas[-1:][0].enlazar_tarea(tarea)
            self.lista_tareas.append(tarea)
    
    def enlazar_proceso(self, proceso) -> None:
        self._proceso_siguiente = proceso
        self._proceso_final = False

    def agregar_producto(self, producto) -> None:
        self.productos.put(producto)
        self._primer_producto_recibido = True
    
    def obtener_tiempo_total(self) -> int:
        return self.tiempo_total
    
    def _actualizar_tiempo(self) -> None:
        hay_procesando = any(tarea.esta_procesando() for tarea in self.lista_tareas)
        hay_productos = not self.productos.empty()
        if hay_procesando:
            self.contador_ciclos += 1
            if self.contador_ciclos > self.tiempo_total:
                self.tiempo_total = self.contador_ciclos
        else:
            self.contador_ciclos = 0 # Reiniciar si no hay productos ni tareas procesando.
            if self._primer_producto_recibido:
                self._contador_inactivo += 1
            if self._contador_inactivo > self.tiempo_inactivo:
                self.tiempo_inactivo = self._contador_inactivo 
    
    def procesar_ciclo(self):
        producto_salida = None
        if self._primer_producto_recibido:
            PRIMERA_TAREA = 0
            primera_tarea_libre = not self.lista_tareas[PRIMERA_TAREA].esta_procesando()
            if primera_tarea_libre and not self.productos.empty():
                producto_actual = self.productos.get()
                self.lista_tareas[PRIMERA_TAREA].asignar_producto(producto_actual)
            for tarea in self.lista_tareas:
                producto_finalizado = tarea.procesar_ciclo()
                if producto_finalizado is not None:
                    if not self._proceso_final:    
                        self._proceso_siguiente.agregar_producto(producto_finalizado)
                    else:
                        producto_salida = producto_finalizado
            self._actualizar_tiempo()
        return producto_salida

    def obtener_estado(self) -> str:
        return f"""Proceso {self.id}
        - Productos en cola: {','.join(str(producto.nombre) for producto in self.productos.queue)}
        - Tareas procesando: {','.join(str(tarea.id) for tarea in self.lista_tareas if tarea.esta_procesando())}
        - Tiempo Total: {self.tiempo_total} 
        - Tiempo Inactivo: {self.tiempo_inactivo}
        """

    def __str__(self) -> str:
        return f"""Proceso {self.id} 
        - Tareas:\n {"\n".join(str(tarea) for tarea in self.lista_tareas)}
        ---------------------------------------------------------------
        - Tiempo Total: {self.tiempo_total} 
        - Tiempo Inactivo: {self.tiempo_inactivo}
        - Proceso Siguiente: {self._proceso_siguiente.id if self._proceso_siguiente else "No hay proceso siguiente"}"""