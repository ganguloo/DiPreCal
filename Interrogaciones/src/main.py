import os
import networkx as nx
import time
import itertools
import logging
import json
import sys

from filtracion_archivos.prerrequisitos import diccionario_cursos_y_prerrequisitos
from filtracion_archivos.prerrequisitos_polars import cursos_ingenieria_polars

from filtracion_archivos.modulos_polars import cursos_y_horario_polars
from filtracion_archivos.modulos import (cursos_y_horario,
                                         cursos_con_macroseccion)

from filtracion_archivos.modulos_mod_dipre import cursos_mod_dipre
from filtracion_archivos.cursos_con_ies import (cursos_con_pruebas, cursos_mat_con_pruebas,
                                                cursos_fisqim_con_pruebas)

from generacion_datos.conexiones import guardado_conexiones
from generacion_datos.cursos import guardado_cursos
from generacion_datos.vacantes import guardar_vacantes
from generacion_datos.cursos_coordinados import coordinados_a_macrosecciones

from grafos.mismo_modulo import grafo_mismo_modulo, reemplazar_siglas_con_macrosecciones
from grafos.graph_addition import nuevos_arcos, juntar_grafos_prerrequisitos_y_modulos
from grafos.prerrequisito import anadir_arcos_transitividad, grafo_prerrequisito
from grafos.drawing import dibujar_grafo

from parametros.parametros import (PATH_CURSOS_IES, PATH_LISTADO_NRC,PATH_LISTADO_NRC_ORIGINAL,PATH_CURSOS_IES_ORIGINAL, PATH_MATERIAS,
                                   IDENTIFICADORES_FMAT, CURSOS_3_IES, CURSOS_COORDINADOS, SEC_COORDINADAS,
                                   INCLUIR_FIS_Y_QIM, INCLUIR_MAT, IDENTIFICADORES_FIS_Y_QIM, PATH_IES,
                                   PATH_FECHAS)

from datos.generacion_calendario import generacion_calendario

def main(crear_parametros_ies=True, crear_parametros_fechas=True):
    logging.basicConfig(filename='debug.log', encoding='utf-8',
                        level=logging.DEBUG, filemode="w")
    
    # -------- MACROSECCIONES CURSOS Y SECCIONES COORDINADAS ---------
    if crear_parametros_ies:
        coordinados_a_macrosecciones(PATH_CURSOS_IES_ORIGINAL,PATH_LISTADO_NRC_ORIGINAL,CURSOS_COORDINADOS,SEC_COORDINADAS)

    # Francisco 5 de Mayo: Para que se usa después lo de coordinados_a_macrosecciones. ¿Cuál es el sentido
    # de hacer esto, si antes ya estaba hecho de que se juntaban los cursos al momento de crear los grafos?
    # Preguntarle al profe

    # Documentación:

    # -- GRAFO PRERREQUISITOS --
    # coordinados_a_macrosecciones: Si tiene
    # cursos_ingenieria_polars: Si tiene
    # diccionario_cursos_y_prerrequisitos: Si tiene
    # grafo_prerrequisito: No tiene -> Igual es medio autoexplicativo
    # anadir_arcos_transitividad: No tiene -> Igual es medio autoexplicativo
    # nuevos_arcos: Si tiene


    # -- GRAFO MÓDULOS --
    # cursos_con_pruebas: No tiene -> Me imagino que retorna todos los cursos que si tienen pruebas.
    # es medio autoexplicativo igual, de ahí revisarlo.
    # cursos_mat_con_pruebas: No tiene -> Me imagino que es lo mismo que arriba
    # cursos_fisquim_con_pruebas: No tiene -> Me imagino que es lo mismo que arriba
    # cursos_mod_dipre: No tiene documentación. OJO Con que hay un comentario con que intentaron
    # implementar algo y no funcionó. Comentar profesor angulo si lo arreglaron y no borraron el comentario
    # o realmente no funciona. De ahí agregar la documentación, ya entendí lo que hace.
    # cursos_con_macroseccion: Si tiene
    # reemplazar_siglas_con_macrosecciones: No tiene, pero es autoexplicativo el nombre. De ahí ver
    # si alcanzo a hacerle documentación
    # juntar_grafos_prerrequisitos_y_modulos: No tiene



    # -------- GRAFO PRERREQUISITOS -------
    start_time = time.time() #Creo que se debe mover arriba
    dataframe_ing = cursos_ingenieria_polars(PATH_MATERIAS, INCLUIR_MAT, INCLUIR_FIS_Y_QIM, IDENTIFICADORES_FMAT, IDENTIFICADORES_FIS_Y_QIM)  # Funciona bien

    cursos = diccionario_cursos_y_prerrequisitos(dataframe_ing, PATH_MATERIAS)
    grafo_prerrequisitos = grafo_prerrequisito(cursos)
    logging.info(f"El grafo de prerrequisitos antes de la transitividad es {grafo_prerrequisitos}")
    anadir_arcos_transitividad(grafo_prerrequisitos)
    logging.info(f"El grafo de prerrequisitos luego de la transitividad es {grafo_prerrequisitos}")
    arcos_nuevos = nuevos_arcos(grafo_prerrequisitos)  # Funciona bien.
    # dibujar_grafo("grafo_prerrequisitos_ing", grafo_prerrequisitos)
    
    # -------- GRAFO MÓDULOS -------
    cursos_ing_ies = cursos_con_pruebas(PATH_CURSOS_IES)
    
    if INCLUIR_MAT:
        cursos_mat = cursos_mat_con_pruebas(PATH_LISTADO_NRC, siglas_fmat=IDENTIFICADORES_FMAT)
        for j in cursos_mat:
            cursos_ing_ies.append(j)
    
    if INCLUIR_FIS_Y_QIM:
        cursos_fisqim = cursos_fisqim_con_pruebas(PATH_LISTADO_NRC, siglas_fisqim=IDENTIFICADORES_FIS_Y_QIM)
        for j in cursos_fisqim:
            cursos_ing_ies.append(j)
    
    cursos_con_horario = cursos_mod_dipre(
        PATH_LISTADO_NRC, cursos_ing_ies, incluir_fmat=INCLUIR_MAT, incluir_fis_y_qim=INCLUIR_FIS_Y_QIM,
        identificadores_fmat=IDENTIFICADORES_FMAT, identificadores_fis_y_qim= IDENTIFICADORES_FIS_Y_QIM).to_pandas()
    
    macrosecciones = cursos_con_macroseccion(cursos_con_horario)


    # Tener cuidado, porque se repite ICT3113-2, revisar si tiene clases en días distintos
    cursos_pertenecientes_a_macroseccion = set(itertools.
                                               chain(*list(macrosecciones.values())))

    grafo_modulos = grafo_mismo_modulo(PATH_LISTADO_NRC, cursos_ing_ies)
    # dibujar_grafo("grafo_antes_macroseccion", grafo_modulos)
    
    grafo_modulos = reemplazar_siglas_con_macrosecciones(grafo_modulos,
                                                         macrosecciones,
                                                         cursos_pertenecientes_a_macroseccion)
    cursos_en_macroseccion = dict()
    for macroseccion, sigla_secc in macrosecciones.items():
        for i in sigla_secc:
            cursos_en_macroseccion[i] = macroseccion

    logging.info(
        f"Grafo antes de juntarlo con prerrequisitos es {grafo_modulos}")
    
    # dibujar_grafo("grafo_luego_macroseccion", grafo_modulos)

    juntar_grafos_prerrequisitos_y_modulos(grafo_modulos,
                                           grafo_prerrequisitos,
                                           cursos_en_macroseccion,
                                           cursos_pertenecientes_a_macroseccion)
    logging.info(f"Grafo luego de juntarlo con prerrequisitos es {grafo_modulos}")
    # dibujar_grafo("grafo_cruce_prerreq_modulos", grafo_modulos)

    lista_nodos = list(grafo_modulos.nodes)
    mapeo_macrosseciones_label = dict()
    for nodo in lista_nodos:
        if "Macrosección" in nodo:
            nombre = nodo.replace("Macrosección", "Macroseccion")
            mapeo_macrosseciones_label[nodo] = nombre

    grafo_modulos = nx.relabel_nodes(grafo_modulos, mapeo_macrosseciones_label)
    
    # Guardado de datos
    guardado_conexiones(grafo_modulos)
    guardado_cursos(grafo_modulos)
    guardar_vacantes(grafo_modulos, macrosecciones,
                     cursos_ing_ies=cursos_ing_ies)
    title = "Grafo de ramos y respectivos módulos, con macrosecciones y prerrequisitos y cursos FMAT"
    # dibujar_grafo(title, grafo_modulos)
    logging.info(f"El grafo al final es {grafo_modulos}")

    nx.write_edgelist(grafo_modulos, os.path.join("instancia_datos", "grafo_main"), delimiter=";")
    nx.write_edgelist(grafo_modulos, "grafo_modulos_edgelist.txt", data=False, delimiter=";")

    
    if crear_parametros_ies:
        with open(PATH_IES, "w", encoding="utf-8") as file:
            conjunto_cursos = dict()
            
            for curso in lista_nodos:
                if "Macrosección" in curso:
                    curso = curso.replace("Macrosección", "Macroseccion")
                    
                if curso in CURSOS_3_IES :
                    conjunto_cursos[curso] = [1, 2, 3]
                else:
                    conjunto_cursos[curso] = [1, 2]
            
            file.write("CONJUNTO_INTERROGACIONES = " +
                       json.dumps(conjunto_cursos, ensure_ascii=False, indent=4))


    # Revisar bien que hace esto, igual se ve medio explicativ, pero revisarlo bien
    if crear_parametros_fechas:
        fechas_validas, *placeholder = generacion_calendario()
        with open(PATH_FECHAS, 'w', encoding="utf-8") as file:
            conjunto_fechas = dict()

            for curso in lista_nodos:
                curso_fmat_bool = any(i in curso
                                      for i in IDENTIFICADORES_FMAT)
                
                if curso_fmat_bool:
                    fechas_validas, *others = generacion_calendario(fmat=True)

                if "Macrosección" in curso:
                    curso = curso.replace("Macrosección", "Macroseccion")
                conjunto_fechas[curso] = fechas_validas

            file.write("CONJUNTO_FECHAS = " +
                       json.dumps(conjunto_fechas, ensure_ascii=False, indent=4))

    logging.info(f"El tiempo de ejecución fue de {time.time() - start_time} segundos")


if __name__ == "__main__":
    main(crear_parametros_ies=True, crear_parametros_fechas=True)
