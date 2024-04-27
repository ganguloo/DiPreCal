import networkx as nx
import logging

def grafo_prerrequisito(cursos: dict):
    grafo_prerrequisitos = nx.DiGraph()

    for curso, prerrequisitos in cursos.items():
        if len(prerrequisitos) != 0:
            for prerrequisito in prerrequisitos:
                grafo_prerrequisitos.add_edge(curso, prerrequisito, relacion="prerrequisito")

        else:
            grafo_prerrequisitos.add_node(curso)

    grafo_prerrequisitos = grafo_prerrequisitos.reverse()
    return grafo_prerrequisitos


def anadir_arcos_transitividad(grafo):
    lista_nodos = list(grafo.nodes)
    lista_nuevas_uniones = list()
    for nodo_inicial in lista_nodos:
        for nodo_final in lista_nodos:
            if nodo_inicial != nodo_final:
                for path in nx.all_simple_paths(grafo, source=nodo_inicial, target=nodo_final):
                    for indice, ramo in enumerate(path):
                        # Se añade el nombre, siempre y cuando aparezca después en el camino simple que el nodo que se está revisando
                        # Ejemplo: A -> B -> C -> D
                        # Solo se puede añadir A ->C, A -> D. Pero no se podría C -> A.
                        nuevas_uniones = [x for indice_loop, x in enumerate(
                            path) if indice_loop > indice]
                        nombre = "anadir_arcos_transitividad"
                        if len(nuevas_uniones) != 0:
                            logging.debug(f"[Función: {nombre}] Se han añadido por transitividad a {ramo} los ramos {nuevas_uniones}")
                            for nodo_vecino in nuevas_uniones:
                                lista_nuevas_uniones.append([ramo, nodo_vecino])

    for arco in lista_nuevas_uniones:
        grafo.add_edge(*arco)
