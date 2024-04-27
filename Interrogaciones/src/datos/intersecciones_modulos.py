import datetime

from datos.conversion_horas import conversion_timedelta


def generacion_intersecciones_modulos(set_horarios, lista_horarios):
    """Lo que hace esta función, es que por ejempo, un curso si tiene horario de las 17:00 hasta
    la 21:20, separa sus modulos en 17:00 - 18:20, 18:30- 19:50, 20:00 - 21:20, permitiendo así que
    los ramos que ocupan más de un módulo de clase, tengan intersección con los ramos que no
    necesariamente tienen exactamente el mismo horario, si no que topan en algún momento.

    """

    for indice, (curso, modulo_cursos) in enumerate(lista_horarios):
        for modulo in modulo_cursos:

            separacion = modulo.split(":")
            if separacion[1].strip() == "" and separacion[2].strip() == "":
                continue

            hora_inicio, minutos_inicio = separacion[1].strip()[:2], separacion[1].strip()[
                2:]
            hora_fin, minutos_fin = separacion[2].strip()[:2], separacion[2].strip()[
                2:]

            tiempo_inicio = datetime.timedelta(hours=int(hora_inicio), minutes=int(minutos_inicio))
            tiempo_final = datetime.timedelta(hours=int(hora_fin), minutes=int(minutos_fin))

            duracion_minutos = ((tiempo_final - tiempo_inicio).seconds) / 60

            nuevos_intervalos = []
            if duracion_minutos > 80.0:
                tiempo_inicio_nuevo = tiempo_inicio
                nuevos_modulos = []
                while True:
                    if tiempo_inicio_nuevo >= tiempo_final:
                        break

                    tiempo_final_nuevo = tiempo_inicio_nuevo + \
                        datetime.timedelta(minutes=80)
                    nuevos_intervalos.append((tiempo_inicio_nuevo, tiempo_final_nuevo))

                    horas_inicio, minutos_inicio = conversion_timedelta(tiempo_inicio_nuevo)
                    horas_fin, minutos_fin = conversion_timedelta(tiempo_final_nuevo)

                    dia = separacion[0].strip()
                    new_module = f"{dia}:{horas_inicio}{minutos_inicio} : {horas_fin}{minutos_fin}"
                    nuevos_modulos.append(new_module)
                    set_horarios.add(new_module)
                    tiempo_inicio_nuevo = tiempo_final_nuevo + \
                        datetime.timedelta(minutes=10)

                nuevos_modulos += modulo_cursos
                lista_horarios[indice][1] = nuevos_modulos

