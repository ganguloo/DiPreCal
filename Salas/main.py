from gurobipy import GRB, Model, quicksum
from carga_datos.cursos import curso
from carga_datos.salas import capacidad_salas
from grafo_salas import crear_grafo
import os
import networkx as nx
import polars as pl

path_nodos = os.path.join('Datos', "Salas SJ 2023-07-13.xlsx")
path_edges = os.path.join('Datos', "datos grafo salas.xlsx")
path_prioridades = os.path.join('Salas', 'datos', "salas.csv")
path_output = os.path.join('Interrogaciones', 'src', "output.csv")
G = crear_grafo(path_edges, path_nodos)
# Se asignan las prioridades a cada sala
prioridades = pl.read_csv(path_prioridades)
sala_prioridades = prioridades.to_pandas()["Location Name"].values
num_prioridades = prioridades.to_pandas()["Priority"].values
Prioridad = {}
for i in range(len(num_prioridades)):
    Prioridad[sala_prioridades[i]] = int(num_prioridades[i])
setprioridades = set(Prioridad.values())

with open(path_output) as archivo:
    info = archivo.readlines()[1:]
info = [x.strip("\n").split(";") for x in info]
setinfo = []
secciones = {}
for linea in info:
    if linea[3] not in setinfo:
        setinfo.append(linea[3])
    secciones[linea[0]] = linea[1]
escribir = []
escribir.append('Curso;Secciones;Fecha;Sala;N°;Cantidad Salas')

for dia in setinfo:
    unresolve = True
    p = 0
    while unresolve and p <= len(setprioridades)-1:

        m = Model()
        m.setParam("TimeLimit", 3600)

        # IMPORT PARAMS
        nombres = curso("nombres", dia)
        num = curso("num", dia)
        vacantes = curso("vacantes", dia)
        particion_maxima = curso("particion", dia)
        capacidad = capacidad_salas("capacidad")
        nombre_sala = capacidad_salas("name")
        for salaa in list(nombre_sala):
            if Prioridad[salaa] > p:
                nombre_sala.remove(salaa)

        # SETS

        C = range(len(nombres))  # curso
        S = range(len(nombre_sala))  # salas
        S_1 = range(len(nombre_sala))  # salas auxiliar


        # PARAMS
        Vacantes = {(c): vacantes[c] for c in C}
        Particion = {(c): particion_maxima[c] for c in C}
        Tamano = {(s): capacidad[s] for s in S}


        # Coloque aca sus variables
        X = m.addVars(C, S, vtype=GRB.BINARY, name="X_cs")  # Si el curso c utiliza la sala s
        Y = m.addVars(C, S, S_1, vtype=GRB.BINARY, name="Y_cs1s2")  # Si el cursos c utiliza las salas s1 y s2
        m.update()

        # Evitar que un cuirso sea dividido en muchas salas chicas
        m.addConstrs((quicksum(X[c, s] for s in S) <= Particion[c] for c in C), name="Granularidad")

        # Relación de variables
        m.addConstrs((X[c, s1] + X[c, s2] <= Y[c, s1, s2] + 1 for c in C for s1 in S for s2 in S_1 if (s1 != s2)), name="Relacion")

        m.addConstrs((quicksum(X[c, s] for c in C) <= 1  for s in S), name="Relacion_2")

        # Todos los alumnos deben ser asignados a alguna sala respetando las capacidades de una prueba (mitad)
        m.addConstrs((quicksum(X[c, s] * capacidad[s] for s in S) >= 2 * Vacantes[c] for c in C), name="Asignacion")

        m.update()
        # nx.shortest_path_length(G,source=s1,target=s2)
        objetivo = quicksum(quicksum(nx.shortest_path_length(G, source=nombre_sala[s1], target=nombre_sala[s2], weight='weight') * Y[c, s1, s2] for s1 in S for s2 in S if (s1 != s2)) for c in C)
        m.setObjective(objetivo, GRB.MINIMIZE)
        m.optimize()
        estado = m.status
        if estado != 2:
            p += 1
        elif estado == 2:
            unresolve = False
    valor_objetivo = m.ObjVal

    # Muestra los valores de las soluciones
    print("\n"+"-"*10+" Manejo Soluciones "+"-"*10)
    print("\n"+"-"*10+dia+"-"*10)

    for c in C:
        salas = []
        for s in S:
            if X[c, s].x == 1:
                salas.append(nombre_sala[s])
        cantidad = len(salas)
        salas = ','.join(salas)
        print(f"El curso {nombres[c]} | {secciones[nombres[c]]} utiliza las salas {salas} para I{num[c]}")
        new = f'{nombres[c]};{secciones[nombres[c]]};{dia};{salas};I{num[c]};{cantidad}'
        escribir.append(new)
with open(os.path.join('Salas', 'datos', "Resultados.csv"), 'w') as arc:
    arc.write('\n'.join(escribir))
