from .planBienestar import PlanBienestar
from datetime import date

class Usuario:
    def __init__(self, id: str, nombre: str) -> None:
        self._id = id
        self._nombre = nombre
        self._planes: list[PlanBienestar] = []
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, otro: str) -> None:
        if not isinstance(otro, str):
            raise TypeError("El nombre debe ser una cadena de texto.")
        
        if not otro.strip():
            raise ValueError("El nombre no puede estar vacío.")
        
        self._nombre = otro.strip()
        
    @property
    def planes(self) -> list[PlanBienestar]:
        return self._planes[:]
        
    def crear_plan(self, nombre: str) -> PlanBienestar:
        nuevo_plan = PlanBienestar(nombre)
        self._planes.append(nuevo_plan)
        return nuevo_plan
    
    def planes_activos(self) -> list[PlanBienestar]:
        if not self._planes:
            # usar excepcion personalizada en un futuro
            raise ValueError(f"El usuario {self._nombre} todavía no tiene ningún plan.")
        
        return self._planes[:]
    
    def progreso_total(self, inicio: date | None, fin: date | None) -> float:
        if not self._planes:
            return 0.0
        
        total = 0.0
        for plan in self._planes:
            total += plan.progreso(inicio, fin)
        
        return total
    
    def __str__(self) -> str:
        return f"Usuario: {self._nombre}: \n -ID: {self._id}\n -Planes totales: {len(self._planes)}"