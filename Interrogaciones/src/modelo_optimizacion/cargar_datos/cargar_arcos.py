import os
import pandas as pd

def cargar_arcos(path=os.path.join("instancia_datos", "conexiones.xlsx")):
    conexiones = pd.read_excel(path)
    return dict(conexiones.values)
