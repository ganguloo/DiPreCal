import os
from datetime import datetime
from datos.conversion_excel_parametros import fechas_prohibidas, excel_cursos_coordinados, mapeo_fechas, mapeo, fijar_interrogaciones



PATH_LISTADO_NRC = os.path.join("excel_horarios",
                                 "Prueba_nrc.xlsx")

# Parece que esta ruta tiene todos los ramos de la U, para sacar también de ahí los ramos matemáticos
# y todo eso
# PATH_LISTADO_NRC_ORIGINAL = os.path.join("excel_horarios", "Listado_NRC_2023_Enero.xlsx")
# PATH_LISTADO_NRC_ORIGINAL = os.path.join("excel_horarios", "Cursos planificados 2024-2 detalle.xlsx")
PATH_LISTADO_NRC_ORIGINAL = os.path.join("excel_horarios", "004 - Listado de NRC Programados.xlsx")



PATH_VACANTES = os.path.join("instancia_datos", "vacantes.xlsx")
PATH_CONEXIONES = os.path.join("instancia_datos", "conexiones.xlsx")
PATH_CURSOS_IES = os.path.join("excel_horarios", "Prueba_ies.xlsx")


# No olvidar desecomentar esto en caso de que no funcione: 22 Junio 2024
# Aquí son los ramos de ingeniería que necesitan prueba
# PATH_CURSOS_IES_ORIGINAL = os.path.join("excel_horarios", "004 - Listado_NRC_Programados.xlsx")

# PATH_CURSOS_IES_ORIGINAL = os.path.join("excel_horarios", "Cursos planificados 2024-2 detalle.xlsx")
PATH_CURSOS_IES_ORIGINAL = os.path.join("excel_horarios", "Declaración de evaluaciones por curso ING2024-2.xlsx")


PATH_IES = os.path.join("parametros", "cursos_ies.py")
PATH_FECHAS = os.path.join("parametros", "cursos_fechas.py")

# PATH_CURSOS_IES = os.path.join(
#     "excel_horarios", "004-filtrado.xlsx")

PATH_MATERIAS = os.path.join("excel_horarios", "Listado_materias.xlsx")
PATH_LISTADO_CURSOS = os.path.join("instancia_datos", "listado_cursos.xlsx")

NUM_EXPERIMENTO = 2

# Ruta excel parametros
# PATH_PARAMETROS = os.path.join("excel_horarios", "parametros.xlsx")
PATH_PARAMETROS = os.path.join("excel_horarios", "parametros_2024.xlsx")

# Obtenemos las fechas prohibidas del excel
FECHAS_PROHIBIDAS = fechas_prohibidas(PATH_PARAMETROS, "Fechas")

# Obtenemos los cursos coordinados del excel
CURSOS_COORDINADOS = excel_cursos_coordinados(PATH_PARAMETROS, "Cursos Coordinados")

# Obtenemos las pruebas preasignadas (solo para cursos coordinados)
#Formato: si cursos todos coordinados: (curso (str), fecha (int), nr de prueba(int)) ¡La fecha debe ser en línea de tiempo real!
PRUEBAS_PREASIGNADAS = fijar_interrogaciones(PATH_PARAMETROS, "Interrogaciones Fijas")

DIA_FECHA_RETIRO_CURSOS = mapeo_fechas(PATH_PARAMETROS, "Fechas", "D1")
DIA_I2 = mapeo_fechas(PATH_PARAMETROS, "Fechas", "F1")


GRUPOS = [["MAT1620","FIS1514","IIC1103"],["MAT1620","ICE1514","IIC1103"],["MAT1630","FIS1523","MAT1640"],["MAT1630","IIQ1003","MAT1640"],
          ["MAT1630","ICM1003","MAT1640"],["EYP1113","FIS1533","ICS1513"],["EYP1113","IEE1533","ICS1513"],["FIS1514","FIS1523","FIS1533"],
          ["FIS1514","IIQ1003","FIS1533"],["FIS1514","ICM1003","FIS1533"],["FIS1514","FIS1523","IEE1533"],["FIS1514","IIQ1003","IEE1533"],
          ["FIS1514","ICM1003","IEE1533"],["IIC1253","IIC2233","IIC2343","MAT1610"],["MAT1610","MAT1203","QIM100E"],
          ["IIC1103","IIC1001","MAT1107","MAT1207"]]

DELTA_DIAS = 2

SEC_COORDINADAS = [["ICS2123", "2", "3"], ["ICS3313", "2", "3"], ["ICS3413", "2", "3"]] #[["ICS3313","2","3"],["ICS3413","2","3"],["ICS2523","1","2"]]

CURSOS_3_IES = ["MAT1107_Coordinado - Macroseccion", "MAT1203_Coordinado - Macroseccion", "MAT1207_Coordinado - Macroseccion", "MAT1610_Coordinado - Macroseccion", "MAT1620_Coordinado - Macroseccion", "MAT1630_Coordinado - Macroseccion", "MAT1640_Coordinado - Macroseccion", "MAT251I_Coordinado - Macroseccion", "MAT253I_Coordinado - Macroseccion", "MAT255I_Coordinado - Macroseccion", "MAT2605_Coordinado - Macroseccion", "MAT380I_Coordinado - Macroseccion",
                "EYP1025_Coordinado - Macroseccion", "EYP1113_Coordinado - Macroseccion", "EYP2114_Coordinado - Macroseccion", "EYP211I_Coordinado - Macroseccion", "EYP230I_Coordinado - Macroseccion"]
#CURSOS_3_IES = ["MAT1640_Coordinado - Macroseccion","MAT1630_Coordinado - Macroseccion","MAT1620_Coordinado - Macroseccion","MAT1610_Coordinado - Macroseccion",
#                "MAT1203_Coordinado - Macroseccion","EYP1113_Coordinado - Macroseccion"]


#["EYP_MOD_MS1 - Macroseccion 1", "XN_MOD_MS1 - Macroseccion 1", "YF_MOD_MS1 - Macroseccion 1", "GCH_MOD_MS1 - Macroseccion 1", 
                #"ED_MOD_MS1 - Macroseccion 1", "WV_MOD_MS1 - Macroseccion 1"]

#Algunos parametros del modelo
DELTAMIN = 28
DELTAMAX = 63
VACANTES = 3000

SEMANA_LICENCIATURA = mapeo(PATH_PARAMETROS, "Fechas", "H1")

#siglas fmat, fis y qim hardcodeadas en filtracion_archivos modulos_mod_dipre

INCLUIR_MAT = True
INCLUIR_FIS_Y_QIM = False

IDENTIFICADORES_FMAT = ["MAT1107", "MAT1203", "MAT1207", "MAT1610", "MAT1620", "MAT1630", "MAT1640", "MAT251I", "MAT253I", "MAT255I", "MAT2605", "MAT380I",
                        "EYP1025", "EYP1113", "EYP2114", "EYP211I", "EYP230I"]

# IDENTIFICADORES_FMAT = ["EYP_MOD", "XN_MOD", "WV_MOD", "YF_MOD", "GCH_MOD", "ED_MOD"]

IDENTIFICADORES_FIS_Y_QIM = ["FIS1514", "FIS1523", "FIS1533", "QIM100E"]


FECHA_INICIO_CLASES = datetime(2024, 8, 5)
FECHA_FIN_CLASES = datetime(2024, 11, 29)

COMPATIBLES = [ ["MAT1610", "MAT1620", "EYP211I", "MAT253I", "MAT380I", "MAT1107"],
                ["MAT1203", "MAT255I"],
                ["EYP1113", "MAT251I"],
                ["EYP2114", "MAT1207", "MAT2605", "MAT1630"],
                ["EYP1025", "EYP230I"],
                ["EYP211I", "MAT253I", "MAT380I", "MAT1203"],
                ["MAT1610", "MAT1620", "MAT255I", "MAT1107"],
                ["EYP1113", "MAT251I"],
                ["EYP2114", "MAT1640", "MAT1207"],
                ["MAT1630", "MAT2605"]]
