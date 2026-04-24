from .habito import Habito
from reglas.reglaHabito import ReglaHabito
from datetime import date

class HabitoNumerico(Habito):

    def __init__(self, id: str, nombre: str, regla: ReglaHabito, unidad_medida: str, activa: bool = True) -> None:
        super().__init__(id, nombre, regla, activa)
        self.unidad_medida = unidad_medida

    @property
    def unidad_medida(self) -> str:
        return self._unidad_medida
    
    @unidad_medida.setter
    def unidad_medida(self, value: str) -> None:
        if value is None or value.strip() == "":
            raise ValueError("La unidad de medida no puede estar vacía")
        self._unidad_medida = value.strip()

    def registrar(self, fecha: date, valor: int | float) -> None:
        if type(valor) not in (int, float):
            raise TypeError("El valor tiene que ser numérico")
        super().registrar(fecha, valor)