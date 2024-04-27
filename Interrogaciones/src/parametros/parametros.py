import os
from datos.conversion_excel_parametros import fechas_prohibidas, excel_cursos_coordinados, mapeo_fechas, mapeo

PATH_LISTADO_NRC = os.path.join("excel_horarios",
                                 "Prueba_nrc.xlsx")
PATH_LISTADO_NRC_ORIGINAL = os.path.join("excel_horarios",
                                 "Listado_NRC_2023_Enero.xlsx")
PATH_VACANTES = os.path.join("instancia_datos", "vacantes.xlsx")
PATH_CONEXIONES = os.path.join("instancia_datos", "conexiones.xlsx")
PATH_CURSOS_IES = os.path.join(
        "excel_horarios", "Prueba_ies.xlsx")
PATH_CURSOS_IES_ORIGINAL = os.path.join(
        "excel_horarios", "004 - Listado_NRC_Programados.xlsx")
# PATH_CURSOS_IES = os.path.join(
#     "excel_horarios", "004-filtrado.xlsx")

PATH_MATERIAS = os.path.join("excel_horarios", "Listado_materias.xlsx")
PATH_LISTADO_CURSOS = os.path.join("instancia_datos", "listado_cursos.xlsx")

NUM_EXPERIMENTO = 2

# Ruta excel parametros
PATH_PARAMETROS = os.path.join("excel_horarios", "parametros.xlsx")

# Obtenemos las fechas prohibidas del excel
FECHAS_PROHIBIDAS = fechas_prohibidas(PATH_PARAMETROS, "Fechas")

# Obtenemos los cursos coordinados del excel
CURSOS_COORDINADOS = excel_cursos_coordinados(PATH_PARAMETROS, "Cursos Coordinados")

# Obtenemos las pruebas preasignadas (solo para cursos coordinados)
#Formato: si cursos todos coordinados: (curso (str), fecha (int), nr de prueba(int)) ¡La fecha debe ser en línea de tiempo real!
PRUEBAS_PREASIGNADAS = excel_cursos_coordinados(PATH_PARAMETROS, "Interrogaciones Fijas")

DIA_FECHA_RETIRO_CURSOS = mapeo_fechas(PATH_PARAMETROS, "Fechas", "D1")
DIA_I2 = mapeo_fechas(PATH_PARAMETROS, "Fechas", "F1")


GRUPOS = [["MAT1620","FIS1514","IIC1103"],["MAT1620","ICE1514","IIC1103"],["MAT1630","FIS1523","MAT1640"],["MAT1630","IIQ1003","MAT1640"],
          ["MAT1630","ICM1003","MAT1640"],["EYP1113","FIS1533","ICS1513"],["EYP1113","IEE1533","ICS1513"],["FIS1514","FIS1523","FIS1533"],
          ["FIS1514","IIQ1003","FIS1533"],["FIS1514","ICM1003","FIS1533"],["FIS1514","FIS1523","IEE1533"],["FIS1514","IIQ1003","IEE1533"],
          ["FIS1514","ICM1003","IEE1533"],["IIC1253","IIC2233","IIC2343","MAT1610"],["MAT1610","MAT1203","QIM100E"],
          ["IIC1103","IIC1001","MAT1107","MAT1207"]]

DELTA_DIAS = 2

SEC_COORDINADAS = [["ICS3313","2","3"],["ICS3413","2","3"],["ICS2523","1","2"]]

CURSOS_3_IES = ["MAT1640_Coordinado - Macroseccion","MAT1630_Coordinado - Macroseccion","MAT1620_Coordinado - Macroseccion","MAT1610_Coordinado - Macroseccion",
                "MAT1203_Coordinado - Macroseccion","EYP1113_Coordinado - Macroseccion"]
#["EYP_MOD_MS1 - Macroseccion 1", "XN_MOD_MS1 - Macroseccion 1", "YF_MOD_MS1 - Macroseccion 1", "GCH_MOD_MS1 - Macroseccion 1", 
                #"ED_MOD_MS1 - Macroseccion 1", "WV_MOD_MS1 - Macroseccion 1"]

#Algunos parametros del modelo
DELTAMIN = 28
DELTAMAX = 63
VACANTES = 2000

SEMANA_LICENCIATURA = mapeo(PATH_PARAMETROS, "Fechas", "H1")

#siglas fmat, fis y qim hardcodeadas en filtracion_archivos modulos_mod_dipre

INCLUIR_MAT = True
INCLUIR_FIS_Y_QIM = True

IDENTIFICADORES_FMAT = ["MAT1640", "MAT1630", "MAT1620", "MAT1610","MAT1207","EYP1113", "MAT1203"]
# IDENTIFICADORES_FMAT = ["EYP_MOD", "XN_MOD", "WV_MOD", "YF_MOD", "GCH_MOD", "ED_MOD"]

IDENTIFICADORES_FIS_Y_QIM = ["FIS1514", "FIS1523", "FIS1533", "QIM100E"]
