from abc import ABC, abstractmethod
from typing import Any, Self
from collections.abc import Sequence
from datetime import date
from habitos.registro import Registro

class ReglaHabito(ABC):
    def __init__(self, frecuencia: str, objetivo: int | float, minimo: int | float) -> None:
        self.frecuencia = frecuencia
        self.objetivo = objetivo
        self.minimo = minimo
    
    def es_valor_valido(self, valor: Any) -> bool:
        # determina si un valor individual es válido según la regla
        raise NotImplementedError()
    
    def cumplido(self, registros: Sequence[Registro], inicio: date, fin: date) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def score(self, registros: Sequence[Registro], inicio: date, fin: date) -> float:
        raise NotImplementedError()
    
    
    @classmethod
    def from_dict(cls, datos: dict[str, Any]) -> Self:
        raise NotImplementedError()
    

class ReglaFrecuencia(ReglaHabito):
    def __init__(self, frecuencia: str, objetivo: int | float, minimo: int | float) -> None:
        super().__init__(frecuencia, objetivo, minimo)
    
    
class ReglaUmbral(ReglaHabito):
    def __init__(self, frecuencia: str, objetivo: int | float, minimo: int | float) -> None:
        super().__init__(frecuencia, objetivo, minimo) 

class ReglaRango(ReglaHabito):
    def __init__(self, frecuencia: str, objetivo: int | float, minimo: int | float) -> None:
        super().__init__(frecuencia, objetivo, minimo)