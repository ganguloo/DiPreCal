import os
import pandas as pd

from filtracion_archivos.modulos import cursos_y_horario, cursos_y_horario_polars
from filtracion_archivos.modulos_mod_dipre import cursos_mod_dipre
from parametros.parametros import (PATH_LISTADO_NRC, PATH_VACANTES, IDENTIFICADORES_FIS_Y_QIM,
                                   IDENTIFICADORES_FMAT, INCLUIR_FIS_Y_QIM, INCLUIR_MAT)


def guardar_vacantes(grafo_modulos,
                     macrosecciones,
                     path=PATH_LISTADO_NRC,
                     path_guardar=PATH_VACANTES,
                     cursos_ing_ies=[]):

    lista_cursos = list(grafo_modulos.nodes)
    # vacantes_dataframe = cursos_y_horario(path, columnas)
    # vacantes_dataframe = vacantes_dataframe.filter(["Sigla_Seccion",
    # "Vacantes Ofrecidas"])
    vacantes_dataframe = cursos_mod_dipre(path, cursos_ing_ies, incluir_fmat = INCLUIR_MAT, 
                                          incluir_fis_y_qim = INCLUIR_FIS_Y_QIM, 
                                          identificadores_fmat = IDENTIFICADORES_FMAT, 
                                          identificadores_fis_y_qim = IDENTIFICADORES_FIS_Y_QIM)
    # vacantes_dataframe = cursos_y_horario_polars(path_excel_listado_nrc=path)
    vacantes_dataframe = vacantes_dataframe.select(["Sigla_Seccion",
                                                    "Vacantes Ofrecidas"]).to_pandas()

    vacantes_sigla_seccion = dict(vacantes_dataframe.values)

    keys_curso_en_macroseccion = list()

    for macroseccion, conjunto_secciones in macrosecciones.items():

        total_vacantes = 0
        for seccion_sigla in conjunto_secciones:
            vacantes = vacantes_sigla_seccion.get(seccion_sigla, 0)
            total_vacantes += vacantes
            keys_curso_en_macroseccion.append(seccion_sigla)

        vacantes_sigla_seccion[macroseccion] = total_vacantes

    for key in keys_curso_en_macroseccion:
        if key in vacantes_sigla_seccion.keys():
            # Removemos de las vacantes los cursos que pertenecen a las macrosecciones
            del vacantes_sigla_seccion[key]

    dataframe_vacantes = pd.DataFrame.from_dict(vacantes_sigla_seccion.items())
    dataframe_vacantes.to_excel(path_guardar, index=False)
