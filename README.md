[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/09uckVan)´

# PROYECTO SOBRE PLANES SALUDABLES Y DEL BIENESTAR
#### ALUMNOS: Alejandro Paco, Nicolás Sánchez

## OBJETIVO DEL PROYECTO
El objetivo principal de este proyecto es proporcionar un motor estructurado para el seguimiento de hábitos y la consecución de objetivos personales. A través de una arquitectura jerárquica clara, permite a los Usuarios diseñar Planes de Bienestar compuestos por Metas (que pueden dividirse en submetas con diferentes niveles de importancia o "peso"), las cuales se alcanzan mediante el cumplimiento de Hábitos diarios, ya sean de acción (sí/no) o de cantidad. En esencia, el sistema busca cuantificar el desarrollo personal registrando el historial diario, manteniendo el recuento de rachas y calculando matemáticamente el progreso global en un rango de fechas, desde el impacto de una pequeña acción individual hasta el éxito general del plan del usuario.

## ESTRUCTURA DEL PROYECTO (ACTUAL):

```text
src/
│
├── usuarios/ (Gestión de Usuarios, Planes y Metas)
│   │
│   ├── CLASE: Usuario
│   │   ├── Atributos (Propiedades): id, nombre, planes
│   │   ├── Métodos: crear_plan(nombre), planes_activos(), progreso_total(inicio, fin)
│   │   └── Sobrecarga: __str__
│   │
│   ├── CLASE: PlanBienestar
│   │   ├── Atributos (Propiedades): nombre, metas, habitos, creado_en
│   │   ├── Métodos: add_habito(habito), progreso(inicio, fin)
│   │   └── Sobrecarga: __add__ (Unir planes), __lt__ (Comparar progresos), __len__, __str__
│   │
│   └── CLASE: Meta (Soporta anidamiento para Submetas)
│       ├── Atributos (Propiedades): id, nombre, peso, hijos, habitos
│       ├── Métodos: add_hijo(meta), add_habito(habito), progreso(inicio, fin)
│       └── Sobrecarga: __str__
│
└── habitos/ (Modelado de Hábitos y Registros)
    │
    ├── CLASE BASE: Habito (Abstracta - ABC)
    │   │
    │   ├── Atributos (Propiedades): id, nombre, regla, activa
    │   ├── Atributos (Solo lectura): registros, racha_actual
    │   ├── Métodos: registrar(fecha, valor) [Abstracto], _add_registro(registro), ajustar_racha(), progreso()
    │   ├── Sobrecarga: __eq__ (Igualdad por ID), __lt__ (Orden por racha), __len__, __str__, __repr__
    │   │
    │   ├── HERENCIA: HabitoBooleano (Para hábitos de "Sí/No")
    │   │   └── Métodos: registrar(fecha, valor) [Valida tipo bool]
    │   │
    │   └── HERENCIA: HabitoNumerico (Para hábitos de cantidad)
    │       ├── Atributos extra (Propiedades): unidad_medida
    │       └── Métodos: registrar(fecha, valor) [Valida tipo int/float]
    │
    └── CLASE DEPENDIENTE: Registro
        │
        ├── Atributos (Propiedades): fecha, valor, nota
        └── Sobrecarga: __lt__ (Orden cronológico por fecha), __str__, __repr__