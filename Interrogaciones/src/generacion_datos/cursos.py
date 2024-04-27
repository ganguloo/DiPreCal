import os
import pandas as pd
from parametros.parametros import PATH_LISTADO_CURSOS

def guardado_cursos(grafo_modulos, path=PATH_LISTADO_CURSOS):
    lista_cursos = list(grafo_modulos.nodes)
    dataframe_cursos = pd.DataFrame(lista_cursos, columns=["cursos"])
    dataframe_cursos.to_excel(path, index=False)
