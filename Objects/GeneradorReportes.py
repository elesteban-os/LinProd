import json
from typing import List, Optional
from queue import Queue
from Objects.Proceso import Proceso
from Objects.Producto import Producto

class GeneradorReportes:
    def __init__(self):
        pass

    def calcula_tiempo_prom(self, productos_finalizados: Queue[Producto]) -> float:
        """
        Calcula el tiempo promedio que tardan los productos en la línea 
        (tiempo de salida - tiempo de entrada).
        """
        if productos_finalizados.empty():
            return 0.0
        
        productos = list(productos_finalizados.queue)
        tiempo_total_acumulado = 0
        
        for p in productos:
            tiempo_total_acumulado += p.get_tiempo_total()
            
        return tiempo_total_acumulado / len(productos)

    def encontrar_cuellobotella(self, lista_procesos: List[Proceso]) -> Optional[Proceso]:
        """
        Busca el proceso (omitiendo el inicial) que tiene más productos en su cola.
        Esto representa el proceso donde se están 'atorando' los productos.
        """
        cuello_botella: Optional[Proceso] = None
        max_productos = -1
        
        for proceso in lista_procesos:
            # Omitiremos el proceso inicial ya que es el que recibe el stock base
            if proceso._proceso_inicial:
                continue
                
            en_cola = proceso.productos.qsize()
            if en_cola > max_productos:
                max_productos = en_cola
                cuello_botella = proceso
                
        return cuello_botella

    def mostrar_stats(self, lista_procesos: List[Proceso], productos_finalizados: Queue[Producto]) -> str:
        """
        Construye y devuelve un string JSON con las métricas requeridas 
        actualizadas al ciclo en curso.
        """
        tiempo_primer_producto = 0
        tiempo_ultimo_producto = 0
        tiempo_total_procesamiento = 0
        
        # Recuperamos la lista sin vaciar el Queue original
        productos_lista = list(productos_finalizados.queue)
        
        if productos_lista:
            # Primer elemento de la cola de finalizados
            tiempo_primer_producto = productos_lista[0].get_tiempo_total()
            # Último elemento depositado en la cola finalizados
            tiempo_ultimo_producto = productos_lista[-1].get_tiempo_total()
            # Tiempo total de procesamiento sumado de todos los productos
            tiempo_total_procesamiento = sum(p.get_tiempo_total() for p in productos_lista)

        promedio = self.calcula_tiempo_prom(productos_finalizados)
        cb = self.encontrar_cuellobotella(lista_procesos)
        
       
        total_espera_tareas = 0
        cantidad_tareas = 0
        max_espera = -1
        proc_max = None
        tarea_max = None
        
        for proceso in lista_procesos:
            for tarea in proceso.lista_tareas:
                # Acumular tiempo promedio de espera de la tarea
                total_espera_tareas += tarea.tiempo_espera_promedio
                cantidad_tareas += 1
                
                # Encontrar el mayor tiempo de espera y su origen
                if tarea.contador_max_espera > max_espera:
                    max_espera = tarea.contador_max_espera
                    proc_max = proceso
                    tarea_max = tarea

        promedio_espera_tareas = total_espera_tareas / cantidad_tareas if cantidad_tareas > 0 else 0
        
        info_procesos = []
        for proceso in lista_procesos:
            info_procesos.append({
                "proceso": proceso.id,
                "tareas_procesando": [tarea.id for tarea in proceso.lista_tareas if tarea.esta_procesando()],
                "tiempo_total": proceso.tiempo_total,
                "tiempo_inactivo": proceso.tiempo_inactivo
            })
        
        datos = {
            "tiempo_primer_producto": tiempo_primer_producto,
            "tiempo_ultimo_producto": tiempo_ultimo_producto,
            "tiempo_promedio_linea": promedio,
            "tiempo_total_todos_productos": tiempo_total_procesamiento,
            "cuello_de_botella": cb.id if cb and cb.productos.qsize() > 0 else "Ninguno",
            "promedio_espera_tareas": promedio_espera_tareas,
            "mayor_espera": max_espera if max_espera > 0 else 0,
            "estado_procesos": info_procesos
        }
        
        return json.dumps(datos, indent=4)


#Mandar en .json