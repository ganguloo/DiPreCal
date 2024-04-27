import pandas as pd
import re
import polars as pl
import logging

def cursos_y_horario(path_excel_listado_nrc: str,
                     columnas: list = ["Nombre Curso", "Horario",
                                       "Sigla_Seccion", "Lista Cruzada",
                                       "Macrosección"]) -> pd.core.frame.DataFrame:
    """Retorna un dataframe que contiene únicamente los módulos de las cátedras junto a otras
    columnas. Por defecto, también incluye el nombre del curso, horario, sigla y seccion, lista
    cruzada y macrosección.

    Args:
        path_excel_listado_nrc (str): Corresponde a la ruta del archivo excel del listado NRC.

    Returns:
        pd.core.frame.DataFrame: Dataframe de los cursos junto a sus módulos.


    """

    cursos = pd.read_excel(path_excel_listado_nrc)
    # print(cursos)
    cursos["Sigla_Seccion"] = cursos["Materia"] + \
        cursos["Número Curso"].astype(str) + \
        "-" + cursos["Sección"].astype(str)
    listado_cursos = cursos.filter(columnas)
    catedras_y_ayudantias = listado_cursos[listado_cursos["Horario"].str.contains(
        "CLAS") == True]

    return catedras_y_ayudantias


def cursos_y_horario_polars(path_excel_listado_nrc: str,
                            reuniones=["CLAS - Cátedra",
                                       "LAB - Laboratorio",
                                       "TAL - Taller"]):
    cursos = pl.read_excel(path_excel_listado_nrc,
                           read_csv_options={"infer_schema_length": 3000})

    new_columns = {col: col.strip() for col in cursos.columns}
    cursos = (cursos.rename(new_columns)
              .with_columns((pl.col("Materia") + pl.col(
                  "Número Curso") + "-" + pl.col("Sección").cast(pl.Utf8)).alias("Sigla_Seccion"))
              .with_columns((pl.col("Materia") + pl.col("Número Curso")).alias("Sigla"))
              .filter(pl.col("Tipo Reunión").is_in(reuniones))
              .filter(pl.col("Escuela") == "04 - Ingeniería")
              )
    return cursos


def limpieza_cursos(lista_cursos: list) -> tuple[set, list]:
    """Limpia el dataframe que contiene las clases y ayudantías, eliminando la parte de CLAS y AYU.
      Además, elimina los whitespaces de los strings.

     Args:
        lista_cursos (list): Corresponde a la lista de los cursos y sus módulos.

     Returns:
        tuple[set, list]: Una tupla que contiene un set de los módulos y una lista de listas, donde
         cada lista es de la forma [nombre_curso, módulos].

    """

    lista_horarios = list()
    set_horarios = set()

    for nombre_curso, horario, sigla, *others in lista_cursos:
        replacements = {"CLAS -": "", "LAB -": "", "TAL - ": ""}

        horas_y_dias_clase = reemplazar_substrings(horario, replacements)

        horas_y_dias_clase = horas_y_dias_clase.replace("a", ":")
        horas_y_dias_clase = horas_y_dias_clase.split(";")
        horas_y_dias_clase.pop()

        for indice, dia in enumerate(horas_y_dias_clase):
            horas_y_dias_clase[indice] = dia.strip()
            set_horarios.add(dia.strip())

        lista_horarios.append([sigla, horas_y_dias_clase])

    return (set_horarios, lista_horarios)


def ramos_mismo_modulo(set_horarios: set, lista_horarios: list) -> dict:
    """Recibe el set de horarios y la lista de horarios entregados por la función limpieza_cursos.
     Entrega un diccionario de los módulos y cursos asociados.

     Args:
        set_horarios (set): Contiene los módulos.
        lista_horarios (list): Es una lista de listas de la forma [nombre_curso, modulos]

     Returns:
        dict[str, list]: Retorna un diccionario donde cada key es un módulo y el value asociado es
          una lista con todos los cursos que usan ese módulo.
    """

    ramos_mismo_modulo = dict()

    for modulo in set_horarios:
        cursos_mismo_horario = list()

        for curso, modulo_curso in lista_horarios:
            if modulo in modulo_curso:
                cursos_mismo_horario.append(curso)

        if modulo not in ramos_mismo_modulo.keys():
            ramos_mismo_modulo[modulo] = cursos_mismo_horario
        else:
            ramos_mismo_modulo[modulo] = ramos_mismo_modulo[modulo] + \
                cursos_mismo_horario
    return ramos_mismo_modulo


def cursos_con_macroseccion(dataframe):
    """Retorna diccionario donde cada key es un ramo con su sigla y sección y el value asociado
    a la key es un string donde aparece la lista cruzada y la macrosección a la que pertenece.

    """
    materias_dataframe = dataframe.copy()
    # Se eliminan los cursos que no tienen lista cruzada
    materias_dataframe = dataframe.dropna(subset=["Lista Cruzada"])
    # materias_dataframe = dataframe.dropna(subset=["Macrosección"])
    grouped_cursos = materias_dataframe.groupby(["Lista Cruzada"])
    grupos = list(grouped_cursos.groups.keys())

    macro_seccion_y_sigla = dict()
    for ramos in grupos:
        ramo_macroseccion = grouped_cursos.get_group(ramos)
        valores = list(
            set(ramo_macroseccion["Macrosección"].values.tolist()))[0]
        if "Macrosección" in valores:
            macrosecc_filter = ramo_macroseccion.filter(
                ["Sigla_Seccion", "Lista Cruzada", "Macrosección"])

            macrosecc_filter["identificacion_grafo"] = macrosecc_filter["Lista Cruzada"] + "_" + \
                macrosecc_filter["Macrosección"]

            macrosecc_filter = macrosecc_filter.drop(
                columns=["Lista Cruzada", "Macrosección"])

            for ramo_sigla_seccion in macrosecc_filter.values.tolist():

                sigla_y_seccion = ramo_sigla_seccion[0]
                macroseccion = ramo_sigla_seccion[1]
                logging.debug(f"[Función: cursos_con_macroseccion]: {sigla_y_seccion} pertenece a la macrosección {macroseccion}")
                if macroseccion not in macro_seccion_y_sigla.keys():
                    macro_seccion_y_sigla[macroseccion] = [sigla_y_seccion]
                else:
                    macro_seccion_y_sigla[macroseccion] = macro_seccion_y_sigla[macroseccion] + [
                        sigla_y_seccion]

    return macro_seccion_y_sigla


def reemplazar_substrings(cadena, reemplazos):
    # Iterar sobre los reemplazos y aplicarlos a la cadena
    for buscar, reemplazar in reemplazos.items():
        cadena = re.sub(buscar, reemplazar, cadena)

    return cadena


if __name__ == "__main__":
    pass
