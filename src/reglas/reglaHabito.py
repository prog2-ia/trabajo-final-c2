from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from typing import TYPE_CHECKING, List

# evito importar Registro directamente para no crear dependencia circular
if TYPE_CHECKING:
    from habitos.registro import Registro


# clase base abstracta para todas las reglas, no se puede usar sola
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

        # guardo todo en minúsculas para evitar problemas con "Diario" vs "diario"
        self._frecuencia = value.lower()


    # MÉTODO ABSTRACTO
    # cada subclase define su propia lógica para saber si el hábito se cumplió
    @abstractmethod
    def cumplido(
        self,
        registros: List[Registro],
        inicio: date,
        fin: date
    ) -> bool:
        pass


    # REPRESENTACIÓN

    def __str__(self) -> str:
        return f"{type(self).__name__}(frecuencia='{self._frecuencia}')"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(frecuencia={self._frecuencia!r})"
