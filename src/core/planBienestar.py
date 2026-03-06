from datetime import datetime, date
from habitos import Habito

class PlanBienestar:
    def __init__(self, nombre):
        self._nombre = nombre
        self._metas = []
        self._habitos = {}
        self._creado_en = datetime.now()
    
    def add_habito(self, habito):
        if not isinstance(habito, Habito):
            raise ValueError("El objeto introducido no es un Hábito válido.")
        
        if habito._nombre in self._habitos:
            pass
            # excepción personalizada DuplicadoError
            # raise DuplicadoError(f"El hábito '{habito._nombre}' ya existe en este plan.")
            
        self._habitos[habito._nombre] = habito
        
        
    def progreso(self, inicio, fin):
        if not self._metas:
            return 0.0
            
        suma_progresos = sum(meta.progreso(inicio, fin) for meta in self._metas_raiz)
        return suma_progresos / len(self._metas_raiz)
    
    # SOBRECARGA OPERADORES
    def __add__(self, otro):
        if not isinstance(otro, PlanBienestar):
            raise TypeError("Solo puedes sumar otro PlanBienestar.")
        
        nuevo_plan = PlanBienestar(f"{self._nombre} + {otro._nombre}")
        
        nuevo_plan._metas = self._metas + otro._metas
        
        # se unen los diccionarios de habitos
        nuevo_plan._habitos = {**self._habitos, **otro._habitos}
        
        return nuevo_plan
    
    def __lt__(self, otro):
        if not isinstance(otro, PlanBienestar):
            raise TypeError("Solo puedes comparar con otro PlanBienestar.")
            
        hoy = datetime.now().date()
        
        progreso_self = self.progreso(self._creado_en.date(), hoy)
        progreso_otro = otro.progreso(otro._creado_en.date(), hoy)
        
        return progreso_self < progreso_otro
    
    def __len__(self):
        return len(self._habitos)
    
    def __str__(self):
        return f"Plan: {self._nombre}. Creado: {self._creado_en.strftime('%Y-%m-%d')}"