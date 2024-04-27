import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import os

def graficar_dias(mapeo_fechas, fechas_actualizado, title="Comb_fechas"):
    pruebas_ramo = dict()

    for iter_curso_1 in fechas_actualizado:
        curso_actual = iter_curso_1[0]

        for iter_curso_2 in fechas_actualizado:
            if curso_actual == iter_curso_2[0] and iter_curso_1[2] != iter_curso_2[2]:
                pruebas_ramo[curso_actual] = [iter_curso_2[1], iter_curso_1[1]]

                # Revisar aquí los cursos con más de 2 ies, porque se pueden sobreecribir

    combinaciones_fechas = list()
    for i in pruebas_ramo.values():
        if i not in combinaciones_fechas:
            combinaciones_fechas.append(i)

    fechas_dict = dict()

    for comb_fecha in combinaciones_fechas:
        contador = 0
        for key, value in pruebas_ramo.items():
            if value == comb_fecha:
                contador += 1

        fechas_dict[tuple(comb_fecha)] = contador

    eje_x = list()
    eje_y = list()

    for fecha_1, fecha_2 in fechas_dict.keys():

        for key, value in mapeo_fechas.items():
            if fecha_1 == value:
                eje_x.append(key)

            if fecha_2 == value:
                eje_y.append(key)

    ejes = list(mapeo_fechas.keys())
    etiquetas = list(mapeo_fechas.values())

    fig, ax = plt.subplots(figsize=(20, 20))

    ax.scatter(eje_x, eje_y)
    plt.xticks(ejes, etiquetas, rotation=60, fontsize=7)
    plt.yticks(ejes, etiquetas, fontsize=7)

    plt.xlabel("Fecha I1")
    plt.ylabel("Fecha I2")

    fig.savefig(f"{title}.pdf")


def graficar_dias_plotly(mapeo_fechas, fechas_actualizado, path, title="Comb_fechas"):
    pruebas_ramo = dict()

    for iter_curso_1 in fechas_actualizado:
        curso_actual = iter_curso_1[0]

        for iter_curso_2 in fechas_actualizado:
            if curso_actual == iter_curso_2[0] and iter_curso_1[2] != iter_curso_2[2]:
                pruebas_ramo[curso_actual] = [iter_curso_2[1], iter_curso_1[1]]

    combinaciones_fechas = list()
    for i in pruebas_ramo.values():
        if i not in combinaciones_fechas:
            combinaciones_fechas.append(i)

    fechas_dict = dict()

    for comb_fecha in combinaciones_fechas:
        contador = 0
        for key, value in pruebas_ramo.items():
            if value == comb_fecha:
                contador += 1

        fechas_dict[tuple(comb_fecha)] = contador

    eje_x = list()
    eje_y = list()

    for fecha_1, fecha_2 in fechas_dict.keys():
        for key, value in mapeo_fechas.items():
            if fecha_1 == value:
                eje_x.append(key)

            if fecha_2 == value:
                eje_y.append(key)
    ejes = list(mapeo_fechas.keys())

    etiquetas = list(mapeo_fechas.values())

    fig = px.scatter(x=eje_x, y=eje_y, labels={
                     'x': 'Fecha I1', 'y': 'Fecha I2'}, title=title)
    fig.update_xaxes(ticktext=etiquetas, tickvals=ejes,
                     tickangle=60, tickfont=dict(size=7))
    fig.update_yaxes(ticktext=etiquetas, tickvals=ejes, tickfont=dict(size=7))

    output_file = f"{title}.html"
    
    pio.write_html(fig, file=path, auto_open=False)
