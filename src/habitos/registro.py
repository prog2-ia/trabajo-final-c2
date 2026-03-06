from datetime import date


class Registro:
    def __init__(self, fecha, valor, nota=None):
        """
        nota: comentario opcional. Si no se pasa nada, será None por defecto.

        """
        self.fecha = fecha
        self.valor = valor
        self.nota = nota

    # -------------------------------------------------
    # FECHA
    # -------------------------------------------------
    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, value):
        if not isinstance(value, date):
            raise TypeError("La fecha debe ser un objeto date")
        self._fecha = value

    # -------------------------------------------------
    # VALOR
    # -------------------------------------------------
    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, value):
      
        if type(value) not in (int, float, bool):
            raise TypeError("El valor debe ser int, float o bool")
        self._valor = value

    # -------------------------------------------------
    # NOTA
    # -------------------------------------------------
    @property
    def nota(self):
        return self._nota

    @nota.setter
    def nota(self, value):
       
        if value is not None and not isinstance(value, str):
            raise TypeError("La nota debe ser una cadena o None")
        self._nota = value

    # -------------------------------------------------
    # SOBRECARGA
    # -------------------------------------------------
    def __lt__(self, other):
        """
        __lt__ significa 'less than' (<).

        Sirve para que Python sepa comparar dos objetos Registro
        usando el operador <.

        En este caso, se compara por fecha para que los registros
        puedan ordenarse cronológicamente.

        Gracias a esto, luego podemos hacer:
            lista_registros.sort()

        y Python sabrá cómo ordenarlos.
        """
        if not isinstance(other, Registro):
            return NotImplemented
        return self._fecha < other._fecha

    def __str__(self):
        return f"Registro(fecha={self._fecha}, valor={self._valor}, nota={self._nota})"

    def __repr__(self):
        return (
            f"Registro(fecha={self._fecha!r}, "
            f"valor={self._valor!r}, nota={self._nota!r})"
        )