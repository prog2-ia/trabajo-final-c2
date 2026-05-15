from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING, List

from reglas.reglaHabito import ReglaHabito

if TYPE_CHECKING:
    from habitos.registro import Registro


class ReglaRango(ReglaHabito):

    def __init__(
        self,
        frecuencia: str,
        minimo: float,
        maximo: float
    ) -> None:

        super().__init__(frecuencia)

        self.minimo = minimo
        self.maximo = maximo

   
    # MÍNIMO
    
    @property
    def minimo(self) -> float:
        return self._minimo

    @minimo.setter
    def minimo(self, value: float) -> None:

        if type(value) not in (int, float):
            raise TypeError("minimo debe ser numérico")

        self._minimo = float(value)

   
    # MÁXIMO

    @property
    def maximo(self) -> float:
        return self._maximo

    @maximo.setter
    def maximo(self, value: float) -> None:

        if type(value) not in (int, float):
            raise TypeError("maximo debe ser numérico")

        self._maximo = float(value)

    # MÉTODO PRINCIPAL

    def cumplido(
        self,
        registros: List[Registro],
        inicio: date,
        fin: date
    ) -> bool:

        valores_periodo = []

        for registro in registros:

            # Solo usamos registros dentro del periodo
            if inicio <= registro.fecha <= fin:

                # Si aparece un valor no numérico, falla
                if type(registro.valor) not in (int, float):
                    return False

                valores_periodo.append(registro.valor)

        # Si no hay datos en el periodo, no se cumple
        if len(valores_periodo) == 0:
            return False

        # Todos los valores deben estar dentro del rango
        for valor in valores_periodo:

            if valor < self._minimo:
                return False

            if valor > self._maximo:
                return False

        return True


    # REPRESENTACIÓN
    def __str__(self) -> str:
        return (
            f"ReglaRango(frecuencia='{self.frecuencia}', "
            f"minimo={self._minimo}, maximo={self._maximo})"
        )

    def __repr__(self) -> str:
        return (
            f"ReglaRango("
            f"frecuencia={self.frecuencia!r}, "
            f"minimo={self._minimo!r}, "
            f"maximo={self._maximo!r})"
        )