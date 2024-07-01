from datetime import datetime, timedelta
from parametros.parametros import (FECHAS_PROHIBIDAS, FECHA_INICIO_CLASES, FECHA_FIN_CLASES)

def generacion_calendario(mes_inicial=8,
                          dia_inicial=5,
                          ano=2024,
                          dias_prohibidos=FECHAS_PROHIBIDAS,
                          fmat=False):
    fecha_calendario = datetime(ano, mes_inicial, dia_inicial)
    fechas = dict()
    fechas_validas = dict()
    mapeo_fechas = dict()

    cantidad_dias = (FECHA_FIN_CLASES - FECHA_INICIO_CLASES).days

    for indice in range(cantidad_dias):
        # si es False, considera los días viernes
        if fmat is False:
            if fecha_calendario.strftime("%d-%b") not in dias_prohibidos and fecha_calendario.weekday() not in [5,6]:
                dia = fecha_calendario.strftime("%d-%b")
                fechas[dia] = fecha_calendario
                fechas_validas[indice] = dia
        # si es true, no considera los días viernes      
        elif fmat is True:
            if fecha_calendario.strftime("%d-%b") not in dias_prohibidos and fecha_calendario.weekday() not in [4,5,6]:
                dia = fecha_calendario.strftime("%d-%b")
                fechas[dia] = fecha_calendario
                fechas_validas[indice] = dia
        mapeo_fechas[indice] = fecha_calendario.strftime("%d-%b")
        fecha_calendario += timedelta(days=1)

    return fechas_validas, mapeo_fechas, fechas
