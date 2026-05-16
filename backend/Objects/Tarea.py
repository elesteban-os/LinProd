
class Tarea():
    def __init__(self, id: int, tiempo_proceso: int):
        self.id = id
        self.tiempo_proceso = tiempo_proceso
        self._esta_procesando = False
        self.ciclos_restantes = tiempo_proceso
        self.producto = None
        self.tarea_siguiente = None
        self._contador_en_espera = 0
        self.contador_max_espera = 0
        self.tiempo_espera_promedio = 0
        self.tarea_final = True

    def asignar_producto(self, producto) -> None:
        self._esta_procesando = True
        self.producto = producto
    
    def actualizar_espera_promedio(self) -> None:
        if self.tiempo_espera_promedio == 0:
            self.tiempo_espera_promedio = self.contador_max_espera
        else:
            self.tiempo_espera_promedio = (self.tiempo_espera_promedio + self._contador_en_espera)/2
    
    def reiniciar_tarea(self) -> None:
        # self.ciclos_restantes = self.tiempo_proceso
        # self._esta_procesando = False
        # self.producto = None
        # self._contador_en_espera = 0
        self.ciclos_restantes = self.tiempo_proceso
        self._esta_procesando = False
        self.producto = None
        self.actualizar_espera_promedio()
        self._contador_en_espera = 0


    def verificar_max_espera(self) -> None:
        if self._contador_en_espera > self.contador_max_espera:
            self.contador_max_espera = self._contador_en_espera

    def incrementar_espera(self) -> None:
        self._contador_en_espera += 1
        self.verificar_max_espera()        

    def esta_completa(self) -> bool:
        return self.ciclos_restantes == 0
    
    def esta_procesando(self) -> bool:
        return self._esta_procesando

    def enlazar_tarea(self, tarea: "Tarea") -> None:
        self.tarea_siguiente = tarea
        self.tarea_final = False

    def transferir_producto(self) -> bool:
        if self.producto and not self.tarea_siguiente.esta_procesando():
            self.tarea_siguiente.asignar_producto(self.producto)
            return True
        return False

    def procesar_ciclo(self):
        if self.ciclos_restantes > 0 and self._esta_procesando:
            self.ciclos_restantes -= 1
        else:
            if self.producto is not None:
                if self.tarea_final:
                    producto = self.producto
                    self.reiniciar_tarea()
                    return producto
                else:
                    if self.transferir_producto():
                        self.reiniciar_tarea()
                    else: self.incrementar_espera()
            else:
                return None      

    def __str__(self) -> str:
        return f"""Tarea {self.id} 
        - Tiempo Proceso: {self.tiempo_proceso} 
        - Procesando: {self._esta_procesando} 
        - Ciclos Restantes: {self.ciclos_restantes} 
        - Producto: {self.producto}
        - Tarea Siguiente: {self.tarea_siguiente.id if self.tarea_siguiente else "No hay tarea siguiente"}"""