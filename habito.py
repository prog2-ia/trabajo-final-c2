from abc import ABC, abstractmethod
from datetime import date
class Habito(ABC):
    num_habitos = 0

    def __init__(self, nombre, frecuencia, descripcion):
        self.nombre = nombre
        self.frecuencia = frecuencia
        self.descripcion = descripcion

        self.activo = True
        self.registros = list[date] = []
        self.racha_actual = 0
        self.mejor_racha = 0

        type(self).num_habitos += 1

    # Método abstracto

    @abstractmethod
    def cumple_en_periodo(self, inicio: date, fin: date) -> bool:
        """Cada subclase define qué significa cumplir en un periodo."""
        raise NotImplementedError
    
    
    # Métodos de instancia

    def registrar(self, fecha):

        if not isinstance(fecha, date):
            raise TypeError("La fecha debe ser de tipo date.")

        if fecha in self.registros:
            raise ValueError("Registro duplicado.")

        self.registros.append(fecha)
        self.registros.sort()
        self._actualizar_racha()
    
    def activar(self):
        self.activo = True


    def desactivar(self):
        self.activo = False

    def _actualizar_racha(self):

        if len(self.registros) == 0:
            self.racha_actual = 0
            self.mejor_racha = 0
            return

        racha_actual = 1
        mejor_racha = 1

        for i in range(1, len(self.registros)):

            diferencia = (self.registros[i] - self.registros[i - 1]).days

            if diferencia == 1:
                racha_actual += 1
            else:
                racha_actual = 1

            if racha_actual > mejor_racha:
                mejor_racha = racha_actual

        self.racha_actual = racha_actual
        self.mejor_racha = mejor_racha