import pandas as pd
import itertools


def generar_ies_cursos(path_cursos) -> dict:
    data = pd.read_excel(path_cursos)
    data = data.values.tolist()
    listado_cursos = list(itertools.chain(*data))

    cursos_ies = dict()

    for curso in listado_cursos:
        # De momento todos los cursos tienen dos interrogaciones
        cursos_ies[curso] = [1, 2]

    return cursos_ies
