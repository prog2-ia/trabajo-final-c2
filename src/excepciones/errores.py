from datetime import date as Date


class PlanVacioError(Exception):
    """Se lanza cuando se intenta operar sobre un plan o lista de planes vacíos."""

    def __init__(self, mensaje: str = "El plan o lista de planes está vacío.", nombre: str | None = None) -> None:
        super().__init__(mensaje)
        self.nombre = nombre


class DuplicadoError(Exception):
    """Se lanza cuando se intenta añadir un elemento que ya existe."""

    def __init__(self, mensaje: str = "El elemento ya existe.", elemento: str | None = None) -> None:
        super().__init__(mensaje)
        self.elemento = elemento


class HabitoInactivoError(Exception):
    """Se lanza cuando se intenta registrar en un hábito inactivo."""

    def __init__(self, mensaje: str = "El hábito está inactivo.", nombre_habito: str | None = None) -> None:
        super().__init__(mensaje)
        self.nombre_habito = nombre_habito


class FechaInvalidaError(Exception):
    """Se lanza cuando se proporciona una fecha no válida o fuera de rango."""

    def __init__(self, mensaje: str = "La fecha proporcionada no es válida.", fecha: Date | None = None) -> None:
        super().__init__(mensaje)
        self.fecha = fecha
