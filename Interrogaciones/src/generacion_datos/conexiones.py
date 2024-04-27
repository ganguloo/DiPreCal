import os
import pandas as pd

from parametros.parametros import PATH_CONEXIONES

def guardado_conexiones(grafo_modulos, path=PATH_CONEXIONES):
    diccionario_conexiones = dict()

    for nodo in grafo_modulos.nodes:
        vecinos = [x for x in grafo_modulos.neighbors(nodo)]

        for vecino in vecinos:
            diccionario_conexiones[f"{nodo}, {vecino}"] = 1 # Ojo con esto. Es lo mismo que poner vecino, nodo


    dataframe_conexiones = pd.DataFrame.from_dict(diccionario_conexiones.items())
    dataframe_conexiones.to_excel(path, index=False)

