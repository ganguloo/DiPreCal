import os
import pandas as pd
from parametros.cursos_ies import CONJUNTO_INTERROGACIONES
from parametros.parametros import GRUPOS

def sort_secciones(a) :
    if 'Macroseccion' in a :
        return 0
    else: 
        return int(a[8:])
def sort_cursos(a) :
    return a[:7]

    # def completar_grupos(path_cursos , grupos) : #Leyendo algun excel de datos
    #     cursos = pd.read_excel(path_cursos)
    #     cursos = cursos.values.tolist()
    #     grupos_nuevo = []

    #     for n,grupo in enumerate(grupos) :
    #         #print(n)
    #         grupos_nuevo.append([])
    #         for curso in grupo:
    #             # if curso == "EYP1113" :
    #             #     grupos_nuevo[n].append("EYP_MOD_MS1 - Macroseccion 1")
    #             # elif curso == "MAT1610" :
    #             #     grupos_nuevo[n].append("XN_MOD_MS1 - Macroseccion 1")
    #             # elif curso == "MAT1620" :
    #             #     grupos_nuevo[n].append("YF_MOD_MS1 - Macroseccion 1")
    #             # elif curso == "MAT1630" :
    #             #     grupos_nuevo[n].append("GCH_MOD_MS1 - Macroseccion 1")
    #             # elif curso == "MAT1640" :
    #             #     grupos_nuevo[n].append("ED_MOD_MS1 - Macroseccion 1")
    #             # elif curso == "MAT1203" :
    #             #     grupos_nuevo[n].append("WV_MOD_MS1 - Macroseccion 1")

    #             # else:
    #             seccion_anterior = 0
    #             for curso_x in cursos :
    #                 ramo = curso_x[5] + str(curso_x[6])

    #                 if curso == ramo :
    #                     #print(f'coincide el curso {curso} del grupo {n} con el ramo {ramo}, seccion {curso_x[7]}')
    #                     if seccion_anterior != curso_x[7] :
    #                         grupos_nuevo[n].append(ramo + '-' + str(curso_x[7]))
    #                         seccion_anterior = curso_x[7]

    #     for i in range(len(grupos_nuevo)):
    #         grupos_nuevo[i].sort(key=sort_secciones)
    #         grupos_nuevo[i].sort(key=sort_cursos)
    #     return grupos_nuevo

    # #print(completar_grupos(PATH_CURSOS_IES,GRUPOS))




def completar_grupos_cursos_ies(cursos = CONJUNTO_INTERROGACIONES, grupos = GRUPOS) : #Usando lista cursos_ies
    grupos_nuevo = []

    for n,grupo in enumerate(grupos) :
        #print(n)
        grupos_nuevo.append([])
        for curso in grupo:
            # if curso == "EYP1113" :
            #     grupos_nuevo[n].append("EYP_MOD_MS1 - Macroseccion 1")
            # elif curso == "MAT1610" :
            #     grupos_nuevo[n].append("XN_MOD_MS1 - Macroseccion 1")
            # elif curso == "MAT1620" :
            #     grupos_nuevo[n].append("YF_MOD_MS1 - Macroseccion 1")
            # elif curso == "MAT1630" :
            #     grupos_nuevo[n].append("GCH_MOD_MS1 - Macroseccion 1")
            # elif curso == "MAT1640" :
            #     grupos_nuevo[n].append("ED_MOD_MS1 - Macroseccion 1")
            # elif curso == "MAT1203" :
            #     grupos_nuevo[n].append("WV_MOD_MS1 - Macroseccion 1")

            # else:
            for curso_l in cursos :
                if curso in curso_l :
                    #print(f'coincide el curso {curso} del grupo {n} con el curso-seccion {curso_l}')
                    grupos_nuevo[n].append(curso_l)

    n = 0
    while n < len(grupos_nuevo):
        if grupos_nuevo[n] == [] :
            grupos_nuevo.pop(n)
        else :
            grupos_nuevo[n].sort(key=sort_secciones)
            grupos_nuevo[n].sort(key=sort_cursos)
            n += 1
    destino = os.path.join("parametros","grupos_modelo.py")
    archivo = open(destino,"w")
    grupos_txt = '['
    for i in grupos_nuevo[:-1]:
        grupos_txt += '\n' + str(i) + ','
    grupos_txt += '\n' + str(grupos_nuevo[-1])
    grupos_txt += ']'
    archivo.write(f'GRUPOS_M = {grupos_txt}')
    #print('Se creo correctamente el archivo "grupos_modelo.py"')
    return grupos_nuevo

#No se para que esta el grupos_ies, es mejor grupos_cursos