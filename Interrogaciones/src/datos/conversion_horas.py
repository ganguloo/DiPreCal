import datetime


def conversion_timedelta(tiempo: datetime.timedelta):
    horas, segundos_restantes = divmod(tiempo.total_seconds(), 3600)
    minutos, segundos = divmod(segundos_restantes, 60)

    if horas < 10:
        horas = f"0{int(horas)}"
    else:
        horas = f"{int(horas)}"

    if int(minutos) == 0:
        minutos = f"0{int(minutos)}"
    else:
        minutos = f"{int(minutos)}"

    return horas, minutos
