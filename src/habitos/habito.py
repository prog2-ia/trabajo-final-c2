from abc import ABC, abstractmethod
from datetime import date

class Habito(ABC):
    num_habitos = 0

    def __init__(self, id,  nombre, regla, activa = True):
        self.id = id
        self.nombre = nombre
        self.regla = regla
        self.activa = activa 

        self._registros = []
        self._racha_actual = 0

#ID
    @property
    def id(self):
        return self._id 
    
    @id.setter
    def id(self, value):
        if hasattr(self, "id"):
            raise AttributeError("El id no puede modificarse")
        if not value:
            raise ValueError("El id no puede estar vacío")
        self._id = value
        
#NAME
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            raise ValueError("El nombre no puede ser None.")

        value = value.strip()

        if len(value) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        
        self._name = value

    @property
    def activa(self):
        return self._activa
    
    @activa.setter
    def activa(self, value):
        if type(value) is not bool:
            raise TypeError("El valor debe ser booleano")
        self._activa = value

   
    # SOLO LECTURA

    @property
    def registros(self):
        # Devuelve copia para evitar modificación externa
        return list(self._registros)

    @property
    def racha_actual(self):
        return self._racha_actual

# MÉTODO ABSTRACTO
@abstractmethod
def registrar(self, fecha: date, valor):
    """
    Crea un Registro válido y lo añade al hábito.
    La validación específica del tipo de 'valor'
    debe realizarse en las subclases.
    """

    # 1️⃣ Validar fecha
    if not isinstance(fecha, date):
        raise TypeError("fecha debe ser un objeto datetime.date")

    # 2️⃣ Comprobar que el hábito esté activo
    if not self._activa:
        raise ValueError("No se puede registrar en un hábito inactivo.")

    # 3️⃣ Evitar registros duplicados en la misma fecha
    for r in self._registros:
        if r.fecha == fecha:
            raise ValueError("Ya existe un registro para esa fecha.")

    # 4️⃣ Crear registro
    from .registro import Registro
    registro = Registro(fecha, valor)

    # 5️⃣ Añadir usando método protegido
    self._add_registro(registro)


# MÉTODOS INTERNOS

def _add_registro(self, registro):
    """
    Método protegido para que las subclases añadan registros.
    """
    self._registros.append(registro)
    self.ajustar_racha()


# LÓGICA

def ajustar_racha(self):
    """
    Calcula la racha diaria consecutiva hacia atrás.
    """
    if len(self._registros) == 0:
        self._racha_actual = 0
        return

    self._registros.sort()

    racha = 0
    ultima_fecha = None

    for registro in reversed(self._registros):

        if not self._regla.cumplido([registro], registro.fecha, registro.fecha):
            break

        if ultima_fecha is None:
            racha = 1
            ultima_fecha = registro.fecha
            continue

        diferencia = (ultima_fecha - registro.fecha).days

        if diferencia == 1:
            racha += 1
            ultima_fecha = registro.fecha
        else:
            break

    self._racha_actual = racha


def progreso(self):
    """
    Devuelve proporción de registros que cumplen la regla.
    """
    total = len(self._registros)

    if total == 0:
        return 0.0

    cumplidos = 0

    for r in self._registros:
        if self._regla.cumplido([r], r.fecha, r.fecha):
            cumplidos += 1

    return cumplidos / total


# MÉTODO ABSTRACTO
@abstractmethod
def registrar(self, fecha: date, valor):
    """
    Crea un Registro válido y lo añade al hábito.
    La validación específica del tipo de 'valor'
    debe realizarse en las subclases.
    """

    # Validar fecha
    if not isinstance(fecha, date):
        raise TypeError("fecha debe ser un objeto datetime.date")

    # Comprobar que el hábito esté activo
    if not self._activa:
        raise ValueError("No se puede registrar en un hábito inactivo.")

    # Evitar registros duplicados en la misma fecha
    for r in self._registros:
        if r.fecha == fecha:
            raise ValueError("Ya existe un registro para esa fecha.")

    # Crear registro
    from .registro import Registro
    registro = Registro(fecha, valor)

    # Añadir usando método protegido
    self._add_registro(registro)


# MÉTODOS INTERNOS
def _add_registro(self, registro):
    """
    Método protegido para que las subclases añadan registros.
    """
    self._registros.append(registro)
    self.ajustar_racha()

# LÓGICA
def ajustar_racha(self):
    """
    Calcula la racha diaria consecutiva hacia atrás.
    """
    if len(self._registros) == 0:
        self._racha_actual = 0
        return

    self._registros.sort()

    racha = 0
    ultima_fecha = None

    for registro in reversed(self._registros):

        if not self._regla.cumplido([registro], registro.fecha, registro.fecha):
            break

        if ultima_fecha is None:
            racha = 1
            ultima_fecha = registro.fecha

        diferencia = (ultima_fecha - registro.fecha).days

        if diferencia == 1:
            racha += 1
            ultima_fecha = registro.fecha
        else:
            break

    self._racha_actual = racha


def progreso(self):
    """
    Devuelve proporción de registros que cumplen la regla.
    """
    total = len(self._registros)

    if total == 0:
        return 0.0

    cumplidos = 0

    for r in self._registros:
        if self._regla.cumplido([r], r.fecha, r.fecha):
            cumplidos += 1

    return cumplidos / total


# SOBRECARGA
def __eq__(self, other):
    if not isinstance(other, Habito):
        return NotImplemented
    return self._id == other._id


def __lt__(self, other):
    return self._racha_actual < other._racha_actual


def __len__(self):
    return len(self._registros)


def __str__(self):
    return f"{type(self).__name__}('{self.nombre}', racha={self._racha_actual})"


def __repr__(self):
    return (
        f"{type(self).__name__}(id='{self._id}', "
        f"nombre='{self._nombre}', activa={self._activa})"
    )