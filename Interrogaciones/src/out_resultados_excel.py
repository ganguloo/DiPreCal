from datos.generacion_calendario import generacion_calendario
from datos.interrogaciones import organizacion_datos_interrogaciones
from modelo_optimizacion.cargar_datos.cargar_vacantes import cargar_vacantes
from filtracion_archivos.modulos_mod_dipre import cursos_mod_dipre
from filtracion_archivos.cursos_con_ies import cursos_con_pruebas
from filtracion_archivos.modulos import cursos_con_macroseccion
from parametros.parametros import (PATH_CURSOS_IES, PATH_LISTADO_NRC,PATH_LISTADO_NRC_ORIGINAL,PATH_CURSOS_IES_ORIGINAL, PATH_MATERIAS,
                                   IDENTIFICADORES_FMAT, CURSOS_3_IES, CURSOS_COORDINADOS, SEC_COORDINADAS,
                                   INCLUIR_FIS_Y_QIM, INCLUIR_MAT, IDENTIFICADORES_FIS_Y_QIM)



fechas_validas, mapeo_fechas, fechas = generacion_calendario()
fechas_actualizado = organizacion_datos_interrogaciones(mapeo_fechas, "resultados_rest_vacantes.txt")
vacantes = cargar_vacantes()
cursos_ing_ies = cursos_con_pruebas(PATH_CURSOS_IES)
# cursos_con_horario = cursos_mod_dipre(PATH_LISTADO_NRC, cursos_ing_ies).to_pandas()

cursos_con_horario = cursos_mod_dipre(
    PATH_LISTADO_NRC, cursos_ing_ies, incluir_fmat=INCLUIR_MAT, incluir_fis_y_qim=INCLUIR_FIS_Y_QIM,
    identificadores_fmat=IDENTIFICADORES_FMAT, identificadores_fis_y_qim= IDENTIFICADORES_FIS_Y_QIM).to_pandas()



macrosecciones = cursos_con_macroseccion(cursos_con_horario)

vacantes_dataframe = cursos_mod_dipre(PATH_LISTADO_NRC, cursos_ing_ies, incluir_fmat = INCLUIR_MAT, 
                                        incluir_fis_y_qim = INCLUIR_FIS_Y_QIM, 
                                        identificadores_fmat = IDENTIFICADORES_FMAT, 
                                        identificadores_fis_y_qim = IDENTIFICADORES_FIS_Y_QIM)
vacantes_dataframe = vacantes_dataframe.select(["Sigla_Seccion", "Vacantes Ofrecidas"]).to_pandas()
vacantes_sigla_seccion = dict(vacantes_dataframe.values)

# print(fechas_actualizado)

output = ""
with open("output.csv", "w", encoding="utf-8") as file:
    output += "Curso;Seccion;N Interrogacion;Fecha;Vacantes\n"
    for fecha in fechas_actualizado:
        if "Macroseccion" in fecha[0]:
            identificador = fecha[0].replace("Macroseccion", "Macrosección")
            cursos_macroseccion = []
            for curso in macrosecciones[identificador]:
                cursos_macroseccion.append(curso[0:7])
            for curso in set(cursos_macroseccion):
                secciones = []
                for seccion in macrosecciones[identificador]:
                    if curso in seccion:
                        secciones.append(seccion)
                secciones = set(secciones)
                numeros_secciones = []
                total_vacantes = 0
                for seccion in secciones:
                    numeros_secciones.append(seccion[8:])
                    total_vacantes += vacantes_sigla_seccion[seccion]
                numeros_secciones = ",".join(numeros_secciones)          
                output += f"{curso[0:7]};{numeros_secciones};{fecha[2]};{fecha[1]};{total_vacantes}\n"
        else:
            output += f"{fecha[0][0:7]};{fecha[0][8:]};{fecha[2]};{fecha[1]};{vacantes[fecha[0]]}\n"
    file.write(output)


# for macroseccion in macrosecciones:
#     print(macroseccion)
#     for curso in macrosecciones[macroseccion]:
#         print(curso, vacantes_sigla_seccion[curso])
#     print()
# print(macrosecciones)

# print(fechas_actualizado)

