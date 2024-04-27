import polars as pl


def cursos_ingenieria_polars(path_excel_cursos: str, incluir_mat: bool, incluir_fis_y_qim: bool, identificadores_fmat: list, identificadores_fis_y_qim: list) -> pl.DataFrame: 
    """Retorna los cursos de Ingeniería junto con sus prerrequisitos y su sigla correspondiente.
        Si se agrega, incluye cursos de MAT, FIS y QIM
    Args:
        path_excel_cursos (str): Corresponde a la ruta del archivo excel del listado de materias.

    Returns:
        pl.DataFrame: Dataframe de los cursos de ingeniería.
    """

    materias_dataframe_main = pl.read_excel(path_excel_cursos)
    new_columns = {col: col.strip() for col in materias_dataframe_main.columns}
    materias_dataframe = (materias_dataframe_main.rename(new_columns)
                          .with_columns(((pl.col("Materia") + pl.col("Número Curso")).alias("Sigla")))
                          .select(["Escuela", "Nombre Curso", "Prerrequisitos", "Sigla"])
                          .drop_nulls(subset=["Prerrequisitos"])
                          .filter(pl.col("Escuela") == '04 - Ingeniería')
                          .with_columns(pl.col("Prerrequisitos").str.replace_all("[()]", ""))
                          .drop("Escuela"))
    
    if incluir_mat :
        materias_mat_dataframe = (materias_dataframe_main.rename(new_columns)
                            .with_columns(((pl.col("Materia") + pl.col("Número Curso")).alias("Sigla")))
                            .select(["Escuela", "Nombre Curso", "Prerrequisitos", "Sigla"])
                            .drop_nulls(subset=["Prerrequisitos"])
                            .filter((pl.col("Escuela") == '06 - Matemáticas') & (pl.col("Sigla").is_in(identificadores_fmat)))
                            .with_columns(pl.col("Prerrequisitos").str.replace_all("[()]", ""))
                            .drop("Escuela"))
        materias_dataframe.extend(materias_mat_dataframe)
    if incluir_fis_y_qim :
        materias_fisqim_dataframe = (materias_dataframe_main.rename(new_columns)
                            .with_columns(((pl.col("Materia") + pl.col("Número Curso")).alias("Sigla")))
                            .select(["Escuela", "Nombre Curso", "Prerrequisitos", "Sigla"])
                            .drop_nulls(subset=["Prerrequisitos"])
                            .filter(((pl.col("Escuela") == '03 - Física') |(pl.col("Escuela") == '10 - Química')) & (pl.col("Sigla").is_in(identificadores_fis_y_qim)))
                            .with_columns(pl.col("Prerrequisitos").str.replace_all("[()]", ""))
                            .drop("Escuela"))
        materias_dataframe.extend(materias_fisqim_dataframe)

    return materias_dataframe.to_pandas()
