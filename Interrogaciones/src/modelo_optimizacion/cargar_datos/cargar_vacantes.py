import os
import pandas as pd


def cargar_vacantes(path=os.path.join("instancia_datos", "vacantes.xlsx")):
    vacantes = pd.read_excel(path)
    vacantes = dict(vacantes.values)
    keys_eliminar = []
    nuevo_dict = dict()

    for key, values in vacantes.items():

        if "Macrosección" in key:
            x = key.replace("Macrosección", "Macroseccion")
            nuevo_dict[x] = vacantes[key]
            keys_eliminar.append(key)

    for key in keys_eliminar:
        del vacantes[key]

    vacantes.update(nuevo_dict)
    return vacantes
