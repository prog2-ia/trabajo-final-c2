from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional, Dict, Any 

class ReglaHabito(ABC):
    def __init__(self, frecuencia, objetivo, minimo):
        self.frecuencia = frecuencia
        self.objetivo = objetivo
        self.minimo = minimo
    
    def es_valor_valido(self, valor):
        # determina si un valor individual es válido según la regla
        pass
    
    def cumplido(self, registros, inicio, fin):
        pass
    
    @abstractmethod
    def score(self, registros, inicio, fin):
        pass
    
    
    @classmethod
    def from_dict(cls, datos):
        pass
    

class ReglaFrecuencia(ReglaHabito):
    def __init__(self, frecuencia, objetivo, minimo):
        super().__init__(frecuencia, objetivo, minimo)
    
    
class ReglaUmbral(ReglaHabito):
    def __init__(self, frecuencia, objetivo, minimo):
        super().__init__(frecuencia, objetivo, minimo) 

class ReglaRango(ReglaHabito):
    def __init__(self, frecuencia, objetivo, minimo):
        super().__init__(frecuencia, objetivo, minimo)
        
     