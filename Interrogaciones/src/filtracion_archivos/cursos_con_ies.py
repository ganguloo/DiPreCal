import polars as pl
import logging

def cursos_con_pruebas(path_excel,
                       excluir_siglas=["IIC1005", "IIC2413", "IIC2513",
                                       "IIC2552", "IIC2233", "ING2030",
                                       "ING1004"],
                       columnas_interes=["Escuela", "Nombre Curso", "Sigla"]
                       ) -> list:
    cursos = pl.read_excel(path_excel, sheet_name="Deben tener Ies",
                           read_csv_options={"infer_schema_length": 3000})
    new_columns = {col: col.strip() for col in cursos.columns}

    cursos = (cursos.rename(new_columns)
              .with_columns((pl.col("Materia") + pl.col("Número Curso").cast(str)).alias("Sigla"))
              .select(columnas_interes)
              .filter(~pl.col("Sigla").is_in(excluir_siglas)))

    siglas_validas = cursos.select("Sigla").unique()
    siglas_validas = siglas_validas["Sigla"].to_list()
    return siglas_validas

def cursos_mat_con_pruebas(path_nrc,columnas_interes=["Escuela", "Nombre Curso", "Sigla"],siglas_fmat = []) -> list: 

    cursos = pl.read_excel(path_nrc, read_csv_options={"infer_schema_length": 3000})
    new_columns = {col: col.strip() for col in cursos.columns}

    cursos = (cursos.rename(new_columns)
              .with_columns((pl.col("Materia") + pl.col("Número Curso").cast(str)).alias("Sigla"))
              .select(columnas_interes)
              .filter((pl.col("Escuela") == '06 - Matemáticas') & (pl.col("Sigla").is_in(siglas_fmat))))

    siglas_validas = cursos.select("Sigla").unique()
    siglas_validas = siglas_validas["Sigla"].to_list()
    return siglas_validas

def cursos_fisqim_con_pruebas(path_nrc,columnas_interes=["Escuela", "Nombre Curso", "Sigla"],siglas_fisqim = []) -> list: 

    cursos = pl.read_excel(path_nrc, read_csv_options={"infer_schema_length": 3000})
    new_columns = {col: col.strip() for col in cursos.columns}

    cursos = (cursos.rename(new_columns)
              .with_columns((pl.col("Materia") + pl.col("Número Curso").cast(str)).alias("Sigla"))
              .select(columnas_interes)
              .filter(((pl.col("Escuela") == '03 - Física') |(pl.col("Escuela") == '10 - Química')) & (pl.col("Sigla").is_in(siglas_fisqim))))

    siglas_validas = cursos.select("Sigla").unique()
    siglas_validas = siglas_validas["Sigla"].to_list()
    return siglas_validas
