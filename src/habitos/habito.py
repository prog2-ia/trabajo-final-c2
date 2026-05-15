from abc import ABC, abstractmethod
from datetime import date
from typing import Any
from reglas.reglaHabito import ReglaHabito
from .registro import Registro
from excepciones import HabitoInactivoError, DuplicadoError, FechaInvalidaError


# clase base para todos los hábitos, uso ABC para que no se pueda instanciar directamente
class Habito(ABC):

    def __init__(self, id: str, nombre: str, regla: ReglaHabito, activa: bool = True) -> None:
        self.id = id
        self.nombre = nombre
        self.regla = regla
        self.activa = activa

        self._registros: list[Registro] = []
        self._racha_actual: int = 0  # empieza en 0, se actualiza cada vez que se registra algo

    # ID
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        # el id no debería cambiar nunca una vez creado el hábito
        if hasattr(self, "_id"):
            raise AttributeError("El id no puede modificarse")
        if not value:
            raise ValueError("El id no puede estar vacío")
        self._id = value

    # NOMBRE
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        if value is None:
            raise ValueError("El nombre no puede ser None")

        value = value.strip()  # saco espacios por si acaso

        if len(value) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")

        self._nombre = value

    # REGLA
    @property
    def regla(self) -> ReglaHabito:
        return self._regla

    @regla.setter
    def regla(self, value: ReglaHabito) -> None:
        if value is None:
            raise ValueError("La regla no puede ser None")
        self._regla = value


    # ACTIVA
    @property
    def activa(self) -> bool:
        return self._activa

    @activa.setter
    def activa(self, value: bool) -> None:
        # uso type() en vez de isinstance() porque sino True/False pasarían como int también
        if type(value) is not bool:
            raise TypeError("El valor debe ser booleano")
        self._activa = value

    # estos dos son solo lectura, no tiene sentido modificarlos desde afuera
    @property
    def registros(self) -> list[Registro]:
        return list(self._registros)  # devuelvo una copia para que no modifiquen la lista interna

    @property
    def racha_actual(self) -> int:
        return self._racha_actual

    # las subclases van a tener que implementar este método según su tipo de valor
    @abstractmethod
    def registrar(self, fecha: date, valor: Any) -> None:
        if not isinstance(fecha, date):
            raise TypeError("fecha debe ser un objeto datetime.date")

        if fecha > date.today():
            raise FechaInvalidaError(f"La fecha {fecha} no puede ser futura.")

        if not self._activa:
            raise HabitoInactivoError(f"No se puede registrar en el hábito '{self._nombre}' porque está inactivo.")

        # no permito registrar dos veces el mismo día
        for r in self._registros:
            if r.fecha == fecha:
                raise DuplicadoError(f"Ya existe un registro para la fecha {fecha} en '{self._nombre}'.")

        from .registro import Registro
        registro = Registro(fecha, valor)

        self._add_registro(registro)

    def _add_registro(self, registro: Registro) -> None:
        self._registros.append(registro)
        self.ajustar_racha()  # recalculo la racha cada vez que entra un registro nuevo

    def ajustar_racha(self) -> None:
        if len(self._registros) == 0:
            self._racha_actual = 0
            return

        # ordeno para poder recorrer de más reciente a más antiguo
        self._registros.sort()

        racha = 0
        ultima_fecha = None

        # recorro al revés: desde el registro más reciente hacia atrás
        for registro in reversed(self._registros):

            # si este registro no cumplió la regla, la racha se corta
            if not self._regla.cumplido([registro], registro.fecha, registro.fecha):
                break

            if ultima_fecha is None:
                racha = 1
                ultima_fecha = registro.fecha
                continue

            diferencia = (ultima_fecha - registro.fecha).days

            # si los días son consecutivos, sumo a la racha
            if diferencia == 1:
                racha += 1
                ultima_fecha = registro.fecha
            else:
                break  # si hay un hueco, la racha se rompe

        self._racha_actual = racha

    def progreso(self, inicio: date | None = None, fin: date | None = None) -> float:
        total = len(self._registros)

        # para compatibilidad con la clase Meta añado este filtro
        # si se pasan fechas, filtramos los registros de ese periodo
        if inicio is not None and fin is not None:
            registros_filtrados = [r for r in self._registros if inicio <= r.fecha <= fin]
        else:
            registros_filtrados = self._registros

        total = len(registros_filtrados)
        if total == 0:
            return 0.0

        cumplidos = sum(1 for r in registros_filtrados if self._regla.cumplido([r], r.fecha, r.fecha))
        return cumplidos / total  # porcentaje entre 0.0 y 1.0


    # SOBRECARGA
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Habito):
            return NotImplemented
        return self._id == other._id  # dos hábitos son iguales si tienen el mismo id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Habito):
            return NotImplemented
        return self._racha_actual < other._racha_actual  # sirve para ordenarlos por racha

    def __len__(self) -> int:
        return len(self._registros)

    def __str__(self) -> str:
        return f"{type(self).__name__}('{self.nombre}', racha={self._racha_actual})"

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(id='{self._id}', "
            f"nombre='{self._nombre}', activa={self._activa})"
        )
