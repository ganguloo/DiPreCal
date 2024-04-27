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

from parametros.parametros import (NUM_EXPERIMENTO, DELTA_DIAS, GRUPOS, DELTAMIN,
                                   DELTAMAX,VACANTES,PRUEBAS_PREASIGNADAS, DIA_FECHA_RETIRO_CURSOS,SEMANA_LICENCIATURA, DIA_I2)

#No se debe importar entremedio pero es la solucion rapida
from generacion_parametros.grupos import completar_grupos_cursos_ies

completar_grupos_cursos_ies(CONJUNTO_INTERROGACIONES,GRUPOS)

from parametros.grupos_modelo import GRUPOS_M


fechas_validas_cliques, mapeo_fechas, *placeholder = generacion_calendario()

fechas_calendario_cliques = list(fechas_validas_cliques.keys())

dia_retiro = DIA_FECHA_RETIRO_CURSOS #8 mayo?
dia_i2 = DIA_I2

diasem = (SEMANA_LICENCIATURA-1)*7

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

V = VACANTES

print('Capacidad', V)
print(f"Se está ejecutando el experimento {NUM_EXPERIMENTO}")
print("Modelo nuevo")
delta_min = DELTAMIN
delta_max = DELTAMAX

dias_calendario = 117

J = range(0,4)

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
            # x[curso, 'A3_MS1 - Macrosección fecha, prueba] = model.addVar(mapeo_cursos[curso], fecha, prueba, vtype=GRB.BINARY)
            name = f"x[{curso},{fecha},{prueba}]"
            x[curso, fecha, prueba] = model.addVar(vtype=GRB.BINARY, name=name)




y = model.addVars(cliques,
                  fechas_calendario_cliques,
                  vtype=GRB.BINARY,
                  name="y")

a = model.addVars(J, vtype=GRB.BINARY, name="a")

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
        # Recorremos hasta el penúltimo
        for interrogacion in CONJUNTO_INTERROGACIONES[curso][:-1]:
            # inferior deberia ser siempre menor a superior, de ahí revisar
            inferior = dia + delta_min
            superior = min(fechas_calendario[curso][-1], dia + delta_max)
            # if inferior < superior:
#
            # En este rango, puede ser que se generen fechas que no estaban inicialmente consideradas
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

#Separa los cursos de grupos en delta días
for grupo in GRUPOS_M :
    for d in range(dias_calendario):
        intervalo = []
        for i in range(DELTA_DIAS + 1) :
            intervalo.append(d + i)
        model.addConstr(quicksum(x[curso,dia,interrogacion] for curso in grupo for interrogacion in CONJUNTO_INTERROGACIONES[curso] for dia in intervalo if dia in fechas_calendario[curso]) <= 1)


model.addConstrs(x[curso,dia,interrogacion] == 1 for (curso,dia,interrogacion) in PRUEBAS_PREASIGNADAS)

#No permite cursos que sólo asignen una de sus pruebas
model.addConstrs(quicksum(z[curso,interrogacion] for interrogacion in CONJUNTO_INTERROGACIONES[curso]) == len(CONJUNTO_INTERROGACIONES[curso])*z[curso, 1] for curso in cursos)

#Restriccion 2 dias consecutivos sin pruebas
model.addConstr(quicksum(a[j] for j in J) == 1)

model.addConstrs(quicksum(quicksum(x[curso,dia,interrogacion] for dia in range(diasem+j,diasem+j+2) if dia in fechas_calendario[curso]) 
                          for curso in cursos for interrogacion in CONJUNTO_INTERROGACIONES[curso]) <= len(cursos)*2*3*(1-a[j]) for j in J) 
#*2*3 para compensar por la suma sobre 2 dias, 3 interrogaciones max


model.write("modelo.lp")

#intento hacer multiobjetivo
#Minimiza por defecto, por lo que no se indica GRB.MINIMIZE
#minimiza vacantes que quedan sin prueba
model.setObjectiveN(quicksum(z[curso, interrogacion] * vacantes[curso] for curso in cursos for interrogacion in CONJUNTO_INTERROGACIONES[curso]), 
                    index = 0, priority = 10, name = "Obj1" )
#minimiza vacantes asignadas antes/despues de las fechas deseadas
model.setObjectiveN(quicksum(quicksum(x[curso,dia,1]*vacantes[curso]*(dia-dia_retiro) for dia in fechas_calendario[curso] if dia >= dia_retiro) +
                    quicksum(x[curso,dia,2]*vacantes[curso]*(dia_i2-dia) for dia in fechas_calendario[curso] if dia <= dia_i2) for curso in cursos),
                   index = 1, priority = 8, name = "Obj2")

# model.setObjectiveN(quicksum(x[curso,dia,1]*vacantes[curso]*dia for curso in cursos for dia in fechas_calendario[curso] if dia >= dia_retiro),
#                     index = 1, priority = 8, name = "Obj2")

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
