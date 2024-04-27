import os
import gurobipy as gp
import sys
import networkx as nx


from gurobipy import Model, GRB, quicksum
from datos.generacion_calendario import generacion_calendario
from itertools import combinations

from modelo_optimizacion.cargar_datos.cargar_arcos import cargar_arcos
from modelo_optimizacion.cargar_datos.cargar_cursos import cargar_cursos
from modelo_optimizacion.cargar_datos.cargar_vacantes import cargar_vacantes
from modelo_optimizacion.cargar_datos.cargar_colores import datos_colores_grafo

from parametros.cursos_ies import CONJUNTO_INTERROGACIONES
from parametros.cursos_fechas import CONJUNTO_FECHAS

from parametros.parametros import NUM_EXPERIMENTO


fechas_validas_cliques, mapeo_fechas, *placeholder = generacion_calendario()

fechas_calendario_cliques = list(fechas_validas_cliques.keys())



arcos = cargar_arcos()
cursos = cargar_cursos()
datos_colores, arcos_restantes, args = datos_colores_grafo(
    os.path.join("instancia_datos", "grafo_main"))

vacantes = cargar_vacantes()

G = nx.read_edgelist("grafo_modulos_edgelist.txt",
                     comments=None, delimiter=";")
G = nx.induced_subgraph(G, cursos)
print('Nodos', len(G.nodes()), 'Arcos', len(G.edges()))

cliques = {}

for clique in nx.find_cliques(G):
    cliques[len(cliques)] = clique

print('Cliques', len(cliques))

# Empieza el modelo
model = Model("Calendarizacion Interrogaciones")
model.setParam("MIPFocus", 1)
model.setParam("LogFile", os.path.join("resultados", "ModeloPruebas"))
# Se podría maximizar un atractivo de pruebas. En el sentido de asignar ciertos días en que uno preferiría agendar pruebas
# o cierto intervalo de días

V = 2000

print('Capacidad', V)
print(f"Se está ejecutando el experimento {NUM_EXPERIMENTO}")
print("Modelo Original")
delta_min = 28
delta_max = 63

x = dict()
z = dict()
mapeo_cursos = dict()
contador = 0
for curso in CONJUNTO_INTERROGACIONES.keys():
    mapeo_cursos[curso] = contador
    contador += 1

fechas_calendario = {curso: [int(i) for i in CONJUNTO_FECHAS[curso].keys()] for curso in cursos}


for curso, interrogaciones in CONJUNTO_INTERROGACIONES.items():
    for prueba in interrogaciones:
        name_binary = f"z[{curso},{prueba}]"
        z[curso, prueba] = model.addVar(vtype=GRB.BINARY, name=name_binary)
        
        for fecha in fechas_calendario[curso]:
            # x[curso, fecha, prueba] = model.addVar(mapeo_cursos[curso], fecha, prueba, vtype=GRB.BINARY)
            name = f"x[{curso},{fecha},{prueba}]"
            x[curso, fecha, prueba] = model.addVar(vtype=GRB.BINARY, name=name)




y = model.addVars(cliques,
                  fechas_calendario_cliques,
                  vtype=GRB.BINARY,
                  name="y")

model.update()

# Cada prueba se asigna una vez
model.addConstrs(quicksum(x[curso, dia, interrogacion] for dia in fechas_calendario[curso])
                 + z[curso, interrogacion] == 1 for curso in cursos for interrogacion in CONJUNTO_INTERROGACIONES[curso])

# No superar el tope máximo por día
# Atento al lado derecho y la indexación respecto a las fechas
model.addConstrs(quicksum(x[curso, dia, interrogacion] * vacantes[curso]
                          for curso in cursos for interrogacion in CONJUNTO_INTERROGACIONES[curso] if mapeo_fechas[dia] in CONJUNTO_FECHAS[curso].values()) <= V for dia in fechas_calendario_cliques)

# Restricción del intervalo posible de días para la I2 dada la I1
for curso in cursos:
    for dia in fechas_calendario[curso]:
        # Recorremos hasta el antepenúltimo
        #DICE ANTEPENULTIMO PERO NO SERIA PENULTIMO?
        for interrogacion in CONJUNTO_INTERROGACIONES[curso][:-1]:
            # inferior deberia ser siempre menor a superior, de ahí revisar
            inferior = dia + delta_min
            superior = min(fechas_calendario[curso][-1], dia + delta_max)
            # if inferior < superior:
#
            # En este rango, puede ser que se generen fechas que no estaban inicialmente consideradas
            #Y ESTO ES BUENO O MALO?
            rango_dias_validos = [x for x in range(
                inferior, superior + 1) if x in fechas_calendario[curso]]
            # if inferior >= fechas_calendario[:-1]:
            # print(rango_dias_validos, fechas_calendario)
            # for t in rango_dias_validos:
            # model.addConstr((x[curso, dia, 1] <= quicksum(x[curso, t, 2])))
            model.addConstr((x[curso, dia, interrogacion] <= quicksum(
                x[curso, t, interrogacion + 1] for t in rango_dias_validos) + z[curso, interrogacion + 1]))


model.addConstrs(quicksum(x[curso, dia, prueba] for prueba in CONJUNTO_INTERROGACIONES[curso]) <= quicksum(
    y[clique, dia] for clique in cliques if curso in cliques[clique]) for curso in cursos for dia in fechas_calendario[curso])

model.addConstrs(quicksum(y[clique, dia]
                 for clique in cliques) <= 1 for dia in fechas_calendario_cliques)

model.write("modelo.lp")

model.setObjective(quicksum(z[curso, interrogacion] * vacantes[curso]
                   for curso in cursos for interrogacion in CONJUNTO_INTERROGACIONES[curso]), GRB.MINIMIZE)

model.optimize()

# Decirle a Gurobi que use un solo Thread
if model.status == gp.GRB.INFEASIBLE:
    print(f"[ERROR]: El modelo es infactible")
    model.computeIIS()
    restricciones_infactibles = model.getConstrs()
    model.write("Infactible.ilp")


# model.write("model.sol")

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


# model.write("modelo.mps")
