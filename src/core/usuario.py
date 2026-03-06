from planBienestar import PlanBienestar

class Usuario:
    def __init__(self, id, nombre):
        self._id = id
        self._nombre = nombre
        self._planes = []
    
    def crear_plan(self, nombre):
        nuevo_plan = PlanBienestar(nombre)
        self._planes.append(nuevo_plan)
        return nuevo_plan
    
    def planes_activos(self):
        if not self._planes:
            # usar excepcion personalizada en un futuro
            raise ValueError(f"El usuario {self._nombre} todavía no tiene ningún plan.")
        
        return self._planes[:]
    
    def progreso_total(self, inicio, fin):
        if not self._planes:
            return 0.0
        
        total = 0
        for plan in self._planes:
            total += plan.progreso(inicio, fin)
        
        return total
    
    def __str__(self):
        return f"Usuario: {self._nombre}: \n -ID: {self._id}\n -Planes totales: {len(self._planes)}"
    