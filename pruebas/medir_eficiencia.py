"""
Mide de forma empírica el costo de la búsqueda lineal (la usada en el SGE)
frente a una búsqueda en diccionario, para respaldar el análisis Big-O.
Se busca el peor caso: un ID que no existe (recorre toda la lista).
"""
import timeit

for n in (50, 1_000, 10_000, 100_000):
    lista = [{"id": i, "nombre": f"Est {i}"} for i in range(1, n + 1)]
    diccionario = {e["id"]: e for e in lista}
    id_inexistente = -5

    def lineal():
        for e in lista:
            if e["id"] == id_inexistente:
                return e
        return None

    def hash_dict():
        return diccionario.get(id_inexistente)

    rep = 200
    t_lineal = timeit.timeit(lineal, number=rep) / rep * 1e6
    t_dict = timeit.timeit(hash_dict, number=rep) / rep * 1e6
    print(f"{n};{t_lineal:.2f};{t_dict:.3f}")
