import pandas as pd
import polars as pl
import time
import logging

def cursos_ingenieria(path_excel_cursos: str) -> pd.core.frame.DataFrame:
    """Retorna los cursos de Ingeniería junto con sus prerrequisitos y su sigla correspondiente.

    Args:
        path_excel_cursos (str): Corresponde a la ruta del archivo excel del listado de materias.

    Returns:
        pd.core.frame.DataFrame: Dataframe de los cursos de ingeniería.


    """

    materias_dataframe = pd.read_excel(path_excel_cursos)
    materias_dataframe.columns = materias_dataframe.columns.str.strip()
    materias_dataframe["Sigla"] = materias_dataframe["Materia"] + \
        materias_dataframe["Número Curso"].astype(str)
    cursos = materias_dataframe.filter(
        ["Escuela", "Nombre Curso", "Prerrequisitos", "Sigla"])

    # Se eliminan los cursos sin prerrequisito
    dataframe_filtrado = cursos.dropna(subset=["Prerrequisitos"])
    dataframe_ing = dataframe_filtrado.loc[dataframe_filtrado["Escuela"]
                                           == '04 - Ingeniería']

    dataframe_ing["Prerrequisitos"] = dataframe_ing["Prerrequisitos"].str.replace(
        "[()]", "")

    dataframe_ing.drop("Escuela", axis=1, inplace=True)
    return dataframe_ing


def diccionario_cursos_y_prerrequisitos(dataframe_ingenieria: pd.core.frame.DataFrame, materias) -> dict:
    """Retorna un diccionario de los cursos junto con sus requisitos, donde cada key es el nombre 
    del curso y el value asociado es una lista con los prerrequisitos.

    Args:
        dataframe_ingenieria (pd.core.frame.DataFrame): Corresponde a un DataFrame que contiene las
         columnas con el nombre de los cursos y los prerrequisitos.


    Returns:
        dict: Diccionario de los cursos con sus prerrequisitos.

    """

    lista_cursos = dataframe_ingenieria.values.tolist()
    dict_cursos_y_prerrequisitos = dict()
    for curso, prerrequisitos, sigla in lista_cursos: 
        # Lo que se hace aquí es eliminar las "o" de los prerrequisitos
        lista = prerrequisitos.strip().split("o")
        # Quitamos los whitespaces de todos los strings
        lista = list(map(str.strip, lista))
        # Con esto separamos en otras listas los prerrequisitos que tienen un "y"
        nueva_lista = [i.split("y") for i in lista]
        # Con esto de aquí removemos nuevamente los whitespaces de los strings
        for sublista in nueva_lista:
            for indice, value in enumerate(sublista):
                sublista[indice] = value.strip()

        '''# Creamos lista de equivalencias ESTO ESTA MAL PORQUE SE DEBE HACER LA LISTA PARA CADA CURSO DE LA LISTA DE PRERREQUISITOS
        excel = pd.read_excel(materias)
        excel = excel.values.tolist()
        equivalencias_curso = excel[n][13] #este n lo iba a sacar de cada iteracion de lista cursos, pero como indico mas arriba, no sirve
        equivalencias_curso = equivalencias_curso.strip().split("o")
        m = 0
        while m < len(equivalencias_curso) :
            if "y" in equivalencias_curso[m] :
                equivalencias_curso.pop(m)
            else:
                m += 1

        # Agregamos las equivalencias
        for m,lista_chica in enumerate(nueva_lista) : #esta lista contiene conjunto de cursos requisito
            for o,chequeo  in enumerate(lista_chica) :
                if 
        '''
                
        
        if len(nueva_lista) == 1:
            # Si es que solo hay un prerrequisito
            result = sum(nueva_lista, [])
            result = list(map(str.strip, result))

        else:
            # Si hay múltiples prerrequisitos, solo nos quedamos con todos los comunes a las disyunciones y uniones.
            result = list(set.intersection(*map(set, nueva_lista)))
        
        # print("La filtración resulto en ", result, "La lista original de prerrequisitos es ", prerrequisitos)
        dict_cursos_y_prerrequisitos[sigla] = result
        nombre = "diccionario_cursos_y_prerrequisitos"
        logging.debug(f"[Función: {nombre}]: El curso {sigla} tiene de prrequisitos {result}")

    return dict_cursos_y_prerrequisitos
