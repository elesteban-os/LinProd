



class Producto:
    """Clase que representa un producto con su ID, nombre, tiempo de entrada y tiempo de salida."""

    def __init__(self, idProducto: int, nombre: str, tiempo_ent: int = 0, tiempo_sal: int = 0):
        # Privado
        self.__ID = idProducto
        self.__tiempo_ent = tiempo_ent
        self.__tiempo_sal = tiempo_sal

        # Público 
        self.nombre = nombre


    # Getters y Setters de los private 
    @property
    def id(self) -> int:
        return self.__ID
    
    @property
    def tiempo_ent(self) -> int:
        return self.__tiempo_ent
    
    @tiempo_ent.setter
    def tiempo_ent(self, tiempo_ent: int):
        self.__tiempo_ent = tiempo_ent

    @property
    def tiempo_sal(self) -> int:
        return self.__tiempo_sal
    @tiempo_sal.setter
    def tiempo_sal(self, tiempo_sal: int):
        self.__tiempo_sal = tiempo_sal


    def get_tiempo_total(self) -> int:
        return self.__tiempo_sal - self.__tiempo_ent