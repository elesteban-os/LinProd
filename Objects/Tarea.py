
class Tarea():
    def __init__(self, id: int, tiempo_proceso: int):
        self.id = id
        self.tiempo_proceso = tiempo_proceso
        self.ciclos_restantes = tiempo_proceso
        self._esta_procesando = False
        self.producto = None

    def asignar_producto(self, producto) -> None:
        self.producto = producto

    def extraer_producto(self):
        producto = self.producto
        return producto

    def procesar_ciclo(self) -> None:
        self.ciclos_restantes -= 1
        self._esta_procesando = True

    def esta_completa(self) -> bool:
        return self.ciclos_restantes == 0
    
    def esta_procesando(self) -> bool:
        return self._esta_procesando
    
    def reiniciar_tarea(self) -> None:
        self.ciclos_restantes = self.tiempo_proceso
        self._esta_procesando = False
        self.producto = None