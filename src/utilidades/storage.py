import os
import pickle
from datetime import date
from typing import TYPE_CHECKING
from excepciones import FechaInvalidaError

if TYPE_CHECKING:
    from habitos.habito import Habito
    from core.usuario import Usuario

# Carpeta data/ en la raíz del proyecto (fuera de src/)
_SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.normpath(os.path.join(_SRC_DIR, '..', 'data'))


def _asegurar_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


# implementación de ficheros de texto .txt

def exportar_historial_habito(habito: 'Habito', nombre_archivo: str) -> str:
    """Exporta los registros de un hábito a data/<nombre_archivo>.txt. Devuelve la ruta."""
    _asegurar_data_dir()
    if not nombre_archivo.endswith('.txt'):
        nombre_archivo += '.txt'
    ruta = os.path.join(DATA_DIR, nombre_archivo)

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

    return ruta


def exportar_informe_progreso(
    usuario: 'Usuario',
    inicio: date,
    fin: date,
    nombre_archivo: str
) -> str:
    """Exporta un informe de progreso a data/<nombre_archivo>.txt. Devuelve la ruta."""
    if inicio > fin:
        raise FechaInvalidaError(f"La fecha de inicio {inicio} es posterior a la fecha de fin {fin}.")

    _asegurar_data_dir()
    if not nombre_archivo.endswith('.txt'):
        nombre_archivo += '.txt'
    ruta = os.path.join(DATA_DIR, nombre_archivo)

    with open(ruta, 'w', encoding='utf-8') as f:
        f.write("\n")
        f.write(f"INFORME DE PROGRESO\n")
        f.write(f"Usuario: {usuario.nombre} (ID: {usuario.id})\n")
        f.write(f"Período: {inicio} → {fin}\n")
        f.write("\n\n")

        if not usuario.planes:
            f.write("El usuario no tiene planes registrados.\n")
            return ruta

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

    return ruta

# implementación de ficheros binarios pickle 

def guardar_sesion(usuario: 'Usuario') -> str:
    """Serializa el objeto Usuario completo en data/sesion_<nombre>.pickle. Devuelve la ruta."""
    _asegurar_data_dir()
    nombre_safe = usuario.nombre.replace(' ', '_').lower()
    ruta = os.path.join(DATA_DIR, f"sesion_{nombre_safe}.pickle")
    with open(ruta, 'wb') as f:
        pickle.dump(usuario, f)
    return ruta


def cargar_sesion(nombre: str) -> 'Usuario | None':
    """Carga un Usuario desde data/sesion_<nombre>.pickle. Devuelve None si no existe."""
    nombre_safe = nombre.replace(' ', '_').lower()
    ruta = os.path.join(DATA_DIR, f"sesion_{nombre_safe}.pickle")
    if not os.path.exists(ruta):
        return None
    with open(ruta, 'rb') as f:
        return pickle.load(f)  
