[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/09uckVan)

# Sistema de Hábitos y Bienestar

**Alumnos:** Alejandro Paco · Nicolás Sánchez  
**Asignatura:** Programación Orientada a Objetos. Trabajo Final C2

---

## Descripción

Proyecto de POO en Python para el seguimiento de hábitos personales y la consecución de objetivos de bienestar. El sistema permite diseñar **Planes de Bienestar** compuestos por **Metas** jerárquicas (con submetas y pesos de importancia), que se alcanzan mediante el cumplimiento diario de **Hábitos** booleanos o numéricos. Se cuantifica el progreso global en un rango de fechas, desde el impacto de una pequeña acción individual hasta el éxito total del plan.

La sesión se guarda automáticamente en un fichero binario (pickle) al salir, y se restaura al volver a entrar con el mismo nombre. Asegurando así la persistencia.

---

## Cómo ejecutar
### Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Ejecutar proyecto
```bash
cd src
python main.py
```

Al arrancar se pide el nombre de usuario. Si existe una sesión guardada para ese nombre, se carga automáticamente. A partir de ahí se navega por un menú interactivo en terminal.

```
 SISTEMA DE HÁBITOS Y BIENESTAR
 ------------------------------

  Introduce tu nombre de usuario: Alex

  Bienvenido/a de nuevo, Alex!
  (Sesión cargada: 2 plan(es) restaurado(s))

--------------------------------------
  MENÚ PRINCIPAL  -  Alex
--------------------------------------
  1. Gestión de Planes
  2. Gestión de Hábitos
  3. Gestión de Metas
  4. Ver Progreso
  5. Exportar a fichero .txt
  6. Salir
--------------------------------------
```

---

## Estructura del proyecto

```
trabajo-final-c2/
│
├── data/                           Generada automáticamente al guardar
│   ├── sesion_<nombre>.pickle      Persistencia entre sesiones (binario)
│   ├── historial_<habito>.txt      Exportaciones de historial
│   └── informe_<usuario>.txt       Exportaciones de progreso
│
└── src/
    │
    ├── main.py                     Punto de entrada · menú interactivo
    │
    ├── core/                       Entidades principales del dominio
    │   ├── usuario.py              Clase Usuario
    │   ├── planBienestar.py        Clase PlanBienestar
    │   └── meta.py                 Clase Meta (soporta anidamiento)
    │
    ├── habitos/                    Modelado de hábitos y registros
    │   ├── habito.py               Clase abstracta Habito (ABC)
    │   ├── habitoBooleano.py       Hábitos Sí/No
    │   ├── habitoNumerico.py       Hábitos de cantidad
    │   └── registro.py             Clase Registro (fecha + valor + nota)
    │
    ├── reglas/                     Reglas de cumplimiento
    │   ├── reglaHabito.py          Clase abstracta ReglaHabito (ABC)
    │   ├── regla_frecuencia.py     ReglaFrecuencia
    │   ├── regla_umbral.py         ReglaUmbral
    │   └── regla_rango.py          ReglaRango
    │
    ├── excepciones/
    │   └── errores.py              Excepciones personalizadas del dominio
    │
    └── utilidades/
        └── storage.py              Exportación .txt y persistencia pickle
```

---

## Persistencia y ficheros

### Sesión automática (con pickle)

Al seleccionar la opción de **Salir** en el menú, el objeto `Usuario` completo (con todos sus planes, metas, hábitos y registros) se serializa mediante `pickle` en `data/sesion_<nombre>.pickle`. Así, la próxima vez que se ejecute el programa con el mismo nombre, el estado se restaura.

```
Sesión guardada en: /data/sesion_alex.pickle
```

### Exportaciones manuales (ficheros .txt)

Desde la opción **"Exportar a fichero .txt"** del menú se pueden generar dos tipos de informes en `data/`:

**Historial de hábito**
```
HISTORIAL DE HÁBITO: Beber 2L Agua
Tipo: HabitoNumerico
Estado: Activo
Racha actual: 3 días
Total registros: 5

Fecha           Valor           Nota

2026-03-01      2.5             Buen día
2026-03-02      2.0             -
```

**Informe de progreso**
```
INFORME DE PROGRESO
Usuario: Alex (ID: u_alex_1)
Período: 2026-03-01 - 2026-03-31

PROGRESO GLOBAL: 80.0%

PLAN: Operación Verano 2026
  Progreso del plan: 80.0%
  Metas:
    - Salud General (peso=10): 80.0%
        - Beber 2L Agua: 100.0% (5 registros)
        - Leer 10 páginas: 60.0% (3 registros)
```

---

## Clases y API

### `Usuario`

| Método / Propiedad | Descripción |
|---|---|
| `__init__(id, nombre)` | Crea el usuario |
| `crear_plan(nombre)` -> `PlanBienestar` | Crea y registra un nuevo plan |
| `planes_activos()` -> `list[PlanBienestar]` | Lista de planes (lanza `PlanVacioError` si no hay ninguno) |
| `progreso_total(inicio, fin)` -> `float` | Suma de progresos de todos los planes |
| `planes` | Propiedad de solo lectura, devuelve copia |

---

### `PlanBienestar`

| Método / Propiedad | Descripción |
|---|---|
| `__init__(nombre)` | Crea el plan con timestamp automático |
| `add_habito(habito)` | Añade un hábito, lanza `DuplicadoError` si ya existe |
| `add_meta(meta)` | Añade una meta, lanza `DuplicadoError` si ya existe |
| `progreso(inicio, fin)` -> `float` | Media del progreso de todas las metas `[0.0 – 1.0]` |
| `__add__(otro)` | `plan_a + plan_b`: nuevo plan combinado |
| `__lt__(otro)` | `plan_a < plan_b`: compara progresos desde la creación |
| `__len__` | Número de hábitos del plan |

---

### `Meta`

| Método / Propiedad | Descripción |
|---|---|
| `__init__(id, nombre, peso)` | `peso` (0, 10], importancia relativa dentro del plan |
| `add_habito(habito)` | Asocia un hábito a esta meta |
| `add_hijo(meta)` | Añade una submeta (anidamiento jerárquico) |
| `progreso(inicio, fin)` -> `float` | Combina progreso de hábitos y submetas, ponderado por peso |

---

### `Habito` (abstracta · ABC)

Subclases concretas: `HabitoBooleano` y `HabitoNumerico`.

| Método / Propiedad | Descripción |
|---|---|
| `__init__(id, nombre, regla, activa=True)` | Constructor base |
| `registrar(fecha, valor)` | Registra un valor, lanza `DuplicadoError` o `HabitoInactivoError` |
| `progreso(inicio, fin)` -> `float` | % de registros que cumplen la regla `[0.0 – 1.0]` |
| `ajustar_racha()` | Recalcula la racha de días consecutivos cumplidos |
| `registros` | Lista de `Registro` (solo lectura) |
| `racha_actual` | Días consecutivos cumplidos (solo lectura) |
| `__eq__` | Igualdad por `id` |
| `__lt__` | Orden por racha actual |
| `__len__` | Número de registros |

- **`HabitoBooleano`** — `registrar(fecha, valor: bool)`
- **`HabitoNumerico`** — `registrar(fecha, valor: int | float)`. atributo extra `unidad_medida`

---

### `Registro`

| Atributo | Tipo | Descripción |
|---|---|---|
| `fecha` | `date` | Día del registro |
| `valor` | `bool \| int \| float` | Valor registrado |
| `nota` | `str \| None` | Comentario opcional |
| `__lt__` |  | Orden cronológico, permite `list.sort()` |

---

### Reglas de cumplimiento

Todas heredan de `ReglaHabito` (ABC) e implementan `cumplido(registros, inicio, fin) -> bool`.

| Clase | Constructor | Se cumple cuandoS |
|---|---|---|
| `ReglaFrecuencia` | `(frecuencia, veces_objetivo)` | hay ≥ `veces_objetivo` registros en el período |
| `ReglaUmbral` | `(frecuencia, objetivo_minimo)` | la suma de valores ≥ `objetivo_minimo` |
| `ReglaRango` | `(frecuencia, minimo, maximo)` | todos los valoresS [`minimo`, `maximo`] |

---

## Excepciones personalizadas

Definidas en `excepciones/errores.py`, todas heredan de `Exception`.

| Excepción | Cuándo se lanza |
|---|---|
| `PlanVacioError` | `usuario.planes_activos()` si el usuario no tiene planes |
| `DuplicadoError` | Añadir hábito, meta o registro que ya existe |
| `HabitoInactivoError` | `habito.registrar()` cuando el hábito está desactivado |
| `FechaInvalidaError` | Fecha de inicio posterior a la de fin en exportaciones o progreso |

---

## Jerarquía de herencia

```
object
├── Usuario
├── PlanBienestar
├── Meta
├── Registro
├── Habito  (ABC)
│   ├── HabitoBooleano
│   └── HabitoNumerico
└── ReglaHabito  (ABC)
    ├── ReglaFrecuencia
    ├── ReglaUmbral
    └── ReglaRango
```

---

## Sobrecarga de operadores

| Clase | Operador | Significado |
|---|---|---|
| `PlanBienestar` | `+` | Une dos planes en uno nuevo |
| `PlanBienestar` | `<` | Compara progresos desde la fecha de creación |
| `PlanBienestar` | `len()` | Número de hábitos |
| `Habito` | `==` | Igualdad por ID |
| `Habito` | `<` | Orden por racha actual |
| `Habito` | `len()` | Número de registros |
| `Registro` | `<` | Orden cronológico por fecha |

---

## Dependencias

Python ≥ 3.10.  
mypy (sirve para comprorbar que el proyecto cumple la sugerencia de tipos)  
[requirements.txt](./requirements.txt)


```bash
python -m mypy src/  # pasa sin errores
```
