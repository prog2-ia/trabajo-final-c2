from datetime import datetime, date
from habitos.habito import Habito
from .meta import Meta
from excepciones import DuplicadoError


class PlanBienestar:
    def __init__(self, nombre: str) -> None:
        self._nombre = nombre
        self._metas: list[Meta] = []
        self._habitos: dict[str, Habito] = {}
        self._creado_en: datetime = datetime.now()

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
    def metas(self) -> list[Meta]:
        return self._metas[:]

    @property
    def habitos(self) -> dict[str, Habito]:
        return dict(self._habitos)

    @property
    def creado_en(self) -> str:
        return f'Plan creado en: {self._creado_en}'

    def add_habito(self, habito: Habito) -> None:
        if not isinstance(habito, Habito):
            raise ValueError("El objeto introducido no es un Hábito válido.")

        if habito.nombre in self._habitos:
            raise DuplicadoError(f"El hábito '{habito.nombre}' ya existe en este plan.")

        self._habitos[habito.nombre] = habito

    def add_meta(self, meta: Meta) -> None:
        if not isinstance(meta, Meta):
            raise ValueError("El objeto introducido no es una Meta válida.")

        for m in self._metas:
            if m.id == meta.id:
                raise DuplicadoError(f"La meta '{meta.nombre}' ya existe en este plan.")

        self._metas.append(meta)

    def progreso(self, inicio: date | None, fin: date | None) -> float:
        if not self._metas:
            return 0.0

        suma_progresos = sum(meta.progreso(inicio, fin) for meta in self._metas)
        return suma_progresos / len(self._metas)

    # SOBRECARGA OPERADORES
    def __add__(self, otro: object) -> 'PlanBienestar':
        if not isinstance(otro, PlanBienestar):
            raise TypeError("Solo puedes sumar otro PlanBienestar.")

        nuevo_plan = PlanBienestar(f"{self._nombre} + {otro.nombre}")
        nuevo_plan._metas = self._metas + otro.metas
        nuevo_plan._habitos = {**self._habitos, **otro._habitos}
        return nuevo_plan

    def __lt__(self, otro: object) -> bool:
        if not isinstance(otro, PlanBienestar):
            raise TypeError("Solo puedes comparar con otro PlanBienestar.")

        hoy = datetime.now().date()
        progreso_self = self.progreso(self._creado_en.date(), hoy)
        progreso_otro = otro.progreso(otro._creado_en.date(), hoy)
        return progreso_self < progreso_otro

    def __len__(self) -> int:
        return len(self._habitos)

    def __str__(self) -> str:
        return f"Plan: {self._nombre}. Creado: {self._creado_en.strftime('%Y-%m-%d')}"
