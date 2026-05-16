from backend.Objects.Proceso import Proceso
from backend.Objects.Tarea import Tarea
from backend.Objects.Producto import Producto

if __name__ == "__main__":
    producto1 = Producto(idProducto=1, nombre="Producto1", tiempo_ent=0, tiempo_sal=0)
    producto2 = Producto(idProducto=2, nombre="Producto2", tiempo_ent=0, tiempo_sal=0)
    producto3 = Producto(idProducto=3, nombre="Producto3", tiempo_ent=0, tiempo_sal=0)
    producto4 = Producto(idProducto=4, nombre="Producto4", tiempo_ent=0, tiempo_sal=0)
    producto5 = Producto(idProducto=5, nombre="Producto5", tiempo_ent=0, tiempo_sal=0)
    producto6 = Producto(idProducto=6, nombre="Producto6", tiempo_ent=0, tiempo_sal=0)

    tarea1 = Tarea(id=1, tiempo_proceso=2)
    tarea2 = Tarea(id=2, tiempo_proceso=3)
    tarea3 = Tarea(id=3, tiempo_proceso=1)
    tarea4 = Tarea(id=4, tiempo_proceso=1)
    tarea5 = Tarea(id=5, tiempo_proceso=2)
    tarea6 = Tarea(id=6, tiempo_proceso=3)

    lista_procesos = []
    proceso1 = Proceso(id=1, proceso_inicial=True) # Tarda 6 ciclos en terminar 1 producto
    proceso2 = Proceso(id=2, proceso_inicial=False) # Tarda 3 ciclos en terminar 1 producto
    proceso3 = Proceso(id=3, proceso_inicial=False)

    proceso1.enlazar_proceso(proceso2)
    proceso2.enlazar_proceso(proceso3)

    proceso1.agregar_tarea(tarea1)
    proceso1.agregar_tarea(tarea2)
    proceso1.agregar_tarea(tarea3)

    proceso2.agregar_tarea(tarea4)
    proceso2.agregar_tarea(tarea5)

    proceso3.agregar_tarea(tarea6)

    proceso1.agregar_producto(producto1)
    proceso1.agregar_producto(producto2)
    proceso1.agregar_producto(producto3)
    proceso1.agregar_producto(producto4)
    proceso1.agregar_producto(producto5)
    proceso1.agregar_producto(producto6)

    lista_procesos.append(proceso1)
    lista_procesos.append(proceso2)
    lista_procesos.append(proceso3)

    for ciclo in range(30):
        print(f"Ciclo {ciclo + 1} -------------------------------")
        for proceso in lista_procesos:
            proceso.procesar_ciclo()
            estado = proceso.obtener_estado()
            print(estado)

