import polars as pl
import pandas as pd
import networkx as nx
import os
import matplotlib.pyplot as plt
from copy import deepcopy
path_nodos = os.path.join('Datos', "Salas SJ 2023-07-13.xlsx")
path_edges = os.path.join('Datos', "datos grafo salas.xlsx")
path_excel_creado = os.path.join('Salas','datos', "salas.csv")

def crear_grafo(path_edges, path_nodos):
    """cargar excel y arreglar nodos"""
    edgelist_pl = pl.read_excel(path_edges)
    nodelist_pl = pl.read_excel(path_nodos)
    new_columns = {col: col.strip() for col in nodelist_pl.columns}
    # Se sacan las salas de educación, teología y citeduc, y las con 30 o menos de capacidad
    # solo se dejan las columnas de nombre y capacidad
    nodelist_pl = (nodelist_pl.rename(new_columns).drop('Location Formal Name')
                   .filter(pl.col("Campus Partition") != '11-Educacion_Ed')
                   .filter(pl.col("Campus Partition") != '12-Educacion_T')
                   .filter(pl.col("Campus Partition") != '53-Salas_Citeduc')
                   .filter(pl.col("Campus Partition") != '55-Salas_Teologia')
                   .drop('Campus Partition').filter(pl.col("Max Capacity") > 30))
    edgelist_pl = (edgelist_pl.filter(pl.col("distancia") != 0))
    lista = []
    for item in nodelist_pl.to_pandas()['Location Name'].values:
        lista.append(item[3:])
    nueva_col = pl.Series(lista)
    nodelist_pl.replace('Location Name', nueva_col)
    nodelist_pd = nodelist_pl.to_pandas()
    edgelist_pd = edgelist_pl.to_pandas()
    nodelist_pdcopy = deepcopy(nodelist_pd)
    """Crear Grafo"""
    g = nx.Graph()
    for i, elrow in edgelist_pd.iterrows():
        g.add_edge(elrow[0], elrow[1], weight=elrow[2])
    for i, nlrow in nodelist_pdcopy.iterrows():
        g.add_node(nlrow[0])

    nodelist_pd.drop(nodelist_pd[nodelist_pd['Available'] == 'F'].index, inplace = True)  #  Elimina salas no disponibles
    nodelist_pd.to_csv(path_excel_creado)

    # Las siguientes 4 lineas muestran el grafo de salas en pantalla

    # edge_colors = [e[2]['w']['color'] for e in list(g.edges(data=True))]
    # plt.figure(figsize=(8, 6))
    # nx.draw(g, edge_color=edge_colors, node_size=10, node_color='black', with_labels=True, font_size=5)
    # plt.show()
    return g


crear_grafo(path_edges, path_nodos)
