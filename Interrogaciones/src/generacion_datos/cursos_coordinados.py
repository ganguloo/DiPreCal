import pandas as pd
from parametros.parametros import PATH_CURSOS_IES, PATH_LISTADO_NRC, CURSOS_COORDINADOS, SEC_COORDINADAS

#5 MATERIA y 6 NR, 12 Lista Cruzada, 13 Macrosec

def coordinados_a_macrosecciones(path_cursos_ies,path_listado_nrc,cursos_coordinados,sec_coordinadas) :
#Reescribe el archivo original de ies y nrcs, generando una macroseccion para los cursos y secciones coordinadas

    iterador = 0
    while iterador < 2: #se itera sobre i para realizar el mismo algoritmo sobre dos archivos distintos
        if iterador == 0:
            excel = pd.read_excel(path_listado_nrc)
        else :
            excel = pd.read_excel(path_cursos_ies, sheet_name="Deben tener Ies")

        header = excel.columns
        excel = excel.values.tolist()


        for n,curso in enumerate(excel) :
            for coordinado in cursos_coordinados:
                if (str(curso[5]) + str(curso[6]) == coordinado) :
                    # if excel[n][12] == ' ' or pd.isna(excel[n][12]) :
                    if excel[n][12] != coordinado :
                        excel[n][12] = coordinado
                        excel[n][13] = "Coordinado - Macrosección"

            for sec_coord in sec_coordinadas :
                tag = ""
                for i in sec_coord :
                        tag += i + "_"
                tag = tag[:-1] 
                secciones = sec_coord[1:]
                # if (str(curso[5])+str(curso[6]) == sec_coord[0]) and str(curso[7]) in secciones and (excel[n][12] == ' ' or pd.isna(excel[n][12])):
                if (str(curso[5])+str(curso[6]) == sec_coord[0]) and str(curso[7]) in secciones and (excel[n][12] != tag):
                        excel[n][12] = tag
                        excel[n][13] = "Sec_Coordinadas - Macrosección"

        df = pd.DataFrame(excel, columns = header)
        if iterador == 0 :
            df.to_excel("./excel_horarios/Prueba_nrc.xlsx",index = False) 
        else :
            df.to_excel("./excel_horarios/Prueba_ies.xlsx",index = False, sheet_name= "Deben tener Ies") 

        iterador += 1

    return True

#coordinados_a_macrosecciones(PATH_CURSOS_IES,PATH_LISTADO_NRC,CURSOS_COORDINADOS,SEC_COORDINADAS)


