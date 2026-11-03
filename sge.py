"""
Sistema de Gestión de Estudiantes (SGE) básico
------------------------------------------------
Aplicación por consola desarrollada en Python 3 para la asignatura
Algoritmos y Programación (grupo 2310 - 1A), Fundación Universitaria Compensar.

Autor: Joan Sebastián Quiñones Arias
Docente: Eliana Marcela Paez Perdomo
Repositorio: https://github.com/Sebastian20031221/Sistema_de_gestion_de_estudiantes-SGE-
Funcionalidades:
    1. Agregar estudiante
    2. Mostrar estudiantes (orden ascendente o descendente)
    3. Buscar estudiante por ID
    4. Ver estadísticas del grupo
    5. Salir del sistema

Requiere Python 3.10 o superior (usa la sentencia match-case).
"""

# ---------------------------------------------------------------------------
# CONSTANTES DE CONFIGURACIÓN
# ---------------------------------------------------------------------------
# Aunque las listas de Python crecen solas, se fija un tope para simular el
# comportamiento de un arreglo de tamaño fijo y practicar el control de límites
# que pide la actividad. Cambiar este valor no exige tocar el resto del código.
MAX_ESTUDIANTES = 50

NOTA_MINIMA = 0.0
NOTA_MAXIMA = 5.0          # escala de calificación usada en Colombia
NOTA_APROBATORIA = 3.0
EDAD_MINIMA = 14
EDAD_MAXIMA = 100


# ---------------------------------------------------------------------------
# FUNCIONES DE LECTURA Y VALIDACIÓN DE ENTRADAS
# ---------------------------------------------------------------------------
# Se separan en funciones propias porque la misma validación se necesita en
# varios lugares (menú, agregar, buscar). Así se evita repetir código y el
# programa nunca se cae si el usuario escribe algo inesperado.

def leer_entero(mensaje, minimo=None, maximo=None):
    """Pide un número entero hasta que el usuario ingrese uno válido."""
    while True:  # se repite hasta obtener un dato correcto
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            # int("abc") lanza ValueError: lo atrapamos para no detener el programa
            print("  [!] Debe ingresar un número entero. Intente de nuevo.")
            continue
        if minimo is not None and valor < minimo:
            print(f"  [!] El valor debe ser mayor o igual a {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"  [!] El valor debe ser menor o igual a {maximo}.")
        else:
            return valor


def leer_decimal(mensaje, minimo, maximo):
    """Pide un número decimal dentro de un rango (acepta coma o punto)."""
    while True:
        # En Colombia es común escribir 4,5 en lugar de 4.5, por eso se reemplaza
        texto = input(mensaje).strip().replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            print("  [!] Debe ingresar un número (ejemplo: 4.5). Intente de nuevo.")
            continue
        if minimo <= valor <= maximo:
            return round(valor, 1)
        print(f"  [!] El valor debe estar entre {minimo} y {maximo}.")


def leer_texto(mensaje, solo_letras=False, es_nombre_propio=False):
    """Pide un texto no vacío; opcionalmente exige que tenga solo letras y espacios."""
    while True:
        texto = " ".join(input(mensaje).split())  # quita espacios sobrantes
        if texto == "":
            print("  [!] Este campo no puede quedar vacío.")
        elif solo_letras and not texto.replace(" ", "").isalpha():
            print("  [!] Solo se permiten letras y espacios.")
        else:
            if es_nombre_propio:
                return texto.title()          # "laura gómez" -> "Laura Gómez"
            return texto[0].upper() + texto[1:]  # "ingeniería de software" -> "Ingeniería de software"


# ---------------------------------------------------------------------------
# FUNCIONES DE BÚSQUEDA Y PRESENTACIÓN (UNIDADES REUTILIZABLES)
# ---------------------------------------------------------------------------

def buscar_indice_por_id(estudiantes, id_buscado):
    """
    Búsqueda lineal (secuencial) de un estudiante por su ID.

    Retorna una tupla (indice, comparaciones):
      - indice: posición del estudiante en la lista, o -1 si no existe.
      - comparaciones: cuántas veces se comparó, útil para analizar Big-O.

    Se usa una variable bandera 'encontrado' y se corta el ciclo con break en
    cuanto aparece el ID, de modo que el mejor caso es O(1) y el peor O(n).
    """
    encontrado = False      # bandera: indica si ya apareció el ID
    indice = -1
    comparaciones = 0       # contador de comparaciones realizadas

    for posicion in range(len(estudiantes)):   # iteración ascendente
        comparaciones += 1
        if estudiantes[posicion]["id"] == id_buscado:
            encontrado = True
            indice = posicion
            break           # no tiene sentido seguir recorriendo

    # La bandera deja explícito el resultado: si nunca se activó, se retorna -1
    return (indice if encontrado else -1), comparaciones


def mostrar_estudiante(estudiante):
    """Imprime los datos de UN estudiante. Se reutiliza en Mostrar y en Buscar."""
    estado = "Aprobado" if estudiante["nota"] >= NOTA_APROBATORIA else "Reprobado"
    print(f"  ID: {estudiante['id']}")
    print(f"  Nombre: {estudiante['nombre']}")
    print(f"  Edad: {estudiante['edad']} años")
    print(f"  Programa: {estudiante['programa']}")
    print(f"  Nota: {estudiante['nota']:.1f}  ({estado})")


def imprimir_fila(numero, estudiante):
    """Imprime un estudiante como fila de tabla (formato compacto para listados)."""
    print(f"  {numero:<3} {estudiante['id']:<10} {estudiante['nombre']:<28} "
          f"{estudiante['edad']:<5} {estudiante['programa'][:28]:<28} {estudiante['nota']:.1f}")


def imprimir_titulo(texto):
    """Encabezado uniforme para cada sección de la consola."""
    print("\n" + "=" * 60)
    print(f"  {texto}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# FUNCIONALIDADES DEL MENÚ
# ---------------------------------------------------------------------------

def agregar_estudiante(estudiantes, total_estudiantes):
    """
    Registra un nuevo estudiante en la lista.
    Recibe el contador actual y retorna el contador actualizado.
    """
    imprimir_titulo("AGREGAR ESTUDIANTE")

    # Decisión simple: controlar que no se supere el tamaño máximo
    if total_estudiantes >= MAX_ESTUDIANTES:
        print(f"  [!] Capacidad máxima alcanzada ({MAX_ESTUDIANTES} estudiantes).")
        return total_estudiantes

    # El ID debe ser único; se repite la lectura mientras ya exista
    id_estudiante = leer_entero("  ID del estudiante: ", minimo=1)
    indice, _ = buscar_indice_por_id(estudiantes, id_estudiante)
    while indice != -1:
        print(f"  [!] Ya existe un estudiante con el ID {id_estudiante}.")
        id_estudiante = leer_entero("  Ingrese otro ID: ", minimo=1)
        indice, _ = buscar_indice_por_id(estudiantes, id_estudiante)

    nombre = leer_texto("  Nombre completo: ", solo_letras=True, es_nombre_propio=True)
    edad = leer_entero("  Edad: ", minimo=EDAD_MINIMA, maximo=EDAD_MAXIMA)
    programa = leer_texto("  Programa académico: ")
    nota = leer_decimal("  Nota promedio (0.0 - 5.0): ", NOTA_MINIMA, NOTA_MAXIMA)

    # Cada estudiante es un diccionario: agrupa sus datos con nombres claros
    nuevo_estudiante = {
        "id": id_estudiante,
        "nombre": nombre,
        "edad": edad,
        "programa": programa,
        "nota": nota,
    }
    estudiantes.append(nuevo_estudiante)   # O(1) amortizado
    total_estudiantes += 1                 # variable de conteo

    print(f"\n  [OK] Estudiante registrado. Total actual: {total_estudiantes}")
    return total_estudiantes


def mostrar_estudiantes(estudiantes, total_estudiantes):
    """Lista todos los estudiantes en orden de registro ascendente o descendente."""
    imprimir_titulo("LISTA DE ESTUDIANTES")

    if total_estudiantes == 0:
        print("  No hay estudiantes registrados todavía.")
        return

    print("  1. Orden de registro (primero al último)")
    print("  2. Orden inverso (último al primero)")
    orden = leer_entero("  Seleccione el orden: ", minimo=1, maximo=2)

    if orden == 1:
        # Iteración ascendente: 0, 1, 2, ..., n-1
        inicio, fin, paso = 0, total_estudiantes, 1
    else:
        # Iteración descendente: n-1, n-2, ..., 0
        inicio, fin, paso = total_estudiantes - 1, -1, -1

    print(f"\n  {'#':<3} {'ID':<10} {'Nombre':<28} {'Edad':<5} {'Programa':<28} Nota")
    print("  " + "-" * 80)
    numero = 1
    for posicion in range(inicio, fin, paso):
        imprimir_fila(numero, estudiantes[posicion])
        numero += 1
    print("  " + "-" * 80)
    print(f"  Total de estudiantes: {total_estudiantes}")


def buscar_estudiante(estudiantes, total_estudiantes):
    """Busca un estudiante por ID e informa si fue encontrado o no."""
    imprimir_titulo("BUSCAR ESTUDIANTE POR ID")

    if total_estudiantes == 0:
        print("  No hay estudiantes registrados para buscar.")
        return

    id_buscado = leer_entero("  Ingrese el ID a buscar: ", minimo=1)
    indice, comparaciones = buscar_indice_por_id(estudiantes, id_buscado)

    # Decisión simple: ¿se encontró o no?
    if indice != -1:
        print("\n  [OK] Estudiante encontrado:")
        mostrar_estudiante(estudiantes[indice])
    else:
        print(f"\n  [X] No existe ningún estudiante con el ID {id_buscado}.")
    print(f"  (Comparaciones realizadas: {comparaciones} de {total_estudiantes})")


def mostrar_estadisticas(estudiantes, total_estudiantes):
    """Calcula promedio, mejor nota y aprobados recorriendo la lista una sola vez."""
    imprimir_titulo("ESTADÍSTICAS DEL GRUPO")

    if total_estudiantes == 0:
        print("  No hay datos para calcular estadísticas.")
        return

    suma_notas = 0.0                 # acumulador
    aprobados = 0                    # contador
    mejor = estudiantes[0]           # variable auxiliar (máximo)

    # Un solo recorrido O(n) calcula las tres cosas a la vez
    for estudiante in estudiantes:
        suma_notas += estudiante["nota"]
        if estudiante["nota"] >= NOTA_APROBATORIA:
            aprobados += 1
        if estudiante["nota"] > mejor["nota"]:
            mejor = estudiante

    promedio = suma_notas / total_estudiantes
    print(f"  Estudiantes registrados: {total_estudiantes} de {MAX_ESTUDIANTES}")
    print(f"  Promedio general:        {promedio:.2f}")
    print(f"  Aprobados (>= {NOTA_APROBATORIA}):      {aprobados}")
    print(f"  Reprobados:              {total_estudiantes - aprobados}")
    print(f"  Mejor nota:              {mejor['nota']:.1f} ({mejor['nombre']})")


def mostrar_menu(total_estudiantes):
    """Imprime el menú principal (salida)."""
    imprimir_titulo(f"SISTEMA DE GESTIÓN DE ESTUDIANTES   [{total_estudiantes}/{MAX_ESTUDIANTES}]")
    print("  1. Agregar estudiante")
    print("  2. Mostrar estudiantes")
    print("  3. Buscar estudiante por ID")
    print("  4. Ver estadísticas")
    print("  5. Salir")


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    estudiantes = []          # estructura de datos: lista de diccionarios
    total_estudiantes = 0     # variable de conteo
    bandera_salir = False     # bandera que controla el ciclo principal

    # Repetición condicionada al comienzo: el menú se muestra mientras
    # el usuario no haya elegido salir.
    while not bandera_salir:
        mostrar_menu(total_estudiantes)
        opcion = leer_entero("  Seleccione una opción: ", minimo=1, maximo=5)

        # Decisión múltiple: equivalente en Python al switch de otros lenguajes
        match opcion:
            case 1:
                total_estudiantes = agregar_estudiante(estudiantes, total_estudiantes)
            case 2:
                mostrar_estudiantes(estudiantes, total_estudiantes)
            case 3:
                buscar_estudiante(estudiantes, total_estudiantes)
            case 4:
                mostrar_estadisticas(estudiantes, total_estudiantes)
            case 5:
                bandera_salir = True   # se activa la bandera y el while termina

    print("\n  Gracias por usar el SGE. ¡Hasta pronto!\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C o fin de entrada: se cierra de forma ordenada, sin traceback
        print("\n\n  Ejecución interrumpida por el usuario. Programa finalizado.\n")
