from backend.Objects.Tarea import Tarea
from queue import Queue

def procesar_ciclo(tareas: list[Tarea]) -> None:
    for tarea in tareas:
        producto = tarea.procesar_ciclo()
        print(tarea)
        print(f"        - Tiempo de espera prom: {tarea.tiempo_espera_promedio}")
        print(f"        - Tiempo de espera maximo: {tarea.contador_max_espera}")
        if producto is not None:
            print(f"Producto: {producto} ha sido completado todas las tareas")

if __name__ == "__main__":
    tareas = []
    tarea1 = Tarea(1, 3)
    tarea2 = Tarea(2, 5)
    tarea3 = Tarea(3, 1)
    tareas.append(tarea1)
    tareas.append(tarea2)
    tareas.append(tarea3)

    tarea1.enlazar_tarea(tarea2)
    tarea2.enlazar_tarea(tarea3)

    producto = "Producto A"
    producto2 = "Producto B"
    productos = Queue()
    productos.put(producto)
    productos.put(producto2)

    for ciclo in range(10):
        print(f"Ciclo {ciclo + 1} -------------------------------")
        if not tareas[0].esta_procesando():
            producto_actual = productos.get()
            tareas[0].asignar_producto(producto_actual)
        procesar_ciclo(tareas)
