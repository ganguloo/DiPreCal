
def nuevos_arcos(grafo_prerrequisitos) -> dict:
    """Se retorna un diccionario que contiene los arcos nuevos que son obtenidos del grafo
    de prerrequisitos y que se implementarán en el grafo de los módulos. Cada key es el
    nodo y el value asociado es una lista de sus vecinos"""
    nuevos_arcos = dict()

    for nodo in grafo_prerrequisitos.nodes:
        vecinos = [x for x in grafo_prerrequisitos.neighbors(nodo)]
        if nodo not in nuevos_arcos.keys():
            if len(vecinos) != 0:
                nuevos_arcos[nodo] = vecinos

        else:
            nuevos_arcos[nodo].extend(vecinos)

    return nuevos_arcos

# Hay que revisar esta función más detenidamente
# Podría ser propenso a error
def juntar_grafos_prerrequisitos_y_modulos(grafo_modulos,
                                           grafo_prerrequisitos,
                                           curso_en_macroseccion,
                                           cursos_pertenecientes_macroseccion
                                           ):
    lista_nodos_modulos = list(grafo_modulos.nodes)
    lista_nodos_prerrequisitos = list(grafo_prerrequisitos.nodes)

    arcos_agregar = list()

    for i in lista_nodos_prerrequisitos:
        vecinos = [x for x in grafo_prerrequisitos.neighbors(i)]
        if len(vecinos) != 0:
            arcos_agregar.append([i, vecinos])

    for arco in arcos_agregar:
        ramos_con_misma_sigla = list(
            filter(lambda x: arco[0] in x, lista_nodos_modulos))
        # arco[0] es el ramo de interés y arco[1] son los prerrequisitos
        prerrequisitos_a_agregar = list()

        for prerreq in arco[1]:
            for sigla_seccion in lista_nodos_modulos:
                if prerreq in sigla_seccion:
                    prerrequisitos_a_agregar.append(sigla_seccion)

        if len(ramos_con_misma_sigla) != 0 and len(prerrequisitos_a_agregar) != 0:

            for sigla_seccion_ramo in ramos_con_misma_sigla:
                for prerrequisito_seccion in prerrequisitos_a_agregar:
                    if sigla_seccion_ramo in curso_en_macroseccion.keys():

                        if prerrequisito_seccion in curso_en_macroseccion.keys():
                            grafo_modulos.add_edge(curso_en_macroseccion[sigla_seccion_ramo],
                                                   curso_en_macroseccion[prerrequisito_seccion],
                                                   relacion="prerrequisito")
                        else:
                            grafo_modulos.add_edge(curso_en_macroseccion[sigla_seccion_ramo],
                                                   prerrequisito_seccion,
                                                   relacion="prerrequisito")

                    elif prerrequisito_seccion in curso_en_macroseccion.keys() and sigla_seccion_ramo not in curso_en_macroseccion.keys():
                        grafo_modulos.add_edge(sigla_seccion_ramo,
                                               curso_en_macroseccion[prerrequisito_seccion],
                                               relacion="prerrequisito")

                    else:
                        grafo_modulos.add_edge(sigla_seccion_ramo,
                                               prerrequisito_seccion,
                                               relacion="prerrequisito")

    for curso in cursos_pertenecientes_macroseccion:
        if curso in list(grafo_modulos.nodes):
            grafo_modulos.remove_node(curso)
