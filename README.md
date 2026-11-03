# Sistema de Gestión de Estudiantes (SGE) básico

Aplicación por consola en **Python** para registrar, listar y buscar estudiantes.
Trabajo de la asignatura **Algoritmos y Programación** (grupo 2310 - 1A), Fundación Universitaria Compensar.

- **Estudiante:** Joan Sebastián Quiñones Arias (jsquinones@ucompensar.edu.co)
- **Instructora:** Eliana Marcela Paez Perdomo
- **Fecha:** 2 de noviembre de 2026
- **Repositorio:** https://github.com/Sebastian20031221/Sistema_de_gestion_de_estudiantes-SGE-

## Funcionalidades

| Opción | Descripción |
|---|---|
| 1. Agregar estudiante | Registra ID, nombre, edad, programa y nota. Valida cada dato y no admite IDs repetidos ni superar la capacidad máxima (50). |
| 2. Mostrar estudiantes | Lista todos los registros en orden de registro (ascendente) o inverso (descendente). |
| 3. Buscar por ID | Búsqueda lineal; informa si se encontró y cuántas comparaciones hizo. |
| 4. Ver estadísticas | Promedio general, aprobados/reprobados y mejor nota. |
| 5. Salir | Activa la bandera de salida y termina el programa. |

## Requisitos y ejecución

Clonar el repositorio:

```bash
git clone https://github.com/Sebastian20031221/Sistema_de_gestion_de_estudiantes-SGE-.git
cd Sistema_de_gestion_de_estudiantes-SGE-
```


Python **3.10 o superior** (se usa `match-case`). No necesita librerías externas.

```bash
python sge.py
```

## Conceptos aplicados

- **Estructuras de control:** `while` (menú y validaciones), `match-case` (decisión múltiple), `if/elif/else`, `for` ascendente y descendente, `try/except`.
- **Variables especiales:** contador `total_estudiantes`, bandera `bandera_salir`, bandera `encontrado`, acumulador `suma_notas`.
- **Estructura de datos:** lista de diccionarios con tamaño máximo controlado.
- **Eficiencia:** búsqueda O(n), agregar O(n) (por la verificación de duplicados), mostrar y estadísticas O(n).

## Estructura del repositorio

```
sge.py                      Programa principal
diagramas/                  Diagramas de flujo (fuente .mmd e imagen .png)
pruebas/                    Entradas de los casos de prueba y salidas obtenidas
  ejecutar_caso.py          Ejecuta sge.py con un archivo de entradas
  medir_eficiencia.py       Medición empírica de la búsqueda lineal vs. diccionario
capturas/                   Evidencias de ejecución
SGE_Documentacion_Tecnica.pdf
```

Para repetir un caso de prueba:

```bash
python pruebas/ejecutar_caso.py pruebas/caso_completo.txt pruebas/salida_completa.txt
python pruebas/ejecutar_caso.py pruebas/caso_limite.txt pruebas/salida_limite.txt 2
```
