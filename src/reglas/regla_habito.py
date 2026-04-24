from abc import ABC, abstractmethod
from datetime import date
from typing import List

from habitos.registro import Registro


class ReglaHabito(ABC):

    def __init__(self, frecuencia: str) -> None:
        self.frecuencia = frecuencia

    # FRECUENCIA
   
    @property
    def frecuencia(self) -> str:
        return self._frecuencia

    @frecuencia.setter
    def frecuencia(self, value: str) -> None:
        if value is None:
            raise ValueError("La frecuencia no puede ser None")

        value = value.strip()

        if value == "":
            raise ValueError("La frecuencia no puede estar vacía")

        self._frecuencia = value.lower()

   
    # MÉTODO ABSTRACTO

    @abstractmethod
    def cumplido(
        self,
        registros: List[Registro],
        inicio: date,
        fin: date
    ) -> bool:
        """
        Devuelve True si la regla se cumple en el periodo [inicio, fin].
        """
        pass

   
    # REPRESENTACIÓN
  
    def __str__(self) -> str:
        return f"{type(self).__name__}(frecuencia='{self._frecuencia}')"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(frecuencia={self._frecuencia!r})"