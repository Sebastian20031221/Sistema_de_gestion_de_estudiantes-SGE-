"""
Ejecuta sge.py con entradas predefinidas y guarda la transcripción de la consola
(incluyendo lo que "teclea" el usuario) para generar las evidencias.
Uso: python ejecutar_caso.py entradas.txt salida.txt [max_estudiantes]
"""
import builtins
import io
import sys
import contextlib

sys.path.insert(0, __file__.rsplit("/pruebas/", 1)[0])
import sge  # noqa: E402

ruta_entradas, ruta_salida = sys.argv[1], sys.argv[2]
if len(sys.argv) > 3:
    sge.MAX_ESTUDIANTES = int(sys.argv[3])

with open(ruta_entradas, encoding="utf-8") as f:
    entradas = [linea.rstrip("\n") for linea in f if not linea.startswith("#")]

buffer = io.StringIO()


def input_simulado(mensaje=""):
    if not entradas:
        raise EOFError
    valor = entradas.pop(0)
    print(mensaje + valor)  # se muestra lo tecleado, como en una terminal real
    return valor


builtins.input = input_simulado
with contextlib.redirect_stdout(buffer):
    print("$ python sge.py")
    try:
        sge.main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n  Ejecución interrumpida por el usuario. Programa finalizado.\n")

with open(ruta_salida, "w", encoding="utf-8") as f:
    f.write(buffer.getvalue())
print(buffer.getvalue())
