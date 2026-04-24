from datetime import date
from core import Usuario, Meta
from habitos import HabitoBooleano
from habitos import HabitoNumerico
from reglas.reglaHabito import ReglaHabito
from habitos.registro import Registro
from collections.abc import Sequence
from typing import Any

class ReglaTemp(ReglaHabito):
    def __init__(self) -> None:
        super().__init__("diario", 1, 1)

    def cumplido(self, registros: Sequence[Registro], inicio: date, fin: date) -> bool:
        return len(registros) > 0
    
    def score(self, registros: Sequence[Registro], inicio: date, fin: date) -> float:
        return 1.0

def main() -> None:
    regla = ReglaTemp()

    habito_agua = HabitoNumerico(id="h1", nombre="Beber 2L Agua", regla=regla, unidad_medida="L")
    habito_leer = HabitoBooleano(id="h2", nombre="Leer 10 pags", regla=regla)
    habito_fruta = HabitoBooleano(id="h3", nombre="Comer fruta", regla=regla)

    habito_agua.registrar(date(2026, 3, 1), 2.5)
    habito_agua.registrar(date(2026, 3, 2), 2.0)
    habito_leer.registrar(date(2026, 3, 1), True)

    meta_nutricion = Meta(id="m1", nombre="Mejorar Alimentacion", peso=8)
    meta_salud = Meta(id="m2", nombre="Salud General", peso=10)

    meta_nutricion.add_habito(habito_agua)
    meta_nutricion.add_habito(habito_fruta)
    
    meta_salud.add_hijo(meta_nutricion)
    meta_salud.add_habito(habito_leer)

    usuario = Usuario(id="u1", nombre="Alex")

    plan_verano = usuario.crear_plan("Operacion Verano 2026")
    plan_invierno = usuario.crear_plan("Mantenimiento Invierno")

    plan_verano.add_habito(habito_agua)
    plan_verano.add_habito(habito_leer)
    plan_verano.add_habito(habito_fruta)

    plan_verano._metas.append(meta_salud)

    plan_combinado = plan_verano + plan_invierno

    print(usuario)
    print(usuario.planes_activos())
    print(plan_verano)
    print(plan_combinado)
    
    print(meta_salud)
    print(meta_nutricion)

    print(habito_agua)
    print(habito_agua.registros)
    print(habito_leer)

    print(plan_verano < plan_invierno)
    print(len(plan_combinado))

    inicio = date(2026, 3, 1)
    fin = date(2026, 3, 31)
    print(meta_salud.progreso(inicio, fin))
    print(plan_verano.progreso(inicio, fin))
    print(usuario.progreso_total(inicio, fin))

if __name__ == "__main__":
    main()