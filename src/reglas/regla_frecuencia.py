from datetime import date
from typing import List

from habitos.registro import Registro
from reglas.regla_habito import ReglaHabito


class ReglaFrecuencia(ReglaHabito):

    def __init__(self, frecuencia: str, veces_objetivo: int) -> None:
        super().__init__(frecuencia)
        self.veces_objetivo = veces_objetivo


    # VECES OBJETIVO
   
    @property
    def veces_objetivo(self) -> int:
        return self._veces_objetivo

    @veces_objetivo.setter
    def veces_objetivo(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError("veces_objetivo debe ser un entero")

        if value <= 0:
            raise ValueError("veces_objetivo debe ser mayor que 0")

        self._veces_objetivo = value

    # MÉTODO PRINCIPAL
   
    def cumplido(
        self,
        registros: List[Registro],
        inicio: date,
        fin: date
    ) -> bool:
        contador = 0

        for registro in registros:
            if inicio <= registro.fecha <= fin:
                contador += 1

        return contador >= self._veces_objetivo


    # REPRESENTACIÓN
  
    def __str__(self) -> str:
        return (
            f"ReglaFrecuencia(frecuencia='{self.frecuencia}', "
            f"veces_objetivo={self._veces_objetivo})"
        )

    def __repr__(self) -> str:
        return (
            f"ReglaFrecuencia("
            f"frecuencia={self.frecuencia!r}, "
            f"veces_objetivo={self._veces_objetivo!r})"
        )