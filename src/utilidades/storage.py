from datetime import date
from typing import TYPE_CHECKING
from excepciones import FechaInvalidaError

if TYPE_CHECKING:
    from habitos.habito import Habito
    from core.usuario import Usuario


def exportar_historial_habito(habito: 'Habito', ruta: str) -> None:
    """Exporta todos los registros de un hábito a un fichero .txt."""
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(f"HISTORIAL DE HÁBITO: {habito.nombre}\n")
        f.write(f"Tipo: {type(habito).__name__}\n")
        f.write(f"Estado: {'Activo' if habito.activa else 'Inactivo'}\n")
        f.write(f"Racha actual: {habito.racha_actual} días\n")
        f.write(f"Total registros: {len(habito.registros)}\n")
        f.write("\n")

        if not habito.registros:
            f.write("Sin registros.\n")
        else:
            f.write(f"{'Fecha':<15} {'Valor':<15} {'Nota'}\n")
            f.write("\n")
            for registro in habito.registros:
                nota = registro.nota if registro.nota else "-"
                f.write(f"{str(registro.fecha):<15} {str(registro.valor):<15} {nota}\n")


def exportar_informe_progreso(
    usuario: 'Usuario',
    inicio: date,
    fin: date,
    ruta: str
) -> None:
    """Exporta un informe de progreso completo del usuario a un fichero .txt."""
    if inicio > fin:
        raise FechaInvalidaError(f"La fecha de inicio {inicio} es posterior a la fecha de fin {fin}.")

    with open(ruta, 'w', encoding='utf-8') as f:
        f.write("\n")
        f.write(f"INFORME DE PROGRESO\n")
        f.write(f"Usuario: {usuario.nombre} (ID: {usuario.id})\n")
        f.write(f"Período: {inicio} → {fin}\n")
        f.write("\n\n")

        if not usuario.planes:
            f.write("El usuario no tiene planes registrados.\n")
            return

        progreso_total = usuario.progreso_total(inicio, fin)
        f.write(f"PROGRESO GLOBAL: {progreso_total / len(usuario.planes) * 100:.1f}%\n\n")

        for plan in usuario.planes:
            f.write(f"PLAN: {plan.nombre}\n")
            f.write(f"  Creado: {plan.creado_en}\n")

            progreso_plan = plan.progreso(inicio, fin)
            f.write(f"  Progreso del plan: {progreso_plan * 100:.1f}%\n")

            if plan.metas:
                f.write("  Metas:\n")
                for meta in plan.metas:
                    progreso_meta = meta.progreso(inicio, fin)
                    f.write(f"    - {meta.nombre} (peso={meta.peso}): {progreso_meta * 100:.1f}%\n")

                    if meta.habitos:
                        for habito in meta.habitos:
                            progreso_h = habito.progreso(inicio, fin)
                            f.write(f"        · {habito.nombre}: {progreso_h * 100:.1f}% ({len(habito.registros)} registros)\n")

            if plan.habitos:
                f.write("  Hábitos del plan:\n")
                for nombre, habito in plan.habitos.items():
                    progreso_h = habito.progreso(inicio, fin)
                    f.write(f"    - {nombre}: {progreso_h * 100:.1f}% (racha={habito.racha_actual})\n")

            f.write("\n")

        f.write("\n")
        f.write("Informe generado automáticamente.\n")
