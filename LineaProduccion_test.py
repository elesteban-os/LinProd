from Objects.LineaProduccion import LineaProduccion
from Objects.Proceso import Proceso
from Objects.Tarea import Tarea
from Objects.Producto import Producto
from Objects.GeneradorReportes import GeneradorReportes
import time

def test_linea_produccion():
    print("--- CONFIGURANDO LINEA DE PRODUCCIÓN ---")
    linea = LineaProduccion()

    # Creando Procesos
    proceso1 = Proceso(1, proceso_inicial=True)
    proceso2 = Proceso(2, proceso_inicial=False)

    # Creando Tareas para el proceso 1
    t1 = Tarea(1, 2) # id, tiempo proceso
    t2 = Tarea(2, 3)
    proceso1.agregar_tarea(t1)
    proceso1.agregar_tarea(t2)

    # Creando Tareas para el proceso 2
    t3 = Tarea(3, 1)
    t4 = Tarea(4, 2)
    proceso2.agregar_tarea(t3)
    proceso2.agregar_tarea(t4)

    # Agregando procesos a la línea
    linea.agregar_proceso(proceso1)
    linea.agregar_proceso(proceso2)

  
    
    # Conectando procesos
    linea.conectar_proceso(proceso1, proceso2)

    # Definiendo inicio y fin de la línea
    linea.definir_proceso_inicial(proceso1)
    linea.definir_proceso_final(proceso2)

    # Creando e inyectando productos en el proceso inicial
    for i in range(1, 4):
        prod = Producto(i, f"Producto-{i}") # ID y producto id xd
        proceso1.agregar_producto(prod)

    # Creando el generador de reportes
    reportes = GeneradorReportes()
    
    print("--- INICIANDO SIMULACION ---")
    # Correremos 15 ciclos como prueba
    for ciclo in range(15):
        print(f"\n>>>> Ciclo {ciclo + 1} <<<<")
        
        # Pausa la línea un par de ciclos para evaluar funcion de pausa
        if ciclo == 5:
            print("[SISTEMA] Pausando línea de producción...")
            linea.pausar()
        if ciclo == 14:
            print("[SISTEMA] Reanudando línea de producción...")
            linea.reanudar()
            
        # Actualizamos la línea (esto ejecuta procesar_ciclo internamente y aplica el sleep)
        linea.actualizacion()
        
        print(proceso1.obtener_estado())
        print(proceso2.obtener_estado())
        
        # Obtenemos los reportes actuales del Generador
        print("--- REPORTES EN VIVO ---")
        stats = reportes.mostrar_stats(linea._lista_procesos, linea.productos_finalizados)
        for stat, valor in stats.items():
            print(f"> {stat}: {valor}")
            
        if not linea.productos_finalizados.empty():
            print("--- PRODUCTOS FINALIZADOS RECOPILADOS ---")
            productos_salida = list(linea.productos_finalizados.queue)
            for p in productos_salida:
                print(f"✅ {p.nombre} ha salido de la línea.")

if __name__ == "__main__":
    test_linea_produccion()