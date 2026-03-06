from .habito import Habito
class HabitoNumerico(Habito):

    def __init__(self, id, nombre, regla, unidad_medida, activa=True):
        super().__init__(id, nombre, regla, activa)
        self.unidad_medida = unidad_medida

    @property
    def unidad_medida(self):
        return self._unidad_medida
    
    @unidad_medida.setter
    def unidad_medida(self, value):
        if value is None or value.strip() == "":
            raise ValueError("La unidad de medida no puede estar vacía")
        self._unidad_medida = value.strip()

    def registrar(self, fecha, valor):
        if type(valor) not in (int, float):
            raise TypeError("El valor tiene que ser numérico")
        super().registrar(fecha, valor)
        