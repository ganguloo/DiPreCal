import networkx as nx
import datetime
import logging
from filtracion_archivos.modulos import (cursos_y_horario,
                                         limpieza_cursos,
                                         ramos_mismo_modulo)
from filtracion_archivos.modulos_polars import cursos_y_horario_polars
from filtracion_archivos.modulos_mod_dipre import cursos_mod_dipre
from datos.intersecciones_modulos import generacion_intersecciones_modulos
from itertools import filterfalse


def grafo_mismo_modulo(path_excel_nrc: str, cursos_ing_considerar) -> nx.classes.graph.Graph:
    """
    TODO
    Hacer documentación de esta función.
    """
    # cursos_con_horario = cursos_y_horario_polars(path_excel_nrc, cursos_ing_considerar)
    # lista_cursos = cursos_con_horario.values.tolist()
    cursos_con_horario = cursos_mod_dipre(path_excel_nrc,
                                          cursos_ing_considerar)  # Recordar que si cambio esta linea, tambn lo tengo
    # que cambiar en el main
    cursos_con_horario = cursos_con_horario.select(["Nombre Curso",
                                                    "union_horarios",
                                                    "Sigla_Seccion"]).to_pandas()
    lista_cursos = cursos_con_horario.values.tolist()

    set_horarios, lista_horarios = limpieza_cursos(lista_cursos)
    generacion_intersecciones_modulos(set_horarios, lista_horarios)
    dict_ramos_mismo_modulo = ramos_mismo_modulo(set_horarios, lista_horarios)

    ramo_seccion_topes_combinaciones = dict()

    for key, value in dict_ramos_mismo_modulo.items():

        for ramo in value:
            # Lo que hace este filterfalse, es hacer una combinación de un ramo con todo el resto
            # de ramos que tiene tope.
            lista_ramos_con_tope = list(
                filterfalse(lambda x: x == ramo, value))
            # Verificar que todas las conexiones de los grafos iniciales estén en el grafo final
            # f"[MODULO]: {key}. [RAMO] {ramo}, [COMBINACIONES] {lista_ramos_con_tope}")
            if ramo not in ramo_seccion_topes_combinaciones.keys():
                ramo_seccion_topes_combinaciones[ramo] = lista_ramos_con_tope

            else:
                if ramo_seccion_topes_combinaciones[ramo] is not None:
                    # Aquí había un extend y lo cambiamos por un +, con eso se arregló
                    ramo_seccion_topes_combinaciones[ramo] = ramo_seccion_topes_combinaciones[ramo] + \
                        lista_ramos_con_tope
                else:
                    ramo_seccion_topes_combinaciones[ramo] = lista_ramos_con_tope

    grafo = nx.Graph()
    for ramo, lista_topes in ramo_seccion_topes_combinaciones.items():

        if len(lista_topes) != 0:
            for ramo_tope in lista_topes:
                grafo.add_edge(ramo, ramo_tope, relacion="Tope horario")
                logging.debug(f"[Funcion: grafo_mismo_modulo]: El curso {ramo} tiene tope de horario con {ramo_tope}")

        else:
            grafo.add_node(ramo)

    return grafo


def reemplazar_siglas_con_macrosecciones(grafo_tope_horario: nx.classes.graph.Graph,
                                         macrosecciones_y_ramos_sigla: dict,
                                         cursos_a_eliminar) -> nx.classes.graph.Graph:
    """
    TODO

    Hacer documentación.
    """

    macrosecciones_tope_horario = dict()
    lista_nodos = list(grafo_tope_horario.nodes)
    macrosecciones_sin_topes = list()

    for macroseccion, value in macrosecciones_y_ramos_sigla.items():
        lista_vecinos = list()

        for sigla_seccion in value:
            if sigla_seccion in lista_nodos:
                # Pasa que hay unas siglas seccion que no están en el grafo. Debe ser donde son
                # ayudantías.
                vecinos = grafo_tope_horario.neighbors(sigla_seccion)
                lista_vecinos.extend(vecinos)
                # lista_vecinos += vecinos

        if len(lista_vecinos) != 0:
            if macroseccion not in macrosecciones_tope_horario.keys():
                macrosecciones_tope_horario[macroseccion] = lista_vecinos
            else:
                macrosecciones_tope_horario[macroseccion] = macrosecciones_tope_horario[macroseccion].extend(
                    lista_vecinos)
        elif len(lista_vecinos) == 0 :
            macrosecciones_sin_topes.append(macroseccion)

        nombre = "reemplazar_siglas_con_macrosecciones"        
        if len(lista_vecinos) != 0 :
            logging.debug(f"[Función: {nombre}]: {macroseccion} tiene de vecinos a {macrosecciones_tope_horario[macroseccion]}")
        elif len(lista_vecinos) == 0 :
            logging.debug(f"[Función: {nombre}]: {macroseccion} no tiene vecinos")

    

    lista_nodos = list(grafo_tope_horario.nodes)
    for nodo in cursos_a_eliminar:
        if nodo in lista_nodos:
            grafo_tope_horario.remove_node(nodo)

    for macroseccion, siglas in macrosecciones_tope_horario.items():
        for sigla in siglas:
            grafo_tope_horario.add_edge(macroseccion, sigla)

    for macroseccion in macrosecciones_sin_topes :
        grafo_tope_horario.add_node(macroseccion)

    return grafo_tope_horario


if __name__ == "__main__":
    pass
