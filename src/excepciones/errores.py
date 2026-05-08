class PlanVacioError(Exception):
    """Se lanza cuando se intenta operar sobre un plan o lista de planes vacíos."""
    pass

class DuplicadoError(Exception):
    """Se lanza cuando se intenta añadir un elemento que ya existe."""
    pass

class HabitoInactivoError(Exception):
    """Se lanza cuando se intenta registrar en un hábito inactivo."""
    pass

class FechaInvalidaError(Exception):
    """Se lanza cuando se proporciona una fecha no válida o fuera de rango."""
    pass
