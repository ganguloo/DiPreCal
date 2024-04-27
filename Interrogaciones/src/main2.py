import os
import pandas as pd
import networkx as nx
import time
import itertools

from filtracion_archivos.prerrequisitos import diccionario_cursos_y_prerrequisitos
from filtracion_archivos.prerrequisitos_polars import (
    cursos_ingenieria_polars)

from filtracion_archivos.modulos_polars import cursos_y_horario_polars

from filtracion_archivos.modulos import (cursos_y_horario,
                                         cursos_con_macroseccion)

from generacion_datos.conexiones import guardado_conexiones
from generacion_datos.cursos import guardado_cursos
from generacion_datos.vacantes import guardar_vacantes

from grafos.mismo_modulo import grafo_mismo_modulo, reemplazar_siglas_con_macrosecciones
from grafos.graph_addition import nuevos_arcos, juntar_grafos_prerrequisitos_y_modulos
from grafos.prerrequisito import anadir_arcos_transitividad, grafo_prerrequisito
from grafos.drawing import dibujar_grafo


def main():
    # Primero formamos el grafo de los prerrequisitos
    start_time = time.time()
    path_excel_materias = os.path.join("excel_horarios",
                                       "Listado_materias.xlsx")
    # dataframe_ing = cursos_ingenieria(path_excel_materias)
    dataframe_ing = cursos_ingenieria_polars(
        path_excel_materias)  # Funciona bien

    cursos = diccionario_cursos_y_prerrequisitos(
        dataframe_ing)  # Pedir validación al profe

    # print(cursos)
    grafo_prerrequisitos = grafo_prerrequisito(cursos)

    # Se hace para que el arco vaya del prerrequisito al ramo
    grafo_prerrequisitos = grafo_prerrequisitos.reverse()
    print(
        f"El grafo de prerrequisitos antes de la transitividad es {grafo_prerrequisitos}")
    # Debería de funcionar bien
    anadir_arcos_transitividad(grafo_prerrequisitos)
    print(
        f"El grafo de prerrequisitos luego de la transitividad es {grafo_prerrequisitos}")
    arcos_nuevos = nuevos_arcos(grafo_prerrequisitos)  # Funciona bien.
    # Ahora se forma el grafo de los modulos

    path_excel_nrc = os.path.join("excel_horarios", "Listado_NRC.xlsx")
    cursos_con_horario = cursos_y_horario(path_excel_nrc)
    # print(cursos_con_horario)
    # cursos_con_horario = cursos_y_horario_polars(path_excel_nrc)
    # Hasta aquí no ha desaparecido ningún ramo

    # Ver lo de las macrosecciones. Por ejemplo, opti no aparece, pues las cátedras no están agrupadas como macrosección
    # pero si bajo la misma lista cruzada
    macrosecciones = cursos_con_macroseccion(cursos_con_horario)

    # Tener cuidado, porque se repite ICT3113-2, revisar si tiene clases en días distintos
    cursos_pertenecientes_a_macroseccion = set(itertools.
                                               chain(*list(macrosecciones.values())))

    # print(cursos_pertenecientes_a_macroseccion)  # Ejemplificar con esto
    grafo_modulos = grafo_mismo_modulo(path_excel_nrc)

    # Hasta aquí siguen ciertas secciones
    grafo_modulos = reemplazar_siglas_con_macrosecciones(grafo_modulos,
                                                         macrosecciones,
                                                         cursos_pertenecientes_a_macroseccion)
    # A partir de aquí desaparacen ciertas secciones
    cursos_en_macroseccion = dict()

    for macroseccion, sigla_secc in macrosecciones.items():
        for i in sigla_secc:
            cursos_en_macroseccion[i] = macroseccion
    # print(cursos_en_macroseccion)
    print("El grafo de los modulos antes de juntarlo con los prerrequsitos es ", grafo_modulos)
    juntar_grafos_prerrequisitos_y_modulos(grafo_modulos,
                                           grafo_prerrequisitos,
                                           cursos_en_macroseccion,
                                           cursos_pertenecientes_a_macroseccion)
    print("El grafo de los modulos luego de juntarlo con los prerrequsitos es", grafo_modulos)

    # OJO CON ICM2503
    # print(len(vacantes_sigla_seccion), len(lista_cursos))

    # Guardado de datos
    guardado_conexiones(grafo_modulos)
    guardado_cursos(grafo_modulos)
    guardar_vacantes(grafo_modulos, macrosecciones)
    # title = "Grafo de ramos y respectivos módulos, con macrosecciones y prerrequisitos"
    # dibujar_grafo(title, grafo_modulos)
    print("El grafo al final es ", grafo_modulos)
    # print("El tiempo total de ejecución es ", time.time() - start_time)
    lista_nodos = list(grafo_modulos.nodes)

    # for nodo in lista_nodos:
    # vecinos = [x for x in grafo_modulos.neighbors(nodo)]
    # print(f"El nodo es {nodo} y sus vecinos son {vecinos}")

    grafo_pd = nx.to_pandas_edgelist(grafo_modulos)
    grafo_pd.to_excel(os.path.join("instancia_datos", "grafo_edgelist.xlsx"), index=False)

    nx.write_edgelist(grafo_modulos, "grafo_modulos_edgelist.txt", data=False, delimiter = ";")

if __name__ == "__main__":
    main()
