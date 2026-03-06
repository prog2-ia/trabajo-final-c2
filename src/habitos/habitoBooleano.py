from .habito import Habito

class HabitoBooleano(Habito):
    def __init__(self, id, nombre, regla, activa =True):
        super().__init__(id, nombre, regla, activa)

    def registrar(self, fecha, valor):

        if type(valor) is not bool:
            raise TypeError("El valor debe ser booleano")
        
        super().registrar(fecha, valor)