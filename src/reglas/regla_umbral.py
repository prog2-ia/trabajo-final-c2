from datetime import date
from typing import List

from habitos.registro import Registro
from reglas.regla_habito import ReglaHabito


class ReglaUmbral(ReglaHabito):

    def __init__(self, frecuencia: str, objetivo_minimo: float) -> None:
        super().__init__(frecuencia)
        self.objetivo_minimo = objetivo_minimo

    # -------------------------------------------------
    # OBJETIVO MÍNIMO
    # -------------------------------------------------
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

    # -------------------------------------------------
    # MÉTODO PRINCIPAL
    # -------------------------------------------------
    def cumplido(
        self,
        registros: List[Registro],
        inicio: date,
        fin: date
    ) -> bool:

        total = 0.0

        for registro in registros:

            # Solo contamos registros dentro del periodo
            if inicio <= registro.fecha <= fin:

                # Ignoramos registros no numéricos
                if type(registro.valor) not in (int, float):
                    continue

                total += registro.valor

        return total >= self._objetivo_minimo

    # -------------------------------------------------
    # REPRESENTACIÓN
    # -------------------------------------------------
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