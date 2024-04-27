import polars as pl
import pandas as pd
import itertools


def  cursos_mod_dipre(path, cursos_ing, columnas: list = ["Nombre Curso", "Horario",
                                                         "Sigla_Seccion", "Lista Cruzada",
                                                         "Macrosección", "Escuela", "Sigla",
                                                         "Socio Integración", "Tipo Reunión",
                                                         "Vacantes Ofrecidas"],
                     reuniones=["CLAS - Cátedra",
                                "LAB - Laboratorio", "TAL - Taller"],
                     incluir_fmat = True, incluir_fis_y_qim = True,
                     identificadores_fmat = [], identificadores_fis_y_qim = []):
    """
    TODO
    Documentar
    """

    cursos = pl.read_excel(path,
                           read_csv_options={"infer_schema_length": 3000})
    new_columns = {col: col.strip() for col in cursos.columns}

    cursos = (cursos.rename(new_columns)
              .with_columns((pl.col("Materia") + pl.col(
                  "Número Curso") + "-" + pl.col("Sección").cast(pl.Utf8)).alias("Sigla_Seccion"))
              .with_columns((pl.col("Materia") + pl.col("Número Curso")).alias("Sigla"))
              .select(columnas)
              .filter(pl.col("Escuela") == "04 - Ingeniería")
              .filter(pl.col("Tipo Reunión").is_in(reuniones))
              )

    cursos_agrupado = cursos.groupby(by="Sigla_Seccion")
    lista_dataframes = list()

    for nombre_curso, dataframe in cursos_agrupado:
        union_horarios = "".join(dataframe["Horario"].to_list())

        dataframe_nuevo = dataframe.with_columns(
            pl.lit(union_horarios).alias("union_horarios"))

        valores_tipo_reunion = dataframe_nuevo.select(
            "Tipo Reunión").unique().to_numpy().tolist()
        valores_tipo_reunion = list(itertools.chain(*valores_tipo_reunion))

        if "CLAS - Cátedra" in valores_tipo_reunion:
            dataframe_nuevo = dataframe_nuevo.filter(
                pl.col("Tipo Reunión") == "CLAS - Cátedra")

        lista_dataframes.append(dataframe_nuevo)

    dataframe = (pl.concat(lista_dataframes)
                 .drop("Horario")
                 .filter(pl.col("union_horarios") != "CLAS - ")
                 .filter(pl.col("Sigla").is_in(cursos_ing)))
    
    # Añadimos los cursos de FMAT
    if incluir_fmat:
        cursos_fmat_dataframe = cursos_fmat(path, siglas_fmat=identificadores_fmat)
        cursos_fmat_dataframe = cursos_fmat_dataframe[dataframe.columns]
        dataframe = dataframe.extend(cursos_fmat_dataframe)
    
    # Añadimos otras facultades No me resulto
    if incluir_fis_y_qim:
        cursos_fisqim_dataframe = cursos_fis_y_qim(path, siglas_fis_qim=identificadores_fis_y_qim)
        cursos_fisqim_dataframe = cursos_fisqim_dataframe[dataframe.columns]
        dataframe = dataframe.extend(cursos_fisqim_dataframe)


    return dataframe


def cursos_fmat(path, columnas: list = ["Nombre Curso", "Horario",
                                        "Sigla_Seccion", "Lista Cruzada",
                                        "Macrosección", "Escuela", "Sigla",
                                        "Socio Integración", "Tipo Reunión",
                                        "Vacantes Ofrecidas"],
                reuniones=["CLAS - Cátedra"], siglas_fmat = []):
    cursos = pl.read_excel(path, read_csv_options={
                           "infer_schema_length": 3000})
    new_columns = {col: col.strip() for col in cursos.columns}
    # Se renombra una columna -> Se crea una nueva -> Se seleccionan ciertas columnas -> Se hace un filtrado
    cursos = (cursos.rename(new_columns)
              .with_columns((pl.col("Materia") + pl.col(
                  "Número Curso") + "-" + pl.col("Sección").cast(pl.Utf8)).alias("Sigla_Seccion"))
              .with_columns((pl.col("Materia") + pl.col("Número Curso")).alias("Sigla"))
              .select(columnas)
              .with_columns((pl.col("Horario")).alias("union_horarios"))
              .filter(pl.col("Tipo Reunión").is_in(reuniones))
              #.filter(pl.col("Socio Integración") == "04 - Ingeniería") #Se sacó en la última versión
              .filter(pl.col("Sigla").is_in(siglas_fmat))
              .filter(pl.col("Escuela").is_in(["06 - Matemáticas"])))
    return cursos

def cursos_fis_y_qim(path, columnas: list = ["Nombre Curso", "Horario",
                                        "Sigla_Seccion", "Lista Cruzada",
                                        "Macrosección", "Escuela", "Sigla",
                                        "Socio Integración", "Tipo Reunión",
                                        "Vacantes Ofrecidas"],
                reuniones=["CLAS - Cátedra"],
                siglas_fis_qim=[]):
    cursos = pl.read_excel(path, read_csv_options={
                           "infer_schema_length": 3000})
    new_columns = {col: col.strip() for col in cursos.columns}
    # Se renombra una columna -> Se crea una nueva -> Se seleccionan ciertas columnas -> Se hace un filtrado
    cursos = (cursos.rename(new_columns)
              .with_columns((pl.col("Materia") + pl.col(
                  "Número Curso") + "-" + pl.col("Sección").cast(pl.Utf8)).alias("Sigla_Seccion"))
              .with_columns((pl.col("Materia") + pl.col("Número Curso")).alias("Sigla"))
              .select(columnas)
              .with_columns((pl.col("Horario")).alias("union_horarios"))
              .filter(pl.col("Tipo Reunión").is_in(reuniones))
              #.filter(pl.col("Socio Integración") == "04 - Ingeniería") #Se sacó en la última versión
              .filter(pl.col("Sigla").is_in(siglas_fis_qim))
              .filter(pl.col("Escuela").is_in(["10 - Química", "03 - Física"])))
    return cursos

    """
        - Tendría que revisar si es que no hay cátedras, si es que hay, eliminamos todo el resto
        - Si es que no hay cátedra, revisamos si es que hay lab, en tal caso, eliminamos todo el resto
        - Si es que no hay cátedra ni lab, revisamos si hay taller, no hacemos nada, se queda como está en ese caso.
        No habría que eliminar ningún elemento
        """
