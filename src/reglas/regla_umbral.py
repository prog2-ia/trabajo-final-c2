from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING, List

from reglas.reglaHabito import ReglaHabito

if TYPE_CHECKING:
    from habitos.registro import Registro


# regla que se cumple si la suma de valores del periodo supera un mínimo
# por ejemplo: "correr al menos 10 km por semana"
class ReglaUmbral(ReglaHabito):

    def __init__(self, frecuencia: str, objetivo_minimo: float) -> None:
        super().__init__(frecuencia)
        self.objetivo_minimo = objetivo_minimo

    # OBJETIVO MÍNIMO
    @property
    def objetivo_minimo(self) -> float:
        return self._objetivo_minimo

    @objetivo_minimo.setter
    def objetivo_minimo(self, value: float) -> None:
        if type(value) not in (int, float):
            raise TypeError("objetivo_minimo debe ser numérico")

        if value < 0:
            raise ValueError("objetivo_minimo no puede ser negativo")

        self._objetivo_minimo = float(value)


    # MÉTODO PRINCIPAL
    def cumplido(
        self,
        registros: List[Registro],
        inicio: date,
        fin: date
    ) -> bool:

        total = 0.0

        for registro in registros:
            if inicio <= registro.fecha <= fin:
                # si el valor no es numérico lo salteo, no quiero que explote
                if type(registro.valor) not in (int, float):
                    continue

                total += registro.valor

        # se cumple si la suma acumulada llega al objetivo
        return total >= self._objetivo_minimo

    # REPRESENTACIÓN
    def __str__(self) -> str:
        return (
            f"ReglaUmbral(frecuencia='{self.frecuencia}', "
            f"objetivo_minimo={self._objetivo_minimo})"
        )

    def __repr__(self) -> str:
        return (
            f"ReglaUmbral("
            f"frecuencia={self.frecuencia!r}, "
            f"objetivo_minimo={self._objetivo_minimo!r})"
        )
