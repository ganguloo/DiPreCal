import pandas as pd
from datetime import datetime

def fechas_prohibidas(excel_file, sheet):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet)

    # Filter the DataFrame to select rows where the second column is 0 (not an available date)
    filtered_df = df[df.iloc[:, 1] == 0]

    # Extract the data from the first column of the filtered DataFrame, convert to string, and store them in a list
    lista_fechas = filtered_df.iloc[:, 0].dt.strftime("%d-%b").tolist()

    # Return the list of data with a value of 0 (not an available date)
    return lista_fechas


def excel_cursos_coordinados(excel_file, sheet):
    # Read the specified sheet of the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet)

    # Extract the data from the first column and store them in a list
    lista_cursos = df.iloc[:, 0].tolist()

    # Return the list of data from the first column
    return lista_cursos


def fijar_interrogaciones(excel_file, sheet):
    # Read the specified sheet of the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet)

    # Extract the data from the first three columns and store them in a list of lists
    first_three_columns_data = df.iloc[:, :3].values.tolist()

    fecha_inicio_clases = datetime(2023, 3, 6)

    cursos_coordinados = excel_cursos_coordinados(excel_file, "Cursos Coordinados")

    for prueba in first_three_columns_data:
        prueba[2] = (prueba[2] - fecha_inicio_clases).days
        if prueba[0] in cursos_coordinados:
            prueba[0] += "_Coordinado - Macroseccion"

    # Return the list of lists
    return first_three_columns_data


def mapeo_fechas(file_path, sheet_name, cell):
    # Read the entire sheet using pandas
    data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Convert cell reference to row and column index
    row_idx = int(cell[1:]) - 1
    col_idx = ord(cell[0].upper()) - ord('A')

    # Extract the value from the DataFrame
    fecha_retiro = data.iat[row_idx, col_idx]
    fecha_inicio_clases = datetime(2023, 3, 6)

    dias = (fecha_retiro - fecha_inicio_clases).days

    return dias

def mapeo(file_path, sheet_name, cell):
    # Read the entire sheet using pandas
    data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Convert cell reference to row and column index
    row_idx = int(cell[1:]) - 1
    col_idx = ord(cell[0].upper()) - ord('A')

    # Extract the value from the DataFrame
    valor = int(data.iat[row_idx, col_idx])

    return valor