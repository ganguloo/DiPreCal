import os
import pandas as pd
import unicodedata


def cargar_cursos(path=os.path.join("instancia_datos", "listado_cursos.xlsx")):
    cursos = pd.read_excel(path)
    cursos = cursos.values.tolist()
    cursos = [i[0] for i in cursos]

    for indice, curso in enumerate(cursos):
        cursos[indice] = ''.join((c for c in unicodedata.normalize(
            'NFD', curso) if unicodedata.category(c) != 'Mn'))

    return cursos
