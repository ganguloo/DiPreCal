import networkx as nx


def datos_colores_grafo(path):
    grafo = nx.read_edgelist(path, delimiter=";")
    grafo_complemento = nx.complement(grafo)
    colores = nx.coloring.greedy_color(grafo)

    dict_colores = dict()
    for curso, color in colores.items():
        if color not in dict_colores.keys():
            dict_colores[color] = [curso]
        else:
            dict_colores[color] = dict_colores[color] + [curso]

    subgrafos_colores = dict()
    for color, cursos in dict_colores.items():
        subgrafo = nx.induced_subgraph(grafo_complemento, cursos)
        subgrafos_colores[color] = subgrafo

    arcos_colores = dict()

    for color, subgrafo in subgrafos_colores.items():
        if len(subgrafo.edges()) != 0:  # Algunos subgrafos no tienen arcos
            arcos_colores[color] = list(subgrafo.edges())

    lista_subgrafos = list(subgrafos_colores.values())
    subgrafo_union_colores = nx.algorithms.operators.all.union_all(
        lista_subgrafos)
    uniones_restantes = nx.difference(
        grafo_complemento, subgrafo_union_colores)
    arcos_faltantes_colores = list(uniones_restantes.edges())
    return arcos_colores, arcos_faltantes_colores, grafo
