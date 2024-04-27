import pandas as pd
import os
import networkx as nx
import unicodedata
import gurobipy as gp

from gurobipy import Model, GRB, quicksum
from datos.generacion_calendario import generacion_calendario
from itertools import combinations

from modelo_optimizacion.cargar_datos.cargar_arcos import cargar_arcos
from modelo_optimizacion.cargar_datos.cargar_cursos import cargar_cursos
from modelo_optimizacion.cargar_datos.cargar_vacantes import cargar_vacantes

fechas_validas, mapeo_fechas, *placeholder = generacion_calendario()

fechas_calendario = list(fechas_validas.keys())
# A partir del 31 de Marzo empezamos a considerar fechas válidas
fechas_calendario = fechas_calendario[25:]


arcos = cargar_arcos()
cursos = cargar_cursos()
# Con 200 se la puede rápido
# Con 300 cursos y 2800 vacantes e la puede rápido
# print(len(cursos))
#cursos = cursos[:300]
vacantes = cargar_vacantes()

G = nx.read_edgelist("grafo_modulos_edgelist.txt", comments=None, delimiter = ";")
G = nx.induced_subgraph(G, cursos)
print(len(G.nodes()), len(G.edges()))

cliques = {}

for clique in nx.find_cliques(G):
    cliques[len(cliques)] = clique

print(len(cliques))

# Empieza el modelo
model = Model("Calendarizacion Interrogaciones")
#model.setParam("MIPFocus", 1)
# Se podría maximizar un atractivo de pruebas. En el sentido de asignar ciertos días en que uno preferiría agendar pruebas
# o cierto intervalo de días

V = 3500
interrogaciones = [1, 2]
delta_min = 45
delta_max = 63

x = model.addVars(cursos,
                  fechas_calendario,
                  interrogaciones,
                  vtype=GRB.BINARY,
                  name="x")

y = model.addVars(cliques,
                  fechas_calendario,
                  vtype=GRB.BINARY,
                  name="y")

model.update()

# Cada prueba se asigna una vez
model.addConstrs(quicksum(x[curso, dia, interrogacion] for dia in fechas_calendario)
                 == 1 for curso in cursos for interrogacion in interrogaciones)

# No superar el tope máximo por día
# Comentar al profe que esto lo cambie un poco
model.addConstrs(quicksum(x[curso, dia, interrogacion] * vacantes[curso]
                 for curso in cursos for interrogacion in interrogaciones) <= V for dia in fechas_calendario)

# Restricción del intervalo posible de días para la I2 dada la I1
for curso in cursos:
    for dia in fechas_calendario:
        inferior = min(fechas_calendario[-1], dia + delta_min)
        superior = min(fechas_calendario[-1], dia + delta_max)
        # if inferior < superior:
#
        # En este rango, puede ser que se generen fechas que no estaban inicialmente consideradas
        rango_dias_validos = [x for x in range(
            inferior, superior + 1) if x in fechas_calendario]
        # print(rango_dias_validos, fechas_calendario)
        model.addConstr(x[curso, dia, 1] <= quicksum(
            x[curso, t, 2] for t in rango_dias_validos))


#combinaciones_cursos = list(combinations(cursos, 2))

#for curso_1, curso_2 in combinaciones_cursos:
#    valor_1 = arcos.get(f"{curso_1}, {curso_2}", 0)
#    valor_2 = arcos.get(f"{curso_2}, {curso_1}", 0)

#    if valor_1 == 0 and valor_2 == 0:
#        for dia in fechas_calendario:
            # model.addConstr(x[curso_1, dia, 1] + x[curso_2, dia, 1] <= 1)
            # model.addConstr(x[curso_1, dia, 1] + x[curso_2, dia, 2] <= 1)
#            model.addConstr(x[curso_1, dia, 1] + x[curso_1, dia, 2] +
#                            x[curso_2, dia, 1] + x[curso_2, dia, 2] <= 1)

model.addConstrs(x[curso, dia, 1] + x[curso, dia, 2] <= quicksum(y[clique, dia] for clique in cliques if curso in cliques[clique]) for curso in cursos for dia in fechas_calendario)

model.addConstrs(quicksum(y[clique, dia] for clique in cliques) <= 1 for dia in fechas_calendario)

model.optimize()


if model.status == gp.GRB.INFEASIBLE:
    print(f"[ERROR]: El modelo es infactible")
    model.computeIIS()
    restricciones_infactibles = model.getConstrs()
    # model.write("model.ilp")
    # Imprimir el conjunto de restricciones infactibles
    print("El modelo es infactible. Las siguientes restricciones deben ser removidas:")
    for restriccion in restricciones_infactibles:
        print(restriccion.constrName)

# model.write("modelo_no_factible.lp")


for variable in model.getVars():
    if variable.X != 0:
        try:
            print(f"{variable.varName} = {variable.X}")
        except UnicodeDecodeError:
            print(f"Error al interpretar los carácteres de una variable")


with open("resultados_rest_vacantes.txt", 'w', encoding="utf-8") as file:
    for variable in model.getVars():
        if variable.X != 0:
            file.write(f"{variable.varName} = {variable.X}\n")


model.write("modelo.mps")
