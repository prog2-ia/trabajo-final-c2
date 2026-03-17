from habitos import Habito

class Meta:
    def __init__(self, id, nombre, peso):
        self._id = id
        self._nombre = nombre
        self._peso = peso
        self._hijos = []
        self._habitos = []
    
    @property
    def id(self):
        return self._id
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, otro):
        if not isinstance(otro, str):
            raise TypeError("El nombre debe ser una cadena de texto.")
        
        if not otro.strip():
            raise ValueError("El nombre no puede estar vacío.")
        
        self._nombre = otro.strip()
    
    @property
    def peso(self):
        return self._peso
    
    @peso.setter
    def peso(self, valor):
        if not isinstance(valor, (int,float)):
            raise TypeError('El peso de la meta debe ser un número.')
        
        if valor<=0 or valor>10:
            raise ValueError("El peso de la meta debe ser mayor que 0 y menor o igual que 10.")

        self._peso = valor
        
    @property
    def hijos(self):
        return self._hijos[:]
    
    @property
    def habitos(self):
        return self._habitos[:]  
    
     
    def add_hijo(self, meta):
        
        if not isinstance(meta, Meta):
                raise ValueError('El hijo debe ser de tipo Meta.')
            
        for hijo in self._hijos:
            if hijo._id == meta.id:
                raise ValueError(f'La meta {meta} ya existe como hija.')
        
        self._hijos.append(meta)
        
    def add_habito(self, habito):
        if not isinstance(habito, Habito):
                raise ValueError('Hijo debe ser de tipo Habito.')
        
        for h in self._habitos:
            if h._nombre == habito.nombre:
                raise ValueError(f'El hábito {habito} ya está en es esta meta.')
        
        self._habitos.append(habito)
    

    def progreso(self, inicio, fin):
        
        progreso_habitos = 0.0
        
        # progreso de los habitos
        if self._habitos:
            suma = sum(h.progreso(inicio, fin) for h in self._habitos)
            progreso_habitos = suma/len(self._habitos)
        
        progreso_hijos = 0.0
        peso_total_hijos = 0.0
        
        # progreso de los hijos
        if self._hijos:
            for hijo in self._hijos:
                progreso_hijos += hijo.progreso(inicio, fin) * hijo._peso
                peso_total_hijos += hijo._peso
            
            if peso_total_hijos > 0:
                progreso_hijos = progreso_hijos / peso_total_hijos

        # progreso total 
        if self._habitos and self._hijos:
            return (progreso_habitos + progreso_hijos) / 2
        elif self._hijos:
            return progreso_hijos
        
        return progreso_habitos

    def __str__(self):
        return f"Meta: {self._nombre} con ID: {self._id} (Peso: {self._peso}). Submetas: {len(self._hijos)}."
    