import os
import sys
with open("resultados_rest_vacantes.txt", encoding="utf-8") as file:
    lineas = [x.strip() for x in file.readlines() if "y" not in x and "z" not in x]
    fechas_interrogaciones_result = {}

    for linea in lineas:
        # print(linea)
        # sys.exit()
        msg = linea.replace("[", "").replace("]", "").replace("x", "")
        # print(msg)
        msg = msg.split("=")[0]
        # print(msg)
        nombre_curso, dia, interrogacion = msg.split(",")

        if nombre_curso not in fechas_interrogaciones_result.keys():
            fechas_interrogaciones_result[nombre_curso] = int(dia)
        else:
            fechas_interrogaciones_result[nombre_curso] = [
                fechas_interrogaciones_result[nombre_curso], int(dia)]
        # print(nombre_curso, dia, interrogacion)

    contador = 0
    for key, value in fechas_interrogaciones_result.items():
        # print(key, value)
        try:
            dias = abs(value[1] - value[0])
            # print(f"La diferencia de días entre I1 e I2 para {key} es {dias}")
            condicion = 28 <= dias and dias <= 63
            if condicion == False:
                print(f"El ramo {key} no respeta el delta de días entre interrogaciones")
            contador += 1
        except TypeError:
            print(f"Ha ocurrido un error con {key, value}")

    print(contador)