from .habito import Habito
from reglas.reglaHabito import ReglaHabito
from datetime import date

class HabitoBooleano(Habito):
    def __init__(self, id: str, nombre: str, regla: ReglaHabito, activa: bool = True) -> None:
        super().__init__(id, nombre, regla, activa)

    def registrar(self, fecha: date, valor: bool) -> None:

        if type(valor) is not bool:
            raise TypeError("El valor debe ser booleano")
        
        super().registrar(fecha, valor)