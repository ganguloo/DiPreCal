import pandas as pd
import itertools

from datos.generacion_calendario import generacion_calendario

# No sé si es mejor generar las fechas aquí, o pasarselas de una a la función
# Ahí ver que es mejor


def generar_fechas_cursos(path_cursos, fechas_validas: list) -> dict:
    data = pd.read_excel(path_cursos)
    data = data.values.tolist()
    listado_cursos = list(itertools.chain(*data))

    cursos_fechas = dict()

    for curso in listado_cursos:
        # De momento, todas las fechas son validas para todos los cursos
        cursos_fechas[curso] = fechas_validas

    return cursos_fechas
