import plotly.express as px
import plotly.io as pio
from bokeh.models import HoverTool
from bokeh.plotting import figure, output_file, save
import pandas as pd
import os
import networkx as nx
import re
import polars as pl
import plotly.graph_objects as go
import sys
import matplotlib.pyplot as plt
# plt.style.use('seaborn')


from datos.generacion_calendario import generacion_calendario
from modelo_optimizacion.cargar_datos.cargar_vacantes import cargar_vacantes
from modelo_optimizacion.cargar_datos.cargar_colores import datos_colores_grafo

from generacion_parametros.interrogaciones_curso import generar_ies_cursos
from generacion_parametros.fechas_interrogacion_curso import generar_fechas_cursos

from filtracion_archivos.modulos_mod_dipre import cursos_mod_dipre
from filtracion_archivos.cursos_con_ies import cursos_con_pruebas
from filtracion_archivos.modulos import limpieza_cursos, cursos_y_horario, cursos_y_horario_polars

from filtracion_archivos.modulos_mod_dipre import cursos_fmat
from parametros.parametros import PATH_LISTADO_NRC, PATH_CURSOS_IES

from datos.interrogaciones import organizacion_datos_interrogaciones, interrogaciones_mes

from resultados.grafico_dias import graficar_dias
from resultados.cupos_fmat_ing import grafico_vacantes_fmat_ing
from parametros.cursos_fechas import CONJUNTO_FECHAS
fechas_validas, mapeo_fechas, fechas = generacion_calendario()
# vacantes = cargar_vacantes()
# print(CONJUNTO_FECHAS["T1_MS1 - Macrosección 1"])

vacantes = cargar_vacantes()
with open("resultados_rest_vacantes.txt", "r", encoding="utf-8") as file:
    lineas = [i.strip() for i in file.readlines() if i.startswith("z")]
    cursos = set()
    for i in lineas:
        msg = i.split("=")[0].replace("[", "").replace("]", "").replace("z", "").split(",")[0]
        # print(msg)
        cursos.add(msg)

    for i in cursos:
        print(i)
    print(len(cursos))

# with open("resultados_rest_vacantes.txt", "r", encoding="utf-8") as result:
    # lineas = [i.strip() for i in result.readlines() if i.startswith("x")]
    # print(lineas)for i in lineas:print(i)

# print(mapeo_fechas)


# print(vacantes)
# fechas_actualizado = organizacion_datos_interrogaciones(mapeo_fechas, "resultados_rest_vacantes.txt")
# print(mapeo_fechas)
# print(fechas_validas)
# print(fechas_validas)
# print(mapeo_fechas)




# graficar_dias_bokeh(mapeo_fechas, fechas_actualizado)
# graficar_dias_plotly(mapeo_fechas, fechas_actualizado)


# graficar_dias(mapeo_fechas, fechas_actualizado)
# grafico_vacantes_fmat_ing(fechas_validas, fechas_actualizado, mapeo_fechas, vacantes)
# Otro grafico
# vacantes_fechas_ing = {n: 0 for n in mapeo_fechas.values()}
# vacantes_fechas_mat = {n: 0 for n in mapeo_fechas.values()}
# cursos_fechas_nombres = {n: 0 for n in mapeo_fechas.values()}

# IDENTIFICADORES_FMAT = ["EYP_MOD", "XN_MOD", "WV_MOD", "YF_MOD", "GCH_MOD", "ED_MOD"]

# for fecha in fechas_validas:
#     lista_cursos = list()
#     mapeo = mapeo_fechas[fecha]
#     cant_vacantes_ing = 0
#     cant_vacantes_mat = 0
#     for curso in fechas_actualizado:
#         if curso[1] == mapeo:
#             lista_cursos.append(curso[0])
#             curso_fmat_bool = any(i in curso[0] for i in IDENTIFICADORES_FMAT)

#             if curso_fmat_bool:
#                 cant_vacantes_mat += vacantes.get(curso[0], 0)
#             else:
#                 cant_vacantes_ing += vacantes.get(curso[0], 0)

#         vacantes_fechas_mat[mapeo] = cant_vacantes_mat
#         vacantes_fechas_ing[mapeo] = cant_vacantes_ing

#     cursos_fechas_nombres[mapeo] = lista_cursos

# print(cursos_fechas_nombres)


# x = list(mapeo_fechas.values())
# vacantes_ing = list(vacantes_fechas_ing.values())
# vacantes_fmat = list(vacantes_fechas_mat.values())

# fig = go.Figure(go.Bar(x=x, y=vacantes_ing, name="Vacantes Ingeniería"))
# fig.add_trace(go.Bar(x=x, y=vacantes_fmat, name="Vacantes FMAT"))

# fig.update_layout(barmode='stack')
# fig.write_html("Vacantes_FMAT_ING.html")
# fig.show()


# print(x)
# print(y)
# print(cursos_fechas_nombres)

# print(fecha)

# print(vacantes_fechas_ing)
# abril = interrogaciones_mes("Apr", fechas_actualizado, fechas)
# print(abril)

# print(vacantes)


# path = os.path.join("instancia_datos", "listado_cursos.xlsx")
# path_excel_nrc = os.path.join("excel_horarios", "Listado_NRC_2023_Enero.xlsx")
# path = os.path.join("excel_horarios", "Listado_NRC.xlsx")
# cursos_horario = cursos_y_horario(path)
# cursos_2 = cursos_y_horario_polars(path_excel_nrc)
# cursos_2 = cursos_2.select(["Sigla_Seccion",
# "Vacantes Ofrecidas"])
# cursos = cursos_fmat(PATH_LISTADO_NRC)
# cursos_ing_ies = cursos_con_pruebas(PATH_CURSOS_IES)
# cursos_2 = cursos_mod_dipre(PATH_LISTADO_NRC, cursos_ing_ies)
# cursos = cursos[cursos_2.columns]
#
# a = cursos.columns
# b = cursos_2.columns
#
# print(cursos)
# actualizado = cursos_2.extend(cursos)
# for i in b:
# if i not in a:
# print(i)
# a = pl.concat([cursos_2.select(cursos.columns) for df in [df1, df2, df3, ..., dfn])
# print(cursos.columns)
# print(cursos_2.columns)
# print(cursos_horario)
# print(cursos_2)
# path_cursos_ies = os.path.join("excel_horarios", "004 - Listado_NRC_Programados.xlsx")
# cursos_ing_ies = cursos_con_pruebas(path_cursos_ies)
# cursos = cursos_mod_dipre(path_excel_nrc, cursos_ing_ies)
# cursos = cursos.select(["Nombre Curso", "union_horarios", "Sigla_Seccion", ]).to_pandas()
# lista_cursos = cursos.values.tolist()
#
# set_horarios, lista_horarios = limpieza_cursos(lista_cursos)


# lista_cursos = cursos.values.tolist()

# print(f"La lista de cursos es {lista_cursos}")
# print(lista_cursos[0])
# set_horarios, lista_horarios = limpieza_cursos(lista_cursos)

# path = os.path.join("excel_horarios", "004 - Listado_NRC_Programados.xlsx")
# cursos = cursos_con_pruebas(path)


# generar_ies_cursos(path)
# fechas_validas, mapeo_fechas, *placeholder = generacion_calendario()

# fechas_calendario = list(fechas_validas.keys())
# A partir del 31 de Marzo empezamos a considerar fechas válidas
# fechas_calendario = fechas_calendario[25:]
# a, b, c = generacion_calendario()
# print(b)
# cursos_fechas = generar_fechas_cursos(path, fechas_calendario)
# print(cursos_fechas)


# datos_colores, arcos_restantes, grafo = datos_colores_grafo(os.path.join("grafo_main"))
# print(grafo)
# lista_nodos = list(grafo.nodes)
# print(lista_nodos)
# mapeo_macrosseciones_label = dict()
# for nodo in lista_nodos:
# if "Macrosección" in nodo:
# nombre = nodo.replace("Macrosección", "Macroseccion")
# mapeo_macrosseciones_label[nodo] = nombre
# print(nodo, nombre)


# grafo = nx.relabel_nodes(grafo, mapeo_macrosseciones_label)
# lista_nodos = list(grafo.nodes)
#
# for i in lista_nodos:
# print(i)
# print(datos_colores[43])
# print(datos_colores)

# for lista_cursos in datos_colores.values():
# print(lista_cursos)
# for indice, cursos in enumerate(lista_cursos):
# curso_1 = cursos[0]
# curso_2 = cursos[1]

# if "Macrosección" in curso_1:
# curso_1 = curso_1.replace("Macrosección", "Macroseccion")
# cursos = curso_1
# if "Macrosección" in curso_2:
# curso_2 = curso_2.replace("Macrosección", "Macroseccion")
# cursos_1 = curso_2
# print(cursos)
# for curso_1, curso_2 in datos_colores[43]:
# print(curso_1, curso_2)

# print(arcos_restantes)

# a = [("Macrosección_1", "Macrosección_2")]


# print(len(arcos_restantes))
# print(arcos_restantes)

# print(datos_colores[43])

# for value in datos_colores.values():
# print(type(value), len(value))
# for val in value:
# print(val)

# for curso_1, curso_2 in arcos_restantes:
# print(curso_1, curso_2)
# a = datos_colores[10]
# a = list(datos_colores.values())
# print(a)
# print(curso)

# for key, value in a.items():
# print(c1[0])
# print(key, value)
# print(type(c1))
# print(c1, c2)
# for color, arcos in datos_colores.items():
# print(arcos)
# fo
# print(list(datos_colores.values()))

# dias_prohibidos = ["30-Mar", "04-Apr", "05-Apr", "06-Apr",
#    "07-Apr", "08-Apr", "09-Apr", "10-Apr",
#    "11-Apr", "12-Apr", "27-Apr", "29-Apr",
#    "01-May", "02-May", "03-May", "04-May",
#    "05-May", "06-May", "07-May", "08-May",
#    "09-May", "15-May", "16-May", "31-May",
#    "07-Jun", "16-Jun", "21-Jun", "24-Jun",
#    "26-Jun"]
# fechas_validas, mapeo = generacion_calendario()
# vacantes = cargar_vacantes()


# print(vacantes)

# num_vacantes = 0
# with open("LWV_4.txt", 'r', encoding="utf-8") as file:

# cursos_lwv_4 = [i.strip() for i in file.readlines()]
# print(len(cursos_lwv_4))

# for curso in cursos_lwv_4:
# numero = vacantes.get(curso, 0)
# num_vacantes += numero

# print(f"Cantidad total vacantes I1 LWV:4 {num_vacantes}")
# print(vacantes)
# print(fechas)
# print(mapeo)

# for key, value in mapeo.items():
# print(key, value)

# for key, value in fechas_validas.items():
# print(key, value)

# for fecha in fechas:
# print(fecha.strftime("%d-%b"))

# fechas = [fecha.strftime("%d-%b") for fecha in fechas]
# print(fechas)


# excel_fechas = pd.DataFrame(fechas.keys(), columns=["Fecha"])
# excel_fechas.to_excel(os.path.join(
# "instancia_datos", "fechas.xlsx"), index=False)
