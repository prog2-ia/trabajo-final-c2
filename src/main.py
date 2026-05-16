from datetime import date, datetime
from core import Usuario, Meta
from core.planBienestar import PlanBienestar
from habitos import Habito, HabitoBooleano, HabitoNumerico
from reglas.regla_frecuencia import ReglaFrecuencia
from reglas.regla_umbral import ReglaUmbral
from reglas.regla_rango import ReglaRango
from reglas.reglaHabito import ReglaHabito
from excepciones import PlanVacioError, DuplicadoError, HabitoInactivoError
from utilidades import (
    exportar_historial_habito,
    exportar_informe_progreso,
    guardar_sesion,
    cargar_sesion,
)

usuario: Usuario | None = None


# funciones auxiliares de entrada

def leer_fecha(mensaje: str) -> date:
    while True:
        entrada = input(mensaje).strip()
        try:
            return datetime.strptime(entrada, "%Y-%m-%d").date()
        except ValueError:
            print("  Formato incorrecto. Usa YYYY-MM-DD (ej: 2026-03-15).")


def leer_entero(mensaje: str, minimo: int = 1) -> int:
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if valor < minimo:
                print(f"  El valor mínimo es {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Introduce un número entero válido.")


def leer_float(mensaje: str, minimo: float = 0.0) -> float:
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = float(entrada)
            if valor < minimo:
                print(f"  El valor mínimo es {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Introduce un número válido.")


def leer_opcion(opciones: list[str]) -> int:
    while True:
        entrada = input("  Opción: ").strip()
        try:
            idx = int(entrada)
            if 1 <= idx <= len(opciones):
                return idx
            print(f"  Elige entre 1 y {len(opciones)}.")
        except ValueError:
            print("  Introduce un número.")


def mostrar_menu(titulo: str, opciones: list[str]) -> int:
    print("--------------------------------------")
    print(f"  {titulo}")
    print("--------------------------------------")
    for i, op in enumerate(opciones, 1):
        print(f"  {i}. {op}")
    print("--------------------------------------")
    return leer_opcion(opciones)


def pausa() -> None:
    input("\n  Pulsa Enter para continuar...")


# funciones auxiliares para la selección en menú

def seleccionar_plan() -> PlanBienestar | None:
    if usuario is None:
        return None
    try:
        planes = usuario.planes_activos()
    except PlanVacioError:
        print("  No hay planes. Crea uno primero.")
        return None
    print("\n  Planes disponibles:")
    for i, p in enumerate(planes):
        print(f"    {i+1}. {p.nombre}")
    nombres = [p.nombre for p in planes]
    idx = leer_opcion(nombres)
    return planes[idx - 1]


def seleccionar_habito(plan: PlanBienestar) -> Habito | None:
    habitos = list(plan.habitos.values())
    if not habitos:
        print("  Este plan no tiene hábitos.")
        return None
    print("\n  Hábitos del plan:")
    for i, h in enumerate(habitos):
        if isinstance(h, HabitoBooleano):
            tipo_str = "Booleano"
        else:
            tipo_str = "Numerico"
        print(f"    {i+1}. {h.nombre} ({tipo_str})")
    nombres = [h.nombre for h in habitos]
    idx = leer_opcion(nombres)
    return habitos[idx - 1]


def seleccionar_meta(plan: PlanBienestar) -> Meta | None:
    metas = plan.metas
    if not metas:
        print("  Este plan no tiene metas.")
        return None
    print("\n  Metas del plan:")
    for i, m in enumerate(metas):
        print(f"    {i+1}. {m.nombre} (peso={m.peso})")
    nombres = [m.nombre for m in metas]
    idx = leer_opcion(nombres)
    return metas[idx - 1]


def crear_regla() -> ReglaHabito:
    opcion = mostrar_menu("TIPO DE REGLA", [
        "Frecuencia  — se cumple al registrar N veces en el período",
        "Umbral      — se cumple si la suma de valores supera un mínimo",
        "Rango       — se cumple si todos los valores están en [min, max]",
    ])
    frecuencia = input("  Frecuencia (diario/semanal/mensual): ").strip()
    if not frecuencia:
        frecuencia = "diario"
    if opcion == 1:
        veces = leer_entero("  ¿Cuántas veces debe cumplirse? ", 1)
        return ReglaFrecuencia(frecuencia, veces)
    elif opcion == 2:
        minimo = leer_float("  Valor mínimo acumulado: ", 0.0)
        return ReglaUmbral(frecuencia, minimo)
    else:
        minimo = leer_float("  Valor mínimo: ", 0.0)
        maximo = leer_float("  Valor máximo: ", minimo)
        return ReglaRango(frecuencia, minimo, maximo)


# submenús de cada opcion

def gestion_planes() -> None:
    if usuario is None:
        return
    while True:
        opcion = mostrar_menu("GESTIÓN DE PLANES", [
            "Crear plan",
            "Ver todos los planes",
            "Combinar dos planes (+)",
            "Comparar progreso de dos planes (<)",
            "Volver",
        ])
        if opcion == 1:
            nombre = input("  Nombre del plan: ").strip()
            if not nombre:
                print("  El nombre no puede estar vacío.")
                continue
            plan = usuario.crear_plan(nombre)
            print(f"  Plan '{plan.nombre}' creado correctamente.")

        elif opcion == 2:
            try:
                for p in usuario.planes_activos():
                    print(f"  - {p}")
            except PlanVacioError as e:
                print(f"  {e}")

        elif opcion == 3:
            print("  Selecciona el PRIMER plan:")
            p1 = seleccionar_plan()
            if p1 is None:
                pausa()
                continue
            print("  Selecciona el SEGUNDO plan:")
            p2 = seleccionar_plan()
            if p2 is None:
                pausa()
                continue
            combinado = p1 + p2
            print(f"  Resultado: {combinado}")

        elif opcion == 4:
            print("  Selecciona el PRIMER plan:")
            p1 = seleccionar_plan()
            if p1 is None:
                pausa()
                continue
            print("  Selecciona el SEGUNDO plan:")
            p2 = seleccionar_plan()
            if p2 is None:
                pausa()
                continue
            if p1 < p2:
                print(f"  '{p1.nombre}' tiene MENOS progreso que '{p2.nombre}'.")
            else:
                print(f"  '{p1.nombre}' tiene MÁS progreso que '{p2.nombre}'.")

        elif opcion == 5:
            break

        pausa()


def gestion_habitos() -> None:
    while True:
        opcion = mostrar_menu("GESTIÓN DE HÁBITOS", [
            "Crear hábito y añadirlo a un plan",
            "Ver hábitos de un plan",
            "Registrar valor en un hábito",
            "Ver registros de un hábito",
            "Activar / Desactivar un hábito",
            "Volver",
        ])

        if opcion == 1:
            plan = seleccionar_plan()
            if plan is None:
                pausa()
                continue
            nombre = input("  Nombre del hábito: ").strip()
            tipo = mostrar_menu("TIPO DE HÁBITO", ["Booleano (Sí/No)", "Numérico (cantidad)"])
            regla = crear_regla()
            try:
                habito_id = f"h_{nombre}_{len(plan.habitos) + 1}"
                if tipo == 1:
                    plan.add_habito(HabitoBooleano(id=habito_id, nombre=nombre, regla=regla))
                else:
                    unidad = input("  Unidad de medida (ej: L, km, min): ").strip() or "unidades"
                    plan.add_habito(HabitoNumerico(id=habito_id, nombre=nombre, regla=regla, unidad_medida=unidad))
                print(f"  Hábito '{nombre}' creado y añadido al plan '{plan.nombre}'.")
            except DuplicadoError as e:
                print(f"  Error: {e}")
            except ValueError as e:
                print(f"  Error de validación: {e}")

        elif opcion == 2:
            plan = seleccionar_plan()
            if plan is None:
                pausa()
                continue
            habitos = plan.habitos
            if not habitos:
                print("  Este plan no tiene hábitos.")
            else:
                print(f"\n  Hábitos del plan '{plan.nombre}':")
                for hab in habitos.values():
                    print(f"    - {hab}  |  registros={len(hab.registros)}  |  activo={hab.activa}")

        elif opcion == 3:
            plan = seleccionar_plan()
            if plan is None:
                pausa()
                continue
            h = seleccionar_habito(plan)
            if h is None:
                pausa()
                continue
            fecha = leer_fecha("  Fecha (YYYY-MM-DD): ")
            try:
                if isinstance(h, HabitoBooleano):
                    resp = input("  ¿Cumplido? (s/n): ")
                    valor_bool = resp.lower() in ("s", "si", "sí")
                    h.registrar(fecha, valor_bool)
                else:
                    valor_num = leer_float("  Valor numérico: ", 0.0)
                    h.registrar(fecha, valor_num)
                nota = input("  Nota opcional (Enter para omitir): ").strip()
                if nota:
                    h.registros[-1].nota = nota
                print(f"  Registro añadido: {h.registros[-1]}")
            except HabitoInactivoError as e:
                print(f"  Error: {e}")
            except DuplicadoError as e:
                print(f"  Error: {e}")
            except TypeError as e:
                print(f"  Error: {e}")
            except ValueError as e:
                print(f"  Error: {e}")

        elif opcion == 4:
            plan = seleccionar_plan()
            if plan is None:
                pausa()
                continue
            h = seleccionar_habito(plan)
            if h is None:
                pausa()
                continue
            if not h.registros:
                print(f"  '{h.nombre}' no tiene registros aún.")
            else:
                print(f"\n  Registros de '{h.nombre}':")
                for r in h.registros:
                    print(f"    {r}")

        elif opcion == 5:
            plan = seleccionar_plan()
            if plan is None:
                pausa()
                continue
            h = seleccionar_habito(plan)
            if h is None:
                pausa()
                continue
            h.activa = not h.activa
            if h.activa:
                estado = "activado"
            else:
                estado = "desactivado"
            print(f"  Hábito '{h.nombre}' {estado}.")

        elif opcion == 6:
            break

        pausa()


def gestion_metas() -> None:
    while True:
        opcion = mostrar_menu("GESTIÓN DE METAS", [
            "Crear meta y añadirla a un plan",
            "Añadir hábito a una meta",
            "Añadir submeta a una meta",
            "Ver metas de un plan",
            "Volver",
        ])

        if opcion == 1:
            plan = seleccionar_plan()
            if plan is None:
                pausa()
                continue
            nombre = input("  Nombre de la meta: ").strip()
            peso = leer_float("  Peso (1-10): ", 1.0)
            meta_id = f"m_{nombre}_{len(plan.metas) + 1}"
            nueva_meta = Meta(id=meta_id, nombre=nombre, peso=peso)
            try:
                plan.add_meta(nueva_meta)
                print(f"  Meta '{nombre}' (peso={peso}) añadida al plan '{plan.nombre}'.")
            except DuplicadoError as e:
                print(f"  Error: {e}")

        elif opcion == 2:
            plan = seleccionar_plan()
            if plan is None:
                pausa()
                continue
            meta = seleccionar_meta(plan)
            if meta is None:
                pausa()
                continue
            h = seleccionar_habito(plan)
            if h is None:
                pausa()
                continue
            try:
                meta.add_habito(h)
                print(f"  Hábito '{h.nombre}' añadido a la meta '{meta.nombre}'.")
            except ValueError as e:
                print(f"  Error: {e}")

        elif opcion == 3:
            plan = seleccionar_plan()
            if plan is None:
                pausa()
                continue
            print("  Selecciona la meta PADRE:")
            padre = seleccionar_meta(plan)
            if padre is None:
                pausa()
                continue
            print("  Selecciona la meta HIJA:")
            hija = seleccionar_meta(plan)
            if hija is None:
                pausa()
                continue
            try:
                padre.add_hijo(hija)
                print(f"  '{hija.nombre}' añadida como submeta de '{padre.nombre}'.")
            except ValueError as e:
                print(f"  Error: {e}")

        elif opcion == 4:
            plan = seleccionar_plan()
            if plan is None:
                pausa()
                continue
            metas = plan.metas
            if not metas:
                print("  Este plan no tiene metas.")
            else:
                print(f"\n  Metas del plan '{plan.nombre}':")
                for m in metas:
                    print(f"    - {m}")

        elif opcion == 5:
            break

        pausa()


def ver_progreso() -> None:
    if usuario is None:
        return
    print("\n  Introduce el período de consulta:")
    inicio = leer_fecha("  Fecha inicio (YYYY-MM-DD): ")
    fin = leer_fecha("  Fecha fin   (YYYY-MM-DD): ")

    if inicio > fin:
        print("  La fecha de inicio no puede ser posterior a la de fin.")
        pausa()
        return

    try:
        planes = usuario.planes_activos()
    except PlanVacioError as e:
        print(f"  {e}")
        pausa()
        return

    print("--------------------------------------")
    print(f"  PROGRESO DE {usuario.nombre.upper()} ({inicio} → {fin})")
    print("--------------------------------------")

    total = usuario.progreso_total(inicio, fin)
    print(f"  Progreso global: {total / len(planes) * 100:.1f}%\n")

    for plan in planes:
        p = plan.progreso(inicio, fin)
        print(f"  Plan: {plan.nombre}")
        print(f"    Progreso: {p * 100:.1f}%")
        for meta in plan.metas:
            pm = meta.progreso(inicio, fin)
            print(f"    Meta '{meta.nombre}' (w={meta.peso}): {pm * 100:.1f}%")
        print()

    pausa()


def exportar_ficheros() -> None:
    if usuario is None:
        return
    opcion = mostrar_menu("EXPORTAR A FICHERO .TXT", [
        "Exportar historial de un hábito",
        "Exportar informe de progreso del usuario",
        "Volver",
    ])

    if opcion == 1:
        plan = seleccionar_plan()
        if plan is None:
            pausa()
            return
        h = seleccionar_habito(plan)
        if h is None:
            pausa()
            return
        nombre_archivo = input(f"  Nombre del fichero (Enter = historial_{h.nombre}.txt): ").strip()
        if not nombre_archivo:
            nombre_archivo = f"historial_{h.nombre}.txt"
        ruta = exportar_historial_habito(h, nombre_archivo)
        print(f"  Fichero guardado en: {ruta}")

    elif opcion == 2:
        print("  Introduce el período:")
        inicio = leer_fecha("  Fecha inicio (YYYY-MM-DD): ")
        fin = leer_fecha("  Fecha fin   (YYYY-MM-DD): ")
        nombre_archivo = input(f"  Nombre del fichero (Enter = informe_{usuario.nombre}.txt): ").strip()
        if not nombre_archivo:
            nombre_archivo = f"informe_{usuario.nombre}.txt"
        ruta = exportar_informe_progreso(usuario, inicio, fin, nombre_archivo)
        print(f"  Informe guardado en: {ruta}")

    pausa()


def menu_principal() -> None:
    if usuario is None:
        return
    while True:
        opcion = mostrar_menu(
            f"MENÚ PRINCIPAL  -  {usuario.nombre}",
            [
                "Gestión de Planes",
                "Gestión de Hábitos",
                "Gestión de Metas",
                "Ver Progreso",
                "Exportar a fichero .txt",
                "Salir",
            ]
        )
        if opcion == 1:
            gestion_planes()
        elif opcion == 2:
            gestion_habitos()
        elif opcion == 3:
            gestion_metas()
        elif opcion == 4:
            ver_progreso()
        elif opcion == 5:
            exportar_ficheros()
        elif opcion == 6:
            # guarda la sesión en pickle antes de salir
            ruta = guardar_sesion(usuario)
            print(f"\n  Sesión guardada en: {ruta}")
            break


def main() -> None:
    global usuario
    print("   SISTEMA DE HÁBITOS Y BIENESTAR")
    print("--------------------------------------")
    nombre = input("\nIntroduce tu nombre de usuario: ").strip()
    if not nombre:
        nombre = "Usuario"

    sesion = cargar_sesion(nombre)
    if sesion is not None:
        usuario = sesion
        print(f"\n  Bienvenido/a de nuevo, {usuario.nombre}")
        print(f"  (Sesión cargada: {len(usuario.planes)} plan(es) restaurado(s))")
    else:
        usuario_id = f"u_{nombre}_1"
        usuario = Usuario(id=usuario_id, nombre=nombre)
        print(f"\n  Bienvenido/a, {usuario.nombre} (nueva sesión)")

    menu_principal()


if __name__ == "__main__":
    main()
