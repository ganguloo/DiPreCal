import polars as pl
import os


def cursos_y_horario_polars(path_excel_listado_nrc: str,
                            cursos_ing_a_considerar,
                            columnas: list = ["Nombre Curso", "Horario",
                                              "Sigla_Seccion", "Lista Cruzada",
                                              "Macrosección", "Escuela", "Sigla",
                                              "Socio Integración"],

                            siglas_fmat=["MAT1630", "EYP1113", "MAT1610",
                                         "MAT1620", "MAT1640", "MAT1203"]):
    """Retorna un dataframe que contiene únicamente los módulos de las cátedras junto a otras
    columnas. Por defecto, también incluye el nombre del curso, horario, sigla y seccion, lista
    cruzada y macrosección.

    Args:
        path_excel_listado_nrc (str): Corresponde a la ruta del archivo excel del listado NRC.

    Returns:
        pd.core.frame.DataFrame: Dataframe de los cursos junto a sus módulos.


    """

    cursos = pl.read_excel(path_excel_listado_nrc, read_csv_options={
                           "infer_schema_length": 3000})
    new_columns = {col: col.strip() for col in cursos.columns}
    # Se renombra una columna -> Se crea una nueva -> Se seleccionan ciertas columnas -> Se hace un filtrado
    cursos = (cursos.rename(new_columns)
              .with_columns((pl.col("Materia") + pl.col(
                  "Número Curso") + "-" + pl.col("Sección").cast(pl.Utf8)).alias("Sigla_Seccion"))
              .with_columns((pl.col("Materia") + pl.col("Número Curso")).alias("Sigla"))
              .select(columnas)
              .filter(pl.col("Horario").str.contains("CLAS"))
              .filter(pl.col("Escuela").is_in(["06 - Matemáticas", "04 - Ingeniería"])))
    #   .filter(pl.col("Socio Integración") == "04 - Ingeniería") # No sé si esta línea es necesaria o no
    # Me atrevería adecir que no, ya que hay cursos de ing que se dictan a otras facultades.

    # Consideramos solo los cursos de FMAT que se dictan a la facultad de ingeniería
    cursos_fmat = (cursos.filter(pl.col("Escuela") == "06 - Matemáticas")
                   .filter(pl.col("Socio Integración") == "04 - Ingeniería")
                   .filter(pl.col("Sigla").is_in(siglas_fmat)))

    # Aquí están los cursos solo de ING, por lo que aquí puedo sacar los que no están en la lista de cursos de ing que
    # necesitan prueba
    cursos = (cursos.filter(pl.col("Escuela") != "06 - Matemáticas")
              .filter(pl.col("Sigla").is_in(cursos_ing_a_considerar)))

    # cursos = cursos.extend(cursos_fmat)
    # print(cursos)

    horarios_eliminar = ['CLAS - ', 'CLAS - L: a ; M: a ; W: a ; J: a ; V: a ; ',
                         'CLAS - J: a ; V: a ; S: a ; ', 'CLAS - W: a ; J: a ; V: a ; ', 'CLAS - W: a ; ']
    mask = ~cursos["Horario"].is_in(horarios_eliminar)
    cursos = cursos.filter(mask)
    return cursos.to_pandas()
